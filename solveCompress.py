import math
import time
from tkinter import filedialog

import numpy
import pylab
from PIL import Image
from appJar import gui
from scipy.fftpack.realtransforms import dct
from scipy.fftpack.realtransforms import idct
import os

# VARIABILI GLOBALI
BMP_PATH = K = L = A_OR_B = None


class NewGui:
    def __init__(self):
        # create the GUI & set a title
        app = gui("Jay Compressor", "600x240")
        app.setGuiPadding(20, 10)
        app.setPadding([0,8])


        def press(btnName):
            global BMP_PATH, K, L, A_OR_B
            if btnName == "Quit":
                app.stop()
            elif btnName == "Submit":
                BMP_PATH = app.getEntry("entryImagePath")
                A_OR_B = app.getRadioButton("radioBtnType")
                try:
                    K = int(app.getEntry("entry_k"))
                except ValueError:
                    K = -1
                    pass

                try:
                    L = int(app.getEntry("entry_l"))
                except ValueError:
                    L = -1
                    pass

                if BMP_PATH is "":
                    app.errorBox("Missing image", "Select a valid image before submitting")
                elif False: # Se l'immagine non è valida per formato, path o che altro# Se l'immagine non è valida per formato, path o che altro
                    app.errorBox("Wrong image path", "Select a valid BPM image")
                elif K < 0:
                    app.errorBox("Wrong K value", "Be sure to fill K field with an integer value")
                elif L < 0:
                    app.errorBox("Wrong L value", "Be sure to fill L field with an integer value")
                else:
                    pass
                    ############################################### SECONDA PARTE - COMPRESSIONE JPEG
                    storedImage = Image.open(BMP_PATH)
                    storedImage.show()

                    #Passo dal canale RGB al canale in scala di grigi
                    greyScale = storedImage.convert('L')
                    arraIm = numpy.array(greyScale)

                    #Estraggo le dimensioni dell'immagine
                    nrow = arraIm.shape[0]
                    ncol = arraIm.shape[1]

                    #Primo passo: applico la DCT all'intera immagine
                    imageVert = dct(dct(arraIm.T,norm='ortho').T, norm='ortho')

                    #Secondo passo: azzeramento delle frequenze scelte dall'utente
                    if A_OR_B=='A' or A_OR_B=='a':
                        print('a')
                        for kkm in range(0,nrow):
                            for kkn in range(0,ncol):
                                if kkm>=K and kkn>=L:
                                    imageVert[kkm][kkn]=0
                    elif A_OR_B=='B' or A_OR_B=='b':
                        print('b')
                        for kkm in range(0,nrow):
                            for kkn in range(0,ncol):
                                if kkm>=K or kkn>=L:
                                    imageVert[kkm][kkn]=0

                    #Terzo step, applicazione della IDCT
                    invertedVer = idct(idct(imageVert.T, norm='ortho').T, norm='ortho')

                    #Quarto step, arrotondamento e sistemazione dei valori dei pixel
                    for kkm in range(0,nrow):
                        for kkn in range(0,ncol):
                            
                            #Arrotondo tutti i valori all'intero più vicino
                            invertedVer[kkm][kkn]=round(invertedVer[kkm][kkn])

                            #I valori negativi o superiori a 255 vengono aggiustati (per avere un intervallo [0,255])
                            if invertedVer[kkm][kkn]<=0:
                                invertedVer[kkm][kkn]=0
                            if invertedVer[kkm][kkn]>=255:
                                invertedVer[kkm][kkn]=255

                    #Stampa nuovo risultato e salva immagine output
                    rgbArray = numpy.zeros((nrow,ncol,3), 'uint8')
                    rgbArray[..., 0] = invertedVer
                    rgbArray[..., 1] = invertedVer
                    rgbArray[..., 2] = invertedVer
                    img = Image.fromarray(rgbArray)
                    img.show()
                    img.save(os.path.join(os.getcwd(),'compressedImg.jpg'), 'JPEG')                    
            else:
                # impossibile entrare in questo branch
                pass

        def selectImage(self):
            file = filedialog.askopenfile(mode='rb',title='Choose a file')
            if file is not None:
                global BMP_PATH
                BMP_PATH = file.name
                app.setEntry("entryImagePath", BMP_PATH, callFunction=False)
                file.close()
            return

        app.addLabel("labelSelectImage", "Select BMP file:", 0, 0, 4)
        app.addEntry("entryImagePath", 1, 0, 3)
        app.addButton("...", selectImage, 1, 3)

        app.addLabel("labelType", "Type:", 2, 0)
        app.addRadioButton("radioBtnType", "A", 2, 1)
        app.addRadioButton("radioBtnType", "B", 2, 2)

        app.addLabel("label_k", "k:", 3, 0)
        app.addEntry("entry_k", 3, 1)
        app.setEntryWidth("entry_k", 2)
        app.setEntry("entry_k", "0", callFunction = False)
        app.addLabel("label_l", "l:", 3, 2)
        app.addEntry("entry_l", 3, 3)
        app.setEntryWidth("entry_l", 2)
        app.setEntry("entry_l", "0", callFunction = False)

        app.addButtons( ["Submit", "Quit"], press, colspan=4)

        # add some enhancements
        app.setLabelAlign("labelSelectImage", "left")
        app.setLabelAlign("labelType", "right")
        app.setLabelAlign("label_k", "right")
        app.setLabelAlign("label_l", "right")
        app.setFocus("entryImagePath")

        # start the GUI
        app.go()



