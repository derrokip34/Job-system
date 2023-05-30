from tkinter import *
from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox
from db_connection import *
from models import User,Job
import re

admin_session = {
    "admin_username": None,
    "logged_in": False,
}

user = User()

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
            users_management()
        else:
            msg1 = "Invalid usermane/password"
            messagebox.showinfo('message',msg1)

    admin_page.mainloop()

def users_management():

    admin_page.title("Manage Users")

    users_frame = Frame(admin_page,bg="wheat",borderwidth=10,width=550,height=1280)
    users_frame.pack(expand=True,fill=BOTH)

    nav_frame = Frame(users_frame, bg="light gray")
    nav_frame.pack(side="top", pady=10, padx=90)

    # Create the buttons in the navigation bar
    users_management_button = Button(nav_frame, text="Manage Users",width=12,command=lambda:[users_frame.destroy(),users_management()])
    users_management_button.pack(side="left", padx=10,pady=10)

    jobs_management_button = Button(nav_frame, text="Manage Jobs",width=12,command=lambda:[users_frame.destroy(),jobs_management()])
    jobs_management_button.pack(side="left", padx=10,pady=10)

    admin_details_button = Button(nav_frame, text="Log Details",width=12,command=lambda:[users_frame.destroy(),log_details()])
    admin_details_button.pack(side="left", padx=10,pady=10)

    scrollbar = Scrollbar(users_frame)
    scrollbar.pack(side="right",fill='y')

    form_frame = Canvas(users_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=10)

    inner_frame = Frame(form_frame,bg="gray")
    form_frame.create_window((0, 10), window=inner_frame, anchor="center")

    add_buttons_frame = Frame(inner_frame,bg="gray")
    add_buttons_frame.pack(fill=X)

    add_job_poster_button = Button(add_buttons_frame,text="Add User",width=15,command=lambda:[])
    add_job_poster_button.pack(side=LEFT,padx=10)

    add_admin_button = Button(add_buttons_frame,text="Add Admin",width=15,command=lambda:[])
    add_admin_button.pack(side=LEFT,padx=10)

    entry_frame = Frame(inner_frame, bg="gray")
    entry_frame.pack(fill="x")

    first_name_search_entry = Entry(entry_frame, width=25)
    first_name_search_entry.pack(side="left", padx=10,pady=20)

    last_name_search_entry = Entry(entry_frame, width=25)
    last_name_search_entry.pack(side="left", padx=10,pady=20)

    all_users = get_job_seekers() + get_job_posters()

    def create_card(parent,first_name,last_name,user_id,user_type,user_status):
        user_card = Frame(parent,bg="white",bd=2,relief="solid",borderwidth=10)
        user_card.pack(fill=X,padx=10,pady=20)
        full_name = first_name + " " + last_name
        user_label = Label(user_card,background="white",text=full_name,font=("Arial",'15', "bold"))
        user_label.pack(side=TOP,anchor=W)
        user_status_label = Label(user_card,background="white",text=f"Status: {user_status}",font=("Arial",'12'))
        user_status_label.pack(side=TOP,anchor=W)
        if user_type == "job_seeker":
            new_user_type = "Job Seeker"
        else:
            new_user_type = "Job Poster"
        user_type_label = Label(user_card,background="white",text=f"User Type: {new_user_type}",font=("Arial",'12'))
        user_type_label.pack(side=TOP,anchor=W)
        update_user_button = Button(user_card,text="Update User",bg="blue",fg="white",command=lambda:[users_frame.destroy(),update_profile_window(user_type,user_id)])
        update_user_button.pack(side=RIGHT,padx=10,pady=20)
        delete_user_button = Button(user_card,text="Delete User",bg="red",fg="white",command=lambda:[users_frame.destroy(),delete_user_function(user_type,user_id)])
        delete_user_button.pack(side=RIGHT,padx=10,pady=20)

    cards =[]
    if len(all_users) == 0:
        none_label = Label(inner_frame,background="grey",text="No Users Found",font=("Arial",'15'))
        none_label.pack()
    for user1 in all_users:
        firstname = user1["first_name"]
        lastname = user1["last_name"]
        user_id = user1["id"]
        user_type = user1["user_type"]
        user_status = user1["user_status"]
        card = create_card(inner_frame,firstname,lastname,user_id,user_type,user_status)
        cards.append(card)

    def delete_user_function(user_type,user_id):
        confirm_window = Tk()
        confirm_window.geometry("200x100")
        confirm_window.title("Confirm deletion")
        
        confirm_label = Label(confirm_window, text="Are you sure you want to delete?")
        confirm_label.pack(anchor="center", pady=20)
        
        def confirm_delete():
            delete_user(user_type,user_id)
            messagebox.showinfo("User Deleted","User Deleted successfully")
            confirm_window.destroy()
            users_management()
        
        def cancel_delete():
            confirm_window.destroy()
            users_management()
        
        yes_button = Button(confirm_window, text="Yes", command=confirm_delete)
        yes_button.pack(side="left", padx=10,anchor=CENTER)
        
        no_button = Button(confirm_window, text="No", command=cancel_delete)
        no_button.pack(side="left", padx=10,anchor=CENTER)
        
        confirm_window.mainloop()

    def update_profile_window(user_type,user_id):
        if user_type == "job_seeker":
            users_profile = user.get_job_seeker_dict(user_id)
        else:
            users_profile = user.get_job_poster_dict(user_id)
        update_profile_page = Tk()
        update_profile_page.geometry("700x200")
        update_profile_page.title(users_profile["first_name"] + " " + users_profile["last_name"] + "'s profile")
        update_profile_page.configure(background="gray")

        fname_var = StringVar(update_profile_page)
        fname_var.set(users_profile["first_name"])
        f_name_label=Label(update_profile_page,text="First Name",background="grey",fg="whitesmoke",font=("Arial",12))
        f_name_label.place(x=20,y=50)
        fname_entry=Entry(update_profile_page,width=30,text=fname_var)
        fname_entry.place(x=160,y=50)
        fname_entry.configure(state="disabled")
        lname_var = StringVar(update_profile_page)
        lname_var.set(users_profile["last_name"])
        l_name_label=Label(update_profile_page,fg="whitesmoke",font=("Arial",12),background="gray",text="    Last Name")
        l_name_label.place(x=310,y=50)
        lname_entry=Entry(update_profile_page,width=30,text=lname_var)
        lname_entry.place(x=420,y=50)
        lname_entry.configure(state="disabled")

        status_label = Label(update_profile_page,fg="whitesmoke",font=("Arial",12),background="gray",text="User Status")
        status_label.place(x=20,y=100)

        status_var = IntVar(update_profile_page)

        non_active_rb = Radiobutton(update_profile_page, text="Non-Active",bg="gray" ,variable=status_var, value=0)
        non_active_rb.place(x=160,y=100)

        active_rb = Radiobutton(update_profile_page, text="Active",bg="gray" , variable=status_var, value=1)
        active_rb.place(x=160,y=130)

        update_button = Button(update_profile_page,text="Update Profile",height=2,background="lavender",command=lambda:[update_profile()])
        update_button.place(x=200,y=160)

        if users_profile["user_status"] == "active":
            status_var.set(1)
        else:
            status_var.set(0)

        def update_profile():
            if status_var.get() == 1:
                user_status = "active"
            else:
                user_status = "not active"
            update_user_status(user_type,user_id,user_status)
            update_profile_page.destroy()
            users_management()

        update_profile_page.mainloop()

    form_frame.update_idletasks()
    form_frame.configure(scrollregion=form_frame.bbox('all'))
    form_frame.yview_moveto(0.0)
    scrollbar.config(command=form_frame.yview)
    form_frame.config(yscrollcommand=scrollbar.set)

    admin_page.mainloop()

