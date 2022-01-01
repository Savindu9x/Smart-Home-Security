import xlsxwriter
import pandas as pd
from tkinter import messagebox
from tkinter.constants import TRUE
from Crypto.Hash import SHA256
#other package Required: openyxl

def hash_data(data):
    salt='Th1sIsEce48o154Lt' # Salt for Hash
    data = (data+salt).encode('utf-8') # Convert String to Bits
    hash_object = SHA256.new(data).hexdigest() # utput encoded in hexadecimal.
    return hash_object

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('account_ECE4810.xlsx')
worksheet = workbook.add_worksheet()
# Some data we want to write to the worksheet.
account = (
    ['username', 'password'],
    ['pasan',  '123'],
    ['arief',  '321'],
    ['dinidu',  'abc'],
    ['ravindu',  'cba'],
)
# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0

# Iterate over the data and write it out row by row.
for username, password in (account):
    if (row<1):
        worksheet.write(row, col,     username) #Write in the username first
        worksheet.write(row, col + 1, password) # Write in password after
        row += 1
    else:
        worksheet.write(row, col,     username) #Write in the username first
        worksheet.write(row, col + 1, hash_data(password)) # Write in password after
        row += 1

workbook.close()




