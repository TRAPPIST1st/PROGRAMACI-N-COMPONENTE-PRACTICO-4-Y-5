"""Clase Cliente con encapsulación y validaciones estrictas."""
import re

from entidad import Entidad
from excepciones import ClienteInvalidoError, ParametroFaltanteError

_RE_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]{3,60}$")
_RE_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")
_RE_TEL = re.compile(r"^\d{7,10}$")
_RE_DOC = re.compile(r"^\d{6,12}$")


class Cliente(Entidad):
    """Cliente de Software FJ. Los datos personales son privados."""

    def __init__(self, nombre=None, documento=None, email=None, telefono=None):
        super().__init__()
        for etiqueta, valor in (("nombre", nombre), ("documento", documento),
                                ("email", email), ("telefono", telefono)):
            if valor is None or str(valor).strip() == "":
                raise ParametroFaltanteError(f"Falta el parámetro obligatorio: {etiqueta}")
        self.__nombre = self._validar(_RE_NOMBRE, nombre, "nombre")
        self.__documento = self._validar(_RE_DOC, documento, "documento")
        self.__email = self._validar(_RE_EMAIL, email, "email")
        self.__telefono = self._validar(_RE_TEL, telefono, "telefono")

    @staticmethod
    def _validar(patron, valor, campo):
        if not isinstance(valor, str):
            raise ClienteInvalidoError(f"El campo '{campo}' debe ser texto, se recibió {type(valor).__name__}")
        valor = valor.strip()
        if not patron.match(valor):
            raise ClienteInvalidoError(f"Valor inválido para '{campo}': '{valor}'")
        return valor

    # Solo lectura para el documento; los demás se pueden actualizar con validación
    @property
    def nombre(self): return self.__nombre

    @property
    def documento(self): return self.__documento

    @property
    def email(self): return self.__email

    @email.setter
    def email(self, valor): self.__email = self._validar(_RE_EMAIL, valor, "email")

    @property
    def telefono(self): return self.__telefono

    @telefono.setter
    def telefono(self, valor): self.__telefono = self._validar(_RE_TEL, valor, "telefono")

    def describir(self) -> str:
        return f"Cliente #{self.id}: {self.__nombre} | Doc: {self.__documento} | {self.__email} | Tel: {self.__telefono}"
