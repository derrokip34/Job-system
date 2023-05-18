#Author: Derrick Kiprop <derrickip34@gmail.com>
#Date:   Mon Apr 10
import psycopg2,bcrypt,uuid,os
from psycopg2.extras import DictCursor
from datetime import date,datetime
from dotenv import load_dotenv
from validate import *

load_dotenv()

db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_port = os.getenv("DB_PORT")

def save_job_seeker_to_db(data):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor()
    query = "INSERT INTO job_seekers (first_name,last_name,email,phone_num,gender,dob,category,area,password) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cur.execute(query, (data["first_name"],data["last_name"],data["email"],data["phone_no"],data["gender"],data["dob"],data["category"],data["area"],data["password"]))
    conn.commit()
    cur.close()
    conn.close()

def save_job_poster_to_db(data):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor()
    session_id = str(uuid.uuid4())
    query = "INSERT INTO job_posters (first_name,last_name,email,phone_num,gender,dob,password) VALUES(%s,%s,%s,%s,%s,%s,%s);"
    cur.execute(query, (data["first_name"],data["last_name"],data["email"],data["phone_no"],data["gender"],data["dob"],data["password"]))
    conn.commit()
    cur.close()
    conn.close()

def get_areas():
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor()
    query = "SELECT area FROM areas;"
    cur.execute(query)
    areas = cur.fetchall()
    columns = [area[0] for area in areas]
    conn.commit()
    cur.close()
    conn.close()
    return columns

def get_user(email,input_password):
    new_password = hash_password(input_password)
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor(cursor_factory=DictCursor)
    login_time = date.now()
    query = """
                UPDATE job_seekers SET session_id = %s AND last_login=%s
                WHERE  email = %s AND password = %s;
                SELECT * FROM job_seekers WHERE email = %s AND password = %s;
            
            """
    session_id = str(uuid.uuid4())
    cur.execute(query,(session_id,login_time,email,new_password,email,new_password))
    user = cur.fetchone()
    if user is None:
        query = """
                    UPDATE job_posters SET session_id = %s AND last_login=%s
                    WHERE  email = %s AND password = %s;
                    SELECT * FROM job_posters WHERE email = %s AND password = %s;
                """
        cur.execute(query,(session_id,login_time,email,new_password,email,new_password,))
        user_type = "job_poster"
        user = cur.fetchone()
    else:
        user_type = "job_seeker"

    conn.commit()
    cur.close()
    conn.close()
    return user,user_type

def get_job_poster_by_id(id):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor(cursor_factory=DictCursor)
    query = "SELECT * FROM job_posters WHERE id = %s;"
    cur.execute(query,(id,))
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return dict(user)

def get_job_seeker_by_id(id):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor(cursor_factory=DictCursor)
    query = "SELECT * FROM job_seekers WHERE id = %s;"
    cur.execute(query,(id,))
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return dict(user)

def update_session(session_id,user_type):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor()
    if user_type is "job_seeker":
        query = "UPDATE job_seekers SET session_id=NULL WHERE session_id=%s;"
        cur.execute(query,(session_id,))
    else:
        query = "UPDATE job_posters SET session_id=NULL WHERE session_id=%s;"
        cur.execute(query,(session_id,))
    
    conn.commit()
    cur.close()
    conn.close()

def get_users():
    print(db_name)
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor()
    query = "SELECT first_name,last_name,email FROM job_posters;"
    cur.execute(query)
    users = cur.fetchall()
    users_list = [user[0]+ " " + user[1] for user in users]

    conn.commit()
    cur.close()
    conn.close()
    return users_list

def get_job_posters():
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor(cursor_factory=DictCursor)

    query = "SELECT id,first_name,last_name,email FROM job_posters;"
    cur.execute(query)
    users = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()
    return users

def get_job_seekers():
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor(cursor_factory=DictCursor)

    query = "SELECT id,first_name,last_name,email FROM job_seekers;"
    cur.execute(query)
    users = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()
    return users

def add_job_to_db(session_id,job_data):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor()

    job_status = "false"
    
    query = "SELECT id FROM job_posters WHERE session_id=%s;"
    cur.execute(query,(session_id,))
    posted_by = cur.fetchone()
    add_job_query = "INSERT INTO jobs(job_category,job_description,posted_by,job_duration,total_amount,job_status,job_location) VALUES(%s,%s,%s,%s,%s,%s,%s);"
    cur.execute(add_job_query,(job_data["job_category"],job_data["job_description"],posted_by[0],job_data["job_duration"],int(job_data["total_amount"]),job_status,job_data["job_location"],))

    conn.commit()
    cur.close()
    conn.close()

def get_all_jobs():
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor(cursor_factory=DictCursor)
    query = "SELECT * FROM jobs;"
    cur.execute(query)
    jobs = cur.fetchall()
    
    conn.commit()
    cur.close()
    conn.close()
    return jobs

def get_jobs_posted_by_user(session_id):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor(cursor_factory=DictCursor)
    query1 = "SELECT id FROM job_posters WHERE session_id=%s"
    cur.execute(query1,(session_id,))
    user = cur.fetchone()

    query = "SELECT * FROM jobs WHERE posted_by=%s;"
    cur.execute(query,(user))
    jobs = cur.fetchall()
    
    conn.commit()
    cur.close()
    conn.close()
    return jobs

