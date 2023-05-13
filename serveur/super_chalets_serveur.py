import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import gzip

#classe permettant de programmer les get, post, put et delete de la classe ci-dessous
class SuperChalet:
#constructeur
    def __init__(self):
        self.__chalet = {}
        self.__utilisateur = {}
        self.__reservation = {}
        self.__reservations = {}

#tous les getter des variables
    @property
    def chalet(self):
        return self.__chalet

    @property
    def utilisateur(self):
        return self.__utilisateur
    @property
    def reservation(self):
        return self.__reservation

    @property
    def reservations(self):
        return self.__reservations
# Méthode pour obtenir les informations d'une réservation
    def infos_reservation(self, id):

        file = f'./voute/{id}.res.gz'
        if os.path.exists(file):
            with gzip.open(file, 'wb') as res:
                inforeservations = self.__reservations
                res.write(inforeservations)
#méthode remplaçant la réservation
    def remplacer_reservation(self, nouvelle_reservation, ancienne_reservation):
        if nouvelle_reservation == ancienne_reservation:
            raise ValueError("Réservation identique déjà en place")
        for reservations, liste_de_reservations in self.__reservations.items():
            if ancienne_reservation in liste_de_reservations:
                index = liste_de_reservations.index(ancienne_reservation)
                liste_de_reservations[index] = nouvelle_reservation
                break
        else:
            raise ValueError("On ne peut remplacer la réservation, car elle n'existe pas")


#méthode pour ajouter un utilisateur
    def ajout_utilisateur(self, utilisateur):
        if utilisateur in self.__chalet.keys():
            raise ValueError('Utilisateur existant')
        self.__chalet[utilisateur] = []
#méthode pour ajouter un chalet
    def ajout_chalet(self, chalet):
        if chalet in self.__chalet.keys():
            raise ValueError('Chalet existant')
        self.__chalet[chalet] = []
#méthode pour ajouter une disponiblité à un chalet
    def ajout_disponibilites_chalet(self, chaletid, dispo):
        if chaletid not in self.__chalet.keys():
            raise ValueError('Chalet inexistant')
        self.__chalet[chaletid].append(dispo)
#méthode pour ajouter une réservation
    def ajout_reservation(self, reservationid):
        if reservationid in self.__reservation.keys():
            raise ValueError('Reservation existante')
        self.__reservation[reservationid] = []
#méthode pour supprimer une réservation
    def supprimer_reservation(self,reservationid):
        if reservationid not in self.__reservation.keys():
            raise ValueError("reservation inexistante")
        else:
            del(self.__reservation[reservationid])
#méthode pour retourner un utilisateur
    def retourner_reservation(self,reservationid):
        for reservation, liste_de_reservations in self.__reservations.items():
            if reservationid in liste_de_reservations:
                return liste_de_reservations[0]
        raise ValueError("cette id de réservation n'existe pas")
#méthode pour retourner les reservations d'un utilisateur
    def retourner_email(self,email):
        if email in self.__reservations:
            return self.__reservations[email]
        raise ValueError("Il n'y a pas de réservation avec cette adresse email")

#méthode pour retourner un chalet
    def retourner_chalet(self,chaletid):
        if chaletid in self.__chalet:
            return self.__chalet[chaletid]
        raise ValueError("Ce chalet n'existe pas")

#méthode pour retourner les reservations triées
    def retourner_reservations(self):
        for i in range(1,len(self.__reservations)):
            courant = self.__reservations[i]
            p = i
            while p > 0 and self.__reservations[p-1] > courant:
                self.__reservations[p] = self.__reservations[ p - 1]
                p = p-1
            self.__reservations[p] = courant
            return self.__reservations


#permet de faire fonctionner get,post,put et delete dans le client
class TPBaseHTTPRequestHandler(BaseHTTPRequestHandler):

    super_chalet = SuperChalet()
#toutes les fonctions de post
    def do_POST(self):
        path = self.path
#post pour le chalet
        if path == '/chalet':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            json_str = json.loads(body)
            try:
                self.super_chalet.ajout_chalet(json_str['chalet'])
                self.send_response(200)
            except ValueError:
                self.send_response(542, 'Chalet existant')
            self.end_headers()
#post pour l'utilisateur
        elif path == '/utilisateur':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            json_str = json.loads(body)
            try:
                self.super_chalet.ajout_utilisateur(json_str['utilisateur'])
                self.send_response(200)
            except ValueError:
                self.send_response(542, 'Utilisateur existant')
            self.end_headers()
#post pour les disponibilités du chalet
        elif path.startswith('/chalet/'):
            chaletid = path.split('/')[2]
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            json_str = json.loads(body)
            self.super_chalet.ajout_disponibilites_chalet(chaletid, json_str['disponibilite'])
            self.send_response(200)
            self.end_headers()
#post pour les réservations
        elif path == '/reservation':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            json_str = json.loads(body)
            try:
                self.super_chalet.ajout_reservation(json_str['reservation'])
                self.send_response(200)
            except ValueError:
                self.send_response(542, 'reservation existante')
            self.end_headers()

    def do_GET(self):
        headers = self.headers
        path = self.path
        print(path)
#get le chalet
        if path.startswith('/chalet/'):
            chalet = path.split('/')[2]
            content = 'chalet: ' + chalet + ' -> ' + str(self.super_chalet.chalet[chalet])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(content, 'utf-8'))
#get la reservation
        elif path.startswith('/reservation/'):
            reservation = path.split('/')[2]
            content = 'reservation: ' + reservation + ' -> ' + str(self.super_chalet.reservation[reservation])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(content, 'utf-8'))
#get les infos de l'utilisateur
        elif path.startswith('/reservations/'):
            reservations = path.split('/')[2]
            content = 'email: ' + reservations + ' -> ' + str(self.super_chalet.reservations[reservations])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(content, 'utf-8'))
#get la liste de reservations triée
        elif path.startswith('/reservations'):
            self.super_chalet.retourner_reservations()
        else:
            self.send_response(542, 'contenu de votre requête non trouvé')
            self.end_headers()
#permettre l'utilisation de put
    def do_PUT(self):
        path = self.path
        if path.startswith('/reservation/'):
            try:
                os.makedirs(os.path.dirname(path))
            except ValueError:
                self.send_response(542, 'reservation inexistante')
            length = int(self.headers['Content-Length'])
            with open(path, 'wb') as f:
                f.write(self.rfile.read(length))
            self.send_response(200)
#permettre l'utilisation de delete
    def do_DELETE(self):
        headers = self.headers
        path = self.path
        print(path)
        if path == '/reservation':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            json_str = json.loads(body)
            try:
                self.super_chalet.supprimer_reservation(json_str['reservation'])
                self.send_response(200)
            except ValueError:
                self.send_response(542, 'reservation inexistante')
            self.end_headers()
class ServeurTest:
    @staticmethod
    def run(serveur_class=HTTPServer, serveur_port=8000, handler_class=TPBaseHTTPRequestHandler):
        serveur_adresse = ('localhost', serveur_port)
        httpd = serveur_class(serveur_adresse, handler_class)
        httpd.serve_forever()


ServeurTest.run()
