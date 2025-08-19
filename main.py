print("Sistema de Registro Contable")

def datos():
    print("Ingrese los datos contables:")
    cuenta = input("Cuenta: ")
    descripcion = input("Descripción: ")
    monto = float(input("Monto: "))
    return cuenta, descripcion, monto

def fechas():
    print("Ingrese las fechas:")
    fecha_inicio = input("Fecha de inicio (DD/MM/AAAA): ")
    fecha_fin = "Fecha de fin (DD/MM/AAAA): "
    return fecha_inicio, fecha_fin

julian = datos()
print("Datos ingresados:", julian)

import pandas as pd
print("Sistema de Registro Contable")



#PARAMETROS DE NOMINA
Smmlv = float(1423500)
Aux_Tranporte = float(200000)
Base_Auxilio = Smmlv * 2


#TABLA DE EMPLEADOS
empleados = pd.DataFrame(columns=["Id", "Nombre Empleado", "Salario"])

def agregar_empleados(df, id, nombre, salario):
    nuevo_empleado = {
        "Id": id,
        "Nombre Empleado": nombre,
        "Salario": salario
    } 

    df = pd.concat([df, pd.DataFrame([nuevo_empleado])], ignore_index=True)
    
    #CALCULO DE AUXILIO DE TRANSPORTE
    df["Auxilio Transporte"] = df["Salario"].apply(lambda x: Aux_Tranporte if x <= Base_Auxilio else 0)

    return df

empleados = agregar_empleados(empleados, 1, "Luis Efanier", 4000000)
empleados = agregar_empleados(empleados,2, "Gustavo Adolfo", 3000000)
empleados = agregar_empleados(empleados, 3, "Darwin", 2000000)

print(empleados)


