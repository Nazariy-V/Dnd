import socket

def client_program():
    host = "localhost"  # Assuming both server and client run on the same machine
    port = 8080  # Change this to the server's port number
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))  # Connect to the server
    
    player_name = input("Enter your name: ")
    client_socket.send(player_name.encode('utf-8'))  # Send player's name to the server

    print(client_socket.recv(1024).decode('utf-8'))  # Receive welcome message

    while True:
        command = input("Enter 'turn' to check whose turn it is, or 'players' to see all players: ")
        client_socket.send(command.encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8')
        print(response)

        if command.lower().strip() == 'bye':
            break

    client_socket.close()

if __name__ == "__main__":
    client_program()
