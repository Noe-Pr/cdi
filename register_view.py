# register_view.py :

import tkinter as tk
from tkinter import messagebox
from database import Database

class RegisterView:
    def __init__(self, master, login_callback, hide_callback):
        self.master = master
        self.database = Database('database/database.db')
        self.login_callback = login_callback
        self.hide_callback = hide_callback

        self.center_frame = tk.Frame(self.master)
        self.center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.center_frame.config(background="#154360")

        self.label_username = tk.Label(self.center_frame, text="Nom d'utilisateur :", font=("Courrier",15), bg="#154360", fg="white")
        self.label_username.pack()

        self.entry_username = tk.Entry(self.center_frame, font=("Courrier",15), bg="#245879", fg="white", width=17)
        self.entry_username.pack(pady=7)

        self.label_password = tk.Label(self.center_frame, text="Mot de passe :", font=("Courrier",15), bg="#154360", fg="white")
        self.label_password.pack()

        self.entry_password = tk.Entry(self.center_frame, font=("Courrier",15), bg="#245879", fg="white", width=17, show="*")
        self.entry_password.pack()

        self.button_register = tk.Button(self.center_frame, text="S'inscrire", font=("Courrier",14), bg="#245879", fg="white", width=16, command=self.register)
        self.button_register.pack(pady=23)

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if not username or not password:
            messagebox.showwarning("Attention", "Les champs ne peuvent pas être vides.")
            return
        if self.database.validate_student(username, password):
            messagebox.showerror("Erreur", "L'utilisateur existe déjà.")
            return
        self.database.add_student(username, password)
        messagebox.showinfo("Succès", "Votre compte a bien été créé, vous pouvez maintenant vous connecter.")
        self.back_to_login()

    def back_to_login(self):
        self.hide_callback()
        self.login_callback()
        