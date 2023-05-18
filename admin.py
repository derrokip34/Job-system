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
admin_page.mainloop()