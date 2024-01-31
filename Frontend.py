from tkinter import *
from customtkinter import *
from tkinter import ttk
from tkinter import messagebox
from Backend_database import *

# Set appearance mode
set_appearance_mode("light")

# Connect to MySQL database
connection, cursor = connect_to_mysql()

# Create main window
window = Tk()
window.title("Employee Management System")
window.geometry("1920x1080+0+0")
window.state("zoom")


# Function to show a specific page and highlight the corresponding button
def show_page(page_index):
    # Hide all pages
    for index, page in enumerate(pages):
        page.place_forget()
        buttons[index].config(font=("calibri", 12, "normal"))

    # Show the selected page
    pages[page_index].place(x=0, y=40, width=1920, height=1080)
    buttons[page_index].config(font=("calibri", 12, "bold"))


# Create pages
page1 = Frame(window, bg="white")
page2 = Frame(window, bg="white")

# Top bar buttons
button_frame = Frame(window, bg="#4B9CD3")
button_frame.place(x=0, y=0, width=1920, height=40)
button1 = Button(button_frame,
                 command=lambda: show_page(0),
                 text="Add Employee",
                 fg="white", bg="#4B9CD3",
                 bd=0, padx=10, pady=4,
                 activebackground="#4B9CD3", activeforeground="white")
button1.pack(side=LEFT, padx=(10, 0), pady=6)
button2 = Button(master=button_frame,
                 command=lambda: show_page(1),
                 text="Employee List",
                 fg="white", bg="#4B9CD3",
                 bd=0, padx=10, pady=4,
                 activebackground="#4B9CD3", activeforeground="white")
button2.pack(side=LEFT, pady=6)

pages = [page1, page2]
buttons = [button1, button2]

# Initially show the first page
show_page(0)

# Inputs
employee_id_var = StringVar()
full_name_var = StringVar()
gender_var = StringVar()
email_id_var = StringVar()
contact_number_var = StringVar()
date_of_joining_var = StringVar()
department_var = StringVar()
address_var = StringVar()


# Function to add an employee
def add_employee():
    if (employee_id_var.get() == ""
            or full_name_var.get() == ""
            or gender_var.get() == ""
            or email_id_var.get() == ""
            or contact_number_var.get() == ""
            or date_of_joining_var.get() == ""
            or department_var.get() == ""
            or address_entry.get("1.0", "end") == ""):

        messagebox.showerror("Input Error", "Please fill in all details")
        return

    # Insert data into the database
    data_to_insert = (employee_id_var.get(),
                      full_name_var.get(),
                      gender_var.get(),
                      email_id_var.get(),
                      contact_number_var.get(),
                      date_of_joining_var.get(),
                      department_var.get(),
                      address_entry.get("1.0", "end"))
    insert_data(connection, cursor, data_to_insert)
    messagebox.showinfo("Success", "Record Inserted")
    clear_all()
    display_all_records()

# Function to clear all input fields
def clear_all():
    employee_id_var.set("")
    full_name_var.set("")
    gender_var.set("")
    email_id_var.set("")
    contact_number_var.set("")
    date_of_joining_var.set("")
    department_var.set("")
    address_entry.delete("1.0", "end")


# Define selected_row at the beginning of your script
selected_row = None
# Function to get data from the selected row in the Treeview
def get_selected_row(event):
    global selected_row
    selected_row = table.focus()  # Focus on the selected table row
    data = table.item(selected_row)  # Get the data from the selected row
    global selected_data
    selected_data = data["values"]  # Store the data in another variable

    # Set the values in the input fields
    employee_id_var.set(selected_data[0])
    full_name_var.set(selected_data[1])
    gender_var.set(selected_data[2])
    email_id_var.set(selected_data[3])
    contact_number_var.set(selected_data[4])
    date_of_joining_var.set(selected_data[5])
    department_var.set(selected_data[6])
    address_entry.delete("1.0", "end")
    address_entry.insert(END, selected_data[7])


# Function to display all records in the Treeview
def display_all_records():
    table.delete(*table.get_children())
    for selected_data in fetch_data(cursor):
        table.insert("", END, values=selected_data)


