from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client

from app.database import get_supabase
from app.models.cliente import ClienteCreate, ClienteUpdate
from app.services import execute_query, reject_null_fields, require_one, response_row


router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente: ClienteCreate, client: Client = Depends(get_supabase)):
    response = execute_query(
        client.table("clientes").insert(cliente.model_dump(mode="json")),
        "al crear el cliente",
    )
    return {"mensaje": "Cliente creado correctamente", "cliente": response_row(response, "el cliente")}


@router.get("")
def obtener_clientes(client: Client = Depends(get_supabase)):
    response = execute_query(
        client.table("clientes").select("*").order("id_cliente"),
        "al consultar los clientes",
    )
    return {"cantidad": len(response.data), "clientes": response.data}


@router.get("/{id_cliente}")
def obtener_cliente(id_cliente: int, client: Client = Depends(get_supabase)):
    row = require_one(client, "clientes", "id_cliente", id_cliente, "Cliente")
    return {"cliente": row}


@router.patch("/{id_cliente}")
def actualizar_cliente(
    id_cliente: int,
    cliente: ClienteUpdate,
    client: Client = Depends(get_supabase),
):
    existing = require_one(client, "clientes", "id_cliente", id_cliente, "Cliente")
    data = cliente.model_dump(mode="json", exclude_unset=True)
    reject_null_fields(data, {"identificacion", "nombre", "apellido", "email"})
    if not data:
        return {"mensaje": "Cliente sin cambios", "cliente": existing}
    response = execute_query(
        client.table("clientes").update(data).eq("id_cliente", id_cliente),
        "al actualizar el cliente",
    )
    return {
        "mensaje": "Cliente actualizado correctamente",
        "cliente": response_row(response, "el cliente"),
    }


@router.delete("/{id_cliente}")
def eliminar_cliente(id_cliente: int, client: Client = Depends(get_supabase)):
    require_one(client, "clientes", "id_cliente", id_cliente, "Cliente")
    sales = execute_query(
        client.table("ventas").select("id_venta").eq("id_cliente", id_cliente).limit(1),
        "al verificar las ventas del cliente",
    )
    if sales.data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El cliente tiene ventas asociadas",
        )
    response = execute_query(
        client.table("clientes").delete().eq("id_cliente", id_cliente),
        "al eliminar el cliente",
    )
    return {"mensaje": "Cliente eliminado correctamente", "cliente": response_row(response, "el cliente")}
