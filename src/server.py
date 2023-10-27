import socket
from typing import List

from command_parser import parse_command

storage = {}

def execute_command(operation: str, arguments: List[str], client_socket: socket.socket) -> None:
  if operation == 'GET':
    value = storage.get(arguments[0], 'nil')
    client_socket.sendall(value.encode())
    
  elif operation == 'SET':
    if len(arguments) != 2:
      client_socket.sendall(b'ERR wrong number of arguments for SET')
    else:
      storage[arguments[0]] = arguments[1]
      client_socket.sendall(b'OK')
    
  elif operation == 'DEL':
    deleted = storage.pop(arguments[0], None)
    client_socket.sendall(b'OK' if deleted else b'nil')
  
  else:
    client_socket.sendall(b'Unknown command')

  

def start_server(host='127.0.0.1', port=6379):
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
  # Reuse address (IP:PORT) immediately after server was shut down
  # OS holds the port in TIME_WAIT if server went off without closing the connection for whatever reason
  # SOL_SOCKET: Indicates that the options are applicable to the socket layer itself.
  # SO_REUSEADDR: The actual option that allows the address (the combination of IP and port) to be reused immediately after the socket is closed.
  # 1: Enables the option. Setting it to 0 would disable it.
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_socket.bind((host, port))
  server_socket.listen(5)

  print(f"Server listening on {host}:{port}")

  # start new client connection
  while True:
    client_socket, client_address = server_socket.accept()
    print(f'{client_address} connected.')
    
    # start a new REPL (continuously listen for client input)
    while True:
      try:
        data = client_socket.recv(1024).decode('utf-8')
      except UnicodeDecodeError:
        client_socket.sendall(b'ERR invalid utf-8 sequence')
        continue
      
      # CTRL+C: client closed connection:
      if not data:
        client_socket.close()
        break
      
      # Operation: GET, args: ['key']
      operation, arguments = parse_command(data)

      execute_command(
        operation=operation,
        arguments=arguments,
        client_socket=client_socket
      )
      
      print(f'Received: {data}\nStorage:{storage}')
      client_socket.sendall(b'\n> ')


if __name__ == '__main__':
  start_server()
