import re
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
import tkinter.font as tkFont

import pygame

import ConnectionDB
from tkcalendar import Calendar
import MainProgram

bg_color = '#EFFFD8'
bg_label = '#EFFFD8' #'#fffadb'
bg_btn_admin = '#a8e6c2' #"#E9F7EF" #'#7DCEA0'

pygame.mixer.init()  # Initialize the mixer
sound = pygame.mixer.Sound("click_sound.wav")

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def back_to_main_frame(admin_settings_frame,main_frame_variables):
    sound.play()

    #root= main_frame_variables[0]
    #admin=main_frame_variables[1]
    #username=main_frame_variables[2]
    #curser=main_frame_variables[3]
    admin_settings_frame.destroy()
    #MainProgram.open_main_frame(root,admin,username,curser)


def add_product(root, cursor,admin_settings_frame):
    sound.play()
    def validate_number(input_text):
        if not input_text:
            return True  # Allow empty input
        try:
            float(input_text)
            return True
        except ValueError:
            # Check if the input has a single decimal point and is a valid float
            if input_text.count('.') == 1 and all(char.isdigit() or char == '.' for char in input_text):
                return True
            return False

    def checkdate(expDate):
        def is_valid_date(date_str):
            if (date_str == ''):
                return True
            else:
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                    return True
                except ValueError:
                    return False

        def is_valid_range(date_str):
            if (date_str == ''):
                return True
            else:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                return datetime(2023, 1, 1) <= date <= datetime(2040, 12, 31)

        if is_valid_date(expDate) and is_valid_range(expDate):
            return True
        else:
            messagebox.showerror("Wrong Exp Date!", "The expiration date should be empty or like this : 2023-02-25")
            return False

    def add_product():
        try:
            barcode = entry1.get()
            Description = entry2.get()
            buyingPrice = entry3.get()
            sellingPrice = entry4.get()
            quantity = entry5.get()
            expDate = entry6.get()

            if (barcode == '' or sellingPrice == '' or not checkdate(expDate)):
                messagebox.showerror("Required Fields", "Please fill the required fields")
            else:
                # Define the SQL query and values tuple
                sql = 'INSERT INTO products (BarCode, SellingPrice'
                values = (barcode, sellingPrice)

                # Check if BuyingPrice is not empty and add it to the query and values tuple as a decimal
                if buyingPrice:
                    sql += ', BuyingPrice'
                    values += (float(buyingPrice),)  # Convert to float

                # Check if quantity is not empty and add it to the query and values tuple as an integer
                if quantity:
                    sql += ', quantity'
                    values += (int(quantity),)  # Convert to int

                # Check if expDate is not empty and add it to the query and values tuple
                if expDate:
                    sql += ', ExpDate'
                    values += (expDate,)

                # Check if Description is not empty and add it to the query and values tuple
                if Description:
                    sql += ', Description'
                    values += (Description,)

                sql += ') VALUES (' + ', '.join(['%s'] * len(values)) + ')'
                cursor.execute(sql, values)
                ConnectionDB.connection.commit()
                messagebox.showinfo("Adding User", "The new user added successfully!")
                display_products(cursor, admin_settings_frame)
                AddProduct_window.destroy()

        except Exception as e:
            print(e)

            messagebox.showerror("Something Wrong", "Something wrong with your inputs!")


    AddProduct_window = tk.Toplevel(root)
    AddProduct_window.title("Add Product")

    frame_width = 300
    frame_height = 400
    AddProduct_window.resizable (False,False)
    center_window(AddProduct_window, frame_width, frame_height)

    # Label 1
    label1 = tk.Label(AddProduct_window, text="Barcode*:", font=tkFont.Font(weight="bold", size=10),fg="red")
    label1.grid(row=0, column=0, padx=15,pady=15)

    entry1 = tk.Entry(AddProduct_window)
    entry1.grid(row=0, column=1, padx=15,pady=15)

    # Label 2
    label2 = tk.Label(AddProduct_window, text="Description:", font=tkFont.Font(weight="bold", size=10))
    label2.grid(row=1, column=0, padx=15,pady=15)

    entry2 = tk.Entry(AddProduct_window)
    entry2.grid(row=1, column=1, padx=15,pady=15)

    # Label 3
    label3 = tk.Label(AddProduct_window, text="Buying Price:", font=tkFont.Font(weight="bold", size=10))
    label3.grid(row=2, column=0, padx=15,pady=15)

    entry3 = tk.Entry(AddProduct_window, validate="key")
    entry3['validatecommand'] = (entry3.register(validate_number), "%P")
    entry3.grid(row=2, column=1, padx=15, pady=15)

    label4 = tk.Label(AddProduct_window, text="Selling Price*:", font=tkFont.Font(weight="bold", size=10),fg="red")
    label4.grid(row=3, column=0, padx=15, pady=15)

    entry4 = tk.Entry(AddProduct_window, validate="key")
    entry4['validatecommand'] = (entry4.register(validate_number), "%P")
    entry4.grid(row=3, column=1, padx=15, pady=15)

    label5 = tk.Label(AddProduct_window, text="Quantity:", font=tkFont.Font(weight="bold", size=10))
    label5.grid(row=4, column=0, padx=15, pady=15)

    entry5 = tk.Entry(AddProduct_window, validate="key")
    entry5['validatecommand'] = (entry5.register(validate_number), "%P")
    entry5.grid(row=4, column=1, padx=15, pady=15)

    label6 = tk.Label(AddProduct_window, text="Exp Date:\n(YYYY-MM-DD)", font=tkFont.Font(weight="bold", size=10))
    label6.grid(row=5, column=0, padx=15, pady=15)

    entry6 = tk.Entry(AddProduct_window)
    entry6.grid(row=5, column=1, padx=15, pady=15)

    button = tk.Button(AddProduct_window, text="Add Product", font=tkFont.Font(weight="bold", size=10), command=add_product)
    button.grid(row=6, column=1, columnspan=2)  # Span two columns

