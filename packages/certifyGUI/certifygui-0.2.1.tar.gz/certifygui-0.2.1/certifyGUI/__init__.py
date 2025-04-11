import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

positions = []
clicked = 0

def on_click(event, canvas, image_on_canvas, header_labels):
    global clicked, positions
    if clicked < len(header_labels):
        x, y = event.x, event.y
        positions.append((x, y))
        canvas.create_oval(x-5, y-5, x+5, y+5, outline="red", width=2)
        canvas.create_text(x+40, y, text=header_labels[clicked], fill="blue", anchor="w")
        clicked += 1
        if clicked == len(header_labels):
            canvas.quit()

def get_positions_gui(image_path, headers):
    global positions, clicked
    clicked = 0
    positions = []

    window = tk.Tk()
    window.title("Click positions for each column")

    img = Image.open(image_path)
    tk_img = ImageTk.PhotoImage(img)
    canvas = tk.Canvas(window, width=img.width, height=img.height)
    canvas.pack()
    canvas_image = canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)

    label = tk.Label(window, text=f"Click on the image for each of the following headers in order:\n{headers}")
    label.pack()

    canvas.bind("<Button-1>", lambda e: on_click(e, canvas, canvas_image, headers))

    window.mainloop()
    window.destroy()
    return positions

def get_font_styles_and_colors(headers):
    font_styles = []
    font_sizes = []
    font_colors = []

    def on_submit():
        # Collect values before destroying the window
        for i in range(len(headers)):
            font_sizes.append(int(size_entries[i].get()))
            font_styles.append(font_options[i].get())
            font_colors.append(color_entries[i].get())
        style_window.destroy()

    style_window = tk.Tk()
    style_window.title("Font Customization")

    size_entries = []
    font_options = []
    color_entries = []

    fonts = ["arial.ttf", "times.ttf", "calibri.ttf", "cour.ttf"]

    for i, header in enumerate(headers):
        tk.Label(style_window, text=f"{header}").grid(row=i, column=0)

        size_entry = tk.Entry(style_window)
        size_entry.insert(0, "30")
        size_entry.grid(row=i, column=1)
        size_entries.append(size_entry)

        font_var = tk.StringVar(style_window)
        font_var.set(fonts[0])
        font_menu = tk.OptionMenu(style_window, font_var, *fonts)
        font_menu.grid(row=i, column=2)
        font_options.append(font_var)

        color_entry = tk.Entry(style_window)
        color_entry.insert(0, "black")
        color_entry.grid(row=i, column=3)
        color_entries.append(color_entry)

    submit_btn = tk.Button(style_window, text="OK", command=on_submit)
    submit_btn.grid(row=len(headers), columnspan=4)

    style_window.mainloop()
    return font_sizes, font_styles, font_colors

def show_preview(template_path, row, headers, positions, sizes, fonts, colors):
    cert = Image.open(template_path).copy()
    draw = ImageDraw.Draw(cert)

    for i in range(len(headers)):
        text = str(row[headers[i]])
        x, y = positions[i]
        y -= sizes[i] // 2  # Fix vertical offset
        try:
            font = ImageFont.truetype(fonts[i], sizes[i])
        except:
            font = ImageFont.load_default()
        draw.text((x, y), text, font=font, fill=colors[i])

    preview_path = "preview_sample.png"
    cert.save(preview_path)

    win = tk.Tk()
    win.title("Preview")
    img = ImageTk.PhotoImage(cert)
    canvas = tk.Canvas(win, width=cert.width, height=cert.height)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=img)

    def proceed():
        win.quit()

    def cancel():
        win.destroy()
        raise SystemExit("User cancelled after preview.")

    tk.Button(win, text="Generate All", command=proceed).pack(side="left", padx=20, pady=10)
    tk.Button(win, text="Cancel", command=cancel).pack(side="right", padx=20, pady=10)

    win.mainloop()
    win.destroy()

def certify(cert_image_path, excel_path, n, name_format_index=None):
    df = pd.read_excel(excel_path)
    cert_template = Image.open(cert_image_path)

    headers = df.columns[:n].tolist()
    positions_selected = get_positions_gui(cert_image_path, headers)
    font_sizes, font_names, font_colors = get_font_styles_and_colors(headers)

    # Show preview for first row
    show_preview(cert_image_path, df.iloc[0], headers, positions_selected, font_sizes, font_names, font_colors)

    output_folder = "certificates"
    os.makedirs(output_folder, exist_ok=True)

    for index, row in df.iterrows():
        cert = cert_template.copy()
        draw = ImageDraw.Draw(cert)

        for i in range(n):
            value = str(row[headers[i]])
            x, y = positions_selected[i]
            y -= font_sizes[i] // 2  # Adjust vertically
            try:
                font = ImageFont.truetype(font_names[i], font_sizes[i])
            except:
                font = ImageFont.load_default()
            draw.text((x, y), value, font=font, fill=font_colors[i])

        file_name = (
            str(row[df.columns[name_format_index]]) if name_format_index is not None else str(row[df.columns[0]])
        ) + ".png"
        cert.save(os.path.join(output_folder, file_name))

    messagebox.showinfo("Done", f"{len(df)} certificates created in '{output_folder}' folder.")

# Usage:
certify("certificate.png", "data.xlsx", 4, name_format_index=0)
exit()