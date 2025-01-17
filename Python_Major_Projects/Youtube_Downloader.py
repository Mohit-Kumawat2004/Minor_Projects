import pyperclip
from tkinter import *
from threading import *
from tkinter import ttk
from pytube import YouTube
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox, ttk
import time
from pytube.exceptions import RegexMatchError, VideoUnavailable, PytubeError

# Resolution Options(Audio Option is also available)
download_quality = ['144p', '360p', '720p', 'Audio Only']

class Yt_Downloader:
    def __init__(self, root):
        # Setting the Tkinter main window
        self.window = root
        self.window.geometry("700x480")
        self.window.title('YouTube Video and Audio Downloader')
        self.window.resizable(width = False, height = False)

        self.save_to_loc = ''

        # Frame 1: For YouTube Logo
        self.frame_1 = Frame(self.window, width=220, height=80)
        self.frame_1.pack()
        self.frame_1.place(x=20, y=20)

        # Frame 2: For Download Logo
        self.frame_2 = Frame(self.window, width=50, height=50)
        self.frame_2.pack()
        self.frame_2.place(x=235, y=40)

        self.show_yt_logo()
        self.show_dn_logo()

        # About Button
        about_btn = Button(self.window, text="About", \
        font=("Kokila", 10, 'bold'), bg="dodger blue", \
        fg="white", width=5, command=self.About_Window)
        about_btn.place(x=600, y=30)

        # Exit Button
        exit_btn = Button(self.window, text="Exit", \
        font=("Kokila", 10, 'bold'), bg="dodger blue", \
        fg="white", width=5, command=self.Exit_Window)
        exit_btn.place(x=600, y=70)

        # Frame 3: For the Main Page Widgets
        self.frame_3 = Frame(self.window,bg="white",\
        width=700,height=480)
        self.frame_3.place(x=0, y=130)

        # Calling the Main_Window() Function
        self.Main_Window()

    # This function displays the YouTube Logo
    def show_yt_logo(self):
        # Opening the YouTube logo image
        image = Image.open(r"C:\Users\harsh\OneDrive\Pictures\ImagesHotel\ytlogo.png")
        # Resizing the image
        resized_image = image.resize((220, 80))
        # Create an object of tkinter ImageT
        self.img_1 = ImageTk.PhotoImage(resized_image)

        # Create a Label Widget to display the text or Image
        label = Label(self.frame_1, image=self.img_1)
        label.pack()

    # This Function displays the Download logo
    def show_dn_logo(self):
        # The image Path(Opening the image)
        image = Image.open(r"C:\Users\harsh\OneDrive\Pictures\ImagesHotel\logo_download.png")
        resized_image = image.resize((50, 50))

        # Create an object of tkinter ImageTk
        self.img_2 = ImageTk.PhotoImage(resized_image)

        # Create a Label Widget to display the text or Image
        label = Label(self.frame_2, image=self.img_2)
        label.pack()


    # This function displays all the widgets in the Main Page
    def Main_Window(self):
        self.URL = Entry(self.frame_3, \
        font=("Helvetica", 18), width=41)
        self.URL.place(x=20,y=20)

        # Paste URL Button
        paste_btn = Button(self.frame_3, text="Paste URL", \
        command=self.Paste_URL)
        paste_btn.place(x=580,y=20)

        # Resolution Label
        resolution_lbl = Label(self.frame_3, \
        text="Download Quality", \
        font=("Times New Roman", 13, 'bold'))
        resolution_lbl.place(x=150, y=70)

        self.quality = StringVar()
        # Combo Box for showing the available video resolution 
        # and  Audio download options
        self.quality_combobox = ttk.Combobox(self.frame_3, \
        textvariable=self.quality, font=("times new roman",13))
        self.quality_combobox['values'] = download_quality
        self.quality_combobox.current(0)
        self.quality_combobox.place(x=310,y=70)

        # Save To Button: Where the downloaded file will be stored
        save_to_btn = Button(self.frame_3, text="Save To", \
        font=("Kokila", 10, 'bold'), bg="gold", width=6, \
        command=self.Select_Directory)
        save_to_btn.place(x=150, y=110)

        # Tkinter Label sor showing the Save To location path
        # on the window
        self.loc_label = Label(self.frame_3, \
        text=self.save_to_loc, font=("Helvetica", 12), \
        fg='blue', bg='white')
        self.loc_label.place(x=240, y=116)

        status_lbl = Label(self.frame_3, text="Status", \
        font=("Times New Roman", 13, 'bold'))
        status_lbl.place(x=150, y=160)

        # Status Label:
        # Options: 'Not Slected(By Default), or 'Downloading...',
        # or 'Download Completed''
        self.status = Label(self.frame_3, text="Not Selected", \
        font=("Helvetica", 12), bg="white", fg="red")
        self.status.place(x=220, y=163)

        download_btn = Button(self.frame_3, text="Download", \
        font=("Kokila", 13, 'bold'), bg="red", fg="white", \
        width=8, command=self.Threading)
        download_btn.place(x=280, y=210)

    # When the 'Paste URL' button is pressed, this function
    # gets a call and paste the pre-copied text(URL) in the
    # Tkinter Entry Box
    def Paste_URL(self):
        exact_URL = StringVar()
        self.URL.config(textvariable=exact_URL)
        exact_URL.set(str(pyperclip.paste()))
        

    # This function opens the Tkinter file dialog to
    # let users select the save to location for the Yt video
    def Select_Directory(self):
        # Storing the 'saving location' for the result file
        self.save_to_loc = filedialog.askdirectory(title = "Select a location")
        self.loc_label.config(text=self.save_to_loc)
        

    # Creating a different thread to run the 'Download' function
    def Threading(self):
        # Killing a thread through "daemon=True" isn't a good idea
        self.x = Thread(target=self.Download, daemon=True)
        self.x.start()

    def Download(self):
        if self.URL.get() == '':
            messagebox.showwarning('Warning!', "Please Enter a Valid URL")
            return
        
        url = self.URL.get()
        max_retries = 5
        retry_delay = 5  # Start with a 5-second delay

        for attempt in range(max_retries):
            try:
                yt = YouTube(url)
                
                if self.quality_combobox.get() == 'Audio Only':
                    self.status.config(text="Downloading...")
                    audio = yt.streams.filter(type="audio").last()
                    audio.download(output_path=self.save_to_loc)
                else:
                    self.status.config(text="Downloading...")
                    video = yt.streams.filter(mime_type="video/mp4", res=self.quality_combobox.get(), progressive=True).first()
                    video.download(output_path=self.save_to_loc)

                self.status.config(text="Download Completed")
                break  # Exit loop if download was successful

            except (RegexMatchError, VideoUnavailable, PytubeError) as e:
                messagebox.showerror("Error!", f"Video error: {e}")
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)  # Wait before retrying
                    retry_delay *= 2  # Exponential backoff
                else:
                    messagebox.showerror("Error!", f"Error due to {e}")




     # When the 'About' button is pressed, this function gets a call   
    def About_Window(self):
        messagebox.showinfo("Yt Downloader Applications",\
        "Developed by Mohit Kumawat- 2024")
    
    # This function closes the main window
    def Exit_Window(self):
        self.window.destroy()


# The main function
if __name__ == "__main__":
    root = Tk()
    # Creating a 'Yt_Downloader' class object
    obj = Yt_Downloader(root)
    root.mainloop()


    
