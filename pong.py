"""
Created on Mon February 27, 2017

author: Gretchen Rice and Nina Tchirkova

This program creates a version of pong. It is a two player game where players
control paddles and try to hit a ball past the other player's paddle to score
points. 
"""

import pygame
import time
import math
import random


BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
SKY = (102, 255, 255)

win_score = 3 #score needed to win, can change fo longer/shorter games
ball_step = 1 #changes ball speed, higher numbers make it faster, different for different computers
paddle_speed = 45.0 #changes paddle speed, higher numbers make them slower, different for different computers

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

    def reset_score(self):
        self.p1_score = 0
        self.p2_score = 0

    def update_score(self, player, ball):
        if player == 1:
            self.p1_score += 1

        else:
            self.p2_score += 1

        # if someone wins, will reset completely
        if self.p1_score >= win_score or self.p2_score >= win_score:
            self.winner()

        ball.reset()


    def winner(self):
        """
            Determines which player wins and returns int for player
        """
        if self.p1_score >= win_score:
            return 1
        elif self.p2_score >= win_score:
            return 2


    def print_score(self):
        """
            Prints score to terminal
        """
        print(self.p1_score, self.p2_score)



class Paddle:
    """
        Encodes the state of the paddle in the game
    """
    def __init__(self, color, height, width, x, y):
        self.color = color
        self.height = height
        self.width = width
        self.x = x
        self.y = y

class Ball(object):
    """
        Creates ball, includes move class, reset, contains point, and methods to determine which player
        scores when bll hits top or bottom
    """
    def __init__(self):
        self.radius = 10
        self.reset()

    def move(self, paddle1, paddle2):
        """
            Determines angle at which ball will bounce
        """
        self.ydouble += self.dy
        self.xdouble += self.dx

        # handles paddle hit
        if self.ydouble >= paddle1.y and self.y <= paddle1.y + paddle1.height and self.x >= paddle1.x and self.x <= paddle1.x + paddle1.width:
            self.angle = -self.angle
            self.dy = self.step*math.sin(self.angle)
            self.dx = self.step*math.cos(self.angle)
        elif self.ydouble <= paddle2.y + paddle2.height and self.y >= paddle2.y and self.x >= paddle2.x and self.x <= paddle2.x + paddle2.width:
            self.angle = -self.angle
            self.dy = self.step*math.sin(self.angle)
            self.dx = self.step*math.cos(self.angle)

        # handles top/bottom hit(not used in this case since ball resets for score)
        elif self.ydouble <= 0:
            self.angle = -self.angle
            self.dy = self.step*math.sin(self.angle)
            self.dx = self.step*math.cos(self.angle)
        elif self.ydouble >= 480:
            self.angle = -self.angle
            self.dy = self.step*math.sin(self.angle)
            self.dx = self.step*math.cos(self.angle)

        #handles side hit
        elif self.xdouble <= 0:
            self.angle = math.pi - self.angle
            self.dy = self.step*math.sin(self.angle)
            self.dx = self.step*math.cos(self.angle)
        elif self.xdouble >= 640:
            self.angle = math.pi - self.angle
            self.dy = self.step*math.sin(self.angle)
            self.dx = self.step*math.cos(self.angle)

        self.x = int(self.xdouble)
        self.y = int(self.ydouble)


    def reset(self):
        self.xdouble = 320.0
        self.ydouble = 240.0
        self.x = 320
        self.y = 240

        # Determines what angle ball will start going
        rand = random.randint(1,4)
        if rand == 1:
            self.angle = math.radians(random.randint(15, 75))
        elif rand ==2:
            self.angle = math.radians(random.randint(105, 165))
        elif rand == 3:
            self.angle = math.radians(random.randint(195, 255))
        else:
            self.angle = math.radians(random.randint(285, 345))

        self.step = ball_step

        self.dy = self.step*math.sin(self.angle)
        self.dx = self.step*math.cos(self.angle)

    def contains_pt(self, pt):
        """
            Checks if the ball contains a point
        """
        return (self.x - pt[0]) ** 2 + (self.y - pt[1]) ** 2 < self.radius ** 2

    def hits_bad_wall(self):
        """
            Checks if ball hits top or bottom
        """
        if self.y <= 0 or self.y >= 480:
            return True
        return False

    def player_score(self):
        """
            Determines which player scores depending on if hit top or bottom
        """
        if self.y <= 0:
            return 1
        elif self.y >= 480:
            return 2
        else:
            return 0



class BallView(object):
    """
        Has draw function so puts ball on screen
    """
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        model = self.model
        pygame.draw.circle(surface, BLUE, (model.x, int(model.y)), model.radius)

class StartWindowView:
    """
        Creates a Welcome page for game
    """
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen

    def text_objects(self,text, font):
        textSurface = font.render(text, True, WHITE)
        return textSurface, textSurface.get_rect()

    def draw(self):
        self.screen.fill(pygame.Color(0, 0, 0))
        pygame.font.init()
        myfont = pygame.font.Font('freesansbold.ttf', 30)
        mylargefont = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = self.text_objects('Welcome to Pro Pong', mylargefont)
        TextSurf1, TextRect1 = self.text_objects('Player1: (bottom) arrow keys', myfont)
        TextSurf2, TextRect2 = self.text_objects('Player2: (top) A move left, D move right', myfont)
        TextSurf3, TextRect3 = self.text_objects('Press Space Bar to Start', mylargefont)
        TextRect.center = ((640/2),(480/4))
        TextRect1.center = ((640/2),(480/2 - 30))
        TextRect2.center = ((640/2),(480/2 + 30))
        TextRect3.center = ((640/2),(480/4 * 3))
        screen.blit(TextSurf, TextRect)
        screen.blit(TextSurf1, TextRect1)
        screen.blit(TextSurf2, TextRect2)
        screen.blit(TextSurf3, TextRect3)
        pygame.display.update()


