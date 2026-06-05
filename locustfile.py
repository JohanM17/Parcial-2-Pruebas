"""
Script de pruebas de rendimiento - RecargaYa S.A.S.
Verifica que el P95 sea menor a 300ms con 30 usuarios simultaneos.

Uso:
    uv run locust -f locustfile.py --host=http://localhost:8000 \
        --users 30 --spawn-rate 5 --run-time 60s --headless \
        --html=reporte_locust.html
"""
from locust import HttpUser, task, between


class RecargaUser(HttpUser):
    """Simula un usuario haciendo recargas en la API."""

    wait_time = between(0.5, 2)

    @task(3)
    def recarga_sin_premium(self):
        """Recarga normal sin plan premium - caso mas frecuente."""
        self.client.post(
            "/recargar",
            json={"monto": 15000, "premium": False},
            name="/recargar [sin premium]",
        )

    @task(2)
    def recarga_con_premium(self):
        """Recarga con plan premium."""
        self.client.post(
            "/recargar",
            json={"monto": 30000, "premium": True},
            name="/recargar [premium]",
        )

    @task(1)
    def recarga_invalida(self):
        """Recarga con monto invalido - verifica manejo de errores bajo carga."""
        self.client.post(
            "/recargar",
            json={"monto": 500, "premium": False},
            name="/recargar [invalida]",
        )

    @task(1)
    def health_check(self):
        """Verificacion de salud del servicio."""
        self.client.get("/health", name="/health")
