import socket
import time
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import pygame

pygame.init()
WIDTH_ROOM, HEIGHT_ROOM = 4000, 4000
WIDTH_SERVER, HEIGHT_SERVER = 300, 300
FPS = 100

screen = pygame.display.set_mode((WIDTH_SERVER, HEIGHT_SERVER))
pygame.display.set_caption("Сервер")
clock = pygame.time.Clock()

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

main_socket.bind(('localhost', 10000))

main_socket.setblocking(False)

main_socket.listen(5)

DATABASE_URL = "postgresql+psycopg2://postgres:11062009Ryzhinkov@localhost/bacteria"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()
s = Session()


class Player(Base):
    __tablename__ = 'gamers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    address = Column(String)
    x = Column(Integer, default=500)
    y = Column(Integer, default=500)
    size = Column(Integer, default=50)
    errors = Column(Integer, default=0)
    abs_speed = Column(Integer, default=1)
    speed_x = Column(Integer, default=0)
    speed_y = Column(Integer, default=0)

    def __init__(self, name, address):
        self.name = name
        self.address = address


class LocalPlayer:
    def __init__(self, id, name, sock, addr):
        self.id = id
        self.db: Player = s.get(Player, self.id)
        self.sock = sock
        self.name = name
        self.address = addr
        self.x = 500
        self.y = 500
        self.size = 50
        self.errors = 0
        self.abs_speed = 1
        self.speed_x = 0
        self.speed_y = 0


print('Сокет создался')

Base.metadata.create_all(engine)

players = {}
server_works = True
while server_works:
    clock.tick(FPS)
    try:
        new_socket, addr = main_socket.accept()
        print('Подключился', addr)
        new_socket.setblocking(False)
        player = Player("Имя", addr)
        s.merge(player)
        s.commit()
        addr = f'({addr[0]}, {addr[1]})'
        data = s.query(Player).filter(Player.address == addr)
        for user in data:
            player = LocalPlayer(user.id, "Имя", new_socket, addr)
            players[user.id] = player

    except BlockingIOError:
        pass

    for id in list(players):
        try:
            data = players[id].sock.recv(1024).decode()
            print(f'Получил {data}')
            # sock.send('Игра'.encode())
        except Exception as e:
            pass
            # players.remove(sock)
            # sock.close()
            # print('Сокет закрыт')
            # print(e)

    for id in list(players):
        try:
            players[id].sock.send('Игра'.encode())
        except Exception as e:
            players[id].sock.close()
            del players[id]
            s.query(Player).filter(Player.id == id).delete()
            s.commit()
            print('Сокет закрыт(')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            server_works = False

pygame.quit()
main_socket.close()
s.query(Player).delete()
s.commit()
