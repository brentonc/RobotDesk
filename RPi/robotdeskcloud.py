import sys
import json
import requests
import robotdesk


def main(argv):
    listen()

def listen():
    print("Starting the robot desk cloud listener...")
    desk = None
    timeout_seconds = 60
    try:
        desk = robotdesk.DeskController(None)
        session = requests.Session()
        url = "https://bcalexaapp.azurewebsites.net/api/desk/command"
        headers = {
            'Content-type': 'application/json'
        }
        session.headers.update(headers)

        while(True):
            try:
                print('waiting...')
                response = session.get(url, timeout=timeout_seconds)
                msg = response.json()
                print("Got a command:" + json.dumps(msg))
                command = msg['CommandCode']
                arg = msg['CommandArg']
                    
                if command == "MOVE":
                    desk.move_to(int(arg))
                if command == "RESET":
                    desk.reset()
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
