import socket

from command_parser import parse_command


def start_server(host='127.0.0.1', port=6379):
  print(f"Starting server")

  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.bind((host, port))
  server_socket.listen(5)

  print(f"Server listening on {host}:{port}")

  while True:
    client_socket, client_address = server_socket.accept()
    print(f'{client_address} connected.')
    data = client_socket.recv(1024).decode('utf-8')
    
    operation, arguments = parse_command(data)
    
    print(f"Received: {data}")
    client_socket.sendall(b'OK')
    client_socket.close()

if __name__ == '__main__':
  start_server()
