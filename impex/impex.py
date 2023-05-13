import client.client
from client import client
import csv
from xml.dom import minidom
import time
import json


# Classe permettant d'instancier les utilisateurs qui seront envoyés vers le serveur avec un constructeur
# qui passe tous les attributs des utilisateurs dans utilisateurs.csv
class Utilisateur:

    def __init__(self, email, mdp, nom, prenom, type, adresse_no, adresse_rue, adresse_ville, adresse_prov,
                 adresse_pays, adresse_cp):
        self.__email = email
        self.__mdp = mdp
        self.__nom = nom
        self.__prenom = prenom
        self.__type = type
        self.__adresse_no = adresse_no
        self.__adresse_rue = adresse_rue
        self.__adresse_ville = adresse_ville
        self.__adresse_prov = adresse_prov
        self.__adresse_pays = adresse_pays
        self.__adresse_cp = adresse_cp

    # Méthode qui permet de convertir les utilisateurs venant du fichier utilisateurs.csv en format json
    def csv_to_json(self):
        return json.dumps({"utilisateur": {"email": self.__email, "mot_de_passe": self.__mdp, "nom": self.__nom,
                                           "prenom": self.__prenom, "type": self.__type,
                                           "adresse": {"no_civique": self.__adresse_no, "rue": self.__adresse_rue,
                                                       "ville": self.__adresse_ville, "province": self.__adresse_prov,
                                                       "pays": self.__adresse_pays, "code_postal": self.__adresse_cp}}})

    # Méthode qui permet de lire le fichier utilisateurs.csv, puis, pour chaque ligne sauf la première,
    # un objet Utilisateur est créé et est passé dans la méthode csv_to_json. Ensuite, tous ces objets se
    # retrouve dans une liste: liste_utilisateurs_json, qui comprend tous les utilisateurs en format json
    @staticmethod
    def lecture_utilisateurs_csv(fichier):
        liste_utilisateurs_json = []
        with open(fichier, 'r') as csv_utilisateurs:
            csv_reader = csv.reader(csv_utilisateurs)
            for utilisateur in csv_reader:
                if utilisateur[0] == 'email':
                    continue
                else:
                    objet = Utilisateur(utilisateur[0], utilisateur[1], utilisateur[2], utilisateur[3], utilisateur[4],
                                        utilisateur[5], utilisateur[6], utilisateur[7], utilisateur[8], utilisateur[9],
                                        utilisateur[10])
                    liste_utilisateurs_json.append(objet.csv_to_json())
        return liste_utilisateurs_json

    # Méthode qui permet de prendre un utilisateur en format json et de l'envoyer dans un nouveau fichier
    # portant le nom de la date. Le fichier est de type csv
    @staticmethod
    def export_csv(utilisateur_json):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open(f'./data/export_{timestamp}', 'w', newline='') as csv_file:
            champs = ['email', 'mdp', 'nom', 'prenom', 'type', 'adresse_no', 'adresse_rue', 'adresse_ville',
                      'adresse_prov', 'adresse_pays', 'adresse_cp']
            csv_dict_writer = csv.DictWriter(csv_file, fieldnames=champs)
            csv_dict_writer.writeheader()
            csv_dict_writer.writerow({'email': utilisateur_json['email'], 'mdp': utilisateur_json['mdp'],
                                 'nom': utilisateur_json['nom'], 'prenom': utilisateur_json['prenom'],
                                 'type': utilisateur_json['type'],'adresse_no': utilisateur_json['adresse_no'],
                                      'adresse_rue': utilisateur_json['adresse_rue'],
                                 'adresse_ville': utilisateur_json['adresse_ville'],
                                      'adresse_prov': utilisateur_json['adresse_prov'],
                                 'adresse_pays': utilisateur_json['adresse_pays'],
                                      'adresse_cp': utilisateur_json['adresse_cp']})


# Classe permettant d'instancier les chalets qui seront envoyés vers le serveur avec un constructeur
# qui passe tous les attributs des chalets dans chalets.csv
class Chalet:

    def __init__(self, id, nom, url_image, geo_lat, geo_long):
        self.__id = id
        self.__nom = nom
        self.__url_image = url_image
        self.__geo_lat = geo_lat
        self.__geo_long = geo_long

    # Méthode qui permet de convertir les chalets venant du fichier chalets.csv en format json
    def csv_en_json(self):
        return json.dumps({"chalet": {"id": self.__id, "nom": self.__nom, "url_image": self.__url_image,
                                      "geolocalisation": {"latitude": self.__geo_lat,
                                                           "longitude": self.__geo_long}}})

    # Méthode qui permet de lire le fichier chalets.csv, puis, pour chaque ligne sauf la première,
    # un objet Chalet est créé et est passé dans la méthode csv_en_json. Ensuite, tous ces objets se
    # retrouve dans une liste: liste_chalets_json, qui comprend tous les chalets en format json
    @staticmethod
    def lecture_chalets_csv(fichier):
        liste_chalets_json = []
        with open(fichier, 'r') as csv_chalets:
            csv_reader = csv.reader(csv_chalets)
            for chalet in csv_reader:
                if chalet[0] == 'id':
                    continue
                else:
                    objet = Chalet(chalet[0], chalet[1], chalet[2], chalet[3], chalet[4])
                    liste_chalets_json.append(objet.csv_en_json())
        return liste_chalets_json


