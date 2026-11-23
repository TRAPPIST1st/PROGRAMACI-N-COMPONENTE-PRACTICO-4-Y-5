"""Clase Reserva: integra cliente, servicio, duración y estado."""
from entidad import Entidad
from excepciones import (CalculoInconsistenteError, OperacionNoPermitidaError,
                         ParametroFaltanteError, ReservaInvalidaError,
                         ServicioInvalidoError, ServicioNoDisponibleError)
from logger import log

PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA = "PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"


class Reserva(Entidad):

    def __init__(self, cliente=None, servicio=None, duracion=None):
        super().__init__()
        if cliente is None or servicio is None or duracion is None:
            raise ParametroFaltanteError("Una reserva requiere cliente, servicio y duración")
        try:
            servicio.validar_parametros(duracion)
        except ServicioInvalidoError as e:
            # Encadenamiento de excepciones
            raise ReservaInvalidaError("No se pudo crear la reserva: duración inválida") from e
        self._cliente, self._servicio, self._duracion = cliente, servicio, duracion
        self._estado = PENDIENTE
        self._costo = None

    @property
    def estado(self): return self._estado

    @property
    def costo(self): return self._costo

    def confirmar(self):
        """Confirma la reserva (try/except/else/finally)."""
        try:
            if self._estado != PENDIENTE:
                raise OperacionNoPermitidaError(f"Solo se confirman reservas PENDIENTES (estado actual: {self._estado})")
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(f"El servicio '{self._servicio.nombre}' no está disponible")
        except (OperacionNoPermitidaError, ServicioNoDisponibleError) as e:
            log.error(f"Reserva #{self.id} no confirmada: {e}")
            raise
        else:
            self._estado = CONFIRMADA
            log.info(f"Reserva #{self.id} CONFIRMADA")
        finally:
            log.debug(f"Intento de confirmación finalizado para reserva #{self.id}")

    def cancelar(self):
        try:
            if self._estado in (CANCELADA, PROCESADA):
                raise OperacionNoPermitidaError(f"No se puede cancelar una reserva {self._estado}")
        except OperacionNoPermitidaError as e:
            log.error(f"Reserva #{self.id} no cancelada: {e}")
            raise
        else:
            self._estado = CANCELADA
            log.info(f"Reserva #{self.id} CANCELADA")
        finally:
            log.debug(f"Intento de cancelación finalizado para reserva #{self.id}")

    def procesar(self, impuesto=0.19, descuento=0.0):
        """Calcula el costo final y marca la reserva como PROCESADA."""
        try:
            if self._estado != CONFIRMADA:
                raise OperacionNoPermitidaError(f"Solo se procesan reservas CONFIRMADAS (estado actual: {self._estado})")
            self._costo = self._servicio.calcular_costo(self._duracion, impuesto, descuento)
        except CalculoInconsistenteError as e:
            raise ReservaInvalidaError(f"Reserva #{self.id}: no se pudo calcular el costo") from e
        else:
            self._estado = PROCESADA
            log.info(f"Reserva #{self.id} PROCESADA - total ${self._costo:,.2f}")
            return self._costo
        finally:
            log.debug(f"Procesamiento finalizado para reserva #{self.id}")

    def describir(self):
        costo = f" | Total: ${self._costo:,.2f}" if self._costo else ""
        return (f"Reserva #{self.id} [{self._estado}] {self._cliente.nombre} -> "
                f"{self._servicio.nombre} ({self._duracion} {self._servicio.unidad}(s)){costo}")
