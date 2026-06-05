"""
API REST - RecargaYa S.A.S.
Exposición del módulo de recargas como servicio web.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.recarga import calcular_recarga

app = FastAPI(
    title="RecargaYa API",
    description="Módulo de cálculo de recargas celulares - RecargaYa S.A.S.",
    version="1.0.0",
)


class RecargaRequest(BaseModel):
    monto: float
    premium: bool = False


class RecargaResponse(BaseModel):
    valido: bool
    mensaje: str
    monto: float
    bonificacion_porcentaje: int


@app.get("/health")
def health_check():
    """Verifica que el servicio esté activo."""
    return {"status": "ok", "servicio": "RecargaYa API"}


@app.post("/recargar", response_model=RecargaResponse)
def recargar(request: RecargaRequest):
    """
    Calcula el valor final de una recarga celular.

    - **monto**: Valor de la recarga entre $1.000 y $50.000
    - **premium**: Si el usuario tiene plan premium (obtiene +5% adicional)
    """
    resultado = calcular_recarga(request.monto, request.premium)

    if not resultado["valido"]:
        raise HTTPException(status_code=400, detail=resultado["mensaje"])

    return resultado
