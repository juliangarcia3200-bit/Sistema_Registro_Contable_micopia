Imagina que eres parte del equipo de desarrollo de un Sistema de Registro Contable. Este sistema debe ayudar a registrar facturas, calcular nómina y determinar impuestos.
Como contadores-programadores, tu misión es aplicar el flujo de ramas en GitHub para organizar el trabajo como si fuera un proyecto real.

Instrucciones

Punto de partida

Clona el repositorio base entregado por el docente (contiene un archivo main.py con el mensaje:

print("Sistema contable versión estable")


Asegúrate de estar en la rama main.

Crear rama de desarrollo

Desde main, crea una rama llamada develop.

Todo el trabajo nuevo debe partir desde ahí.

Funciones contables (feature branches)

Cada grupo creará una rama feature para añadir una funcionalidad:

feature-facturas → registrar facturas y calcular el total.

feature-nomina → simular pagos de nómina.

feature-impuestos → calcular IVA de unas transacciones.

Modifica main.py agregando tu función, haz commit y merge a develop.

Corrección de errores (bugfix)

El docente introducirá un error en develop.

Crea una rama bugfix, corrige el error, haz commit y regresa la solución a develop.

Error en producción (hotfix)

Supón que en la rama main falta un mensaje obligatorio:

print("Reporte validado por auditor")


Corrige este error creando una rama hotfix, haz commit y merge a main.

Versión final (release)

Desde develop, crea una rama release.

Ajusta detalles menores (ejemplo: agregar un mensaje de versión print("Sistema contable v1.0")).

Haz merge de release tanto en main como en develop.