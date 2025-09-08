"""
Sistema de Registro Contable — versión optimizada
- Código modular, con tipado y validaciones.
- Manejo de dinero con Decimal para evitar errores de redondeo.
- Cálculo de facturas, renta (UVT Colombia 2024), utilidades de fechas y nómina.
- CLI con arguparse para ejecutar casos de uso o una demo integral.

Requisitos: pandas
"""
from __future__ import annotations

import argparse
import sys
import logging
from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Tuple

import pandas as pd

# =====================
# Metadatos de versión
# =====================
__VERSION__ = "2.0.0"  # <— incrementa para cada release

# =====================
# Configuración global
# =====================
LOG_FORMAT = "%(levelname)s | %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
log = logging.getLogger("contable")

# Dinero con Decimal
TWO_PLACES = Decimal("0.01")

# UVT y tabla 2024 (DIAN)
UVT_2024 = Decimal("47065")
TABLAS_UVT = [
    {"desde": 0,     "hasta": 1090,   "tarifa": Decimal("0.00"), "resta": 0,     "fijo": 0},
    {"desde": 1090,  "hasta": 1700,   "tarifa": Decimal("0.19"), "resta": 1090,  "fijo": 0},
    {"desde": 1700,  "hasta": 4100,   "tarifa": Decimal("0.28"), "resta": 1700,  "fijo": 116},
    {"desde": 4100,  "hasta": 8670,   "tarifa": Decimal("0.33"), "resta": 4100,  "fijo": 788},
    {"desde": 8670,  "hasta": 18970,  "tarifa": Decimal("0.35"), "resta": 8670,  "fijo": 2296},
    {"desde": 18970, "hasta": 31000,  "tarifa": Decimal("0.37"), "resta": 18970, "fijo": 5901},
    {"desde": 31000, "hasta": Decimal("Infinity"), "tarifa": Decimal("0.39"), "resta": 31000, "fijo": 10352},
]

# Parámetros de nómina
SMMLV = Decimal("1423500")
AUX_TRANSPORTE = Decimal("200000")
BASE_AUXILIO = SMMLV * 2


# ================
# Modelos y tipos
# ================
@dataclass(frozen=True)
class Product:
    nombre: str
    precio: Decimal
    cantidad: int

    @staticmethod
    def from_dict(d: Dict) -> "Product":
        return Product(
            nombre=str(d["nombre"]).strip(),
            precio=Decimal(str(d["precio"]) ),
            cantidad=int(d["cantidad"]),
        )


@dataclass(frozen=True)
class TaxInput:
    ingresos: Decimal
    incrngo: Decimal  # ingresos no constitutivos de renta/ganancia ocasional
    retefuente: Decimal
    dependientes: bool


# =====================
# Utilidades de dinero
# =====================

def money(x: Decimal) -> Decimal:
    """Redondea a 2 decimales con HALF_UP."""
    return x.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


# =====================
# Facturación
# =====================

def calcular_factura(productos: List[Product], tasa_iva: Decimal = Decimal("0.19")) -> Dict[str, Decimal]:
    if not (Decimal("0") <= tasa_iva <= Decimal("1")):
        raise ValueError("tasa_iva debe estar en [0,1]")

    subtotales = [p.precio * p.cantidad for p in productos]
    subtotal = sum(subtotales, start=Decimal("0"))
    iva = money(subtotal * tasa_iva)
    total = money(subtotal + iva)

    return {
        "subtotal": money(subtotal),
        "iva": iva,
        "total": total,
    }


# =====================
# Renta en UVT
# =====================

def impuesto_uvt(base_gravable_uvt: Decimal) -> Decimal:
    """Calcula el impuesto en UVT dado una base gravable expresada en UVT."""
    for rango in TABLAS_UVT:
        if Decimal(rango["desde"]) < base_gravable_uvt <= Decimal(rango["hasta"]):
            exceso = base_gravable_uvt - Decimal(rango["resta"])  # no trunques
            return money(exceso * Decimal(rango["tarifa"]) + Decimal(rango["fijo"]))
    return Decimal("0")


def calcular_renta(inp: TaxInput) -> Dict[str, Decimal]:
    if inp.ingresos < 0 or inp.incrngo < 0 or inp.retefuente < 0:
        raise ValueError("Valores negativos no permitidos en los insumos de renta")
    if inp.incrngo > inp.ingresos:
        raise ValueError("INCRNGO no puede superar los ingresos")

    ingresos_netos = inp.ingresos - inp.incrngo
    deduc_dep = money(Decimal("0.10") * ingresos_netos) if inp.dependientes else Decimal("0")
    renta_exenta = money(Decimal("0.25") * (ingresos_netos - deduc_dep))
    base_pesos = money(ingresos_netos - deduc_dep - renta_exenta)

    base_uvt = base_pesos / UVT_2024  # precisión Decimal, no truncar
    imp_en_uvt = impuesto_uvt(base_uvt)
    imp_pesos = money(imp_en_uvt * UVT_2024)

    saldo = money(imp_pesos - inp.retefuente)

    return {
        "ingresos_netos": money(ingresos_netos),
        "deduc_dep": deduc_dep,
        "renta_exenta": renta_exenta,
        "base_gravable_pesos": base_pesos,
        "base_gravable_uvt": money(base_uvt),  # representable
        "impuesto_pesos": imp_pesos,
        "saldo": saldo,
    }


