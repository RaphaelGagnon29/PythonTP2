from client import client
import csv
from xml.dom import minidom
import time
import json


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

    def csv_to_json(self):
        return json.dumps({"utilisateur": {"email": self.__email, "mot_de_passe": self.__mdp, "nom": self.__nom,
                                           "prenom": self.__prenom, "type": self.__type,
                                           "adresse": {"no_civique": self.__adresse_no, "rue": self.__adresse_rue,
                                                       "ville": self.__adresse_ville, "province": self.__adresse_prov,
                                                       "pays": self.__adresse_pays, "code_postal": self.__adresse_cp}}})


    @staticmethod
    def export_csv(utilisateur_json):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open(f'./export_{timestamp}.csv', 'w', newline='') as csv_file:
            champs = ['email', 'mdp', 'nom', 'prenom', 'type', 'adresse_no', 'adresse_rue', 'adresse_ville',
                      'adresse_prov', 'adresse_pays', 'adresse_cp']
            csv_dict_writer = csv.DictWriter(csv_file, fieldnames=champs)
            csv_dict_writer.writeheader()
            csv_dict_writer.writerow(utilisateur_json)


class Chalet:

    def __init__(self, id, nom, url_image, geo_lat, geo_long):
        self.__id = id
        self.__nom = nom
        self.__url_image = url_image
        self.__geo_lat = geo_lat
        self.__geo_long = geo_long

    def csv_en_json(self):
        return json.dumps({"chalet": {"id": self.__id, "nom": self.__nom, "url_image": self.__url_image,
                                      "geolocalisation": {"latitude": self.__geo_lat,
                                                           "longitude": self.__geo_long}}})


class Reservation:

    def __init__(self, id, chalet, utilisateur, plage):
        self.__id = id
        self.__chalet = chalet
        self.__utilisateur = utilisateur
        self.__plage = plage

    def xml_to_json(self):
        return json.dumps({"reservation": {"id": self.__id, "chalet": self.__chalet, "plages": self.__plage,
                                           "utilisateur": self.__utilisateur}})


liste_utilisateurs_json = []
with open('./data/utilisateurs.csv', 'r') as csv_utilisateurs:
    csv_reader = csv.reader(csv_utilisateurs)
    for utilisateur in csv_reader:
        if utilisateur[0] == 'email':
            continue
        else:
            objet = Utilisateur(utilisateur[0], utilisateur[1], utilisateur[2], utilisateur[3], utilisateur[4],
                                utilisateur[5], utilisateur[6], utilisateur[7], utilisateur[8], utilisateur[9],
                                utilisateur[10])
            liste_utilisateurs_json.append(objet.csv_to_json())

for i in liste_utilisateurs_json:
    client.ClientServeurChalet('http://localhost:8000').ajout_utilisateur(i)


liste_chalets_json = []
with open('./data/chalets.csv', 'r') as csv_chalets:
    csv_reader_ = csv.reader(csv_chalets)
    for chalet in csv_reader_:
        if chalet[0] == 'id':
            continue
        else:
            objet_ = Chalet(chalet[0], chalet[1], chalet[2], chalet[3], chalet[4])
            liste_chalets_json.append(objet_.csv_en_json())

for j in liste_chalets_json:
    client.ClientServeurChalet('http://localhost:8000').ajout_chalet(j)


for x in liste_utilisateurs_json:
    Utilisateur.export_csv(x)


with open('./data/reservations.xml', 'r') as xml_file:
    doc = minidom.parse(xml_file)

liste_reservations = []
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
    liste_reservations.append([id, chalet, utilisateur, liste_plage])

