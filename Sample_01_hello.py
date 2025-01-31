import random
import time

"""
127.0.0.1:8001
192.168.1.102:8001
127.0.0.118:8001
"""
import socket
import asyncio
from iid42 import SendUdpIID
import threading

m_target_ip = "127.0.0.1"
m_target_port = 2504
m_listened_port = 8001


# Choose random player index
# Choose random player index
int_player_index = -42


tank: SendUdpIID = SendUdpIID(m_target_ip, m_target_port,True, True)




upPress=1038
downPress=1040
leftPress=1037
rightPress=1039
attackSpacePress=1032


def go_left_start():
    tank.push_index_integer_date_ntp_in_milliseconds(int_player_index, leftPress, 0)
def go_left_stop():
    tank.push_index_integer_date_ntp_in_milliseconds(int_player_index, leftPress+1000, 0)
def go_right_start():
    tank.push_index_integer_date_ntp_in_milliseconds(int_player_index, rightPress, 0)
def go_right_stop():
    tank.push_index_integer_date_ntp_in_milliseconds(int_player_index, rightPress+1000, 0)
def go_up_start():
    tank.push_index_integer_date_ntp_in_milliseconds(int_player_index, upPress, 0)
def go_up_stop():
    tank.push_index_integer_date_ntp_in_milliseconds(int_player_index, upPress+1000, 0)
def go_down_start():
    tank.push_index_integer_date_ntp_in_milliseconds(int_player_index, downPress, 0)
def go_down_stop():
    tank.push_index_integer_date_ntp_in_milliseconds(int_player_index, downPress+1000, 0)
def attack_start():
    tank.push_index_integer_date_ntp_in_milliseconds(int_player_index, attackSpacePress, 0)
def attack_stop():
    tank.push_index_integer_date_ntp_in_milliseconds(int_player_index, attackSpacePress+1000, 0)
    
def attack():
    attack_start()
    attack_stop()


class PlayerInGame:
    
    def __init__(self, player_id, team_id, position_x, position_y, position_z, rotation_euler_x, rotation_euler_y, rotation_euler_z, size, xtozangle, timestamp):
        self.player_id = player_id
        self.team_id = team_id
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.rotation_euler_x = rotation_euler_x
        self.rotation_euler_y = rotation_euler_y
        self.rotation_euler_z = rotation_euler_z
        self.size = size
        self.xtozangle = xtozangle
        self.timestamp = timestamp
        
    def set_information(self, player_id, team_id, position_x, position_y, position_z, rotation_euler_x, rotation_euler_y, rotation_euler_z, size, xtozangle, timestamp):
        self.player_id = player_id
        self.team_id = team_id
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.rotation_euler_x = rotation_euler_x
        self.rotation_euler_y = rotation_euler_y
        self.rotation_euler_z = rotation_euler_z
        self.size = size
        self.xtozangle = xtozangle
        self.timestamp = timestamp
        
        
player_dictionnary= {}

player_in_game =[]
def get_player(player_id):
    player_id = str(player_id)
    if player_id in player_dictionnary:
        return player_dictionnary[player_id]
    else:
        player = PlayerInGame(player_id, 0, 0, 0, 0, 0, 0, 0, 0,0, time.time())
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
           #  print("\nWaiting to receive message...")
            data, address = sock.recvfrom(65535)  # Buffer size is 65535 bytes
            
            lines = data.decode('utf-8').split('\n')
            timestamp = time.time()
            player_in_game.clear()
            
            for line in lines:
                player_info = line.split(':')
                
                if len(player_info) != 10:
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
                player.rotation_euler_x = int(player_info[5])/1000
                player.rotation_euler_y = int(player_info[6])/1000
                player.rotation_euler_z = int(player_info[7])/1000
                player.size = int(player_info[8])/1000
                player.xtozangle = int(player_info[9])/1000
                player.timestamp = timestamp

            # print("Player Count:",len(player_in_game))                
                
                
            # print(f"Received {len(data)} bytes from {address}:")
            if len(player_in_game) > 0:
                index_first_player = player_in_game[0]
                player = get_player(index_first_player)
                # print(f"First player: {index_first_player} - Team: {player.team_id} - Position: ({player.position_x}, {player.position_y}, {player.position_z}) - Rotation: ({player.rotation_x}, {player.rotation_y}, {player.rotation_z}) - Size: {player.size} - Timestamp: {player.timestamp}")
            
    
    except KeyboardInterrupt:
        print("\nShutting down UDP listener...")
    finally:
        sock.close()

