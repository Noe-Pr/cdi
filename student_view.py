# student_view.py :

import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class BookCard(tk.Frame):
    def __init__(self, parent, book_id, title, author, available, student_id, width, height, database, *args, **kwargs):
        super().__init__(parent, width=width, height=height, *args, **kwargs)
        self.config(borderwidth=2, relief="groove", background="#154360")
        self.book_id = book_id
        self.student_id = student_id
        self.database = database
        content_frame = tk.Frame(self, background="#154360")
        content_frame.pack(expand=True, fill=tk.BOTH)
        title_label = tk.Label(content_frame, text=title, font=("Courrier", 15), bg="#154360", fg="white", wraplength=width-20)
        title_label.pack(expand=True)
        author_label = tk.Label(content_frame, text=f"par {author}", font=("Courrier", 12), bg="#154360", fg="white", wraplength=width-20)
        author_label.pack(expand=True)
        self.available_label = tk.Label(content_frame, text="", font=("Courrier", 10), bg="#154360", fg="white")
        self.available_label.pack(expand=True)
        self.update_availability(available)
        self.reserve_button = tk.Button(content_frame, text="", command=self.toggle_reservation)
        self.update_reserve_button()

    def update_availability(self, available):
        reservation = self.database.get_reservation_by_book(self.book_id)
        if reservation and reservation[1] != self.student_id:
            self.available_label.config(text="Indisponible")
            self.reserved = False
        elif reservation and reservation[1] == self.student_id:
            self.available_label.config(text="Réservé par vous")
            self.reserved = True
            self.reservation_code = reservation[2]  # Ici, l'indice [2] est correct si reservation_code est le troisième champ dans le tuple
        else:
            self.available_label.config(text="Disponible" if available == 'yes' else "Indisponible")
            self.reserved = False

    def update_reserve_button(self):
        if self.reserved:
            self.reserve_button.config(text="Annuler Réservation", font=("Courrier", 10), bg="#245879", fg="white", width=18)
            self.reserve_button.pack(pady=5)
            self.view_code_button = tk.Button(self, text="Voir le code", font=("Courrier", 10), bg="#245879", fg="white", width=18, command=self.view_reservation_code)
            self.view_code_button.pack(pady=5)
        elif not self.reserved and self.available_label.cget("text") == "Disponible":
            self.reserve_button.config(text="Réserver", font=("Courrier", 12), bg="#245879", fg="white", width=16)
            self.reserve_button.pack(pady=5)
        else:
            self.reserve_button.pack_forget()

    def view_reservation_code(self):
        messagebox.showinfo("Code de Réservation", f"Votre code de réservation est : {self.reservation_code}")

    def toggle_reservation(self):
        if self.reserved:
            reservation = self.database.get_reservation_by_book(self.book_id)
            if reservation:
                self.database.cancel_reservation(reservation[0])
            self.update_availability('yes')
            self.update_reserve_button()
        else:
            if self.database.check_existing_reservation(self.student_id):
                messagebox.showerror("Erreur", "Vous avez déjà réservé un livre.")
                return
            reservation_code = self.database.create_reservation(self.book_id, self.student_id)
            messagebox.showinfo("Réservation", f"Pour récupérer votre livre veuillez vous présenter au CDI et présenter le code suivant : {reservation_code}")
            self.update_availability('no')
            self.update_reserve_button()

class StudentView:
    def __init__(self, master, student_id):
        self.master = master
        self.master.title("CDI DDH : Espace Élève")
        self.database = Database('database/database.db')
        self.student_id = student_id
        self.canvas = tk.Canvas(self.master, background="#154360")
        self.scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.cards_frame = tk.Frame(self.canvas, background="#154360")
        self.canvas_frame_id = self.canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")
        self.master.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.update_books_list()
        self.center_books()

    def center_books(self):
        self.master.after(100, self._center_books)

    def _center_books(self):
        self.canvas.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        cards_frame_width = self.cards_frame.winfo_reqwidth()
        new_x = (canvas_width - cards_frame_width) / 2
        self.canvas.coords(self.canvas_frame_id, new_x, 0)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def update_books_list(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        books = self.database.get_books()
        num_books = len(books)
        num_cols = 5  # Mise à jour du nombre de colonnes à 5
        num_rows = (num_books + num_cols - 1) // num_cols
        card_width = 175
        card_height = 215
        for i in range(num_rows):
            row_frame = tk.Frame(self.cards_frame, background="#154360")
            row_frame.pack(side=tk.TOP, pady=20, expand=True)
            for j in range(num_cols):
                index = i * num_cols + j
                if index < num_books:
                    book = books[index]
                    card = BookCard(row_frame, book[0], book[1], book[2], book[3], self.student_id, card_width, card_height, self.database)
                    card.pack_propagate(False)
                    card.pack(side=tk.LEFT, padx=15, anchor="n")
                    