from typing import Any, Dict

from fastapi import APIRouter, Depends, status
from supabase import Client

from app.database import get_supabase
from app.models.usuario import UsuarioCreate, UsuarioUpdate
from app.security import hash_password
from app.services import execute_query, require_one


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
PUBLIC_COLUMNS = "id_usuario,username,nombre,rol,activo,fecha_creacion"


def public_user(row: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in row.items() if key != "password_hash"}


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_usuario(
    usuario: UsuarioCreate,
    client: Client = Depends(get_supabase),
):
    data = usuario.model_dump(mode="json", exclude={"password"})
    data["password_hash"] = hash_password(usuario.password)
    response = execute_query(
        client.table("usuarios").insert(data),
        "al crear el usuario",
    )
    return {
        "mensaje": "Usuario creado correctamente",
        "usuario": public_user(response.data[0]),
    }


@router.get("")
def obtener_usuarios(client: Client = Depends(get_supabase)):
    response = execute_query(
        client.table("usuarios").select(PUBLIC_COLUMNS).order("id_usuario"),
        "al consultar los usuarios",
    )
    return {"cantidad": len(response.data), "usuarios": response.data}


@router.get("/{id_usuario}")
def obtener_usuario(id_usuario: int, client: Client = Depends(get_supabase)):
    row = require_one(client, "usuarios", "id_usuario", id_usuario, "Usuario")
    return {"usuario": public_user(row)}


@router.patch("/{id_usuario}")
def actualizar_usuario(
    id_usuario: int,
    usuario: UsuarioUpdate,
    client: Client = Depends(get_supabase),
):
    existing = require_one(client, "usuarios", "id_usuario", id_usuario, "Usuario")
    data = usuario.model_dump(mode="json", exclude_unset=True, exclude={"password"})
    if usuario.password is not None:
        data["password_hash"] = hash_password(usuario.password)
    if not data:
        return {"mensaje": "Usuario sin cambios", "usuario": public_user(existing)}
    response = execute_query(
        client.table("usuarios").update(data).eq("id_usuario", id_usuario),
        "al actualizar el usuario",
    )
    return {
        "mensaje": "Usuario actualizado correctamente",
        "usuario": public_user(response.data[0]),
    }


@router.delete("/{id_usuario}")
def eliminar_usuario(id_usuario: int, client: Client = Depends(get_supabase)):
    require_one(client, "usuarios", "id_usuario", id_usuario, "Usuario")
    response = execute_query(
        client.table("usuarios").update({"activo": False}).eq("id_usuario", id_usuario),
        "al desactivar el usuario",
    )
    return {
        "mensaje": "Usuario desactivado correctamente",
        "usuario": public_user(response.data[0]),
    }
