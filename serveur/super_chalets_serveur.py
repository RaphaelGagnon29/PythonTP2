import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class SuperChalet:

    def __init__(self):
        self.__chalet = {}
        self.__utilisateur = {}

    @property
    def chalet(self):
        return self.__chalet

    @property
    def utilisateur(self):
        return self.__utilisateur

    def ajout_utilisateur(self, utilisateur):
        if utilisateur in self.__chalet.keys():
            raise ValueError('Utilisateur existant')
        self.__chalet[utilisateur] = []

    def ajout_chalet(self, chalet):
        if chalet in self.__chalet.keys():
            raise ValueError('Chalet existant')
        self.__chalet[chalet] = []


class TPBaseHTTPRequestHandler(BaseHTTPRequestHandler):

    super_chalet = SuperChalet()

    def do_POST(self):
        path = self.path
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


class ServeurTest:
    @staticmethod
    def run(serveur_class=HTTPServer, serveur_port=8000, handler_class=TPBaseHTTPRequestHandler):
        serveur_adresse = ('localhost', serveur_port)
        httpd = serveur_class(serveur_adresse, handler_class)
        httpd.serve_forever()


ServeurTest.run()