############################## CONTROLLO DELLA DCT
#INPUT: 'v' o 'V' per controllare il vettore, 'm' o 'M' per controllare la matrice
#OUTPUT: un vettore o una matrice con valori nello spazio delle frequenze
def checkMyDCT(*args):
    #Controllo  del vettore
    if args[0]=='v' or args[0]=='V':
        y = [231, 32, 233, 161, 24, 71, 140, 245]
        libSingleDCT = dct(y, norm='ortho')
        mySingleDCT = myDCT(y)
        print(libSingleDCT)
        print(mySingleDCT)
    else:
        #Controllo  della matrice
        if args[0]=='m' or args[0]=='M':
            y2 = numpy.matrix('231 32 233 161 24 71 140 245; 247 40 248 245 124 204 36 107; 234 202 245 167 9 217 239 173; 193 190 100 167 43 180 8 70; 11 24 210 177 81 243 8 112; 97 195 203 47 125 114 165 181; 193 70 174 167 41 30 127 245; 87 149 57 192 65 129 178 228')
            libDCT = dct(dct(y2.T, norm='ortho').T, norm='ortho')

            myHorizzy = numpy.zeros((8,8))
            myVerty = numpy.zeros((8,8))
            for jk in range(0,8):
                myHorizzy[jk]=dct(y2[jk], norm='ortho')
            myHorizzy = myHorizzy.transpose()
            for jk in range(0,8):
                myVerty[jk]=dct(myHorizzy[jk], norm='ortho')
            myVerty = myVerty.transpose()

            #Stampa del risultato ottenuto da homemade e fast DCT. Si devono confrontare entrambe con la DCT di MATLAB
            print(libDCT)
            print('\n\n')
            print(myVerty)
        else:
            print('Missing input parameters')



########################### PRIMA PARTE DEL PROGETTO - COMPARAZIONE DCT
#INPUT OPZIONALI: due interi a,b tali che a < b.
#INPUT STANDARD: range da 8 a 17
def compareDCTs(*args):
    minRang=8
    maxRang=17
    if len(args)==2:
        minRang=args[0]
        maxRang=args[1]

    #Array dei risultati
    timeLIB = []
    timeMINE = []
    sizes = []
    
    #Elaborazione delle matrici di dimensione da A a B
    for countTurns in range(minRang,maxRang):
        singleBlock = numpy.random.randint(255, size=(countTurns,countTurns))
        sizes.append(countTurns)

        print(countTurns)

        #Computazione della libreria
        tLIBs = time.time()
        dct(dct(singleBlock.T, norm='ortho').T, norm='ortho')
        tLIBe = time.time()
        elapsedLIB = tLIBe-tLIBs
        timeLIB.append(elapsedLIB)
        print('lib: ', elapsedLIB)

        #Computazione della DCT casalinga
        tMINEs = time.time()
        myHordct = numpy.zeros((countTurns,countTurns))
        myVerdct = numpy.zeros((countTurns,countTurns))
        for jk in range(0,countTurns):
            myHordct[jk]=myDCT(singleBlock[jk])
        myHordct = myHordct.transpose()
        for jk in range(0,countTurns):
            myVerdct[jk]=myDCT(myHordct[jk])
        myVerdct = myVerdct.transpose()
        tMINEe = time.time()
        elapsedMINE = tMINEe - tMINEs
        timeMINE.append(elapsedMINE)
        print('mat: ', elapsedMINE)

    #Plotto i grafici con legenda
    pylab.figure(1)
    pylab.title('Elapsed Time')
    pylab.xlabel('Matrix dimension')
    pylab.ylabel('Time (microsec)')
    pylab.plot(sizes, timeLIB, marker='.', alpha=1, color='b', label="Library DCT")
    pylab.plot(sizes, timeMINE, marker='.', alpha=1, color='r', label='Homemade DCT')
    pylab.legend(loc='upper right')
    pylab.show()



##################################################### Versione casalinga della DCT            
def myDCT(y):
    N = len(y)
    c = []
    for u in range(0,N):
        summation = 0
        if u==0:
            a=numpy.sqrt(1/N)
        else:
            a=numpy.sqrt(2/N)

        for i in range(0,N):
            summation = summation + y[i]*math.cos(u*math.pi*((2*i+1)/(2*N)))

        c.append(a*summation)
    return c



###################################################### Versione casalinga della DCT inversa
def myIDCT(y):
    N = len(y)
    c = []
    for i in range(0,N):
        summation = 0

        for u in range(0,N):
            if u==0:
                a=numpy.sqrt(1/N)
            else:
                a=numpy.sqrt(2/N)
            summation = summation + a*y[u]*math.cos(u*math.pi*((2*i+1)/(2*N)))

        c.append(summation)
    return c



###################################################### Modulo principale che richiama l'interfaccia grafica    
if __name__ == '__main__':
    #main(argv)
    NewGui()