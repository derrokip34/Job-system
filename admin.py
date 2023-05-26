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

admin_page = Tk()
admin_page.geometry("900x500")
admin_page.configure(background="gray")
admin_page.resizable(0,0)

def view_users():

    admin_page.title("Users")

    users_admin_menu_bar = Frame(admin_page,bg="dimgrey",height=70)
    users_admin_menu_bar.pack(expand=True,side=TOP,fill=X,padx=20)

    users_admin_frame = Frame(admin_page,bg="wheat",borderwidth=10,width=250,height=1280)
    users_admin_frame.pack(expand=True,fill=BOTH)

    form_frame = Frame(users_admin_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    home_nav = Button(users_admin_menu_bar,background="lavender",width=12,height=2,text="Home",fg="black",bd=5,command=lambda:[])
    home_nav.place(x=10,y=10)
    login_nav = Button(users_admin_menu_bar,background="lavender",width=12,height=2,text="Login",fg="black",bd=3,command=lambda: [])
    login_nav.place(x=120,y=10)
    new1_nav = Button(users_admin_menu_bar,background="lavender",width=12,height=2,text="Post Job",fg="black",bd=3)
    new1_nav.place(x=230,y=10)
    new2_nav = Button(users_admin_menu_bar,background="lavender",width=12,height=2,text="Home",fg="black",bd=3)
    new2_nav.place(x=340,y=10)
    new3_nav = Button(users_admin_menu_bar,background="lavender",width=12,height=2,text="Logout",fg="black",bd=3,command=lambda:[])
    new3_nav.place(x=450,y=10)

    admin_page.mainloop()

def add_categories_areas():

    admin_page.title("Add Job Categories and Areas")

    users_admin_menu_bar = Frame(admin_page,bg="dimgrey",height=70)
    users_admin_menu_bar.pack(expand=True,side=TOP,fill=X,padx=20)

    users_admin_frame = Frame(admin_page,bg="wheat",borderwidth=10,width=250,height=1280)
    users_admin_frame.pack(expand=True,fill=BOTH)

    form_frame = Frame(users_admin_frame,bg="gray",borderwidth=10,height=1280)
    form_frame.pack(expand=True,fill=BOTH,padx=20,pady=20)

    home_nav = Button(users_admin_menu_bar,background="lavender",width=12,height=2,text="Home",fg="black",bd=5,command=lambda:[])
    home_nav.place(x=10,y=10)
    login_nav = Button(users_admin_menu_bar,background="lavender",width=12,height=2,text="Login",fg="black",bd=3,command=lambda: [])
    login_nav.place(x=120,y=10)
    new1_nav = Button(users_admin_menu_bar,background="lavender",width=12,height=2,text="Post Job",fg="black",bd=3)
    new1_nav.place(x=230,y=10)
    new2_nav = Button(users_admin_menu_bar,background="lavender",width=12,height=2,text="Home",fg="black",bd=3)
    new2_nav.place(x=340,y=10)
    new3_nav = Button(users_admin_menu_bar,background="lavender",width=12,height=2,text="Logout",fg="black",bd=3,command=lambda:[])
    new3_nav.place(x=450,y=10)

    admin_page.mainloop()

add_categories_areas()