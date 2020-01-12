#!/usr/bin/python3

import requests
import simplejson as json

#nDames
class NDames:
    """Generate all valid solutions for the n queens puzzle"""
    def __init__(self, size):
        # Store the puzzle (problem) size and the number of valid solutions
        self.size = size
        self.solutions = 0
        self.solve()
        return(self.solutions)

    def solve(self):
        """Solve the n queens puzzle and print the number of solutions"""
        positions = [-1] * self.size
        self.put_queen(positions, 0)

    def put_queen(self, positions, target_row):
        """
        Try to place a queen on target_row by checking all N possible cases.
        If a valid place is found the function calls itself trying to place a queen
        on the next row until all N queens are placed on the NxN board.
        """
        # Base (stop) case - all N rows are occupied
        if target_row == self.size:
            self.solutions += 1
        else:
            # For all N columns positions try to place a queen
            for column in range(self.size):
                # Reject all invalid positions
                if self.check_place(positions, target_row, column):
                    positions[target_row] = column
                    self.put_queen(positions, target_row + 1)

    def check_place(self, positions, ocuppied_rows, column):
        """
        Check if a given position is under attack from any of
        the previously placed queens (check column and diagonal positions)
        """
        for i in range(ocuppied_rows):
            if positions[i] == column or \
                positions[i] - i == column - ocuppied_rows or \
                positions[i] + i == column + ocuppied_rows:

                return False
        return True


#fonctions Files de messages

def demandeCreationFile(url, nomFile):
    #x = {}
    #x["nomFile"] = nomFile
    #myParam={"donnees" : json.dumps(x)}
    myParam = {"nomFile":nomFile}
    r = requests.post("http://{}/rabbit".format(url), data=myParam)
    donnees = json.loads(r.text)
    print("File {} créée".format(donnees["nomFile"]))

def demandeDepotMessageDansFile(url, nomFile, message):
    myParam={"message":message}
    r = requests.post("http://{}/rabbit/{}".format(url, nomFile),data=myParam)
    donnees = json.loads(r.text)
    print("Message déposé : {} ".format(donnees["message"]))

def lectureMessageDansFile(url, nomFile):
    myParam={"nomFile":nomFile}
    r = requests.get("http://{}/rabbit/{}".format(url, nomFile),params=myParam)
    donnees = json.loads(r.text)
    #print("Message lu : {} ".format(donnees["message"]))
    return (format(donnees["message"]))


    client = docker.from_env()
    conteneur = client.containers.get(nom)
    conteneur.stop()

if __name__ == '__main__':
    
    #l'ip du message initial devra peut être, être remplacée
    #manuellement
    message = lectureMessageDansFile("172.17.0.1:5000", "ToDo")
    
    while(message != "Vide"):
        #un replace a été mis en place car une erreur était générée par
        #le json.loads -> le json lu contenait des quotes à la place
        #des doubles quotes
        tache = json.loads(message.replace("\'","\""))
        #numProjet = tache["id_projet"]
        #numTache = tache["id_tache"]
        ip = tache["dataOut"][0]["ip"]
        #demandeDepotMessageDansFile(ip, "Done", "idProjet : {} idTache : {} ip : {}".format(numProjet, numTache, ip))
        solution = NDames(5)
        demandeDepotMessageDansFile(ip, "Done", "nbSolutions : {}".format(solution))
        message = lectureMessageDansFile(ip, "ToDo")
