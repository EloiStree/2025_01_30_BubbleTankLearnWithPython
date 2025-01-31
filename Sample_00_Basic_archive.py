import socket
import time

"""
127.0.0.1:8001
192.168.1.102:8001
127.0.0.118:8001
"""
import socket

class PlayerInGame:
    
    def __init__(self, player_id, team_id, position_x, position_y, position_z, rotation_yaw, rotation_pitch, rotation_roll, size, timestamp):
        self.player_id = player_id
        self.team_id = team_id
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.rotation_x = rotation_yaw
        self.rotation_y = rotation_pitch
        self.rotation_z = rotation_roll
        self.size = size
        self.timestamp = timestamp
        
    def set_information(self, player_id, team_id, position_x, position_y, position_z, rotation_yaw, rotation_pitch, rotation_roll, size, timestamp):
        self.player_id = player_id
        self.team_id = team_id
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.rotation_x = rotation_yaw
        self.rotation_y = rotation_pitch
        self.rotation_z = rotation_roll
        self.size = size
        self.timestamp = timestamp
        
        
player_dictionnary= {}

player_in_game =[]
def get_player(player_id):
    if player_id in player_dictionnary:
        return player_dictionnary[player_id]
    else:
        player = PlayerInGame(player_id, 0, 0, 0, 0, 0, 0, 0, 0, time.time())
        player_dictionnary[player_id] = player
        return player

def udp_listener(port):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to the port
    server_address = ('0.0.0.0', port)
    print(f"Starting UDP listener on port {port}...")
    sock.bind(server_address)
    
    try:
        while True:
            print("\nWaiting to receive message...")
            data, address = sock.recvfrom(65535)  # Buffer size is 65535 bytes
            
            lines = data.decode('utf-8').split('\n')
            timestamp = time.time()
            player_in_game.clear()
            
            for line in lines:
                player_info = line.split(':')
                
                if len(player_info) != 9:
                    continue
                if player_info[0] == "ID":
                    continue
                int_player_index=  int(player_info[0])
                player_in_game.append(int_player_index)
                player :PlayerInGame= get_player(int_player_index)
                player.team_id = int(player_info[1])
                player.position_x = int(player_info[2])/1000
                player.position_y = int(player_info[3])/1000
                player.position_z = int(player_info[4])/1000
                player.rotation_x = int(player_info[5])/1000
                player.rotation_y = int(player_info[6])/1000
                player.rotation_z = int(player_info[7])/1000
                player.size = int(player_info[8])/1000
                player.xtozangle = int(player_info[9])/1000
                player.timestamp = timestamp

            print("Player Count:",len(player_in_game))                
                
                
            print(f"Received {len(data)} bytes from {address}:")
            if len(player_in_game) > 0:
                index_first_player = player_in_game[0]
                player = get_player(index_first_player)
                print(f"First player: {index_first_player} - Team: {player.team_id} - Position: ({player.position_x}, {player.position_y}, {player.position_z}) - Rotation: ({player.rotation_x}, {player.rotation_y}, {player.rotation_z}) - Size: {player.size} - Timestamp: {player.timestamp}")
            
    
    except KeyboardInterrupt:
        print("\nShutting down UDP listener...")
    finally:
        sock.close()

if __name__ == "__main__":
    udp_listener(8001)