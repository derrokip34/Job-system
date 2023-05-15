from tkinter import *
from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox
from models import User,Job
import re
from validate import *
from PIL import Image,ImageTk

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
        new3_nav = Button(home_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3, command=lambda:[home_frame.destroy(),home_menu_bar.destroy(),logout()])
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
            session["username"] = login_user["email"]
            session["logged_in"] = True
            if user_type is "job_seeker":
                session["session_id"] = login_user["session_id"]
            else:
                session["session_id"] = login_user["session_id"]
            session["user_type"] = user_type
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
        new3_nav = Button(login_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3)
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
                    user.job_poster_registration(registration_data["first_name"],registration_data["last_name"],registration_data["email"],registration_data["phone_no"],registration_data["gender"],registration_data["dob"],registration_data["password"])
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

    job_location_label =Label(form_frame,text="Amount",background="grey",fg="whitesmoke",font=("Arial",12))
    job_location_label.place(x=0,y=280)
    areas = ["Balozi Road","Chuna"]
    area_entry = AutocompleteCombobox(form_frame,completevalues=areas)
    area_entry.place(x=160,y=280)

    def save_job_data():
        input_job_category = category_entry.get()
        input_job_description = description_entry.get("1.0","end")
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

    inner_frame = Frame(form_frame,bg="gray")
    form_frame.create_window((10, 0), window=inner_frame, anchor="center")

    search_frame = Frame(inner_frame,bg="gray")
    search_frame.pack(fill=X)

    names,ids = user.get_job_posters()

    category_search = AutocompleteCombobox(search_frame,completevalues=["Electrictian","Delivery Person","Laundry Services"])
    category_search.pack(side=LEFT,padx=10)
    posted_by_search = AutocompleteCombobox(search_frame,completevalues=names)
    posted_by_search.pack(side=LEFT,padx=10)
    search_button = Button(search_frame,text="Search",command=lambda:[search_jobs(),create_cards_function()])
    search_button.pack(side=LEFT,padx=10)

    def search_jobs():
        selected_index = posted_by_search.current()
        if selected_index >= 0:
            searched_jobs = job.search_jobs(ids[selected_index],category_search.get())
        else:
            searched_jobs = job.get_jobs_posted()
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

    def create_card(parent, card_label, description, id):
        job_card = Frame(parent,bg="gray",bd=2,relief="solid")
        job_card.pack(fill=X,padx=10,pady=20)
        job_label = Label(job_card,background="grey",text=card_label,font=("Arial",'15'))
        job_label.pack(side=TOP)
        job_description_label = Label(job_card,background="grey",text=description,width=50,height=2,font=("Arial",'10'))
        job_description_label.pack(side=TOP)
        button_text = StringVar(job_card)
        if ([id] in applications) is True:
            button_text = "Withdraw Application"
        else:
            button_text = "Apply"
        job_application_button = Button(job_card,text=button_text,command=lambda:[apply_job(job_application_button,id)])
        job_application_button.pack(side=RIGHT,padx=10,pady=20)
        view_button = Button(job_card,text="View Job",command=lambda:[view_jobs_frame.destroy(),view_jobs_menu_bar.destroy(),job_details_page(id)])
        view_button.pack(side=RIGHT,padx=10,pady=20)

        return job_card

    cards = []

    def create_cards_function():
        for widg in inner_frame.winfo_children():
            if widg != search_frame:
                widg.destroy()
        jobs = search_jobs()

        for a_job in jobs:
            card = create_card(inner_frame,a_job["job_category"],a_job["job_description"],a_job["job_id"])
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
        new3_nav = Button(view_jobs_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3)
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

    def display_applicants(job_id):
        display_applicants_window = Tk()
        display_applicants_window.geometry('400x400')
        job_applications = job.get_job_applications(job_id)
        applicants_frame = Canvas(display_applicants_window)

        applicant_scrollbar = Scrollbar(display_applicants_window,command=applicants_frame.yview)
        applicant_scrollbar.pack(side="right",fill='y')

        def create_applicant_cards(card_label, date_applied, applicant_id,application_status):
            applicant_card = Frame(display_applicants_window,bg="gray",bd=2,relief="solid")
            applicant_card.pack(fill=X,padx=10,pady=20)
            applicant_name_label = Label(applicant_card,text="Applicant Name: " + card_label,background="grey",fg="black",font=("Arial","13"))
            applicant_name_label.pack(side=TOP)
            date_applied_label = Label(applicant_card,text=f"Applied on: {date_applied}",background="grey",fg="black",font=("Arial","13"))
            date_applied_label.pack(side=TOP)
            view_profile_button = Button(applicant_card,text="View User profile",command=lambda:[job.select_job_applicant(applicant_id)])
            view_profile_button.pack(side=RIGHT,padx=10,pady=20)

            if application_status == "ND":
                button_text = "Select Applicant"
            elif application_status == "S":
                button_text = "Remove Applicant"

            select_applicant_button = Button(applicant_card,text=button_text,command=lambda:[select_unselect_applicant(select_applicant_button,applicant_id)])
            select_applicant_button.pack(side=RIGHT,padx=10,pady=20)

            return applicant_card
        
        def select_unselect_applicant(button,applicant_id):
            if button.cget("text") == "Select Applicant":
                button.config(text="Remove Applicant")
                job.select_job_applicant(applicant_id)
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
                applicant_card = create_applicant_cards(applicant,application["application_date"],application["application_id"],application["application_status"])
                applicant_cards.append(applicant_card)

        applicants_frame.update_idletasks()
        applicants_frame.configure(scrollregion=applicants_frame.bbox('all'))
        
        applicants_frame.yview_moveto(0.0)
        applicant_scrollbar.config(command=applicants_frame.yview)
        applicants_frame.config(yscrollcommand=applicant_scrollbar.set)

        display_applicants_window.mainloop()

    def job_rating():
        print("Job done")

    jobs = job.get_user_jobs(session["session_id"])

    def create_card(parent, card_label, description, id):
        job_card = Frame(parent,bg="gray",bd=2,relief="solid")
        job_card.pack(fill=X,padx=10,pady=20)
        job_label = Label(job_card,background="grey",text=card_label,font=("Arial",'15'))
        job_label.pack(side=TOP)
        job_description_label = Label(job_card,background="grey",text=description,width=50,height=2,font=("Arial",'10'))
        job_description_label.pack(side=TOP)
        job_application_button = Button(job_card,text="View Applicants",command=lambda:[display_applicants(id)])
        job_application_button.pack(side=RIGHT,padx=10,pady=20)
        view_button = Button(job_card,text="View Job",command=lambda:[view_jobs_frame.destroy(),view_jobs_menu_bar.destroy(),job_details_page(id)])
        view_button.pack(side=RIGHT,padx=10,pady=20)
        job_done_button = Button(job_card,text="Job Completed",command=lambda:[job.mark_done_job(id),view_jobs_frame.destroy(),view_jobs_menu_bar.destroy(),job_rating(),job_details_page(id)])
        job_done_button.pack(side=RIGHT,padx=10,pady=20)

        return job_card

    cards = []

    for a_job in jobs:
        card = create_card(inner_frame,a_job["job_category"],a_job["job_description"],a_job["job_id"])
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
        new3_nav = Button(view_jobs_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3)
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

    job_id_label = Label(form_frame,text=f"Job J-{job_id}",background="grey",fg="whitesmoke",font=("Arial",20))
    job_id_label.place(x=20,y=0)

    job_category_label = Label(form_frame,text="Category:\t\t"+spec_job["job_category"],background="grey",fg="whitesmoke",font=("Arial",15))
    job_category_label.place(x=20,y=50)

    job_description_label = Label(form_frame,text="Description:\t",background="grey",fg="whitesmoke",font=("Arial",15))
    job_description_label.place(x=20,y=100)

    job_description_label2 = Label(form_frame,wraplength=400,text=spec_job["job_description"],background="grey",fg="whitesmoke",font=("Arial",15))
    job_description_label2.place(x=200,y=100)

    date = spec_job["date_posted"]
    date_posted_label = Label(form_frame,text=f"Posted on:\t{date}",background="grey",fg="whitesmoke",font=("Arial",15))
    date_posted_label.place(x=20,y=150)

    posted_user = user.get_job_poster(spec_job["posted_by"])
    posted_by_label = Label(form_frame,text=f"Posted by:\t" + posted_user,background="grey",fg="whitesmoke",font=("Arial",15))
    posted_by_label.place(x=20,y=200)

    if spec_job["done_by"]  is not None:
        done_by_user = user.get_job_seeker(spec_job["done_by"])
    else:
        done_by_user = "No one selected yet"
    done_by_label = Label(form_frame,text=f"Done by:\t\t" + done_by_user,background="grey",fg="whitesmoke",font=("Arial",15))
    done_by_label.place(x=20,y=250)

    if spec_job["job_duration"] is 'L':
        job_duration = "Large(More than one working day)"
    elif spec_job["job_duration"] is 'M':
        job_duration = "Medium(5-12 hours)"
    else:
        job_duration = "Small(1-5 hours)"
    duration_label = Label(form_frame,text=f"Job Duration by:\t" + job_duration,background="grey",fg="whitesmoke",font=("Arial",15))
    duration_label.place(x=20,y=300)

    job_cost = spec_job["total_amount"]
    job_cost_label = Label(form_frame,text=f"Price:\t\t{job_cost}" + " Kshs.",background="grey",fg="whitesmoke",font=("Arial",15))
    job_cost_label.place(x=20,y=350)

    home_nav = Button(job_details_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=5,command=lambda:[job_details_frame.destroy(),job_details_menu_bar.destroy(),home()])
    home_nav.place(x=10,y=10)
    login_nav = Button(job_details_menu_bar,background="lavender",width=15,height=3,text="Login",fg="black",bd=3,command=lambda: [job_details_frame.destroy(),job_details_menu_bar.destroy(),login_page()])
    login_nav.place(x=10,y=90)
    if session["logged_in"] is True:
        new1_nav = Button(job_details_menu_bar,background="lavender",width=15,height=3,text="Post Job",fg="black",bd=3)
        new1_nav.place(x=10,y=170)
        new2_nav = Button(job_details_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3)
        new2_nav.place(x=10,y=250)
        new3_nav = Button(job_details_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3)
        new3_nav.place(x=10,y=330)

    home_pg.mainloop()

