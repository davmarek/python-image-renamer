import os
import sys
import tkinter as tk

from PIL import Image, ImageTk

PROGRAM_NAME = "Renamer"  # název se projevuje v titulku okna
VALID_IMAGES = [".jpg", ".png", ".jpeg"]
APP_PATH = os.path.dirname(sys.executable) + "/"
PROD = False


# in: pole o dvou prvcích (název souboru, koncovka)
# return: název souboru ve formátu "název.jpg"
def f_ext(fext):
    return fext[0] + "." + fext[1]


# return: dvou dimenzionální pole
# example: [ ["nazev1", "jpg"], ["nazev2", "png"] ]
def get_img_addresses():
    images = []

    # gets image addresses from APP_PATH or current directory based on PROD
    files = os.listdir(APP_PATH) if PROD else os.listdir()

    # iterates over the addresses
    for f in files:
        # splits "nazev.jpg" to ("nazev", ".jpg")
        f_tuple = os.path.splitext(f)

        ext = f_tuple[1]  # extension
        if ext.lower() not in VALID_IMAGES:
            continue

        images.append([f_tuple[0], ext[1:]])
    return images


# gets image from address, resizes it to with fixed_height
# and converts it to ImageTk(PIL) to be used in tkinter gui
def get_image(address):
    # open image
    image = Image.open(APP_PATH + address)

    # calculate new image width (height is fixed)
    fixed_height = 420
    height_percent = (fixed_height / float(image.size[1]))
    width_size = int((float(image.size[0]) * float(height_percent)))

    # resize loaded image
    image = image.resize((width_size, fixed_height), Image.ANTIALIAS)

    # convert image to tkinter image
    return ImageTk.PhotoImage(image)


# creates and displays window
# saying that there's no image in the folder
def no_image_window():
    master = tk.Tk()
    master.geometry("400x120+20+20")
    master.title(PROGRAM_NAME)
    master.eval('tk::PlaceWindow . center')

    label = tk.Label(master,
                     text="V aktuální složce není žádný obrázek")

    label.pack(pady=10)
    btn = tk.Button(master,
                    text="Zavřít",
                    command=sys.exit
                    )
    btn.pack(pady=10)
    tk.mainloop()


class ImageRenamer:
    def __init__(self):
        self.addresses = get_img_addresses()

        if len(self.addresses) <= 0:
            no_image_window()
            quit()

        self.master = None
        self.input_name = None
        self.btn_skip = None
        self.label_image = None
        self.construct_main_window()

    def construct_main_window(self):
        self.master = tk.Tk()
        self.master.geometry("800x560+20+40")
        self.update_window_title()

        tk.Label(self.master,
                 text="Zadejte nový název obrázku").pack(pady=10)

        self.input_name = tk.Entry(self.master)
        self.input_name.pack(fill="x", padx=50)

        self.input_name.focus()

        self.btn_skip = tk.Button(self.master,
                                  text="Skip",
                                  command=self.skip_image)
        self.btn_skip.pack(pady=10)

        image = get_image(f_ext(self.addresses[0]))
        self.label_image = tk.Label(self.master, image=image)
        self.label_image.pack()

        self.input_name.bind("<Return>", self.rename_image)
        self.input_name.bind("<Tab>", self.skip_image)
        self.input_name.bind("<Up>", lambda e: self.set_input_text(self.addresses[0][0]))
        self.input_name.bind("<Down>", lambda e: self.set_input_text(""))

        self.master.mainloop()

    def skip_image(self, *e):
        if len(self.addresses) == 1:
            return
        self.addresses.pop(0)

        self.update_window_title()

        self.set_input_text("")

        image = get_image(f_ext(self.addresses[0]))
        self.label_image.configure(image=image)
        self.label_image.image = image

        if len(self.addresses) == 1:
            self.btn_skip["state"] = "disabled"

    def set_input_text(self, text):
        self.input_name.delete(0, tk.END)
        if text != "":
            self.input_name.insert(0, text)

    def rename_image(self, e):
        if self.input_name.get() == "":
            return
        old_name = APP_PATH + f_ext(self.addresses[0])
        new_name = APP_PATH + self.input_name.get() + "." + self.addresses[0][1]
        if old_name != new_name:
            os.rename(old_name, new_name)

        if len(self.addresses) > 1:
            # pokud jsou v addresses další obrázky
            self.skip_image()
            return

        # pokud je zobrazený obrázek poslední
        self.addresses = [[self.input_name.get(), self.addresses[0][1]]]
        self.update_window_title()

    def update_window_title(self):
        self.master.title(PROGRAM_NAME + " - " + f_ext(self.addresses[0]))


def main():
    global APP_PATH
    if not PROD:
        APP_PATH = ""
    ImageRenamer()


if __name__ == "__main__":
    main()
