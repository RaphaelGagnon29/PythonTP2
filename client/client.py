import requests
import unittest as ut

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

class TestReservation(ut.TestCase):

    def test_retourne_reservation(self):


if __name__ == '__main__':
    ut.main()
session = requests.Session()
session.trust_env = False
session.get('http://localhost:8000')
client = ClientServeurChalet('http://localhost:8000')
