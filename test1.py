import socket
import threading

# Player class to store player information
class Player:
    def __init__(self, name, address):
        self.name = name
        self.address = address

# Initialize the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.1.12', 8080)  # Change this to your desired host and port
server_socket.bind(server_address)
server_socket.listen(5)
print(server_socket.getsockname())
# List to store connected players
players = []

def handle_client(client_socket, address):
    try:
        # Receive player's name
        player_name = client_socket.recv(1024).decode('utf-8')
        print(f"Player {player_name} connected from {address}")
        player = Player(player_name, address)
        players.append(player)

        # Send welcome message
        client_socket.send(f"Welcome, {player_name}! You are connected.".encode('utf-8'))

        # Main game loop
        while True:
            client_socket.send("".encode('utf-8'))
            command = client_socket.recv(1024).decode('utf-8')
            if command.lower() == "pass":
                print("Player passed")
            if command.lower() == 'turn':
                # Implement logic to determine whose turn it is
                # For example, alternate turns between players
                # You can customize this based on your game rules
                # Send the turn information back to the player
                client_socket.send("It's your turn!".encode('utf-8'))
            elif command.lower() == 'players':
                # Send the list of current players to the player
                player_list = ", ".join(p.name for p in players)
                client_socket.send(f"Current players: {player_list}".encode('utf-8'))
            else:
                client_socket.send("Invalid command. Try again.".encode('utf-8'))

    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        # Clean up: remove player from the list
        
        client_socket.close()

# Accept incoming connections
print("Server listening on", server_address)
while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