def edit_product(root,cursor,admin_settings_frame):
    sound.play()

    def checkdate(expDate):
        def is_valid_date(date_str):
            if (date_str.strip() == ''):
                return True
            else:
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                    return True
                except ValueError:
                    return False

        def is_valid_range(date_str):
            if (date_str.strip() == ''):
                return True
            else:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                return datetime(2023, 1, 1) <= date <= datetime(2040, 12, 31)

        if is_valid_date(expDate) and is_valid_range(expDate):
            return True
        else:
            return False


    def validate_number(input_text):
        if not input_text:
            return True  # Allow empty input
        try:
            float(input_text)
            return True
        except ValueError:
            # Check if the input has a single decimal point and is a valid float
            if input_text.count('.') == 1 and all(char.isdigit() or char == '.' for char in input_text):
                return True
            return False
    def save_changes():
        try:
            barcode = entry1.get()
            description = entry2.get()
            Buying_Price = entry3.get()
            Selling_Price = entry4.get()
            Quantity = entry5.get()
            ExpDate = entry6.get()
            if ExpDate.strip() =='':
                ExpDate = ' '

            if Selling_Price == '':
                messagebox.showerror("Empty Selling Price", "You didn't enter Selling Price ")
            elif not checkdate(ExpDate):
                messagebox.showerror("Wrong Expiration Date!", "The expiration date should be empty or like this : 2023-02-25")

            else:
                sql = "UPDATE products SET "
                values = []

                if description.strip() != "":
                    sql += "description = %s, "
                    values.append(description)
                else:
                    sql += "description = %s, "  # Keep the placeholder even if the value is empty
                    values.append(None)  # Use None as a placeholder value

                if Buying_Price.strip() != "":
                    sql += "BuyingPrice = %s, "
                    values.append(Buying_Price)
                else:
                    sql += "BuyingPrice = %s, "  # Keep the placeholder even if the value is empty
                    values.append(None)  # Use None as a placeholder value

                if Selling_Price.strip() != "":
                    sql += "SellingPrice = %s, "
                    values.append(Selling_Price)
                else:
                    sql += "SellingPrice = %s, "  # Keep the placeholder even if the value is empty
                    values.append(None)  # Use None as a placeholder value

                if Quantity.strip() != "":
                    sql += "Quantity = %s, "
                    values.append(Quantity)
                else:
                    sql += "Quantity = %s, "  # Keep the placeholder even if the value is empty
                    values.append(None)  # Use None as a placeholder value

                if ExpDate.strip() != "":
                    sql += "ExpDate = %s, "
                    values.append(ExpDate)
                else:
                    sql += "ExpDate = %s, "  # Keep the placeholder even if the value is empty
                    values.append(None)  # Use None as a placeholder value

                # Remove the trailing comma and space
                sql = sql[:-2]


                # Remove the trailing comma and complete the SQL statement
                sql = sql.rstrip(', ') + " WHERE barcode = %s"
                values.append(barcode)

                cursor.execute(sql, values)
                ConnectionDB.connection.commit()
                messagebox.showinfo("Updated", "The information of the selected product updated successfully!")
                display_products(cursor, admin_settings_frame)
                EditProduct_window.destroy()


        except Exception as e:
            print(e)
            messagebox.showerror("Something Wrong", "Something wrong with your inputs or the user already exists!")

    selected_item = treeProducts.selection()  # Get the selected item (row)

    if selected_item:
        barcode = treeProducts.item(selected_item, 'values')[0]
        description = treeProducts.item(selected_item, 'values')[1]
        Buying_Price = treeProducts.item(selected_item, 'values')[2]
        Selling_Price = treeProducts.item(selected_item, 'values')[3]
        Quantity = treeProducts.item(selected_item, 'values')[4]
        ExpDate = treeProducts.item(selected_item, 'values')[5]
        if ExpDate == 'None':
            ExpDate = ''

        EditProduct_window = tk.Toplevel(root)
        EditProduct_window.title("Edit Product")

        frame_width = 300
        frame_height = 400
        EditProduct_window.resizable(False, False)
        center_window(EditProduct_window, frame_width, frame_height)

        # Label 1
        # Label 1
        label1 = tk.Label(EditProduct_window, text="Barcode:", font=tkFont.Font(weight="bold", size=10))
        label1.grid(row=0, column=0, padx=15, pady=15)

        entry1 = tk.Entry(EditProduct_window)
        entry1.grid(row=0, column=1, padx=15, pady=15)
        entry1.insert(0, barcode)
        entry1.config(state='disabled')

        # Label 2
        label2 = tk.Label(EditProduct_window, text="Description:", font=tkFont.Font(weight="bold", size=10))
        label2.grid(row=1, column=0, padx=15, pady=15)

        entry2 = tk.Entry(EditProduct_window)
        entry2.grid(row=1, column=1, padx=15, pady=15)
        entry2.insert(0, description)

        # Label 3
        label3 = tk.Label(EditProduct_window, text="Buying Price:", font=tkFont.Font(weight="bold", size=10))
        label3.grid(row=2, column=0, padx=15, pady=15)

        entry3 = tk.Entry(EditProduct_window, validate="key")
        entry3['validatecommand'] = (entry3.register(validate_number), "%P")
        entry3.grid(row=2, column=1, padx=15, pady=15)
        entry3.insert(0, Buying_Price)

        label4 = tk.Label(EditProduct_window, text="Selling Price:", font=tkFont.Font(weight="bold", size=10))
        label4.grid(row=3, column=0, padx=15, pady=15)

        entry4 = tk.Entry(EditProduct_window, validate="key")
        entry4['validatecommand'] = (entry4.register(validate_number), "%P")
        entry4.grid(row=3, column=1, padx=15, pady=15)
        entry4.insert(0, Selling_Price)

        label5 = tk.Label(EditProduct_window, text="Quantity:", font=tkFont.Font(weight="bold", size=10))
        label5.grid(row=4, column=0, padx=15, pady=15)

        entry5 = tk.Entry(EditProduct_window, validate="key")
        entry5['validatecommand'] = (entry5.register(validate_number), "%P")
        entry5.grid(row=4, column=1, padx=15, pady=15)
        entry5.insert(0, Quantity)

        label6 = tk.Label(EditProduct_window, text="Exp Date:", font=tkFont.Font(weight="bold", size=10))
        label6.grid(row=5, column=0, padx=15, pady=15)

        entry6 = tk.Entry(EditProduct_window)
        entry6.grid(row=5, column=1, padx=15, pady=15)
        entry6.insert(0, ExpDate)

        button = tk.Button(EditProduct_window, text="Edit Product", font=tkFont.Font(weight="bold", size=10),
                           command=save_changes)
        button.grid(row=6, column=1, columnspan=2)  # Span two columns

    else:
        messagebox.showerror("No Selection", "Please Select Product")


