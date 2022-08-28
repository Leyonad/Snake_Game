import pygame
import random
pygame.init()
pygame.font.init()

fps = 10
WIDTH = 900
HEIGHT = WIDTH

SQUARES = 30
R = WIDTH/SQUARES
SPEED = R
COLORGRID = (80,80,80)
BACKGROUNDCOLOR = (8, 4, 0)

RED = (240, 50, 50)
GREEN = (50, 240, 50)

FONTSTYLE = 'ROBOTO'
FONTSIZE = 40
FONTSIZETITLE = 60
FONTCOLOR = (30, 30, 30)
FONT = pygame.font.SysFont(FONTSTYLE, FONTSIZE)
FONTTITLE = pygame.font.SysFont(FONTSTYLE, FONTSIZETITLE)

SNAKESTARTX = R*(SQUARES/2-1)
SNAKESTARTY = R*(SQUARES/2-1)

APPLESTARTX = R*(SQUARES*3//4)
APPLESTARTY = R*(SQUARES/2-1)

ROUNDNESS = 30

pygame.display.set_caption(f'Snake Game')
win = pygame.display.set_mode((WIDTH, HEIGHT))
gamestate = 0

class Snake():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = R
        self.height = R
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = [1, 0]
        self.segments = []

        self.gaveCommand = False
        self.moved = False

    def draw(self, win):
        tl, tr, bl, br = 0, 0, 0, 0
        if self.direction == [1, 0]:
            tr, br = ROUNDNESS, ROUNDNESS
        elif self.direction == [-1, 0]:
            tl, bl = ROUNDNESS, ROUNDNESS
        elif self.direction == [0, -1]:
            tl, tr = ROUNDNESS, ROUNDNESS
        elif self.direction == [0, 1]:
            bl, br = ROUNDNESS, ROUNDNESS

        pygame.draw.rect(win, self.color, pygame.Rect(self.x, self.y, self.width, self.height), 
                    border_top_left_radius=tl, border_top_right_radius=tr, border_bottom_left_radius=bl, border_bottom_right_radius=br)
        for segment in self.segments:
            pygame.draw.rect(win, self.color, pygame.Rect(segment[0], segment[1], self.width, self.height))

    def move(self):
        if self.gaveCommand != 0:
            self.updateDirection(self.gaveCommand)

        self.x += self.direction[0]*SPEED
        self.y += self.direction[1]*SPEED

        if [self.x, self.y] in self.segments:
            global gamestate
            gamestate = 1

        for i in range(len(self.segments)-1):
            self.segments[i] = self.segments[i+1]
        if len(self.segments) > 0:
            self.segments[-1] = [self.x-self.direction[0]*SPEED, self.y-self.direction[1]*SPEED]

        if self.x+R > WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = WIDTH-R
        if self.y+R > HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = HEIGHT-R

        self.moved = True

    def updateDirection(self, direction):
        self.moved = False
        if self.x%R == 0 and self.y%R == 0:
            self.direction = direction
            self.gaveCommand = 0
        else:
            self.gaveCommand = direction
        

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Apple():
    def __init__(self, color):
        self.color = color
        self.x = APPLESTARTX
        self.y = APPLESTARTY
        self.width = R
        self.height = R

    def draw(self, win):
        pygame.draw.rect(win, self.color, pygame.Rect(self.x, self.y, self.width, self.height), border_radius=10)

    def updatePosition(self):
        self.x = random.randrange(0, SQUARES)*R
        self.y = random.randrange(0, SQUARES)*R
        if [self.x, self.y] in snake.segments or [self.x, self.y] == [snake.x, snake.y]:
            self.updatePosition()

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

apple = Apple(RED)
snake = Snake(SNAKESTARTX, SNAKESTARTY, GREEN)

def resetGame():
    global gamestate
    gamestate = 0
    snake.segments = []
    snake.direction = [1, 0]
    snake.x, snake.y = SNAKESTARTX, SNAKESTARTY
    apple.x, apple.y = APPLESTARTX, APPLESTARTY

def drawGrid(win):
    for i in range(SQUARES):
        pygame.draw.line(win, COLORGRID, (0, i*R), (WIDTH, i*R))
        pygame.draw.line(win, COLORGRID, (i*R, 0), (i*R, HEIGHT))

def drawWindow(win):
    win.fill(BACKGROUNDCOLOR)

    if gamestate == 0:
        #drawGrid(win)
        if snake.getRect().colliderect(apple.getRect()):
            apple.updatePosition()
            snake.segments.append([snake.x, snake.y])
        snake.move()
        apple.draw(win)
        snake.draw(win)
    else:
        label = FONTTITLE.render(f'YOU LOST!', True, FONTCOLOR)
        label_rect = label.get_rect(center=(WIDTH/2, HEIGHT/3))
        label2 = FONT.render(f'POINTS: {len(snake.segments)}', True, FONTCOLOR)
        label_rect2 = label2.get_rect(center=(WIDTH/2, HEIGHT/2+label.get_height()))
        label3 = FONT.render(f'PRESS ENTER TO RESTART', True, FONTCOLOR)
        label_rect3 = label3.get_rect(center=(WIDTH/2, HEIGHT/2+label.get_height()*2))
        win.blit(label, label_rect)
        win.blit(label2, label_rect2)
        win.blit(label3, label_rect3)

def main():
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            et = event.type
            if et == pygame.QUIT:
                run = False
                break

            elif et == pygame.KEYDOWN:
                if snake.moved is True:
                    if event.key == pygame.K_LEFT:
                        if snake.direction != [1, 0]:
                            snake.updateDirection([-1, 0])
                    elif event.key == pygame.K_RIGHT:
                        if snake.direction != [-1, 0]:
                            snake.updateDirection([1, 0])
                    
                    elif event.key == pygame.K_UP:
                        if snake.direction != [0, 1]:
                            snake.updateDirection([0, -1])
                    elif event.key == pygame.K_DOWN:
                        if snake.direction != [0, -1]:
                            snake.updateDirection([0, 1])

                if gamestate == 1 and event.key == pygame.K_RETURN:
                    resetGame()

        drawWindow(win)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()