def profile_pg(user_id):
    session["user_type"] = "job_seeker"
    if session["user_type"] is "job_seeker":
        profile,user_name = user.get_job_seeker(user_id)
    elif session["user_type"] is "job_poster":
        profile,user_name = user.get_job_poster(user_id)

    home_pg.title(f"{user_name}'s Profile")

    profile_page_menu_bar = Frame(home_pg,bg="dimgrey",width=150,height=1280)
    profile_page_menu_bar.pack(side=LEFT)

    profile_page_frame = Frame(home_pg,bg="wheat",borderwidth=10,width=550,height=1280)
    profile_page_frame.pack(expand=True,fill=BOTH)

    form_frame = Frame(profile_page_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    home_nav = Button(profile_page_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=5,command=lambda:[profile_page_frame.destroy(),profile_page_menu_bar.destroy(),home()])
    home_nav.place(x=10,y=10)
    login_nav = Button(profile_page_menu_bar,background="lavender",width=15,height=3,text="Login",fg="black",bd=3,command=lambda: [profile_page_frame.destroy(),profile_page_menu_bar.destroy(),login_page()])
    login_nav.place(x=10,y=90)
    if session["logged_in"] is True:
        new1_nav = Button(profile_page_menu_bar,background="lavender",width=15,height=3,text="Post Job",fg="black",bd=3)
        new1_nav.place(x=10,y=170)
        new2_nav = Button(profile_page_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3)
        new2_nav.place(x=10,y=250)
        new3_nav = Button(profile_page_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3)
        new3_nav.place(x=10,y=330)

    home_pg.mainloop()

def set_profile(user_id):
    session["user_type"] = "job_seeker"
    if session["user_type"] is "job_seeker":
        user_name = user.get_job_seeker(user_id)
    elif session["user_type"] is "job_poster":
        user_name = user.get_job_poster(user_id)

    home_pg.title(f"{user_name}'s Profile")

    set_profile_menu_bar = Frame(home_pg,bg="dimgrey",width=150,height=1280)
    set_profile_menu_bar.pack(side=LEFT)

    set_profile_frame = Frame(home_pg,bg="wheat",borderwidth=10,width=550,height=1280)
    set_profile_frame.pack(expand=True,fill=BOTH)

    form_frame = Frame(set_profile_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    img =Image.open("profile_pics/anonymous.png")
    img = img.resize((100, 100))
    tk_img = ImageTk.PhotoImage(img)
    img_label = Label(form_frame, image=tk_img)
    img_label.pack(anchor=NW)

    home_nav = Button(set_profile_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=5,command=lambda:[set_profile_frame.destroy(),set_profile_menu_bar.destroy(),home()])
    home_nav.place(x=10,y=10)
    login_nav = Button(set_profile_menu_bar,background="lavender",width=15,height=3,text="Login",fg="black",bd=3,command=lambda: [set_profile_frame.destroy(),set_profile_menu_bar.destroy(),login_page()])
    login_nav.place(x=10,y=90)
    if session["logged_in"] is True:
        new1_nav = Button(set_profile_menu_bar,background="lavender",width=15,height=3,text="Post Job",fg="black",bd=3)
        new1_nav.place(x=10,y=170)
        new2_nav = Button(set_profile_menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3)
        new2_nav.place(x=10,y=250)
        new3_nav = Button(set_profile_menu_bar,background="lavender",width=15,height=3,text="Logout",fg="black",bd=3)
        new3_nav.place(x=10,y=330)

    home_pg.mainloop()

home()