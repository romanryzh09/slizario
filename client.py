import socket
import pygame
import math
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox


def scroll(event):
    global color
    color = combo.get()
    style.configure('TCombobox', fieldbackground=color, background='white')


def login():
    global name
    name = row.get()
    if name and color:
        root.destroy()
        root.quit()
    else:
        tk.messagebox.showerror('Ошибка', 'Ты не выбрал цвет или не ввел имя!')


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect(('localhost', 10000))


pygame.init()

WIDTH = 800
HEIGHT = 600

CC = (WIDTH // 2, HEIGHT // 2)

old = (0, 0)

radius = 50

font = pygame.font.SysFont('calibri', 10)
nickname = font.render('Litwiz1337', 1, (0, 0, 0))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Бактерии')

colors = ['Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato', 'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown',
          'DarkOrange', 'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow', 'YellowGreen', 'GreenYellow',
          'Chartreuse', 'LawnGreen', 'Green', 'Lime', 'Lime Green', 'SpringGreen', 'MediumSpringGreen', 'Turquoise',
          'LightSeaGreen', 'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 'Cyan', 'Dark Turquoise', 'DeepSkyBlue',
          'DodgerBlue', 'RoyalBlue', 'Navy', 'DarkBlue', 'MediumBlue']

name = ""
color = ""

root = tk.Tk()
root.title('Логин')
root.geometry("300x200")

style = ttk.Style()
style.theme_use('classic')

name_label = tk.Label(root, text='Введите свой никнейм:')
name_label.pack()
row = tk.Entry(root, width=30, justify='center')
row.pack()
color_label = tk.Label(root, text='Выбери цвет:')
color_label.pack()
combo = ttk.Combobox(root, values=colors, textvariable=color)
combo.bind("<<ComboboxSelected>>", scroll)
combo.pack()
name_btn = tk.Button(root, text='Зайти в игру', command=login)
name_btn.pack()

sock.send(('color:<' + name + ',' + color + '>').encode())
root.mainloop()

run = True
while run:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            run = False
    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        vector = pos[0] - CC[0], pos[1] - CC[1]

        lenv = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        vector = vector[0] / lenv, vector[1] / lenv

        if lenv <= radius:
            vector = 0, 0

        if vector != old:
            old = vector
            msg = f"<{vector[0]},{vector[1]}>\n"
            sock.send(msg.encode())

    # data = sock.recv(1024).decode()
    # print('Получил:', data)

    screen.fill('gray')
    pygame.draw.circle(screen, color, CC, radius)
    screen.blit(nickname, CC)
    pygame.display.update()

pygame.quit()

