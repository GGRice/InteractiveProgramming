"""
Created on Mon February 27, 2017

author: Gretchen Rice and Nina Tchirkova

"""

import pygame
import time
import math
import random


BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
win_score = 5

class PongModel:
    """ Encodes the game state """
    def __init__(self):
        self.paddle1 = Paddle((255, 255, 255), 20, 100, 200, 450)
        self.paddle2 = Paddle((255, 255, 255), 20, 100, 200, 10)
        self.ball = Ball()
        self.score = Score(0, 0)

class Score:
    """
        Updates, keeps, and returns score.
    """
    def __init__(self, p1_score, p2_score):
        self.p1_score = p1_score
        self.p2_score = p2_score

    def reset_score():
        p1_score = 0
        p2_score = 0

    def update_score(self, player, ball):
        print('here!')
        print(self.p1_score, self.p2_score)
        if player == 1:
            self.p1_score += 1

        else:
            self.p2_score += 1

        ball.reset()

        print(self.p1_score, self.p2_score)

        # if p >= win_score:
        #    self.reset_score

    def print_score(self):
        print(self.p1_score, self.p2_score)




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

    def move(self, paddle1, paddle2): # ,ms):
        self.y += self.dy
        self.x += self.dx

        if self.y >= paddle1.y and self.y <= paddle1.y + paddle1.height and self.x >= paddle1.x and self.x <= paddle1.x + paddle1.width:
            self.angle = -self.angle
            self.dy = int(self.step*math.sin(self.angle))
            self.dx = int(self.step*math.cos(self.angle))
        elif self.y <= paddle2.y + paddle2.height and self.y >= paddle2.y and self.x >= paddle2.x and self.x <= paddle2.x + paddle2.width:
            self.angle = -self.angle
            self.dy = int(self.step*math.sin(self.angle))
            self.dx = int(self.step*math.cos(self.angle))
        elif self.y <= 0:
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

        rand = random.randint(1,4)
        if rand == 1:
            self.angle = math.radians(random.randint(15, 75))
        elif rand ==2:
            self.angle = math.radians(random.randint(105, 165))
        elif rand == 3:
            self.angle = math.radians(random.randint(195, 255))
        else:
            self.angle = math.radians(random.randint(285, 345))
        self.step = 10

        self.dy = int(self.step*math.sin(self.angle))
        self.dx = int(self.step*math.cos(self.angle))

    def contains_pt(self, pt):
        return (self.x - pt[0]) ** 2 + (self.y - pt[1]) ** 2 < self.radius ** 2

    def hits_bad_wall(self):
        if self.y <= 0 or self.y >= 480:
            return True
        return False

    def player_score(self):
        if self.y <= 0:
            return 1
        elif self.y >= 480:
            return 2
        else:
            return 0



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
    # clock = pygame.time.Clock()

    size = (640, 480)
    screen = pygame.display.set_mode(size)

    model = PongModel()
    view = PyGameWindowView(model, screen)
    controller = PyGameKeyController(model)

    running = True

    # ms = clock.tick()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                controller.handle_key_event(event)

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT] != 0 and model.paddle1.x > 0:
            model.paddle1.x = model.paddle1.x - model.paddle1.width/2.0

        if keys_pressed[pygame.K_RIGHT] != 0 and model.paddle1.x < size[0]-model.paddle1.width:
            model.paddle1.x = model.paddle1.x + model.paddle1.width/2.0

        if keys_pressed[pygame.K_a] != 0 and model.paddle2.x > 0:
            model.paddle2.x = model.paddle2.x - model.paddle2.width/2.0

        if keys_pressed[pygame.K_d] != 0 and model.paddle2.x < size[0]-model.paddle2.width:
            model.paddle2.x = model.paddle2.x + model.paddle2.width/2.0

        view.draw()
        model.ball.move(model.paddle1, model.paddle2) # , ms)

        time.sleep(.001)
        if model.ball.hits_bad_wall():
            print('update')
            model.score.update_score(model.ball.player_score(), model.ball)
            time.sleep(1)
        model.score.print_score()
        # ms = clock.tick()

    pygame.quit()