# Function to show the update page
def show_update_page():
    if not selected_row:
        messagebox.showinfo("Info", "Please select data from the table.")
        return

    # Hide page2
    page2.place_forget()
    button2.config(font=("calibri", 12, "normal"))
    submit_button.destroy()
    clear_button.destroy()

    # Show page1
    show_page(0)
    global update_submit_button, cancel_button
    update_submit_button = CTkButton(master=page1,
                                     command=update_employee,
                                     text="Update",
                                     font=("calibri", 18),
                                     text_color="white",
                                     width=120,
                                     height=40,
                                     corner_radius=6,
                                     fg_color="#359f07",
                                     hover_color="#2e7e0c")
    update_submit_button.place(x=1160, y=650)
    cancel_button = CTkButton(master=page1,
                              command=cancel_update,
                              text="Cancel",
                              font=("calibri", 18),
                              text_color="white",
                              width=120,
                              height=40,
                              corner_radius=6)
    cancel_button.place(x=1020, y=650)

# Function to update an employee record
def update_employee():
    if (employee_id_var.get() == ""
            or full_name_var.get() == ""
            or gender_var.get() == ""
            or email_id_var.get() == ""
            or contact_number_var.get() == ""
            or date_of_joining_var.get() == ""
            or department_var.get() == ""
            or address_entry.get("1.0", "end") == ""):

        messagebox.showerror("Input Error", "Please fill in all details")
        return

    # Update data in the database
    data_to_insert = (employee_id_var.get(),
                      full_name_var.get(),
                      gender_var.get(),
                      email_id_var.get(),
                      contact_number_var.get(),
                      date_of_joining_var.get(),
                      department_var.get(),
                      address_entry.get("1.0", "end"))

    update_data(connection, cursor, data_to_insert, selected_data[0])
    messagebox.showinfo("Success", "Record updated")
    clear_all()
    display_all_records()
    show_page(1)
    global selected_row
    selected_row = None


# Function to cancel the update and go back to the main page
def cancel_update():
    update_submit_button.destroy()
    cancel_button.destroy()

    clear_button = CTkButton(master=page1,
                             command=clear_all,
                             text="Clear",
                             font=("calibri", 18),
                             text_color="white",
                             width=120,
                             height=40,
                             corner_radius=6)
    clear_button.place(x=1020, y=650)
    submit_button = CTkButton(master=page1,
                              command=add_employee,
                              text="Submit",
                              font=("calibri", 18),
                              text_color="white",
                              width=120,
                              height=40,
                              corner_radius=6,
                              fg_color="#359f07",
                              hover_color="#2e7e0c")
    submit_button.place(x=1160, y=650)
    clear_all()
    display_all_records()
    show_page(1)
    global selected_row
    selected_row = None

# Function to delete all records
def delete_all_records():
    if not selected_row:
        messagebox.showinfo("Info", "Please select data from the table.")
        return
    remove_data(connection, cursor, selected_data[0])
    clear_all()
    display_all_records()

# page1 contents
# system title
main_label = Label(page1,
                   text="Employee management system",
                   font=("calibri", 19, "bold"),
                   fg="#36454F",
                   bg="white")
main_label.place(x=630, y=25)
line = CTkEntry(master=page1,
                bg_color="white",
                fg_color="white",
                corner_radius=12,
                width=1236,
                height=640)
line.place(x=142, y=76)

# Employee_ID_inputfields
employee_id_label = Label(page1,
                          text="Employee ID",
                          font=("calibri", 14),
                          fg="black",
                          bg="white")
employee_id_label.place(x=250, y=110)
employee_id_entry = CTkEntry(master=page1,
                             textvariable=employee_id_var,
                             font=("calibri", 18),
                             width=460,
                             height=40,
                             corner_radius=6)
employee_id_entry.place(x=250, y=150)

# Name_inputfields
name_label = Label(page1,
                   text="Name",
                   font=("calibri", 14),
                   fg="black",
                   bg="white")
name_label.place(x=820, y=110)
name_entry = CTkEntry(master=page1,
                      textvariable=full_name_var,
                      font=("calibri", 18),
                      width=460,
                      height=40,
                      corner_radius=6)
name_entry.place(x=820, y=150)

# Gender_inputfields
gender_label = Label(page1,
                     text="Gender",
                     font=("calibri", 14),
                     fg="black",
                     bg="white")
gender_label.place(x=250, y=220)
gender_entry = CTkComboBox(master=page1,
                           variable=gender_var,
                           font=("calibri", 18),
                           width=460,
                           height=40,
                           corner_radius=6,
                           state="readonly")
gender_entry.configure(values=["Male", "Female"])
gender_entry.place(x=250, y=260)

# Email_inputfields
email_label = Label(page1,
                    text="Email ID",
                    font=("calibri", 14),
                    fg="black",
                    bg="white")
email_label.place(x=820, y=220)
email_entry = CTkEntry(master=page1,
                       textvariable=email_id_var,
                       font=("calibri", 18),
                       width=460,
                       height=40,
                       corner_radius=6)
email_entry.place(x=820, y=260)

