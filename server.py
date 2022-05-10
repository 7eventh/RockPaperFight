import socket
from _thread import *
import pickle
from game import Game
                            # Home          # School 
server = "10.154.196.62"   #"192.168.1.75"  #"10.154.196.89" 
port = 5556

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2) 
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0

player_champions = ["RangeChampionOne", "MeleeChampionOne", "MeleeChampionTwo", "MeleeChampionThree", "EnemyMeleeChampionOne"]
moves = ["Rock", "Paper", "Scissors", "rock", "paper", "scissors", "ROCK", "PAPER", "SCISSORS"]
data_types = ["reset", "get"]

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096*4).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    if data != "get" and data in moves:
                        game.play(p, data)
                    if data not in data_types and data in player_champions: 
                        game.set_champions(p, data) 
                    


                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId)) 
    
