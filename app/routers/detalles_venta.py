from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from supabase import Client

from app.database import get_supabase
from app.models.detalle_venta import DetalleVentaCreate, DetalleVentaUpdate
from app.services import execute_query, require_one, rpc_row


router = APIRouter(prefix="/detalles-venta", tags=["Detalle de ventas"])


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_detalle(
    detalle: DetalleVentaCreate,
    client: Client = Depends(get_supabase),
):
    params = {
        "p_id_venta": detalle.id_venta,
        "p_id_producto": detalle.id_producto,
        "p_cantidad": detalle.cantidad,
        "p_descuento": str(detalle.descuento.quantize(Decimal("0.01"))),
    }
    response = execute_query(
        client.rpc("agregar_detalle_venta", params),
        "al crear el detalle de venta",
    )
    return {
        "mensaje": "Detalle de venta creado correctamente",
        "detalle": rpc_row(response, "el detalle de venta"),
    }


@router.get("")
def obtener_detalles(
    id_venta: Optional[int] = Query(default=None, gt=0),
    id_producto: Optional[int] = Query(default=None, gt=0),
    client: Client = Depends(get_supabase),
):
    query = client.table("detalle_ventas").select("*").order("id_detalle")
    if id_venta is not None:
        query = query.eq("id_venta", id_venta)
    if id_producto is not None:
        query = query.eq("id_producto", id_producto)
    response = execute_query(query, "al consultar los detalles de venta")
    return {"cantidad": len(response.data), "detalles": response.data}


@router.get("/{id_detalle}")
def obtener_detalle(id_detalle: int, client: Client = Depends(get_supabase)):
    row = require_one(
        client,
        "detalle_ventas",
        "id_detalle",
        id_detalle,
        "Detalle de venta",
    )
    return {"detalle": row}


@router.patch("/{id_detalle}")
def actualizar_detalle(
    id_detalle: int,
    detalle: DetalleVentaUpdate,
    client: Client = Depends(get_supabase),
):
    params = {
        "p_id_detalle": id_detalle,
        "p_cantidad": detalle.cantidad,
        "p_descuento": (
            str(detalle.descuento.quantize(Decimal("0.01")))
            if detalle.descuento is not None
            else None
        ),
    }
    response = execute_query(
        client.rpc("actualizar_detalle_venta", params),
        "al actualizar el detalle de venta",
    )
    return {
        "mensaje": "Detalle de venta actualizado correctamente",
        "detalle": rpc_row(response, "el detalle de venta"),
    }


@router.delete("/{id_detalle}")
def eliminar_detalle(id_detalle: int, client: Client = Depends(get_supabase)):
    response = execute_query(
        client.rpc("eliminar_detalle_venta", {"p_id_detalle": id_detalle}),
        "al eliminar el detalle de venta",
    )
    return {
        "mensaje": "Detalle de venta eliminado correctamente",
        "detalle": rpc_row(response, "el detalle de venta"),
    }
