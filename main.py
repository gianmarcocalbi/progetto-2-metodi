"""
Created on 13 mag 2017

@author: Nico
"""

import math
import time
from sys import argv
from tkinter import Tk, Frame, BOTH, filedialog
from tkinter.ttk import Button

import numpy
import pylab
from PIL import Image
# from tkinter.filedialog import FileDialog, askopenfile
from scipy.fftpack.realtransforms import dct
from scipy.fftpack.realtransforms import idct

global C


class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.initUI()


    def initUI(self):

        self.parent.title("DCT2 algorithm")
        self.pack(fill=BOTH, expand=1)

        chooseButton = Button(self, text="Select image..",command=self.askopenfile)
        chooseButton.place(x=100, y=150)

        quitButton = Button(self, text="Exit",command=self.quit)
        quitButton.place(x=600, y=150)


    def askopenfile(self):
        file = filedialog.askopenfile(mode='rb',title='Choose a file')
        if file is not None:
            global C
            C = file.name
            file.close()


        #Function to check DCT
def checkMyDCT(*args):
    #Check dct on row
    if args[0]=='v':
        y = [231, 32, 233, 161, 24, 71, 140, 245]
        libSingleDCT = dct(y, norm='ortho')
        mySingleDCT = myDCT(y)
        print(libSingleDCT)
        print(mySingleDCT)

    #check dct on 8x8 block
    if args[0]=='m':
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

        print(libDCT)
        print('\n\n')
        print(myVerty)


###########################First part of the project
def primaParte(*args):
    #Range da 8 a 17, se ci sono i parametri viene aggiornato
    numpy.random.seed()
    minRang=8
    maxRang=17
    if len(args)==2:
        minRang=args[0]
        maxRang=args[1]

    #Array vuoti dei risultati
    timeLIB = []
    timeMINE = []
    sizes = []

    '''
    for countTurns in range(minRang,maxRang):
        singleBlock = numpy.random.randint(255, size=(countTurns,countTurns))
        sizes.append(countTurns)

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
        print(elapsedMINE)
    '''

    for countTurns in range(minRang,maxRang):
        numpy.random.seed()
        tLIBs = time.time()
        singleBlock = numpy.random.randint(255, size=(countTurns, countTurns))
        sizes.append(countTurns)
        #Computazione della libreria
        dct(dct(singleBlock.T, norm='ortho').T, norm='ortho')
        tLIBe = time.time()
        elapsedLIB = tLIBe-tLIBs
        timeLIB.append(elapsedLIB)
        print(elapsedLIB)
        time.sleep(0.2)




    #Plotto i grafici con legenda
    pylab.figure(1)
    pylab.title('Elapsed Time')
    pylab.xlabel('Matrix dimension')
    pylab.ylabel('Time (sec)')
    pylab.plot(sizes, timeLIB, marker='.', alpha=1, color='b', label="Library DCT")
    timeLIB.sort()
    pylab.plot(sizes, timeLIB, marker='.', alpha=1, color='r', label="Library DCT")
    #pylab.plot(sizes, timeMINE, marker='.', alpha=1, color='r', label='Homemade DCT')
    pylab.legend(loc='upper right')
    pylab.show()





###############################################Second part of the project
def main(*args):
    #Avvio dell'interfaccia
    root = Tk()
    root.geometry("750x200+300+300")
    Example(root)
    root.mainloop()

    #Salvataggio del path dell'immagine C, caricamento immagine e stampa
    storedImage = Image.open(C)

    #Passo dal canale RGB al canale in scala di grigi
    greyScale = storedImage.convert('L')
    arraIm = numpy.array(greyScale)

    #Estraggo le dimensioni dell'immagine
    nrow = arraIm.shape[0]
    ncol = arraIm.shape[1]

    #Primo passo: applico la DCT all'intera immagine
    imageOrizz = numpy.zeros((nrow,ncol))
    imageVert = numpy.zeros((ncol,nrow))
    for jk in range(0,nrow):
        imageOrizz[jk]=myDCT(arraIm[jk])
    imageOrizz = imageOrizz.transpose()
    for jk in range(0,ncol):
        imageVert[jk]=myDCT(imageOrizz[jk])
    imageVert = imageVert.transpose()
    #imageVert = dct(dct(arraIm.T,norm='ortho').T, norm='ortho')

    #Secondo pass: azzeramento delle frequenze scelte dall'utente
    param1=args[0]
    param2=args[1]
    mode=args[2]
    if mode=='A':
        for kkm in range(0,nrow):
            for kkn in range(0,ncol):
                if kkm>=param1 and kkn>=param2 :
                    imageVert[kkm][kkn]=0

    if mode=='B':
        for kkm in range(0,nrow):
            for kkn in range(0,ncol):
                if kkm>=param1 or kkn>=param2 :
                    imageVert[kkm][kkn]=0


    #Terzo step
    invertedVer = idct(idct(imageVert.T, norm='ortho').T, norm='ortho')
    '''invertedHor = numpy.zeros((nrow,ncol))
    invertedVer = numpy.zeros((ncol,nrow))
    for jk in range(0,nrow):
        invertedHor[jk]=myIDCT(imageVert[jk])
    invertedHor = invertedHor.transpose()
    for jk in range(0,ncol):
        invertedVer[jk]=myIDCT(invertedHor[jk])
    invertedVer = invertedVer.transpose() '''

    #Quarto step
    for kkm in range(0,nrow):
        for kkn in range(0,ncol):
            if(invertedVer[kkm][kkn]<=0):
                invertedVer[kkm][kkn]=0

            if(invertedVer[kkm][kkn]>=255):
                invertedVer[kkm][kkn]=255

    #Stampa nuovo risultato
    rgbArray = numpy.zeros((nrow,ncol,3), 'uint8')
    rgbArray[..., 0] = invertedVer
    rgbArray[..., 1] = invertedVer
    rgbArray[..., 2] = invertedVer
    img = Image.fromarray(rgbArray)
    img.show()
    img.save('out.jpg')


#Versione casalinga della DCT
def myDCT(y):
    N = len(y)
    c = []
    for u in range(0,N):
        summation = 0
        if(u==0):
            a=numpy.sqrt(1/N)
        else:
            a=numpy.sqrt(2/N)

        for i in range(0,N):
            summation = summation + y[i]*math.cos(u*math.pi*((2*i+1)/(2*N)))

        c.append(a*summation)
    return c


#Versione casalinga della DCT inversa
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


#Modulo principale
if __name__ == '__main__':
    main(argv)