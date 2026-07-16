from typing import Any, Dict

from fastapi import HTTPException, status

from app.errors import supabase_http_exception


def execute_query(query: Any, action: str) -> Any:
    try:
        return query.execute()
    except HTTPException:
        raise
    except Exception as error:
        raise supabase_http_exception(error, action) from error


def require_one(
    client: Any,
    table: str,
    id_column: str,
    value: int,
    label: str,
) -> Dict[str, Any]:
    response = execute_query(
        client.table(table).select("*").eq(id_column, value).limit(1),
        f"al consultar {label}",
    )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{label} no encontrado",
        )
    return response.data[0]


def require_active_user(client: Any, id_usuario: int) -> Dict[str, Any]:
    user = require_one(client, "usuarios", "id_usuario", id_usuario, "Usuario")
    if not user.get("activo", False):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario esta inactivo",
        )
    return user


def rpc_row(response: Any, label: str) -> Dict[str, Any]:
    data = response.data
    if isinstance(data, list) and data:
        return data[0]
    if isinstance(data, dict):
        return data
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Respuesta invalida al procesar {label}",
    )
