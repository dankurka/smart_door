from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer as BaseHTTPServer
import os
import urlparse
import json


def loadUserFile():
    f = open('users.json', 'r')
    content = f.read()
    f.close()
    data = json.loads(content)
    return [user for user in data['users']]

def verifyUser(username, password):
    for user in loadUserFile():
        if user['username'] == username and user['password'] == password:
            return True
    return False

class HTTPHandler(SimpleHTTPRequestHandler):
    """This handler uses server.base_path instead of always using os.getcwd()"""
    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(self.server.base_path, relpath)
        return fullpath
    def do_POST(self):
        parsed_path = urlparse.urlparse(self.path)
        parsed_query = urlparse.parse_qs(parsed_path.query)
        username = parsed_query['username'][0]
        password = parsed_query['password'][0]
        if parsed_path.path == '/open_door':
            self.handle_open_door(username, password)
        elif parsed_path.path == '/login':
            self.handle_login(username, password)
        else:
            self.send_response(404)
            self.end_headers()

    def handle_login(self, username, password):
        if not verifyUser(username, password):
            self.send_response(400)
            self.end_headers()
            self.wfile.write("Invalid username or password.")
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Valid login.")
       
    def handle_open_door(self, username, password):
         if not verifyUser(username, password):
             self.send_response(400)
             self.end_headers()
             self.wfile.write("Invalid username or password.")
             return
         self.send_response(200)
         self.end_headers()
         self.wfile.write("Opening door.")
         self.server.openDoorFunction()


class HTTPServer(BaseHTTPServer):
    """The main server, you pass in base_path which is the path you want to serve requests from"""
    def __init__(self, base_path, openDoorFunction, server_address, RequestHandlerClass=HTTPHandler):
        self.base_path = base_path
        self.openDoorFunction = openDoorFunction
        BaseHTTPServer.__init__(self, server_address, RequestHandlerClass)

def setupServer(openDoorFunction):
    web_dir = os.path.join(os.path.dirname(__file__), 'web')
    httpd = HTTPServer(web_dir, openDoorFunction, ("", 8080))
    return httpd


if __name__ == "__main__":
    def testing_door():
        print('opening door')
    setupServer(testing_door).serve_forever()
