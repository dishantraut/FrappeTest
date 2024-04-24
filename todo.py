# def check_jwt_auth():
#   try:
#     auth_header = request.headers.get('Authorization')
#     if not auth_header:
#       return False
#     split_header = auth_header.split()
#     if split_header[0] != 'Bearer':
#       return False
#     token = split_header[1]
#     data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
#     # You can access user data from payload (data['user_id']) here if needed
#     return True
#   except jwt.exceptions.JWTError:
#     return False

# def requires_login(func):
#   @wraps(func)
#   def decorated_function(*args, **kwargs):
#     if not (check_jwt_auth() or "user_id" in session):
#       return redirect("/login")
#     return func(*args, **kwargs)
#   return decorated_function