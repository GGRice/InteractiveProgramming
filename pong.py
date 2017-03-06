"""
Created on Mon February 27, 2017

author: Amon Millner, building upon examples built by previous
SoftDes instructors, such as Paul Ruvolo and Ben Hill.

"""

import pygame
import time
import math
import random

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

class PongModel:
    """ Encodes the game state """
    def __init__(self):
        self.paddle1 = Paddle((255, 255, 255), 20, 100, 200, 450)
        self.paddle2 = Paddle((255, 255, 255), 20, 100, 200, 10)
        self.ball = Ball()




class Paddle:
    """ Encodes the state of the paddle in the game """
    def __init__(self, color, height, width, x, y):
        self.color = color
        self.height = height
        self.width = width
        self.x = x
        self.y = y

class Ball(object):
    def __init__(self):
        self.radius = 10
        self.reset()

    def move(self):
        self.y += self.dy
        self.x += self.dx
        if self.y <= 0:
            self.angle = -self.angle
            self.dy = int(self.step*math.sin(self.angle))
            self.dx = int(self.step*math.cos(self.angle))
        elif self.y >= 480:
            self.angle = -self.angle
            self.dy = int(self.step*math.sin(self.angle))
            self.dx = int(self.step*math.cos(self.angle))
        elif self.x <= 0:
            self.angle = math.pi - self.angle
            self.dy = int(self.step*math.sin(self.angle))
            self.dx = int(self.step*math.cos(self.angle))
        elif self.x >= 640:
            self.angle = math.pi - self.angle
            self.dy = int(self.step*math.sin(self.angle))
            self.dx = int(self.step*math.cos(self.angle))


    def reset(self):
        self.x = 320
        self.y = 240
        self.angle = math.radians(random.randint(0,360))
        self.step = 10
        self.dy = int(self.step*math.sin(self.angle))
        self.dx = int(self.step*math.cos(self.angle))

    def contains_pt(self, pt):
        return (self.x - pt[0]) ** 2 + (self.y - pt[1]) ** 2 < self.radius ** 2

class BallView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        model = self.model
        pygame.draw.circle(surface, BLUE, (model.x, int(model.y)), model.radius)

class PyGameWindowView:
    """ A view of brick breaker rendered in a Pygame window """
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen

    def draw(self):
        self.screen.fill(pygame.Color(0, 0, 0))

        pygame.draw.rect(self.screen, pygame.Color(
                         self.model.paddle1.color[0],
                         self.model.paddle1.color[1],
                         self.model.paddle1.color[2]), pygame.Rect(
                         self.model.paddle1.x, self.model.paddle1.y,
                         self.model.paddle1.width, self.model.paddle1.height))

        pygame.draw.rect(self.screen, pygame.Color(
                         self.model.paddle2.color[0],
                         self.model.paddle2.color[1],
                         self.model.paddle2.color[2]), pygame.Rect(
                         self.model.paddle2.x, self.model.paddle2.y,
                         self.model.paddle2.width, self.model.paddle2.height))
        BallView(self.model.ball).draw(self.screen)
        pygame.display.update()


class PyGameKeyController:
    def __init__(self, model):
        self.model = model

    def handle_key_event(self, event):
        if event.key == pygame.K_LEFT and self.model.paddle1.x > 0:
            self.model.paddle1.x = self.model.paddle1.x - self.model.paddle1.width/2.0
        elif event.key == pygame.K_RIGHT and self.model.paddle1.x < size[0]-self.model.paddle1.width:
            self.model.paddle1.x = self.model.paddle1.x + self.model.paddle1.width/2.0
        elif event.key == pygame.K_a and self.model.paddle2.x > 0:
            self.model.paddle2.x = self.model.paddle2.x - self.model.paddle2.width/2.0
        elif event.key == pygame.K_d and self.model.paddle2.x < size[0]-self.model.paddle2.width:
            self.model.paddle2.x = self.model.paddle2.x + self.model.paddle2.width/2.0


if __name__ == '__main__':
    pygame.init()

    size = (640, 480)
    screen = pygame.display.set_mode(size)

    model = PongModel()
    view = PyGameWindowView(model, screen)
    controller = PyGameKeyController(model)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                controller.handle_key_event(event)
        view.draw()
        model.ball.move()
        time.sleep(.001)

    pygame.quit()