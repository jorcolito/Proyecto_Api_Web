from typing import Any

from fastapi import HTTPException, status


SAFE_DATABASE_MESSAGES = frozenset(
    {
        "Cliente no encontrado",
        "Detalle de venta no encontrado",
        "El descuento no puede superar el importe de la linea",
        "El motivo es obligatorio",
        "El usuario esta inactivo",
        "La cantidad debe ser positiva",
        "Movimiento de inventario no encontrado",
        "Producto no encontrado",
        "Stock insuficiente",
        "Tipo de movimiento invalido",
        "Usuario no encontrado",
        "Venta no encontrada",
    }
)


def supabase_http_exception(error: Any, action: str) -> HTTPException:
    code = str(getattr(error, "code", ""))
    message = str(getattr(error, "message", ""))

    if code == "P0002":
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message if message in SAFE_DATABASE_MESSAGES else "Registro no encontrado",
        )
    if code == "23505":
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El registro ya existe",
        )
    if code in {"22003", "23502"}:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Los datos no cumplen las restricciones del registro",
        )
    if code in {"23503", "23514", "P0001"}:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                message
                if message in SAFE_DATABASE_MESSAGES
                else "La operacion entra en conflicto con los datos actuales"
            ),
        )
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error {action}",
    )
