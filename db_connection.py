#Author: Derrick Kiprop <derrickip34@gmail.com>
#Date:   Mon Apr 10
import psycopg2

def save_to_db(data):
    conn = psycopg2.connect(database='csc_227',user='postgres',host='localhost',port='5432',password='enkay2008')
    cur = conn.cursor()
    query = "INSERT INTO job_seekers (first_name,last_name,email,phone_num,gender,dob,category,area,password) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cur.execute(query, (data["first_name"],data["last_name"],data["email"],data["phone_no"],data["gender"],data["dob"],data["category"],data["area"],data["password"]))
    conn.commit()
    cur.close()
    conn.close()

def get_areas():
    conn = psycopg2.connect(database='csc_227',user='postgres',host='localhost',port='5432',password='enkay2008')
    cur = conn.cursor()
    query = "SELECT area_name FROM areas;"
    cur.execute(query)
    areas = cur.fetchall()
    columns = [area[0] for area in areas]
    conn.commit()
    cur.close()
    conn.close()
    return columns