"""Gestor en memoria (listas internas) de clientes, servicios y reservas."""
from cliente import Cliente
from excepciones import ReservaInvalidaError, SoftwareFJError
from logger import log
from reserva import Reserva


class GestorFJ:
    def __init__(self):
        self.clientes, self.servicios, self.reservas = [], [], []

    def registrar_cliente(self, **datos):
        if any(c.documento == str(datos.get("documento")) for c in self.clientes):
            raise ReservaInvalidaError(f"Ya existe un cliente con documento {datos.get('documento')}")
        cliente = Cliente(**datos)
        self.clientes.append(cliente)
        log.info(f"Cliente registrado: {cliente.nombre}")
        return cliente

    def agregar_servicio(self, clase, **datos):
        servicio = clase(**datos)
        self.servicios.append(servicio)
        log.info(f"Servicio creado: {servicio.describir()}")
        return servicio

    def crear_reserva(self, cliente, servicio, duracion):
        try:
            reserva = Reserva(cliente, servicio, duracion)
        except TypeError as e:
            raise ReservaInvalidaError("Tipos de datos incorrectos al reservar") from e
        self.reservas.append(reserva)
        log.info(f"Reserva creada: {reserva.describir()}")
        return reserva

    def resumen(self):
        return (f"Clientes: {len(self.clientes)} | Servicios: {len(self.servicios)} | "
                f"Reservas: {len(self.reservas)}")
