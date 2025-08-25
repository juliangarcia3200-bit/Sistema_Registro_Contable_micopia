import pandas as pd
print("Sistema de Registro Contable")

# facturación
def calcular_facturas(productos):
    subtotal = 0
    tasa_iva = 0.19

    # Calcular el subtotal de los productos
    for producto in productos:
        subtotal_producto = producto['precio'] * producto['cantidad']
        producto['subtotal'] = subtotal_producto
        subtotal += subtotal_producto

    iva = subtotal * tasa_iva
    total_factura = subtotal + iva
    return subtotal, iva, total_factura


# Ejemplo de uso
productos = [
    {'nombre': 'resma', 'precio': 25000, 'cantidad': 2},
    {'nombre': 'calculadora', 'precio': 28000,  'cantidad': 3},
]

subtotal, iva, total_factura = calcular_facturas(productos)
print(f"Subtotal: {subtotal:.2f}")
print(f"IVA: {iva:.2f}")
print(f"Total factura: {total_factura:.2f}")


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

    
    base_gravable_uvt = base_gravable_pesos // UVT_2024

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

renta = calcular_impuesto()


def datos():
    print("Ingrese los datos contables:")
    cuenta = input("Cuenta: ")
    descripcion = input("Descripción: ")
    monto = float(input("Monto: "))
    return cuenta, descripcion, monto

def fechas():
    print("Ingrese las fechas:")
    fecha_inicio = input("Fecha de inicio (DD/MM/AAAA): ")
    fecha_fin = input("Fecha de fin (DD/MM/AAAA): ")
    
    return fecha_inicio,fecha_fin #Se corrige el orden de las fechas

julian = datos()
print("Datos ingresados:", julian)

inicio, fin = fechas()
print("Rango de fechas:", inicio, "->", fin)


pd = "Pago diferido"

print("Sistema de Registro Contable")

# PARAMETROS DE NOMINA
Smmlv = float(1423500)
Aux_Tranporte = float(200000)
Base_Auxilio = Smmlv * 2

# TABLA DE EMPLEADOS
empleados = pd.DataFrame(columns=["Id", "Nombre Empleado", "Salario"])

def agregar_empleados(df, id, nombre, salario):
    nuevo_empleado = {
        "Id": id,
        "Nombre Empleado": nombre,
        "Salario": salario
    }
    df = pd.concat([df, pd.DataFrame([nuevo_empleado])], ignore_index=True)

    # CALCULO DE AUXILIO DE TRANSPORTE
    df["Auxilio Transporte"] = df["Salario"].apply(lambda x: Aux_Tranporte if x <= Base_Auxilio else 0)
    return df

empleados = agregar_empleados(empleados, 1, "Luis Efanier", 4000000)
empleados = agregar_empleados(empleados, 2, "Gustavo Adolfo", 3000000)
empleados = agregar_empleados(empleados, 3, "Darwin", 2000000)

print(empleados)

def mostrar_cliente():
    clientes = ["Ana", "Carlos", "María", "Jesus"]
    print("El cuarto cliente es:", clientes[3])

mostrar_cliente()

def aplicar_descuento():
    precio = 1000
    descuento = 0
    if descuento == 0:
        precio_final = precio
    else:
        precio_final = precio / descuento
    print("Precio final:", precio_final)

aplicar_descuento()

def calcular_balance():
    ingresos = 5000
    gastos = 3000
    balance = ingresos - gastos
    return print(balance)

calcular_balance()