# Contact_inputfields
contact_label = Label(page1,
                      text="Contact Number",
                      font=("calibri", 14),
                      fg="black",
                      bg="white")
contact_label.place(x=250, y=340)
contact_entry = CTkEntry(master=page1,
                         textvariable=contact_number_var,
                         font=("calibri", 18),
                         width=460,
                         height=40,
                         corner_radius=6)
contact_entry.place(x=250, y=380)

# DOJ_inputfields
doj_label = Label(page1,
                  text="Date of Joining",
                  font=("calibri", 14),
                  fg="black",
                  bg="white")
doj_label.place(x=820, y=340)
doj_entry = CTkEntry(master=page1,
                     textvariable=date_of_joining_var,
                     font=("calibri", 18),
                     width=460,
                     height=40,
                     corner_radius=6)
doj_entry.place(x=820, y=380)

# Department_inputfields
department_label = Label(page1,
                         text="Department",
                         font=("calibri", 14),
                         fg="black",
                         bg="white")
department_label.place(x=250, y=460)
department_entry = CTkComboBox(master=page1,
                               variable=department_var,
                               font=("calibri", 18),
                               width=460,
                               height=40,
                               corner_radius=6,
                               state="readonly")
department_entry.configure(values=["Software Development",
                                   "Network Administration",
                                   "Cybersecurity",
                                   "Database Administration",
                                   "Finance",
                                   "Human Resources", ])
department_entry.place(x=250, y=500)

# Address_inputfields
address_label = Label(page1,
                      text="Address",
                      font=("calibri", 14),
                      fg="black",
                      bg="white")
address_label.place(x=820, y=460)
address_entry = CTkTextbox(master=page1,
                           font=("calibri", 18),
                           width=460,
                           height=100,
                           corner_radius=6,
                           border_width=2)
address_entry.place(x=820, y=500)

# Buttons
clear_button = CTkButton(master=page1,
                         command=clear_all,
                         text="Clear",
                         font=("calibri", 18),
                         text_color="white",
                         width=120,
                         height=40,
                         corner_radius=6)
clear_button.place(x=1020, y=650)
submit_button = CTkButton(master=page1,
                          command=add_employee,
                          text="Submit",
                          font=("calibri", 18),
                          text_color="white",
                          width=120,
                          height=40,
                          corner_radius=6,
                          fg_color="#359f07",
                          hover_color="#2e7e0c")
submit_button.place(x=1160, y=650)

# page2 contents display employee list page
# system title
main_label = Label(page2,
                   text="Employee Management System",
                   font=("calibri", 19, "bold"),
                   fg="#36454F",
                   bg="white")
main_label.place(x=630, y=25)

# Treeview configuration
tree_frame = Frame(page2,
                   bg="white")
tree_frame.place(x=40, y=100, width=1836, height=770)

style = ttk.Style()
style.configure("mystyle.Treeview", font=("calibri", 10), rowheight=40)
style.configure("mystyle.Treeview.Heading", font=("calibri", 13), rowheight=40)

table = ttk.Treeview(tree_frame,
                     column=(1, 2, 3, 4, 5, 6, 7, 8),
                     show="headings",
                     style="mystyle.Treeview")
table.heading("1", text="Employee_ID")
table.column("1", width=30)
table.heading("2", text="Full_Name")
table.column("2", width=90)
table.heading("3", text="Gender")
table.column("3", width=20)
table.heading("4", text="Email_ID")
table.column("4", width=150)
table.heading("5", text="Contact_Number")
table.column("5", width=100)
table.heading("6", text="Date_of_Joining")
table.column("6", width=50)
table.heading("7", text="Department")
table.column("7", width=100)
table.heading("8", text="Address")
table.bind("<ButtonRelease-1>", get_selected_row)
table.place(x=0, y=0, width=1455, height=570)

scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scroll.set)
scroll.place(x=1437, y=1, height=568)

# Buttons for page 2
update_button = CTkButton(master=page2,
                          command=show_update_page,
                          text="Update",
                          font=("calibri", 18),
                          text_color="white",
                          width=120,
                          height=40,
                          corner_radius=6)
update_button.place(x=1355, y=690)
delete_button = CTkButton(master=page2,
                          command=delete_all_records,
                          text="Delete",
                          font=("calibri", 18),
                          text_color="white",
                          width=120,
                          height=40,
                          corner_radius=6,
                          fg_color="#ca3e30",
                          hover_color="#ba1b0a")
delete_button.place(x=1215, y=690)

# Display employee data in the Treeview
for row in fetch_data(cursor):
    table.insert("", END, values=row)

# Run the main loop
window.mainloop()
