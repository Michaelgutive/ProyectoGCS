class TestHealthCheck:
    """Tests para el endpoint de health check."""

    def test_health_check_returns_200(self, client):
        """Verifica que el health check responde correctamente."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_status_healthy(self, client):
        """Verifica que el status sea 'healthy'."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_check_has_version(self, client):
        """Verifica que incluya la versión de la API."""
        response = client.get("/health")
        data = response.json()
        assert "version" in data
        assert data["version"] == "1.0.0"

    def test_health_check_has_service_name(self, client):
        """Verifica que incluya el nombre del servicio."""
        response = client.get("/health")
        data = response.json()
        assert data["service"] == "task-manager-api"
