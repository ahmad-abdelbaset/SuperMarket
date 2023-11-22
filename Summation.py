import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import ConnectionDB
import tkinter.font as tkFont
import AdminSettings
from PIL import Image, ImageTk
import pygame
import keyboard

bg_color = '#FFE7DB'
bg_color_table = '#fffddb'
current_barcode = ""
pygame.mixer.init()  # Initialize the mixer
sound = pygame.mixer.Sound("click_sound.wav")


def on_window_close():
    # Stop listening for keyboard events when the window is closed
    keyboard.unhook(hook_id)
    sum_parts_window.destroy()
    # Close the Tkinter window

def checkout(cursor, sum_parts_window):
    sound.play()
    try:
        # Iterate through the items in the TreeView and update the quantities in the database
        for item in tree_sum.get_children():
            barcode = tree_sum.item(item, 'values')[0]
            quantity = int(tree_sum.item(item, 'values')[2])

            # Subtract the quantity from the database for each barcode
            command_check_quantity = f'SELECT quantity FROM products WHERE BarCode = {barcode}'
            cursor.execute(command_check_quantity)
            quantity_result = cursor.fetchone()

            if quantity_result:
                quantity_value = quantity_result[0]
                if isinstance(quantity_value, int):
                    command = f'UPDATE products SET quantity = quantity - {quantity} WHERE BarCode = {barcode}'
                    cursor.execute(command)
                    # Commit the changes to the database
                    ConnectionDB.connection.commit()

        messagebox.showinfo("Checkout", "Checkout successful!")
        sum_parts_window.destroy()  # Close the window after checkout
        keyboard.unhook(hook_id)

    except Exception as e:
        print(e)
        messagebox.showerror("Error", "Something went wrong during checkout. Please try again.")


def increase_quantity():
    sound.play()

    selected_item = tree_sum.selection()  # Get the selected item (row)
    if selected_item:
        barcode = tree_sum.item(selected_item, 'values')[0]
        Description = tree_sum.item(selected_item, 'values')[1]
        current_count = int(tree_sum.item(selected_item, 'values')[2])
        Price = float(tree_sum.item(selected_item, 'values')[3])

        tree_sum.item(selected_item,
                      values=(barcode, Description, current_count + 1, Price, (current_count + 1) * Price))

        update_total_value()
    else:
        messagebox.showerror("No Selected Value", "Please select product!")

def decrease_quantity():
    sound.play()
    selected_item = tree_sum.selection()  # Get the selected item (row)
    if selected_item:
        barcode = tree_sum.item(selected_item, 'values')[0]
        Description = tree_sum.item(selected_item, 'values')[1]
        current_count = int(tree_sum.item(selected_item, 'values')[2])
        Price = float(tree_sum.item(selected_item, 'values')[3])

        if current_count == 1:
            tree_sum.delete(selected_item)
        else:
            tree_sum.item(selected_item,
                      values=(barcode, Description, current_count - 1, Price, (current_count - 1) * Price))

        update_total_value()
    else:
        messagebox.showerror("No Selected Value", "Please select product!")



def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def add_barcode_to_tree(barcode,cursor):

    try:
        command = f'SELECT Description, SellingPrice FROM products WHERE BarCode = {barcode}'
        cursor.execute(command)

        result = cursor.fetchall()

        # Check if the result list is empty
        if not result:
            messagebox.showerror("Product Not Found", f"Product with barcode {barcode} not found.")
        else:
            # Iterate through the results and print them
            for row in result:
                Description = row[0]
                Price = row[1]


    except Exception as e:
        print(e)
        messagebox.showerror("Error", "Something went wrong. Please try again.")


    product_info = (barcode, Description, 1, Price)

    # Check if the barcode already exists in the tree_sum
    existing_item = None
    for item in tree_sum.get_children():
        if tree_sum.item(item, 'values')[0] == barcode:
            existing_item = item
            break

    if existing_item is not None:
        # Barcode already exists, update the count
        current_count = int(tree_sum.item(existing_item, 'values')[2])
        tree_sum.item(existing_item,
                      values=(barcode, Description, current_count + 1, Price, (current_count + 1) * Price))
    else:
        # Barcode doesn't exist, add a new row to the TreeView
        tree_sum.insert("", "end", values=(product_info[0], product_info[1], product_info[2], product_info[3], product_info[2] * product_info[3]))


    # Add a new row to the TreeView
    #tree_sum.insert("", "end", values=(product_info[0], product_info[1], product_info[2], product_info[3], product_info[2] * product_info[3]))


    update_total_value()

def update_total_value():
    # Calculate and update the total value label based on the values in the TreeView
    total = calculate_total_from_tree()
    total_value_label.config(text=total)

def calculate_total_from_tree():
    # Calculate the total value based on the values in the TreeView
    total = 0
    for item in tree_sum.get_children():
        total += float(tree_sum.item(item, "values")[-1])
    return total


def on_barcode_scanned(e,cursor):
    global current_barcode

    # Check if the scanned value is a digit
    if e.event_type == keyboard.KEY_DOWN and e.name.isdigit():
        # Append the digit to the current barcode
        current_barcode += e.name
    elif e.event_type == keyboard.KEY_UP and e.name == "enter":
        # Assuming "enter" key is used to signify the end of the barcode
        # Now you can add the complete barcode to your TreeView or perform any other desired action
        #print("Scanned Barcode:", current_barcode)
        add_barcode_to_tree(current_barcode,cursor)

        # Reset the current barcode for the next scan
        current_barcode = ""



