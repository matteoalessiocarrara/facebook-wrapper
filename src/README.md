Promemoria per il programmatore:

 * Riporta bot-virtualbrowser sul branch master, eventualmente prima includi 
   le modifiche che hai fatto durante lo sviluppo di questa libreria
   
 * Se hai aggiornato qualcosa in lib/
  * Assicurati di aggiornare anche il codice della libreria, in modo che richieda
    la nuova versione e non la vecchia
    
 * Se hai modificato test.py, aggiorna il readme
    
 * Se hai modificato la libreria:
  * Controlla che non ci siano bug evidenti, esegui test.py
  * Aggiorna il changelog
  * Aggiorna la versione in version.py
  * Esegui pydoc-update.sh (modificalo se hai aggiunto dei file)
 
