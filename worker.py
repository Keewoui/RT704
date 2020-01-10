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
    
    #print("oui")
    #demandeCreationFile("172.17.0.1:5000", "fileConteneur")
    #demandeDepotMessageDansFile("fileConteneur", "oui", "localhost:5000")
    #print("hello script lancé !!")
    message = lectureMessageDansFile("172.17.0.1:5000", "ToDo")
    while(message != "Vide"):
        #un replace a été mis en place car une erreur était générée par
        #le json.loads -> le json lu contenait des quotes à la place
        #des doubles quotes
        tache = json.loads(message.replace("\'","\""))
        test1 = tache["id_projet"]
        test = tache["id_tache"]
        demandeDepotMessageDansFile("172.17.0.1:5000", "Done", "idProjet : {} idTache".format(test1, test))
        message = lectureMessageDansFile("172.17.0.1:5000", "ToDo")
