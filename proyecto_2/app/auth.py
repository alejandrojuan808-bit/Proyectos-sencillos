import hashlib

from .storage import load_users, save_users


class AuthError(Exception):
    """Error base para autenticación."""


class UserAlreadyExistsError(AuthError):
    """Se lanza cuando el usuario ya existe."""


class InvalidCredentialsError(AuthError):
    """Se lanza cuando las credenciales no son válidas."""


def hash_password(password: str) -> str:
    """Genera un hash seguro de la contraseña."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_user(username: str, password: str) -> dict:
    """Registra un usuario nuevo si no existe."""
    username = username.strip()
    password = password.strip()

    if not username or not password:
        raise ValueError("Usuario y contraseña no pueden estar vacíos.")

    users = load_users()
    if username in users:
        raise UserAlreadyExistsError(f"El usuario '{username}' ya existe.")

    users[username] = {
        "username": username,
        "password_hash": hash_password(password),
    }
    save_users(users)
    return {"username": username, "message": "Usuario registrado correctamente."}


def login_user(username: str, password: str) -> dict:
    """Verifica si las credenciales del usuario son válidas."""
    username = username.strip()
    password = password.strip()

    if not username or not password:
        raise ValueError("Usuario y contraseña son obligatorios.")

    users = load_users()
    user = users.get(username)
    if not user:
        raise InvalidCredentialsError("Usuario o contraseña incorrectos.")

    stored_hash = user.get("password_hash")
    if hash_password(password) != stored_hash:
        raise InvalidCredentialsError("Usuario o contraseña incorrectos.")

    return {"username": username, "message": "Inicio de sesión correcto."}