def get_jobs_posted_by_user_and_status(session_id,status):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor(cursor_factory=DictCursor)
    query1 = "SELECT id FROM job_posters WHERE session_id=%s"
    cur.execute(query1,(session_id,))
    user = cur.fetchone()

    query = "SELECT * FROM jobs WHERE posted_by=%s AND job_status=%s;"
    cur.execute(query,(user[0],status,))
    jobs = cur.fetchall()
    
    conn.commit()
    cur.close()
    conn.close()
    return jobs

def search_jobs(category,duration1,duration2,payment1,payment2,location):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor(cursor_factory=DictCursor)

    query = """
            SELECT * FROM jobs WHERE job_duration BETWEEN %s AND %s 
                                     OR job_category=%s
                                     OR total_amount BETWEEN %s AND %s
                                     OR job_location=%s;
            """
    cur.execute(query,(duration1,duration2,category,payment1,payment2,location,))
    jobs = cur.fetchall()
    
    conn.commit()
    cur.close()
    conn.close()
    return jobs

def insert_application_to_db(session_id,job_id):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor()

    application_status = "ND"

    today_date = date.today()
    
    query = "SELECT id FROM job_seekers WHERE session_id=%s;"
    cur.execute(query,(session_id,))
    applicant = cur.fetchone()
    application_query = "INSERT INTO job_applications(applicant,job,application_status,application_date) VALUES(%s,%s,%s,%s);"
    cur.execute(application_query,(applicant,job_id,application_status,today_date))

    conn.commit()
    cur.close()
    conn.close()

def remove_application_from_db(session_id,job_id):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor()

    query = "SELECT id FROM job_seekers WHERE session_id=%s;"
    cur.execute(query,(session_id,))
    applicant = cur.fetchone()

    delete_query = "DELETE FROM job_applications WHERE job=%s AND applicant=%s;"
    cur.execute(delete_query,(job_id,applicant))

    conn.commit()
    cur.close()
    conn.close()

def get_user_applications(session_id):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor(cursor_factory=DictCursor)

    query = "SELECT id FROM job_seekers WHERE session_id=%s;"
    cur.execute(query,(session_id,))
    applicant = cur.fetchone()

    query2 = "SELECT job FROM job_applications WHERE applicant=%s;"
    cur.execute(query2,(applicant[0],))

    applications = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()
    return applications

def get_job_applications(job_id):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor(cursor_factory=DictCursor)

    query = "SELECT * FROM job_applications WHERE job=%s;"
    cur.execute(query,(job_id,))

    applications = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()
    return applications

def get_job(job_id):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor(cursor_factory=DictCursor)

    query = "SELECT * FROM jobs WHERE job_id=%s;"
    cur.execute(query,(job_id,))
    job = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()
    return job

def select_applicant(application_id,job):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor()

    query = """UPDATE job_applications
                SET application_status='S'
                WHERE application_id=%s;
                UPDATE jobs
                SET done_by=%s
                WHERE job_id=%s;
            """
    query2 = "SELECT applicant FROM job_applications WHERE application_id=%s"
    cur.execute(query2,(application_id,))
    done_by = cur.fetchone()
    cur.execute(query,(application_id,done_by,job,))
    conn.commit()
    cur.close()
    conn.close()

def reverse_applicant(application_id):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor()

    query = """UPDATE job_applications
                SET application_status='ND'
                WHERE application_id=%s;
            """
    cur.execute(query,(application_id,))
    conn.commit()
    cur.close()
    conn.close()

def job_done(job_id):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor()

    done_on = date.today()
    job_status = "true"

    query = """UPDATE jobs
                SET job_status=%s,done_on=%s
                WHERE job_id=%s;
            """
    cur.execute(query,(job_status,done_on,job_id,))
    conn.commit()
    cur.close()
    conn.close()

def get_jobs_by_category(category):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor(cursor_factory=DictCursor)

    query = "SELECT * FROM jobs WHERE job_category=%s;"
    cur.execute(query,(category,))
    jobs = cur.fetchall()
    
    conn.commit()
    cur.close()
    conn.close()
    return jobs

def update_job_in_db(job_id,category,description,duration,amount,location):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor()

    time_updated = datetime.now()

    query="""
            UPDATE jobs
            SET job_category=%s, job_description=%s, job_duration=%s, total_amount=%s, job_location=%s, updated_on=%s
            WHERE job_id=%s;
          """
    cur.execute(query,(category,description,int(duration),int(amount),location,time_updated,job_id,))
    
    conn.commit()
    cur.close()
    conn.close()

def add_job_rating(job,rating_value,comment):
    conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
    cur = conn.cursor(cursor_factory=DictCursor)

    query = "INSERT INTO job_ratings(job_rated,rating_value,comment) VALUES(%s,%s,%s);"
    cur.execute(query,(job,int(rating_value),comment,))
    
    conn.commit()
    cur.close()
    conn.close()
    