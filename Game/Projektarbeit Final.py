import pygame, math, random, button
from pygame.locals import *

pygame.init()

#Konstanten/Counter
display_size = pygame.display.get_desktop_sizes()
SCREEN_WIDTH = display_size[0][0]
SCREEN_HEIGHT = display_size[0][1]
FPS = 60
font1 = "comicsansm"
font2 = "arialblack"
x = SCREEN_WIDTH/2
y = SCREEN_HEIGHT/2
initital_health = 10000
kills = 0
shots = 10

#Game Settings

# 1 = lowest
player1_pace = 5
player2_pace = 7
spider_pace = 3

speed_powerup = 2

# 1s = 100
speedboost_duration = 300

# 1 = fastest
player1_cooldown_duration = 20
player2_cooldown_duration = 30

# 1 = most frequent
flame_chance= 4
powerup_chance=8

# 1 HP = 100
heal_boost = 1000

# 1 = least
amount_spiders=1

#Scenes
game_paused = True
game_finished = True
game_info = False
gamemode = ""

#Screen
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Projektarbeit")

#Backgrounds
background_img = pygame.image.load("assets/backgrounds/background.jpg")
background = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

background_dark_img = pygame.image.load("assets/backgrounds/background_dark.png")
background_dark = pygame.transform.scale(background_dark_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

#Menu
menu_img = pygame.image.load("assets/backgrounds/menu.png")
menu = pygame.transform.scale(menu_img, ((SCREEN_WIDTH/1.2),(SCREEN_HEIGHT/1.2)))

#GameOver
game_over_img = pygame.image.load("assets/backgrounds/gameover.png")
game_over = pygame.transform.scale(game_over_img, ((SCREEN_WIDTH/1.5),(SCREEN_HEIGHT/1.5)))

#Info
info_img = pygame.image.load("assets/backgrounds/info.png")
info = pygame.transform.scale(info_img, ((SCREEN_WIDTH/1.2),(SCREEN_HEIGHT/1.2)))

#Button Images
sp_img = pygame.image.load("assets/buttons/singleplayer.png").convert_alpha()
sp_scale = pygame.transform.scale(sp_img, ((SCREEN_WIDTH/2), SCREEN_HEIGHT/3))

mp_img = pygame.image.load("assets/buttons/multiplayer.png").convert_alpha()
mp_scale = pygame.transform.scale(mp_img, ((SCREEN_WIDTH/2), SCREEN_HEIGHT/3))

replay_img = pygame.image.load("assets/buttons/replay.png").convert_alpha()
replay_scale = pygame.transform.scale(replay_img, ((SCREEN_WIDTH/2), SCREEN_HEIGHT/3))

info_img = pygame.image.load("assets/buttons/info.png").convert_alpha()
info_scale = pygame.transform.scale(info_img, (150, 150))

back_img = pygame.image.load("assets/buttons/back.png").convert_alpha()
back_scale = pygame.transform.scale(back_img, (150, 150))

#Button creation
sp_button = button.Button(screen.get_rect().centerx-sp_scale.get_rect().width/2, SCREEN_HEIGHT/4.4, sp_scale, 1)
mp_button = button.Button(screen.get_rect().centerx-sp_scale.get_rect().width/2, SCREEN_HEIGHT/2.1, mp_scale, 1)
replay_button = button.Button(screen.get_rect().centerx-sp_scale.get_rect().width/2, SCREEN_HEIGHT/1.5, replay_scale, 1)
info_button = button.Button(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150, info_scale, 1)
back_button = button.Button(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150, back_scale, 1)



#Players
class PlayerOne:
    def __init__(self, x, y):
        self.img = pygame.image.load("assets/players/playerOne.png").convert()
        self.img.set_colorkey((0, 0, 0), RLEACCEL)
        self.img_scaled = pygame.transform.scale(self.img, (50,50))
        self.rect = self.img_scaled.get_rect()

        #Pace, Coordinates & Direction
        self.pace = player1_pace
        self.rect.x = y
        self.rect.y = x
        self.face_left = False
        self.face_right = False
        self.face_up = True
        self.face_down = False
        
        #Shots & Cooldown
        self.bullets= []
        self.cooldown_duration = 0
        self.shots = shots

    #Playermovement & orientation
    def move_player(self, input):
        self.velx = 0
        self.vely = 0

        if input[pygame.K_a] and self.rect.x > 0:
            self.velx = -self.pace
            self.vely = 0
            self.face_left = True
            self.face_right = False
            self.face_up = False
            self.face_down = False
        if input[pygame.K_d] and self.rect.x < SCREEN_WIDTH - 50:
            self.velx = self.pace
            self.vely = 0
            self.face_left = False
            self.face_right = True
            self.face_up = False
            self.face_down = False
        if input[pygame.K_w] and self.rect.y > 0:
            self.velx = 0
            self.vely = -self.pace    
            self.face_left = False
            self.face_right = False
            self.face_up = True
            self.face_down = False
        if input[pygame.K_s] and self.rect.y < SCREEN_HEIGHT - 50:
            self.velx = 0
            self.vely = self.pace
            self.face_left = False
            self.face_right = False
            self.face_up = False
            self.face_down = True

        self.rect.x += self.velx
        self.rect.y += self.vely
    
    #Draw Player
    def draw(self, screen):
        if self.face_up:
            screen.blit(pygame.transform.rotate(self.img_scaled, 90), (self.rect.x, self.rect.y))
        if self.face_down:
            screen.blit(pygame.transform.rotate(self.img_scaled, 270), (self.rect.x, self.rect.y))
        if self.face_left:
            screen.blit(pygame.transform.rotate(self.img_scaled, 180), (self.rect.x, self.rect.y))
        if self.face_right:
            screen.blit(pygame.transform.rotate(self.img_scaled, 0), (self.rect.x, self.rect.y))
    
    #Orientation creation
    def direction(self):
        if self.face_up:
            return 1
        if self.face_right:
            return 2
        if self.face_down:
            return 3
        if self.face_left:
            return 4

    #Weaponcooldown
    def cooldown(self):
        if self.cooldown_duration >= player1_cooldown_duration:
            self.cooldown_duration = 0
        elif self.cooldown_duration > 0:
            self.cooldown_duration +=1

    #Shooting
    def shoot(self):
        self.cooldown()

        if input[pygame.K_SPACE] and self.cooldown_duration == 0 and self.shots >= 1:
            bullet = Bullet(self.rect.x, self.rect.y, self.direction())
            self.bullets.append(bullet)
            bullets_group.add(bullet)
            self.cooldown_duration = 1
            self.shots -= 1

    #Reload Weapon
        if self.velx == 0 and self.vely == 0:
            if life > 3000:
                self.shots += 1/60
            else:
                self.shots += 1/30

        if self.shots > shots:
            self.shots = shots
            
        for bullet in self.bullets:
            bullet.move()


            if bullet.off_screen():
                self.bullets.remove(bullet)
                bullets_group.remove(bullet)

class PlayerTwo:
    def __init__(self, x, y):
        self.img = pygame.image.load("assets/players/playerTwo.png").convert()
        self.img.set_colorkey((255, 255, 255), RLEACCEL)
        self.img_scaled = pygame.transform.scale(self.img, (150,150))
        self.rect = self.img_scaled.get_rect()

        #Laufen und Blickrichtung
        self.pace = player2_pace
        self.rect.x = y
        self.rect.y = x
        self.face_left = False
        self.face_right = False
        self.face_up = True
        self.face_down = False
        

        #Waffen
        self.fireballs= []
        self.flames=[]
        self.cooldown_duration = 0

    #Playermovement & orientation
    def move_player(self, input):

        self.velx = 0
        self.vely = 0

        if input[pygame.K_j] and self.rect.x > 0:
            self.velx = -self.pace
            self.vely = 0
            self.face_left = True
            self.face_right = False
            self.face_up = False
            self.face_down = False
        if input[pygame.K_l] and self.rect.x < SCREEN_WIDTH - 50:
            self.velx = self.pace
            self.vely = 0
            self.face_left = False
            self.face_right = True
            self.face_up = False
            self.face_down = False
        if input[pygame.K_i] and self.rect.y != 0:
            self.velx = 0
            self.vely = -self.pace    
            self.face_left = False
            self.face_right = False
            self.face_up = True
            self.face_down = False
        if input[pygame.K_k] and self.rect.y < SCREEN_HEIGHT - 50:
            self.velx = 0
            self.vely = self.pace
            self.face_left = False
            self.face_right = False
            self.face_up = False
            self.face_down = True

        self.rect.x += self.velx
        self.rect.y += self.vely
    
    #Draw Player
    def draw(self, screen):
        if self.face_up:
            screen.blit(pygame.transform.rotate(self.img_scaled, 0), (self.rect.x, self.rect.y))
        if self.face_down:
            screen.blit(pygame.transform.rotate(self.img_scaled, 180), (self.rect.x, self.rect.y))
        if self.face_left:
            screen.blit(pygame.transform.rotate(self.img_scaled, 90), (self.rect.x, self.rect.y))
        if self.face_right:
            screen.blit(pygame.transform.rotate(self.img_scaled, 270), (self.rect.x, self.rect.y))
    
    #Orientation creation
    def direction(self):
        if self.face_up:
            return 1
        if self.face_right:
            return 2
        if self.face_down:
            return 3
        if self.face_left:
            return 4

    #Weaponcooldown
    def cooldown(self):
        if self.cooldown_duration >= player2_cooldown_duration:
            self.cooldown_duration = 0
        elif self.cooldown_duration > 0:
            self.cooldown_duration +=1

    #Shooting
    def shoot(self):
        if gamemode == "multiplayer":
            self.cooldown()
            if input[pygame.K_RCTRL] and self.cooldown_duration == 0:
                flame.random_flame()
                fireball = Fireball(self.rect.x, self.rect.y, self.direction())
                self.fireballs.append(fireball)
                fireballs_group.add(fireball)
                self.cooldown_duration = 1

            #Feuerball bewegung
            for fireball in self.fireballs:
                fireball.move()

                if fireball.off_screen():
                    self.fireballs.remove(fireball)
                    fireballs_group.remove(fireball)
#Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load("assets/weapons/laser.png").convert()
        self.img.set_colorkey((0, 0, 0), RLEACCEL)
        self.img_scaled = pygame.transform.scale(self.img, (10,30))
        self.rect = self.img_scaled.get_rect()

        self.rect.x = y
        self.rect.y = x
        self.direction = direction
        self.pace = 7

        #Bullet Position & Orientation
        if direction == 1:
            self.rect.x = player.rect.x + 12
            self.rect.y = player.rect.y - 15
        if direction == 2:
            self.img_scaled = pygame.transform.rotate(self.img_scaled, 270)
            self.rect.x = player.rect.x + 37
            self.rect.y = player.rect.y + 12
        if direction == 3:
            self.img_scaled = pygame.transform.rotate(self.img_scaled, 180)
            self.rect.x = player.rect.x + 28
            self.rect.y = player.rect.y + 35
        if direction == 4:
            self.img_scaled = pygame.transform.rotate(self.img_scaled, 90)
            self.rect.x = player.rect.x - 15
            self.rect.y = player.rect.y + 28

       
    #Draw Bullet
    def draw(self):
        screen.blit(self.img_scaled, (self.rect.x, self.rect.y))
    
    #Bullet Movement
    def move(self):
        if self.direction == 1:
            self.rect.y -= self.pace
        if self.direction == 2:
            self.rect.x += self.pace
        if self.direction == 3:
            self.rect.y += self.pace
        if self.direction == 4:
            self.rect.x -= self.pace

    #Delete Bullet Offscreen
    def off_screen(self):
        return not (self.rect.x >= 0 and self.rect.x <= SCREEN_WIDTH) and not (self.rect.y >= 0 and self.rect.y <= SCREEN_HEIGHT)

#Fireball
class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load("assets/weapons/fireball.png").convert()
        self.img.set_colorkey((255,255,255), RLEACCEL)
        self.img_scaled = pygame.transform.scale(self.img, (70,40))
        self.rect = self.img_scaled.get_rect()

        self.rect.x = y
        self.rect.y = x
        self.direction = direction
        self.pace = 7

        #Fireball Position & Orientation
        if direction == 1:
            self.img_scaled = pygame.transform.rotate(self.img_scaled, 90)
            self.rect.x = player2.rect.x + 52
            self.rect.y = player2.rect.y - 10
        if direction == 2:
            self.img_scaled = pygame.transform.rotate(self.img_scaled, 0)
            self.rect.x = player2.rect.x + 110
            self.rect.y = player2.rect.y + 50
        if direction == 3:
            self.img_scaled = pygame.transform.rotate(self.img_scaled, 270)
            self.rect.x = player2.rect.x + 58
            self.rect.y = player2.rect.y + 110
        if direction == 4:
            self.img_scaled = pygame.transform.rotate(self.img_scaled, 180)
            self.rect.x = player2.rect.x - 12
            self.rect.y = player2.rect.y + 57

       
    #Draw Fireball
    def draw(self):
        screen.blit(self.img_scaled, (self.rect.x, self.rect.y))
    
    #Fireball Movement
    def move(self):
        if self.direction == 1:
            self.rect.y -= self.pace
        if self.direction == 2:
            self.rect.x += self.pace
        if self.direction == 3:
            self.rect.y += self.pace
        if self.direction == 4:
            self.rect.x -= self.pace

    #Delete Fireball Offscreen
    def off_screen(self):
        return not (self.rect.x >= 0 and self.rect.x <= SCREEN_WIDTH) and not (self.rect.y >= 0 and self.rect.y <= SCREEN_HEIGHT)

#Flame
class Flame(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load("assets/weapons/flame.png").convert()
        self.img.set_colorkey((255,255,255), RLEACCEL)
        self.img_scaled = pygame.transform.scale(self.img, (50,70))
        self.rect = self.img_scaled.get_rect()

        self.rect.x = x
        self.rect.y = y

    #Random Flames after Fireball
    def random_flame(self):
        for fireball in fireballs_group:
            i = random.randint(1,flame_chance)
            if i == 1:
                flame = Flame(fireball.rect.x, fireball.rect.y)
                player2.flames.append(flame)
                flames_group.add(flame)

    #Draw Flame
    def draw(self):
        screen.blit(self.flame_scaled, (self.rect.x, self.rect.y))

#Spider
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.front = [pygame.image.load("assets/spider/front (1).jpg").convert(), pygame.image.load("assets/spider/front (2).jpg").convert(),
        pygame.image.load("assets/spider/front (3).jpg").convert(), pygame.image.load("assets/spider/front (4).jpg").convert(), 
        pygame.image.load("assets/spider/front (5).jpg").convert(), pygame.image.load("assets/spider/front (6).jpg").convert(), 
        pygame.image.load("assets/spider/front (7).jpg").convert(), pygame.image.load("assets/spider/front (8).jpg").convert(), 
        pygame.image.load("assets/spider/front (9).jpg").convert(), pygame.image.load("assets/spider/front (10).jpg").convert(), 
        pygame.image.load("assets/spider/front (11).jpg").convert(), pygame.image.load("assets/spider/front (12).jpg").convert()]

        self.front_scaled_list = []

        for element in self.front:
            element.set_colorkey((95, 73, 59), RLEACCEL)
            self.front_scaled = pygame.transform.scale(element, (50,50))
            self.rect = self.front_scaled.get_rect()
            self.front_scaled_list.append(self.front_scaled)
            

        self.back = [pygame.image.load("assets/spider/back (1).jpg").convert(), pygame.image.load("assets/spider/back (2).jpg").convert(),
        pygame.image.load("assets/spider/back (3).jpg").convert(), pygame.image.load("assets/spider/back (4).jpg").convert(), 
        pygame.image.load("assets/spider/back (5).jpg").convert(), pygame.image.load("assets/spider/back (6).jpg").convert(), 
        pygame.image.load("assets/spider/back (7).jpg").convert(), pygame.image.load("assets/spider/back (8).jpg").convert(), 
        pygame.image.load("assets/spider/back (9).jpg").convert(), pygame.image.load("assets/spider/back (10).jpg").convert(), 
        pygame.image.load("assets/spider/back (11).jpg").convert(), pygame.image.load("assets/spider/back (12).jpg").convert()]

        self.back_scaled_list = []

        for element in self.back:
            element.set_colorkey((95, 73, 59), RLEACCEL)
            self.back_scaled = pygame.transform.scale(element, (50,50))
            self.rect = self.back_scaled.get_rect()
            self.back_scaled_list.append(self.back_scaled)


        self.left = [pygame.image.load("assets/spider/left (1).jpg").convert(), pygame.image.load("assets/spider/left (2).jpg").convert(),
        pygame.image.load("assets/spider/left (3).jpg").convert(), pygame.image.load("assets/spider/left (4).jpg").convert(), 
        pygame.image.load("assets/spider/left (5).jpg").convert(), pygame.image.load("assets/spider/left (6).jpg").convert(), 
        pygame.image.load("assets/spider/left (7).jpg").convert(), pygame.image.load("assets/spider/left (8).jpg").convert(), 
        pygame.image.load("assets/spider/left (9).jpg").convert(), pygame.image.load("assets/spider/left (10).jpg").convert(), 
        pygame.image.load("assets/spider/left (11).jpg").convert(), pygame.image.load("assets/spider/left (12).jpg").convert()]

        self.left_scaled_list = []

        for element in self.left:
            element.set_colorkey((95, 73, 59), RLEACCEL)
            self.left_scaled = pygame.transform.scale(element, (50,50))
            self.rect = self.left_scaled.get_rect()
            self.left_scaled_list.append(self.left_scaled)

        self.right = [pygame.image.load("assets/spider/right (1).jpg").convert(), pygame.image.load("assets/spider/right (2).jpg").convert(),
        pygame.image.load("assets/spider/right (3).jpg").convert(), pygame.image.load("assets/spider/right (4).jpg").convert(), 
        pygame.image.load("assets/spider/right (5).jpg").convert(), pygame.image.load("assets/spider/right (6).jpg").convert(), 
        pygame.image.load("assets/spider/right (7).jpg").convert(), pygame.image.load("assets/spider/right (8).jpg").convert(), 
        pygame.image.load("assets/spider/right (9).jpg").convert(), pygame.image.load("assets/spider/right (10).jpg").convert(), 
        pygame.image.load("assets/spider/right (11).jpg").convert(), pygame.image.load("assets/spider/right (12).jpg").convert()]

        self.right_scaled_list = []

        for element in self.right:
            element.set_colorkey((95, 73, 59), RLEACCEL)
            self.right_scaled = pygame.transform.scale(element, (50,50))
            self.rect = self.right_scaled.get_rect()
            self.right_scaled_list.append(self.right_scaled)

        self.rect.top = y
        self.rect.left = x

        self.speed = spider_pace

        self.face_up= False
        self.face_down = False
        self.face_left = True
        self.face_right = False

        self.stepIndex = 0

    #Spider Animation 
    def step(self):
        if self.stepIndex >= 120:
            self.stepIndex = 0

    #Draw Spider
    def draw(self, screen):
        self.step()
        self.direction()
        
        if self.face_up:
            screen.blit(self.front_scaled_list[self.stepIndex//10], self.rect)
        if self.face_down:
            screen.blit(self.back_scaled_list[self.stepIndex//10], self.rect)
        if self.face_left:
            screen.blit(self.left_scaled_list[self.stepIndex//10], self.rect)
        if self.face_right:
            screen.blit(self.right_scaled_list[self.stepIndex//10], self.rect)

        self.stepIndex += 1
    
    #Spider Orientation
    def direction(self):
        self.distance_x = player.rect.x - self.rect.left
        self.distance_y = player.rect.y - self.rect.top

        if (self.distance_y < 0) and (abs(self.distance_y) > abs(self.distance_x)) :
            self.face_up= True
            self.face_down = False
            self.face_left = False
            self.face_right = False

        if (self.distance_y > 0) and (abs(self.distance_y) > abs(self.distance_x)) :
            self.face_up= False
            self.face_down = True
            self.face_left = False
            self.face_right = False  

        if (self.distance_x < 0) and (abs(self.distance_x) > abs(self.distance_y)) :
            self.face_up= False
            self.face_down = False
            self.face_left = True
            self.face_right = False

        if (self.distance_x > 0) and (abs(self.distance_x) > abs(self.distance_y)) :
            self.face_up= False
            self.face_down = False
            self.face_left = False
            self.face_right = True  

    #Spider Attack
    def move(self, player):
        self.distancex = player.rect.x - self.rect.left
        self.distancey = player.rect.y - self.rect.top
        distance = math.hypot(self.distancex, self.distancey)
        if distance > 0:
          self.distancex, self.distancey = self.distancex / distance, self.distancey / distance
        else:
            self.distancex = 0
            self.distancey = 0

        self.rect.move_ip(self.distancex * self.speed, self.distancey * self.speed)

#Power-Ups
class Powerup(pygame.sprite.Sprite):
    def __init__(self,x,y,powerup):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load("assets/powerups/" + powerup + ".png").convert()
        self.img.set_colorkey((255,255,255), RLEACCEL)
        self.img_scaled = pygame.transform.scale(self.img, (50,50))
        self.rect = self.img_scaled.get_rect()

        self.rect.x = x
        self.rect.y = y

    #Draw PowerUp
    def draw(self):
        screen.blit(self.img_scaled, (self.rect.x, self.rect.y))

#Displays
def lifedisplay(life):
    amount_life= pygame.font.SysFont(font1, 25).render("Leben: " + str(int(life/100)), True, [0,0,0])
    screen.blit(amount_life, [10, 10])

def shotdisplay():
    amount_shots= pygame.font.SysFont(font1, 25).render("Schüsse: " + str(int(player.shots)), True, [0,0,0])
    screen.blit(amount_shots, [SCREEN_WIDTH/2.5 ,10])

def killdisplay(kills):
    if game_finished ==  False:
        amount_kills= pygame.font.SysFont(font1, 25).render("Kills: " + str(int(kills)), True, [0,0,0])
        screen.blit(amount_kills, [SCREEN_WIDTH/1.2, 10])
    elif game_finished == True:
        amount_kills= pygame.font.SysFont(font1, 150).render("Kills: " + str(int(kills)), True, [0,0,0])
        screen.blit(amount_kills, [SCREEN_WIDTH/3, SCREEN_HEIGHT/2.1])

#Draw Game
def draw_game():
    screen.fill ((0,0,0))
    screen.blit(background, (0,0))
        
    player.draw(screen)
    
    for enemy in mobs.sprites():
        enemy.draw(screen)
    
    for powerup in speed_group.sprites():
        powerup.draw()

    for powerup in heal_group.sprites():
        powerup.draw()

    for bullet in bullets_group.sprites():
        bullet.draw()

    for fireball in fireballs_group.sprites():
        fireball.draw()

    for flame in flames_group.sprites():
        flame.draw()

    if gamemode == "multiplayer":
        player2.draw(screen)

    lifedisplay(life)
    shotdisplay()
    killdisplay(kills)
    
    pygame.time.delay(10)
    pygame.display.update()

#Draw Pausescreen
def draw_pause():
    screen.fill((0, 0, 0))
    screen.blit(background_dark, (0,0))
    screen.blit(menu, menu.get_rect(center=screen.get_rect().center))
    sp_button.draw(screen)
    mp_button.draw(screen)
    info_button.draw(screen)
        
    pygame.time.delay(10)
    pygame.display.update()

#Draw Endscreen
def draw_finish():
    screen.fill((0, 0, 0))
    screen.blit(background_dark, (0,0))
    screen.blit(game_over, (SCREEN_WIDTH/5.8, 50))
    killdisplay(kills)
    replay_button.draw(screen)

    for enemy in mobs:
        mobs.remove(enemy)
    
    for speed in speed_group:
        speed_group.remove(speed)

    for heal in heal_group:
        heal_group.remove(heal)

    for flame in flames_group:
        flames_group.remove(flame)

    pygame.time.delay(10)
    pygame.display.update()

#Draw Infoscreen
def draw_info():
    screen.fill((0, 0, 0))
    screen.blit(background_dark, (0,0))
    screen.blit(info, info.get_rect(center=screen.get_rect().center))
    back_button.draw(screen)
    pygame.time.delay(10)
    pygame.display.update()

#Spiders at the beginning
def start():
    for enemies in range(10):
        i = random.randint(1,4)
        if i == 1:
            for enemies in range(random.randint(0,2)):
                enemy = Enemy(random.randint(0,SCREEN_WIDTH), -50)
                mobs.add(enemy)
        elif i == 2:
            for enemies in range(random.randint(0,2)):
                enemy = Enemy(random.randint(0,SCREEN_WIDTH), SCREEN_HEIGHT + 60)
                mobs.add(enemy)
        elif i == 3:
            for enemies in range(random.randint(0,2)):
                enemy = Enemy(-70, random.randint(0, SCREEN_HEIGHT))
                mobs.add(enemy)
        elif i == 4:
            for enemies in range(random.randint(0,2)):
                enemy = Enemy((SCREEN_WIDTH + 80), random.randint(0, SCREEN_HEIGHT))
                mobs.add(enemy)

#Objects & Groups
player = PlayerOne(SCREEN_HEIGHT/2, SCREEN_WIDTH/3)
player2 = PlayerTwo(SCREEN_HEIGHT/2, SCREEN_WIDTH/3*2)
flame = Flame(x,y)
speed = Powerup(x,y,"speed")
heal = Powerup(x,y,"heal")

mobs = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
fireballs_group = pygame.sprite.Group()
flames_group = pygame.sprite.Group()

speed_group = pygame.sprite.Group()
heal_group = pygame.sprite.Group()
    
start()

#Main Loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                game_paused = False

    #Pausescreen
    if game_paused == True and game_finished == True and game_info == False:
        if sp_button.draw(screen):
            game_paused = False
            game_finished = False
            gamemode = "singleplayer"
            player = PlayerOne(SCREEN_HEIGHT/2, SCREEN_WIDTH/2)

        if mp_button.draw(screen):
            game_paused = False
            game_finished = False
            gamemode = "multiplayer"

        life = initital_health

        if info_button.draw(screen):
            game_info = True
            draw_info()
        else:
            draw_pause()

    if game_info == True and game_finished == True and game_paused == True:
        if back_button.draw(screen):
            game_info = False
            draw_pause()
            

    #Endscreen
    if game_paused == False and game_finished == True:
        
        if replay_button.draw(screen):
            game_finished = False
            kills = 0
            life = initital_health
            mobs.remove()
            speed_group.remove()
            heal_group.remove()

            if gamemode == "singleplayer":
                player = PlayerOne(SCREEN_HEIGHT/2, SCREEN_WIDTH/2)
            if gamemode == "multiplayer":
                player = PlayerOne(SCREEN_HEIGHT/2, SCREEN_WIDTH/3)
                player2 = PlayerTwo(SCREEN_HEIGHT/2, SCREEN_WIDTH/3*2)

        draw_finish()
        if game_finished == False:
            start()
        
    #Game
    if game_paused == False and game_finished == False:      
        #Quality of Life Variable
        input = pygame.key.get_pressed()

        #Abilities PlayerOne
        player.move_player(input)
        player.shoot()

        #Abilities PlayerTwo
        player2.move_player(input)
        player2.shoot()
        
        #Abilities Spider
        for enemy in mobs.sprites():
            enemy.move(player)

        #Collision Attack/Spider
        bullet_collision = pygame.sprite.groupcollide(mobs, bullets_group, True, True)
        fireball_collision = pygame.sprite.groupcollide(mobs, fireballs_group, True, True)
        flame_collision = pygame.sprite.groupcollide(mobs, flames_group, True, True)

        #Collision PlayerOne/PowerUp
        speed_collision = pygame.sprite.spritecollide(player, speed_group, True)
        heal_collision = pygame.sprite.spritecollide(player, heal_group, True)

        #Collision PlayerOne/Spider
        player_collision = pygame.sprite.spritecollide(player, mobs, False)

        #Health PlayerOne
        if player_collision:
            life -= 20
            if life == 0:
                game_finished = True

        #PowerUp (Speed)
        if speed_collision:
            player.pace = player1_pace + speed_powerup
            speed_duration = speedboost_duration

        if player.pace == player1_pace + speed_powerup:
            speed_duration -= 1
            if speed_duration <= 0:
                player.pace = player1_pace

        #PowerUp (Health)
        if heal_collision:
            life += heal_boost
            if life > initital_health:
                life = initital_health

        #Restore shots
        if bullet_collision:
            player.shots += 1
        
        if bullet_collision or fireball_collision:
            #Killcounter
            kills += 1
            
            #Difficulty
            if kills == 10:
                amount_spiders += 1
            if kills == 50:
                spider_pace += 0.5
            if kills == 100:
                amount_spiders += 1
            if kills == 150:
                spider_pace += 0.5

            #Spawn Power-Ups
            i = random.randint(1, powerup_chance)
            if i == 1:
                i = random.randint(1, 2)
                if i == 1:
                    speed = Powerup(random.randint(0,SCREEN_WIDTH), random.randint(0,(SCREEN_HEIGHT-50)), "speed")
                    speed_group.add(speed)
                
                if i == 2:
                    heal = Powerup(random.randint(0,SCREEN_WIDTH), random.randint(0,(SCREEN_HEIGHT-50)), "heal")
                    heal_group.add(heal)

            #Spawn Spiders If Lack Of Enemies
            while len(mobs) < 3: 
                for repeat in range(2):
                    i = random.randint(1,4)
                    if i == 1:
                        for enemies in range(random.randint(0,amount_spiders)):
                            enemy = Enemy(random.randint(0,SCREEN_WIDTH), -100)
                            mobs.add(enemy)
                    elif i == 2:
                        for enemies in range(random.randint(0,amount_spiders)):
                            enemy = Enemy(random.randint(0,SCREEN_WIDTH), SCREEN_HEIGHT + 100)
                            mobs.add(enemy)
                    elif i == 3:
                        for enemies in range(random.randint(0,amount_spiders)):
                            enemy = Enemy(-100, random.randint(0, SCREEN_HEIGHT))
                            mobs.add(enemy)
                    elif i == 4:
                        for enemies in range(random.randint(0,amount_spiders)):
                            enemy = Enemy((SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT))
                            mobs.add(enemy)

            #Spawn Spiders If Spider Killed
            for repeat in range(1):
                i = random.randint(1,4)
                if i == 1:
                    for enemies in range(random.randint(0,amount_spiders)):
                        enemy = Enemy(random.randint(0,SCREEN_WIDTH), -100)
                        mobs.add(enemy)
                elif i == 2:
                    for enemies in range(random.randint(0,amount_spiders)):
                        enemy = Enemy(random.randint(0,SCREEN_WIDTH), SCREEN_HEIGHT + 100)
                        mobs.add(enemy)
                elif i == 3:
                    for enemies in range(random.randint(0,amount_spiders)):
                        enemy = Enemy(-100, random.randint(0, SCREEN_HEIGHT))
                        mobs.add(enemy)
                elif i == 4:
                    for enemies in range(random.randint(0,amount_spiders)):
                        enemy = Enemy((SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT))
                        mobs.add(enemy)

        #Draw Game
        draw_game()