# Classe permettant d'instancier les réservations qui seront envoyées vers le serveur avec un constructeur
# qui passe tous les attributs des réservations dans reservations.xml
class Reservation:

    def __init__(self, id, chalet, utilisateur, plage):
        self.__id = id
        self.__chalet = chalet
        self.__utilisateur = utilisateur
        self.__plage = plage

    # Méthode qui permet de convertir les réservations venant de reservations.xml en format json
    def xml_to_json(self):
        return json.dumps({"reservation": {"id": self.__id, "chalet": self.__chalet, "plages": self.__plage,
                                           "utilisateur": self.__utilisateur}})

    # Méthode qui permet de lire le fichier reservations.xml puis de séparer avec un minidom.
    # Elle crée ensuite une liste comportant chaque réservations grâce aux attributs définis dans le fichier
    @staticmethod
    def lecture_reservations_xml(fichier):
        with open(fichier, 'r') as xml_file:
            doc = minidom.parse(xml_file)

        liste_reservations_json = []
        elements = doc.getElementsByTagName('reservation')
        for element in elements:
            liste_plage = []
            id = element.getAttribute('id')
            chalet = element.getElementsByTagName('chalet')[0].firstChild.data
            utilisateur = element.getElementsByTagName('utilisateur')[0].firstChild.data
            plages = element.getElementsByTagName('plage')
            for plage in plages:
                p = plage.firstChild.data
                liste_plage.append(p)
            objet = Reservation(id, chalet, utilisateur, liste_plage)
            liste_reservations_json.append(objet.xml_to_json())
        return liste_reservations_json


# Classe permettant d'instancier les disponibilités qui seront envoyées vers le serveur avec un constructeur
# qui passe tous les attributs des disponibilités dans disponibilites.xml
class Disponibilite:

    def __init__(self, chalet, plage):
        self.__chalet = chalet
        self.__plage = plage

    # Méthode qui permet de convertir les disponibilités venant de disponibilites.xml en format json
    def xml_en_json(self):
        return json.dumps({'chalet': self.__chalet, 'plage': self.__plage})

    # Méthode qui permet de lire le fichier disponibilites.xml puis de séparer avec un minidom.
    # Elle crée ensuite une liste comportant chaque disponibilites grâce aux attributs définis dans le fichier
    @staticmethod
    def lecture_dispo_xml(fichier):
        with open(fichier, 'r') as xml_file:
            doc = minidom.parse(xml_file)

        liste_dispo_json = []
        elements = doc.getElementsByTagName('chalet')
        for element in elements:
            liste_plage = []
            chalet = element.getAttribute('id')
            plages = element.getElementsByTagName('plage')
            for plage in plages:
                p = plage.getAttribute('id')
                liste_plage.append(p)
            objet = Disponibilite(chalet, liste_plage)
            liste_dispo_json.append(objet.xml_en_json())
        return liste_dispo_json


# Fonction qui prend les listes de contenu en json
# Chaque élément de ces listes sont envoyés vers le serveur grâce au client
def executer():
    # Envoie de chaque utilisateur vers le serveur
    for utilisateur_json in Utilisateur.lecture_utilisateurs_csv('./data/utilisateurs.csv'):
        client.ClientServeurChalet('http://localhost:8000').ajout_utilisateur(utilisateur_json)
    # Envoie de chaque chalet vers le serveur
    for chalet_json in Chalet.lecture_chalets_csv('./data/chalets.csv'):
        client.ClientServeurChalet('http://localhost:8000').ajout_chalet(chalet_json)
    # Envoie de chaque reservation vers le serveur
    for reservation_json in Reservation.lecture_reservations_xml('./data/reservations.xml'):
        client.ClientServeurChalet('http://localhost:8000').ajout_reservation(reservation_json)
    # Envoie de chaque disponibilite vers le serveur
    for disponibilite_json in Disponibilite.lecture_dispo_xml('./data/disponibilites.xml'):
        client.ClientServeurChalet('http://localhost:8000').ajout_disponibilites_chalet(json.loads(disponibilite_json)
                                                                                        ['chalet'], disponibilite_json)


executer()
