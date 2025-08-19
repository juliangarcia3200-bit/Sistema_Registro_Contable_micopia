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
