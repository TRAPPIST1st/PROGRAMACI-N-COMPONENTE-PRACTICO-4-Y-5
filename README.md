# Software FJ - Sistema de Gestión de Clientes, Servicios y Reservas
Curso Programación (213023) - UNAD. Python 3.8+, sin bases de datos ni librerías externas.

Ejecutar: `python main.py`  ->  genera `logs/eventos.log`

| Archivo | Contenido |
|---|---|
| entidad.py | Clase abstracta `Entidad` |
| cliente.py | `Cliente` (encapsulación + validaciones) |
| servicios.py | `Servicio` (abstracta), `SalaReuniones`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| reserva.py | `Reserva` (confirmar, cancelar, procesar) |
| gestor.py | Listas en memoria |
| excepciones.py | Excepciones personalizadas |
| logger.py | Configuración del log |
| main.py | Simulación de 14 operaciones |

Conceptos: abstracción, herencia, polimorfismo, encapsulación, sobrecarga (`calcular_costo` con
parámetros opcionales), try/except/else/finally y encadenamiento (`raise ... from ...`).
