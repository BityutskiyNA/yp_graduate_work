# from app.config import config
# from app.src.databases.db import db_session
# from app.app import models
# from app.src.repositories.cache import CacheRepository
#
#
# def authorization_superuser(client):
#     mode_user = models[0]
#     admin_user =db_session.query(mode_user).filter(mode_user.login == config.admin.login).first()
#     CacheRepository.block(admin_user.id)
#     response = client.post("/login", json={
#         "login": config.admin.login,
#         "password": config.admin.password,
#     })
#     return response
#
#
# def create_test_user(client, token):
#     response = client.post("/admin/user", headers={"Authorization": f"Bearer {token}"}, json={
#         "login": "testcreate_user",
#         "password": "testcreate_user",
#     })
#     return response
#
#
# # def test_create_user(client, app):
# #     response = authorization_superuser(client)
# #
# #     token = response.json["access_token"]
# #     response = create_test_user(client, token)
# #
# #     assert response.status_code == 200
#
#
# def test_retrieve_user(client, app):
#     response = authorization_superuser(client)
#     access_token = response.json["access_token"]
#     # user = create_user(client, token)
#     # user_id = user.json['data']['id']
#     mode_user = models[0]
#     admin_user = db_session.query(mode_user).filter(mode_user.login == config.admin.login).first()
#
#     response = client.get(f"/admin/user/{admin_user.id}", headers={"Authorization": f"Bearer {access_token}"}, )
#     assert response.status_code == 200
# #
# #
# # def test_retrieve_users(client, app):
# #     response = authorization_superuser(client)
# #     token = response.json["access_token"]
# #     # user = create_user(client, token)
# #
# #     response = client.get(f"/admin/users", headers={"Authorization": f"Bearer {token}"})
# #     assert response.status_code == 200
# # #
# #
# # # def test_retrieve_sessions(client, app):
# # #     response = authorization_superuser(client)
# # #     token = response.json["access_token"]
# # #     user = create_user(client, token)
# # #     user_id = user.json['data']['id']
# # #
# # #     response = client.get(f"/admin/user/{user_id}/sessions", headers={"Authorization": f"Bearer {token}"}, )
# # #     assert response.status_code == 200
# #
# # # def test_retrieve_all_sessions(client, app):
# # #
# # #     response = authorization_superuser(client)
# # #     token = response.json["access_token"]
# # #     user = create_user(client, token)
# # #
# # #     response = client.get(f"/admin/users/sessions", headers={"Authorization": f"Bearer {token}"},)
# # #     assert response.status_code == 200
# #
# # # def test_delete_user(client, app):
# # #     response = authorization_superuser(client)
# # #     token = response.json["access_token"]
# # #     user = create_user(client, token)
# # #     user_id = user.json['data']['id']
# # #     response = client.delete(f"/admin/user/{user_id}", headers={"Authorization": f"Bearer {token}"}, )
# # #     assert response.status_code == 200
