import pandas as pd 
print("Sistema de Registro Contable")   

#facturación   

def calcular_facturas(productos): 
    subtotal = 0
    tasa_iva = 0.19

    #Calcular el suntotal de los productos
    for producto in productos:
        subtotal_producto = producto['precio'] * producto['cantidad']
        producto['subtotal'] = subtotal_producto                                                        
        subtotal += subtotal_producto

iva = subtotal * tasa_iva

total_factura = subtotal + iva
       
    return subtotal, iva, total_factura


#Ejemplo de uso
productos = [
    {'nombre': 'resma', 'precio': ´25000´, 'cantidad': 2},        
    {'nombre': 'calculadora', 'precio': ´28000´,  'cantidad': 3},
]

susbtotal, iva, total_factura = calcular_facturas(productos)
print(f"Subtotal: {subtotal:.2f}")  
print(f"IVA: {iva:.2f}")
print(f"Total factura: {total_factura:.2f}")    
