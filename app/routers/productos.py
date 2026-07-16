from fastapi import APIRouter, Depends, status
from supabase import Client

from app.database import get_supabase
from app.models.producto import ProductoCreate, ProductoUpdate
from app.services import execute_query, reject_null_fields, require_one, response_row


router = APIRouter(
    prefix="/productos",
    tags=["Productos"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_producto(
    producto: ProductoCreate,
    client: Client = Depends(get_supabase),
):
    response = execute_query(
        client.table("productos").insert(producto.model_dump(mode="json")),
        "al crear el producto",
    )
    return {
        "mensaje": "Producto creado correctamente",
        "producto": response_row(response, "el producto"),
    }


@router.get("")
def obtener_productos(client: Client = Depends(get_supabase)):
    response = execute_query(
        client.table("productos").select("*").order("id_producto"),
        "al consultar los productos",
    )
    return {"cantidad": len(response.data), "productos": response.data}


@router.get("/{id_producto}")
def obtener_producto(id_producto: int, client: Client = Depends(get_supabase)):
    row = require_one(client, "productos", "id_producto", id_producto, "Producto")
    return {"producto": row}


@router.patch("/{id_producto}")
def actualizar_producto(
    id_producto: int,
    producto: ProductoUpdate,
    client: Client = Depends(get_supabase),
):
    existing = require_one(client, "productos", "id_producto", id_producto, "Producto")
    data = producto.model_dump(mode="json", exclude_unset=True)
    reject_null_fields(data, {"codigo_barras", "nombre", "precio_venta", "stock_minimo", "estado"})
    if not data:
        return {"mensaje": "Producto sin cambios", "producto": existing}
    response = execute_query(
        client.table("productos").update(data).eq("id_producto", id_producto),
        "al actualizar el producto",
    )
    return {
        "mensaje": "Producto actualizado correctamente",
        "producto": response_row(response, "el producto"),
    }


@router.delete("/{id_producto}")
def eliminar_producto(id_producto: int, client: Client = Depends(get_supabase)):
    require_one(client, "productos", "id_producto", id_producto, "Producto")
    response = execute_query(
        client.table("productos")
        .update({"estado": False})
        .eq("id_producto", id_producto),
        "al desactivar el producto",
    )
    return {
        "mensaje": "Producto desactivado correctamente",
        "producto": response_row(response, "el producto"),
    }
