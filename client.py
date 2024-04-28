import socket
import pygame

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect(('localhost', 10000))

pygame.init()

WIDTH = 800
HEIGHT = 600

CC = (WIDTH // 2, HEIGHT // 2)

old = (0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Бактерии')

run = True
while run:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            run = False
    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        vector = pos[0] - CC[0], pos[1] - CC[1]
        if vector != old:
            old = vector
            msg = f"<{vector[0]}, {vector[1]}>"
            sock.send(msg.encode())

    data = sock.recv(1024).decode()
    print('Получил:', data)










pygame.quit()
