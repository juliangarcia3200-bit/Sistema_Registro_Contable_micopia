print("Sistema de Registro Contable")

def datos():
    print("Ingrese los datos contables:")
    cuenta = input("Cuenta: ")
    descripcion = input("Descripción: ")
    monto = float(input("Monto: "))
    return cuenta, descripcion, monto