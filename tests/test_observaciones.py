import pytest

from escaner.observaciones import revisar_observaciones

MENSAJE = "No escriba datos personales"


# Casos normales

def test_texto_normal_se_devuelve_sin_espacios_sobrantes():
    texto = "  las hojas de abajo se pusieron amarillas  "
    assert revisar_observaciones(texto) == "las hojas de abajo se pusieron amarillas"


def test_acepta_numeros_cortos_y_codigo_de_planta():
    texto = "la riego cada 3 días, mide 30 cm y es la PL-0007"
    assert revisar_observaciones(texto) == texto


# Casos límite

def test_campo_sin_llenar_devuelve_texto_vacio():
    assert revisar_observaciones(None) == ""


def test_texto_con_solo_espacios_devuelve_texto_vacio():
    assert revisar_observaciones("     ") == ""


def test_numero_de_9_digitos_no_es_celular_y_se_acepta():
    texto = "la compré con la factura 312345678"
    assert revisar_observaciones(texto) == texto


# Casos de error (escenario 2 de HU-09)

def test_rechaza_celular_escrito_junto():
    with pytest.raises(ValueError, match=MENSAJE):
        revisar_observaciones("soy Pedro y mi cel es 3000000000")


def test_rechaza_celular_con_espacios_y_prefijo():
    with pytest.raises(ValueError, match=MENSAJE):
        revisar_observaciones("llámenme al +57 300 123 4567")


def test_rechaza_correo_electronico():
    with pytest.raises(ValueError, match=MENSAJE):
        revisar_observaciones("escríbanme a pedro.gomez@correo.com")