def sum_products(root,cursor):
    global tree_sum
    global sum_parts_window

    pygame.mixer.init()  # Initialize the mixer
    sound = pygame.mixer.Sound("click_sound.wav")  # Replace with your sound file
    sound.play()


    sum_parts_window = tk.Toplevel(root)
    sum_parts_window.title("Sum Products")
    sum_parts_window.config(bg=bg_color)

    # Calculate the size of the TreeView and buttons based on the 2/3 and 1/3 requirement
    frame_width = 1000
    frame_height = 600
    sum_parts_window.resizable

    center_window(sum_parts_window, frame_width, frame_height)


    treeview_width = int(frame_width * 6 / 8)
    buttons_width = int(frame_width * 2 / 8)

    # Create the main frame
    main_frame = tk.Frame(sum_parts_window, width=frame_width, height=frame_height)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Create the TreeView on the left

    treeview_frame = tk.Frame(main_frame, width=treeview_width, height=frame_height)
    treeview_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    h_scrollbar = ttk.Scrollbar(treeview_frame, orient="horizontal")
    v_scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=(None, 10), tag="tree_sum_style")
    style.configure("Treeview", font=(None, 14), tag="tree_sum_style")
    style.configure("Treeview", fieldbackground=bg_color_table, tag="tree_sum_style")
    style.configure("Treeview", rowheight=40)


    columns = ("Barcode", "Description", "Units", "Price Per Unit", "Total Price")
    tree_sum = ttk.Treeview(treeview_frame, columns=columns, show="headings")

    h_scrollbar.config(command=tree_sum.xview)  # Configure the scrollbar to control horizontal scrolling
    h_scrollbar.pack(fill="x", side="bottom")  # Pack the scrollbar at the bottom of the frame
    v_scrollbar.config(command=tree_sum.yview)  # Configure the scrollbar to control vertical scrolling
    v_scrollbar.pack(fill="y", side="right")  # Pack the scrollbar at the right side of the frame


    for col in columns:
        tree_sum.heading(col, text=col)
        tree_sum.column(col, width=treeview_width // len(columns), anchor=tk.CENTER)


    units_column_width = treeview_width // len(columns)  # Original width
    new_units_column_width = int(units_column_width * 0.5)  # 50% of the original width
    tree_sum.column("Units", width=new_units_column_width, anchor=tk.CENTER)
    tree_sum.column("Price Per Unit", width=new_units_column_width, anchor=tk.CENTER)
    tree_sum.column("Total Price", width=new_units_column_width, anchor=tk.CENTER)


    tree_sum.pack(fill=tk.BOTH, expand=True)

#-------------------- Buttons -----------------------------------------------------------#


    summation_btn_img = Image.open('summation_btn.png')
    summation_btn_img_photo = ImageTk.PhotoImage(summation_btn_img)

    button_width = 130  # Set your desired button width
    button_height = 60  # Set your desired button height
    resized_img = summation_btn_img.resize((button_width, button_height), Image.ANTIALIAS)
    summation_btn_img_photo = ImageTk.PhotoImage(resized_img)

    resized_img_checkout = summation_btn_img.resize((240, 60), Image.ANTIALIAS)
    summation_btn_img_photo_checkout = ImageTk.PhotoImage(resized_img_checkout)


    buttons_frame = tk.Frame(main_frame, width=buttons_width, height=frame_height)
    buttons_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    buttons_frame.config(bg=bg_color)

    plus_button = tk.Button(buttons_frame, text="+", command=lambda:increase_quantity(), borderwidth=0, bg=bg_color, font = tkFont.Font(weight="bold", size=14))
    minus_button = tk.Button(buttons_frame, text="_", command=lambda:decrease_quantity(), borderwidth=0, bg=bg_color, font = tkFont.Font(weight="bold", size=14))

    plus_button.config(image=summation_btn_img_photo,compound="center")
    plus_button.image = summation_btn_img_photo

    minus_button.config(image=summation_btn_img_photo,compound="center")
    minus_button.image = summation_btn_img_photo

    # Set the width of the buttons to be equal
    plus_button.config(width=10)
    minus_button.config(width=10)

    checkout_button = tk.Button(buttons_frame, text="Checkout", command= lambda:checkout(cursor,sum_parts_window),borderwidth=0, bg=bg_color, font = tkFont.Font(weight="bold", size=14))
    checkout_button.config(image=summation_btn_img_photo_checkout,compound="center")
    checkout_button.image = summation_btn_img_photo_checkout

    plus_button.grid(row=0, column=0, sticky=tk.W + tk.E)
    minus_button.grid(row=0, column=1, sticky=tk.W + tk.E)
    checkout_button.grid(row=1, column=0, columnspan=2, sticky=tk.W + tk.E)

#------------------------------------------- labels -------------------------------------

    global total_value_label
    total_label = tk.Label(buttons_frame, text="Total:", font=("Helvetica", 14, "bold"))
    total_value_label = tk.Label(buttons_frame, text="0", font=("Helvetica", 14, "bold"))

    total_label.config(bg=bg_color)
    total_value_label.config(bg=bg_color)

    total_label.grid(row=2, column=0, pady=5, sticky=tk.W + tk.E)
    total_value_label.grid(row=2, column=1, pady=5, sticky=tk.W + tk.E)


    # Configure column weights to make buttons expand proportionally
    buttons_frame.columnconfigure(0, weight=1)
    buttons_frame.columnconfigure(1, weight=1)

    # Center the window after all components are added
    center_window(sum_parts_window, frame_width, frame_height)

    width = minus_button.winfo_reqwidth()
    print(width)





    global hook_id

    hook_id = keyboard.hook(lambda e: on_barcode_scanned(e, cursor))


    sum_parts_window.protocol("WM_DELETE_WINDOW", on_window_close)

