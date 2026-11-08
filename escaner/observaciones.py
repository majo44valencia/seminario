"""HU-09: revisa las observaciones del cliente antes de enviar la foto."""
import re

MENSAJE_DATO_PERSONAL = "No escriba datos personales"

# Espacio o guion que queda entre dos dígitos: "300 123-4567" -> "3001234567"
SEPARADOR_ENTRE_DIGITOS = re.compile(r"(?<=\d)[ -](?=\d)")
# Celular colombiano: 10 dígitos que empiezan por 3, con o sin 57 adelante
CELULAR = re.compile(r"(?<!\d)(57)?3\d{9}(?!\d)")
# Correo: algo@algo.algo
CORREO = re.compile(r"\S+@\S+\.\S+")


def tiene_dato_personal(texto: str) -> bool:
    numeros_juntos = SEPARADOR_ENTRE_DIGITOS.sub("", texto)
    return bool(CELULAR.search(numeros_juntos) or CORREO.search(texto))


def revisar_observaciones(texto: str | None) -> str:
    if texto is None:
        return ""
    texto = texto.strip()
    if tiene_dato_personal(texto):
        raise ValueError(MENSAJE_DATO_PERSONAL)
    return texto
