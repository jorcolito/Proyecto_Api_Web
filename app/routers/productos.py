from fastapi import APIRouter, HTTPException, status

from app.database import supabase
from app.models.producto import ProductoCreate

router = APIRouter(
    prefix="/productos",
    tags=["Productos"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate):
    try:
        datos = producto.model_dump(mode="json")

        response = (
            supabase.table("productos")
            .insert(datos)
            .execute()
        )

        return {
            "mensaje": "Producto creado correctamente",
            "producto": response.data[0]
        }

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el producto: {error}"
        )


@router.get("")
def obtener_productos():
    try:
        response = (
            supabase.table("productos")
            .select("*")
            .order("id_producto")
            .execute()
        )

        return {
            "cantidad": len(response.data),
            "productos": response.data
        }

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al consultar los productos: {error}"
        )