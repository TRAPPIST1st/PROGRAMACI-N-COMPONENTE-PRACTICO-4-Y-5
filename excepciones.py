"""Excepciones personalizadas de Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base de la que heredan todos los errores del sistema."""


class ClienteInvalidoError(SoftwareFJError):
    """Datos de cliente inválidos (nombre, correo, teléfono, documento)."""


class ParametroFaltanteError(SoftwareFJError):
    """Falta un parámetro obligatorio."""


class ServicioInvalidoError(SoftwareFJError):
    """Parámetros inválidos al crear o usar un servicio."""


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio solicitado no está disponible."""


class ReservaInvalidaError(SoftwareFJError):
    """Intento de reserva incorrecto."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Operación no permitida para el estado actual de la reserva."""


class CalculoInconsistenteError(SoftwareFJError):
    """Cálculo de costos con resultados o parámetros inconsistentes."""
