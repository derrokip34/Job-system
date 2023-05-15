import psycopg2,os
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_port = os.getenv("DB_PORT")

conn = psycopg2.connect(database=db_name,user=db_user,host=db_host,port=db_port,password=db_password)
cur = conn.cursor()
query = """
        CREATE TABLE job_posters(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(30),
            last_name VARCHAR(30),
            email VARCHAR(30),
            phone_num VARCHAR(10),
            gender VARCHAR(2),
            dob DATE,
            password VARCHAR(70),
            profile_pic_path VARCHAR(100),
            overview VARCHAR(200),
            location VARCHAR(50),
            session_id UUID
        );
        CREATE TABLE job_seekers(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(30),
            last_name VARCHAR(30),
            email VARCHAR(30),
            phone_num VARCHAR(10),
            gender VARCHAR(2),
            dob DATE,
            password VARCHAR(70),
            category VARCHAR(40),
            area VARCHAR(40),
            rating INT,
            profile_pic_path VARCHAR(100),
            overview VARCHAR(200),
            days_availability VARCHAR(100),
            hours_availability VARCHAR(20),
            session_id UUID
        );
        CREATE TABLE jobs(
            job_id SERIAL PRIMARY KEY,
            job_category VARCHAR(40),
            job_description VARCHAR(255),
            date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            posted_by INT,
            done_by INT,
            job_duration INT,
            total_amount INT,
            done_on TIMESTAMP,
            job_status VARCHAR(10),
            rating INT,
            comment VARCHAR(255),
            job_location VARCHAR(30),
            updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (posted_by) REFERENCES job_posters(id),
            FOREIGN KEY (done_by) REFERENCES job_seekers(id)
        );
        CREATE TABLE job_applications(
            application_id SERIAL PRIMARY KEY,
            applicant INT,
            job INT,
            application_status VARCHAR(5),
            application_date DATE,
            FOREIGN KEY (applicant) REFERENCES job_seekers(id),
            FOREIGN KEY (job) REFERENCES jobs(job_id)
        );
        CREATE TABLE job_ratings(
            rating_value INT,
            job_rated INT,
            job_seeker_rated INT,
            FOREIGN KEY (job_rated) REFERENCES jobs(job_id),
            FOREIGN KEY (job_seeker_rated) REFERENCES job_seekers(id)
        );
        CREATE TABLE job_categories(
            category_id SERIAL PRIMARY KEY,
            category VARCHAR(40)
        );
        CREATE TABLE areas(
            area_id SERIAL PRIMARY KEY,
            area VARCHAR(40)
        );
        """

cur.execute(query)
conn.commit()
cur.close()
conn.close()