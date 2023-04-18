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

class Job:
    def save_job(self,session_id,job_category,job_description,job_duration,total_amount):
        job_data = {
            "job_category": job_category,
            "job_description": job_description,
            "job_duration": job_duration,
            "total_amount": total_amount
        }
        add_job_to_db(session_id,job_data)

    def get_jobs_posted(self):
        all_jobs_posted = get_all_jobs()
        return all_jobs_posted
    
    def job_application(self,sessionid,jobid):
        insert_application_to_db(sessionid,jobid)

    def remove_application(self,sessionid,jobid):
        remove_application_from_db(sessionid,jobid)
