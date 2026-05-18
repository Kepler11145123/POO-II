"""create initial tables

Revision ID: 20260514_0001
Revises:
Create Date: 2026-05-14 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260514_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("nombre_completo", sa.String(length=100), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=True),
        sa.Column("password_hash", sa.String(length=255), nullable=True),
        sa.Column("rol", sa.String(length=20), nullable=True),
        sa.Column("fecha_registro", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "proyectos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=True),
        sa.Column("lider_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["lider_id"], ["usuarios.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tareas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("titulo", sa.String(length=200), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("estado", sa.String(length=20), nullable=True),
        sa.Column("prioridad", sa.String(length=10), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(), nullable=True),
        sa.Column("fecha_completada", sa.DateTime(), nullable=True),
        sa.Column("fecha_limite", sa.DateTime(), nullable=True),
        sa.Column("proyecto_id", sa.Integer(), nullable=False),
        sa.Column("asignado_a", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["asignado_a"], ["usuarios.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["proyecto_id"], ["proyectos.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("tareas")
    op.drop_table("proyectos")
    op.drop_table("usuarios")
