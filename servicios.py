"""Servicio (abstracta) y servicios especializados con polimorfismo."""
from abc import abstractmethod

from entidad import Entidad
from excepciones import (CalculoInconsistenteError, ParametroFaltanteError,
                         ServicioInvalidoError)


class Servicio(Entidad):
    """Clase abstracta de la que heredan todos los servicios."""

    unidad = "hora"

    def __init__(self, nombre=None, tarifa_base=None):
        super().__init__()
        if not nombre or not str(nombre).strip():
            raise ParametroFaltanteError("El servicio requiere un nombre")
        if tarifa_base is None:
            raise ParametroFaltanteError("El servicio requiere una tarifa base")
        if not isinstance(tarifa_base, (int, float)) or isinstance(tarifa_base, bool) or tarifa_base <= 0:
            raise ServicioInvalidoError(f"Tarifa base inválida: {tarifa_base!r}")
        self._nombre = str(nombre).strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = True

    @property
    def nombre(self): return self._nombre

    @property
    def disponible(self): return self._disponible

    @disponible.setter
    def disponible(self, valor: bool): self._disponible = bool(valor)

    # ---- métodos abstractos (polimorfismo) ----
    @abstractmethod
    def costo_base(self, duracion: float) -> float:
        """Costo sin impuestos ni descuentos."""

    @abstractmethod
    def validar_parametros(self, duracion: float) -> None:
        """Lanza ServicioInvalidoError si la duración no es válida."""

    @abstractmethod
    def describir(self) -> str: ...

    # ---- método sobrecargado (parámetros opcionales) ----
    def calcular_costo(self, duracion, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """Variantes:
        calcular_costo(d)                  -> costo base
        calcular_costo(d, 0.19)            -> con impuesto (IVA)
        calcular_costo(d, 0.19, 0.10)      -> con impuesto y descuento
        calcular_costo(d, descuento=0.10)  -> solo descuento
        """
        self.validar_parametros(duracion)
        if not 0 <= impuesto <= 1:
            raise CalculoInconsistenteError(f"Impuesto fuera de rango [0,1]: {impuesto}")
        if not 0 <= descuento < 1:
            raise CalculoInconsistenteError(f"Descuento fuera de rango [0,1): {descuento}")
        total = self.costo_base(duracion) * (1 - descuento) * (1 + impuesto)
        if total <= 0:
            raise CalculoInconsistenteError(f"Costo calculado inconsistente: {total}")
        return round(total, 2)


class SalaReuniones(Servicio):
    """Reserva de salas (por hora)."""

    unidad = "hora"

    def __init__(self, nombre=None, tarifa_base=None, capacidad=None):
        super().__init__(nombre, tarifa_base)
        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad de sala inválida: {capacidad!r}")
        self._capacidad = capacidad

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or not 1 <= duracion <= 12:
            raise ServicioInvalidoError(f"Una sala se reserva entre 1 y 12 horas (recibido: {duracion!r})")

    def costo_base(self, duracion):
        return self._tarifa_base * duracion

    def describir(self):
        return f"Sala '{self._nombre}' (capacidad {self._capacidad}) - ${self._tarifa_base:,.0f}/hora"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos (por día, con seguro fijo)."""

    unidad = "día"
    SEGURO = 15000.0

    def __init__(self, nombre=None, tarifa_base=None, tipo_equipo=None):
        super().__init__(nombre, tarifa_base)
        if not tipo_equipo or not str(tipo_equipo).strip():
            raise ParametroFaltanteError("Falta el tipo de equipo")
        self._tipo_equipo = str(tipo_equipo).strip()

    def validar_parametros(self, duracion):
        if not isinstance(duracion, int) or isinstance(duracion, bool) or not 1 <= duracion <= 30:
            raise ServicioInvalidoError(f"El alquiler es de 1 a 30 días enteros (recibido: {duracion!r})")

    def costo_base(self, duracion):
        return self._tarifa_base * duracion + self.SEGURO

    def describir(self):
        return f"Equipo '{self._nombre}' ({self._tipo_equipo}) - ${self._tarifa_base:,.0f}/día + seguro"


class AsesoriaEspecializada(Servicio):
    """Asesorías (por hora, con recargo según nivel del asesor)."""

    unidad = "hora"
    RECARGOS = {"junior": 1.0, "senior": 1.35, "experto": 1.6}

    def __init__(self, nombre=None, tarifa_base=None, especialidad=None, nivel="junior"):
        super().__init__(nombre, tarifa_base)
        if not especialidad or not str(especialidad).strip():
            raise ParametroFaltanteError("Falta la especialidad de la asesoría")
        if nivel not in self.RECARGOS:
            raise ServicioInvalidoError(f"Nivel de asesor inválido: {nivel!r}")
        self._especialidad = str(especialidad).strip()
        self._nivel = nivel

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or not 0.5 <= duracion <= 8:
            raise ServicioInvalidoError(f"Una asesoría dura entre 0.5 y 8 horas (recibido: {duracion!r})")

    def costo_base(self, duracion):
        return self._tarifa_base * self.RECARGOS[self._nivel] * duracion

    def describir(self):
        return f"Asesoría '{self._nombre}' de {self._especialidad} (nivel {self._nivel}) - ${self._tarifa_base:,.0f}/hora"
