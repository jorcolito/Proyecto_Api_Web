# Proyecto API Web

Una API para manejar las ventas y el inventario de una tienda, hecha con FastAPI y Supabase.

Creado por **Jorge Colamarco** y **Josias Pérez**.

## ¿De qué trata?

La idea es simple: tienes productos, clientes y usuarios, y necesitas registrar ventas sin que el inventario se te descuadre. Esta API se encarga de todo eso. Cada vez que se vende algo, el stock se descuenta solo, y si entra o sale mercancía queda registrado en un historial.

Lo interesante es que los cálculos delicados (descontar stock, calcular totales con impuestos) no se hacen en Python sino directamente en la base de datos, así no hay forma de que dos ventas al mismo tiempo dejen los números mal.

## ¿Qué se puede hacer?

- **Productos**: crearlos, consultarlos, editarlos y "eliminarlos" (en realidad solo se desactivan, no se borra nada). El stock no se puede editar a mano — solo cambia con ventas o movimientos de inventario, que es como debe ser.
- **Usuarios**: registro con contraseña (guardada con hash, obviamente nunca en texto plano) y desactivación en vez de borrado.
- **Clientes**: lo típico de un CRUD, con validación de email. Si un cliente ya tiene ventas, no se puede eliminar.
- **Ventas**: se crean con sus detalles, la API calcula impuestos y totales por ti.
- **Detalles de venta**: agregar o quitar productos de una venta ajusta el stock automáticamente.
- **Historial de inventario**: para registrar entradas y salidas de mercancía, y consultar qué pasó con filtros por producto o tipo de movimiento.

Toda la documentación de los endpoints se genera sola — levanta el servidor y entra a `/docs`.

## Con qué está hecho

- **Python 3** con **FastAPI**
- **Supabase** (PostgreSQL) como base de datos
- **Pydantic** para validar los datos que entran
- **Pytest** para las pruebas

## Cómo correrlo

Primero clona el repo y crea un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Luego crea un archivo `.env` en la raíz con tus credenciales de Supabase:

```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-clave
```

Y listo, arranca el servidor:

```bash
uvicorn app.main:app --reload
```

Abre [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) y ahí puedes probar todos los endpoints desde el navegador.

## Pruebas

```bash
python -m pytest -q
```

---

Hecho por Jorge Colamarco y Josias Pérez.
