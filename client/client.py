import requests
import unittest as ut

#Cette classe permet de faire les demandes de manipulation des données qui seront envoyés au serveur
class ClientServeurChalet:
    def __init__(self, url_base):
        self.__url_base = url_base
        self.__post_headers = {'Content-Type': 'text/json'}

#retourner la réservation selon le reservationID. (numéro 1 client)
    def retourne_reservation(self, reservationid):
        req = requests.get(self.__url_base + f'/reservation/{reservationid}')
        print(req.status_code)
        print(req.content)

#retourner toutes les réservations d'un utilisateur (numéro 2 client)
    def retourne_reservations_utilisateur(self, utilisateur):
        req = requests.get(self.__url_base + f'/reservations/{utilisateur}')
        print(req.status_code)
        print(req.content)

#ajouter une reservation ( numéro 3 client)
    def ajout_reservation(self, reservation):
        json_body = '{"reservation": "' + reservation + '" }'
        req = requests.post(self.__url_base + '/reservation', data=json_body)
        print(req.status_code)
        print(req.content)

#remplacer une réservation existante ( numéro 4 client)
    def remplacer_reservation(self, reservationid):
        json_body = '{"reservation": "' + reservationid + '" }'
        req = requests.put(self.__url_base + f'/reservation/', data=json_body)
        print(req.status_code)
        print(req.content)

#supprimer une réservation ( numéro 5 client)
    def supprimer_reservation(self, reservationid):
        req = requests.delete(self.__url_base + f'/reservations/{reservationid}')
        print(req.status_code)
        print(req.content)

#ajouter un utilisateur ( numéro 6 client)
    def ajout_utilisateur(self, utilisateur):
        json_body = '{"utilisateur": "' + utilisateur + '" }'
        req = requests.post(self.__url_base + '/utilisateur', data=json_body)
        print(req.status_code)
        print(req.content)

#retourner la liste triée des réservations selon leur reservationID (numéro 7 client)
    def retourne_reservations(self):
        req = requests.get(self.__url_base + '/reservations')
        print(req.status_code)
        print(req.content)

#ajouter un chalet ( numéro 8 client)
    def ajout_chalet(self, chalet):
        json_body = '{"chalet": "' + chalet + '" }'
        req = requests.post(self.__url_base + '/chalet', data=json_body)
        print(req.status_code)
        print(req.content)

#retourner les informations d'un chalet ( numéro 9 client)
    def retourne_chalet(self, chaletid):
        req = requests.get(self.__url_base + f'/chalet/{chaletid}')
        print(req.status_code)
        print(req.content)

#créer une disponibilité pour le chalet (numéro 10 client)
    def ajout_disponibilites_chalet(self, chaletid, dispo):
        json_body = '{"disponiblité": "' + dispo + '" }'
        req = requests.post(self.__url_base + f'/chalet/{chaletid}/plage', data=json_body)
        print(req.status_code)
        print(req.content)

#cette classe permet d'effectuer les tests unitaires
class Test(ut.TestCase):
#tests unitaires split à la méthode des notes de cours
#test unitaire sur le retour de la reservation
    def test_retourne_reservation(self,req):
        s = req
        self.assertEqual(s.split(), req, 'reservation')

        with self.assertRaises(TypeError):
            s.split(2)
#test unitaire sur le retour de l'utilisateur
    def test_retourne_utilisateur(self,req):
        s = req
        self.assertEqual(s.split(), req, 'utilisateur')

        with self.assertRaises(TypeError):
            s.split(2)
#test unitaire sur le retour des informations d'un chalet
    def test_ajout_chalet(self,req):
        s = req
        self.assertEqual(s.split(), req, 'chaletid')

        with self.assertRaises(TypeError):
            s.split(2)




if __name__ == '__main__':
   ut.main()
session = requests.Session()
session.trust_env = False
session.get('http://localhost:8000')
client = ClientServeurChalet('http://localhost:8000')
