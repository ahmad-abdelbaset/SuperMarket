import tkinter as tk
from tkinter import messagebox
import ConnectionDB
import tkinter.font as tkFont
import AdminSettings
from PIL import Image, ImageTk
import pygame
import Summation
import sounddevice as sd
from tkinter import ttk



global level
global admin_settings_frame

global bg_color
bg_color = '#EFFFD8'
bg_color_checkProducts = '#BFFAEF'



def open_admin_settings(root,cursor,main_frame_variables):

    pygame.mixer.init()  # Initialize the mixer
    sound = pygame.mixer.Sound("click_sound.wav")  # Replace with your sound file
    sound.play()

    admin_settings_frame = tk.Frame(root, bg=bg_color)

    AdminSettings.admin_frame(admin_settings_frame,root,cursor,main_frame_variables)

    # Hide the original main_frame
    main_frame.forget

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def open_checkProducts_window(root,cursor):

    pygame.mixer.init()  # Initialize the mixer
    sound = pygame.mixer.Sound("click_sound.wav")
    sound.play()


    checkproducts_img = Image.open('check_products_btn.png')
    checkproducts_btn_img = ImageTk.PhotoImage(checkproducts_img)

    button_width = 100  # Set your desired button width
    button_height = 40  # Set your desired button height
    resized_img = checkproducts_img.resize((button_width, button_height), Image.ANTIALIAS)

    checkproducts_btn_img = ImageTk.PhotoImage(resized_img)

    def show_input():
        sound.play()
        try:
            user_input = entry.get()  # Get the input from the Entry widget
            command = 'SELECT Description,SellingPrice FROM products where BarCode =' + user_input
            cursor.execute(command)

            result = cursor.fetchall()

            # Check if the result list is empty
            if not result:
                messagebox.showerror("Product Not Found", f"Product with barcode {user_input} not found.")
            else:
                # Iterate through the results and print them
                for row in result:
                    Description = row[0]
                    Price = row[1]

                    messagebox.showinfo("Product", f"{Description} - {Price} ILS")


        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Something went wrong. Please try again.")

    def show_custom_info(title, message):
        custom_info_window = tk.Toplevel(root)
        custom_info_window.title(title)

        label = tk.Label(custom_info_window, text=message, padx=20, pady=20)
        label.pack()

        ok_button = tk.Button(custom_info_window, text="OK", command=custom_info_window.destroy)
        ok_button.pack(pady=10)


    checkProducs_window = tk.Toplevel(root)
    checkProducs_window.title("Check Products")

    frame_width = 270
    frame_height = 150
    checkProducs_window.resizable
    checkProducs_window.config(bg=bg_color_checkProducts)
    center_window(checkProducs_window, frame_width, frame_height)

    label = tk.Label(checkProducs_window, text="Barcode:",font = tkFont.Font(weight="bold", size=10))
    label.pack(pady=10)
    label.config(bg=bg_color_checkProducts)


    entry = tk.Entry(checkProducs_window)
    entry.pack(pady=10)

    button = tk.Button(checkProducs_window, text="Check Price", width=button_width, height=button_height , font = tkFont.Font(weight="bold", size=10), command=show_input, borderwidth=0, bg=bg_color_checkProducts)
    button.pack(pady=10)
    button.config(image=checkproducts_btn_img,compound="center")
    button.image = checkproducts_btn_img

    checkProducs_window.bind("<Return>", lambda event=None: button.invoke())

def open_main_frame(root,admin,username,cursor):

    main_frame_variables = [root,admin,username,cursor]

    pygame.mixer.init()  # Initialize the mixer
    sound = pygame.mixer.Sound("login.wav")  # Replace with your sound file
    sound.play()

    style_font = tkFont.Font(weight="bold", size=12)

    if admin:
        level = "High"
    else:
        level = "Low"

    global main_frame

    main_frame = tk.Toplevel(root)
    main_frame.title("Supermarket Management")
    #main_frame.geometry("700x800")
    frame_width = 1200
    frame_height = 750
    main_frame.resizable
    center_window(main_frame, frame_width, frame_height)
    #level_label = tk.Label(main_frame, text="Level: "+ level)
    #level_label.pack()

    main_frame.config(bg=bg_color)



    first_image = Image.open('btn1.png')
    first_btn_img = ImageTk.PhotoImage(first_image)

    # Store a reference to the image to prevent it from being garbage collected

    left_label = tk.Label(main_frame, text="User: " + username, font = style_font, bg = bg_color)
    left_label.grid(row=0, column=0, sticky=tk.NW)

    # Create the right label
    right_label = tk.Label(main_frame, text="Level: " + level, font = style_font, bg = bg_color)
    right_label.grid(row=0, column=2, sticky=tk.NE)

    # Create the sub-frame under the labels
    sub_frame = tk.Frame(main_frame,)
    sub_frame.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW)
    sub_frame.config(bg=bg_color)

    # Center the sub-frame content using the grid layout
    sub_frame.grid_rowconfigure(0, weight=1)
    sub_frame.grid_rowconfigure(1, weight=1)
    sub_frame.grid_rowconfigure(2, weight=1)
    sub_frame.grid_columnconfigure(0, weight=1)

    # Add buttons to the sub-frame

    button1 = tk.Button(sub_frame, text="Check Price", width=500, height=50, font=style_font, command=lambda: open_checkProducts_window(main_frame,cursor),borderwidth=0,bg = bg_color)
    button1.config(image=first_btn_img, compound="center", width=first_btn_img.width(), height=first_btn_img.height())
    button1.image = first_btn_img

    button2 = tk.Button(sub_frame, text="Sum Products", width=50, height=5, font=style_font,borderwidth=0,command=lambda: Summation.sum_products(main_frame,cursor),bg = bg_color)
    button2.config(image=first_btn_img, compound="center", width=first_btn_img.width(), height=first_btn_img.height())
    button2.image = first_btn_img

    button3 = tk.Button(sub_frame, text="Admin Settings", width=50, height=5, font=style_font, command=lambda: open_admin_settings(main_frame,cursor,main_frame_variables),borderwidth=0,bg = bg_color)
    button3.config(image=first_btn_img, compound="center", width=first_btn_img.width(), height=first_btn_img.height())
    button3.image = first_btn_img

    #button2 = tk.Button(sub_frame, text="Sum Products", width=50, height=5, font=style_font)


    if level == 'Low':
        button3.config(state=tk.DISABLED)

    # Position the buttons vertically in the center
    button1.grid(row=0, column=0, pady=(0, 20))
    button2.grid(row=1, column=0, pady=(0, 20))
    button3.grid(row=2, column=0, pady=(0, 20))

    # Configure grid weights for resizing
    main_frame.grid_rowconfigure(1, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)


if __name__ == '__main__':
    pass