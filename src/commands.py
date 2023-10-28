import pickle
import socket
import time
from typing import List, Tuple

from constants import PERIODIC_SAVE_INTERVAL_SECONDS, storage


def save_to_disk():
    with open("redis_data.pkl", "wb") as f:
        pickle.dump(storage, f)


def periodic_save():
    while True:
        save_to_disk()
        time.sleep(PERIODIC_SAVE_INTERVAL_SECONDS)


def parse_command(raw_command: str) -> Tuple[str, List[str]]:
    tokens = raw_command.strip().split()

    operation = tokens[0].upper()
    arguments = tokens[1:]

    return operation, arguments


def execute_command(
    operation: str, arguments: List[str], client_socket: socket.socket
) -> None:
    if operation == "GET":
        value, expire_time = storage.get(arguments[0], ("nil", None))

        # check if key is expired
        if expire_time and time.time() > expire_time:
            del storage[arguments[0]]
            value = "nil"

        client_socket.sendall(value.encode())

    elif operation == "SET":
        if len(arguments) < 2 or len(arguments) > 3:
            client_socket.sendall(b"ERR wrong number of arguments for SET")
        else:
            key, value = arguments[:2]
            ttl = int(arguments[2]) if len(arguments) == 3 else None
            storage[key] = (value, ttl)
            client_socket.sendall(b"OK")

    elif operation == "DEL":
        deleted = storage.pop(arguments[0], None)
        client_socket.sendall(b"OK" if deleted else b"nil")

    elif operation == "SAVE":
        save_to_disk()
        client_socket.sendall(b"OK")
    elif operation == "EXPIRE":
        if len(arguments) != 2:
            client_socket.sendall(b"ERR wrong number of arguments for EXPIRE")
        else:
            key, ttl = arguments
            ttl = int(ttl)
            entry = storage.get(key, None)
            if entry:
                value, _ = entry
                expire_time = time.time() + ttl
                storage[key] = (value, expire_time)
                client_socket.sendall(b"OK")

    else:
        client_socket.sendall(b"Unknown command")