def push(value, delay):
    global int_player_index
    tank.push_index_integer_date_ntp_in_milliseconds(int_player_index, value, delay)

def console_thread():
    while True:
        command = input("Enter a command: ")
        if command == "exit":
            break
        elif command == "list":
            print("Players in game:")
            for player_id, player in player_dictionnary.items():
                print(f"Player ID: {player_id} - Team: {player.team_id} - Position: ({player.position_x}, {player.position_y}, {player.position_z}) - Rotation: ({player.rotation_x}, {player.rotation_y}, {player.rotation_z}) - Size: {player.size} - Timestamp: {player.timestamp}")
        else:
            print("Unknown command")
    
    print("Exiting console thread...")
    
def display_all_players():
    print("Players in game:")
    for player_id, player in player_dictionnary.items():
        print(f"Player ID: {player_id} - Team: {player.team_id} - Position: ({player.position_x}, {player.position_y}, {player.position_z}) - Rotation: ({player.rotation_x}, {player.rotation_y}, {player.rotation_z}) - Size: {player.size} - Timestamp: {player.timestamp}")
    
    
def push_joystick_value( x:float, y:float, lx:float, ly:float):
    
    
    
    value = 1800000000
    if ly != 0:
        value += (int((ly+1)/2.0  *98)+1)
    if lx != 0:
        value += (int((lx+1)/2.0 *98)+1)*100
    if y != 0:
        value += (int((y+1)/2.0  *98)+1)*10000
    if x != 0:
        value += (int((x+1)/2.0 *98)+1)*1000000
    print (f"JOYSTICK: {value}")
    tank.push_index_integer_date_ntp_in_milliseconds(int_player_index, value, 0)

