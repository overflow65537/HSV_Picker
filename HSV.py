from tkinter import Tk, Label, Canvas, NW, filedialog, Button
from PIL import Image, ImageTk, ImageDraw
import colorsys
import pyperclip

def get_hsv(event):

    x, y = event.x, event.y
    r, g, b = img.getpixel((x, y))

    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

    h = int(h * 255)
    s = int(s * 255)
    v = int(v * 255)

    print(f"HSV: {h}, {s}, {v}")

    hsv_str = f"{h}, {s}, {v}"
    pyperclip.copy(hsv_str)

def select_image():
    global img, canvas  

    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
    )
    if file_path:
        img = Image.open(file_path)
        photo = ImageTk.PhotoImage(img)

        canvas.config(width=img.width, height=img.height)
        canvas.create_image(0, 0, anchor=NW, image=photo)
        canvas.image = photo

def start_selection(event):
    global selection_start
    selection_start = (event.x, event.y)

def end_selection(event):
    global selection_start, selection_end
    selection_end = (event.x, event.y)
    calculate_hsv_range()

def calculate_hsv_range():
    global img, selection_start, selection_end
    min_hsv = [255, 255, 255]
    max_hsv = [0, 0, 0]

    for x in range(selection_start[0], selection_end[0]):
        for y in range(selection_start[1], selection_end[1]):
            r, g, b = img.getpixel((x, y))
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            h, s, v = int(h * 255), int(s * 255), int(v * 255)

            min_hsv = [min(min_hsv[0], h), min(min_hsv[1], s), min(min_hsv[2], v)]
            max_hsv = [max(max_hsv[0], h), max(max_hsv[1], s), max(max_hsv[2], v)]

    print(f"Min HSV: {min_hsv}, Max HSV: {max_hsv}")


root = Tk()
root.title("HSV Picker")

select_button = Button(root, text="选择图片", command=select_image)
select_button.pack()

canvas = Canvas(root)
canvas.pack()

canvas.bind("<Button-1>", start_selection)
canvas.bind("<ButtonRelease-1>", end_selection)

root.mainloop()
