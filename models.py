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

    def get_job_poster(self,id):
        user = get_job_poster_by_id(id)
        full_username = user[0] + " " + user[1]
        return full_username
    
    def get_job_seeker(self,id):
        user = get_job_seeker_by_id(id)
        if user is not None:
            full_username = user[0] + " " + user[1]
        else:
            full_username = "Not selected yet"
        return full_username

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

    def get_application(self,sessionid):
        user_applications = get_user_applications(sessionid)
        return user_applications
    
    def get_specified_job(self,job_id):
        job = get_job(job_id)
        return job
    
    def get_user_jobs(self,session_id):
        jobs = get_jobs_posted_by_user(session_id)
        return jobs
    
    def get_job_applications(self,job_id):
        applications = get_job_applications(job_id)
        return applications