def delete_product(cursor,admin_settings_frame):
    sound.play()
    selected_item = treeProducts.selection()  # Get the selected item (row)
    if selected_item:
        # Extract the username to identify the row in the database
        barcode = treeProducts.item(selected_item, 'values')[0]

        # Delete the row from the database
        confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to delete {barcode}?")
        if confirmation:
            sql = "DELETE FROM products WHERE barcode = %s"
            cursor.execute(sql, (barcode,))
            ConnectionDB.connection.commit()  # Commit the transaction

            # Delete the selected row from the Treeview
            treeProducts.delete(selected_item)
            display_products(cursor, admin_settings_frame)

    else:
        messagebox.showerror("No Selected Value", "Please select product!")


def edit_user(root,cursor,admin_settings_frame):
    sound.play()

    def save_changes():
        try:
            username = entry1.get()
            new_password = entry2.get()

            if combo.get() == 'Low':
                new_permission = 0
            elif combo.get() == 'High':
                new_permission = 1
            else:
                messagebox.showerror("Permission Value", "Something wrong with permission")

            if username == '' or new_password == '':
                messagebox.showerror("Empty Username", "You didn't enter a username or password")
            else:
                sql = "UPDATE users SET password = %s, AdminPermissions = %s WHERE username = %s"
                values = (new_password, new_permission, username)

                cursor.execute(sql, values)
                ConnectionDB.connection.commit()
                messagebox.showinfo("Updated", "The information of the selected user updated successfully")
                display_users(cursor, admin_settings_frame)
                EditUser_window.destroy()


        except Exception as e:
            messagebox.showerror("Something Wrong", "Something wrong with your inputs or the user already exists!")

    selected_item = tree.selection()  # Get the selected item (row)

    if selected_item:
        # Extract the username to identify the row in the database
        username = tree.item(selected_item, 'values')[0]
        level = tree.item(selected_item, 'values')[1]
        password = tree.item(selected_item, 'values')[2]

        EditUser_window = tk.Toplevel(root)
        EditUser_window.title("Edit User")

        frame_width = 300
        frame_height = 200
        EditUser_window.resizable(False, False)
        center_window(EditUser_window, frame_width, frame_height)

        # Label 1
        label1 = tk.Label(EditUser_window, text="Username:", font=tkFont.Font(weight="bold", size=10))
        label1.grid(row=0, column=0, padx=15, pady=15)

        entry1 = tk.Entry(EditUser_window)
        entry1.grid(row=0, column=1, padx=15, pady=15)
        entry1.insert(0, username)
        entry1.config(state='disabled')

        # Label 2
        label2 = tk.Label(EditUser_window, text="Password:", font=tkFont.Font(weight="bold", size=10))
        label2.grid(row=1, column=0, padx=15, pady=15)

        entry2 = tk.Entry(EditUser_window)
        entry2.grid(row=1, column=1, padx=15, pady=15)
        entry2.insert(0, password)

        # Label 3
        label3 = tk.Label(EditUser_window, text="Permission:", font=tkFont.Font(weight="bold", size=10))
        label3.grid(row=2, column=0, padx=15, pady=15)

        combo = ttk.Combobox(EditUser_window, state="readonly")
        combo['values'] = ('Low', 'High')
        combo.set(level)
        combo.grid(row=2, column=1, padx=15, pady=15)

        button = tk.Button(EditUser_window, text="Save Changes", font=tkFont.Font(weight="bold", size=10),
                           command=save_changes)
        button.grid(row=3, column=1, columnspan=2)  # Span two columns

    else:
        messagebox.showerror("No Selection", "Please Select User")


