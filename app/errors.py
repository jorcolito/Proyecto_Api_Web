from typing import Any

from fastapi import HTTPException, status


def supabase_http_exception(error: Any, action: str) -> HTTPException:
    code = str(getattr(error, "code", ""))
    message = str(getattr(error, "message", ""))

    if code == "P0002":
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )
    if code == "23505":
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El registro ya existe",
        )
    if code in {"23503", "23514", "P0001"}:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=message or "La operacion entra en conflicto con los datos actuales",
        )
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error {action}",
    )
