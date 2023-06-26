import tkinter as tk
import hashlib
from tkinter import filedialog


def getwordlist():
    # This generates a simple GUI file dialog for Windows devices.
    # Mostly because I got tired of typing filepaths
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path


def crack(file_path, hash):
    # The section of the program that compares the hashes.

    # Opens the file and strips the new line character off.
    # The newline character can actually alter the hash if not stripped
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    # This loop reads the file, hashes each word, and converts the unicode word into binary
    for line in lines:
        hashed_line = hashlib.sha256(line.encode('utf-8')).hexdigest()
        print(hash, ">", hashed_line)

        # Below we do a simple comparison of the two hashes
        if hashed_line == hash:
            print("We found a match!")
            print(line, ":", hashed_line)
            return
    else:
        print("No matches found.")


def main():
    print("""                                                                                                                                       
 ____  _   _    _    ____  ____   __      ____                _             
/ ___|| | | |  / \  |___ \| ___| / /_    / ___|_ __ __ _  ___| | _____ _ __ 
\___ \| |_| | / _ \   __) |___ \| '_ \  | |   | '__/ _` |/ __| |/ / _ \ '__|
 ___) |  _  |/ ___ \ / __/ ___) | (_) | | |___| | | (_| | (__|   <  __/ |   
|____/|_| |_/_/   \_\_____|____/ \___/   \____|_|  \__,_|\___|_|\_\___|_| """)
    userhash = input("Please enter your hash: ")
    print("Please navigate to your wordlist.")
    file = getwordlist()
    crack(file, userhash)


main()
