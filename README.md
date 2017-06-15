# PROGETTO2

## Obiettivo
Compressione di un'immagine BMP in JPEG e valutazione dei tempistiche della libreria DCT.

## Linguaggi utilizzati
Python.


## CHECKMYDCT
Lo script `solveCompress.checkMyDCT()` verifica che la homemade DCT e la Fast DCT utilizzano lo scaling JPEG visto a lezione.

La funzione richiede in input un carattere:
* `v` o `V` : verifica del vettore proposto sulla traccia;
* `m` o `M` : verifica della matrice proposta sulla traccia.


## COMPAREDCT
Lo script `solveCompress.compareDCTs()` permette di valutare le tempistiche della DCT homemade e fast.

Chiamare la funzione `solveCompress.compareDCTs()` con i seguenti input:
* **nessuno** : viene utilizzato un range di matrici NxN, con N da 8 a 16;
* **due numeri reali A e B, tali che A<B** : viene utilizzato un range di matrici NxN, con N da A a B.


## NEWGUI
Chiamare la funzione "solveCompress.NewGui()" per avviare l'interfaccia ed eseguire la compressione JPEG con immagine e parametri scelti dall'utente.