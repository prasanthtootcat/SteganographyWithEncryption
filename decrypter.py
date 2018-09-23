import pyAesCrypt, hashlib
from os import stat, remove
from PIL import Image 

bufferSize = 64 * 1024

def aes_dec(inputFile, password):
    flag = True
    try:
        with open(inputFile, "rb") as fIn:
            with open("stegano_output.png", "wb") as fOut:
                try:
                    encFileSize = stat(inputFile).st_size
                    pyAesCrypt.decryptStream(fIn, fOut, password, bufferSize, encFileSize)
                except ValueError:
                    print('Error: Incorrect password!')
                    fOut.close()
                    flag = False
                    remove("stegano_output.png")

    except FileNotFoundError:
        flag = False
        print('Encrypted message file not found!')

    if flag:
        return decode()
    else:
        return 'Failed to decrypt!'

def decode(): 
    image = Image.open('stegano_output.png', 'r')
    data = '' 
    imgdata = iter(image.getdata())
    image.close()
    remove("stegano_output.png")
      
    while (True): 
        pixels = [value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]] 
        binstr = '' 
          
        for i in pixels[:8]: 
            if (i % 2 == 0): 
                binstr += '0'
            else: 
                binstr += '1'
                  
        data += chr(int(binstr, 2)) 
        if (pixels[-1] % 2 != 0): 
            return 'The decrypted message is:   '+data

if __name__ == '__main__' :  
    password = input('Enter the password:   ')

    #sha 512 hashing
    password = hashlib.sha512(password.encode('utf-8')).hexdigest()

    #aes decryption and reverse steganography
    print(aes_dec('message.enc',password))