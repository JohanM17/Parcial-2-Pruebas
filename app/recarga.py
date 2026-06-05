"""
Módulo de cálculo de recargas - RecargaYa S.A.S.

Reglas de negocio:
- Monto válido: $1.000 – $50.000
- Monto >= $10.000: 10% de bonificación en datos
- Monto >= $30.000: 25% de bonificación en datos
- Usuario premium: +5% adicional sobre cualquier bonificación
"""

MONTO_MINIMO = 1_000
MONTO_MAXIMO = 50_000
BONIFICACION_MEDIA = 10
BONIFICACION_ALTA = 25
BONUS_PREMIUM = 5
UMBRAL_MEDIA = 10_000
UMBRAL_ALTA = 30_000


def _bonificacion_base(monto: int | float) -> int:
    """Retorna el porcentaje de bonificación según el monto (sin premium)."""
    if monto >= UMBRAL_ALTA:
        return BONIFICACION_ALTA
    if monto >= UMBRAL_MEDIA:
        return BONIFICACION_MEDIA
    return 0


def _es_monto_valido(monto: int | float) -> bool:
    """Verifica si el monto está dentro del rango permitido."""
    return MONTO_MINIMO <= monto <= MONTO_MAXIMO


def calcular_recarga(monto: int | float, premium: bool = False) -> dict:
    """
    Calcula el resultado de una recarga celular.

    Args:
        monto: Valor de la recarga en pesos colombianos.
        premium: Si el usuario tiene plan premium.

    Returns:
        dict con claves: valido, mensaje, monto, bonificacion_porcentaje
    """
    if not _es_monto_valido(monto):
        return {
            "valido": False,
            "mensaje": "Monto rechazado: debe estar entre $1.000 y $50.000",
            "monto": monto,
            "bonificacion_porcentaje": 0,
        }

    bonificacion = _bonificacion_base(monto)
    if premium:
        bonificacion += BONUS_PREMIUM

    return {
        "valido": True,
        "mensaje": "Recarga exitosa",
        "monto": monto,
        "bonificacion_porcentaje": bonificacion,
    }
