import tkinter as tk
from tkinter import messagebox
import random
import math

# Fonction pour l'exponentiation rapide
def expo_rapide(g, x, n):
    result = 1
    g = g % n
    while x > 0:
        if x % 2 == 1:
            result = (result * g) % n
        g = (g * g) % n
        x = x // 2
    return result

# Fonction pour le test de primalité probabiliste
def est_premier(p):
    for a in [2, 3, 5, 7]:
        if expo_rapide(a, p - 1, p) != 1:
            return False
    return True

# Fonction pour générer un nombre premier
def generer_premier(n):
    while True:
        p = random.randint(2, n)
        if est_premier(p):
            return p

# Fonction pour calculer le PGCD
def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Fonction pour trouver l'inverse modulaire
def euclide_etendu(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, x, y = euclide_etendu(b, a % b)
        return g, y, x - (a // b) * y

def inverse_modulaire(e, phi):
    g, x, _ = euclide_etendu(e, phi)
    if g != 1:
        return None  # Pas d'inverse si PGCD(e, phi) ≠ 1
    else:
        return x % phi  # L'inverse modulaire est toujours positif


# Fonction pour générer les clés RSA
def generer_cles():
    p = generer_premier(100)
    q = generer_premier(100)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randint(2, phi - 1)
    while pgcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    d = inverse_modulaire(e, phi)
    return (e, n), (d, n)

# Fonction pour signer un message
def signer_message(M, d, n):
    return expo_rapide(M, d, n)

# Fonction pour vérifier la signature
def verifier_signature(S, e, n, M):
    return expo_rapide(S, e, n) == M

# Interface graphique
class RSAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Signature RSA")

        self.label_message = tk.Label(root, text="Message (entier):")
        self.label_message.pack()

        self.entry_message = tk.Entry(root)
        self.entry_message.pack()

        self.button_generer_cles = tk.Button(root, text="Générer les clés", command=self.generer_cles)
        self.button_generer_cles.pack()

        self.label_cle_publique = tk.Label(root, text="Clé publique (e, n):")
        self.label_cle_publique.pack()

        self.label_cle_privee = tk.Label(root, text="Clé privée (d, n):")
        self.label_cle_privee.pack()

        self.button_signer = tk.Button(root, text="Signer le message", command=self.signer)
        self.button_signer.pack()

        self.label_signature = tk.Label(root, text="Signature:")
        self.label_signature.pack()

        self.button_verifier = tk.Button(root, text="Vérifier la signature", command=self.verifier)
        self.button_verifier.pack()

        self.label_resultat = tk.Label(root, text="Résultat de la vérification:")
        self.label_resultat.pack()

    def generer_cles(self):
        self.cle_publique, self.cle_privee = generer_cles()
        self.label_cle_publique.config(text=f"Clé publique (e, n): {self.cle_publique}")
        self.label_cle_privee.config(text=f"Clé privée (d, n): {self.cle_privee}")

    def signer(self):
        M = int(self.entry_message.get())
        d, n = self.cle_privee
        S = signer_message(M, d, n)
        self.label_signature.config(text=f"Signature: {S}")

    def verifier(self):
        M = int(self.entry_message.get())
        e, n = self.cle_publique
        S = int(self.label_signature.cget("text").split(": ")[1])
        if verifier_signature(S, e, n, M):
            self.label_resultat.config(text="Résultat de la vérification: Signature valide")
        else:
            self.label_resultat.config(text="Résultat de la vérification: Signature invalide")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300")
    app = RSAApp(root)
    root.mainloop()