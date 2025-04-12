import socket
import logging
import os

# load vars from file
from dotenv import load_dotenv
load_dotenv() 



# tcp/ip address and port
ADDRESS = os.getenv("ADDRESS")
PORT = os.getenv("PORT")
LOG_LEVEL = os.getenv("LOG_LEVEL")

# Configure logging (adjust level to logging.INFO or logging.ERROR to reduce verbosity)
if LOG_LEVEL=='INFO':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
elif LOG_LEVEL=='DEBUG':
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
else:
    logging.basicConfig(level=logging.ERROR, format='%(message)s')
    
def read_until_done(sock):
    buffer, results = b"", []
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            logging.debug("Connection closed by server.")
            break
        buffer += chunk

        if b"ACK\r\n" in buffer:
            buffer = buffer.split(b"ACK\r\n", 1)[1]
            logging.debug("ACK received.")

        if b"DONE" in buffer:
            segment, _, buffer = buffer.partition(b"DONE")
            if segment:
                decoded_segment = segment.decode().strip()
                results.append(decoded_segment)
                logging.debug(f"Result segment: {decoded_segment}")
            logging.debug("DONE marker found.")
            break
    return results

def ask_PV(*args):
    logging.debug((ADDRESS,int(PORT)))
    command = chr(1).join(args)
    if not command.endswith('\r\n'):
        command += '\r\n'    
    logging.debug(command[:-2])
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((ADDRESS,PORT))
        sock.sendall(command.encode())
        results = read_until_done(sock)
        print(f" {args}, {results}")    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if sock:
            sock.sendall("-x".encode())
            sock.close()
        