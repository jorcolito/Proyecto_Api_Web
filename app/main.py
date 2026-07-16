from fastapi import FastAPI, HTTPException

from app.database import supabase

from app.routers.productos import router as productos_router

app = FastAPI(
    title="Proyecto API Web",
    description="API para gestion de ventas e inventario de productos",
    version="1.0.0",
)

app.include_router(productos_router)

@app.get("/")
async def root():
    return {"message": "API funcionando correctamente"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/test-supabase")
def test_supabase():
    try:
        response = (
            supabase.table("productos")
            .select("*")
            .limit(1)
            .execute()
        )

        return {
            "mensaje":"Conexión exitosa a Supabase",
            "datos": response.data
        }
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error al conectar con Supabase: {error}"
        )