from tkinter import *
from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox
from models import User,Job
import re
from validate import *

session = {
    "username": None,
    "session_id": None,
    "user_type": None,
    "logged_in": False
}
user = User()
job =Job()

home_pg = Tk()
home_pg.geometry("900x500")
home_pg.configure(background="gray")
home_pg.resizable(0,0)

def logout():
    user.log_out(session["session_id"],session["user_type"])
    session["logged_in"] = False
    session["session_id"] = None
    session["user_type"] = None
    session["username"] = None
    messagebox.showinfo("Log Out","User Logged out")
    home()

def home():
    home_pg.title("Home")

    home_menu_bar = Frame(home_pg,bg="dimgrey",width=150,height=1280)
    home_menu_bar.pack(side=LEFT)

    home_frame = Frame(home_pg,bg="wheat",borderwidth=10,width=550,height=1280)
    home_frame.pack(expand=True,fill=BOTH)

    form_frame = Frame(home_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    if session["logged_in"] is False:
        Button(form_frame,text="Job Seeker",command=lambda:[home_frame.destroy(),home_menu_bar.destroy(),registration_page()]).place(x=100,y=30)
        Button(form_frame,text="Job Poster",command=lambda:[job_poster_form()]).place(x=20,y=30)
    else:
        Button(form_frame,text="Logout",command=lambda:[home_menu_bar.destroy(),home_frame.destroy(),logout()]).place(x=20,y=30)

    def job_poster_form():
        user_details_window = Tk()
        user_details_window.geometry('700x400')
        user_details_window.configure(background="gray")
        f_name_label=Label(user_details_window,text="First Name",background="grey",fg="whitesmoke",font=("Arial",12))
        f_name_label.place(x=20,y=50)
        fname_entry=Entry(user_details_window,width=30)
        fname_entry.place(x=160,y=50)
        l_name_label=Label(user_details_window,fg="whitesmoke",font=("Arial",12),background="gray",text="    Last Name")
        l_name_label.place(x=310,y=50)
        lname_entry=Entry(user_details_window,width=30)
        lname_entry.place(x=420,y=50)
        
        gender_label = Label(user_details_window,text="Gender",background="grey",fg="whitesmoke",font=("Arial",12))
        gender_label.place(x=20,y=90)
        gender_var = StringVar(user_details_window)
        Radiobutton(user_details_window,text="Male",variable=gender_var,value="M",background="grey").place(x=160,y=90)
        Radiobutton(user_details_window,text="Female",variable=gender_var,value="F",background="grey").place(x=220,y=90)
        dob_label = Label(user_details_window,text="Date of Birth",background="grey",fg="whitesmoke",font=("Arial",12))
        dob_label.place(x=20,y=130)
        day_entry = Entry(user_details_window,width=5)
        day_entry.place(x=160,y=130)
        day_label = Label(user_details_window,text="DD",background="grey",fg="whitesmoke",font=("Arial",12))
        day_label.place(x=160,y=150)
        month_entry = Entry(user_details_window,width=5)
        month_entry.place(x=200,y=130)
        month_label = Label(user_details_window,text="MM",background="grey",fg="whitesmoke",font=("Arial",12))
        month_label.place(x=200,y=150)
        year_entry = Entry(user_details_window,width=8)
        year_entry.place(x=240,y=130)
        year_label = Label(user_details_window,text="YYYY",background="grey",fg="whitesmoke",font=("Arial",12))
        year_label.place(x=240,y=150)
        phone_no_label=Label(user_details_window,text="Phone Number",background="grey",fg="whitesmoke",font=("Arial",12))
        phone_no_label.place(x=20,y=190)
        phone_no_entry=Entry(user_details_window,width=20)
        phone_no_entry.place(x=160,y=190)
        email_label = Label(user_details_window,text="Email",background="grey",fg="whitesmoke",font=("Arial",12))
        email_label.place(x=310,y=190)
        email_entry = Entry(user_details_window,width=25)
        email_entry.place(x=420,y=190)
        
        password_label = Label(user_details_window,text="Password",background="grey",fg="whitesmoke",font=("Arial",12))
        password_label.place(x=20,y=230)
        password_entry = Entry(user_details_window,width=25,show="*")
        password_entry.place(x=160,y=230)
        confirm_password_label = Label(user_details_window,text="Confirm Password",background="grey",fg="whitesmoke",font=("Arial",12))
        confirm_password_label.place(x=20,y=270)
        confirm_password_entry = Entry(user_details_window,width=25,show="*")
        confirm_password_entry.place(x=160,y=270)
        register_button = Button(user_details_window,background="lavender",width=20,height=2,text="Register",command=lambda:[validate_registration_data()])
        register_button.place(x=250,y=320)

        def validate_registration_data():
            first_name = fname_entry.get()
            last_name = lname_entry.get()
            gender = gender_var.get()
            phone_num = phone_no_entry.get()
            email = email_entry.get()
            day_of_birth = day_entry.get()
            month_of_birth = month_entry.get()
            year_of_birth = year_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                email_msg = "Invalid Email"
                messagebox.showinfo('message',email_msg)
                return
            elif len(password) < 8:
                password_msg = "Password must be longer than eight characters"
                messagebox.showinfo('message',password_msg)
                return
            elif not re.search(r"[A-Z]",password):
                password_msg = "Password must have at least one uppercase letter"
                messagebox.showinfo('message',password_msg)
                return
            elif not re.search(r"\d",password):
                password_msg = "Password must have at least one number"
                messagebox.showinfo('message',password_msg)
                return
            elif password != confirm_password:
                password_msg = "Passwords must match"
                messagebox.showinfo('message',password_msg)
                return
            else:
                global registration_data
                hashed_password = hash_password(password)
                dateofbirth = get_date_of_birth(day_of_birth,month_of_birth,year_of_birth)
                registration_data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "gender": gender,
                    "dob": dateofbirth,
                    "phone_no": phone_num,
                    "email": email,
                    "password":hashed_password
                }
                user.job_poster_registration(registration_data["first_name"],registration_data["last_name"],registration_data["email"],registration_data["phone_no"],registration_data["gender"],registration_data["dob"],registration_data["password"])
                messagebox.showinfo('message',"User succesfully added\nProceed to Login")
                user_details_window.destroy()
                home_frame.destroy()
                home_menu_bar.destroy()
                login_page()

        user_details_window.mainloop()

    home_nav = Button(home_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3)
    home_nav.place(x=10,y=10)
    login_nav = Button(home_menu_bar,background="lavender",width=15,height=3,text="Login",fg="black",bd=3,command=lambda: [home_frame.destroy(),home_menu_bar.destroy(),login_page()])
    login_nav.place(x=10,y=90)
    if session["logged_in"] is True :
        new1_nav = Button(home_menu_bar,background="lavender",width=15,height=3,text="Post Job",fg="black",bd=3,command=lambda: [home_frame.destroy(),home_menu_bar.destroy(),post_job_form()])
        new1_nav.place(x=10,y=170)
        new2_nav = Button(home_menu_bar,background="lavender",width=15,height=3,text="View Jobs",fg="black",bd=3,command=lambda: [home_frame.destroy(),home_menu_bar.destroy(),view_jobs()])
        new2_nav.place(x=10,y=250)
        new3_nav = Button(home_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3)
        new3_nav.place(x=10,y=330)

    home_pg.mainloop()

