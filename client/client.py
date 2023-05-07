import requests


class ClientServeur:

    def __init__(self, url_base):
        self.__url_base = url_base
        self.__post_headers = {'Content-Type': 'text/json'}

    def ajout_chalet(self, chalet):
        json_body = '{"nom": "' + chalet + '" }'
        req = requests.post(self.__url_base + '/chalet', data=json_body)
        print(req.status_code)
        print(req.content)

    def retourne_chalet(self, chaletid):
        req = requests.get(self.__url_base + '/chalet/' + chaletid)
        print(req.status_code)
        print(req.content)

    def ajout_disponibilites_chalet(self, chaletid, dispo):
        json_body = '{"nom": "' + dispo + '" }'
        req = requests.post(self.__url_base + '/chalet/' + chaletid + '/plage', data=json_body)
        print(req.status_code)
        print(req.content)

    def ajout_utilisateur(self, utilisateur):
        json_body = '{"nom": "' + utilisateur + '" }'
        req = requests.post(self.__url_base + '/utilisateur', data=json_body)
        print(req.status_code)
        print(req.content)


client = ClientServeur('http://localhost:8000')