def delete_username(cursor,admin_settings_frame):
    sound.play()
    selected_item = tree.selection()  # Get the selected item (row)
    if selected_item:
        # Extract the username to identify the row in the database
        username = tree.item(selected_item, 'values')[0]

        # Delete the row from the database
        confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to delete {username}?")
        if confirmation:
            sql = "DELETE FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            ConnectionDB.connection.commit()  # Commit the transaction

            # Delete the selected row from the Treeview
            tree.delete(selected_item)
            display_users(cursor, admin_settings_frame)

    else:
        messagebox.showerror("No Selected Value", "Please select user!")

def add_user(root, cursor,admin_settings_frame):
    sound.play()
    def add_user():
        try:

            new_username = entry1.get()
            new_password = entry2.get()

            if combo.get() == 'Low':
                new_permission = 0
            elif combo.get() == 'High':
                new_permission = 1
            else:
                messagebox.showerror("Permission Value", "Something wrong with permission")
            # Get the input from the Entry widget

            if (new_username =='' or new_password == ''):
                messagebox.showerror("Empty Username", "You didn't enter username or password")
            else:
                sql = 'INSERT INTO users (Username, Password, AdminPermissions) VALUES (%s, %s, %s)'
                values = (new_username, new_password, new_permission)

                cursor.execute(sql, values)

                ConnectionDB.connection.commit()
                messagebox.showinfo("Adding User", "The new user added successfully!")
                display_users(cursor, admin_settings_frame)
                AddUser_window.destroy()

        except:

            messagebox.showerror("Something Wrong", "Something wrong with your inputs or the user already exists!")

    AddUser_window = tk.Toplevel(root)
    AddUser_window.title("Add User")

    frame_width = 300
    frame_height = 200
    AddUser_window.resizable (False,False)
    center_window(AddUser_window, frame_width, frame_height)

    # Label 1
    label1 = tk.Label(AddUser_window, text="Username:", font=tkFont.Font(weight="bold", size=10))
    label1.grid(row=0, column=0, padx=15,pady=15)

    entry1 = tk.Entry(AddUser_window)
    entry1.grid(row=0, column=1, padx=15,pady=15)

    # Label 2
    label2 = tk.Label(AddUser_window, text="Password:", font=tkFont.Font(weight="bold", size=10))
    label2.grid(row=1, column=0, padx=15,pady=15)

    entry2 = tk.Entry(AddUser_window)
    entry2.grid(row=1, column=1, padx=15,pady=15)

    # Label 3
    label3 = tk.Label(AddUser_window, text="Permission:", font=tkFont.Font(weight="bold", size=10))
    label3.grid(row=2, column=0, padx=15,pady=15)


    combo = ttk.Combobox(AddUser_window, state="readonly")
    combo['values'] = ('Low', 'High')
    combo.current(0)
    combo.grid(row=2, column=1, padx=15, pady=15)


    button = tk.Button(AddUser_window, text="Add User", font=tkFont.Font(weight="bold", size=10), command=add_user)
    button.grid(row=3, column=1, columnspan=2)  # Span two columns

