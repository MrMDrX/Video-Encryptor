import sys
import os
import tkinter as tk
from tkinter import PhotoImage, messagebox, filedialog
import customtkinter as ctk
from PIL import Image
from utils.compressor import compress_video
from utils.decompressor import decompress_video
from utils.encryptor import encrypt_video
from utils.decryptor import decrypt_video

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self._video_path = ctk.StringVar()
        self._secret_key = ctk.StringVar()
        self._status = tk.StringVar()
        self._status.set("---")
        self._PROJECT_FOLDER = os.path.dirname(os.path.realpath(__file__))

        self.title("Video Encryptor")
        self.geometry("800x500")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "images")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(
            image_path, "video_encryptor_logo_512.png")), size=(36, 36))
        self.large_banner = ctk.CTkImage(Image.open(
            os.path.join(image_path, "video_encryptor_banner.png")), size=(500, 150))
        self.browse_icon = ctk.CTkImage(Image.open(
            os.path.join(image_path, "browse_light.png")), size=(20, 20))
        self.compress_icon = ctk.CTkImage(Image.open(
            os.path.join(image_path, "compress_light.png")), size=(20, 20))
        self.decompress_icon = ctk.CTkImage(Image.open(
            os.path.join(image_path, "decompress_light.png")), size=(20, 20))
        self.encrypt_icon = ctk.CTkImage(Image.open(
            os.path.join(image_path, "encrypt_light.png")), size=(20, 20))
        self.decrypt_icon = ctk.CTkImage(Image.open(
            os.path.join(image_path, "decrypt_light.png")), size=(20, 20))
        self.reset_icon = ctk.CTkImage(Image.open(
            os.path.join(image_path, "reset_light.png")), size=(20, 20))
        self.exit_icon_image = ctk.CTkImage(Image.open(
            os.path.join(image_path, "exit_light.png")), size=(20, 20))
        self.encrypt_image = ctk.CTkImage(light_image=Image.open(os.path.join(
            image_path, "encrypt_dark.png")), dark_image=Image.open(os.path.join(image_path, "encrypt_light.png")), size=(20, 20))
        self.decrypt_image = ctk.CTkImage(light_image=Image.open(os.path.join(
            image_path, "decrypt_dark.png")), dark_image=Image.open(os.path.join(image_path, "decrypt_light.png")), size=(20, 20))
        self.about_image = ctk.CTkImage(light_image=Image.open(os.path.join(
            image_path, "about_dark.png")), dark_image=Image.open(os.path.join(image_path, "about_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  Video Encryptor", image=self.logo_image,
                                                   compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.encrypt_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Encrypt",
                                            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                            image=self.encrypt_image, font=ctk.CTkFont(size=15, weight="bold"), anchor="w", command=self.encrypt_button_event)
        self.encrypt_button.grid(row=1, column=0, sticky="ew")

        self.decrypt_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Decrypt",
                                            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                            image=self.decrypt_image, font=ctk.CTkFont(size=15, weight="bold"), anchor="w", command=self.decrypt_button_event)
        self.decrypt_button.grid(row=2, column=0, sticky="ew")

        self.about_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="About",
                                          fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                          image=self.about_image, font=ctk.CTkFont(size=15, weight="bold"), anchor="w", command=self.about_button_event)
        self.about_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=[
            "System", "Dark", "Light"], font=ctk.CTkFont(size=15, weight="bold"), command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(
            row=6, column=0, padx=20, pady=20, sticky="s")
        
        ########################
        # create encrypt frame #
        ########################
        self.encrypt_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.encrypt_frame.grid_columnconfigure(0, weight=1)

        self.encrypt_frame_large_image_label = ctk.CTkLabel(
            self.encrypt_frame, text="", image=self.large_banner)
        self.encrypt_frame_large_image_label.grid(
            row=0, column=0, padx=20, pady=10, columnspan=2, sticky="WE")

        self.file_entry_label_enc = ctk.CTkLabel(
            self.encrypt_frame, text="Enter file path or click select file button", anchor=ctk.W, font=ctk.CTkFont(size=14, weight="bold"))
        self.file_entry_label_enc.grid(
            row=1, column=0, padx=20, pady=10, sticky="W")

        self.file_entry_enc = ctk.CTkEntry(
            self.encrypt_frame,
            textvariable=self._video_path, exportselection=0)
        self.file_entry_enc.grid(
            row=2, column=0, padx=20, pady=10, sticky="WE")

        self.select_btn_enc = ctk.CTkButton(
            self.encrypt_frame, text="Select file", image=self.browse_icon, command=self.selectfile_callback, font=ctk.CTkFont(size=15, weight="bold"))
        self.select_btn_enc.grid(
            row=2, column=1, padx=20, pady=10, sticky="W")

        self.compress_btn = ctk.CTkButton(
            self.encrypt_frame, text="Compress", image=self.compress_icon, command=self.compress_callback, font=ctk.CTkFont(size=15, weight="bold"))  #
        self.compress_btn.grid(
            row=3, column=0, padx=20, pady=10, sticky="WE", columnspan="2")

        self.key_entry_label_enc = ctk.CTkLabel(
            self.encrypt_frame, text="Enter key and remember it for decryption", anchor=ctk.W, font=ctk.CTkFont(size=14, weight="bold"))
        self.key_entry_label_enc.grid(
            row=4, column=0, padx=20, pady=10, sticky="W")

        self.key_entry_enc = ctk.CTkEntry(
            self.encrypt_frame,
            textvariable=self._secret_key, exportselection=0)
        self.key_entry_enc.grid(
            row=5, column=0, padx=20, pady=10, sticky="WE")

        self.encrypt_btn = ctk.CTkButton(
            self.encrypt_frame, text="Encrypt", command=self.encrypt_callback, image=self.encrypt_icon, font=ctk.CTkFont(size=15, weight="bold"))
        self.encrypt_btn.grid(
            row=5, column=1, padx=20, pady=10, sticky="WE")

        self.reset_btn = ctk.CTkButton(
            self.encrypt_frame, text="Reset", command=self.reset_callback, image=self.reset_icon, font=ctk.CTkFont(size=15, weight="bold"))
        self.reset_btn.grid(
            row=6, column=0, padx=20, pady=10, sticky="WE", columnspan="2")
        
        ########################
        # create decrypt frame #
        ########################
        self.decrypt_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.decrypt_frame.grid_columnconfigure(0, weight=1)

        self.decrypt_frame_large_image_label = ctk.CTkLabel(
            self.decrypt_frame, text="", image=self.large_banner)
        self.decrypt_frame_large_image_label.grid(
            row=0, column=0, padx=20, pady=10, columnspan=2, sticky="WE")

        self.file_entry_label_dec = ctk.CTkLabel(
            self.decrypt_frame, text="Enter file path or click select file button", anchor=ctk.W, font=ctk.CTkFont(size=14, weight="bold"))
        self.file_entry_label_dec.grid(
            row=1, column=0, padx=20, pady=10, sticky="W")

        self.file_entry_dec = ctk.CTkEntry(
            self.decrypt_frame,
            textvariable=self._video_path, exportselection=0)
        self.file_entry_dec.grid(
            row=2, column=0, padx=20, pady=10, sticky="WE")

        self.select_btn_dec = ctk.CTkButton(
            self.decrypt_frame, text="Select file", image=self.browse_icon, command=self.selectfile_callback, font=ctk.CTkFont(size=15, weight="bold"))
        self.select_btn_dec.grid(
            row=2, column=1, padx=20, pady=10, sticky="W")

        self.key_entry_label_dec = ctk.CTkLabel(
            self.decrypt_frame, text="Enter old key used for encryption", anchor=ctk.W, font=ctk.CTkFont(size=14, weight="bold"))
        self.key_entry_label_dec.grid(
            row=3, column=0, padx=20, pady=10, sticky="W")

        self.key_entry_dec = ctk.CTkEntry(
            self.decrypt_frame,
            textvariable=self._secret_key, exportselection=0)
        self.key_entry_dec.grid(
            row=4, column=0, padx=20, pady=10, sticky="WE")

        self.decrypt_btn = ctk.CTkButton(
            self.decrypt_frame, text="Decrypt", command=self.decrypt_callback, image=self.decrypt_icon, font=ctk.CTkFont(size=15, weight="bold"))
        self.decrypt_btn.grid(
            row=4, column=1, padx=20, pady=10, sticky="WE")

        self.decompress_btn = ctk.CTkButton(
            self.decrypt_frame, text="Decompress", image=self.decompress_icon, command=self.decompress_callback, font=ctk.CTkFont(size=15, weight="bold"))  #
        self.decompress_btn.grid(
            row=5, column=0, padx=20, pady=10, sticky="WE", columnspan="2")

        self.reset_btn = ctk.CTkButton(
            self.decrypt_frame, text="Reset", command=self.reset_callback, image=self.reset_icon, font=ctk.CTkFont(size=15, weight="bold"))
        self.reset_btn.grid(
            row=6, column=0, padx=20, pady=10, sticky="WE", columnspan="2")
        
        ######################
        # create about frame #
        ######################
        self.about_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.decrypt_frame.grid_columnconfigure(0, weight=1)

        txt = "Welcome to our video compression and encryption application!\nOur tool allows you to compress and encrypt your video files using the Discrete Wavelet Transform (DWT) and Advanced Encryption \nStandard (AES) algorithms. You can also decompress and decrypt \nthe compressed and encrypted videos using the same tool.\n\nOur application is designed to be easy to use, with a user-friendly \ninterface that guides you through the compression and encryption process. \n\nWe hope that our tool will help you to protect your video files and \nreduce their size without sacrificing quality.\nThank you for using our application!\n\n\tThis project is licensed under the MIT License\n\n\t\t© Made with ❤️ by Med0X"

        self.about_txt = ctk.CTkTextbox(
            self.about_frame, width=550, height=400, font=ctk.CTkFont(size=18, weight="normal"))
        self.about_txt.insert("0.0", text=txt)
        self.about_txt.grid(
            row=1, column=0, padx=20, pady=10)

        self.exit_btn = ctk.CTkButton(
            self.about_frame, text="Exit", command=self.destroy, image=self.exit_icon_image, font=ctk.CTkFont(size=15, weight="bold"), anchor=tk.CENTER)
        self.exit_btn.grid(
            row=2, column=0, padx=20, pady=20, sticky="S")

        # select default frame
        self.select_frame_by_name("Encrypt")

    def selectfile_callback(self):
        try:
            name = filedialog.askopenfile()
            self._video_path.set(name.name)
            print(name.name)
        except Exception as e:
            self._status.set(e)
            self.status_label.update()

    def compress_callback(self):
        input_video = self._video_path.get()
        output_video = self._PROJECT_FOLDER + "/videos/compressed_video.mp4"
        compress_video(input_video, output_video)
        messagebox.showinfo('Compression Complete',
                            f'Compressed video saved to {output_video}.')

    def decompress_callback(self):
        input_video = self._PROJECT_FOLDER + "/videos/decrypted_video.mp4"
        output_video = self._PROJECT_FOLDER + "/videos/decompressed_video.mp4"
        decompress_video(input_video, output_video)
        messagebox.showinfo('Decompression Complete',
                            f'Decompressed video saved to {output_video}.')

    def encrypt_callback(self):
        input_video = self._PROJECT_FOLDER + "/videos/compressed_video.mp4"
        output_video = self._PROJECT_FOLDER + "/videos/encrypted_video.mp4"
        encrypt_video(input_video, output_video, self._secret_key.get())
        messagebox.showinfo('Encryption complete',
                            f'Encrypted video saved to {output_video}.')

    def decrypt_callback(self):
        input_video = self._video_path.get()
        output_video = self._PROJECT_FOLDER + "/videos/decrypted_video.mp4"
        decrypt_video(input_video, output_video, self._secret_key.get())
        messagebox.showinfo('Decryption complete',
                            f'Decrypted video saved to {output_video}.')

    def reset_callback(self):
        self._cipher = None
        self._video_path.set("")
        self._secret_key.set("")
        self._status.set("---")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.encrypt_button.configure(
            fg_color=("gray75", "gray25") if name == "Encrypt" else "transparent")
        self.decrypt_button.configure(
            fg_color=("gray75", "gray25") if name == "Decrypt" else "transparent")
        self.about_button.configure(
            fg_color=("gray75", "gray25") if name == "About" else "transparent")

        # show selected frame
        if name == "Encrypt":
            self.encrypt_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.encrypt_frame.grid_forget()
        if name == "Decrypt":
            self.decrypt_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.decrypt_frame.grid_forget()
        if name == "About":
            self.about_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.about_frame.grid_forget()

    def encrypt_button_event(self):
        self.select_frame_by_name("Encrypt")

    def decrypt_button_event(self):
        self.select_frame_by_name("Decrypt")

    def about_button_event(self):
        self.select_frame_by_name("About")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = App()
    app.mainloop()

'''
/**********************************************************
 **  ©Med0X All rights reserved to me @MrMdrX in Github  **
 **               https://mrmdrx.github.io               **
 *********************************************************/
 '''