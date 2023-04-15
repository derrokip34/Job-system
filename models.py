from db_connection import *

class User:
    def job_seeker_registration(self,first_name,last_name,email,phone_num,gender,dob,category,area,password):
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
        save_job_seeker_to_db(registration_data)

    def job_poster_registration(self,first_name,last_name,email,phone_num,gender,dob,password):
        registration_data = {
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "dob": dob,
            "phone_no": phone_num,
            "email": email,
            "password": password
            }
        save_job_poster_to_db(registration_data)

    def login(self,email,password):
        logged_in_user,user_type = get_user(email,password)
        return logged_in_user,user_type
    
    def log_out(self,sessionid,usertype):
        update_session(sessionid,usertype)
