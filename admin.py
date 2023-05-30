from tkinter import *
from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox
from db_connection import *
import re

admin_session = {
    "admin_username": None,
    "logged_in": False,
}

admin_page = Tk()
admin_page.geometry("900x500")
admin_page.configure(background="gray")
admin_page.resizable(0,0)

def admin_registration():
    admin_page.title("Admin registration")

    admin_login_frame = Frame(admin_page,bg="wheat",borderwidth=10,width=550,height=1280)
    admin_login_frame.pack(expand=True,fill=BOTH)

    form_frame = Frame(admin_login_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    nav_frame = Frame(form_frame, bg="light gray")
    nav_frame.pack(side="top", pady=10, padx=90)

    login_button1 = Button(nav_frame, text="Login",width=12,command=lambda:[admin_login_frame.destroy(),admin_login()])
    login_button1.pack(side="left", padx=10,pady=10)

    register_button2 = Button(nav_frame, text="Register",width=12)
    register_button2.pack(side="left", padx=10,pady=10)

    #Registration form here
    name_label = Label(form_frame,fg="whitesmoke",font=("Arial",14),background="gray",text="Name")
    name_label.place(x=100,y=60)

    # First name and last name entries
    first_name_entry = Entry(form_frame, width=25)
    first_name_entry.place(x=100,y=90)

    last_name_entry = Entry(form_frame, width=25)
    last_name_entry.place(x=300,y=90)

    # Email label and entry
    email_label = Label(form_frame,fg="whitesmoke",font=("Arial",14),background="gray",text="Email")
    email_label.place(x=100,y=120)

    email_entry = Entry(form_frame, width=30)
    email_entry.place(x=100,y=150)

    # Password label and entry
    password_label = Label(form_frame,fg="whitesmoke",font=("Arial",14),background="gray",text="Password")
    password_label.place(x=100,y=180)

    password_entry = Entry(form_frame, show="*", width=30)
    password_entry.place(x=100,y=210)

    confirm_password_label = Label(form_frame,fg="whitesmoke",font=("Arial",14),background="gray",text="Confirm Password")
    confirm_password_label.place(x=100,y=240)

    confirm_password_entry = Entry(form_frame, show="*", width=30)
    confirm_password_entry.place(x=100,y=270)

    show_password = Button(form_frame,text="Show Password",command=lambda:[toggle_show_hide_password()])
    show_password.place(x=300,y=270)
        
    def toggle_show_hide_password():
        if password_entry.cget("show") == "" and confirm_password_entry.cget("show") == "":
            password_entry.config(show="*")
            confirm_password_entry.config(show="*")
            show_password.config(text="Show Password")
        else:
            password_entry.config(show="")
            confirm_password_entry.config(show="")
            show_password.config(text="Hide Password")

    # Register button
    register_button = Button(form_frame,background="lavender",width=20,height=2,text="Register",command=lambda:[register()])
    register_button.place(x=200,y=310)

    def register():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        hashed_password = hash_password(password)
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
            admin_user_data = {
                "first_name": first_name,
                "last_name": last_name,
                "password": hashed_password,
                "email": email
            }
            register_admin(admin_user_data)
        messagebox.showinfo('message',"User succesfully added\nProceed to Login")
        admin_login_frame.destroy()
        admin_login()

    admin_page.mainloop()

def admin_login():
    admin_page.title("Admin login")

    admin_login_frame = Frame(admin_page,bg="wheat",borderwidth=10,width=550,height=1280)
    admin_login_frame.pack(expand=True,fill=BOTH)

    form_frame = Frame(admin_login_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    nav_frame = Frame(form_frame, bg="light gray")
    nav_frame.pack(side="top", pady=10, padx=90)

    login_button1 = Button(nav_frame, text="Login",width=12)
    login_button1.pack(side="left", padx=10,pady=10)

    register_button2 = Button(nav_frame, text="Register",width=12,command=lambda:[admin_login_frame.destroy(),admin_registration()])
    register_button2.pack(side="left", padx=10,pady=10)

    login_label = Label(form_frame,fg="whitesmoke",font=("Arial",20),background="gray",text="Login Form")
    login_label.pack(fill=NONE,anchor=CENTER,pady=30)

    login_email = Label(form_frame,fg="whitesmoke",font=("Arial",12),background="gray",text="Email Address")
    login_email.pack(fill=NONE,anchor=CENTER)
    login_email_entry = Entry(form_frame,width=30)
    login_email_entry.pack(fill=NONE,anchor=CENTER,pady=10)

    login_password = Label(form_frame,fg="whitesmoke",font=("Arial",12),background="gray",text="Password")
    login_password.pack(fill=BOTH,anchor=CENTER)
    login_password_entry = Entry(form_frame,width=30,show="*")
    login_password_entry.pack(fill=NONE,anchor=CENTER,pady=10)
    
    show_password_button = Button(form_frame,background="grey",text="Show Password",width=12,command=lambda:[toggle_show_password()])
    show_password_button.pack(fill=NONE,anchor=CENTER,pady=10)

    login_button = Button(form_frame,background="grey",width=10,text="Login",command=lambda:[login()])
    login_button.pack(fill=NONE,anchor=CENTER,pady=30)

    def toggle_show_password():
        if login_password_entry.cget("show") == "":
            login_password_entry.config(show="*")
            show_password_button.config(text="Show Password")
        else:
            login_password_entry.config(show="")
            show_password_button.config(text="Hide Password")

    def login():
        input_password = login_password_entry.get()
        input_email = login_email_entry.get()
        hashed_input_password = hash_password(input_password)
        admin = login_admin(input_email,hashed_input_password)
        if admin is not None:
            admin_session["admin_username"] = admin["email"]
            admin_session["logged_in"] = True
            admin_login_frame.destroy()
            admin_home_page()
        else:
            msg1 = "Invalid usermane/password"
            messagebox.showinfo('message',msg1)

    admin_page.mainloop()

def admin_home_page():

    admin_page.title("Admin page")

    admin_home_frame = Frame(admin_page,bg="wheat",borderwidth=10,width=550,height=1280)
    admin_home_frame.pack(expand=True,fill=BOTH)

    form_frame = Frame(admin_home_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    nav_frame = Frame(form_frame, bg="light gray")
    nav_frame.pack(side="top", pady=10, padx=90)

    # Create the buttons in the navigation bar
    users_management_button = Button(nav_frame, text="Manage Users",width=12,command=lambda:[admin_home_frame.destroy(),users_management()])
    users_management_button.pack(side="left", padx=10,pady=10)

    jobs_management_button = Button(nav_frame, text="Manage Jobs",width=12,command=lambda:[admin_home_frame.destroy(),jobs_management()])
    jobs_management_button.pack(side="left", padx=10,pady=10)

    admin_details_button = Button(nav_frame, text="Manage Jobs",width=12,command=lambda:[admin_home_frame.destroy(),jobs_management()])
    admin_details_button.pack(side="left", padx=10,pady=10)

    admin_page.mainloop()

def users_management():

    admin_page.title("Manage Users")

    users_frame = Frame(admin_page,bg="wheat",borderwidth=10,width=550,height=1280)
    users_frame.pack(expand=True,fill=BOTH)

    form_frame = Frame(users_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    nav_frame = Frame(form_frame, bg="light gray")
    nav_frame.pack(side="top", pady=10, padx=90)

    # Create the buttons in the navigation bar
    users_management_button = Button(nav_frame, text="Manage Users",width=12,command=lambda:[users_frame.destroy(),users_management()])
    users_management_button.pack(side="left", padx=10,pady=10)

    jobs_management_button = Button(nav_frame, text="Manage Jobs",width=12,command=lambda:[users_frame.destroy(),jobs_management()])
    jobs_management_button.pack(side="left", padx=10,pady=10)

    admin_details_button = Button(nav_frame, text="Manage Jobs",width=12,command=lambda:[users_frame.destroy(),jobs_management()])
    admin_details_button.pack(side="left", padx=10,pady=10)

    admin_page.mainloop()

def jobs_management():

    admin_page.title("Manage Jobs")

    jobs_frame = Frame(admin_page,bg="wheat",borderwidth=10,width=550,height=1280)
    jobs_frame.pack(expand=True,fill=BOTH)

    form_frame = Frame(jobs_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    nav_frame = Frame(form_frame, bg="light gray")
    nav_frame.pack(side="top", pady=10, padx=90)

    # Create the buttons in the navigation bar
    button1 = Button(nav_frame, text="Manage Users",width=12)
    button1.pack(side="left", padx=10,pady=10)

    button2 = Button(nav_frame, text="Manage Jobs",width=12)
    button2.pack(side="left", padx=10,pady=10)

    admin_page.mainloop()

admin_registration()