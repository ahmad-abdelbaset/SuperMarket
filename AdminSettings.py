import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont



def display_users(cursor,admin_settings_frame):
    # Create a frame for the Treeview
    treeview_frame = tk.Frame(admin_settings_frame)
    treeview_frame.grid(row=1, column=0, padx=5, pady=0, sticky=tk.NSEW)

    tree = ttk.Treeview(treeview_frame, columns=("Username", "Level", "Password"), show="headings")
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

    for row in data:
        username, level, password = row
        level_text = "High" if level == 1 else "Low"
        tree.insert('', 'end', values=(username, level_text, password))

    for button in products_buttons:
        button.config(state=tk.DISABLED)

    for button in users_buttons:
        button.config(state=tk.NORMAL)

def display_products(cursor,admin_settings_frame):

    treeview_frame = tk.Frame(admin_settings_frame)
    treeview_frame.grid(row=1, column=0, padx=5, pady=0, sticky=tk.NSEW)

    # Create a horizontal scrollbar
    h_scrollbar = ttk.Scrollbar(treeview_frame, orient="horizontal")
    v_scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical")

    tree = ttk.Treeview(treeview_frame, columns=("Barcode", "Description", "Buying Price","Selling Price", "Quantity", "Expiration Date"), show="headings")
    tree.heading("Barcode", text="Barcode")
    tree.heading("Description", text="Description")
    tree.heading("Buying Price", text="Buying Price")
    tree.heading("Selling Price", text="Selling Price")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Expiration Date", text="Expiration Date")

    tree.column("Barcode", anchor="center",minwidth=0, width=120)
    tree.column("Description", anchor="center")
    tree.column("Buying Price", anchor="center",minwidth=0, width=90)
    tree.column("Selling Price", anchor="center",minwidth=0, width=90)
    tree.column("Quantity", anchor="center",minwidth=0, width=90)
    tree.column("Expiration Date", anchor="center")

    h_scrollbar.config(command=tree.xview)  # Configure the scrollbar to control horizontal scrolling
    h_scrollbar.pack(fill="x", side="bottom")  # Pack the scrollbar at the bottom of the frame
    v_scrollbar.config(command=tree.yview)  # Configure the scrollbar to control vertical scrolling
    v_scrollbar.pack(fill="y", side="right")  # Pack the scrollbar at the right side of the frame

    for button in users_buttons:
        button.config(state=tk.DISABLED)

    for button in products_buttons:
        button.config(state=tk.NORMAL)


    tree.pack(fill=tk.BOTH, expand=True)  # Use pack to fill the frame

    tree.delete(*tree.get_children())
    cursor.execute('SELECT BarCode, Description, BuyingPrice,SellingPrice, Quantity, ExpDate FROM products')
    data = cursor.fetchall()

    for row in data:
        Barcode, Description, BuyingPrice,SellingPrice, Quantity, ExpDate = row
        tree.insert('', 'end', values=(Barcode, Description, BuyingPrice,SellingPrice, Quantity, ExpDate))

def create_buttons(cursor, admin_settings_frame,button_frame,style_font):
    buttons = [
        ("Show Users", lambda: display_users(cursor, admin_settings_frame)),
        ("Add User", None),
        ("Edit User", None),
        ("Delete User", None),
        ("Show Product", lambda: display_products(cursor, admin_settings_frame)),
        ("Add Product", None),
        ("Edit Product", None),
        ("Delete Product", None)
    ]

    created_buttons = []

    for i, (text, command) in enumerate(buttons):
        row = i % 4
        col = i // 4
        button = tk.Button(button_frame, text=text, width=15, height=2,
                           font=style_font, command=command)
        button.grid(row=row, column=col, pady=(0, 10), padx=5, sticky=tk.NSEW)
        created_buttons.append(button)

    button = tk.Button(button_frame,text="Back", width=30, height=2,font=style_font)
    button.grid(row=5, columnspan=2)

    return created_buttons

def admin_frame(admin_settings_frame, root, cursor):
    style_font = tkFont.Font(weight="bold", size=12)
    admin_settings_frame.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW)

    # Create a frame for the label
    label_frame = tk.Frame(admin_settings_frame,borderwidth=2, relief="raised")
    label_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=10, sticky=tk.NSEW)

    label = tk.Label(label_frame, text="Admin Settings")
    label.pack()

    # Create a frame for the buttons
    button_frame = tk.Frame(admin_settings_frame, borderwidth=2, relief="raised")
    button_frame.grid(row=1, column=1, padx=5, pady=0, sticky=tk.NSEW)



    buttons = create_buttons(cursor, admin_settings_frame,button_frame,style_font)

    global products_buttons
    products_buttons = buttons[5:8]

    global users_buttons
    users_buttons = buttons[1:4]

    display_users(cursor, admin_settings_frame)





    lower_frame = tk.Frame(admin_settings_frame,borderwidth=2, relief="raised")
    lower_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky=tk.NSEW)

    label = tk.Label(lower_frame, text="Lower Frame")
    label.pack()

    # Configure column and row weights
    admin_settings_frame.columnconfigure(0, weight=1)
    admin_settings_frame.columnconfigure(1, weight=0)  # Adjust weight to 0 for button_frame column
    admin_settings_frame.rowconfigure(0, weight=0)  # Disable row weight for label_frame
    admin_settings_frame.rowconfigure(1, weight=1)  # Allow row 1 (treeview_frame and button_frame) to expand
