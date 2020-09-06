import pygame, sys, random
import Colours


pygame.init()

screen = pygame.display.set_mode((1000,500))
pygame.display.set_caption("PONG!")


class Paddle(pygame.sprite.Sprite):
    def __init__(self, colour, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(Colours.BLACK)
        self.image.set_colorkey(Colours.BLACK)

        pygame.draw.rect(self.image, colour, [0, 0, width, height])

        self.rect = self.image.get_rect()

    def move_up(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
            self.rect.y = 0
        
    def move_down(self, pixels):
        self.rect.y += pixels
        if self.rect.y > 400:
            self.rect.y = 400

class Ball(pygame.sprite.Sprite):
    def __init__(self, colour, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(Colours.BLACK)
        self.image.set_colorkey(Colours.BLACK)

        pygame.draw.rect(self.image, colour, [0, 0, width, height])

        self.velocity = [5,random.randint(-5,5)]

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = self.velocity[1] + random.randint(-3,3)

    def reset(self):
        Ball.rect.x = 500
        Ball.rect.y = 250
        self.velocity = [random.choice((-5,5)),random.randint(-5,5)]

class Player(pygame.sprite.Sprite):
    def __init__(self, side):
        super().__init__()

        self.score = 0

        self.paddle = Paddle(Colours.WHITE, 10, 100)
        if side == "left":
            self.paddle.rect.x = 30
            self.paddle.rect.y = 200
            sprites_list.add(self.paddle)
        else:
            self.paddle.rect.x = 970
            self.paddle.rect.y = 200
            sprites_list.add(self.paddle)

#init ball
Ball = Ball(Colours.WHITE, 10, 10)
Ball.reset()
#add sprites to list
sprites_list = pygame.sprite.Group()

sprites_list.add(Ball)
#enable clock
clock = pygame.time.Clock()
#init scores
Player1 = Player("left")
Player2 = Player("right")


while True:
    #quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #play keys
    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        Player2.paddle.move_up(5)
    if key[pygame.K_DOWN]:
        Player2.paddle.move_down(5)
    if key[pygame.K_w]:
        Player1.paddle.move_up(5)
    if key[pygame.K_s]:
        Player1.paddle.move_down(5)
    
    #Hit floor or ceiling
    if Ball.rect.y>500:
        Ball.velocity[1] = -Ball.velocity[1]
    if Ball.rect.y<0:
        Ball.velocity[1] = -Ball.velocity[1]
    #hit paddle
    if pygame.sprite.collide_mask(Ball, Player1.paddle) or pygame.sprite.collide_mask(Ball, Player2.paddle):
        Ball.bounce()

    #Git goal
    if Ball.rect.x>=990:
        Player1.score += 1
        Ball.reset()
    if Ball.rect.x<=0:
        Player2.score += 1
        Ball.reset()

    screen.fill(Colours.BLACK)
    #Display Score
    font = pygame.font.Font(None, 74)
    text = font.render(str(Player1.score), 1, Colours.WHITE)
    screen.blit(text, (450,50))
    text = font.render(str(Player2.score), 1, Colours.WHITE)
    screen.blit(text, (550,50))

    #Update screen
    sprites_list.update()
    pygame.draw.line(screen, (Colours.WHITE), (500, 0), (500, 500), 5)
    sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)

