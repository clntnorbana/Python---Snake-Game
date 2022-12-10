import pygame
from random import randrange

vec2 = pygame.math.Vector2

class Snake:
    def __init__(self, game):
        self.game = game
        self.size = game.TITLE_SIZE
        self.rect = pygame.rect.Rect([0, 0, game.TITLE_SIZE, game.TITLE_SIZE])
        self.rect.center = self.get_rand_pos()
        self.direction = vec2(self.size, 0)
        self.step_delay = 100
        self.time = 0
        self.length = 2
        self.segments = []
        self.directions = {pygame.K_w: 1, pygame.K_s: 1, pygame.K_a: 1, pygame.K_d: 1}

    def control(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and self.directions[pygame.K_w]:
                self.direction = vec2(0, -self.size)
                self.directions = {pygame.K_w: 1, pygame.K_s: 0, pygame.K_a: 1, pygame.K_d: 1}
            if event.key == pygame.K_s and self.directions[pygame.K_s]:
                self.direction = vec2(0, self.size)
                self.directions = {pygame.K_w: 0, pygame.K_s: 1, pygame.K_a: 1, pygame.K_d: 1}
            if event.key == pygame.K_a and self.directions[pygame.K_a]:
                self.direction = vec2(-self.size, 0)
                self.directions = {pygame.K_w: 1, pygame.K_s: 1, pygame.K_a: 1, pygame.K_d: 0}
            if event.key == pygame.K_d and self.directions[pygame.K_d]:
                self.direction = vec2(self.size, 0)
                self.directions = {pygame.K_w: 1, pygame.K_s: 1, pygame.K_a: 0, pygame.K_d: 1}
    
    def delta_time(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.time > self.step_delay:
            self.time = time_now
            return True
        return False

    def get_rand_pos(self):
        return [randrange(self.size // 2, self.game.WINDOW_SIZE - self.size // 2, self.size)] * 2

    def check_border(self):
        if self.rect.left < 0 or self.rect.right > self.game.WINDOW_SIZE:
            self.game.new_game()
        if self.rect.top < 0 or self.rect.bottom > self.game.WINDOW_SIZE:
            self.game.new_game()

    def check_food(self):
        if self.rect.center == self.game.food.rect.center:
            self.game.food.rect.center = self.get_rand_pos()
            self.length += 1
            self.step_delay -= 2

    def check_self_eating(self):
        if len(self.segments) != len(set(segment.center for segment in self.segments)):
            self.game.new_game()

    def move(self):
        if self.delta_time():
            self.rect.move_ip(self.direction)
            self.segments.append(self.rect.copy())
            self.segments = self.segments[-self.length:]

    def update(self):
        self.check_self_eating()
        self.check_border()
        self.check_food()
        self.move()

    def draw(self):
        for segment in self.segments:
            pygame.draw.rect(self.game.screen, 'green', segment)

class Food:
    def __init__(self, game):
        self.game = game
        self.size = game.TITLE_SIZE
        self.rect = pygame.rect.Rect([0, 0, game.TITLE_SIZE, game.TITLE_SIZE])
        self.rect.center = self.game.snake.get_rand_pos()  
    
    def draw(self):
        pygame.draw.rect(self.game.screen, 'red', self.rect)
