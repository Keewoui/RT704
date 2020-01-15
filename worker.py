#!/usr/bin/python3

import time
import requests
import simplejson as json

#nDames
class NDames:
    #generation des valeurs possibles pour les n dames
    def __init__(self, size):
        #la taille du plateau ainsi que
        #le nombre de solutions valides
        #sont stockés
        self.size = size
        self.solutions = 0
        self.solve()

    def solve(self):
        #résolution du problème des n dames
        positions = [-1] * self.size
        self.put_queen(positions, 0)

    def put_queen(self, positions, target_row):

        if target_row == self.size:
            self.solutions += 1
        else:
            #pour toutes les n colonnes on essaie de placer une dames
            for column in range(self.size):
                # Reject all invalid positions
                if self.check_place(positions, target_row, column):
                    positions[target_row] = column
                    self.put_queen(positions, target_row + 1)

    def check_place(self, positions, ocuppied_rows, column):
        #on vérifie si on peut placer une dame sur la position donnée
        #en regardant notamment les colonnes ainsi que les diagonales
        for i in range(ocuppied_rows):
            if positions[i] == column or \
                positions[i] - i == column - ocuppied_rows or \
                positions[i] + i == column + ocuppied_rows:

                return False
        return True


#fonctions Files de messages

def demandeDepotMessageDansFile(ip, nomFile, message):
    myParam={"message":message}
    r = requests.post("http://{}/rabbit/{}".format(ip, nomFile),data=myParam)
    donnees = json.loads(r.text)

def lectureMessageDansFile(ip, nomFile):
    myParam={"nomFile":nomFile}
    r = requests.get("http://{}/rabbit/{}".format(ip, nomFile),params=myParam)
    donnees = json.loads(r.text)
    return (format(donnees["message"]))

if __name__ == '__main__':
    
    
    while(1):
        #l'ip du message initial devra être remplacée
        #manuellement
        message = lectureMessageDansFile("172.17.0.1:5000", "ToDo")
        
        if (message != "Vide"):
            #un replace a été mis en place car une erreur était générée par
            #le json.loads -> le json lu contenait des quotes à la place
            #des doubles quotes
            tache = json.loads(message.replace("\'","\""))
            #on récupère l'ID du projet
            numProjet = tache["id_projet"]
            #on récupère l'IP pour renvoyer le résultat
            ip = tache["dataOut"][0]["ip"]
            #on récupère le nombre de dames à calculer
            numDamesACalculer = tache["nbDames"]
            #on calcule le nombre de solutions en fonction
            #du nombre de dames
            nbSolutions = NDames(numDamesACalculer).solutions
            #envoi de la solution dans la file Done 
            solution = json.dumps({"id_projet" : numProjet, "nbDames" : numDamesACalculer, "nbSolutions" : nbSolutions})
            demandeDepotMessageDansFile(ip, "Done", solution)
        time.sleep(5)
