# login_view.py :

import tkinter as tk
from tkinter import messagebox
from database import Database

class LoginView:
    def __init__(self, master, role, success_callback, failure_callback=None):
        self.master = master
        self.role = role
        self.success_callback = success_callback
        self.failure_callback = failure_callback
        self.database = Database('database/database.db')

        self.center_frame = tk.Frame(self.master)
        self.center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.center_frame.config(background="#154360")

        self.label_username = tk.Label(self.center_frame, text="Nom d'utilisateur :", font=("Courrier",15), bg="#154360", fg="white")
        self.label_username.pack()

        self.entry_username = tk.Entry(self.center_frame, font=("Courrier",15), bg="#245879", fg="white", width=17)
        self.entry_username.pack(pady = 7)

        self.label_password = tk.Label(self.center_frame, text="Mot de passe :", font=("Courrier",15), bg="#154360", fg="white")
        self.label_password.pack(pady = 0)

        self.entry_password = tk.Entry(self.center_frame, font=("Courrier",15), bg="#245879", fg="white", width=17, show="*")
        self.entry_password.pack(pady = 7)

        self.button_login = tk.Button(self.center_frame, text="Connexion", font=("Courrier",14), bg="#245879", fg="white", width=16, command=self.login)
        self.button_login.pack(pady = 10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if self.role == 'admin':
            admin_id = self.database.validate_admin(username, password)
            if admin_id:
                self.success_callback()
            else:
                messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")
                if self.failure_callback:
                    self.failure_callback()
        elif self.role == 'student':
            student_id = self.database.validate_student(username, password)
            if student_id:
                self.success_callback(student_id)
            else:
                messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")
                if self.failure_callback:
                    self.failure_callback()

    def register(self):
        self.registrer_callback()
        
class StudentLoginView(LoginView):
    def __init__(self, master, success_callback, register_callback):
        super().__init__(master, 'student', success_callback)
        self.register_callback = register_callback
        
        self.label_password = tk.Label(self.center_frame, text="Ou", font=("Courrier",13), bg="#154360", fg="white")
        self.label_password.pack()
        self.button_register = tk.Button(self.center_frame, text="S'inscrire", font=("Courrier",14), bg="#245879", fg="white", width=16, command=self.register)
        self.button_register.pack(pady = 10)

    def register(self):
        self.register_callback()
        