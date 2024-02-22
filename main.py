# main.py : 

import tkinter as tk
from login_view import LoginView, StudentLoginView
from admin_view import AdminView
from student_view import StudentView
from register_view import RegisterView

def hide_current_frame():
    for widget in root.winfo_children():
        widget.destroy()  # Cela détruira le widget au lieu de simplement le cacher

def show_admin_management_view():
    hide_current_frame()
    AdminView(root)

def show_student_management_view(student_id):
    hide_current_frame()
    StudentView(root, student_id)

def show_register_view():
    hide_current_frame()
    RegisterView(root, show_student_view, hide_current_frame)

def show_student_view():
    hide_current_frame()
    StudentLoginView(root, show_student_management_view, show_register_view)

def show_admin_view():
    hide_current_frame()
    LoginView(root, 'admin', show_admin_management_view)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("CDI DDH")
    root.state('zoomed')
    root.config(background="#154360")
    root.iconbitmap('logo.ico')

    # Créez un Frame comme conteneur pour les boutons
    center_frame = tk.Frame(root)
    center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    center_frame.config(background="#154360")

    # Placez les boutons à l'intérieur du Frame
    student_button = tk.Button(center_frame, text="Espace Élève", font=("Courrier",15), bg="#245879", fg="white", width=20, command=show_student_view)
    student_button.pack()  # Ajoutez un peu d'espace vertical entre les boutons

    admin_button = tk.Button(center_frame, text="Espace Administrateur", font=("Courrier",15), bg="#245879", fg="white", width=20, command=show_admin_view)
    admin_button.pack(pady=20)

    root.mainloop()
    