def jobs_management():

    admin_page.title("Manage Jobs")

    jobs_frame = Frame(admin_page,bg="wheat",borderwidth=10,width=550,height=1280)
    jobs_frame.pack(expand=True,fill=BOTH)

    nav_frame = Frame(jobs_frame, bg="light gray")
    nav_frame.pack(side="top", padx=90)

    # Create the buttons in the navigation bar
    users_management_button = Button(nav_frame, text="Manage Users",width=12,command=lambda:[jobs_frame.destroy(),users_management()])
    users_management_button.pack(side="left", padx=10,pady=10)

    jobs_management_button = Button(nav_frame, text="Manage Jobs",width=12,command=lambda:[jobs_frame.destroy(),jobs_management()])
    jobs_management_button.pack(side="left", padx=10,pady=10)

    admin_details_button = Button(nav_frame, text="Log Details",width=12,command=lambda:[jobs_frame.destroy(),log_details()])
    admin_details_button.pack(side="left", padx=10,pady=10)

    scrollbar = Scrollbar(jobs_frame)
    scrollbar.pack(side="right",fill='y')

    form_frame = Canvas(jobs_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=10)

    inner_frame = Frame(form_frame,bg="gray")
    form_frame.create_window((0, 10), window=inner_frame, anchor="center")

    add_buttons_frame = Frame(inner_frame,bg="gray")
    add_buttons_frame.pack(fill=X)

    add_job_poster_button = Button(add_buttons_frame,text="Add Job Category",width=15,command=lambda:[])
    add_job_poster_button.pack(side=LEFT,padx=10)

    add_job_poster_button = Button(add_buttons_frame,text="Add Area/Location",width=15,command=lambda:[])
    add_job_poster_button.pack(side=LEFT,padx=10)

    entry_frame = Frame(inner_frame, bg="gray")
    entry_frame.pack(fill="x")

    category_search_entry = Entry(entry_frame, width=25)
    category_search_entry.pack(side="left", padx=10,pady=20)

    job_location_search_entry = Entry(entry_frame, width=25)
    job_location_search_entry.pack(side="left", padx=10,pady=20)

    search_job_button = Button(entry_frame,text="Search",command=lambda:[])
    search_job_button.pack(side=LEFT,padx=10)

    all_jobs = get_all_jobs()

    def create_card(parent,job_id,job_category,date_posted):
        job_card = Frame(parent,bg="white",bd=2,relief="solid",borderwidth=10)
        job_card.pack(fill=X,padx=10,pady=20)
        jobid = f"J-{job_id}"
        user_label = Label(job_card,background="white",text=jobid,font=("Arial",'15', "bold"))
        user_label.pack(side=TOP,anchor=W)
        job_category_label = Label(job_card,background="white",text=job_category,width=50,height=2,font=("Arial",'12', "italic"),justify=LEFT,fg="black")
        job_category_label.pack(anchor=W)
        posted_on_label = Label(job_card,background="white",text="Posted on " + str(date_posted),width=50,height=2,font=("Arial",'12', "italic"),justify=LEFT,fg="black")
        posted_on_label.pack(anchor=W)
        update_job_button = Button(job_card,text="Update Job",bg="blue",fg="white",command=lambda:[])
        update_job_button.pack(side=RIGHT,padx=10,pady=5)
        delete_job_button = Button(job_card,text="Delete Job",bg="red",fg="white",command=lambda:[])
        delete_job_button.pack(side=RIGHT,padx=10,pady=5)

    cards =[]
    if len(all_jobs) == 0:
        none_label = Label(inner_frame,background="grey",text="No Jobs Found",font=("Arial",'15'))
        none_label.pack()
    for job in all_jobs:
        card = create_card(inner_frame,job["job_id"],job["job_category"],job["date_posted"])
        cards.append(card)

    form_frame.update_idletasks()
    form_frame.configure(scrollregion=form_frame.bbox('all'))
    form_frame.yview_moveto(0.0)
    scrollbar.config(command=form_frame.yview)
    form_frame.config(yscrollcommand=scrollbar.set)

    admin_page.mainloop()

def log_details():

    admin_page.title("Log Details")

    jobs_frame = Frame(admin_page,bg="wheat",borderwidth=10,width=550,height=1280)
    jobs_frame.pack(expand=True,fill=BOTH)

    form_frame = Frame(jobs_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    nav_frame = Frame(form_frame, bg="light gray")
    nav_frame.pack(side="top", padx=90)

    # Create the buttons in the navigation bar
    users_management_button = Button(nav_frame, text="Manage Users",width=12,command=lambda:[jobs_frame.destroy(),users_management()])
    users_management_button.pack(side="left", padx=10,pady=10)

    jobs_management_button = Button(nav_frame, text="Manage Jobs",width=12,command=lambda:[jobs_frame.destroy(),jobs_management()])
    jobs_management_button.pack(side="left", padx=10,pady=10)

    admin_details_button = Button(nav_frame, text="Manage Jobs",width=12,command=lambda:[jobs_frame.destroy(),log_details()])
    admin_details_button.pack(side="left", padx=10,pady=10)



    admin_page.mainloop()

users_management()