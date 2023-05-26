from tkinter import *
from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox
from models import User,Job,get_areas_array
import re,datetime
from validate import *
from PIL import Image,ImageTk

session = {
    "username": None,
    "user_id" : None,
    "session_id": None,
    "user_type": None,
    "logged_in": False,
    "category": None,
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
    session["category"] = None
    session["user_id"] = None
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
        Button(form_frame,text="Job Seeker",command=lambda:[home_frame.destroy(),home_menu_bar.destroy(),registration_page("job_seeker")]).place(x=100,y=30)
        Button(form_frame,text="Job Poster",command=lambda:[home_frame.destroy(),home_menu_bar.destroy(),registration_page("job_poster")]).place(x=20,y=30)
    else:
        Button(form_frame,text="View Jobs",command=lambda:[]).place(x=20,y=30)

    home_nav = Button(home_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3)
    home_nav.place(x=10,y=10)
    login_nav = Button(home_menu_bar,background="lavender",width=15,height=3,text="Login",fg="black",bd=3,command=lambda: [home_frame.destroy(),home_menu_bar.destroy(),login_page()])
    login_nav.place(x=10,y=90)
    if session["logged_in"] is True :
        new1_nav = Button(home_menu_bar,background="lavender",width=15,height=3,text="Post Job",fg="black",bd=3,command=lambda: [home_frame.destroy(),home_menu_bar.destroy(),post_job_form()])
        new1_nav.place(x=10,y=170)
        if session["user_type"] is "job_seeker":
            new2_nav = Button(home_menu_bar,background="lavender",width=15,height=3,text="View Jobs",fg="black",bd=3,command=lambda: [home_frame.destroy(),home_menu_bar.destroy(),view_jobs()])
            new2_nav.place(x=10,y=250)
        else:
            new2_nav = Button(home_menu_bar,background="lavender",width=15,height=3,text="View Jobs",fg="black",bd=3,command=lambda: [home_frame.destroy(),home_menu_bar.destroy(),job_posters_jobs_view()])
            new2_nav.place(x=10,y=250)
        new3_nav = Button(home_menu_bar,background="lavender",width=15,height=3,text="View Profile",fg="black",bd=3, command=lambda:[home_frame.destroy(),home_menu_bar.destroy(),profile_pg(session["user_id"])])
        new3_nav.place(x=10,y=330)
        new4_nav = Button(home_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3, command=lambda:[home_frame.destroy(),home_menu_bar.destroy(),logout()])
        new4_nav.place(x=10,y=410)

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
            session["username"] = login_user["email"]
            session["user_id"] = login_user["id"]
            session["logged_in"] = True
            if user_type is "job_seeker":
                session["category"] = login_user["category"]
            else:
                session["category"] = None
            session["user_type"] = user_type
            session["session_id"] = login_user["session_id"]
            msg = login_user["first_name"] + " " + login_user["last_name"] +" successfully logged in"
            messagebox.showinfo('Login',msg)
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
        new3_nav = Button(login_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3,command=lambda:[login_frame.destroy(),login_menu_bar.destroy(),logout()])
        new3_nav.place(x=10,y=330)

    home_pg.mainloop()

def registration_page(user_type):
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

        show_password = Button(user_details_window,text="Show Password",command=lambda:[toggle_show_hide_password()])
        show_password.place(x=350,y=270)
        
        def toggle_show_hide_password():
            if password_entry.cget("show") == "" and confirm_password_entry.cget("show") == "":
                password_entry.config(show="*")
                confirm_password_entry.config(show="*")
                show_password.config(text="Show Password")
            else:
                password_entry.config(show="")
                confirm_password_entry.config(show="")
                show_password.config(text="Hide Password")

        register_button = Button(user_details_window,background="lavender",width=20,height=2,text="Register",command=lambda:[validate_registration_data()])
        register_button.place(x=250,y=320)

        def validate_registration_data():
            first_name = fname_entry.get()
            last_name = lname_entry.get()
            gender = gender_var.get()
            area = area_entry.get()
            phone_num = phone_no_entry.get()
            email = email_entry.get()
            if user_type is "job_seeker":
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
                if user_type is "job_seeker":
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
                elif user_type is "job_poster":
                    registration_data = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "gender": gender,
                        "dob": date_of_birth,
                        "area": area,
                        "phone_no": phone_num,
                        "email": email,
                        "password":hashed_password
                    }
                    user.job_poster_registration(registration_data["first_name"],registration_data["last_name"],registration_data["email"],registration_data["phone_no"],registration_data["gender"],registration_data["dob"],registration_data["password"],registration_data["area"])
                messagebox.showinfo('message',"User succesfully added\nProceed to Login")
                user_details_window.destroy()
                registration_frame.destroy()
                registration_menu_bar.destroy()
                login_page()

        user_details_window.mainloop()

    if user_type is "job_seeker":
        specialty_label = Label(form_frame,text="Choose a Category",background="grey",fg="whitesmoke",font=("Arial",12))
        specialty_label.pack(fill=NONE,anchor=CENTER,pady=10)
        var2 = StringVar(form_frame)
        var2.set("Delivery")
        categories0 = ["Delivery","Electrictian","Farming","Laundry Services"]
        global specialty_entry
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
        new3_nav = Button(registration_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3,command=lambda:[registration_frame.destroy(),registration_menu_bar.destroy(),logout()])
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
    description_entry = Text(form_frame,width=60,height=7)
    description_entry.place(x=150,y=70)

    duration_label = Label(form_frame,text="Job Duration(in hours)",background="grey",fg="whitesmoke",font=("Arial",12))
    duration_label.place(x=0,y=200)
    value_label = Label(form_frame, text="0", background="white",width=3)
    value_label.place(x=200, y=200)
    MAX_VALUE = 8
    MIN_VALUE = 1
    def increment():
        current_value = int(value_label['text'])
        if current_value < MAX_VALUE:
            new_value = current_value + 1
            value_label['text'] = str(new_value)
    def decrement():
        current_value = int(value_label['text'])
        if current_value > MIN_VALUE:
            new_value = current_value - 1
            value_label['text'] = str(new_value)
    def get_value():
        return int(value_label["text"])
    increment_button = Button(form_frame, text="+", height=1,command=increment)
    increment_button.place(x=260, y=200)
    decrement_button = Button(form_frame, text="-", height=1, command=decrement)
    decrement_button.place(x=160, y=200)
    
    amount_label = Label(form_frame,text="Amount",background="grey",fg="whitesmoke",font=("Arial",12))
    amount_label.place(x=0,y=240)
    amount_entry = Entry(form_frame,width=10)
    amount_entry.place(x=160,y=240)
    p_hr_label = Label(form_frame,text="/hr",background="grey",fg="whitesmoke",font=("Arial",12))
    p_hr_label.place(x=220,y=240)

    job_location_label =Label(form_frame,text="Job location",background="grey",fg="whitesmoke",font=("Arial",12))
    job_location_label.place(x=0,y=280)
    areas = ["Balozi Road","Chuna"]
    area_entry = AutocompleteCombobox(form_frame,completevalues=areas)
    area_entry.place(x=160,y=280)

    def save_job_data():
        input_job_category = category_entry.get()
        input_job_description = description_entry.get("1.0","end-1c")
        input_job_duration = get_value()
        input_job_rate = amount_entry.get()
        input_job_location = area_entry.get()

        job.save_job(session["session_id"],input_job_category,input_job_description,input_job_duration,input_job_rate,input_job_location)

        messagebox.showinfo("Job Posted","Job Posted Succesfully")
        post_job_frame.destroy()
        post_job_menu_bar.destroy()
        home()

    post_job_button = Button(form_frame,background="lavender",width=15,text="Post Job",command=lambda: [save_job_data()])
    post_job_button.place(x=240,y=340)

    home_nav = Button(post_job_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3,command=lambda:[post_job_frame.destroy(),post_job_menu_bar.destroy(),home()])
    home_nav.place(x=10,y=10)
    login_nav = Button(post_job_menu_bar,background="lavender",width=15,height=3,text="Login",fg="black",bd=3,command=lambda: [post_job_frame.destroy(),post_job_menu_bar.destroy(),login_page()])
    login_nav.place(x=10,y=90)
    if session["logged_in"] is True:
        new1_nav = Button(post_job_menu_bar,background="lavender",width=15,height=3,text="Post Job",fg="black",bd=3 )
        new1_nav.place(x=10,y=170)
        new2_nav = Button(post_job_menu_bar,background="lavender",width=15,height=3,text="View Jobs",fg="black",bd=3)
        new2_nav.place(x=10,y=250)
        new3_nav = Button(post_job_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3,command=lambda:[post_job_frame.destroy(),post_job_menu_bar.destroy(),logout()])
        new3_nav.place(x=10,y=330)

    home_pg.mainloop()

