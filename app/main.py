from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import sales, metrics

# Crear instancia de FastAPI
app = FastAPI(title="Sales Dashboard API",
             description="API for Sales Dashboard",
             version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

# Incluir routers
app.include_router(sales.router)
app.include_router(metrics.router)

@app.get("/")
async def read_root():
    """
    Root endpoint that returns a welcome message
    """
    return {
        "message": "Welcome to the Sales Dashboard API",
        "status": "running"
    }

# No es necesario el bloque if __name__ == "__main__" 
# ya que gunicorn manejará la ejecución