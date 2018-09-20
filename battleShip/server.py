#
#Authors: Matthew Sagen & Cory Petersen
#Date:    09/07/18
#
#server.py sets up an HTTP server used for recieving shots fired
#by an opponent in Battleship.
#

import sys
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qsl

arg_length = len(sys.argv)
port    = sys.argv[1]
portNum = int(port)
board_arr = [['_' for x in range(10)] for y in range(10)]

class RequestHandler(BaseHTTPRequestHandler):
    def send_result(self, coordinates):
        x = int(coordinates['x'])
        y = int(coordinates['y'])
        print(x,y)
        print(board_arr[x][y])
        if(board_arr[x][y] == 'C' or board_arr[x][y] == 'B' or
             board_arr[x][y] == 'R' or board_arr[x][y] == 'S' or board_arr[x][y]== 'D'):#if we hit a boat return hit=1
            msg = 'hit'
            self.send_response(200,msg)
        elif(board_arr[x][y] == '_'):#if we miss the boat return hit=0
            msg = 'miss'
            self.send_response(200,msg)
        elif(board_arr[x][y] == 'x'): #if we hit the same spot return HTTP Gone
            self.send_response(410)
        elif(x > 10 or y > 10):#if we hit out of bound return HTTP Not Found
            self.send_response(404)
        elif(x < 0 or y < 0):#lower bound check
            self.send_response(404)
        else:
            self.send_response(400)
            print("bad format")

    def do_POST(self):
        coordinates = self.get_coordinates()
        self.send_result(coordinates)
        self.end_headers()

    def get_coordinates(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        byte_coordinates = dict(parse_qsl(data))
        string_coordinates = {key.decode(): val.decode() for key, val in byte_coordinates.items()}
        return string_coordinates

def handle_board():
    global board_arr
    with open("own_board.txt") as textFile:
        board_arr = [list(line.rstrip()) for line in textFile]
    return board_arr
def throw_argument_error():
    print ("Error: incorrect arguments. Try python3 server.py <port_number> <file_name> <file_name>")
    sys.exit(0)

def handle_args():
    if (arg_length != 4):
        throw_argument_error()

def start_server(board_arr):
    try:
        server_address = ('127.0.0.1', portNum)
        print("Starting server 127.0.0.1 on port " + port)
        httpd = HTTPServer(server_address, RequestHandler)
        httpd.serve_forever()
    except Exception as e:
        print(str(e))

def main():
    print ("Processing...")
    handle_args()  #make sure arguments are valid
    board_arr = handle_board() #open own_board.txt and populate matrix with contents
    for x in board_arr:
        print(x)
    start_server(board_arr)
    print ("End of script.")

main()
