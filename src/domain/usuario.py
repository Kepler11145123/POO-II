from datetime import datetime
from typing import Optional

class Usuario:
    def __init__(self, username:str, email:str, nombre_completo: Optional[str] = None) -> None:
    
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

    @property
    def username(self) -> str:
        return self._username

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        if "@" not in valor or "." not in valor:
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