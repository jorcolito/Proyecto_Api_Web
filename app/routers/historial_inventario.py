from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from supabase import Client

from app.database import get_supabase
from app.models.historial_inventario import MovimientoInventarioCreate, TipoMovimiento
from app.services import execute_query, require_one, rpc_row


router = APIRouter(
    prefix="/historial-inventario",
    tags=["Historial de inventario"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
def registrar_movimiento(
    movimiento: MovimientoInventarioCreate,
    client: Client = Depends(get_supabase),
):
    params = {
        "p_id_producto": movimiento.id_producto,
        "p_id_usuario": movimiento.id_usuario,
        "p_tipo_movimiento": movimiento.tipo_movimiento.value,
        "p_cantidad": movimiento.cantidad,
        "p_motivo": movimiento.motivo,
    }
    response = execute_query(
        client.rpc("registrar_movimiento_inventario", params),
        "al registrar el movimiento de inventario",
    )
    return {
        "mensaje": "Movimiento de inventario registrado correctamente",
        "movimiento": rpc_row(response, "el movimiento de inventario"),
    }


@router.get("")
def obtener_historial(
    id_producto: Optional[int] = Query(default=None, gt=0),
    id_usuario: Optional[int] = Query(default=None, gt=0),
    tipo_movimiento: Optional[TipoMovimiento] = None,
    client: Client = Depends(get_supabase),
):
    query = client.table("historial_inventario").select("*").order("id_movimiento")
    if id_producto is not None:
        query = query.eq("id_producto", id_producto)
    if id_usuario is not None:
        query = query.eq("id_usuario", id_usuario)
    if tipo_movimiento is not None:
        query = query.eq("tipo_movimiento", tipo_movimiento.value)
    response = execute_query(query, "al consultar el historial de inventario")
    return {"cantidad": len(response.data), "movimientos": response.data}


@router.get("/{id_movimiento}")
def obtener_movimiento(id_movimiento: int, client: Client = Depends(get_supabase)):
    row = require_one(
        client,
        "historial_inventario",
        "id_movimiento",
        id_movimiento,
        "Movimiento de inventario",
    )
    return {"movimiento": row}