# =====================
# Fechas
# =====================

def parse_date(texto: str) -> date:
    """Parses DD/MM/AAAA to date; lanza ValueError si no coincide."""
    try:
        return datetime.strptime(texto.strip(), "%d/%m/%Y").date()
    except Exception as e:
        raise ValueError(f"Fecha inválida: '{texto}' (esperado DD/MM/AAAA)") from e


# =====================
# Nómina
# =====================

def tabla_empleados(rows: List[Tuple[int, str, Decimal]]) -> pd.DataFrame:
    """Construye DataFrame vectorizado con Auxilio de Transporte.
    rows: lista de (Id, Nombre, Salario)
    """
    df = pd.DataFrame(rows, columns=["Id", "Nombre Empleado", "Salario"])
    # Vectorizado
    df["Auxilio Transporte"] = (df["Salario"] <= BASE_AUXILIO).astype(int) * int(AUX_TRANSPORTE)
    return df


# =====================
# CLI / Demos
# =====================

def demo_factura() -> None:
    productos = [
        Product("resma", Decimal("25000"), 2),
        Product("calculadora", Decimal("28000"), 3),
    ]
    totales = calcular_factura(productos)
    log.info("Factura — Subtotal: $%s | IVA: $%s | Total: $%s", *(f"{v:,.2f}" for v in totales.values()))


def demo_renta() -> None:
    inp = TaxInput(
        ingresos=Decimal("10000000"),
        incrngo=Decimal("2000000"),
        retefuente=Decimal("500000"),
        dependientes=True,
    )
    r = calcular_renta(inp)
    log.info(
        "Renta — Base: $%s (UVT %s) | Impuesto: $%s | Saldo: $%s",
        f"{r['base_gravable_pesos']:,.2f}", f"{r['base_gravable_uvt']:,.2f}", f"{r['impuesto_pesos']:,.2f}", f"{r['saldo']:,.2f}"
    )


def demo_nomina() -> None:
    df = tabla_empleados([
        (1, "Luis Efanier", Decimal("4000000")),
        (2, "Gustavo Adolfo", Decimal("3000000")),
        (3, "Darwin", Decimal("2000000")),
    ])
    print("\nTABLA DE EMPLEADOS\n", df.to_string(index=False))


def run_cli(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="Sistema de Registro Contable (optimizado)")
    sub = parser.add_subparsers(dest="cmd")

    # factura
    sub.add_parser("factura", help="Calcula una factura de ejemplo")

    # renta
    renta_p = sub.add_parser("renta", help="Calcula renta a partir de parámetros")
    renta_p.add_argument("--ingresos", type=str, required=False, default="10000000")
    renta_p.add_argument("--incrngo", type=str, required=False, default="2000000")
    renta_p.add_argument("--retefuente", type=str, required=False, default="500000")
    renta_p.add_argument("--dependientes", type=str, choices=["si", "no"], default="si")

    # nómina
    sub.add_parser("nomina", help="Construye y muestra la tabla de empleados")

    # demo integral
    parser.add_argument("--demo", action="store_true", help="Ejecuta todos los módulos con datos de ejemplo")

    args = parser.parse_args(argv)

    if args.demo:
        demo_factura()
        demo_renta()
        demo_nomina()
        return 0

    if args.cmd == "factura":
        demo_factura()
        return 0
    if args.cmd == "renta":
        inp = TaxInput(
            ingresos=Decimal(args.ingresos.replace("_", "")),
            incrngo=Decimal(args.incrngo.replace("_", "")),
            retefuente=Decimal(args.retefuente.replace("_", "")),
            dependientes=(args.dependientes == "si"),
        )
        r = calcular_renta(inp)
        print("\n--- Resultados ---")
        print(f"Ingresos netos:      ${r['ingresos_netos']:,.2f}")
        print(f"Deducción dep.:      ${r['deduc_dep']:,.2f}")
        print(f"Renta exenta (25%):  ${r['renta_exenta']:,.2f}")
        print(f"Base gravable:       ${r['base_gravable_pesos']:,.2f}  ({r['base_gravable_uvt']:,.2f} UVT)")
        print(f"Impuesto:            ${r['impuesto_pesos']:,.2f}")
        if r['saldo'] > 0:
            print(f"Saldo a pagar:       ${r['saldo']:,.2f}")
        elif r['saldo'] < 0:
            print(f"Saldo a favor:       ${(-r['saldo']):,.2f}")
        else:
            print("Sin saldo a pagar ni a favor.")
        return 0
    if args.cmd == "nomina":
        demo_nomina()
        return 0

    # Sin subcomando, muestra ayuda
    parser.print_help()
    return 0


if __name__ == "__main__":
    try:
        code = run_cli(sys.argv[1:])
        # no usar sys.exit aquí para evitar SystemExit en tests
        sys.exit(code)
    except SystemExit as se:
        # permitir exit con código específico en CLI real, ignorar en tests
        if se.code != 0:
            raise
    except Exception as exc:
        log.error("Error: %s", exc)
        sys.exit(1)
        print("hola")
        print("hola otra vez")