def display_users(cursor,admin_settings_frame):
    sound.play()

    def sort_treeview_column(tree, col, reverse):
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        data.sort(reverse=reverse)

        for index, (val, child) in enumerate(data):
            tree.move(child, '', index)

        tree.heading(col, command=lambda: sort_treeview_column(tree, col, not reverse))


    global tree
    # Create a frame for the Treeview
    treeview_frame = tk.Frame(admin_settings_frame)
    treeview_frame.grid(row=1, column=0, padx=5, pady=0, sticky=tk.NSEW)

    tree = ttk.Treeview(treeview_frame, columns=("Username", "Level", "Password"), show="headings",selectmode="browse")
    tree.heading("Username", text="Username")
    tree.heading("Level", text="Level")
    tree.heading("Password", text="Password")

    tree.column("Username", anchor="center")
    tree.column("Level", anchor="center")
    tree.column("Password", anchor="center")
    tree.pack(fill=tk.BOTH, expand=True)  # Use pack to fill the frame

    tree.delete(*tree.get_children())
    cursor.execute('SELECT username, AdminPermissions, Password FROM users')
    data = cursor.fetchall()

    for col in ["Username", "Level", "Password",]:
        tree.heading(col, text=col, command=lambda c=col: sort_treeview_column(tree, c, False))

    for row in data:
        username, level, password = row
        level_text = "High" if level == 1 else "Low"
        tree.insert('', 'end', values=(username, level_text, password))

    for button in products_buttons:
        button.config(state=tk.DISABLED)

    for button in users_buttons:
        button.config(state=tk.NORMAL)

    search_entry.config(state=tk.DISABLED)

