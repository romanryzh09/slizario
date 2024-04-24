import socket
import pygame

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect(('localhost', 10000))

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Бактерии')

run = True
while run:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            run = False
    sock.send('Привет'.encode())

    data = sock.recv(1024).decode()
    print('Получил:', data)










pygame.quit()
