#Author: Derrick Kiprop <derrickip34@gmail.com>
#Date:   Mon Apr 10
import psycopg2,bcrypt,uuid

def save_job_seeker_to_db(data):
    conn = psycopg2.connect(database='csc_227_project',user='postgres',host='localhost',port='5432',password='enkay2008')
    cur = conn.cursor()
    session_id = str(uuid.uuid4())
    query = "INSERT INTO job_seekers (first_name,last_name,email,phone_num,gender,dob,category,area,password,session_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cur.execute(query, (data["first_name"],data["last_name"],data["email"],data["phone_no"],data["gender"],data["dob"],data["category"],data["area"],data["password"],session_id))
    conn.commit()
    cur.close()
    conn.close()

def save_job_poster_to_db(data):
    conn = psycopg2.connect(database='csc_227_project',user='postgres',host='localhost',port='5432',password='enkay2008')
    cur = conn.cursor()
    session_id = str(uuid.uuid4())
    query = "INSERT INTO job_posters (first_name,last_name,email,phone_num,gender,dob,password,session_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"
    cur.execute(query, (data["first_name"],data["last_name"],data["email"],data["phone_no"],data["gender"],data["dob"],data["password"],session_id))
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
    query = "SELECT * FROM job_seekers WHERE email=%s AND password=%s;"
    cur.execute(query,(email,new_password))
    user = cur.fetchone()
    user_type = "job_seeker"
    if user is None:
        query = "SELECT * FROM job_posters WHERE email=%s AND password=%s;"
        cur.execute(query,(email,new_password))
        user_type = "job_poster"
        user = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()
    return user,user_type