from db_connection import save_to_db,get_user

class User:
    def user_registration(self,first_name,last_name,email,phone_num,gender,dob,category,area,password):
        registration_data = {
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "dob": dob,
            "area": area,
            "phone_no": phone_num,
            "email": email,
            "category": category,
            "password": password
            }
        save_to_db(registration_data)

    def login(self,email,password):
        logged_in_user = get_user(email,password)
        return logged_in_user
