#!/usr/bin/python3

import requests
import simplejson as json


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
        numProjet = tache["id_projet"]
        numTache = tache["id_tache"]
        ip = tache["dataOut"][0]["ip"]
        demandeDepotMessageDansFile(ip, "Done", "idProjet : {} idTache : {} ip : {}".format(numProjet, numTache, ip))
        message = lectureMessageDansFile(ip, "ToDo")