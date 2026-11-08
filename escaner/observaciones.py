# HU-09: revisa las observaciones del cliente antes de enviar la foto
import re


def revisar_observaciones(texto):
    if texto is None:
        return ""
    texto = texto.strip()
    solo_numeros_juntos = re.sub(r"(?<=\d)[ -](?=\d)", "", texto)
    if re.search(r"(?<!\d)(57)?3\d{9}(?!\d)", solo_numeros_juntos) or re.search(r"\S+@\S+\.\S+", texto):
        raise ValueError("No escriba datos personales")
    return texto
