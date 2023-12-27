import tkinter as tk
from tkinter import messagebox
import MainProgram
import ConnectionDB
from ConnectionDB import get_connection, close_connection


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")



def check_login():
    username = username_entry.get()
    password = password_entry.get()

    # Create a cursor

    connection = get_connection()
    cursor = connection.cursor()
    #cursor = ConnectionDB.connection.cursor()

    # Execute a SELECT query to check login credentials
    query = "SELECT UserName,Password, AdminPermissions FROM users WHERE UserName = %s AND Password = %s"
    cursor.execute(query, (username, password))


    # Fetch the first row (if exists)
    row = cursor.fetchone()


    # Check if the username and password are correct (you can replace this with your own logic)
    if (username == "admin" and password == "admin") or row:

            #messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
            root.withdraw()  # Hide the login window

            if row:
                if row[2] == 1:
                    admin = True
                    username = row[0]
                else:
                    admin = False
                    username = row[0]
            else:
                admin = True
                username = "admin"


            MainProgram.open_main_frame(root,admin,username,cursor)



    else:
        messagebox.showerror("Login Failed", "Incorrect username or password. Please try again.")


# Create the main window
root = tk.Tk()
root.title("Login..")
root.geometry("300x200")
root.resizable(False, False)

# Center the window on the screen
window_width = 300
window_height = 200
center_window(root, window_width, window_height)

# Create and place widgets on the window
username_label = tk.Label(root, text="Username:")
username_label.pack(pady=10)
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack(pady=10)
password_entry = tk.Entry(root, show="*")
password_entry.pack()

login_button = tk.Button(root, text="Login", command=check_login, width=10, height=3)
login_button.pack(pady=15)
root.bind("<Return>", lambda event=None: login_button.invoke())  # Bind Enter key to login_button

# Start the main loop
root.mainloop()

def close_program(root):
    root.destroy()  # Close the main Tkinter root window
#root.protocol("WM_DELETE_WINDOW", close_program)
