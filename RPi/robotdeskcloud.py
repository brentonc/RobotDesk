import sys
import json
import requests
import robotdesk
import getopt


def main(argv):
    """Primary entry point"""

    whatif = False
    
    opts, args = getopt.getopt(argv, "w")
    for opt, arg in opts:
        if opt == '-w':
            whatif = True

    listen(whatif)

def listen(whatif):
    """ Main program.  Listens to web service for desk commands. """
    print("Starting the robot desk cloud listener...")
    desk = None
    timeout_seconds = 60
    try:
        desk = robotdesk.DeskController(azure=None, whatif=whatif)
        session = requests.Session()
        command_url = "https://bcalexaapp.azurewebsites.net/api/desk/command"
        height_info_url = "https://bcalexaapp.azurewebsites.net/api/desk/heightinfo"
        headers = {
            'Content-type': 'application/json'
        }
        session.headers.update(headers)

        while True:
            try:
                
                ht = desk.read_height()
                session.post(height_info_url,data = str(ht))
                
                print('waiting...')
                response = session.get(command_url, timeout=timeout_seconds)
                msg = response.json()
                if msg is not None:
                    print("Got a command:" + json.dumps(msg))
                    command = msg['CommandCode']
                    arg = msg['CommandArg']
                    if command == "MOVE":
                        desk.move_to(int(arg))
                    if command == "RESET":
                        desk.reset()
                ht = desk.read_height()
                response = session.post(height_info_url,data = str(ht))
            except TimeoutError:
                #that's ok, just ask again
                pass
            except requests.ReadTimeout:
                #that's ok, just ask again
                pass
    finally:
        print("Stopping the robot desk cloud listener.  Have a nice day!")
        if desk is not None:
            desk.cleanup()

if __name__ == "__main__":
    main(sys.argv[1:])
