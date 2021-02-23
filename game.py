import pygame
import sqlite3
import random
import time


def welcome():
    pygame.init()
    size = 750, 500
    screen = pygame.display.set_mode(size)
    screen.fill((106, 193, 255))

    text = 'Здесь мы можем поотгадывать загадки!'
    text2 = 'Сыграем?'
    blitlines(screen, text, pygame.font.SysFont('serif', 43), (255, 255, 255), 10, 200)
    blitlines(screen, text2, pygame.font.SysFont('serif', 45), (255, 255, 255), 280, 240)

    pygame.display.flip()
    in_main_menu = True

    while in_main_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_main_menu = False
                pygame.display.quit()
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return Board()


def get_riddle():
    con = sqlite3.connect('riddle.db')
    cur = con.cursor()
    query = "SELECT id,answer, text FROM riddle ORDER BY RANDOM() LIMIT 1;"
    res = cur.execute(query).fetchone()
    con.commit()
    con.close()

    id_r, answer, text = res
    riddle = {'text': text, 'answer': answer.upper()}

    return riddle


def play_again(board):
    board.screen.fill((106, 193, 255))
    pygame.display.flip()
    time.sleep(0.5)
    text = pygame.font.SysFont('serif', 55).render('Молодец! Сыграем еще раз?', True, (0, 0, 0))
    textx = 750 / 2 - text.get_width() / 2
    texty = 500 / 2 - text.get_height() / 2

    textx_size = text.get_width()
    texty_size = text.get_height()

    pygame.draw.rect(board.screen, (255, 255, 255), ((textx - 5, texty - 5),
                                                     (textx_size + 10, texty_size +
                                                      10)))

    board.screen.blit(text, (750 / 2 - text.get_width() / 2,
                             500 / 2 - text.get_height() / 2))

    pygame.display.flip()
    in_main_menu = True

    while in_main_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_main_menu = False
                pygame.display.quit()
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if textx - 5 <= x <= textx + textx_size + 5:
                    if texty - 5 <= y <= texty + texty_size + 5:
                        return Board()


def blitlines(surf, text, renderer, color, x, y):
    h = renderer.get_height()
    lines = text.split('\\n')

    for i, ll in enumerate(lines):
        txt_surface = renderer.render(ll, True, color)
        surf.blit(txt_surface, (x, y + (i * h)))


class Board:
    def __init__(self):
        pygame.init()

        size = 750, 500
        self.screen = pygame.display.set_mode(size)

        self.content = get_riddle()
        self.answer = {}
        self.font = pygame.font.SysFont('Arial', 25)
        self.width = len(self.content['text'])
        self.words = self.content['answer']
        self.height = 1
        self.all_rects = []
        self.counter = 1

        self.letters = random.sample(self.words, len(self.words))
        self.set_view(17, 400, 50)

        self.left = 0
        self.top = 0
        self.cell = 0

        self.userfont = pygame.font.Font(None, 40)
        rd = str(self.content['text'])
        blitlines(self.screen, rd, self.userfont, (255, 255, 255), 30, 30)

    def set_view(self, left, top, cell):
        self.left = left
        self.top = top - 50
        self.cell = cell
        self.prepare()

    def prepare(self):
        x = 0
        for _ in self.letters:
            rect = pygame.Rect(x * self.cell + self.left, self.cell + self.top, self.cell, self.cell)
            x = x + 1
            self.all_rects.append([rect, None, 'q'])

    def render(self, screen, color):
        i = 0
        for letter in self.letters:
            pygame.draw.rect(screen, pygame.Color(color), self.all_rects[i][0], 1)
            x, y, w, h = self.all_rects[i][0]
            screen.blit(self.font.render(letter, True, (0, 0, 0)),
                        (x + 20, y + 6))
            i = i + 1


board = welcome()
color = 'black'
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for idx, rect in enumerate(board.all_rects):
                x, y, w, h = rect[0]
                if rect[0].collidepoint(event.pos):
                    if board.all_rects[idx][2] == 'q':
                        board.all_rects[idx][0] = pygame.Rect(50 * board.counter, y - 100, w, h)
                        board.all_rects[idx][1] = pygame.Rect(x, y, w, h)
                        board.all_rects[idx][2] = 'a'
                        board.counter += 1
                        board.answer.update({idx: board.letters[idx]})

                    else:
                        color = 'black'
                        if x == 50 * (board.counter - 1):
                            board.all_rects[idx][0] = pygame.Rect(board.all_rects[idx][1])
                            board.all_rects[idx][1] = None
                            board.all_rects[idx][2] = 'q'
                            board.counter -= 1
                            del board.answer[idx]

                    if len(board.answer.values()) == len(board.words):
                        if ''.join(board.answer.values()) == board.words:
                            # time.sleep(0.5)
                            board = play_again(board)
                        else:
                            color = 'red'

        bg = pygame.image.load("background.png")
        board.screen.blit(bg, (0, 0))
        board.render(board.screen, color)
        userfont = pygame.font.Font(None, 40)
        rd = str(board.content['text'])
        blitlines(board.screen, rd, userfont, (0, 0, 0), 15, 20)

    pygame.display.flip()
