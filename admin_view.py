# admin_view.py :

import tkinter as tk
from tkinter import messagebox
from database import Database

class AdminView:
    def __init__(self, master):
        self.master = master
        self.master.title("CDI DDH : Espace Administrateur")
        self.database = Database('database/database.db')
        self.book_ids = []
        self.selected_book_id = None

        self.center_frame = tk.Frame(self.master)
        self.center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.center_frame.config(background="#154360")

        self.label = tk.Label(self.center_frame, text="Gestion des Livres", font=("Courrier",22), bg="#154360", fg="white")
        self.label.pack(pady=25)

        self.title_label = tk.Label(self.center_frame, text="Titre :", font=("Courrier",17), bg="#154360", fg="white")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.center_frame, font=("Courrier",15), bg="#245879", fg="white", width=17)
        self.title_entry.pack(pady=8)

        self.author_label = tk.Label(self.center_frame, text="Auteur :", font=("Courrier",17), bg="#154360", fg="white")
        self.author_label.pack()
        self.author_entry = tk.Entry(self.center_frame, font=("Courrier",15), bg="#245879", fg="white", width=17)
        self.author_entry.pack(pady=8)

        self.add_button = tk.Button(self.center_frame, text="Ajouter Livre", font=("Courrier",14), bg="#245879", fg="white", width=18, command=self.add_book)
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(self.center_frame, text="Supprimer Livre", font=("Courrier",14), bg="#245879", fg="white", width=18, command=self.remove_book)
        self.remove_button.pack(pady=5)

        self.update_button = tk.Button(self.center_frame, text="Mettre à Jour Livre", font=("Courrier",14), bg="#245879", fg="white", width=18, command=self.update_book)
        self.update_button.pack(pady=5)

        self.toggle_availability_button = tk.Button(self.center_frame, text="Changer Disponibilité", font=("Courrier",14), bg="#245879", fg="white", width=18, command=self.toggle_book_availability)
        self.toggle_availability_button.pack(pady=5)

        self.view_reservations_button = tk.Button(self.center_frame, text="Voir Réservations", font=("Courrier",14), bg="#245879", fg="white", width=18, command=self.view_reservations)
        self.view_reservations_button.pack(pady=5)

        self.books_listbox = tk.Listbox(self.center_frame, font=("Courrier",11), bg="#245879", fg="white", width=50)
        self.books_listbox.pack(pady=20)
        self.books_listbox.bind('<<ListboxSelect>>', self.on_book_select)

        self.update_books_list()

    def update_books_list(self):
        self.books_listbox.delete(0, tk.END)
        self.book_ids.clear()
        for book in self.database.get_books():
            self.books_listbox.insert(tk.END, f"{book[1]} par {book[2]}   -   {'Disponible' if book[3] == 'yes' else 'Indisponible'}")
            self.book_ids.append(book[0])

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        if not title.strip() or not author.strip():
            messagebox.showwarning("Attention", "Veillez à remplir tous les champs.")
            return
        self.database.add_book(title, author)
        self.update_books_list()

    def remove_book(self):
        selected_indices = self.books_listbox.curselection()
        if not selected_indices:
            return
        selected_index = selected_indices[0]
        book_id = self.book_ids[selected_index]
        self.database.remove_book(book_id)
        self.update_books_list()

    def update_book(self):
        if self.selected_book_id is None:
            messagebox.showwarning("Attention", "Aucun livre sélectionné pour la mise à jour.")
            return
        title = self.title_entry.get()
        author = self.author_entry.get()
        if not title.strip() or not author.strip():
            messagebox.showwarning("Attention", "Veillez à remplir tous les champs.")
            return
        self.database.update_book(self.selected_book_id, title, author)
        self.update_books_list()
        self.selected_book_id = None

    def toggle_book_availability(self):
        selected_indices = self.books_listbox.curselection()
        if not selected_indices:
            return
        selected_index = selected_indices[0]
        book_id = self.book_ids[selected_index]
        book = self.database.get_book_by_id(book_id)
        new_availability = 'no' if book['disponible'] == 'yes' else 'yes'
        self.database.update_book_availability(book_id, new_availability)
        reservation = self.database.get_reservation_by_book(book_id)
        if reservation and new_availability == 'no':
            self.database.cancel_reservation(reservation['id'])
        self.update_books_list()

    def view_reservations(self):
        reserved_books = self.database.get_reserved_books()
        reservations_str = "\n".join([f"{title} par {author}, Réservé par: {username}, Code: {code}" for title, author, code, username in reserved_books])
        messagebox.showinfo("Livres Réservés", reservations_str)

    def on_book_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.selected_book_id = self.book_ids[index]
            book = self.database.get_book_by_id(self.selected_book_id)
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, book['titre'])
            self.author_entry.delete(0, tk.END)
            self.author_entry.insert(0, book['auteur'])
            