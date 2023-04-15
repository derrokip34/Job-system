#Author: Derrick Kiprop <derrickip34@gmail.com>
#Date:   Mon Apr 10
import psycopg2,bcrypt,uuid
from datetime import date

def save_job_seeker_to_db(data):
    conn = psycopg2.connect(database='csc_227_project',user='postgres',host='localhost',port='5432',password='enkay2008')
    cur = conn.cursor()
    query = "INSERT INTO job_seekers (first_name,last_name,email,phone_num,gender,dob,category,area,password) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cur.execute(query, (data["first_name"],data["last_name"],data["email"],data["phone_no"],data["gender"],data["dob"],data["category"],data["area"],data["password"]))
    conn.commit()
    cur.close()
    conn.close()

def save_job_poster_to_db(data):
    conn = psycopg2.connect(database='csc_227_project',user='postgres',host='localhost',port='5432',password='enkay2008')
    cur = conn.cursor()
    session_id = str(uuid.uuid4())
    query = "INSERT INTO job_posters (first_name,last_name,email,phone_num,gender,dob,password) VALUES(%s,%s,%s,%s,%s,%s,%s);"
    cur.execute(query, (data["first_name"],data["last_name"],data["email"],data["phone_no"],data["gender"],data["dob"],data["password"]))
    conn.commit()
    cur.close()
    conn.close()

def get_areas():
    conn = psycopg2.connect(database='csc_227_project',user='postgres',host='localhost',port='5432',password='enkay2008')
    cur = conn.cursor()
    query = "SELECT area_name FROM areas;"
    cur.execute(query)
    areas = cur.fetchall()
    columns = [area[0] for area in areas]
    conn.commit()
    cur.close()
    conn.close()
    return columns

def hash_password(password):
    salt = b'$2b$12$SJv9T2zvJFjI6bYtibhZv.'
    new_pass_bytes = password.encode('utf-8')
    new_hashed = bcrypt.hashpw(new_pass_bytes,salt)
    global hashed_password
    hashed_password = new_hashed.decode('utf-8')
    return hashed_password

def get_user(email,input_password):
    new_password = hash_password(input_password)
    conn = psycopg2.connect(database='csc_227_project',user='postgres',host='localhost',port='5432',password='enkay2008')
    cur = conn.cursor()
    query = """
                UPDATE job_seekers SET session_id = %s WHERE  email = %s AND password = %s;
                SELECT * FROM job_seekers WHERE email = %s AND password = %s;
            
            """
    session_id = str(uuid.uuid4())
    cur.execute(query,(session_id,email,new_password,email,new_password))
    user = cur.fetchone()
    if user is None:
        query = """
                    UPDATE job_posters SET session_id = %s WHERE  email = %s AND password = %s;
                    SELECT * FROM job_posters WHERE email = %s AND password = %s;
                """
        cur.execute(query,(session_id,email,new_password,email,new_password,))
        user_type = "job_poster"
        user = cur.fetchone()
    else:
        user_type = "job_seeker"

    conn.commit()
    cur.close()
    conn.close()
    return user,user_type

def update_session(session_id,user_type):
    conn = psycopg2.connect(database='csc_227_project',user='postgres',host='localhost',port='5432',password='enkay2008')
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
    conn = psycopg2.connect(database='csc_227_project',user='postgres',host='localhost',port='5432',password='enkay2008')
    cur = conn.cursor()
    query = "SELECT first_name,last_name,email FROM job_posters;"
    cur.execute(query)
    users = cur.fetchall()
    users_list = [user[0]+ " " + user[1] for user in users]

    conn.commit()
    cur.close()
    conn.close()
    return users_list

def add_job_to_db(session_id,job_data):
    conn = psycopg2.connect(database='csc_227_project',user='postgres',host='localhost',port='5432',password='enkay2008')
    cur = conn.cursor()

    today = date.today()
    formatted_date = today.strftime("%d/%m/%Y")

    query = "SELECT id FROM job_posters WHERE session_id=%s;"
    cur.execute(query,(session_id,))
    posted_by = cur.fetchone()
    add_job_query = "INSERT INTO jobs(job_category,job_description,date_posted,posted_by,job_duration,total_amount) VALUES(%s,%s,%s,%s,%s,%s);"
    cur.execute(add_job_query,(job_data["job_category"],job_data["job_description"],formatted_date,posted_by[0],job_data["job_duration"],int(job_data["total_amount"]),))

    conn.commit()
    cur.close()
    conn.close()
