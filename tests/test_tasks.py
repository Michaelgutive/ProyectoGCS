class TestCreateTask:
    """Tests para POST /tasks/."""

    def test_create_task_success(self, client):
        """Crear una tarea con datos válidos."""
        response = client.post(
            "/tasks/",
            json={
                "title": "Configurar pipeline CI",
                "description": "Crear ci.yml con lint y tests",
                "priority": "high",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Configurar pipeline CI"
        assert data["description"] == "Crear ci.yml con lint y tests"
        assert data["priority"] == "high"
        assert data["status"] == "pending"
        assert "id" in data
        assert "created_at" in data

    def test_create_task_minimal(self, client):
        """Crear una tarea solo con título (campos opcionales usan defaults)."""
        response = client.post("/tasks/", json={"title": "Tarea mínima"})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Tarea mínima"
        assert data["status"] == "pending"
        assert data["priority"] == "medium"
        assert data["description"] is None

    def test_create_task_empty_title_fails(self, client):
        """Título vacío debe fallar con 422."""
        response = client.post("/tasks/", json={"title": ""})
        assert response.status_code == 422

    def test_create_task_no_title_fails(self, client):
        """Sin título debe fallar con 422."""
        response = client.post("/tasks/", json={"description": "Sin título"})
        assert response.status_code == 422

    def test_create_task_all_statuses(self, client):
        """Verificar que se pueden crear tareas con todos los status."""
        for task_status in ["pending", "in_progress", "completed"]:
            response = client.post(
                "/tasks/",
                json={"title": f"Task {task_status}", "status": task_status},
            )
            assert response.status_code == 201
            assert response.json()["status"] == task_status

    def test_create_task_all_priorities(self, client):
        """Verificar que se pueden crear tareas con todas las prioridades."""
        for priority in ["low", "medium", "high"]:
            response = client.post(
                "/tasks/",
                json={"title": f"Task {priority}", "priority": priority},
            )
            assert response.status_code == 201
            assert response.json()["priority"] == priority


class TestGetTasks:
    """Tests para GET /tasks/."""

    def test_get_tasks_empty(self, client):
        """Lista vacía cuando no hay tareas."""
        response = client.get("/tasks/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_tasks_returns_all(self, client):
        """Devuelve todas las tareas creadas."""
        client.post("/tasks/", json={"title": "Task 1"})
        client.post("/tasks/", json={"title": "Task 2"})
        client.post("/tasks/", json={"title": "Task 3"})

        response = client.get("/tasks/")
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_get_tasks_pagination(self, client):
        """Verificar que skip y limit funcionan."""
        for i in range(5):
            client.post("/tasks/", json={"title": f"Task {i}"})

        response = client.get("/tasks/?skip=2&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_tasks_filter_by_status(self, client):
        """Filtrar tareas por estado devuelve solo las que coinciden."""
        client.post("/tasks/", json={"title": "Pendiente 1"})
        client.post("/tasks/", json={"title": "Pendiente 2"})
        client.post("/tasks/", json={"title": "Completada", "status": "completed"})

        response = client.get("/tasks/?status_filter=completed")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Completada"


class TestGetTaskById:
    """Tests para GET /tasks/{task_id}."""

    def test_get_task_by_id(self, client):
        """Obtener tarea existente por ID."""
        create_resp = client.post("/tasks/", json={"title": "Mi tarea"})
        task_id = create_resp.json()["id"]

        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Mi tarea"

    def test_get_task_not_found(self, client):
        """ID inexistente devuelve 404."""
        response = client.get("/tasks/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestUpdateTask:
    """Tests para PUT /tasks/{task_id}."""

    def test_update_task_title(self, client):
        """Actualizar solo el título."""
        create_resp = client.post("/tasks/", json={"title": "Original"})
        task_id = create_resp.json()["id"]

        response = client.put(f"/tasks/{task_id}", json={"title": "Actualizado"})
        assert response.status_code == 200
        assert response.json()["title"] == "Actualizado"

    def test_update_task_status(self, client):
        """Cambiar el estado de una tarea."""
        create_resp = client.post("/tasks/", json={"title": "Tarea"})
        task_id = create_resp.json()["id"]

        response = client.put(f"/tasks/{task_id}", json={"status": "completed"})
        assert response.status_code == 200
        assert response.json()["status"] == "completed"

    def test_update_task_multiple_fields(self, client):
        """Actualizar múltiples campos a la vez."""
        create_resp = client.post("/tasks/", json={"title": "Tarea"})
        task_id = create_resp.json()["id"]

        response = client.put(
            f"/tasks/{task_id}",
            json={
                "title": "Tarea actualizada",
                "status": "in_progress",
                "priority": "high",
                "description": "Descripción nueva",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Tarea actualizada"
        assert data["status"] == "in_progress"
        assert data["priority"] == "high"
        assert data["description"] == "Descripción nueva"

    def test_update_task_not_found(self, client):
        """Actualizar tarea inexistente devuelve 404."""
        response = client.put("/tasks/999", json={"title": "Nope"})
        assert response.status_code == 404

    def test_update_preserves_unchanged_fields(self, client):
        """Los campos no enviados mantienen su valor original."""
        create_resp = client.post(
            "/tasks/",
            json={"title": "Original", "priority": "high"},
        )
        task_id = create_resp.json()["id"]

        response = client.put(f"/tasks/{task_id}", json={"status": "completed"})
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Original"
        assert data["priority"] == "high"
        assert data["status"] == "completed"


class TestDeleteTask:
    """Tests para DELETE /tasks/{task_id}."""

    def test_delete_task(self, client):
        """Eliminar tarea existente devuelve 204."""
        create_resp = client.post("/tasks/", json={"title": "A eliminar"})
        task_id = create_resp.json()["id"]

        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 204

    def test_delete_task_removes_from_db(self, client):
        """Verificar que la tarea ya no existe después de eliminarla."""
        create_resp = client.post("/tasks/", json={"title": "A eliminar"})
        task_id = create_resp.json()["id"]

        client.delete(f"/tasks/{task_id}")

        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 404

    def test_delete_task_not_found(self, client):
        """Eliminar tarea inexistente devuelve 404."""
        response = client.delete("/tasks/999")
        assert response.status_code == 404


class TestTaskStats:
    """Tests para GET /tasks/stats/summary."""

    def test_stats_empty(self, client):
        """Sin tareas, todos los contadores están en cero."""
        response = client.get("/tasks/stats/summary")
        assert response.status_code == 200
        data = response.json()
        assert data["total_tasks"] == 0
        assert data["by_status"]["pending"] == 0
        assert data["by_priority"]["medium"] == 0

    def test_stats_counts_tasks(self, client):
        """Los contadores reflejan las tareas creadas por estado y prioridad."""
        client.post("/tasks/", json={"title": "T1", "priority": "high"})
        client.post("/tasks/", json={"title": "T2", "priority": "high"})
        client.post("/tasks/", json={"title": "T3", "status": "completed"})

        response = client.get("/tasks/stats/summary")
        data = response.json()

        assert data["total_tasks"] == 3
        assert data["by_priority"]["high"] == 2
        assert data["by_status"]["completed"] == 1
        assert data["by_status"]["pending"] == 2
