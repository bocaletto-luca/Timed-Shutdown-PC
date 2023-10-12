# Importa il modulo tkinter per creare l'interfaccia utente grafica
import tkinter as tk
from tkinter import ttk
import os
import time
import threading
from tkinter import messagebox

# Definisci la classe principale dell'applicazione
class AppOrario:
    def __init__(self, root):
        self.root = root
        self.root.title("Spegnimento Programmato del PC")  # Imposta il titolo dell'applicazione

        # Crea una label per visualizzare l'orario corrente
        self.etichetta_orario = tk.Label(root, text="", font=("Helvetica", 48))
        self.etichetta_orario.pack()

        # Avvia l'aggiornamento dell'orario
        self.avvia_orologio()

        # Crea l'interfaccia per la pianificazione delle azioni
        self.crea_interfaccia_pianificazione()

    def avvia_orologio(self):
        # Funzione per aggiornare l'orario in tempo reale
        def aggiorna_orologio():
            while True:
                orario_corrente = time.strftime("%H:%M:%S")
                self.etichetta_orario.config(text=orario_corrente)
                time.sleep(1)

        # Crea un thread per l'orologio che viene eseguito in background
        thread_orologio = threading.Thread(target=aggiorna_orologio)
        thread_orologio.daemon = True  # Il thread terminerà quando l'app verrà chiusa
        thread_orologio.start()

    def crea_interfaccia_pianificazione(self):
        # Crea un frame per l'interfaccia di pianificazione
        frame_pianificazione = ttk.LabelFrame(self.root, text="Pianificazione")
        frame_pianificazione.pack(padx=20, pady=20)

        # Etichetta per inserire l'orario
        etichetta_orario = ttk.Label(frame_pianificazione, text="Orario (HH:MM):")
        etichetta_orario.grid(row=0, column=0, padx=10, pady=10)

        # Casella di testo per inserire l'orario
        self.casella_orario = ttk.Entry(frame_pianificazione)
        self.casella_orario.grid(row=0, column=1, padx=10, pady=10)

        # Variabile per memorizzare l'azione selezionata
        self.variabile_azione = tk.StringVar()
        self.variabile_azione.set("Spegnimento")  # Imposta l'azione predefinita su "Spegnimento"

        # Pulsanti per diverse azioni
        pulsante_spegnimento = ttk.Button(frame_pianificazione, text="Spegnimento", command=self.azione_spegnimento)
        pulsante_spegnimento.grid(row=1, column=0, padx=10, pady=10)

        pulsante_riavvio = ttk.Button(frame_pianificazione, text="Riavvio", command=self.azione_riavvio)
        pulsante_riavvio.grid(row=1, column=1, padx=10, pady=10)

        pulsante_sospensione = ttk.Button(frame_pianificazione, text="Sospensione", command=self.azione_sospensione)
        pulsante_sospensione.grid(row=2, column=0, padx=10, pady=10)

        pulsante_pianifica = ttk.Button(frame_pianificazione, text="Pianifica", command=self.pianifica_azione)
        pulsante_pianifica.grid(row=2, column=1, padx=10, pady=10)

    def pianifica_azione(self):
        # Funzione per pianificare un'azione
        orario_pianificato = self.casella_orario.get()

        if not orario_pianificato:
            # Se l'orario non è stato inserito, mostra un messaggio di errore
            messagebox.showerror("Errore", "Inserisci un orario valido prima di pianificare un'azione.")
            return

        try:
            hh, mm = map(int, orario_pianificato.split(':'))
            orario_attuale = time.localtime()
            orario_pianificato = time.mktime((orario_attuale.tm_year, orario_attuale.tm_mon, orario_attuale.tm_mday, hh, mm, 0, -1, -1, -1))
            orario_corrente = time.mktime(time.localtime())
            ritardo = orario_pianificato - orario_corrente

            if ritardo <= 0:
                # Se l'orario è nel passato, mostra un messaggio di errore
                messagebox.showerror("Errore", "Inserisci un orario futuro valido.")
            else:
                # Attendi il ritardo e quindi esegui l'azione pianificata
                self.root.after(int(ritardo * 1000), self.esegui_azione)
        except ValueError:
            # Se l'orario ha un formato non valido, mostra un messaggio di errore
            messagebox.showerror("Errore", "Formato orario non valido (HH:MM).")

    def esegui_azione(self):
        # Funzione per eseguire l'azione pianificata
        azione_selezionata = self.variabile_azione.get()
        if azione_selezionata == "Spegnimento":
            os.system("shutdown /s /f /t 0")  # Spegni il sistema
        elif azione_selezionata == "Riavvio":
            os.system("shutdown /r /f /t 0")  # Riavvia il sistema
        elif azione_selezionata == "Sospensione":
            os.system("shutdown /h /f")  # Sospendi il sistema

    def azione_spegnimento(self):
        self.variabile_azione.set("Spegnimento")

    def azione_riavvio(self):
        self.variabile_azione.set("Riavvio")

    def azione_sospensione(self):
        self.variabile_azione.set("Sospensione")

if __name__ == "__main__":
    # Crea la finestra principale dell'applicazione
    root = tk.Tk()
    app = AppOrario(root)
    root.mainloop()  # Avvia l'interfaccia utente principale