def display_products(cursor,admin_settings_frame):
    sound.play()

    def add_data_to_table():
        cursor.execute('SELECT BarCode, Description, BuyingPrice,SellingPrice, Quantity, ExpDate FROM products')
        data = cursor.fetchall()

        for row in data:
            Barcode, Description, BuyingPrice, SellingPrice, Quantity, ExpDate = row
            treeProducts.insert('', 'end', values=(Barcode, Description, BuyingPrice, SellingPrice, Quantity, ExpDate),
                                open=True)

    def search_treeview():

        #to clear the previous searched data
        for item in treeProducts.get_children():
            treeProducts.delete(item)

        add_data_to_table()

        search_term = search_entry.get().lower()

        # Clear the existing selection
        treeProducts.selection_remove(treeProducts.selection())

        # Iterate through all items in the treeview
        for item in treeProducts.get_children():

            values = treeProducts.item(item, 'values')

            # Check if any cell in the row contains the search term
            if search_term and any(search_term in str(cell).lower() for cell in values):
                # Show the item and highlight it
                treeProducts.item(item, open=True)

            else:
                # Remove the non-matching item
                treeProducts.delete(item)



                # You can also add a function to show all items in case the search term is empty
    def show_all_items():
        for item in treeProducts.get_children():
            treeProducts.delete(item)
        add_data_to_table()

    # Bind the search function to the Entry widget


    def sort_treeview_column(tree, col, reverse):
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        data.sort(reverse=reverse)

        for index, (val, child) in enumerate(data):
            tree.move(child, '', index)

        tree.heading(col, command=lambda: sort_treeview_column(tree, col, not reverse))


    global treeProducts
    treeview_frame = tk.Frame(admin_settings_frame)
    treeview_frame.grid(row=1, column=0, padx=5, pady=0, sticky=tk.NSEW)

    # Create a horizontal scrollbar
    h_scrollbar = ttk.Scrollbar(treeview_frame, orient="horizontal")
    v_scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical")

    treeProducts = ttk.Treeview(treeview_frame, columns=("Barcode", "Description", "Buying Price","Selling Price", "Quantity", "Expiration Date"), show="headings",selectmode="browse")
    treeProducts.heading("Barcode", text="Barcode")
    treeProducts.heading("Description", text="Description")
    treeProducts.heading("Buying Price", text="Buying Price")
    treeProducts.heading("Selling Price", text="Selling Price")
    treeProducts.heading("Quantity", text="Quantity")
    treeProducts.heading("Expiration Date", text="Expiration Date")

    treeProducts.column("Barcode", anchor="center",minwidth=0, width=120)
    treeProducts.column("Description", anchor="center")
    treeProducts.column("Buying Price", anchor="center",minwidth=0, width=90)
    treeProducts.column("Selling Price", anchor="center",minwidth=0, width=90)
    treeProducts.column("Quantity", anchor="center",minwidth=0, width=90)
    treeProducts.column("Expiration Date", anchor="center")

    h_scrollbar.config(command=treeProducts.xview)  # Configure the scrollbar to control horizontal scrolling
    h_scrollbar.pack(fill="x", side="bottom")  # Pack the scrollbar at the bottom of the frame
    v_scrollbar.config(command=treeProducts.yview)  # Configure the scrollbar to control vertical scrolling
    v_scrollbar.pack(fill="y", side="right")  # Pack the scrollbar at the right side of the frame

    for col in ["Barcode", "Description", "Buying Price", "Selling Price", "Quantity", "Expiration Date"]:
        treeProducts.heading(col, text=col, command=lambda c=col: sort_treeview_column(treeProducts, c, False))

    for button in users_buttons:
        button.config(state=tk.DISABLED)

    for button in products_buttons:
        button.config(state=tk.NORMAL)

    search_entry.config(state=tk.NORMAL)


    treeProducts.pack(fill=tk.BOTH, expand=True)  # Use pack to fill the frame

    treeProducts.delete(*treeProducts.get_children())

    add_data_to_table()


    search_entry.bind("<KeyRelease>", lambda event: search_treeview() if search_entry.get() else show_all_items())

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=(None, 10), tag="tree_sum_style")
    style.configure("Treeview", font=(None, 14), tag="tree_sum_style")
    style.configure("Treeview", background ="#E9F7EF" ,fieldbackground="#E9F7EF")
    style.configure("Treeview", rowheight=40)

