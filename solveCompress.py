from tkinter import Tk, Frame, BOTH, filedialog
from PIL import Image
import numpy
from tkinter.ttk import Button
from scipy.fftpack.realtransforms import dct
from scipy.fftpack.realtransforms import idct
import math
import pylab
from datetime import datetime
from sys import argv
from appJar import gui
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
        if file != None:
            global C
            C = file.name      
            file.close()  

class NewGui:
    def __init__(self):
        # create the GUI & set a title
        app = gui("Jay Compressor", "500x380")

        def press(btnName):
            if btnName == "Cancel":
                app.stop()
                return

            if app.getEntry("userEnt") == "rjarvis":
                if app.getEntry("passEnt") == "abc":
                    app.infoBox("Success", "Congratulations, you are logged in!")
                else:
                    app.errorBox("Failed login", "Invalid password")
            else:
                app.errorBox("Failed login", "Invalid username")

        def selectImage():
            return

        # add labels & entries
        # in the correct row & column
        app.addLabel("labelSelectImage", "Select BMP file:", 0, 0)
        app.addEntry("entryImagePath", 1, 1)
        app.addButton("...", selectImage, 1, 2)
        app.addLabel("passLab", "Password:", 1, 0)
        app.addSecretEntry("passEnt", 1, 1)

        # changed this line to call a function
        app.addButtons( ["Submit", "Cancel"], press, colspan=2)

        # add some enhancements
        app.setFocus("entryImagePath")
        app.enableEnter(press)

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
            
            print(libDCT)
            print('\n\n')
            print(myVerty)
        else:
            print('Missing input parameters')



########################### PRIMA PARTE DEL PROGETTO - COMPARAZIONE DCT
#INPUT OPZIONALI: due interi a,b tali che a < b.
#INPUT STANDARD: range da 8 a 17
def primaParte(*args):  
    minRang=8
    maxRang=17
    if len(args)==2 and args[0]<args[1] :
        minRang=args[0]
        maxRang=args[1]
    else:
        print('I valori inseriti non sono coerenti. La procedura richiede che A < B')
    
    #Array dei risultati
    timeLIB = []
    timeMINE = []
    sizes = []  
    
    #Elaborazione delle matrici di dimensione da A a B
    for countTurns in range(minRang,maxRang):
        singleBlock = numpy.random.randint(255, size=(countTurns,countTurns))   
        sizes.append(countTurns)  
        
        #Computazione della libreria
        tLIBs = datetime.now()
        dct(dct(singleBlock.T, norm='ortho').T, norm='ortho')
        tLIBe = datetime.now()
        elapsedLIB = tLIBe-tLIBs
        timeLIB.append(elapsedLIB.microseconds)
        print('lib: ', elapsedLIB.microseconds)
                
        #Computazione della DCT casalinga        
        tMINEs = datetime.now()
        myHordct = numpy.zeros((countTurns,countTurns))
        myVerdct = numpy.zeros((countTurns,countTurns))
        for jk in range(0,countTurns):
            myHordct[jk]=myDCT(singleBlock[jk])
        myHordct = myHordct.transpose()    
        for jk in range(0,countTurns):
            myVerdct[jk]=myDCT(myHordct[jk])
        myVerdct = myVerdct.transpose()
        tMINEe = datetime.now()
        elapsedMINE = tMINEe - tMINEs
        timeMINE.append(elapsedMINE.microseconds)     
        print('mat: ',elapsedMINE.microseconds)        
        
    #Plotto i grafici con legenda
    pylab.figure(1)
    pylab.title('Elapsed Time')
    pylab.xlabel('Matrix dimension')
    pylab.ylabel('Time (microsec)')
    pylab.plot(sizes, timeLIB, marker='.', alpha=1, color='b', label="Library DCT")       
    pylab.plot(sizes, timeMINE, marker='.', alpha=1, color='r', label='Homemade DCT')
    pylab.legend(loc='upper right')
    pylab.show()
    
    
    
############################################### SECONDA PARTE - COMPRESSIONE JPEG
def main(*args):
    #Avvio dell'interfaccia per selezionare l'immagine
    root = Tk()
    root.geometry("750x200+300+300")
    Example(root)
    root.mainloop() 
    
    #Salvataggio del path dell'immagine C, caricamento immagine e stampa
    storedImage = Image.open(C)
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
    param1=args[0]
    param2=args[1]
    mode=args[2]
    if mode=='A' or mode=='a':
        print('a')
        for kkm in range(0,nrow):
            for kkn in range(0,ncol):
                if(kkm>=param1 and kkn>=param2):
                    imageVert[kkm][kkn]=0
    elif mode=='B' or mode=='b':
        print('b')
        for kkm in range(0,nrow):
            for kkn in range(0,ncol):
                if(kkm>=param1 or kkn>=param2):
                    imageVert[kkm][kkn]=0
                    
        #Terzo step       
        invertedVer = idct(idct(imageVert.T, norm='ortho').T, norm='ortho')
    
        #Quarto step
        for kkm in range(0,nrow):
            for kkn in range(0,ncol):  
            
            #Arrotondo tutti i valori all'intero pi� vicino
                invertedVer[kkm][kkn]=round(invertedVer[kkm][kkn])
             
                #I valori negativi o superiori a 255 vengono aggiustati  
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
    else:
        print("Wrong input parameters")        

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
    
        c.append(a*summation);
    return c


#Versione casalinga della DCT inversa
def myIDCT(y):
    N = len(y)
    c = []    
    for i in range(0,N):    
        summation = 0
        
        for u in range(0,N):
            if(u==0):
                a=numpy.sqrt(1/N)
            else:
                a=numpy.sqrt(2/N)
            summation = summation + a*y[u]*math.cos(u*math.pi*((2*i+1)/(2*N)))
    
        c.append(summation);
    return c

#Modulo principale    
if __name__ == '__main__':
    main(argv)