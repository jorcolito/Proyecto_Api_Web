from fastapi import Depends, FastAPI
from supabase import Client

from app.database import get_supabase
from app.routers.clientes import router as clientes_router
from app.routers.detalles_venta import router as detalles_venta_router
from app.routers.historial_inventario import router as historial_inventario_router
from app.routers.productos import router as productos_router
from app.routers.usuarios import router as usuarios_router
from app.routers.ventas import router as ventas_router
from app.services import execute_query


app = FastAPI(
    title="Proyecto API Web",
    description="API para gestion de ventas e inventario de productos",
    version="2.0.0",
)

app.include_router(productos_router)
app.include_router(usuarios_router)
app.include_router(clientes_router)
app.include_router(ventas_router)
app.include_router(detalles_venta_router)
app.include_router(historial_inventario_router)


@app.get("/")
async def root():
    return {"message": "API funcionando correctamente"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/test-supabase")
def test_supabase(client: Client = Depends(get_supabase)):
    response = execute_query(
        client.table("productos").select("*").limit(1),
        "al conectar con Supabase",
    )
    return {
        "mensaje": "Conexion exitosa a Supabase",
        "datos": response.data,
    }