def update_job_form(job_id):
    home_pg.title("Update Job Details")

    update_job = job.get_specified_job(job_id)

    update_job_menu_bar = Frame(home_pg,bg="dimgrey",width=150,height=1280)
    update_job_menu_bar.pack(side=LEFT)

    update_job_frame = Frame(home_pg,bg="wheat",borderwidth=10,width=550,height=1280)
    update_job_frame.pack(expand=True,fill=BOTH)

    form_frame = Frame(update_job_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    category_label = Label(form_frame,text="Job Category ",background="grey",fg="whitesmoke",font=("Arial",12))
    category_label.place(x=0,y=30)
    var3 = StringVar(form_frame)
    var3.set("Delivery")
    categories = ["Delivery Person","Electrictian","Laundry Services"]
    category_entry = AutocompleteCombobox(form_frame,completevalues=categories)
    category_entry.set(update_job["job_category"])
    category_entry.place(x=150,y=30)

    description_label = Label(form_frame,text="Job Description ",background="grey",fg="whitesmoke",font=("Arial",12))
    description_label.place(x=0,y=70)
    description_entry = Text(form_frame,width=60,height=7)
    description_entry.insert('1.0',update_job["job_description"])
    description_entry.place(x=150,y=70)


    duration_label = Label(form_frame,text="Job Duration(in hours)",background="grey",fg="whitesmoke",font=("Arial",12))
    duration_label.place(x=0,y=200)
    value_label = Label(form_frame, text=int(update_job["job_duration"]), background="white",width=3)
    value_label.place(x=200, y=200)
    MAX_VALUE = 8
    MIN_VALUE = 1
    def increment():
        current_value = int(value_label['text'])
        if current_value < MAX_VALUE:
            new_value = current_value + 1
            value_label['text'] = str(new_value)
    def decrement():
        current_value = int(value_label['text'])
        if current_value > MIN_VALUE:
            new_value = current_value - 1
            value_label['text'] = str(new_value)
    def get_value():
        return int(value_label["text"])
    increment_button = Button(form_frame, text="+", height=1,command=increment)
    increment_button.place(x=260, y=200)
    decrement_button = Button(form_frame, text="-", height=1, command=decrement)
    decrement_button.place(x=160, y=200)
    
    amount_var = StringVar()
    amount_var.set(update_job["total_amount"])
    amount_label = Label(form_frame,text="Amount",background="grey",fg="whitesmoke",font=("Arial",12))
    amount_label.place(x=0,y=240)
    amount_entry = Entry(form_frame,width=10,textvariable=amount_var)
    amount_entry.place(x=160,y=240)
    p_hr_label = Label(form_frame,text="/hr",background="grey",fg="whitesmoke",font=("Arial",12))
    p_hr_label.place(x=220,y=240)

    job_location_label =Label(form_frame,text="Amount",background="grey",fg="whitesmoke",font=("Arial",12))
    job_location_label.place(x=0,y=280)
    areas = ["Balozi Road","Chuna"]
    area_entry = AutocompleteCombobox(form_frame,completevalues=areas)
    area_entry.set(update_job["job_location"])
    area_entry.place(x=160,y=280)

    def update_job_data():
        input_job_category = category_entry.get()
        input_job_description = description_entry.get("1.0","end-1c")
        input_job_duration = get_value()
        input_job_rate = amount_entry.get()
        input_job_location = area_entry.get()

        job.update_job(job_id,input_job_category,input_job_description,input_job_duration,input_job_rate,input_job_location)

        messagebox.showinfo("Job Details Updated","Job Details Updated Succesfully")
        update_job_frame.destroy()
        update_job_menu_bar.destroy()
        job_posters_jobs_view()

    update_job_button = Button(form_frame,background="lavender",width=15,text="Update Job",command=lambda: [update_job_data()])
    update_job_button.place(x=240,y=340)

    home_nav = Button(update_job_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3,command=lambda:[update_job_frame.destroy(),update_job_menu_bar.destroy(),home()])
    home_nav.place(x=10,y=10)
    login_nav = Button(update_job_menu_bar,background="lavender",width=15,height=3,text="Login",fg="black",bd=3,command=lambda: [update_job_frame.destroy(),update_job_menu_bar.destroy(),login_page()])
    login_nav.place(x=10,y=90)
    if session["logged_in"] is True:
        new1_nav = Button(update_job_menu_bar,background="lavender",width=15,height=3,text="Post Job",fg="black",bd=3 )
        new1_nav.place(x=10,y=170)
        new2_nav = Button(update_job_menu_bar,background="lavender",width=15,height=3,text="View Jobs",fg="black",bd=3)
        new2_nav.place(x=10,y=250)
        new3_nav = Button(update_job_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3,command=lambda:[update_job_frame.destroy(),update_job_menu_bar.destroy(),logout()])
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

    inner_frame = Frame(form_frame,bg="gray")
    form_frame.create_window((10, 0), window=inner_frame, anchor="center")

    search_frame = Frame(inner_frame,bg="gray")
    search_frame.pack(fill=X)

    names,ids = user.get_job_posters()
    areas = get_areas_array()
    payment_options = ["less than 900","900-2100","greater than 2100"]
    duration_options = ["less than 6 hours","6-10 hours","more than 10 hours"]

    category_search = AutocompleteCombobox(search_frame,completevalues=["Electrictian","Delivery Person","Laundry Services"],width=12)
    category_search.pack(side=LEFT,padx=10)
    category_search.set("Category")
    location_search = AutocompleteCombobox(search_frame,completevalues=areas,width=12)
    location_search.pack(side=LEFT,padx=10)
    location_search.set("Location")
    payment_rate_search = AutocompleteCombobox(search_frame,completevalues=payment_options,width=12)
    payment_rate_search.pack(side=LEFT,padx=10)
    payment_rate_search.set("Amount")
    duration_search = AutocompleteCombobox(search_frame,completevalues=duration_options,width=12)
    duration_search.pack(side=LEFT,padx=10)
    duration_search.set("Job duration")
    search_button = Button(search_frame,text="Search",command=lambda:[search_jobs(),create_cards_function()])
    search_button.pack(side=LEFT,padx=10)

    def search_jobs():
        payment_index =  payment_rate_search.current()
        duration_index = duration_search.current()
        if payment_index == 0:
            payment_1 = 0
            payment_2 = 899
        elif payment_index == 1:
            payment_1 = 900
            payment_2 = 2099
        elif payment_index == 2:
            payment_1 = 2100
            payment_2 = 210000
        else:
            payment_1 = None
            payment_2 = None
        if duration_index ==0:
            duration_1 = 1
            duration_2 = 10
        elif duration_index ==1:
            duration_1 = 11
            duration_2 = 20
        elif duration_index ==2:
            duration_1 = 21
            duration_2 = 100
        else:
            duration_1 = None
            duration_2 = None
        searched_jobs = job.search_jobs(category_search.get(),duration_1,duration_2,payment_1,payment_2,location_search.get())
        return searched_jobs

    applications = job.get_application(session["session_id"])

    def apply_job(button,job_id):
        if button.cget("text") == "Apply":
            button.config(text="Withdraw Application")
            job.job_application(session["session_id"],job_id)
        else:
            button.config(text="Withdraw Application")
            button.config(text="Apply")
            job.remove_application(session["session_id"],job_id)

    def create_card(parent, card_label, description, id, amount, date):
        job_card = Frame(parent,bg="white",bd=2,relief="solid",borderwidth=10)
        job_card.pack(fill=X,padx=10,pady=20)
        job_label = Label(job_card,background="white",text=card_label,font=("Arial",'15', "bold"))
        job_label.pack(side=TOP,anchor=W)
        job_description_label = Label(job_card,background="white",text=description,width=50,height=2,font=("Arial",'12', "italic"),justify=LEFT)
        job_description_label.pack(anchor=W)
        posted_on_label = Label(job_card,background="white",text="Posted on " + str(date),width=50,height=2,font=("Arial",'12', "italic"),justify=LEFT,fg="black")
        posted_on_label.pack(anchor=W)
        job_amount_label = Label(job_card,background="white",text="Amount: Kshs." + str(amount),width=50,height=2,font=("Arial",'12', "italic"),justify=LEFT,fg="green")
        job_amount_label.pack(anchor=W)
        button_text = StringVar(job_card)
        if ([id] in applications) is True:
            button_text = "Withdraw Application"
        else:
            button_text = "Apply"
        job_application_button = Button(job_card,bg="blue",fg="white",text=button_text,command=lambda:[apply_job(job_application_button,id)])
        job_application_button.pack(side=RIGHT,padx=10,pady=20)
        view_button = Button(job_card,text="View Job",bg="blue",fg="white",command=lambda:[view_jobs_frame.destroy(),view_jobs_menu_bar.destroy(),job_details_page(id)])
        view_button.pack(side=RIGHT,padx=10,pady=20)

        return job_card

    cards = []
    jobs = job.get_category_jobs(session["category"])
    if len(jobs) == 0:
        none_label = Label(inner_frame,background="grey",text="No Jobs Found",font=("Arial",'15'))
        none_label.pack()
    for a_job in jobs:
        job_amount = int(a_job["job_duration"])*int(a_job["total_amount"])
        date_str = str(a_job["date_posted"])
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        new_date = datetime.strptime(date_str, date_format)
        formatted_date = new_date.strftime("%B %d, %Y %I:%M %p")
        card = create_card(inner_frame,a_job["job_category"],a_job["job_description"],a_job["job_id"],job_amount,formatted_date)
        cards.append(card)

    def create_cards_function():
        for widg in inner_frame.winfo_children():
            if widg != search_frame:
                widg.destroy()
        jobs = search_jobs()
        if len(jobs) == 0:
            none_label = Label(inner_frame,background="grey",text="No Jobs Found",font=("Arial",'15'))
            none_label.pack()
        else:
            for a_job in jobs:
                job_amount = int(a_job["job_duration"])*int(a_job["total_amount"])
                date_str = str(a_job["date_posted"])
                date_format = "%Y-%m-%d %H:%M:%S.%f"
                new_date = datetime.strptime(date_str, date_format)
                formatted_date = new_date.strftime("%B %d, %Y %I:%M %p")
                card = create_card(inner_frame,a_job["job_category"],a_job["job_description"],a_job["job_id"],job_amount,formatted_date)
                cards.append(card)

        form_frame.update_idletasks()
        form_frame.configure(scrollregion=form_frame.bbox('all'))
        form_frame.yview_moveto(0.0)
    
    form_frame.update_idletasks()
    form_frame.configure(scrollregion=form_frame.bbox('all'))
    form_frame.yview_moveto(0.0)
    scrollbar.config(command=form_frame.yview)
    form_frame.config(yscrollcommand=scrollbar.set)

    home_nav = Button(view_jobs_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=5,command=lambda:[view_jobs_frame.destroy(),view_jobs_menu_bar.destroy(),home()])
    home_nav.place(x=10,y=10)
    login_nav = Button(view_jobs_menu_bar,background="lavender",width=15,height=3,text="Login",fg="black",bd=3,command=lambda: [view_jobs_frame.destroy(),view_jobs_menu_bar.destroy(),login_page()])
    login_nav.place(x=10,y=90)
    if session["logged_in"] is True:
        new1_nav = Button(view_jobs_menu_bar,background="lavender",width=15,height=3,text="Post Job",fg="black",bd=3)
        new1_nav.place(x=10,y=170)
        new2_nav = Button(view_jobs_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3)
        new2_nav.place(x=10,y=250)
        new3_nav = Button(view_jobs_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3,command=lambda:[view_jobs_frame.destroy(),view_jobs_menu_bar.destroy(),logout()])
        new3_nav.place(x=10,y=330)

    home_pg.mainloop()

def job_posters_jobs_view():
    home_pg.title("Jobs Posted")

    view_jobs_menu_bar = Frame(home_pg,bg="dimgrey",width=150,height=1280)
    view_jobs_menu_bar.pack(side=LEFT)

    view_jobs_frame = Frame(home_pg,bg="wheat",borderwidth=10,width=550,height=1280)
    view_jobs_frame.pack(expand=True,fill=BOTH)

    scrollbar = Scrollbar(view_jobs_frame)
    scrollbar.pack(side="right",fill='y')

    form_frame = Canvas(view_jobs_frame,bg="gray",borderwidth=10)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    inner_frame = Frame(form_frame,bg="gray")
    form_frame.create_window((10, 0), window=inner_frame, anchor="center")

    select_jobs_frame = Frame(inner_frame,bg="gray")
    select_jobs_frame.pack(fill=X,side=TOP)

    jobs_done_button = Button(select_jobs_frame,text="Jobs Completed",bg="grey",fg="black",command=lambda:[create_cards_funtion("true")])
    jobs_done_button.pack(side=LEFT,padx=10)

    jobs_not_done_button = Button(select_jobs_frame,text="Jobs Not Completed",bg="grey",fg="black",command=lambda:[create_cards_funtion("false")])
    jobs_not_done_button.pack(side=LEFT,padx=10)

    def display_applicants(job_id):
        display_applicants_window = Tk()
        display_applicants_window.geometry('400x400')
        job_applications = job.get_job_applications(job_id)
        applicants_frame = Canvas(display_applicants_window)

        applicant_scrollbar = Scrollbar(display_applicants_window,command=applicants_frame.yview)
        applicant_scrollbar.pack(side="right",fill='y')

        def create_applicant_cards(card_label, date_applied, applicant_id,application_status, job):
            applicant_card = Frame(display_applicants_window,bg="white",bd=2,relief="solid")
            applicant_card.pack(fill=X,padx=10,pady=20)
            applicant_name_label = Label(applicant_card,text="Applicant Name: " + card_label,background="grey",fg="black",font=("Arial","13"))
            applicant_name_label.pack(side=TOP)
            date_applied_label = Label(applicant_card,text=f"Applied on: {date_applied}",background="grey",fg="black",font=("Arial","13"))
            date_applied_label.pack(side=TOP)
            view_profile_button = Button(applicant_card,text="View User profile",command=lambda:[])
            view_profile_button.pack(side=RIGHT,padx=10,pady=20)

            if application_status == "ND":
                button_text = "Select Applicant"
            elif application_status == "S":
                button_text = "Remove Applicant"

            select_applicant_button = Button(applicant_card,text=button_text,command=lambda:[select_unselect_applicant(select_applicant_button,applicant_id,job)])
            select_applicant_button.pack(side=RIGHT,padx=10,pady=20)

            return applicant_card
        
        def select_unselect_applicant(button,applicant_id,job_id):
            if button.cget("text") == "Select Applicant":
                button.config(text="Remove Applicant")
                job.select_job_applicant(applicant_id,job_id)
            else:
                button.config(text="Remove Applicant")
                button.config(text="Select Applicant")
                job.unselect_job_applicant(applicant_id)

        if len(job_applications) is 0:
            no_applicants_label = Label(display_applicants_window,background="grey",text="No Applicants",font=("Arial",'15'))
            no_applicants_label.place(x=20,y=40)
        else:
            inner_applicants_frame = Frame(applicants_frame,bg="gray")
            applicants_frame.create_window((10,0),window=inner_applicants_frame,anchor="center")
            applicant_cards=[]
            for application in job_applications:
                applicant = user.get_job_seeker(application["applicant"])
                applicant_card = create_applicant_cards(applicant,application["application_date"],application["application_id"],application["application_status"],application["job"])
                applicant_cards.append(applicant_card)

        applicants_frame.update_idletasks()
        applicants_frame.configure(scrollregion=applicants_frame.bbox('all'))
        
        applicants_frame.yview_moveto(0.0)
        applicant_scrollbar.config(command=applicants_frame.yview)
        applicants_frame.config(yscrollcommand=applicant_scrollbar.set)

        display_applicants_window.mainloop()

    def job_rating(job_id):
        rating_window = Tk()
        rating_window.geometry("400x400")
        rating_window.title("Job Rating")

        rating_var = IntVar(rating_window)

        rating_label = Label(rating_window, text="Rate our service (1-5 stars):")
        rating_label.pack(pady=(20, 5))

        rating_scale = Scale(rating_window,from_=1,to=5,orient=HORIZONTAL,variable=rating_var)
        rating_scale.pack()

        comment_label = Label(rating_window,text="Add a coment/review(optional):")
        comment_label.pack(pady=(20, 5))

        comment_entry = Text(rating_window,height=10,width=30)
        comment_entry.pack()

        def submit_rating():
            rating = rating_var.get()
            comment = comment_entry.get('1.0','end')
            job.post_job_rating(job_id,int(rating),comment)
            rating_window.destroy()
            view_jobs_frame.destroy()
            view_jobs_menu_bar.destroy()
            job_posters_jobs_view()

        submit_button = Button(rating_window, text="Submit Rating", command=submit_rating)
        submit_button.pack(pady=20)

        rating_window.mainloop()

    jobs = job.get_user_jobs(session["session_id"])

    def create_card(parent, card_label, description, id, done_by, status):
        job_card = Frame(parent,bg="white",bd=2,relief="solid")
        job_card.pack(fill=X,padx=10,pady=20)
        job_label = Label(job_card,background="white",text=card_label,font=("Arial",'15'))
        job_label.pack(side=TOP,anchor=NW)
        job_description_label = Label(job_card,background="white",text=description,width=50,height=2,font=("Arial",'10'))
        job_description_label.pack(side=TOP,anchor=NW)
        if status == "true":
            job_status_label = Label(job_card,background="white",text="Job Completed",width=50,height=2,font=("Arial",'10'))
            job_status_label.pack(side=TOP,anchor=NW)
        else:
            job_applicants_button = Button(job_card,text="View Applicants",bg="blue",fg="white",command=lambda:[display_applicants(id)])
            job_applicants_button.pack(side=RIGHT,padx=10,pady=20)
        view_button = Button(job_card,text="View Job",bg="blue",fg="white",command=lambda:[view_jobs_frame.destroy(),view_jobs_menu_bar.destroy(),job_details_page(id)])
        view_button.pack(side=RIGHT,padx=10,pady=20)
        update_job_button = Button(job_card,text="Update Job",bg="blue",fg="white",command=lambda:[view_jobs_frame.destroy(),view_jobs_menu_bar.destroy(),update_job_form(id)])
        update_job_button.pack(side=RIGHT,padx=10,pady=20)
        if done_by is not None:
            job_done_button = Button(job_card,text="Job Completed",bg="blue",fg="white",command=lambda:[job.mark_done_job(id),job_rating(id)])
            job_done_button.pack(side=RIGHT,padx=10,pady=20)

        return job_card

    cards = []

    def create_cards_funtion(status):
        for widget in inner_frame.winfo_children():
            if widget != select_jobs_frame:
                widget.destroy()
        jobs = job.get_user_jobs_by_status(session["session_id"],status)
        if len(jobs) == 0:
            no_jobs_label = Label(inner_frame,text="No Jobs",bg="gray",fg="black",font=("Arial","15"),justify=CENTER)
            no_jobs_label.pack()
        else:
            if status == "true":
                for a_job in jobs:
                    card = create_card(inner_frame,a_job["job_category"],a_job["job_description"],a_job["job_id"],a_job["done_by"],a_job["job_status"])
                    cards.append(card)
            elif status == "false":
                for a_job in jobs:
                    card = create_card(inner_frame,a_job["job_category"],a_job["job_description"],a_job["job_id"],a_job["done_by"],a_job["job_status"])
                    cards.append(card)

    if len(jobs) == 0:
        no_jobs_label = Label(inner_frame,text="No Jobs",bg="gray",fg="black",font=("Arial","15"),justify=CENTER)
        no_jobs_label.pack()
    else:
        for a_job in jobs:
            card = create_card(inner_frame,a_job["job_category"],a_job["job_description"],a_job["job_id"],a_job["done_by"],a_job["job_status"])
            cards.append(card)

    form_frame.update_idletasks()
    form_frame.configure(scrollregion=form_frame.bbox('all'))
    form_frame.yview_moveto(0.0)

    scrollbar.config(command=form_frame.yview)
    form_frame.config(yscrollcommand=scrollbar.set)

    home_nav = Button(view_jobs_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=5,command=lambda:[view_jobs_frame.destroy(),view_jobs_menu_bar.destroy(),home()])
    home_nav.place(x=10,y=10)
    login_nav = Button(view_jobs_menu_bar,background="lavender",width=15,height=3,text="Login",fg="black",bd=3,command=lambda: [view_jobs_frame.destroy(),view_jobs_menu_bar.destroy(),login_page()])
    login_nav.place(x=10,y=90)
    if session["logged_in"] is True:
        new1_nav = Button(view_jobs_menu_bar,background="lavender",width=15,height=3,text="Post Job",fg="black",bd=3)
        new1_nav.place(x=10,y=170)
        new2_nav = Button(view_jobs_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3)
        new2_nav.place(x=10,y=250)
        new3_nav = Button(view_jobs_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3,command=lambda:[view_jobs_frame.destroy(),view_jobs_menu_bar.destroy(),logout()])
        new3_nav.place(x=10,y=330)

    home_pg.mainloop()

def job_details_page(job_id):
    page_title = f"Job J-{job_id}"

    spec_job = job.get_specified_job(job_id)

    home_pg.title(page_title)

    job_details_menu_bar = Frame(home_pg,bg="dimgrey",width=150,height=1280)
    job_details_menu_bar.pack(side=LEFT)

    job_details_frame = Frame(home_pg,bg="wheat",borderwidth=10,width=550,height=1280)
    job_details_frame.pack(expand=True,fill=BOTH)

    form_frame = Frame(job_details_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    job_id_label = Label(form_frame,text=f"Job J-{job_id}",background="grey",fg="black",font=("Arial",20))
    job_id_label.place(x=20,y=0)

    job_category_var = StringVar(form_frame)
    job_category_var.set(spec_job["job_category"])
    job_category_label = Label(form_frame,text="Category",background="grey",fg="black",font=("Arial",12))
    job_category_label.place(x=20,y=50)
    job_category_value = Entry(form_frame,text=job_category_var,fg="black",font=("Helvetica",10))
    job_category_value.place(x=150,y=50)
    job_category_value.configure(state="disabled")

    job_description_label = Label(form_frame, text="Bio: ",background="grey",fg="black",font=("Helvetica",12))
    job_description_label.place(x=20,y=80)
    job_description_value = Text(form_frame,width=40,height=5)
    job_description_value.place(x=150,y=80)
    job_description_value.insert('1.0',spec_job["job_description"])
    job_description_value.config(state=DISABLED)

    job_date_var = StringVar(form_frame)
    job_date_var.set(spec_job["date_posted"])
    job_date_label = Label(form_frame,text="Date posted",background="grey",fg="black",font=("Arial",12))
    job_date_label.place(x=20,y=180)
    job_date_value = Entry(form_frame,text=job_date_var,fg="black",font=("Helvetica",10))
    job_date_value.place(x=150,y=180)
    job_date_value.configure(state="disabled")

    posted_user = user.get_job_poster(spec_job["posted_by"])
    posted_by_var = StringVar(form_frame)
    posted_by_var.set(posted_user)
    posted_by_label = Label(form_frame,text="Posted by",background="grey",fg="black",font=("Arial",12))
    posted_by_label.place(x=20,y=210)
    posted_by_value = Entry(form_frame,text=posted_by_var,fg="black",font=("Helvetica",10))
    posted_by_value.place(x=150,y=210)
    posted_by_value.configure(state="disabled")

    if spec_job["done_by"]  is not None:
        done_by_user = user.get_job_seeker(spec_job["done_by"])
    else:
        done_by_user = "No one selected yet"
    done_by_var = StringVar(form_frame)
    done_by_var.set(done_by_user)
    done_by_label = Label(form_frame,text="Done by",background="grey",fg="black",font=("Arial",12))
    done_by_label.place(x=20,y=240)
    done_by_value = Entry(form_frame,text=done_by_var,fg="black",font=("Helvetica",10))
    done_by_value.place(x=150,y=240)
    done_by_value.configure(state="disabled")

    job_duration_var = StringVar(form_frame)
    job_duration_var.set(str(spec_job["job_duration"]))
    job_duration_label = Label(form_frame,text="Job Duration(hrs)",background="grey",fg="black",font=("Arial",12))
    job_duration_label.place(x=20,y=270)
    job_duration_value = Entry(form_frame,text=job_duration_var,fg="black",font=("Helvetica",10))
    job_duration_value.place(x=150,y=270)
    job_duration_value.configure(state="disabled")

    job_cost_var = StringVar(form_frame)
    job_cost_var.set(spec_job["total_amount"])
    job_cost_label = Label(form_frame,text="Total Amount",background="grey",fg="black",font=("Arial",12))
    job_cost_label.place(x=20,y=300)
    job_cost_value = Entry(form_frame,text=posted_by_var,fg="black",font=("Helvetica",10))
    job_cost_value.place(x=150,y=300)
    job_cost_value.configure(state="disabled")

    no_of_applicants = job.get_no_of_applicants(job_id)
    no_of_applicants_var = StringVar(form_frame)
    no_of_applicants_var.set(str(no_of_applicants))
    no_of_applicants_label = Label(form_frame,text="No. of applicants",background="grey",fg="black",font=("Arial",12))
    no_of_applicants_label.place(x=20,y=300)
    no_of_applicants_value = Entry(form_frame,text=no_of_applicants_var,fg="black",font=("Helvetica",10))
    no_of_applicants_value.place(x=150,y=300)
    no_of_applicants_value.configure(state="disabled")

    home_nav = Button(job_details_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=5,command=lambda:[job_details_frame.destroy(),job_details_menu_bar.destroy(),home()])
    home_nav.place(x=10,y=10)
    login_nav = Button(job_details_menu_bar,background="lavender",width=15,height=3,text="Login",fg="black",bd=3,command=lambda: [job_details_frame.destroy(),job_details_menu_bar.destroy(),login_page()])
    login_nav.place(x=10,y=90)
    if session["logged_in"] is True:
        new1_nav = Button(job_details_menu_bar,background="lavender",width=15,height=3,text="Post Job",fg="black",bd=3)
        new1_nav.place(x=10,y=170)
        new2_nav = Button(job_details_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3)
        new2_nav.place(x=10,y=250)
        new3_nav = Button(job_details_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3,command=lambda:[job_details_frame.destroy(),job_details_menu_bar.destroy(),logout()])
        new3_nav.place(x=10,y=330)

    home_pg.mainloop()

def profile_pg(user_id):
    if session["user_type"] is "job_seeker":
        users_profile = user.get_job_seeker_dict(user_id)
    elif session["user_type"] is "job_poster":
        users_profile = user.get_job_poster_dict(user_id)

    full_name = users_profile["first_name"] + " " + users_profile["last_name"]

    home_pg.title(f"{full_name}'s Profile")

    profile_page_menu_bar = Frame(home_pg,bg="dimgrey",width=150,height=1280)
    profile_page_menu_bar.pack(side=LEFT)

    profile_page_frame = Frame(home_pg,bg="wheat",borderwidth=10,width=550,height=1280)
    profile_page_frame.pack(expand=True,fill=BOTH)

    form_frame = Frame(profile_page_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    img =Image.open("profile_pics/cap.png")
    img = img.resize((100, 100))
    tk_img = ImageTk.PhotoImage(img)
    img_label = Label(form_frame, image=tk_img)
    img_label.place(x=10,y=10)

    full_name_var = StringVar(form_frame)
    full_name_var.set(users_profile["first_name"] + " " + users_profile["last_name"])
    full_name_label = Label(form_frame, text="Full Name: ",background="grey",fg="black",font=("Helvetica",12))
    full_name_label.place(x=130,y=10)
    full_name_value = Entry(form_frame, text=full_name_var,fg="black",font=("Helvetica",10))
    full_name_value.configure(state="disabled")
    full_name_value.place(x=270,y=10)

    gender_var = StringVar(form_frame)
    if users_profile["gender"] == 'M':
        gender_var.set("Male")
    else:
        gender_var.set("Female")
    gender_display_label = Label(form_frame, text="Gender: ",background="grey",fg="black",font=("Helvetica",12))
    gender_display_label.place(x=130,y=40)
    gender_display_value = Entry(form_frame, text=gender_var,fg="black",font=("Helvetica",10))
    gender_display_value.configure(state="disabled")
    gender_display_value.place(x=270,y=40)

    dob_var = StringVar(form_frame)
    dob_var.set(users_profile["dob"])
    dob_display_label = Label(form_frame, text="Date of Birth: ",background="grey",fg="black",font=("Helvetica",12))
    dob_display_label.place(x=130,y=70)
    dob_display_value = Entry(form_frame, text=dob_var,fg="black",font=("Helvetica",10))
    dob_display_value.configure(state="disabled")
    dob_display_value.place(x=270,y=70)

    phone_num_var = StringVar(form_frame)
    phone_num_var.set(users_profile["phone_num"])
    phone_num_label = Label(form_frame, text="Phone number: ",background="grey",fg="black",font=("Helvetica",12))
    phone_num_label.place(x=130,y=100)
    phone_num_values = Entry(form_frame, text=phone_num_var,background="grey",fg="black",font=("Helvetica",10))
    phone_num_values.configure(state="disabled")
    phone_num_values.place(x=270,y=100)

    email_var = StringVar(form_frame)
    email_var.set(users_profile["email"])
    email_label = Label(form_frame, text="Email: ",background="grey",fg="black",font=("Helvetica",12))
    email_label.place(x=130,y=130)
    email_values = Entry(form_frame, text=email_var,background="grey",fg="black",font=("Helvetica",10))
    email_values.configure(state="disabled")
    email_values.place(x=270,y=130)

    bio_display_label = Label(form_frame, text="Bio: ",background="grey",fg="black",font=("Helvetica",12))
    bio_display_label.place(x=130,y=160)
    bio_value = Text(form_frame,width=40,height=5)
    bio_value.place(x=270,y=160)
    bio_value.insert('1.0',users_profile["overview"])
    bio_value.config(state=DISABLED)

    if session["user_type"] == "job_seeker":
        job_categories_var = StringVar(form_frame)
        job_categories_var.set(users_profile["category"])
        job_categories_label = Label(form_frame, text="Job Categories: ",background="grey",fg="black",font=("Helvetica",12))
        job_categories_label.place(x=130,y=260)
        job_categories_values = Entry(form_frame,text=job_categories_var,fg="black",font=("Helvetica",10))
        job_categories_values.configure(state="disabled")
        job_categories_values.place(x=270,y=260)

        rate_var = StringVar(form_frame)
        rate_var.set(users_profile["rate"])
        rate_label = Label(form_frame, text="Payment rate/hour: ",background="grey",fg="black",font=("Helvetica",12))
        rate_label.place(x=130,y=290)
        rate_values = Entry(form_frame,text=rate_var,fg="black",font=("Helvetica",10))
        rate_values.configure(state="disabled")
        rate_values.place(x=270,y=290)
    
    def update_profile_window():
        update_profile_page = Tk()
        update_profile_page.geometry("700x500")
        update_profile_page.title(users_profile["first_name"] + " " + users_profile["last_name"] + "'s profile")
        update_profile_page.configure(background="gray")

        fname_var = StringVar(update_profile_page)
        fname_var.set(users_profile["first_name"])
        f_name_label=Label(update_profile_page,text="First Name",background="grey",fg="whitesmoke",font=("Arial",12))
        f_name_label.place(x=20,y=50)
        fname_entry=Entry(update_profile_page,width=30,text=fname_var)
        fname_entry.place(x=160,y=50)
        lname_var = StringVar(update_profile_page)
        lname_var.set(users_profile["last_name"])
        l_name_label=Label(update_profile_page,fg="whitesmoke",font=("Arial",12),background="gray",text="    Last Name")
        l_name_label.place(x=310,y=50)
        lname_entry=Entry(update_profile_page,width=30,text=lname_var)
        lname_entry.place(x=420,y=50)

        phone_no_var = StringVar(update_profile_page)
        phone_no_var.set(users_profile["phone_num"])
        phone_no_label=Label(update_profile_page,text="Phone Number",background="grey",fg="whitesmoke",font=("Arial",12))
        phone_no_label.place(x=20,y=90)
        phone_no_entry=Entry(update_profile_page,width=20,text=phone_no_var)
        phone_no_entry.place(x=160,y=90)
        update_email_var = StringVar(update_profile_page)
        update_email_var.set(users_profile["email"])
        email_label = Label(update_profile_page,text="Email",background="grey",fg="whitesmoke",font=("Arial",12))
        email_label.place(x=330,y=90)
        email_entry = Entry(update_profile_page,width=25,text=update_email_var)
        email_entry.place(x=420,y=90)

        profile_pic_var = StringVar(update_profile_page)
        profile_pic_var.set(users_profile["profile_pic_path"])
        profile_pic_label = Label(update_profile_page,text="Profile picture",background="grey",fg="whitesmoke",font=("Arial",12))
        profile_pic_label.place(x=20,y=130)
        profile_pic_entry = Entry(update_profile_page,width=25,text=profile_pic_var)
        profile_pic_entry.place(x=160,y=130)
        profile_pic_entry.configure(state="disabled")
        change_profile_pic_button = Button(update_profile_page,text="Change",background="lavender",command=lambda:[])
        change_profile_pic_button.place(x=320,y=130)

        bio_update_label = Label(update_profile_page,text="Bio",background="grey",fg="whitesmoke",font=("Arial",12))
        bio_update_label.place(x=20,y=170)
        bio_update_entry = Text(update_profile_page,width=40,height=5)
        bio_update_entry.place(x=160,y=170)
        bio_update_entry.insert("1.0",users_profile["overview"])

        location_update_label = Label(update_profile_page,text="Location",background="grey",fg="whitesmoke",font=("Arial",12))
        location_update_label.place(x=20,y=270)
        areas = ["Balozi Road","Chuna"]
        location_update_entry = AutocompleteCombobox(update_profile_page,completevalues=areas)
        location_update_entry.set(users_profile["location"])
        location_update_entry.place(x=160,y=270)

        old_password_label = Label(update_profile_page,text="Password",background="grey",fg="whitesmoke",font=("Arial",12))
        old_password_label.place(x=20,y=310)
        old_password_entry = Entry(update_profile_page,width=25,show="*")
        old_password_entry.place(x=160,y=310)

        new_password_label = Label(update_profile_page,text="Confirm Password",background="grey",fg="whitesmoke",font=("Arial",12))
        new_password_label.place(x=20,y=350)
        new_password_entry = Entry(update_profile_page,width=25,show="*")
        new_password_entry.place(x=160,y=350)

        confirm_new_password_label = Label(update_profile_page,text="Confirm Password",background="grey",fg="whitesmoke",font=("Arial",12))
        confirm_new_password_label.place(x=20,y=390)
        confirm_new_password_entry = Entry(update_profile_page,width=25,show="*")
        confirm_new_password_entry.place(x=160,y=390)

        show_password = Button(update_profile_page,text="Show Password",command=lambda:[toggle_show_hide_password()])
        show_password.place(x=350,y=390)

        update_profile_button = Button(update_profile_page,text="Update Profile",background="lavender",command=lambda:[update_profile()])
        update_profile_button.place(x=200,y=420)

        def toggle_show_hide_password():
            if old_password_entry.cget("show") == "":
                old_password_entry.config(show="*")
                new_password_entry.config(show="*")
                confirm_new_password_entry.config(show="*")
                show_password.config(text="Show Password")
            else:
                old_password_entry.config(show="")
                confirm_new_password_entry.config(show="")
                new_password_entry.config(show="")
                show_password.config(text="Hide Password")

        def update_profile():
            first_name = fname_entry.get()
            last_name = lname_entry.get()
            phone_no = phone_no_entry.get()
            email = email_entry.get()
            profile_pic_path = profile_pic_entry.get()
            bio = bio_update_entry.get("1.0","end")
            location = location_update_entry.get()
            old_password = old_password_entry.get()
            new_password = new_password_entry.get()
            new_password_confrmation = confirm_new_password_entry.get()

            new_hashed_password = hash_password(new_password)
            old_hashed_password = hash_password(old_password)


            if new_password:
                #print(new_password)
                if users_profile["password"] != old_hashed_password:
                    password_msg = "Your old password is incorrect"
                    messagebox.showinfo('message',password_msg)
                    return
                elif len(new_password) < 8:
                    password_msg = "Password must be longer than eight characters"
                    messagebox.showinfo('message',password_msg)
                    return
                elif not re.search(r"[A-Z]",new_password):
                    password_msg = "Password must have at least one uppercase letter"
                    messagebox.showinfo('message',password_msg)
                    return
                elif not re.search(r"\d",new_password):
                    password_msg = "Password must have at least one number"
                    messagebox.showinfo('message',password_msg)
                    return
                elif new_password != new_password_confrmation:
                    password_msg = "Passwords must match"
                    messagebox.showinfo('message',password_msg)
                    return
                
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                email_msg = "Invalid Email"
                messagebox.showinfo('message',email_msg)
                
            if new_password:            
                update_data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "location": location,
                    "phone_no": phone_no,
                    "email": email,
                    "password":new_hashed_password,
                    "profile_pic_path": profile_pic_path,
                    "bio": bio
                }
                user.update_user_profile(session["session_id"],session["user_type"],update_data)
                    
            else:
                update_data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "location": location,
                    "phone_no": phone_no,
                    "email": email,
                    "password":users_profile["password"],
                    "profile_pic_path": profile_pic_path,
                    "bio": bio
                }
                user.update_user_profile(session["session_id"],session["user_type"],update_data)
                
            profile_page_frame.destroy()
            profile_page_menu_bar.destroy()
            update_profile_page.destroy()
            profile_pg(session["user_id"])
   
        update_profile_page.mainloop()

    update_profile_button = Button(form_frame,text="Update Profile",background="lavender",command=lambda:[update_profile_window()])
    update_profile_button.place(x=200,y=320)

    home_nav = Button(profile_page_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=5,command=lambda:[profile_page_frame.destroy(),profile_page_menu_bar.destroy(),home()])
    home_nav.place(x=10,y=10)
    login_nav = Button(profile_page_menu_bar,background="lavender",width=15,height=3,text="Login",fg="black",bd=3,command=lambda: [profile_page_frame.destroy(),profile_page_menu_bar.destroy(),login_page()])
    login_nav.place(x=10,y=90)
    if session["logged_in"] is True:
        if session["user_type"] is "job_poster":
            new1_nav = Button(profile_page_menu_bar,background="lavender",width=15,height=3,text="Post Job",fg="black",bd=3)
            new1_nav.place(x=10,y=170)
            new2_nav = Button(profile_page_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3)
            new2_nav.place(x=10,y=250)
            new3_nav = Button(profile_page_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3,command=lambda:[profile_page_frame.destroy(),profile_page_menu_bar.destroy(),logout()])
            new3_nav.place(x=10,y=330)
        elif session["user_type"] is "job_seeker":
            new1_nav = Button(profile_page_menu_bar,background="lavender",width=15,height=3,text="View Jobs",fg="black",bd=3)
            new1_nav.place(x=10,y=170)
            new3_nav = Button(profile_page_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3,command=lambda:[profile_page_frame.destroy(),profile_page_menu_bar.destroy(),logout()])
            new3_nav.place(x=10,y=250)

    home_pg.mainloop()

home()