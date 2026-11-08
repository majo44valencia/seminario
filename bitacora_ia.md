# Bitácora de uso de IA

Proyecto: Escáner Inteligente para Plantas de Vivero
Estudiante: María José Valencia Ramírez
Funcionalidad: HU-09 Usar el escáner sin dejar datos personales (revisión del campo de observaciones)
Asistente usado: Claude (Anthropic), modo chat y agente

## Entradas

### Entrada 1

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:**

  > **Rol:** eres un desarrollador de Python con experiencia en desarrollo guiado por pruebas (TDD) y en protección de datos personales.
  >
  > **Contexto:** mi proyecto final es el «Escáner Inteligente para Plantas de Vivero». El cliente toma una foto de su planta y el sistema le dice qué planta es, qué le pasa y qué cuidado necesita. En la entrevista, el administrador del vivero fue claro en que no se guarden datos personales de los clientes (HU-09, prioridad Must). El cliente solo envía la foto y un campo opcional de observaciones. El criterio de error dice: si escribo «soy Pedro y mi cel es 3000000000» y oprimo «Analizar», debo ver «No escriba datos personales» y la foto no se envía.
  >
  > **Tarea:** antes de cualquier código, escribe:
  > 1. El contrato de una función que revise las observaciones, con este formato: nombre y firma con tipos, qué recibe, qué devuelve, supuestos y casos límite, y al menos 3 ejemplos de entrada → salida.
  > 2. Al menos 5 pruebas con pytest: 2 casos normales, 2 casos límite (campo vacío, `None`, un número que esté justo en el borde de parecer un celular) y al menos 1 caso de error que salga del criterio de aceptación.
  >
  > **Restricciones:** solo librería estándar de Python; los números cortos como «cada 3 días» o el código «PL-0007» no se deben rechazar; no escribas todavía la implementación.
  >
  > **Formato de respuesta:** primero el contrato en Markdown para pegarlo en el README, después el archivo `tests/test_observaciones.py` completo y al final una lista de los supuestos que tomaste y que yo debería confirmar con el cliente.

  El asistente propuso la función `revisar_observaciones(texto: str | None) -> str`, el contrato y 8 pruebas.
- **Decisión:** Aceptada
- **Por qué:** La función es pequeña, se puede probar sin la foto ni el servicio de visión y cumple directamente el escenario de error de la HU-09. Las pruebas cubren lo que pide la tarea: 2 normales, 3 de límite y 3 de error.
- **Verificación:** Revisé que cada prueba saliera del contrato o del criterio de aceptación. Corrí `pytest` con la función sin implementar y fallaron las 8, como debía ser.
- **Commit relacionado:** `75511c1` Pruebas de HU-09 revisar observaciones sin datos personales (en rojo)

### Entrada 2

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** «Implementa `revisar_observaciones` en `escaner/observaciones.py` cumpliendo el contrato del README y las pruebas de `tests/test_observaciones.py`». Para el celular, el asistente usó la expresión `\b3\d{9}\b`.
- **Decisión:** Aceptada con cambios
- **Por qué:** Esa expresión solo encuentra el celular cuando los 10 dígitos van pegados. La gente escribe el número como «300 123 4567» o con el +57 adelante, y así se colaba. Le pedí que antes de buscar quitara los espacios y guiones que quedan entre dos dígitos y que aceptara un 57 opcional adelante.
- **Verificación:** Con la primera versión pasaron 7 de 8 y falló `test_rechaza_celular_con_espacios_y_prefijo`. Después del cambio pasaron las 8. Además probé a mano que «cada 3 30 días» y «mide 3 metros» siguieran aceptándose y que «300-123-4567» se rechazara.
- **Commit relacionado:** `18924f1` Implementación de HU-09 con todas las pruebas en verde

