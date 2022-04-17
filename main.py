import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk,Image

root = Tk()

# Main Window & Settings
root.title("CD/DVD/Disk Organizer")
root_icon = PhotoImage(file = 'bluray-disc.png')
root.iconphoto(False, root_icon)
main_width=800
main_height=600
main_screen_width = root.winfo_screenwidth()
main_screen_height = root.winfo_screenheight()
main_alignstr = '%dx%d+%d+%d' % (main_width, main_height, (main_screen_width - main_width) / 2, (main_screen_height - main_height) / 2)
root.geometry(main_alignstr)
root.resizable(width=False, height=False)
main_img = ImageTk.PhotoImage(Image.open("blu-rayfront.png"))
main_label_img = Label(image=main_img)
main_label_img.place(x=230,y=70,width=340,height=200)

# Database Creation
conn = sqlite3.connect('organizer.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE if not exists cd (cdname text NOT NULL)""")
cur.execute("""CREATE TABLE if not exists cover (id INTEGER PRIMARY KEY AUTOINCREMENT, name text NOT NULL, year INT NOT NULL, cd text)""")
conn.commit()
conn.close()


# List Window
def list_window():

    # Global variables
    global list_window_treeview
    global list_query_get

    # List Window Settings
    list_window = Toplevel()
    list_window.title("List")
    list_window.iconphoto(False, root_icon)
    width=800
    height=800
    screenwidth = list_window.winfo_screenwidth()
    screenheight = list_window.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    list_window.geometry(alignstr)
    list_window.resizable(width=False, height=False)

    # Database query to fill selection box
    conn = sqlite3.connect('organizer.db')
    cur = conn.cursor()
    cur.execute("SELECT cdname FROM cd")
    temp_list = [r for r, in cur]
    conn.commit()
    conn.close()

    # Selection box & buttons for ascending & descending listing
    list_query_get = StringVar(list_window)
    list_query_get.set(temp_list[0])
    drop = OptionMenu(list_window, list_query_get, *temp_list)
    drop.place(x=320,y=30,width=160,height=40)
    list_button_ascending = Button(list_window, text="Check Ascending", command=list_ascending, bg='#3F88C5', fg='#FFFFFF')
    list_button_ascending.place(x=220,y=90,width=150,height=40)
    list_button_descending = Button(list_window, text="Check Descending", command=list_descending, bg='#3F88C5', fg='#FFFFFF')
    list_button_descending.place(x=430,y=90,width=150,height=40)

    # Treeview
    list_window_treeview = ttk.Treeview(list_window)
    list_window_treeview['columns'] = ("ID", "Value", "CD", "Year")
    list_window_treeview.column("#0", width=0, minwidth=25, stretch=NO)
    list_window_treeview.column("ID", anchor=W, width=50, stretch=NO)
    list_window_treeview.column("Value", anchor=W, width=320, stretch=NO)
    list_window_treeview.column("CD", anchor=W, width=100)
    list_window_treeview.column("Year", anchor=W, width=80, stretch=NO)
    list_window_treeview.heading("#0", anchor=W)
    list_window_treeview.heading("ID", text="ID", anchor=W)
    list_window_treeview.heading("Value", text="Value", anchor=W)
    list_window_treeview.heading("CD", text="CD", anchor=W)
    list_window_treeview.heading("Year", text="Year", anchor=W)
    list_window_treeview.place(x=100,y=160,width=600,height=600)


# Function to make descending list inside the List Window
def list_descending():

    # Removes old treeview values & resets input counter
    list_window_treeview.delete(*list_window_treeview.get_children())
    input_counter = 0

    # Database query to fill Treeview
    conn = sqlite3.connect('organizer.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM cover WHERE cd = '{list_query_get.get()}' ORDER BY id DESC ")
    rows = cur.fetchall()

    # Loops through values & places them according to counter
    for row in rows:
        if input_counter % 2 == 0:
            list_window_treeview.insert(parent='', index='end', iid=input_counter, values=(row[0], row[1], row[3], row[2]), tags=('evenrow',))
        else:
            list_window_treeview.insert(parent='', index='end', iid=input_counter, values=(row[0], row[1], row[3], row[2]), tags=('oddrow',))
        input_counter += 1

    conn.commit()
    conn.close()


# Function to make ascending list inside the List Window
def list_ascending():
    list_window_treeview.delete(*list_window_treeview.get_children())
    input_counter = 0

    conn = sqlite3.connect('organizer.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM cover WHERE cd = '{list_query_get.get()}' ")
    rows = cur.fetchall()

    for row in rows:
        if input_counter % 2 == 0:
            list_window_treeview.insert(parent='', index='end', iid=input_counter, values=(row[0], row[1], row[3], row[2]), tags=('evenrow',))
        else:
            list_window_treeview.insert(parent='', index='end', iid=input_counter, values=(row[0], row[1], row[3], row[2]), tags=('oddrow',))
        input_counter += 1

    conn.commit()
    conn.close()


# Organizer Window
def organize_window():

    # Global variables
    global organize_id
    global organize_name
    global organize_year
    global organize_window_treeview
    global organize_query_get

    # Organizer Window Settings
    organize_window = Toplevel()
    organize_window.title("Organize")
    organize_window.iconphoto(False, root_icon)
    width=800
    height=700
    screenwidth = organize_window.winfo_screenwidth()
    screenheight = organize_window.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    organize_window.geometry(alignstr)
    organize_window.resizable(width=False, height=False)

    # Treeview
    organize_window_treeview = ttk.Treeview(organize_window)
    organize_window_treeview['columns'] = ("ID", "Value", "CD", "Year")
    organize_window_treeview.column("#0", width=0, minwidth=25, stretch=NO)
    organize_window_treeview.column("ID", anchor=W, width=60, stretch=NO)
    organize_window_treeview.column("Value", anchor=W, width=350, stretch=NO)
    organize_window_treeview.column("CD", anchor=W, width=100)
    organize_window_treeview.column("Year", anchor=W, width=80, stretch=NO)
    organize_window_treeview.heading("#0", anchor=W)
    organize_window_treeview.heading("ID", text="ID", anchor=W)
    organize_window_treeview.heading("Value", text="Value", anchor=W)
    organize_window_treeview.heading("CD", text="CD", anchor=W)
    organize_window_treeview.heading("Year", text="Year", anchor=W)
    organize_window_treeview.place(x=40,y=20,width=711,height=369)

    # Button to run organize selection function
    organize_button_selection = Button(organize_window, text="Select Value", command=organize_selection, bg='#3F88C5', fg='#FFFFFF')
    organize_button_selection.place(x=70,y=450,width=100,height=50)

    # Database query grab values for the Treeview
    conn = sqlite3.connect('organizer.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM cover ORDER BY id DESC")
    rows = cur.fetchall()
    input_counter = 0

    # Buttons & Labels for input values
    organize_id = Entry(organize_window)
    organize_id.place(x=350,y=450,width=150,height=30)
    organize_id_label = Label(organize_window, text="ID:")
    organize_id_label.place(x=270,y=450,width=70,height=25)
    organize_id.configure(state='disabled')
    organize_name = Entry(organize_window)
    organize_name.place(x=350,y=490,width=150,height=31)
    organize_name_label = Label(organize_window, text="Value:")
    organize_name_label.place(x=270,y=490,width=70,height=25) 
    organize_year = Entry(organize_window)
    organize_year.place(x=350,y=570,width=150,height=30)
    organize_year_label = Label(organize_window, text="Year:")
    organize_year_label.place(x=270,y=570,width=70,height=25)

    # Database query grabs values for selection box
    conn = sqlite3.connect('organizer.db')
    cur = conn.cursor()
    cur.execute("SELECT cdname FROM cd")
    temp_list = [r for r, in cur]
    conn.commit()
    conn.close()

    # Button, label, selection box & loads values from temp_list for the selection box
    organize_query_get = StringVar(organize_window)
    organize_query_get.set(temp_list[0])
    drop = OptionMenu(organize_window, organize_query_get, *temp_list)
    drop.place(x=348,y=525,width=155,height=40)
    organize_cd_label = Label(organize_window, text="CD:")
    organize_cd_label.place(x=270,y=530,width=70,height=25)

    # Button to load function organize_add
    organize_button_add = Button(organize_window, text="Add Value", command=organize_add, bg='#44BBA4', fg='#FFFFFF')
    organize_button_add.place(x=620,y=450,width=100,height=50)

    # Button to load function organize_delete
    organize_button_delete = Button(organize_window, text="Delete Value", command=organize_delete, bg='#E94F37', fg='#FFFFFF')
    organize_button_delete.place(x=620,y=510,width=100,height=50)

    # Loops through values & places them according to counter into the Treeview
    for row in rows:
        if input_counter % 2 == 0:
            organize_window_treeview.insert(parent='', index='end', iid=input_counter, values=(row[0], row[1], row[3], row[2]), tags=('evenrow',))
        else:
            organize_window_treeview.insert(parent='', index='end', iid=input_counter, values=(row[0], row[1], row[3], row[2]), tags=('oddrow',))
        input_counter += 1

    # Button to load function organize_update
    organize_button_update = Button(organize_window, text="Update Value", command=organize_update, bg='#3F88C5', fg='#FFFFFF')
    organize_button_update.place(x=70,y=510,width=100,height=50)


# Function to delete a row from organize window Treeview
def organize_delete():

    # Returns warning if id is null
    if organize_id.get() == '':
        messagebox.showwarning(parent=organize_window_treeview, title="Value Error", message="Please select a Value first")
    else:
        # Deletes the row from database & empties input boxes 
        conn = sqlite3.connect('organizer.db')
        cur = conn.cursor()
        cur.execute(f"DELETE FROM cover WHERE id = '{organize_id.get()}' ")
        conn.commit()
        conn.close()
        organize_id.configure(state='normal')
        organize_id.delete(0, END)
        organize_id.configure(state='disabled')
        organize_name.delete(0, END)
        organize_year.delete(0, END)

        # Refresh organize window Treeview
        organize_window_treeview.delete(*organize_window_treeview.get_children())
        organize_query()


# Function to select a row from organize window Treeview
def organize_selection():

    # Returns warning if no row has been focused on
    if organize_window_treeview.focus() == '':
        messagebox.showwarning(parent=organize_window_treeview, title="Value Error", message="Please select a Value first")
    else:
        # Empties & load new values into input boxes
        organize_id.configure(state='normal')
        organize_id.delete(0, END)
        organize_name.delete(0, END)
        organize_year.delete(0, END)

        selected = organize_window_treeview.focus()

        values = organize_window_treeview.item(selected, 'values')
        organize_id.insert(0, values[0])
        organize_id.configure(state='disabled')
        organize_name.insert(0, values[1])
        organize_year.insert(0, values[3])


# Function to update a row from organize window Treeview
def organize_update():

    # Returns warning if no row has been focused on
    if organize_id.get() == '':
        messagebox.showwarning(parent=organize_window_treeview, title="Value Error", message="Please select a Value first")
        return
    else:
        # Returns warning no name was given
        if organize_name.get() == '':
            messagebox.showwarning(parent=organize_window_treeview, title="Value Error", message="Please fill in the Value name")
        else:
            # Updates name, year, cd where ID was the same
            conn = sqlite3.connect('organizer.db')
            cur = conn.cursor()
            cur.execute("""UPDATE cover SET
            name = :name,
            year = :year,
            cd = :cd
            WHERE id = :id""",
            {'name': organize_name.get(),
            'year': organize_year.get(),
            'cd': organize_query_get.get(),
            'id': organize_id.get(),
            })
            conn.commit()
            conn.close()

            # Refresh organize window Treeview & resets input boxes
            organize_id.configure(state='normal')
            organize_id.delete(0, END)
            organize_id.configure(state='disabled')
            organize_name.delete(0, END)
            organize_year.delete(0, END)
            organize_window_treeview.delete(*organize_window_treeview.get_children())
            organize_query()


# Function to load & fill in from organize window Treeview
def organize_query():

    # Global variables
    global input_counter
    input_counter = 0

    # Database query grabs values for organize window Treeview
    conn = sqlite3.connect('organizer.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM cover ORDER BY id DESC")
    rows = cur.fetchall()
    
    # Loops through values & places them according to counter into the Treeview
    for row in rows:
        if input_counter % 2 == 0:
            organize_window_treeview.insert(parent='', index='end', iid=input_counter, values=(row[0], row[1], row[3], row[2]), tags=('evenrow',))
        else:
            organize_window_treeview.insert(parent='', index='end', iid=input_counter, values=(row[0], row[1], row[3], row[2]), tags=('oddrow',))
        input_counter += 1

    conn.commit()
    conn.close()


# Function to add a row in from organize window Treeview
def organize_add():
    # Returns warning no name was given
    if organize_name.get() == '':
        messagebox.showwarning(parent=organize_window_treeview, title="Value Error", message="Please fill in the Value name")
    else:
        # Loads db and inserts value name, year & cd - ID is autoincrement
        conn = sqlite3.connect('organizer.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO cover VALUES (NULL, :name, :year, :cd)",
                    {
                        'name': organize_name.get(),
                        'year': organize_year.get(),
                        'cd': organize_query_get.get()
                    })
        conn.commit()
        conn.close()

        # Refresh organize window Treeview & resets input boxes
        organize_name.delete(0, END)
        organize_year.delete(0, END)
        organize_window_treeview.delete(*organize_window_treeview.get_children())
        organize_query()


# CD Window
def cd_window():

    # Global Variables
    global cd_menu
    global cd_name
    global cd_listbox

    # CD Window Settings
    cd_menu = Toplevel()
    cd_menu.title("Create CD")
    cd_menu.iconphoto(False, root_icon)
    width=600
    height=400
    screenwidth = cd_menu.winfo_screenwidth()
    screenheight = cd_menu.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    cd_menu.geometry(alignstr)
    cd_menu.resizable(width=False, height=False)

    # Input box & Label for name
    cd_name = Entry(cd_menu, width=30)
    cd_name.place(x=170,y=280,width=249,height=30)
    cd_name_label = Label(cd_menu, text="CD Name:")
    cd_name_label.place(x=50,y=280,width=70,height=25)

    # Button for cd creation
    cd_button_add = Button(cd_menu, text="Add CD", command=cd_creation, bg='#44BBA4', fg='#FFFFFF')
    cd_button_add.place(x=480,y=280,width=70,height=25)

    # Button for cd delete
    cd_button_delete = Button(cd_menu, text="Delete CD", command=cd_delete, bg='#E94F37', fg='#FFFFFF')
    cd_button_delete.place(x=480,y=90,width=70,height=25)

    # Button for cd update
    cd_button_update = Button(cd_menu, text="Update CD", command=cd_update_window, bg='#3F88C5', fg='#FFFFFF')
    cd_button_update.place(x=480,y=160,width=70,height=25)
    
    # Creates listbox & runs cd_query to fill it with cds
    cd_listbox_frame = Frame(cd_menu)
    cd_listbox_scroll = Scrollbar(cd_listbox_frame, orient=VERTICAL)
    cd_listbox = Listbox(cd_listbox_frame, yscrollcommand=cd_listbox_scroll.set)
    cd_listbox_scroll.config(command=cd_listbox.yview)
    cd_listbox_scroll.pack(side=RIGHT, fill=Y)
    cd_listbox_frame.place(x=10,y=30,width=412,height=233)
    cd_listbox.place(x=160,y=20,width=235,height=203)
    cd_query()


# Function to create a CD
def cd_creation():
    # Returns warning if no name has been given
    if cd_name.get() ==  '':
        messagebox.showwarning(parent=cd_menu, title="CD Error", message="Please fill in the CD name")
    else:
        # Checks if given name already exist in database
        conn = sqlite3.connect('organizer.db')
        cur = conn.cursor()
        cur.execute("SELECT EXISTS(SELECT 1 FROM cd WHERE cdname=? LIMIT 1)", (cd_name.get(),))
        record = cur.fetchone()
        # Returns warning if CD name already exist
        if record[0] == 1:
            messagebox.showwarning(parent=cd_menu, title="Value Error", message="CD name already exist")
        else:
            # Inserts name into database
            conn = sqlite3.connect('organizer.db')
            cur = conn.cursor()
            cur.execute("INSERT INTO cd VALUES (:cdname)",
                        {
                            'cdname': cd_name.get()
                        })
            conn.commit()
            conn.close()

            # Runs CD list query & removes old value cd name input box
            cd_name.delete(0, END)
            cd_query()


# Function to load all CD values from database
def cd_query():
    # Removes old values
    cd_listbox.delete(0, END)

    # Fetches all name values from database
    conn = sqlite3.connect('organizer.db')
    cur = conn.cursor()
    cur.execute("SELECT *, oid FROM cd")
    rows = cur.fetchall()

    # Inserts all values in CD Listbox
    for row in rows:
        cd_listbox.insert(0, str(row[0]))

    conn.commit()
    conn.close()


# Function to delete a CD
def cd_delete():
    # Sets selected value into seperate variable
    record = cd_listbox.get(ANCHOR)

    # Returns warning of no CD is selected
    if cd_listbox.get(ANCHOR) == '':
        messagebox.showwarning(parent=cd_menu, title="CD Error", message="Please select a CD first")
    else:
        # Deletes CD name from DB
        conn = sqlite3.connect('organizer.db')
        cur = conn.cursor()
        cur.execute(f"DELETE FROM cd WHERE cdname = '{record}' ")
        conn.commit()
        conn.close()
        conn = sqlite3.connect('organizer.db')
        cur = conn.cursor()
        cur.execute("""UPDATE cover SET
        cd = :cd
        WHERE cd = :cd2""",
        {
        'cd': 'None',
        'cd2': record,
        })
        conn.commit()
        conn.close()

        # Loads query cd listbox
        cd_query()


# CD Update Window
def cd_update_window():
    # Returns warning of no CD is selected
    if cd_listbox.curselection() == ():
        messagebox.showwarning(parent=cd_menu, title="CD Error", message="Please select a CD")
    else:
        # Global Variables
        global cd_update_menu
        global cd_update_name

        # CD Update Window Settings
        cd_update_menu = Toplevel()
        cd_update_menu.title("Update a CD")
        cd_update_menu.iconphoto(False, root_icon)
        width=300
        height=100
        screenwidth = cd_update_menu.winfo_screenwidth()
        screenheight = cd_update_menu.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        cd_update_menu.geometry(alignstr)
        cd_update_menu.resizable(width=False, height=False)

        # DB connection to select all cd names
        conn = sqlite3.connect('organizer.db')
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM cd WHERE cdname = '{cd_listbox.get(ANCHOR)}' ")
        rows = cur.fetchall()

        # Input box & label to update name
        cd_update_name = Entry(cd_update_menu, width=30)
        cd_update_name.grid(row=0, column=1, padx=20)
        cd_update_name_label = Label(cd_update_menu, text="CD Name:")
        cd_update_name_label.grid(row=0, column=0)

        # Insert name into update_name_label
        for row in rows:
            cd_update_name.insert(0, row[0])

        # Button for cd_update function
        cd_button_update_name = Button(cd_update_menu, text="Update CD", command=cd_update)
        cd_button_update_name.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=100)


# Function to update a CD
def cd_update():
    # Loads database & grabs selected name
    conn = sqlite3.connect('organizer.db')
    cur = conn.cursor()
    cur.execute("SELECT EXISTS(SELECT 1 FROM cd WHERE cdname=? LIMIT 1)", (cd_update_name.get(),))
    record = cur.fetchone()
    # Returns warning if name already exist
    if record[0] == 1:
        messagebox.showwarning(parent=cd_update_menu, title="CD Error", message="CD name already exist")
    else:
        # Sets selected value into seperate variable
        cd_listbox_value = cd_listbox.get(ANCHOR)
        
        # Updates CD name according to given value
        conn = sqlite3.connect('organizer.db')
        cur = conn.cursor()
        cur.execute("""UPDATE cd SET
        cdname = :cd_update_name
        WHERE cdname = :record""",
        {'cd_update_name': cd_update_name.get(),
        'record': cd_listbox_value})
        conn.commit()
        conn.close()

        # Updates all CD names in cover
        conn = sqlite3.connect('organizer.db')
        cur = conn.cursor()
        cur.execute("""UPDATE cover SET
        cd = :cd
        WHERE cd = :cd2""",
        {
        'cd': cd_update_name.get(),
        'cd2': cd_listbox_value,
        })
        conn.commit()
        conn.close()

        # Runs query to reset Listbox & closes window
        cd_update_name.delete(0, END)
        cd_query()
        cd_update_menu.destroy()


# Main Window Buttons
main_button_create = Button(root, text="Create CD", command=cd_window, pady=50, width = 20, font='sans 16 bold', bg='#3F88C5', fg='#FFFFFF')
main_button_create.place(x=100,y=320,width=198,height=139)

main_button_organize = Button(root, text="Organizer", command=organize_window, pady=50, width = 20, font='sans 16 bold', bg='#3F88C5', fg='#FFFFFF')
main_button_organize.place(x=300,y=320,width=198,height=139)

main_button_list = Button(root, text="List", command=list_window, pady=50, width = 20, font='sans 16 bold', bg='#3F88C5', fg='#FFFFFF')
main_button_list.place(x=500,y=320,width=198,height=139)

# Runcommand
root.mainloop()