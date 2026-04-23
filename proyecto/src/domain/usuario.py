import hashlib
from datetime import datetime
from typing import Optional

def hashear(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()  # corregido encodne -> encode

class Usuario:
    def __init__(self, username: str, email: str, nombre_completo: Optional[str] = None, password: Optional[str] = None, password_hash: Optional[str] = None) -> None:
        if len(username) < 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres.")
        if not username.isalnum():
            raise ValueError("Username solo puede contener letras y números.")

        self._username = username
        self._email = None
        self.email = email
        self._nombre_completo = nombre_completo
        self._activo = True
        self.fecha_registro = datetime.now()

        if password:
            self._password_hash = hashear(password)  # corregido == -> =
        elif password_hash:
            self._password_hash = password_hash
        else:
            self._password_hash = None

    def verificar_password(self, password: str) -> bool:  # corregido nombre del método
        return self._password_hash == hashear(password)

    def to_dict(self) -> dict:
        return {
            "username": self._username,
            "email": self._email,
            "nombre_completo": self._nombre_completo,
            "activo": self._activo,
            "password_hash": self._password_hash,
            "fecha_registro": self.fecha_registro.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Usuario":
        u = cls(
            username=data["username"],
            email=data["email"],
            nombre_completo=data.get("nombre_completo"),
            password_hash=data.get("password_hash")
        )
        u._activo = data.get("activo", True)
        u.fecha_registro = datetime.fromisoformat(data["fecha_registro"])
        return u

    @property
    def username(self) -> str:
        return self._username

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        partes = valor.split("@")
        if len(partes) != 2 or not partes[0] or "." not in partes[1] or not partes[1].split(".")[-1]:
            raise ValueError(f"Email inválido: {valor}")
        self._email = valor

    def activar(self) -> None:
        self._activo = True

    def desactivar(self) -> None:
        self._activo = False

    def __str__(self) -> str:
        return f"@{self.username}"

    def __repr__(self) -> str:
        return f"Usuario('{self.username}', '{self.email}')"