# Server side
import threading
import socket
import pickle  # For serializing/deserializing game state

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(2)  # Listen for two clients

# Initialize the game state
GRID_SIZE = 10
game_state = {
    'grid': [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)],
    'players': [{'row': 0, 'col': 0}, {'row': 9, 'col': 9}],  # Example: Two players at opposite corners
    'visited_cells': []
}

# Function to handle client connections
def handle_client(client_socket, player_id):
    while True:
        # Receive action from client
        action = client_socket.recv(1024)
        # Update game state based on action
        # For simplicity, let's assume the action is just a move
        if action == b'UP':
            game_state['players'][player_id]['row'] -= 1
        elif action == b'DOWN':
            game_state['players'][player_id]['row'] += 1
        elif action == b'LEFT':
            game_state['players'][player_id]['col'] -= 1
        elif action == b'RIGHT':
            game_state['players'][player_id]['col'] += 1
        # Serialize game state and send to all clients
        serialized_state = pickle.dumps(game_state)
        for client in clients:
            client.send(serialized_state)

# Accept client connections
clients = []
for i in range(2):
    client_socket, _ = server_socket.accept()
    clients.append(client_socket)
    # Start a new thread to handle the client
    threading.Thread(target=handle_client, args=(client_socket, i)).start()

# Close server socket
server_socket.close()
