#
#Authors: Matthew Sagen & Cory Petersen
#Date:    09/07/18
#
#client.py sets up an HTTP client used for sending shots fired
#by an opponent in Battleship.
#
import sys
import requests
from urllib.parse import parse_qsl

ipAdd      = sys.argv[1]  #IP Address
portNum    = sys.argv[2]  #port number
x          = sys.argv[3]  #x coordinate
y          = sys.argv[4]  #y coordinate

def throw_argument_error():
    print ("Error: incorrect arguments. Try python3 server.py <ip_address> <port_number> <xCoordinate> <yCoordinate>")
    sys.exit(0)

def handle_args():
    if(len(sys.argv) != 5):
        throw_argument_error()
def server_connection():
    try:
        newAddress = 'http://' + ipAdd + ':' + portNum
        print("Firing at " + newAddress + " at x=" + x + "&y=" + y)
        payload = {'x':x, 'y':y}
        r = requests.post(newAddress, data=payload)
        print(r.status_code, r.reason)

    except Exception as e:
        print(str(e))

def main():
    print ("Processing...")
    handle_args()       #make sure arguments are valid
    server_connection() #create connection with server
    print ("End of turn.")

main()
