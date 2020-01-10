#!/usr/bin/python3

from flask import request
import requests
import simplejson as json
import docker


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

#fonctions Docker
def executerConteneurSimple(nomConteneur):
    #un client doit être instantié pour communiquer avec un demon Docker
    client = docker.from_env()
    client.containers.run("rabbitmq", detach=True, name=nomConteneur)

#path est le chemin du répertoire qui contient le dockerFile
#tag est le nom que portera l'image résultante
def buildImageFromDockerFile(cheminDockerFile, tagImage):
    client = docker.from_env()
    client.images.build(path=cheminDockerFile, tag=tagImage)

#l'image est l'image créée à la suite de l'appel de la fonction du dessus
def construireConteneurFromDockerFile(nomConteneur, image):
    client = docker.from_env()
    client.containers.run(image, detach=True, name=nomConteneur)

def afficherConteneursEnCoursExecution():
    client = docker.from_env()
    for conteneur in client.containers.list():
        print(conteneur.attrs['Name'])

def demarrerConteneur(nom):
    client = docker.from_env()
    conteneur = client.containers.get(nom)
    conteneur.start()

def arreterConteneur(nom):
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
