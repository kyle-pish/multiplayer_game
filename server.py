import socket
from _thread import *
from player import Player
import pickle
from powerup import PowerUp

# Server setup and player initialization
#server = "127.0.0.1"
server = "10.6.8.167"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(8)  # Increase the number of clients that the server can listen to
print("Waiting for connections, Server Started")

# Dictionary used to store player objects for 2 different gamelobbies
players = {
    0 : [
        Player(0, 50, 30, 30, (255, 0, 0)),
        Player(970, 770, 30, 30, (0, 0, 255)),
        Player(0, 770, 30, 30, (0, 255, 0)),
        Player(970, 50, 30, 30, (255, 255, 0))
    ],
    1 : [
        Player(0, 50, 30, 30, (255, 0, 0)),
        Player(970, 770, 30, 30, (0, 0, 255)),
        Player(0, 770, 30, 30, (0, 255, 0)),
        Player(970, 50, 30, 30, (255, 255, 0))
    ]
}

def all_players_ready(players_list):
    # Function to check if all players are ready
    for player in players_list:
        if not player.ready:
            return False
    return True

def check_win_condition(players_list):
    # Check if the current player has won
    for player in players_list:
        if player.victory == True:
            print(f"Player {player} won")
            return True  # Other players still alive, no win yet

power_ups = []
def initialize_powerups():
    global power_ups
    power_ups = [PowerUp(500, 85, 'speed_boost'), 
                 PowerUp(500, 750, 'speed_boost'),
                 PowerUp(25, 425, 'speed_boost'), 
                 PowerUp(975, 425, 'speed_boost'),
                 PowerUp(375, 425, 'triple_shot'),
                 PowerUp(625, 425, 'triple_shot'),
                 PowerUp(325, 325, 'med_pack'),
                 PowerUp(325, 525, 'med_pack'),
                 PowerUp(675, 325, 'med_pack'),
                 PowerUp(675, 525, 'med_pack'),
                 PowerUp(500, 375, 'shield'),
                 PowerUp(500, 475, 'shield')
                 ]

def reset_game_state(game_id):
    # Reset all player states to default/starting state
    for player in players[game_id]:
        player.reset()

def send_power_ups():
    return power_ups

def threaded_client(conn, player, game_id):
    player_id = player  # Assign an ID to the player
   
    # Based on the players game lobby and player ID, send them their player info
    if game_id == 0:
        print((player_id, players[game_id][player_id]))
        print(f"Player ID: {player_id}")
        print(f"Player Object: {players[game_id][player_id]}")
        print(f"Game Lobby ID: {game_id}")
        conn.send(pickle.dumps((player_id, players[game_id][player_id])))
    else:
        print(f"Player ID: {player_id - 4}")
        print(f"Player Object: {players[game_id][player_id - 4]}")
        print(f"Game Lobby ID: {game_id}")
        conn.send(pickle.dumps((player_id-4, players[game_id][player_id - 4])))

    reply = ""
    while True:
        try:
            # Recieve data from client and split into flag/msgtype and msg_data
            data = pickle.loads(conn.recv(2048))
            msgtype, msg_data = data

            if not data:
                print("Disconnected")
                break

            # Recieving data from and sending to players in lobby 0
            if game_id == 0:
                if msgtype == 'PLAYER_DATA':
                    players[game_id][player_id] = msg_data
                    print(msg_data)

                elif msgtype == 'PLAYER_READY':
                    print(f"Player {player_id} is ready")
                    reply = True

                elif msgtype == 'READY_CHECK':
                    reply = (all_players_ready(msg_data))

                elif msgtype == 'GET_PLAYERS':
                    reply = players[game_id]

                elif msgtype == 'INITIALIZE_POWERUPS':
                    initialize_powerups()

                elif msgtype == 'GET_POWER_UPS':
                    reply = send_power_ups()

                elif msgtype == 'PLAYER_COLLECTED_POWER_UP':
                    power_up_index = msg_data
                    power_up = power_ups[power_up_index]
                    power_ups.remove(power_up)
                    reply = send_power_ups()

                elif msgtype == 'PLAYER_WON':
                    reply = (check_win_condition(msg_data))
                    print(reply)
                    currentPlayer = 0  

                elif msgtype == 'RESET_GAME_STATE':
                    reset_game_state(game_id)

            # Recieving data from and sending to players in lobby 0
            elif game_id == 1:
                if msgtype == 'PLAYER_DATA':
                    players[game_id][player_id - 4] = msg_data
                    print(msg_data)

                elif msgtype == 'PLAYER_READY':
                    print(f"Player {player_id - 4} is ready")
                    reply = True

                elif msgtype == 'READY_CHECK':
                    reply = (all_players_ready(msg_data))

                elif msgtype == 'GET_PLAYERS':
                    reply = players[game_id]

                elif msgtype == 'INITIALIZE_POWERUPS':
                    initialize_powerups()

                elif msgtype == 'GET_POWER_UPS':
                    reply = send_power_ups()

                elif msgtype == 'PLAYER_COLLECTED_POWER_UP':
                    power_up_index = msg_data
                    power_up = power_ups[power_up_index]
                    power_ups.remove(power_up)
                    reply = send_power_ups()

                elif msgtype == 'PLAYER_WON':                  
                    reply = (check_win_condition(msg_data))
                    print(reply)
                    currentPlayer = 0

                elif msgtype == 'RESET_GAME_STATE':
                    reset_game_state(game_id)
            
            conn.sendall(pickle.dumps(reply))  # Send updated player information to all clients
        except:
            break

    print("Lost connection")
    conn.close()

game_id = None
currentPlayer = 0
while True:
    conn, addr = s.accept()  # Accept incoming connections
    print("Connected to:", addr)

    # Assign game lobby ID
    if currentPlayer < 4:
        game_id = 0
    else:
        game_id = 1

    start_new_thread(threaded_client, (conn, currentPlayer, game_id)) # Start new threaded client
    currentPlayer += 1
