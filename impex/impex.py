from client import client
import csv
from xml.dom import minidom

with open('./data/utilisateurs.csv', 'r') as csv_utilisateurs:
    csv_reader = csv.reader(csv_utilisateurs)
    for utilisateur in csv_reader:
        client.ClientServeur('http://localhost:8000').ajout_utilisateur(utilisateur)

with open('./data/ chalets,csv', 'r') as csv_chalets:
    csv_reader_ = csv.reader(csv_chalets)
    for chalet in csv_reader_:
        client.ClientServeur('http://localhost:8000').ajout_chalet(chalet)

