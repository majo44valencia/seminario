# Escáner Inteligente para Plantas de Vivero

Proyecto final del Seminario de Inteligencia Artificial Aplicada al Ciclo de Vida del Software (FET).

Estudiante: María José Valencia Ramírez

Con una foto tomada desde el celular, el escáner le dice al cliente del vivero qué planta tiene, qué le pasa y qué cuidado necesita. Un empleado puede corregir el resultado cuando el sistema se equivoca. El cliente no deja nombre, teléfono ni correo: solo la foto y, si quiere, unas observaciones.

## Funcionalidad de la semana 5

### Historia de usuario

**HU-09 (Must).** Como cliente, quiero usar el escáner sin dar mi nombre ni mi teléfono para que mis datos no queden en el vivero.

**Criterios de aceptación**

- **Escenario 1: solo se pide la foto.** Dado que abro el escáner, cuando reviso lo que me pide, entonces solo me pide la foto y un campo opcional de observaciones.
- **Escenario 2 (error): dato personal en observaciones.** Dado que escribo «soy Pedro y mi cel es 3000000000» en observaciones, cuando oprimo «Analizar», entonces veo «No escriba datos personales» y la foto no se envía hasta que lo borre.

Esta semana construí la parte que revisa el campo de observaciones antes de enviar la foto, que es la que hace cumplir el escenario 2.

### Contrato de la función

**Nombre y firma**

```python
def revisar_observaciones(texto: str | None) -> str
```

Archivo: `escaner/observaciones.py`

**Qué recibe**

El texto que el cliente escribió en el campo de observaciones (`str`). Como el campo es opcional, también puede llegar vacío o como `None`.

**Qué devuelve**

El texto listo para enviar junto con la foto (`str`), sin espacios al inicio ni al final. Si el campo llegó vacío, con solo espacios o como `None`, devuelve `""`. Si el texto trae un dato personal, no devuelve nada: lanza `ValueError` con el mensaje `"No escriba datos personales"`, y la foto no se envía.

**Supuestos y casos límite**

- Se considera dato personal un número de celular colombiano (10 dígitos que empiezan por 3), escrito junto, con espacios o con guiones, y con o sin el +57 adelante. También un correo electrónico (algo@algo.algo).
- Los números cortos no son datos personales: «la riego cada 3 días», «mide 30 cm» o el código de una planta como «PL-0007» se aceptan.
- Un número de 9 dígitos que empieza por 3 no es un celular y se acepta; con 10 dígitos ya se rechaza.
- `None`, `""` y un texto con solo espacios devuelven `""`.
- Un nombre suelto («soy Pedro») no se puede distinguir de forma segura del nombre de una planta, así que esta versión no lo detecta. Queda como pregunta para el cliente.

**Ejemplos (entrada → salida)**

| # | Entrada | Salida |
|---|---|---|
| 1 | `"  las hojas de abajo se pusieron amarillas  "` | `"las hojas de abajo se pusieron amarillas"` |
| 2 | `"la riego cada 3 días y mide 30 cm"` | `"la riego cada 3 días y mide 30 cm"` |
| 3 | `None` | `""` |
| 4 | `"soy Pedro y mi cel es 3000000000"` | `ValueError: No escriba datos personales` |
| 5 | `"escríbanme a pedro.gomez@correo.com"` | `ValueError: No escriba datos personales` |

### Cómo correr las pruebas

Se necesita Python 3.10 o superior. Desde la carpeta del proyecto:

```bash
pip install -r requirements.txt
pytest
```

Las pruebas están en `tests/test_observaciones.py`.

### Estructura

```
.
├── README.md
├── bitacora_ia.md
├── requirements.txt
├── escaner/
│   ├── __init__.py
│   └── observaciones.py
└── tests/
    └── test_observaciones.py
```
