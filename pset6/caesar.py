#!/usr/bin/python

import sys
import cs50
import string


def main():

    # print command line arguments
    if len(sys.argv) != 2:
        print("too many arguments")
        return 1

    if not str.isdigit(sys.argv[1]):
        print("this is not a digit")
        return 1


    key = int(sys.argv[1])

    message = cs50.get_string("Enter message: ")

    print("plaintext: " + message)
    print("ciphertext: " , end="")

    for char in message:
        if str.islower(char):
            # convert character to ascii number
            ascChar = ord(char)
            # add ket index and iterate over letter map
            ascChar = ((((ascChar + key) - 97) % 26) + 97)
            # convert back to alphabet
            char = chr(ascChar)
            print (char, end="")

        elif str.isupper(char):
            # convert character to ascii number
            ascChar = ord(char)
            # add ket index and iterate over letter map
            ascChar = ((((ascChar + key) - 65) % 26) + 65)
            # convert back to alphabet
            char = chr(ascChar)
            print (char, end="")
        else:
            print(f"{char}", end="")

    print()



if __name__ == "__main__":
    main()