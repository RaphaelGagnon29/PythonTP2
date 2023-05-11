import requests


class ClientServeurChalet:

    def __init__(self, url_base):
        self.__url_base = url_base
        self.__post_headers = {'Content-Type': 'text/json'}

    def retourne_reservation(self, reservationid):
        req = requests.get(self.__url_base + '/reservation/' + reservationid)
        print(req.status_code)
        print(req.content)

    def retourne_reservations(self, utilisateur):
        req = requests.get(self.__url_base + '/reservations/' + utilisateur)
        print(req.status_code)
        print(req.content)

    def ajout_reservation(self, reservation):
        json_body = reservation
        req = requests.post(self.__url_base + '/reservation/', data=json_body)
        print(req.status_code)
        print(req.content)

    def modifier_reservation(self, reservation):
        json_body = reservation
        req = requests.put(self.__url_base + '/reservation/', data=json_body)
        print(req.status_code)
        print(req.content)
    def ajout_chalet(self, chalet):
        json_body = chalet
        req = requests.post(self.__url_base + '/chalet', data=json_body)
        print(req.status_code)
        print(req.content)

    def retourne_chalet(self, chaletid):
        req = requests.get(self.__url_base + '/chalet/' + chaletid)
        print(req.status_code)
        print(req.content)

    def ajout_disponibilites_chalet(self, chaletid, dispo):
        json_body = dispo
        req = requests.post(self.__url_base + '/chalet/' + chaletid + '/plage', data=json_body)
        print(req.status_code)
        print(req.content)

    def ajout_utilisateur(self, utilisateur):
        json_body = utilisateur
        req = requests.post(self.__url_base + '/utilisateur', data=json_body)
        print(req.status_code)
        print(req.content)


session = requests.Session()
session.trust_env = False
session.get('http://localhost:8000')
client = ClientServeurChalet('http://localhost:8000')
