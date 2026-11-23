"""Configuración del archivo de logs (único archivo que usa el sistema)."""
import logging
import os

RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "eventos.log")


def obtener_logger(nombre: str = "software_fj") -> logging.Logger:
    """Devuelve un logger que escribe en logs/eventos.log y en consola."""
    logger = logging.getLogger(nombre)
    if logger.handlers:          # evita duplicar handlers
        return logger
    logger.setLevel(logging.DEBUG)
    os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)
    formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
    archivo = logging.FileHandler(RUTA_LOG, encoding="utf-8")
    archivo.setFormatter(formato)
    consola = logging.StreamHandler()
    consola.setLevel(logging.INFO)
    consola.setFormatter(logging.Formatter("%(levelname)-8s | %(message)s"))
    logger.addHandler(archivo)
    logger.addHandler(consola)
    return logger


log = obtener_logger()