def login_page():
    home_pg.title("Login")

    login_menu_bar = Frame(home_pg,bg="dimgrey",width=150,height=1280)
    login_menu_bar.pack(side=LEFT)

    login_frame = Frame(home_pg,bg="wheat",borderwidth=10,width=550,height=1280)
    login_frame.pack(expand=True,fill=BOTH)

    form_frame = Frame(login_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    Label(form_frame,fg="whitesmoke",font=("Arial",20),background="gray",text="Login Form").pack(fill=NONE,anchor=CENTER,pady=30)
    
    Label(form_frame,fg="whitesmoke",font=("Arial",12),background="gray",text="Email Address").pack(fill=NONE,anchor=CENTER)
    login_email_entry = Entry(form_frame,width=30)
    login_email_entry.pack(fill=NONE,anchor=CENTER,pady=10)
    
    Label(form_frame,fg="whitesmoke",font=("Arial",12),background="gray",text="Password").pack(fill=BOTH,anchor=CENTER)
    login_password_entry = Entry(form_frame,width=30,show="*")
    login_password_entry.pack(fill=NONE,anchor=CENTER,pady=10)
    
    show_password_button = Button(form_frame,background="grey",text="Show Password",width=12,command=lambda:[toggle_show_password()])
    show_password_button.pack(fill=NONE,anchor=CENTER,pady=10)

    def toggle_show_password():
        if login_password_entry.cget("show") == "":
            login_password_entry.config(show="*")
            show_password_button.config(text="Show Password")
        else:
            login_password_entry.config(show="")
            show_password_button.config(text="Hide Password")

    def user_login():
        input_password = login_password_entry.get()
        input_email = login_email_entry.get()
        login_user,user_type = user.login(input_email,input_password)
        if login_user is not None:
            session["username"] = login_user[6]
            session["logged_in"] = True
            if user_type is "job_seeker":
                session["session_id"] = login_user[10]
            else:
                session["session_id"] = login_user[9]
            session["user_type"] = user_type
            msg = login_user[1] + " " + login_user[2] +" successfully logged in"
            messagebox.showinfo('message',msg)
            login_frame.destroy()
            login_menu_bar.destroy()
            home()
        else:
            msg1 = "Invalid usermane/password"
            messagebox.showinfo('message',msg1)
    
    Button(form_frame,background="grey",width=10,text="Login",command=lambda:[user_login()]).pack(fill=NONE,anchor=CENTER,pady=30)

    home_nav = Button(login_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3,command=lambda:[login_frame.destroy(),login_menu_bar.destroy(),home()])
    home_nav.place(x=10,y=10)
    reg_nav = Button(login_menu_bar,background="lavender",width=15,height=3,text="Register",fg="black",bd=3,command=lambda: [login_frame.destroy(),login_menu_bar.destroy(),registration_page()])
    reg_nav.place(x=10,y=90)
    if session["logged_in"] is True:
        new1_nav = Button(login_menu_bar,background="lavender",width=15,height=3,text="Show Jobs",fg="black",bd=3,command=lambda: [login_frame.destroy(),login_menu_bar.destroy(),post_job_form()])
        new1_nav.place(x=10,y=170)
        new2_nav = Button(login_menu_bar,background="lavender",width=15,height=3,text="View Jobs",fg="black",bd=3,command=lambda: [login_frame.destroy(),login_menu_bar.destroy(),view_jobs()])
        new2_nav.place(x=10,y=250)
        new3_nav = Button(login_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3)
        new3_nav.place(x=10,y=330)

    home_pg.mainloop()

def registration_page():
    home_pg.title("Login")

    registration_menu_bar = Frame(home_pg,bg="dimgrey",width=150,height=1280)
    registration_menu_bar.pack(side=LEFT)

    registration_frame = Frame(home_pg,bg="wheat",borderwidth=10,width=550,height=1280)
    registration_frame.pack(expand=True,fill=BOTH)

    form_frame = Frame(registration_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    def user_details_form():
        user_details_window = Tk()
        user_details_window.geometry('700x400')
        user_details_window.configure(background="gray")
        f_name_label=Label(user_details_window,text="First Name",background="grey",fg="whitesmoke",font=("Arial",12))
        f_name_label.place(x=20,y=50)
        fname_entry=Entry(user_details_window,width=30)
        fname_entry.place(x=160,y=50)
        l_name_label=Label(user_details_window,fg="whitesmoke",font=("Arial",12),background="gray",text="    Last Name")
        l_name_label.place(x=310,y=50)
        lname_entry=Entry(user_details_window,width=30)
        lname_entry.place(x=420,y=50)
        
        gender_label = Label(user_details_window,text="Gender",background="grey",fg="whitesmoke",font=("Arial",12))
        gender_label.place(x=20,y=90)
        gender_var = StringVar(user_details_window)
        Radiobutton(user_details_window,text="Male",variable=gender_var,value="M",background="grey").place(x=160,y=90)
        Radiobutton(user_details_window,text="Female",variable=gender_var,value="F",background="grey").place(x=220,y=90)

        dob_label = Label(user_details_window,text="Date of Birth",background="grey",fg="whitesmoke",font=("Arial",12))
        dob_label.place(x=20,y=130)
        day_entry = Entry(user_details_window,width=5)
        day_entry.place(x=160,y=130)
        day_label = Label(user_details_window,text="DD",background="grey",fg="whitesmoke",font=("Arial",12))
        day_label.place(x=160,y=150)
        month_entry = Entry(user_details_window,width=5)
        month_entry.place(x=200,y=130)
        month_label = Label(user_details_window,text="MM",background="grey",fg="whitesmoke",font=("Arial",12))
        month_label.place(x=200,y=150)
        year_entry = Entry(user_details_window,width=8)
        year_entry.place(x=240,y=130)
        year_label = Label(user_details_window,text="YYYY",background="grey",fg="whitesmoke",font=("Arial",12))
        year_label.place(x=240,y=150)

        phone_no_label=Label(user_details_window,text="Phone Number",background="grey",fg="whitesmoke",font=("Arial",12))
        phone_no_label.place(x=20,y=190)
        phone_no_entry=Entry(user_details_window,width=20)
        phone_no_entry.place(x=160,y=190)
        email_label = Label(user_details_window,text="Email",background="grey",fg="whitesmoke",font=("Arial",12))
        email_label.place(x=310,y=190)
        email_entry = Entry(user_details_window,width=25)
        email_entry.place(x=420,y=190)
        
        password_label = Label(user_details_window,text="Password",background="grey",fg="whitesmoke",font=("Arial",12))
        password_label.place(x=20,y=230)
        password_entry = Entry(user_details_window,width=25,show="*")
        password_entry.place(x=160,y=230)

        confirm_password_label = Label(user_details_window,text="Confirm Password",background="grey",fg="whitesmoke",font=("Arial",12))
        confirm_password_label.place(x=20,y=270)
        confirm_password_entry = Entry(user_details_window,width=25,show="*")
        confirm_password_entry.place(x=160,y=270)

        register_button = Button(user_details_window,background="lavender",width=20,height=2,text="Register",command=lambda:[validate_registration_data()])
        register_button.place(x=250,y=320)

        def validate_registration_data():
            first_name = fname_entry.get()
            last_name = lname_entry.get()
            gender = gender_var.get()
            area = area_entry.get()
            phone_num = phone_no_entry.get()
            email = email_entry.get()
            category = specialty_entry.get()
            day_of_birth = day_entry.get()
            month_of_birth = month_entry.get()
            year_of_birth = year_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                email_msg = "Invalid Email"
                messagebox.showinfo('message',email_msg)
                return
            elif len(password) < 8:
                password_msg = "Password must be longer than eight characters"
                messagebox.showinfo('message',password_msg)
                return
            elif not re.search(r"[A-Z]",password):
                password_msg = "Password must have at least one uppercase letter"
                messagebox.showinfo('message',password_msg)
                return
            elif not re.search(r"\d",password):
                password_msg = "Password must have at least one number"
                messagebox.showinfo('message',password_msg)
                return
            elif password != confirm_password:
                password_msg = "Passwords must match"
                messagebox.showinfo('message',password_msg)
                return
            else:
                global registration_data
                date_of_birth = get_date_of_birth(day_of_birth,month_of_birth,year_of_birth)
                hashed_password = hash_password(password)
                registration_data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "gender": gender,
                    "dob": date_of_birth,
                    "area": area,
                    "phone_no": phone_num,
                    "email": email,
                    "category": category,
                    "password":hashed_password
                }
                user.job_seeker_registration(registration_data["first_name"],registration_data["last_name"],registration_data["email"],registration_data["phone_no"],registration_data["gender"],registration_data["dob"],registration_data["category"],registration_data["area"],registration_data["password"])
                messagebox.showinfo('message',"User succesfully added\nProceed to Login")
                user_details_window.destroy()
                registration_frame.destroy()
                registration_menu_bar.destroy()
                login_page()

        user_details_window.mainloop()

    specialty_label = Label(form_frame,text="Choose a Category",background="grey",fg="whitesmoke",font=("Arial",12))
    specialty_label.pack(fill=NONE,anchor=CENTER,pady=10)
    var2 = StringVar(form_frame)
    var2.set("Delivery")
    categories0 = ["Delivery","Electrictian","Farming","Laundry Services"]
    specialty_entry = AutocompleteCombobox(form_frame,completevalues=categories0)
    specialty_entry.pack(fill=NONE,anchor=CENTER,pady=10)

    areas = ["Balozi Road","Chuna"]
    area_label = Label(form_frame,text="Which area are you from",background="grey",fg="whitesmoke",font=("Arial",12))
    area_label.pack(fill=NONE,anchor=CENTER,pady=10)
    var3 = StringVar(form_frame)
    var3.set("Balozi Road")
    areas = ["Balozi Road","Chuna"]
    area_entry = AutocompleteCombobox(form_frame,completevalues=areas)
    area_entry.pack(fill=NONE,anchor=CENTER,pady=10)

    submit_button = Button(form_frame,background="lavender",width=30,height=2,text="Enter personal details",command=lambda: [user_details_form()])
    submit_button.pack(fill=NONE,anchor=CENTER,pady=10)

    home_nav = Button(registration_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3,command=lambda:[registration_frame.destroy(),registration_menu_bar.destroy(),home()])
    home_nav.place(x=10,y=10)
    login_nav = Button(registration_menu_bar,background="lavender",width=15,height=3,text="Login",fg="black",bd=3,command=lambda: [registration_frame.destroy(),registration_menu_bar.destroy(),login_page()])
    login_nav.place(x=10,y=90)
    if session["logged_in"] is True:
        new1_nav = Button(registration_menu_bar,background="lavender",width=15,height=3,text="Post Job",fg="black",bd=3)
        new1_nav.place(x=10,y=170)
        new2_nav = Button(registration_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3)
        new2_nav.place(x=10,y=250)
        new3_nav = Button(registration_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3)
        new3_nav.place(x=10,y=330)

    home_pg.mainloop()

def post_job_form():
    home_pg.title("Post a Job")

    post_job_menu_bar = Frame(home_pg,bg="dimgrey",width=150,height=1280)
    post_job_menu_bar.pack(side=LEFT)

    post_job_frame = Frame(home_pg,bg="wheat",borderwidth=10,width=550,height=1280)
    post_job_frame.pack(expand=True,fill=BOTH)

    form_frame = Frame(post_job_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    category_label = Label(form_frame,text="Job Category ",background="grey",fg="whitesmoke",font=("Arial",12))
    category_label.place(x=0,y=30)
    var3 = StringVar(form_frame)
    var3.set("Delivery")
    categories = ["Delivery Person","Electrictian","Laundry Services"]
    category_entry = AutocompleteCombobox(form_frame,completevalues=categories)
    category_entry.place(x=150,y=30)

    description_label = Label(form_frame,text="Job Description ",background="grey",fg="whitesmoke",font=("Arial",12))
    description_label.place(x=0,y=70)
    description_entry = Text(form_frame,width=25,height=5)
    description_entry.place(x=150,y=70)

    job_duration_label = Label(form_frame,text="Job length/duration",background="grey",fg="whitesmoke",font=("Arial",12))
    job_duration_label.place(x=0,y=170)
    global job_duration_var
    job_duration_var = StringVar(None,"S")
    Radiobutton(form_frame,text="Small  (1-5 hours)",value="S",background="grey",variable=job_duration_var).place(x=160,y=170)
    Radiobutton(form_frame,text="Medium (5-12 hours)",value="M",background="grey",variable=job_duration_var).place(x=160,y=190)
    Radiobutton(form_frame,text="Large  (More than one working day)",value="L",background="grey",variable=job_duration_var).place(x=160,y=210)
    
    amount_label = Label(form_frame,text="Amount",background="grey",fg="whitesmoke",font=("Arial",12))
    amount_label.place(x=0,y=240)
    amount_entry = Entry(form_frame,width=10)
    amount_entry.place(x=160,y=240)

    def save_job_data():
        input_job_category = category_entry.get()
        input_job_description = description_entry.get("1.0","end")
        input_job_duration = job_duration_var.get()
        input_job_amount = amount_entry.get()

        job.save_job(session["session_id"],input_job_category,input_job_description,input_job_duration,input_job_amount)

        messagebox.showinfo("Job Posted","Job Posted Succesfully")
        post_job_frame.destroy()
        post_job_menu_bar.destroy()
        home()

    post_job_button = Button(form_frame,background="lavender",width=15,text="Post Job",command=lambda: [save_job_data()])
    post_job_button.place(x=240,y=300)

    home_nav = Button(post_job_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3,command=lambda:[post_job_frame.destroy(),post_job_menu_bar.destroy(),home()])
    home_nav.place(x=10,y=10)
    login_nav = Button(post_job_menu_bar,background="lavender",width=15,height=3,text="Login",fg="black",bd=3,command=lambda: [post_job_frame.destroy(),post_job_menu_bar.destroy(),login_page()])
    login_nav.place(x=10,y=90)
    if session["logged_in"] is True:
        new1_nav = Button(post_job_menu_bar,background="lavender",width=15,height=3,text="Post Job",fg="black",bd=3 )
        new1_nav.place(x=10,y=170)
        new2_nav = Button(post_job_menu_bar,background="lavender",width=15,height=3,text="View Jobs",fg="black",bd=3)
        new2_nav.place(x=10,y=250)
        new3_nav = Button(post_job_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3)
        new3_nav.place(x=10,y=330)

    home_pg.mainloop()

def view_jobs():
    home_pg.title("Jobs Posted")

    view_jobs_menu_bar = Frame(home_pg,bg="dimgrey",width=150,height=1280)
    view_jobs_menu_bar.pack(side=LEFT)

    view_jobs_frame = Frame(home_pg,bg="wheat",borderwidth=10,width=550,height=1280)
    view_jobs_frame.pack(expand=True,fill=BOTH)

    scrollbar = Scrollbar(view_jobs_frame)
    scrollbar.pack(side="right",fill='y')

    form_frame = Canvas(view_jobs_frame,bg="gray",borderwidth=10)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    scrollbar.config(command=form_frame.yview)

    form_frame.configure(yscrollcommand=scrollbar.set)

    inner_frame = Frame(form_frame,bg="gray")
    form_frame.create_window((10, 0), window=inner_frame, anchor="center")

    jobs = job.get_jobs_posted()
    job_buttons = []

    def apply_job(job_id):
        job.job_application(session["session_id"],job_id)

    for i,a_job in enumerate(jobs):
        job_card = Frame(inner_frame,bg="gray",bd=2,relief="solid")
        job_card.pack(fill=X,padx=10,pady=20)
        job_label = Label(job_card,background="grey",text=a_job["job_category"],font=("Arial",'15'))
        job_label.pack(side=TOP)
        #job_label.grid(row=0,column=0)
        #job_label.place(x=0,y=0)
        job_description_label = Label(job_card,background="grey",width=50,height=2,text=a_job["job_description"],font=("Arial",'10'))
        #job_description_label.grid(row=1,column=0)
        job_description_label.pack(side=TOP)
        job_application_button = Button(job_card,text="Apply",command=lambda i=i+1:[apply_job(i)])
        job_buttons.append(job_application_button)
        job_application_button.pack(side=RIGHT,padx=10,pady=20)        

    form_frame.update_idletasks()
    form_frame.configure(scrollregion=form_frame.bbox('all'))

    home_nav = Button(view_jobs_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=5,command=lambda:[view_jobs_frame.destroy(),view_jobs_menu_bar.destroy(),home()])
    home_nav.place(x=10,y=10)
    login_nav = Button(view_jobs_menu_bar,background="lavender",width=15,height=3,text="Login",fg="black",bd=3,command=lambda: [view_jobs_frame.destroy(),view_jobs_menu_bar.destroy(),login_page()])
    login_nav.place(x=10,y=90)
    if session["logged_in"] is True:
        new1_nav = Button(view_jobs_menu_bar,background="lavender",width=15,height=3,text="Post Job",fg="black",bd=3)
        new1_nav.place(x=10,y=170)
        new2_nav = Button(view_jobs_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3)
        new2_nav.place(x=10,y=250)
        new3_nav = Button(view_jobs_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3)
        new3_nav.place(x=10,y=330)

    home_pg.mainloop()

home()