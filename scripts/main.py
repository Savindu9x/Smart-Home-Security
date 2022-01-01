# Written by Savindu9x
# Version:1.0
# File No:0.0
# Source: https://github.com/Savindu9x/ECE4810/tree/main/Project

# Importing modules
import presenceDetection
import enablePermission
import tempPrediction
import loadInterface
import time
import threading
# Main block of code



def main():
    print("0.1: Welcome to inGrid Smart Door System")
    presenceDetection.objectDetect()
    loadInterface.loginPage()

    print("so far so good")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


