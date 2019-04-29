from cs50 import get_string
from sys import argv


def main():

    # check command line argument length

    while True:
        print("these many arguments: " + str(len(argv)))
        if  len(argv) > 2 or len(argv) < 2:
            print("Not enough arguments")
            return 1

        print(argv[1])
        dictionary = argv[1]
        break

    #create file name

    fileName = argv[1]

    # read from file and create list out of word on every line
    f = open(fileName, "r")
    words = f.read().splitlines()
    s = set(words)

    message = get_string("what is the message? ")
    msgList = message.split()

    # get input message
    for messageWord in msgList:

        if not messageWord.isalpha():
            print("Invalid string input")
            return 1

    #iterate over message and compare with words list

    i = 0

    for word in words:
        while i < len(msgList):
            if msgList[i].lower() == word.lower():
                msgList[i] = len(msgList[i]) * "*"
            i += 1
        i = 0

    print(' '.join(msgList))


if __name__ == "__main__":
    main()
