import bcrypt

def hash_password(password):
    salt = b'$2b$12$SJv9T2zvJFjI6bYtibhZv.'
    new_pass_bytes = password.encode('utf-8')
    new_hashed = bcrypt.hashpw(new_pass_bytes,salt)
    hashed_password = new_hashed.decode('utf-8')
    return hashed_password

def get_date_of_birth(day,month,year):
    date_of_birth = day + "/" + month + "/" + year
    return date_of_birth