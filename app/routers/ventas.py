from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client

from app.database import get_supabase
from app.models.venta import VentaCreate, VentaUpdate
from app.services import execute_query, require_active_user, require_one


router = APIRouter(prefix="/ventas", tags=["Ventas"])


def validate_sale_relations(client: Client, id_cliente: int, id_usuario: int) -> None:
    require_one(client, "clientes", "id_cliente", id_cliente, "Cliente")
    require_active_user(client, id_usuario)


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_venta(venta: VentaCreate, client: Client = Depends(get_supabase)):
    validate_sale_relations(client, venta.id_cliente, venta.id_usuario)
    taxes = venta.impuestos.quantize(Decimal("0.01"))
    data = {
        "id_cliente": venta.id_cliente,
        "id_usuario": venta.id_usuario,
        "subtotal": "0.00",
        "impuestos": str(taxes),
        "total": str(taxes),
    }
    response = execute_query(
        client.table("ventas").insert(data),
        "al crear la venta",
    )
    return {"mensaje": "Venta creada correctamente", "venta": response.data[0]}


@router.get("")
def obtener_ventas(client: Client = Depends(get_supabase)):
    response = execute_query(
        client.table("ventas").select("*").order("id_venta"),
        "al consultar las ventas",
    )
    return {"cantidad": len(response.data), "ventas": response.data}


@router.get("/{id_venta}")
def obtener_venta(id_venta: int, client: Client = Depends(get_supabase)):
    sale = require_one(client, "ventas", "id_venta", id_venta, "Venta")
    details = execute_query(
        client.table("detalle_ventas")
        .select("*")
        .eq("id_venta", id_venta)
        .order("id_detalle"),
        "al consultar los detalles de la venta",
    )
    sale["detalles"] = details.data
    return {"venta": sale}


@router.patch("/{id_venta}")
def actualizar_venta(
    id_venta: int,
    venta: VentaUpdate,
    client: Client = Depends(get_supabase),
):
    existing = require_one(client, "ventas", "id_venta", id_venta, "Venta")
    data = venta.model_dump(mode="json", exclude_unset=True)
    if venta.id_cliente is not None:
        require_one(client, "clientes", "id_cliente", venta.id_cliente, "Cliente")
    if venta.id_usuario is not None:
        require_active_user(client, venta.id_usuario)
    if venta.impuestos is not None:
        subtotal = Decimal(str(existing["subtotal"]))
        taxes = venta.impuestos.quantize(Decimal("0.01"))
        data["impuestos"] = str(taxes)
        data["total"] = str((subtotal + taxes).quantize(Decimal("0.01")))
    if not data:
        return {"mensaje": "Venta sin cambios", "venta": existing}
    response = execute_query(
        client.table("ventas").update(data).eq("id_venta", id_venta),
        "al actualizar la venta",
    )
    return {"mensaje": "Venta actualizada correctamente", "venta": response.data[0]}


@router.delete("/{id_venta}")
def eliminar_venta(id_venta: int, client: Client = Depends(get_supabase)):
    require_one(client, "ventas", "id_venta", id_venta, "Venta")
    details = execute_query(
        client.table("detalle_ventas")
        .select("id_detalle")
        .eq("id_venta", id_venta)
        .limit(1),
        "al verificar los detalles de la venta",
    )
    if details.data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La venta tiene detalles asociados",
        )
    response = execute_query(
        client.table("ventas").delete().eq("id_venta", id_venta),
        "al eliminar la venta",
    )
    return {"mensaje": "Venta eliminada correctamente", "venta": response.data[0]}
