import pyAesCrypt, hashlib
from os import stat, remove
from PIL import Image 

bufferSize = 64 * 1024

def aes_enc(inputFile, outputFile, password):
    with open(inputFile, "rb") as fIn:
         with open(outputFile, "wb") as fOut:
             pyAesCrypt.encryptStream(fIn, fOut, password, bufferSize)
    fIn.close()
    remove(inputFile)

def genData(data):  
        newd = []  
          
        for i in data: 
            newd.append(format(ord(i), '08b')) 
        return newd 
           
def modPix(pix, data):     
    datalist = genData(data) 
    lendata = len(datalist) 
    imdata = iter(pix) 
  
    for i in range(lendata):  
        pix = [value for value in imdata.__next__()[:3] +
                                  imdata.__next__()[:3] +
                                  imdata.__next__()[:3]] 
        for j in range(0, 8): 
            if (datalist[i][j]=='0') and (pix[j]% 2 != 0): 
                if (pix[j]% 2 != 0): 
                    pix[j] -= 1
            elif (datalist[i][j] == '1') and (pix[j] % 2 == 0): 
                pix[j] -= 1

        if (i == lendata - 1): 
            if (pix[-1] % 2 == 0): 
                pix[-1] -= 1
        else: 
            if (pix[-1] % 2 != 0): 
                pix[-1] -= 1
  
        pix = tuple(pix) 
        yield pix[0:3] 
        yield pix[3:6] 
        yield pix[6:9] 
  
def encode_enc(newimg, data): 
    w = newimg.size[0] 
    (x, y) = (0, 0) 
      
    for pixel in modPix(newimg.getdata(), data):  
        newimg.putpixel((x, y), pixel) 
        if (x == w - 1): 
            x = 0
            y += 1
        else: 
            x += 1
              
def encode(): 
    img = input("Enter the image name for steganography:   ") 
    try:
        image = Image.open(img, 'r')
        
        data = input("Enter the secret message for transmission:   ") 
        if (len(data) == 0): 
            raise ValueError('Message is blank!')

        newimg = image.copy() 
        encode_enc(newimg, data)
        newimg.save('stegano_'+img)
        password = input('Enter the password for encryption:   ')
        password = hashlib.sha512(password.encode('utf-8')).hexdigest()
        
        aes_enc('stegano_'+img,'message.enc', password)

    except FileNotFoundError:
        print('Incorrect file name / File does not exist!')

if __name__ == '__main__' :  
    encode()
