# Written by Savindu9x
# Version:1.0
# File No:0.1
# Source: https://github.com/Savindu9x/ECE4810/tree/main/Project

#Instructions
# 1. Run the main.py


# Contents of the file
# Activity 04 - login page
# Activity 05 - security encryption and decryption

import time
import os, random, string
from tkinter import Tk, Label, Entry, Button, messagebox, PhotoImage
import tkinter as tk
import PIL.Image as Image
import PIL.ImageTk as ImageTk

from functools import partial
import enablePermission

def loginPage():
    #Setting up the tkinter window
    root = Tk()
    root.title('Main Login Page')
    canvas1 = tk.Canvas(root, width=600, height=400, relief='raised')
    canvas1.pack()

    #from PIL import ImageTk, Image
    bg = ImageTk.PhotoImage(Image.open("ez.jpg"))

    # Show image using label
    label1 = Label(root, image=bg)
    label1.place(x=0, y=0)

    # Define Label for Sign in text
    toptextlabel = Label(root, text="Sign In", bg="#BFD0D8")
    canvas1.create_window(350, 25, window=toptextlabel)
    toptextlabel.config(font=('Helvetica', 14, 'bold'))

    # Define Label and textbox for username input
    userNamelabel = Label(root, text="Username", bg="#BFD0D8")
    canvas1.create_window(350, 75, window=userNamelabel)
    userNamelabel.config(font=('Helvetica', 10, 'bold'))

    # Box to Enter the userName
    user = Entry(root)
    canvas1.create_window(380, 100, window=user)

    # Define Label and textbox for password input
    passwordlabel = Label(root, text="Password", bg="#BFD0D8")
    canvas1.create_window(350, 150, window=passwordlabel)
    passwordlabel.config(font=('Helvetica', 10, 'bold'))

    # Box to Enter the password
    passwd = Entry(root, show='*')
    canvas1.create_window(380, 175, window=passwd, )

    # Define Label for help link
    helplabel = Label(root, text="Forgot password?", bg="#BFD0D8")
    canvas1.create_window(380, 197, window=helplabel)
    helplabel.config(font=('Helvetica', 8, 'bold'))

    def grantAccess():
        userName = str(user.get())
        password = str(passwd.get())
        permission, message  = enablePermission.validateLogin(userName, password)
        if permission:

            messagebox.showinfo("showinfo", message)
            # Exit the current window
            root.destroy()
            # calling the second window for verification code
            verify_key = enablePermission.generateVerifyCode()
            verificationPage(verify_key)
        else:
            # Show user access denied error
            messagebox.showinfo("showinfo", message)
            # return user back to login page to enter his creditionals
            root.destroy()
            loginPage()

    # Login Button
    loginButton = Button(root, text="LOGIN", font=(('Helvetica', 12, 'bold')), command=lambda: grantAccess())
    canvas1.create_window(375,250, window=loginButton)

    root.mainloop()


def verificationPage(verify_key):
    # Re-Creating main window
    root = Tk()
    root.title('Two-factor Authentication')
    canvas1 = tk.Canvas(root, width=640, height=480, relief='raised')
    canvas1.pack()

    # from PIL import ImageTk, Image
    bg = ImageTk.PhotoImage(Image.open("ez.jpg"))

    # Show image using label
    label1 = Label(root, image=bg)
    label1.place(x=0, y=0)

    # Define textbox for label
    textlabel = Label(root, text="Enter Verification code", bg="#BFD0D8")
    canvas1.create_window(400, 100, window=textlabel)
    textlabel.config(font=('Helvetica', 12, 'bold'))

    # Box to Enter the verification code
    vericode = Entry(root)
    canvas1.create_window(390, 130, window=vericode)

    # function to verify the entered the password is equal to generated password.
    def verify():
        verification_code = str(vericode.get()) #get the user entered verification code
        # returns permission true, if entered code similar to produced key.
        permission, message = enablePermission.compareVerifyCode(verification_code, verify_key)

        if permission: # permission successful, lets the user enter.
            messagebox.showinfo("show info", message)
            root.destroy()
            enablePermission.doorUnlock()
        else:
            counter = 1
            if counter == 1:
                messagebox.showinfo("show info", message)
                counter = counter + 1
            else:
                messagebox.showinfo("show info", 'Verification Failed.Please generate new OTP')

    # function to resend the code once the user failed to
    # enter correct code.
    def resend_code():
        verify_key = enablePermission.generateVerifyCode()
        root.destroy()
        verificationPage(verify_key)

    # Verify code Button
    verifyButton = Button(root, text="Verify Code", font=(('Helvetica', 12, 'bold')), command=lambda: verify())
    canvas1.create_window(400, 170, window=verifyButton)

    # Resend Button
    resendButton = Button(root, text="Resend Code", font=(('Helvetica', 12, 'bold')), command=lambda: resend_code())
    canvas1.create_window(400, 220, window=resendButton)

    root.mainloop()


