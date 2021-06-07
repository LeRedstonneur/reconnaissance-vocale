#!/usr/bin/env python3

# Traitement du retour de VOSK
import json
# Accès aux fichiers
import os
# GUI
import tkinter as tk
# Manipulation d'audio
import wave
# Enregistrement de l'audio
import sounddevice as sd
# Traitement de l'audio de sounddevice
import numpy
# Parfois, il faut attendre
import time
# Ecrire l'audio dans un fichier WAV
import soundfile as sf
# Reconnaissance vocale
from vosk import Model, KaldiRecognizer
# Pour convertir une string en dictionnaire. Utilisé sur le partialResult de Vosk
import ast
assert numpy


class Application(tk.Tk):
    def __init__(self):
        self.enregistrement = None
        self.frames = None
        self.rate = None
        self.network = None
        self.compteur2 = None

        tk.Tk.__init__(self)

        self.grid()
        # Création du label
        self.label = tk.Label(self, text="")
        self.label.grid(row=2, column=1, padx=3, pady=8)

        # Création du champ de saisie pour l'opération
        self.entryVariable = tk.StringVar()
        self.Entry = tk.Entry(self, textvariable=self.entryVariable,
                              bg='white', width="20",
                              highlightbackground="blue", font=("Helvetica", 14),
                              highlightcolor="green")
        self.Entry.grid(row=2, column=1, padx=3, pady=8)
        self.Entry.focus_set()

        # Bouton modèle
        self.bouton2 = tk.Button(self, text='Configurer le modèle', width='30', bg='red', command=self.model)
        self.bouton2.grid(row=2, column=2, padx=5, pady=20)

        # Deuxième input
        self.entryVariable2 = tk.StringVar()
        self.Entry2 = tk.Entry(self, textvariable=self.entryVariable2,
                               bg='white', width="20",
                               highlightbackground="blue", font=("Helvetica", 14),
                               highlightcolor="green")
        self.Entry2.grid(row=3, column=1, padx=3, pady=8)

        # Création d'un label qui affiche le résultat
        self.labelVariable = tk.StringVar()
        self.label = tk.Label(self, textvariable=self.labelVariable,
                              font=("Helvetica", 20))
        self.label.grid(row=4, column=1, columnspan=2, padx=3, pady=10)

        # #----- Création des boutons -----##
        self.bouton = tk.Button(self, text='Reconnaître', width='30', bg='red', command=self.recognize)
        self.bouton.grid(row=3, column=2, padx=5, pady=20)

        self.record = tk.Button(self, text="Démarrer l'enregistrement", width='30', bg='green', command=self.record)
        self.record.grid(row=2, column=3, padx=5, pady=20)

    def recognize(self):
        """On applique le réseau neuronal sur un audio fourni"""
        if self.network is None:
            self.labelVariable.set("Un modèle est requis pour analyser un audio.")
            return None
        self.labelVariable.set("Reconnaissance vocale en cours. Veuillez patienter...")
        self.labelVariable.set(Reconnaissance(self.network, self.entryVariable2.get()))

    def model(self):
        """Cette fonction configure un modèle pour le réseau neuronal de reconnaissance vocale"""
        if not os.path.exists(self.entryVariable.get()):
            self.labelVariable.set("Modèle non trouvé.")
            return None
        self.bouton2.configure(text=f"Modèle en configuration")
        self.update_idletasks()
        self.network = Neural(self.entryVariable.get())
        self.labelVariable.set(f"Modèle configuré : {self.entryVariable.get()}")

    def record(self):
        """Cette fonction enregistre un vocal dans un fichier WAV pour permettre ensuite son analyse"""
        self.frames = 240000
        self.rate = 48000
        self.enregistrement = sd.rec(self.frames, samplerate=self.rate, channels=1)
        print("Enregistrement !")
        for i in range(int(self.frames / self.rate)):
            self.labelVariable.set(f"Il reste {int(self.frames / self.rate - i)}s")
            self.update_idletasks()
            time.sleep(1)
        sd.wait()
        print("Enregistrement terminé")
        sd.play(self.enregistrement, 48000)
        sd.wait()
        print("Son joué")
        self.record.configure(text="Enregistrement terminé", command=self.record)
        self.compteur2 = 0
        sf.write('new_file.wav', self.enregistrement, 48000)


class Neural:
    """Une classe qui continent un modèle de reconnaissance vocale."""

    def __init__(self, nom_du_modele: str):
        """On initialise les variables utilisées par la fonction."""
        self.model_name = nom_du_modele
        if not os.path.exists(self.model_name):
            print(
                "Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the "
                "current folder.")
            exit(1)
        self.model = Model(self.model_name)


class Reconnaissance:
    """Cette classe prend en argument un objet Neural ainsi que l'adresse d'un audio."""
    def __init__(self, model2: 'Neural', source2: str):
        """On initialise les variables."""
        self.source = source2
        self.modele = model2
        self.wf = wave.open(self.source, "rb")
        if self.wf.getnchannels() != 1 or self.wf.getsampwidth() != 2 or self.wf.getcomptype() != "NONE":
            print("Audio file must be WAV format mono PCM.")
            exit(1)
        self.rec = KaldiRecognizer(model2.model, self.wf.getframerate())
        self.compteur = 0
        while True:
            self.compteur += 1
            self.data = self.wf.readframes(4000)
            if len(self.data) == 0:
                break
            if self.rec.AcceptWaveform(self.data):
                self.rec.Result()
                # print(rec.Result())
            else:
                self.test = self.rec.PartialResult()
                app.labelVariable.set(ast.literal_eval(self.test)["partial"])
                # print(self.rec.PartialResult())
                app.update()
        self.a = json.loads(str(self.rec.FinalResult()))
        # for i in self.a["result"]:
        #     print(f"{i['word']}    {i['start']}-{i['end']}    Conf : {i['conf']}")

    def __str__(self):
        """"Pour afficher le modèle utilisé par l'objet. En réalité peu utile."""
        return self.a["text"]


if __name__ == "__main__":
    app = Application()
    app.title("Test reconnaissance vocale")
    app.geometry("720x480")
    # #----- Programme principal -----##
    app.mainloop()  # Boucle d'attente des événements
