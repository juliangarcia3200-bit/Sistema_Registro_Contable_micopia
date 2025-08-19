print("Sistema de Registro Contable")


UVT_2024 = 47065  # pesos

TABLAS_UVT = [
    {"desde": 0,     "hasta": 1090,   "tarifa": 0.00, "resta": 0,     "fijo": 0},
    {"desde": 1090,  "hasta": 1700,   "tarifa": 0.19, "resta": 1090,  "fijo": 0},
    {"desde": 1700,  "hasta": 4100,   "tarifa": 0.28, "resta": 1700,  "fijo": 116},
    {"desde": 4100,  "hasta": 8670,   "tarifa": 0.33, "resta": 4100,  "fijo": 788},
    {"desde": 8670,  "hasta": 18970,  "tarifa": 0.35, "resta": 8670,  "fijo": 2296},
    {"desde": 18970, "hasta": 31000,  "tarifa": 0.37, "resta": 18970, "fijo": 5901},
    {"desde": 31000, "hasta": float("inf"), "tarifa": 0.39, "resta": 31000, "fijo": 10352},
]

def impuesto_uvt(base_gravable_uvt: float) -> float:
    for rango in TABLAS_UVT:
        if rango["desde"] < base_gravable_uvt <= rango["hasta"]:
            return (base_gravable_uvt - rango["resta"]) * rango["tarifa"] + rango["fijo"]
    return 0.0

def calcular_impuesto():
    print("Cálculo Renta año Gravable 2024")
    ingresos = float(input("Ingresos (en pesos): "))
    incrngo  = float(input("INCRNGO (en pesos): "))
    retefuente = float(input("Retención en la fuente (en pesos): "))
    dependientes = input("¿Tiene dependientes? (si/no): ").strip().lower()

    ingresos_netos = ingresos - incrngo
    deduc_dep = 0.10 * ingresos_netos if dependientes == "si" else 0.0
    renta_exenta = 0.25 * (ingresos_netos - deduc_dep)
    base_gravable_pesos = ingresos_netos - deduc_dep - renta_exenta
    base_gravable_uvt = base_gravable_pesos / UVT_2024

    imp_uvt = impuesto_uvt(base_gravable_uvt)
    imp_pesos = imp_uvt * UVT_2024
    saldo = imp_pesos - retefuente

    print("\n--- Resultados ---")
    print(f"Ingresos netos:      ${ingresos_netos:,.2f}")
    print(f"Deducción dep.:      ${deduc_dep:,.2f}")
    print(f"Renta exenta (25%):  ${renta_exenta:,.2f}")
    print(f"Base gravable:       ${base_gravable_pesos:,.2f}  ({base_gravable_uvt:,.2f} UVT)")
    print(f"Impuesto:            ${imp_pesos:,.2f}")
    print(f"Retención fuente:    ${retefuente:,.2f}")

    if saldo > 0:
        print(f"Saldo a pagar:       ${saldo:,.2f}")
    elif saldo < 0:
        print(f"Saldo a favor:       ${-saldo:,.2f}")
    else:
        print("Sin saldo a pagar ni a favor.")