from werkzeug.security import generate_password_hash
p=generate_password_hash("12345678")
print(p)