from tkinter import *
from tkinter.ttk import Combobox
from ttkwidgets.autocomplete import AutocompleteCombobox
from models import JobSeeker
import bcrypt

home_pg = Tk()
home_pg.geometry("900x500")
home_pg.configure(background="gray")
home_pg.resizable(0,0)
menu_bar = Frame(home_pg,bg="dimgrey",width=150,height=1280)
menu_bar.pack(side=LEFT)
login_frame = Frame(home_pg,bg="wheat",borderwidth=10,width=550,height=1280)
login_frame.pack(expand=True,fill=BOTH)

global fname_entry,lname_entry,registration_data

def home():
    home_pg.title("Home")
    home_frame = Frame(home_pg,bg="wheat",borderwidth=10,width=550,height=1280)
    home_frame.pack(expand=True,fill=BOTH)
    form_frame = Frame(login_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    Button(menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3).place(x=10,y=10)
    Button(menu_bar,background="lavender",width=15,height=3,text="Login",fg="black",bd=3,command=lambda: [home_frame.destroy(),form_frame.destroy(),login_page()]).place(x=10,y=90)
    Button(menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3).place(x=10,y=170)
    Button(menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3).place(x=10,y=250)
    Button(menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3).place(x=10,y=330)
    home_pg.mainloop()

def login_page():
    home_pg.title("Login")
    
    #Login Form starts here
    form_frame = Frame(login_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)
    Label(form_frame,fg="whitesmoke",font=("Arial",20),background="gray",text="Login Form").pack(fill=NONE,anchor=CENTER,pady=30)
    Label(form_frame,fg="whitesmoke",font=("Arial",12),background="gray",text="Email Address").pack(fill=NONE,anchor=CENTER)
    Entry(form_frame,width=30).pack(fill=NONE,anchor=CENTER,pady=10)
    Label(form_frame,fg="whitesmoke",font=("Arial",12),background="gray",text="Password").pack(fill=BOTH,anchor=CENTER)
    Entry(form_frame,width=30,show="*").pack(fill=NONE,anchor=CENTER,pady=10)
    Button(form_frame,background="grey",width=10,text="Login").pack(fill=NONE,anchor=CENTER,pady=30)

    #Navigation buttons
    Button(menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3,command=lambda: [form_frame.destroy(),home()]).place(x=10,y=10)
    if login_page:
        Button(menu_bar,background="lavender",width=15,height=3,text="Register",fg="black",bd=3,command=lambda: [form_frame.destroy(),register_page()]).place(x=10,y=90)
    else:
        Button(menu_bar,background="lavender",width=15,height=3,text="Login",fg="black",bd=3).place(x=10,y=90)
    Button(menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3).place(x=10,y=170)
    Button(menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3).place(x=10,y=250)
    Button(menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3).place(x=10,y=330)
    home_pg.mainloop()

def register_page():
    home_pg.title("Register")

    # Job Seeker Registration Form
    register_frame = Frame(login_frame,bg="gray",borderwidth=10,height=1280)
    register_frame.pack(expand=True,fill=BOTH,anchor=CENTER,padx=20,pady=20)
    name_frame = Frame(register_frame,bg="gray")
    name_frame.pack(fill=BOTH,expand=TRUE,anchor=CENTER)

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
        global gender_var
        gender_var = StringVar(None,"M")
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

        register_button = Button(user_details_window,background="lavender",width=20,height=2,text="Register",command=lambda:[get_date_of_birth(),hash_password(),validate_registration_data()])
        register_button.place(x=250,y=320)

        def get_date_of_birth():
            day_of_birth = day_entry.get()
            month_of_birth = month_entry.get()
            year_of_birth = year_entry.get()
            global date_of_birth
            date_of_birth = day_of_birth + "/" + month_of_birth + "/" + year_of_birth

        def hash_password():
            salt = b'$2b$12$SJv9T2zvJFjI6bYtibhZv.'
            new_password = password_entry.get()
            new_pass_bytes = new_password.encode('utf-8')
            new_hashed = bcrypt.hashpw(new_pass_bytes,salt)
            global hashed_password
            hashed_password = new_hashed.decode('utf-8')

        def validate_registration_data():
            global registration_data
            registration_data = {
                "first_name": fname_entry.get(),
                "last_name":lname_entry.get(),
                "gender":gender_var.get(),
                "dob":date_of_birth,
                "area":area_entry.get(),
                "phone_no":phone_no_entry.get(),
                "email":email_entry.get(),
                "category":specialty_entry.get(),
                "password":hashed_password
            }
            job_seeker = JobSeeker()
            job_seeker.save_data(registration_data["first_name"],registration_data["last_name"],registration_data["email"],registration_data["phone_no"],registration_data["gender"],registration_data["dob"],registration_data["category"],registration_data["area"],registration_data["password"])


        user_details_window.mainloop()

    specialty_label = Label(name_frame,text="Choose a Category",background="grey",fg="whitesmoke",font=("Arial",12))
    specialty_label.pack(fill=NONE,anchor=CENTER,pady=10)
    var2 = StringVar(name_frame)
    var2.set("Delivery")
    categories0 = ["Delivery","Electrictian","Farming","Laundry Services"]
    specialty_entry = AutocompleteCombobox(name_frame,completevalues=categories0)
    specialty_entry.pack(fill=NONE,anchor=CENTER,pady=10)

    areas = ["Balozi Road","Chuna"]
    area_label = Label(name_frame,text="Which area are you from",background="grey",fg="whitesmoke",font=("Arial",12))
    area_label.pack(fill=NONE,anchor=CENTER,pady=10)
    var3 = StringVar(name_frame)
    var3.set("Balozi Road")
    areas = ["Balozi Road","Chuna"]
    area_entry = AutocompleteCombobox(name_frame,completevalues=areas)
    area_entry.pack(fill=NONE,anchor=CENTER,pady=10)

    submit_button = Button(name_frame,background="lavender",width=30,height=2,text="Enter personal details",command=lambda: [user_details_form()])
    submit_button.pack(fill=NONE,anchor=CENTER,pady=10)

    Button(menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3,command=lambda: [register_frame.destroy(),home()]).place(x=10,y=10)
    if register_page:
        Button(menu_bar,background="lavender",width=15,height=3,text="Login",fg="black",bd=3,command=lambda: [register_frame.destroy(),login_page()]).place(x=10,y=90)
    else:
        Button(menu_bar,background="lavender",width=15,height=3,text="Register",fg="black",bd=3).place(x=10,y=90)
    Button(menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3).place(x=10,y=170)
    Button(menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3).place(x=10,y=250)
    Button(menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3).place(x=10,y=330)
    home_pg.mainloop()

def job_creation_form():
    home_pg.title("Home")
    home_frame = Frame(home_pg,bg="wheat",borderwidth=10,width=550,height=1280)
    home_frame.pack(expand=True,fill=BOTH)
    form_frame = Frame(login_frame,bg="gray",borderwidth=10,height=1280)
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

    date_posted_label = Label(form_frame,text="Posted on ",background="grey",fg="whitesmoke",font=("Arial",12))
    date_posted_label.place(x=0,y=165)
    day_posted_entry = Entry(form_frame,width=5)
    day_posted_entry.place(x=150,y=165)
    day_posted_label = Label(form_frame,text="DD",background="grey",fg="whitesmoke",font=("Arial",12))
    day_posted_label.place(x=150,y=185)
    month_posted_entry = Entry(form_frame,width=5)
    month_posted_entry.place(x=190,y=165)
    month_posted_label = Label(form_frame,text="MM",background="grey",fg="whitesmoke",font=("Arial",12))
    month_posted_label.place(x=190,y=185)
    year_posted_entry = Entry(form_frame,width=8)
    year_posted_entry.place(x=230,y=165)
    year_posted_label = Label(form_frame,text="YYYY",background="grey",fg="whitesmoke",font=("Arial",12))
    year_posted_label.place(x=230,y=185)

    job_duration_label = Label(form_frame,text="Job length/duration",background="grey",fg="whitesmoke",font=("Arial",12))
    job_duration_label.place(x=0,y=210)
    global var4
    var4 = StringVar(None,"S")
    Radiobutton(form_frame,text="Small  (1-5 hours)",value="S",background="grey",variable=var4).place(x=160,y=210)
    Radiobutton(form_frame,text="Medium (5-12 hours)",value="M",background="grey",variable=var4).place(x=160,y=230)
    Radiobutton(form_frame,text="Large  (More than one working day)",value="L",background="grey",variable=var4).place(x=160,y=250)
    
    payment_label = Label(form_frame,text="Payment",background="grey",fg="whitesmoke",font=("Arial",12))
    payment_label.place(x=0,y=280)
    global var5
    var5 = StringVar(None,"O")
    Radiobutton(form_frame,text="One Time",value="O",background="grey",variable=var5).place(x=160,y=280)
    Radiobutton(form_frame,text="Hourly",value="H",background="grey",variable=var5).place(x=160,y=300)
    amount_label = Label(form_frame,text="Amount",background="grey",fg="whitesmoke",font=("Arial",12))
    amount_label.place(x=0,y=340)
    amount_entry = Entry(form_frame,width=10)
    amount_entry.place(x=160,y=340)

    Button(menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3).place(x=10,y=10)
    Button(menu_bar,background="lavender",width=15,height=3,text="Login",fg="black",bd=3,command=lambda: [home_frame.destroy(),form_frame.destroy(),login_page()]).place(x=10,y=90)
    Button(menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3).place(x=10,y=170)
    Button(menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3).place(x=10,y=250)
    Button(menu_bar,background="lavender",width=15,height=3,text="Home",fg="black",bd=3).place(x=10,y=330)
    home_pg.mainloop()

register_page()