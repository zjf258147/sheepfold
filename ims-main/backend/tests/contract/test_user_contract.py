"""
用户管理 契约测试
验证 API 请求参数格式、响应数据结构、状态码。
需要管理员权限。
"""

import pytest


class TestUserContract:
    """用户管理 API 契约测试。"""

    def test_list_users_returns_page_result(self, client, auth_headers, seed_data):
        """GET /users 返回分页结构。"""
        res = client.get("/api/v1/users", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]
        assert "total" in data["data"]
        assert len(data["data"]["items"]) >= 5

    def test_get_user_detail(self, client, auth_headers, seed_data):
        """GET /users/{id} 返回用户详情。"""
        res = client.get(f"/api/v1/users/{seed_data['admin'].id}", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["data"]["username"] == "admin"

    def test_create_user_success(self, client, auth_headers):
        """POST /users 创建用户成功。"""
        payload = {
            "username": "contract_test_user",
            "password": "test123456",
            "nickname": "契约测试用户",
            "role": "WAREHOUSE",
        }
        res = client.post("/api/v1/users", json=payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["username"] == "contract_test_user"

    def test_create_user_duplicate(self, client, auth_headers, seed_data):
        """POST /users 重复用户名返回 409。"""
        payload = {
            "username": seed_data["admin"].username,
            "password": "test123456",
            "nickname": "重复用户",
            "role": "WAREHOUSE",
        }
        res = client.post("/api/v1/users", json=payload, headers=auth_headers)
        assert res.status_code == 409

    def test_update_user(self, client, auth_headers, seed_data):
        """PUT /users/{id} 更新用户信息。"""
        res = client.put(
            f"/api/v1/users/{seed_data['warehouse'].id}",
            json={"nickname": "已更新昵称"},
            headers=auth_headers,
        )
        assert res.status_code == 200

    def test_toggle_user_status(self, client, auth_headers, seed_data):
        """PATCH /users/{id}/status 启用/禁用用户。"""
        res = client.patch(
            f"/api/v1/users/{seed_data['warehouse'].id}/status",
            headers=auth_headers,
        )
        assert res.status_code == 200
        assert res.json()["data"]["status"] == 0

        # 恢复启用
        res2 = client.patch(
            f"/api/v1/users/{seed_data['warehouse'].id}/status",
            headers=auth_headers,
        )
        assert res2.json()["data"]["status"] == 1

    def test_delete_user(self, client, auth_headers):
        """DELETE /users/{id} 删除用户。"""
        create_res = client.post("/api/v1/users", json={
            "username": "to_delete_user",
            "password": "test123456",
            "nickname": "待删除",
            "role": "WAREHOUSE",
        }, headers=auth_headers)
        user_id = create_res.json()["data"]["id"]

        delete_res = client.delete(f"/api/v1/users/{user_id}", headers=auth_headers)
        assert delete_res.status_code == 200

    def test_cannot_delete_self(self, client, auth_headers, seed_data):
        """DELETE /users/{id} 不可删除自己。"""
        res = client.delete(f"/api/v1/users/{seed_data['admin'].id}", headers=auth_headers)
        assert res.status_code == 400

    def test_change_password(self, client, auth_headers):
        """POST /users/change-password 修改密码。"""
        res = client.post("/api/v1/users/change-password", json={
            "old_password": "admin123",
            "new_password": "newpass123",
        }, headers=auth_headers)
        assert res.status_code == 200

    def test_change_password_wrong_old(self, client, auth_headers):
        """POST /users/change-password 旧密码错误返回 400。"""
        res = client.post("/api/v1/users/change-password", json={
            "old_password": "wrongpassword",
            "new_password": "newpass123",
        }, headers=auth_headers)
        assert res.status_code == 400

    def test_create_user_validates_fields(self, client, auth_headers):
        """POST /users 缺少必填字段返回 422。"""
        res = client.post("/api/v1/users", json={}, headers=auth_headers)
        assert res.status_code == 422