import string, random, sqlite3
import pyAesCrypt as pyenc
from sqlite3 import Error
from os import path, remove
from datetime import date
import getpass

DB_NAME = "Codes.db"
BUFFER_SIZE = 64 * 1024

def create_connection(dbfile):
    try:
        return sqlite3.connect(dbfile)
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def get_passcode(action):
    return getpass.getpass(f"Enter your Pass Code to {action}: ")

def encrypt_file():
    try:
        pyenc.encryptFile(DB_NAME, f"{DB_NAME}.aes", get_passcode("encrypt"), BUFFER_SIZE)
        remove(DB_NAME)
        print("File encryption successful.")
    except Exception as e:
        print("File encryption failed:", e)

def decrypt_file():
    try:
        pyenc.decryptFile(f"{DB_NAME}.aes", DB_NAME, get_passcode("decrypt"), BUFFER_SIZE)
        remove(f"{DB_NAME}.aes")
    except Exception as e:
        print("File decryption failed:", e)
        exit()

def generate_password(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def initialize_database():
    conn = create_connection(DB_NAME)
    if conn:
        with conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS Passwords (
                            Site TEXT, Password TEXT NOT NULL, DateCreated TEXT);""")
            site = input("Input the site for this password: ")
            password = generate_password(int(input("Enter max chars: ")))
            conn.execute("INSERT INTO Passwords(Site,Password,DateCreated) VALUES (?,?,?)", 
                         (site, password, str(date.today())))
            print("Generated password:", password)

def open_database():
    conn = create_connection(DB_NAME)
    if conn:
        with conn:
            results = conn.execute("SELECT * FROM Passwords").fetchall()
            for row in results:
                print(row)

if __name__ == "__main__":
    choice = int(input("Press 1 to open file or 2 to create password: "))
    if choice == 1:
        if path.exists(f"{DB_NAME}.aes"):
            decrypt_file()
        open_database()
        encrypt_file()
    elif choice == 2:
        if path.exists(f"{DB_NA
