import requests

# response = requests.post(
#     "http://127.0.0.1:5000/users",
#     json={"name": "user_2", "password": "1234"},
# )
# print(response.status_code)
# print(response.json())

# response = requests.get(
#     "http://127.0.0.1:5000/users/1666",
# )
# print(response.status_code)
# print(response.json())


# response = requests.patch(
#     "http://127.0.0.1:5000/users/1",
#     json={"name": "new_name", "password": "1234"},
# )
# print(response.status_code)
# print(response.json())


# response = requests.get(
#     "http://127.0.0.1:5000/users/144444",
# )
# print(response.status_code)
# print(response.json())

# response = requests.delete(
#     "http://127.0.0.1:5000/users/1",
# )
# print(response.status_code)
# print(response.json())

response = requests.delete(
    "http://127.0.0.1:5000/users/1",
)
print(response.status_code)
print(response.json())