def create_buttons(cursor, admin_settings_frame,button_frame,style_font,root,main_frame_variables):
    buttons = [
        ("Show Users", lambda: display_users(cursor, admin_settings_frame)),
        ("Add User", lambda: add_user(root,cursor,admin_settings_frame)),
        ("Edit User", lambda: edit_user(root,cursor,admin_settings_frame)),
        ("Delete User", lambda: delete_username(cursor,admin_settings_frame)),
        ("Show Product", lambda: display_products(cursor, admin_settings_frame)),
        ("Add Product", lambda: add_product(root,cursor,admin_settings_frame)),
        ("Edit Product", lambda: edit_product(root,cursor,admin_settings_frame)),
        ("Delete Product", lambda: delete_product(cursor,admin_settings_frame))
    ]

    created_buttons = []

    for i, (text, command) in enumerate(buttons):
        row = i % 4
        col = i // 4
        button = tk.Button(button_frame, text=text, width=15, height=2,
                           font=style_font, command=command, bg=bg_btn_admin)
        button.grid(row=row, column=col, pady=(0, 10), padx=5, sticky=tk.NSEW)
        created_buttons.append(button)

    button_back = tk.Button(button_frame,text="Back", width=30, height=2,font=style_font,command= lambda: back_to_main_frame(admin_settings_frame,main_frame_variables), bg=bg_btn_admin)
    button_back.grid(row=5, columnspan=2)

    return created_buttons

def admin_frame(admin_settings_frame, root, cursor,main_frame_variables):
    style_font = tkFont.Font(weight="bold", size=12)
    admin_settings_frame.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW)

    # Create a frame for the label
    label_frame = tk.Label(admin_settings_frame,borderwidth=2, relief="raised",bg=bg_label)
    label_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=10, sticky=tk.NSEW)


    search_label = tk.Label(label_frame, text="Search:",bg=bg_label)
    search_label.pack(side=tk.LEFT, padx=10)

    global search_entry
    search_entry = tk.Entry(label_frame, width=100)
    search_entry.pack(side=tk.LEFT)

    '''    global search_combobox
        options = ["Barcode", "Description"]
        search_combobox = ttk.Combobox(label_frame, values=options, state='readonly')
        search_combobox.current(0)
        search_combobox.pack(side=tk.LEFT, padx=10)'''

    # Create a frame for the buttons
    button_frame = tk.Frame(admin_settings_frame, borderwidth=2, relief="raised",bg=bg_label)
    button_frame.grid(row=1, column=1, padx=5, pady=0, sticky=tk.NSEW)



    buttons = create_buttons(cursor, admin_settings_frame,button_frame,style_font,root,main_frame_variables)

    global products_buttons
    products_buttons = buttons[5:8]

    global users_buttons
    users_buttons = buttons[1:4]

    display_products(cursor, admin_settings_frame)


    lower_frame = tk.Frame(admin_settings_frame,borderwidth=2, relief="raised", bg=bg_label)
    lower_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky=tk.NSEW)

    label = tk.Label(lower_frame, text="For any issue: ahmad.abdelbaset@outlook.com       Phone: 052-3173008", bg=bg_label )
    label.pack()


    # Configure column and row weights
    admin_settings_frame.columnconfigure(0, weight=1)
    admin_settings_frame.columnconfigure(1, weight=0)  # Adjust weight to 0 for button_frame column
    admin_settings_frame.rowconfigure(0, weight=0)  # Disable row weight for label_frame
    admin_settings_frame.rowconfigure(1, weight=1)  # Allow row 1 (treeview_frame and button_frame) to expand
