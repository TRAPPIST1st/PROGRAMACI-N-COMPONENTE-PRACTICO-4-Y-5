"""Simulación de 12 operaciones de Software FJ (válidas e inválidas)."""
from cliente import Cliente
from excepciones import SoftwareFJError
from gestor import GestorFJ
from logger import log, RUTA_LOG
from servicios import AlquilerEquipo, AsesoriaEspecializada, SalaReuniones

gestor = GestorFJ()
resultados = {"ok": 0, "error": 0}


def ejecutar(numero, titulo, operacion):
    """Ejecuta una operación sin que un error detenga el programa."""
    print(f"\n--- Operación {numero}: {titulo} ---")
    try:
        resultado = operacion()
    except SoftwareFJError as e:
        resultados["error"] += 1
        causa = f" (causa: {e.__cause__})" if e.__cause__ else ""
        log.error(f"Op {numero} falló [{type(e).__name__}]: {e}{causa}")
    except Exception as e:          # errores inesperados: el sistema sigue activo
        resultados["error"] += 1
        log.critical(f"Op {numero} error inesperado [{type(e).__name__}]: {e}")
    else:
        resultados["ok"] += 1
        log.info(f"Op {numero} exitosa")
        return resultado
    finally:
        log.debug(f"Op {numero} finalizada")


def main():
    log.info("===== INICIO DE SIMULACIÓN SOFTWARE FJ =====")
    ana = ejecutar(1, "Cliente válido", lambda: gestor.registrar_cliente(
        nombre="Ana Torres", documento="1144050123", email="ana@correo.com", telefono="3101234567"))
    ejecutar(2, "Cliente con email inválido", lambda: gestor.registrar_cliente(
        nombre="Luis Pérez", documento="1000200300", email="luis-sin-arroba", telefono="3001112233"))
    ejecutar(3, "Cliente con parámetro faltante", lambda: gestor.registrar_cliente(
        nombre="Marta Ruiz", documento="9876543", email="marta@correo.com", telefono=None))
    carlos = ejecutar(4, "Segundo cliente válido", lambda: gestor.registrar_cliente(
        nombre="Carlos Gómez", documento="79854321", email="carlos@correo.com", telefono="3209876543"))

    sala = ejecutar(5, "Sala de reuniones válida", lambda: gestor.agregar_servicio(
        SalaReuniones, nombre="Sala Andes", tarifa_base=50000, capacidad=10))
    ejecutar(6, "Servicio con tarifa negativa", lambda: gestor.agregar_servicio(
        AlquilerEquipo, nombre="Portátil", tarifa_base=-5000, tipo_equipo="Laptop"))
    equipo = ejecutar(7, "Alquiler de equipo válido", lambda: gestor.agregar_servicio(
        AlquilerEquipo, nombre="Video Beam", tarifa_base=40000, tipo_equipo="Proyector"))
    asesoria = ejecutar(8, "Asesoría válida", lambda: gestor.agregar_servicio(
        AsesoriaEspecializada, nombre="Asesoría Python", tarifa_base=80000,
        especialidad="Programación", nivel="senior"))

    def reserva_exitosa():
        r = gestor.crear_reserva(ana, sala, 3)
        r.confirmar()
        r.procesar(impuesto=0.19, descuento=0.10)
        print(r.describir())
        return r
    reserva = ejecutar(9, "Reserva exitosa (sala 3 h, IVA y descuento)", reserva_exitosa)

    ejecutar(10, "Reserva con duración inválida (sala 20 h)", lambda: gestor.crear_reserva(ana, sala, 20))

    def reserva_no_disponible():
        equipo.disponible = False
        gestor.crear_reserva(carlos, equipo, 2).confirmar()
    ejecutar(11, "Reserva de servicio no disponible", reserva_no_disponible)

    def cancelar_y_reprocesar():
        r = gestor.crear_reserva(carlos, asesoria, 2)
        r.confirmar()
        r.cancelar()
        r.procesar()                # operación no permitida
    ejecutar(12, "Procesar una reserva cancelada", cancelar_y_reprocesar)

    ejecutar(13, "Cálculo inconsistente (descuento 150 %)",
             lambda: sala.calcular_costo(2, 0.19, 1.5))
    ejecutar(14, "Reserva sin cliente (parámetro faltante)",
             lambda: gestor.crear_reserva(None, sala, 2))

    print("\n========== RESUMEN ==========")
    print(gestor.resumen())
    print(f"Operaciones exitosas: {resultados['ok']} | con error controlado: {resultados['error']}")
    for r in gestor.reservas:
        print(" ", r.describir())
    print(f"Log completo en: {RUTA_LOG}")
    log.info("===== FIN DE SIMULACIÓN =====")


if __name__ == "__main__":
    main()
