# database.py :

import sqlite3
import random
import string

class Database:
    def __init__(self, db_filename):
        self.connection = sqlite3.connect(db_filename)
        self.cursor = self.connection.cursor()

    def get_books(self):
        self.cursor.execute("SELECT id, titre, auteur, disponible FROM livre")
        return self.cursor.fetchall()

    def get_book_by_id(self, book_id):
        self.cursor.execute("SELECT titre, auteur, disponible FROM livre WHERE id = ?", (book_id,))
        book = self.cursor.fetchone()
        return {'titre': book[0], 'auteur': book[1], 'disponible': book[2]} if book else None

    def add_book(self, titre, auteur):
        self.cursor.execute("INSERT INTO livre (titre, auteur, disponible) VALUES (?, ?, 'yes')", (titre, auteur))
        self.connection.commit()

    def remove_book(self, book_id):
        self.cursor.execute("DELETE FROM livre WHERE id = ?", (book_id,))
        self.connection.commit()

    def update_book(self, book_id, titre, auteur):
        self.cursor.execute("UPDATE livre SET titre = ?, auteur = ? WHERE id = ?", (titre, auteur, book_id))
        self.connection.commit()

    def update_book_availability(self, book_id, new_availability):
        self.cursor.execute("UPDATE livre SET disponible = ? WHERE id = ?", (new_availability, book_id))
        self.connection.commit()

    def validate_admin(self, username, password):
        self.cursor.execute("SELECT id FROM admin WHERE username = ? AND password = ?", (username, password))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def validate_student(self, username, password):
        self.cursor.execute("SELECT id FROM eleve WHERE username = ? AND password = ?", (username, password))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def add_student(self, username, password):
        self.cursor.execute("INSERT INTO eleve (username, password) VALUES (?, ?)", (username, password))
        self.connection.commit()

    def create_reservation(self, book_id, student_id):
        reservation_code = ''.join(random.choices(string.ascii_uppercase, k=3))
        self.cursor.execute("INSERT INTO reservation (book_id, student_id, reservation_code) VALUES (?, ?, ?)", (book_id, student_id, reservation_code))
        self.connection.commit()
        return reservation_code

    def check_existing_reservation(self, student_id):
        self.cursor.execute("SELECT * FROM reservation WHERE student_id = ?", (student_id,))
        return self.cursor.fetchone()

    def cancel_reservation(self, reservation_id):
        self.cursor.execute("DELETE FROM reservation WHERE id = ?", (reservation_id,))
        self.connection.commit()

    def get_reserved_books(self):
        self.cursor.execute("""
            SELECT livre.titre, livre.auteur, reservation.reservation_code, eleve.username
            FROM reservation
            JOIN livre ON reservation.book_id = livre.id
            JOIN eleve ON reservation.student_id = eleve.id
        """)
        return self.cursor.fetchall()

    def get_reservation_by_book(self, book_id):
        self.cursor.execute("SELECT id, student_id, reservation_code FROM reservation WHERE book_id = ?", (book_id,))
        return self.cursor.fetchone()

    def __del__(self):
        self.connection.close()
        