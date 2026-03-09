"""File utilities"""
import hashlib

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_SIZE = 5 * 1024 * 1024  # 5MB


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def hash_file(file_bytes: bytes) -> str:
    """SHA-256 de los bytes de la imagen — sirve como nombre único y para comparar."""
    return hashlib.sha256(file_bytes).hexdigest()


def get_extension(filename: str) -> str:
    """Obtiene la extension de cualquier tipo que sea"""
    return filename.rsplit(".", 1)[1].lower()


def build_file_path(file_bytes: bytes, filename: str) -> str:
    """Construye el path: <sha256>.<ext>"""
    return f"{hash_file(file_bytes)}.{get_extension(filename)}"
