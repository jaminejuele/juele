import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# =========================
# DATABASE
# =========================

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    course TEXT NOT NULL
)
""")

conn.commit()


# =========================
# FUNCTIONS
# =========================

# CREATE
def add_student():
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()

    if name == "" or age == "" or course == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return

    cursor.execute(
        "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
        (name, age, course)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Student added successfully."
    )

    clear_fields()
    display_students()


# READ
def display_students():
    # Clear the Treeview first
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    for index, student in enumerate(students):
        if index % 2 == 0:
            tree.insert(
                "",
                tk.END,
                values=student,
                tags=("evenrow",)
            )
        else:
            tree.insert(
                "",
                tk.END,
                values=student,
                tags=("oddrow",)
            )


# UPDATE
def update_student():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a student to update."
        )
        return

    student_id = tree.item(selected[0])["values"][0]

    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()

    if name == "" or age == "" or course == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        age = int(age)
        name = str(name)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return

    cursor.execute("""
        UPDATE students
        SET name = ?, age = ?, course = ?
        WHERE id = ?
    """, (name, age, course, student_id))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Student updated successfully."
    )

    clear_fields()
    display_students()


# DELETE
def delete_student():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a student to delete."
        )
        return

    student_id = tree.item(selected[0])["values"][0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if confirm:
        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Student deleted successfully."
        )

        clear_fields()
        display_students()


# CLEAR INPUTS
def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)


# SELECT STUDENT
def select_student(event):
    selected = tree.selection()

    if selected:
        student = tree.item(selected[0])["values"]

        clear_fields()

        name_entry.insert(0, student[1])
        age_entry.insert(0, student[2])
        course_entry.insert(0, student[3])


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()
root.title("Student Management System")
root.geometry("700x550")
root.configure(bg="#EDE7F6")


# =========================
# COLORS
# =========================

BG_COLOR = "#EDE7F6"
TITLE_COLOR = "#6A1B9A"
LABEL_COLOR = "#7B1FA2"
ENTRY_BG = "#FFFFFF"

ADD_COLOR = "#66BB6A"
UPDATE_COLOR = "#FFA726"
DELETE_COLOR = "#EF5350"
CLEAR_COLOR = "#8E8E8E"

BUTTON_TEXT = "white"


# =========================
# TITLE
# =========================

title_label = tk.Label(
    root,
    text="Student Management System",
    font=("Arial", 20, "bold"),
    bg=BG_COLOR,
    fg=TITLE_COLOR
)

title_label.pack(pady=15)


# =========================
# INPUT FRAME
# =========================

input_frame = tk.Frame(
    root,
    bg="white",
    bd=2,
    relief="groove"
)

input_frame.pack(
    pady=5,
    padx=20,
    fill="x"
)


# =========================
# NAME
# =========================

tk.Label(
    input_frame,
    text="Name:",
    font=("Arial", 11, "bold"),
    bg="white",
    fg=LABEL_COLOR
).grid(
    row=0,
    column=0,
    padx=10,
    pady=8,
    sticky="e"
)

name_entry = tk.Entry(
    input_frame,
    width=35,
    font=("Arial", 11),
    bg=ENTRY_BG,
    fg="#212121",
    relief="solid",
    bd=1
)

name_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=8
)


# =========================
# AGE
# =========================

tk.Label(
    input_frame,
    text="Age:",
    font=("Arial", 11, "bold"),
    bg="white",
    fg=LABEL_COLOR
).grid(
    row=1,
    column=0,
    padx=10,
    pady=8,
    sticky="e"
)

age_entry = tk.Entry(
    input_frame,
    width=35,
    font=("Arial", 11),
    bg=ENTRY_BG,
    fg="#212121",
    relief="solid",
    bd=1
)

age_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=8
)


# =========================
# COURSE
# =========================

tk.Label(
    input_frame,
    text="Course:",
    font=("Arial", 11, "bold"),
    bg="white",
    fg=LABEL_COLOR
).grid(
    row=2,
    column=0,
    padx=10,
    pady=8,
    sticky="e"
)

course_entry = tk.Entry(
    input_frame,
    width=35,
    font=("Arial", 11),
    bg=ENTRY_BG,
    fg="#212121",
    relief="solid",
    bd=1
)

course_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=8
)


# =========================
# BUTTON FRAME
# =========================

button_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

button_frame.pack(pady=15)


# ADD BUTTON
tk.Button(
    button_frame,
    text="Add",
    width=12,
    font=("Arial", 10, "bold"),
    bg=ADD_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#388E3C",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=add_student
).grid(
    row=0,
    column=0,
    padx=5
)


# UPDATE BUTTON
tk.Button(
    button_frame,
    text="Update",
    width=12,
    font=("Arial", 10, "bold"),
    bg=UPDATE_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#EF6C00",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=update_student
).grid(
    row=0,
    column=1,
    padx=5
)


# DELETE BUTTON
tk.Button(
    button_frame,
    text="Delete",
    width=12,
    font=("Arial", 10, "bold"),
    bg=DELETE_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#C62828",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=delete_student
).grid(
    row=0,
    column=2,
    padx=5
)


# CLEAR BUTTON
tk.Button(
    button_frame,
    text="Clear",
    width=12,
    font=("Arial", 10, "bold"),
    bg=CLEAR_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#616161",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=clear_fields
).grid(
    row=0,
    column=3,
    padx=5
)


# =========================
# TREEVIEW STYLE
# =========================

style = ttk.Style()

style.theme_use("clam")


# Table heading
style.configure(
    "Treeview.Heading",
    background="#7B1FA2",
    foreground="white",
    font=("Arial", 10, "bold"),
    padding=8
)


# Table body
style.configure(
    "Treeview",
    background="white",
    foreground="#212121",
    rowheight=30,
    fieldbackground="white",
    font=("Arial", 10)
)


# Selected row
style.map(
    "Treeview",
    background=[
        ("selected", "#BA68C8")
    ],
    foreground=[
        ("selected", "white")
    ]
)


# =========================
# TABLE
# =========================

tree = ttk.Treeview(
    root,
    columns=("ID", "Name", "Age", "Course"),
    show="headings"
)

tree.heading(
    "ID",
    text="ID"
)

tree.heading(
    "Name",
    text="Name"
)

tree.heading(
    "Age",
    text="Age"
)

tree.heading(
    "Course",
    text="Course"
)


# Column widths
tree.column(
    "ID",
    width=60,
    anchor="center"
)

tree.column(
    "Name",
    width=200
)

tree.column(
    "Age",
    width=80,
    anchor="center"
)

tree.column(
    "Course",
    width=220
)


# Alternating row colors
tree.tag_configure(
    "evenrow",
    background="#F3E5F5"
)

tree.tag_configure(
    "oddrow",
    background="#E1BEE7"
)


tree.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)


# =========================
# SELECT EVENT
# =========================

tree.bind(
    "<<TreeviewSelect>>",
    select_student
)


# =========================
# DISPLAY EXISTING RECORDS
# =========================

display_students()


# =========================
# START APPLICATION
# =========================

root.mainloop()


# =========================
# CLOSE DATABASE
# =========================

conn.close()
