import pygame

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500

# TODO change drawings to sprites
class Score_handler(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0
        pygame.font.init() 
        self.myfont = pygame.font.Font('Pixeled.ttf', 15)

    def draw_score(self):
        score_text = self.myfont.render('SCORE ' + str(self.score), False, (255, 255, 255))
        win.blit(score_text,(self.x, self.y))

        
class Player(object):
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 8
        self.last_shoot_time = 0
        self.lives = 3

    def draw(self):
        pygame.draw.line(win, (255, 255, 255), (self.x - 15, self.y), (self.x + 15, self.y), 16)
        pygame.draw.polygon(win, (255, 255, 255), [[self.x - 4, self.y - 8], [self.x, self.y - 13], [self.x + 4, self.y - 8]], 5)

    def move_left(self):
        if self.x  - 20 - self.velocity >= 0:
            self.x -= self.velocity

    def move_right(self):
        if self.x + 20 + self.velocity <= WINDOW_WIDTH:
            self.x += self.velocity

    def shoot(self):
        if pygame.time.get_ticks() - self.last_shoot_time > 1000:
            bullets.append(Player_bullet(self.x, self.y - 13))
            self.last_shoot_time = pygame.time.get_ticks()

    def is_hit(self, bullet):
        #print('Bullet: X - ' + str(bullet.x) + ', Y - ' + str(bullet.y))
        #print('Player: left border - ' + str(self.x - 15) + ', right border - ' + str(self.x + 15) + ', Y - ' + str(self.y))
        return bullet.y >= self.y and bullet.y <= self.y + 8 and bullet.x >= self.x - 15 and bullet.x  <= self.x + 15



class Bullet(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 10
        self.HEIGHT = 5
        self.WIDTH = 2

    def draw(self):
        pygame.draw.line(win, (255, 255, 255), (self.x, self.y), (self.x, self.y - self.HEIGHT), self.WIDTH)
        self.y += self.velocity


class Player_bullet(Bullet):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.velocity = -self.velocity


class Enemy_bullet(Bullet):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.HEIGHT = self.HEIGHT


class Enemy(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = self.x + 10
        self.last_move = 0
        self.move_count = 4
        self.move_left = False
        self.move_right = True
        self.HEIGHT = 20
        self.last_shoot_time = 0

    def draw(self):
        if pygame.time.get_ticks() - self.last_move> 2000:
            self.move()
            self.last_move = pygame.time.get_ticks()
        pygame.draw.line(win, (255, 255, 255), (self.x, self.y), (self.x + 30, self.y), self.HEIGHT)

    # make rows of enemies move on delay (1st row first, 2nd row second etc)
    def move(self):
        if self.move_left:
            neg = -1
        else:
            neg = 1
            
        if self.move_count == 6:
            self.y += 30
            self.x -= 20 * neg
            self.move_count = 0
            self.move_left = not self.move_left
            self.move_right = not self.move_right
        self.x += 20 * neg
        self.move_count += 1

    def is_hit(self, bullet):
        return bullet.y - bullet.HEIGHT <= self.y and bullet.y >= self.y - self.HEIGHT and bullet.x >= self.x and bullet.x <= self.x + 30

    def shoot(self):
        if pygame.time.get_ticks() - self.last_shoot_time > 1000:
            bullets.append(Enemy_bullet(self.x, self.y + 15))
            self.last_shoot_time = pygame.time.get_ticks()
    

def generate_enemies():
    # generate two dimensional list with length [4][10]
    enemies = [[0] * 11 for i in range(5)]
    # fill array with enemy objects
    for i in range(5):
         for j in range(11):
            enemies[i][j] = Enemy(110 + j * 45, 80 + i * 35)
    return enemies


pygame.init()
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Invaders')

clock = pygame.time.Clock()
score_handler = Score_handler(10, 10)
player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)
bullets = []
enemies = generate_enemies()

score = 0

def redraw_game_window():
    win.fill((0, 0, 0))
    score_handler.draw_score()
    
    # TODO change drawings to player sprite
    for i in range (player.lives):
        pygame.draw.line(win, (255, 255, 255), (10 + i * 30, 60), (30 + i * 30, 60), 12)
        pygame.draw.polygon(win, (255, 255, 255), [[15 + i * 30, 60], [20 + i * 30, 51], [25 + i * 30, 60]], 3)
        
    player.draw()
    for row in enemies:
        for enemy in row:
            enemy.draw()
    enemies[4][5].shoot()
    for bullet in bullets:
        bullet.draw()
    pygame.display.update()

last_check = 0
run = True
while run:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # TODO optimalize this loop to check only collisions player bullet - enemy, enemy bullet - player, not bullet - enemy, bullet - player
    for bullet in bullets:
        for row in enemies:
            for enemy in row:
                if bullet.__class__.__name__ == 'Player_bullet' and enemy.is_hit(bullet):
                    row.pop(row.index(enemy))
                    bullets.pop(bullets.index(bullet))
                    score_handler.score += 10
                elif player.is_hit(bullet) and pygame.time.get_ticks() - last_check > 1000:
                    # TODO try to find better way to live system implementation (maybe move it to Player class, do some player blink animations on hit and
                    # stop game while blinking
                    player.lives -= 1
                    if player.lives == 0:
                        run = False
                    last_check = pygame.time.get_ticks()
                    print('HIT')
        if bullet.y - bullet.HEIGHT <= 0:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()
    if keys[pygame.K_SPACE]:
        player.shoot()

    redraw_game_window()

pygame.quit()
