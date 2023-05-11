from client import client
import csv
from xml.dom import minidom


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

    def csv_en_json(self):
        return {
            "utilisateur":
                {
                    "email": self.__email,
                    "mot_de_passe": self.__mdp,
                    "nom": self.__nom,
                    "prenom": self.__prenom,
                    "type": self.__type,
                    "adresse":
                        {
                            "no_civique": self.__adresse_no,
                            "rue": self.__adresse_rue,
                            "ville": self.__adresse_ville,
                            "province": self.__adresse_prov,
                            "pays": self.__adresse_pays,
                            "code_postal": self.__adresse_cp
                        }
                }
            }

class Chalet:

    def __init__(self, id, nom, url_image, geo_lat, geo_long):
        self.__id = id
        self.__nom = nom
        self.__url_image = url_image
        self.__geo_lat = geo_lat
        self.__geo_long = geo_long

    def csv_en_json(self):
        return {
            "chalet":
                {
                    "id": self.__id,
                    "nom": self.__nom,
                    "url_image": self.__url_image,
                    "geolocalisation":
                        {
                            "latitude": self.__geo_lat,
                            "longitude": self.__geo_long
                        }
                }
            }


liste_utilisateurs = []
with open('./data/utilisateurs.csv', 'r') as csv_utilisateurs:
    csv_reader = csv.reader(csv_utilisateurs)
    for utilisateur in csv_reader:
        if utilisateur[0] == 'email':
            continue
        else:
            objet = Utilisateur(utilisateur[0], utilisateur[1], utilisateur[2], utilisateur[3], utilisateur[4],
                                utilisateur[5], utilisateur[6], utilisateur[7], utilisateur[8], utilisateur[9],
                                utilisateur[10])
            liste_utilisateurs.append(objet.csv_en_json())

for i in liste_utilisateurs:
    client.ClientServeurChalet('http://localhost:8000').ajout_utilisateur(i)


liste_chalets = []
with open('./data/ chalets,csv', 'r') as csv_chalets:
    csv_reader_ = csv.reader(csv_chalets)
    for chalet in csv_reader_:
        if chalet[0] == 'id':
            continue
        else:
            objet_ = Chalet(chalet[0], chalet[1], chalet[2], chalet[3], chalet[4])
            liste_chalets.append(objet_.csv_en_json())

for j in liste_chalets:
    client.ClientServeurChalet('http://localhost:8000').ajout_chalet(j)