class EndWindowView:
    """
        Creates end page to show everytime someone wins
    """
    def __init__(self, model, screen, player):
        self.model = model
        self.screen = screen
        self.player = player

    def text_objects(self,text, font):
        textSurface = font.render(text, True, WHITE)
        return textSurface, textSurface.get_rect()

    def draw(self):
        self.screen.fill(pygame.Color(0, 0, 0))
        pygame.font.init()
        mylargefont = pygame.font.Font('freesansbold.ttf', 50)

        #prints proper message depending who won
        if self.player == 1:
            TextSurf, TextRect = self.text_objects('Player 1 Wins!', mylargefont)
        else:
            TextSurf, TextRect = self.text_objects('Player 2 Wins!', mylargefont)

        TextSurf2, TextRect2 = self.text_objects('Press Space Bar to Start', mylargefont)

        TextRect.center = ((640/2),(480/4))
        TextRect2.center = ((640/2),(480/4 * 3))
        screen.blit(TextSurf, TextRect)
        screen.blit(TextSurf2, TextRect2)

        pygame.display.update()



class PyGameWindowView:
    """
        A view of brick breaker rendered in a Pygame window
    """
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
        scoretext1 = myfont.render("PLAYER 1 SCORE: "+str(model.score.p1_score), 1, SKY)
        screen.blit(scoretext1, (5, 450))
        scoretext1 = myfont.render("PLAYER 2 SCORE: "+str(model.score.p2_score), 1, SKY)
        screen.blit(scoretext1, (5, 10))
        pygame.display.update()


class PyGameKeyController:
    """
        Sets up events for when key is first pressed to move paddle
    """
    def __init__(self, model):
        self.model = model

    # the 45 can be changed to create
    def handle_key_event(self, event):
        if event.key == pygame.K_LEFT and self.model.paddle1.x > 0:
            self.model.paddle1.x = self.model.paddle1.x - self.model.paddle1.width/paddle_speed
        elif event.key == pygame.K_RIGHT and self.model.paddle1.x < size[0]-self.model.paddle1.width:
            self.model.paddle1.x = self.model.paddle1.x + self.model.paddle1.width/paddle_speed
        elif event.key == pygame.K_a and self.model.paddle2.x > 0:
            self.model.paddle2.x = self.model.paddle2.x - self.model.paddle2.width/paddle_speed
        elif event.key == pygame.K_d and self.model.paddle2.x < size[0]-self.model.paddle2.width:
            self.model.paddle2.x = self.model.paddle2.x + self.model.paddle2.width/paddle_speed


if __name__ == '__main__':
    pygame.init()

    myfont = pygame.font.SysFont("monospace", 20)

    size = (640, 480)
    screen = pygame.display.set_mode(size)

    model = PongModel()
    start_view = StartWindowView(model,screen)
    view = PyGameWindowView(model, screen)
    controller = PyGameKeyController(model)

    running = True
    start = True
    end = False
    pygame.display.set_caption('Pro Pong')

    # opens Welcome window and starts game only when spacebar pressed
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start = False


        start_view.draw()

    index = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                controller.handle_key_event(event)

        # handles events of keys being pressed to move paddles
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT] != 0 and model.paddle1.x > 0:
            model.paddle1.x = model.paddle1.x - model.paddle1.width/paddle_speed

        if keys_pressed[pygame.K_RIGHT] != 0 and model.paddle1.x < size[0]-model.paddle1.width:
            model.paddle1.x = model.paddle1.x + model.paddle1.width/paddle_speed

        if keys_pressed[pygame.K_a] != 0 and model.paddle2.x > 0:
            model.paddle2.x = model.paddle2.x - model.paddle2.width/paddle_speed

        if keys_pressed[pygame.K_d] != 0 and model.paddle2.x < size[0]-model.paddle2.width:
            model.paddle2.x = model.paddle2.x + model.paddle2.width/paddle_speed



        time.sleep(.001)
        # if ball hits top or bottom, scor updates
        if model.ball.hits_bad_wall():
            model.score.update_score(model.ball.player_score(), model.ball)
            if model.score.winner() is not None:
                # if there is a round winner, will go to exit screen
                player = model.score.winner()
                end = True
                end_view = EndWindowView(model,screen, player)
            view.draw()
            time.sleep(1) # resets ball to center then waits until moving
        else:
            view.draw()
            if index == 0:
                time.sleep(1)
            index = 1

        model.ball.move(model.paddle1, model.paddle2)

        # end screen when someone wins, only continue when space bar hit
        while end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = False
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    model.ball.reset()
                    model.score.reset_score()
                    index = 0
                    end = False


            end_view.draw()

    pygame.quit()