### Entrada 3

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Para el correo, el asistente usó una expresión simple: `\S+@\S+\.\S+`.
- **Decisión:** Aceptada
- **Por qué:** Aquí no hay que validar si el correo existe ni si está bien escrito, solo notar que alguien está dejando un correo. Una expresión simple basta y se puede explicar en una línea.
- **Verificación:** Pasó `test_rechaza_correo_electronico` con «pedro.gomez@correo.com».
- **Commit relacionado:** `18924f1` Implementación de HU-09 con todas las pruebas en verde

### Entrada 4

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** El asistente planteó detectar también nombres, rechazando frases como «soy …» o «me llamo …».
- **Decisión:** Rechazada
- **Por qué:** Daría muchos falsos positivos: «soy nueva con las plantas» o «se llama lengua de suegra» quedarían bloqueados, y el cliente no podría enviar su foto. El criterio de aceptación ya se cumple con el celular del ejemplo. Lo dejé escrito como supuesto en el contrato y como pregunta para el administrador.
- **Verificación:** Revisé el escenario 2 de la HU-09: el ejemplo «soy Pedro y mi cel es 3000000000» se rechaza por el celular, y la prueba lo confirma.
- **Commit relacionado:** `18924f1` Implementación de HU-09 con todas las pruebas en verde

### Entrada 5

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** El asistente mencionó usar la librería `phonenumbers` para reconocer teléfonos de cualquier país.
- **Decisión:** Rechazada
- **Por qué:** El vivero atiende clientes de aquí y basta con el celular colombiano. Agregar una dependencia para eso hace más pesado el proyecto, y en el prompt pedí solo la librería estándar.
- **Verificación:** Las 8 pruebas pasan solo con `re`, que viene con Python. En `requirements.txt` solo está `pytest`.
- **Commit relacionado:** `18924f1` Implementación de HU-09 con todas las pruebas en verde

### Entrada 6

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** «Refactoriza `observaciones.py` para que se lea mejor, sin cambiar lo que hace y sin tocar las pruebas». El asistente compiló las expresiones con nombres (`CELULAR`, `CORREO`, `SEPARADOR_ENTRE_DIGITOS`), pasó el mensaje a la constante `MENSAJE_DATO_PERSONAL` y sacó la revisión a la función `tiene_dato_personal`.
- **Decisión:** Aceptada
- **Por qué:** La línea larga con dos expresiones era difícil de leer. Ahora cada patrón tiene un nombre y un comentario que dice qué busca, y `revisar_observaciones` se entiende de una leída.
- **Verificación:** Pasaron las 8 pruebas y `git diff --stat -- tests/` no mostró cambios en las pruebas.
- **Commit relacionado:** `2c7e29b` Refactor HU-09: patrones con nombre, mensaje en constante y función tiene_dato_personal

## Resumen

| Decisión | Cantidad |
|---|---|
| Aceptadas | 3 |
| Aceptadas con cambios | 1 |
| Rechazadas | 2 |

## Errores que atraparon las pruebas

En la primera versión, la prueba `test_rechaza_celular_con_espacios_y_prefijo` falló con el texto «llámenme al +57 300 123 4567». La función lo dejaba pasar porque buscaba los 10 dígitos pegados, y con espacios no los encontraba. Si eso hubiera llegado al vivero, el teléfono del cliente habría quedado guardado con la consulta, que es justo lo que la HU-09 quiere evitar. Lo corregí juntando primero los dígitos separados por espacio o guion, y buscando después el celular con un 57 opcional adelante.

## Reflexión final

Lo que más me sirvió del asistente fue escribir las expresiones regulares, que es lo que más me cuesta. Pero también fue donde más tuve que revisar. La primera versión parecía correcta y pasaba casi todo, y solo la prueba con espacios mostró que un número escrito como lo escribe la gente se colaba. Por eso valió la pena pensar las pruebas antes del código, y pensarlas desde cómo escribe un cliente real y no desde el ejemplo perfecto. También aprendí a decirle que no a sugerencias que sonaban completas, como detectar nombres, porque iban a bloquear a clientes que no estaban haciendo nada malo. En la próxima funcionalidad le pediría al asistente que me proponga casos raros desde el principio y confirmaría con el cliente los supuestos antes de programar.
