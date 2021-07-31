#! /bin/python
#code by Mchana
import string , random , sqlite3
import pyAesCrypt as pyenc
from sqlite3 import Error
from os import path, remove
from datetime import date
import getpass
def create_connection(dbfile):
    conn = None
    try:
        conn = sqlite3.connect(dbfile)
        return conn
    except Error as e:
        print(e)

def getCode(function):
	PassCode = getpass.getpass("Enter your Pass Code to {}: ".format(function))
	return PassCode

def encryper():
	bufferSize = 64 * 1024
	PassCode = getCode("encrypt")
	try:
		pyenc.encryptFile("Codes.db","Codes.db.aes",PassCode,bufferSize)
	except Exception as e:
		print("File Encryption Unsucessfull")
		print(e)
	else:
		remove("Codes.db")
		print("File Encryption was Sucessful")
def decrypter():
	bufferSize = 64 * 1024
	PassCode = getCode("decrypt")
	try:
		pyenc.decryptFile("Codes.db.aes","Codes.db",PassCode,bufferSize)
	except Exception as err:
		print("File Decryption Failed")
		print(err)
		exit()
	else:
		remove("Codes.db.aes")

def getchar():
	while True:
		try:
			max_char = int(input("Enter max chars: "))
		except ValueError:
			print("You did not enter a number! ")
		else:
			return max_char

def generateNew():
	max = getchar()
	numbers = [i for i in string.digits]
	upper = [i for i in string.ascii_uppercase]
	lower = [i for i in string.ascii_lowercase]
	generated=[]
	while True:
		if (max-1 >=len(generated)):
			chance = [random.choice(upper),random.choice(lower),random.choice(numbers)]
			generated.append(random.choice(chance))
		else:
			break
	generated = "".join(generated)
	return generated

def initdb():
	conn = create_connection("Codes.db")
	today = str(date.today())
	site = str(input("Input the Site To Be used by this Password: "))
	password = generateNew()
	create_table = """CREATE TABLE IF NOT EXISTS Passwords (
				                                        Site text,
				                                        Password text NOT NULL,
				                                        DateCreated text
				                                    );"""
	sql = '''INSERT INTO Passwords(Site,Password,DateCreated)
						              VALUES(?,?,?)'''
	print(password)
	insertRow = (site,password,today);
	try:
		c = conn.cursor()
		c.execute(create_table)
		c.execute(sql, insertRow)
		c.close()
	except Error as e:
		print(e)
	conn.commit()
def opendb():
	con = sql.connect('Codes.db')
	cur = con.cursor() 
	cur.execute("SELECT * FROM Passwords;")
	results = (cur.fetchall())
if __name__ == "__main__" :
	start = int(input("press 1 to open file or 2 to create password: "))
	if(start == 1):
		if path.exists("Codes.db.aes"):
			decrypter()
			opendb()
			encryper()
		else:
			opendb()
			encryper()
			print("Encryption successfull;\n note:please remember your last password")
	elif(start == 2):
		if path.exists("Codes.db.aes"):
			decrypter()
			initdb()
			encryper()
			print("Encryption successfull;\n note:please remember your last password")
		else:
			initdb()
			