import math    
class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def copy(self):
        return Vector3(self.x, self.y, self.z)

    def normalize(self):
        length = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        if length != 0:
            self.x /= length
            self.y /= length
            self.z /= length

    def scale(self, scalar):
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar

    def add(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def sub(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        
    def rotate_around_y(self, angle):
        new_x = self.x * math.cos(angle) + self.z * math.sin(angle)
        new_z = -self.x * math.sin(angle) + self.z * math.cos(angle)
        self.x = new_x
        self.z = new_z

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"

# Placeholder for the angle calculation function
def angle_left_to_right_from_direction_signe_angle(dir1, dir2):
    # Calculate the angle between two vectors using the dot product
    dot_product = dir1.x * dir2.x + dir1.y * dir2.y + dir1.z * dir2.z
    magnitude1 = math.sqrt(dir1.x**2 + dir1.y**2 + dir1.z**2)
    magnitude2 = math.sqrt(dir2.x**2 + dir2.y**2 + dir2.z**2)
    angle = math.acos(dot_product / (magnitude1 * magnitude2))
    return angle
# Corrected function
def update_player_movement(player: PlayerInGame, targetPlayer: PlayerInGame, speed: float):
    # POSITION ARE UNITY TYPE X RIGHT, Y UP, Z FORWARD
    # ROTATION ARE UNITY TYPE X RIGHT, Y UP, Z FORWARD
    player_position = Vector3(player.position_x, player.position_y, player.position_z)
    target_position = Vector3(targetPlayer.position_x, targetPlayer.position_y, targetPlayer.position_z)
    
    player_forward_position = player_position.copy()
    
    
    target_direction = Vector3(target_position.x - player_position.x,0, target_position.z - player_position.z)
    target_direction.normalize()
    
    print (f"PLAYER POSITION: {player_position}")
    print (f"TARGET POSITION: {target_position}")
    
    target_angle_trigono = math.degrees(math.atan2(target_direction.z, target_direction.x))
    if target_angle_trigono > 180:
        target_angle_trigono -= 360
    elif target_angle_trigono < -180:
        target_angle_trigono += 360
    print(f"Target TRIGONO Angle TAN: {target_angle_trigono}")
    print (f"PLAYER ROTATION: {player.xtozangle}")
    
    
    float_angle_delta = player.xtozangle - target_angle_trigono
    
    print (f"ANGLE DELTA: {float_angle_delta}")
    
    
    if float_angle_delta > 0:
        print("Turn Right")
        push_joystick_value(0.3, 1, 0, 0)
    else:
        print("Turn Left")
        push_joystick_value(-0.3, 1, 0, 0)

    
# Example usage

def get_distance_between(player1: PlayerInGame, player2: PlayerInGame):
    return math.sqrt((player1.position_x - player2.position_x)**2 + (player1.position_y - player2.position_y)**2 + (player1.position_z - player2.position_z)**2)

    
def your_ai_code():
    print("Your AI code here")
    while True:
        
        bool_quick_test= False
        if bool_quick_test:
            display_all_players()
            player :PlayerInGame= get_player(int_player_index)
            print(f"First CC player: {int_player_index} - Team: {player.team_id} - Position: ({player.position_x}, {player.position_y}, {player.position_z}) - Rotation: ({player.rotation_euler_x}, {player.rotation_euler_y}, {player.rotation_euler_z}) - Size: {player.size} - Timestamp: {player.timestamp}")
            time.sleep(1)
            push(1899000000,0)
            time.sleep(1)
            push(1855000000,0)
            time.sleep(1)
            
            for i in range(10):
                time.sleep(1)
                go_up_start()
                
                time.sleep(1)
                go_up_stop()
                attack()
            for i in range(10):
                time.sleep(1)
                go_left_start()
                time.sleep(1)
                go_left_start()
                attack()
                
        bool_code_testing = False
        if bool_code_testing:
            print ("Move Up")
            go_up_start()
            time.sleep(2)
            attack()
            go_up_stop()
            time.sleep(2)
            attack()
            
            
            print ("Move Down")
            go_down_start()
            time.sleep(2)
            attack()
            go_down_stop()
            time.sleep(2)
            attack()
            
            
            print ("Move Right")
            go_right_start()
            time.sleep(2)
            attack()
            go_right_stop()
            time.sleep(2)
            attack()
            
            
            print ("Move Left")
            go_left_start()
            time.sleep(2)
            attack()
            go_left_stop()
            time.sleep(2)
            attack()
            
            
            print ("Move Up")
            push_joystick_value(0,1,0,0)
            time.sleep(2)
            attack()
            push_joystick_value(0,0,0,0)
            time.sleep(2)
            attack()
            
            
            print ("Move Down")
            push_joystick_value(0,-1,0,0)
            time.sleep(2)
            attack()
            push_joystick_value(0,-1,0,0)
            time.sleep(2)
            attack()
            
            
            print ("Move Right")
            push_joystick_value(1,0,0,0)
            time.sleep(2)
            attack()
            push_joystick_value(1,0,0,0)
            time.sleep(2)
            attack()
            
            
            print ("Move Left")
            push_joystick_value(-1,0,0,0)
            time.sleep(2)
            attack()
            push_joystick_value(-1,0,0,0)
            time.sleep(2)
            attack()
            
            
            
        
        bool_find_closest_player = True
        if bool_find_closest_player:
            
            time.sleep(0.2)
            attack()
            player = get_player(int_player_index)
            print("TRIGONOANGLE:",player.xtozangle)
            distance_near = float('inf')
            player_near = None
            for player_id_loop, player_in_loop in player_dictionnary.items():
                if int_player_index == int(player_id_loop):
                    continue
                if player_in_loop.team_id == player.team_id:
                    continue
                
                player_near = player_in_loop
                distance = get_distance_between(player, player_in_loop)
                if distance < distance_near:
                    distance_near = distance
                    player_near = player_in_loop
            
            print(".")
            if player_near is not None:
                print(f">> Distance to player {player.player_id} {player_near.player_id}: {distance_near}")
                update_player_movement(player, player_near,0.5)
            
        
    

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    
    udp_thread = threading.Thread(target=udp_listener, args=(m_listened_port,))
    udp_thread.start()
    
    ai_task = loop.create_task(asyncio.to_thread(your_ai_code))
    
    try:
        loop.run_until_complete(asyncio.to_thread(console_thread))
    finally:
        loop.run_until_complete(ai_task)
        loop.close()