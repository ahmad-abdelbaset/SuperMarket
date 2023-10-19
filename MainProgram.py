import tkinter as tk
from tkinter import messagebox
import ConnectionDB
import tkinter.font as tkFont
import AdminSettings

global level

def open_admin_settings(root,cursor):
    admin_settings_frame = tk.Frame(root)

    AdminSettings.admin_frame(admin_settings_frame,root,cursor)

    # Hide the original main_frame
    main_frame.forget

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def open_checkProducts_window(root):
    checkProducs_window = tk.Toplevel(root)
    checkProducs_window.title("Check Products")

    frame_width = 270
    frame_height = 150
    checkProducs_window.resizable
    center_window(checkProducs_window, frame_width, frame_height)

    label = tk.Label(checkProducs_window, text="Barcode:",font = tkFont.Font(weight="bold", size=10))
    label.pack(pady=10)

    entry = tk.Entry(checkProducs_window)
    entry.pack(pady=10)

    button = tk.Button(checkProducs_window, text="Check Price", font = tkFont.Font(weight="bold", size=10))
    button.pack(pady=10)

def open_main_frame(root,admin,username,cursor):
    style_font = tkFont.Font(weight="bold", size=12)

    if admin:
        level = "High"
    else:
        level = "Low"

    global main_frame

    main_frame = tk.Toplevel(root)
    main_frame.title("Supermarket Management")
    #main_frame.geometry("700x800")
    frame_width = 1100
    frame_height = 750
    main_frame.resizable
    center_window(main_frame, frame_width, frame_height)
    #level_label = tk.Label(main_frame, text="Level: "+ level)
    #level_label.pack()

    # Create the left label
    # Create the left label


    left_label = tk.Label(main_frame, text="User: " + username, font = style_font)
    left_label.grid(row=0, column=0, sticky=tk.NW)

    # Create the right label
    right_label = tk.Label(main_frame, text="Level: " + level, font = style_font)
    right_label.grid(row=0, column=2, sticky=tk.NE)

    # Create the sub-frame under the labels
    sub_frame = tk.Frame(main_frame)
    sub_frame.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW)

    # Center the sub-frame content using the grid layout
    sub_frame.grid_rowconfigure(0, weight=1)
    sub_frame.grid_rowconfigure(1, weight=1)
    sub_frame.grid_rowconfigure(2, weight=1)
    sub_frame.grid_columnconfigure(0, weight=1)

    # Add buttons to the sub-frame

    button1 = tk.Button(sub_frame, text="Check Price", width=50, height=5, font=style_font, command=lambda: open_checkProducts_window(main_frame))
    button2 = tk.Button(sub_frame, text="Sum Products", width=50, height=5, font=style_font)
    button3 = tk.Button(sub_frame, text="Admin Settings", width=50, height=5, font=style_font, command=lambda: open_admin_settings(main_frame,cursor))

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