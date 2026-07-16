from fastapi import FastAPI

app = FastAPI(
    title="Proyecto API Web",
    description="API para gestion de ventas e inventario de productos",
    version="1.0.0",
)

@app.get("/")
async def root():
    return {"message": "API funcionando correctamente"}

@app.get("/health")
def health_check():
    return {"status": "ok"}