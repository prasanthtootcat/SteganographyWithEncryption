import pyAesCrypt
from os import stat, remove

bufferSize = 64 * 1024
password = "holakk"

with open("data.txt.aes", "rb") as fIn:
    with open("dataout.png", "wb") as fOut:
        try:
            encFileSize = stat("data.txt.aes").st_size
            pyAesCrypt.decryptStream(fIn, fOut, password, bufferSize, encFileSize)
        except ValueError:
            print('Error: Incorrect password! Try again!')
            fOut.close()
            remove("dataout.png")