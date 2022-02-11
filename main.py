import pygame
import sys
import math
pygame.init()
pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

display = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
throw_sound = pygame.mixer.Sound("throw.mp3")

player_walk_images = [pygame.image.load("graphics/run1.png"), pygame.image.load("graphics/run2.png"), pygame.image.load("graphics/run3.png"), pygame.image.load("graphics/run4.png")]
player_idle_images = [pygame.image.load("graphics/idle/idle.png"), pygame.image.load("graphics/idle/idle1.png"), pygame.image.load("graphics/idle/idle2.png"), pygame.image.load("graphics/idle/idle4.png"), pygame.image.load("graphics/idle/idle5.png"), pygame.image.load("graphics/idle/idle6.png"), pygame.image.load("graphics/idle/idle7.png")]
teacher_image = pygame.image.load("graphics/teacher.png")

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_count = 0
        self.idle_count = 0
        self.moving_right = False
        self.moving_left = False
    def main(self, display):
        if self.animation_count + 1 >= 16:
            self.animation_count = 0

            
        self.animation_count += 1
        
        if self.idle_count + 1 >= 32:
            self.idle_count = 0

            
        self.idle_count += 1

        if self.moving_right:
            self.x += 2
            display.blit(pygame.transform.scale(player_walk_images[self.animation_count//4], (32, 42)), (self.x, self.y))
        elif self.moving_left:
            self.x -= 2
            display.blit(pygame.transform.scale(pygame.transform.flip(player_walk_images[self.animation_count//4], True, False), (32, 42)), (self.x, self.y))
        else:
            display.blit(pygame.transform.scale(player_idle_images[self.idle_count//8], (32, 42)), (self.x, self.y))
        #pygame.draw.rect(display, (255, 0, 0), (self.x, self.y, self.width, self.height))
        self.moving_right = False
        self.moving_left = False

class Teacher:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def main(self, display):
        display.blit(pygame.transform.scale(teacher_image, (72, 72)), (100-display_scroll[0], 100-display_scroll[1]))
    


    
class PlayerBullet:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 15
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
    def main(self, display):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)

        pygame.draw.circle(display, (0,0,0), (self.x, self.y), 5)
    



player = Player(400, 300, 32, 32)
teacher = Teacher(300, 300, 32, 32)
display_scroll = [0,0]



player_bullets = []

while True:
    display.fill((0,0,255))
    distance = pygame.math.Vector2(player.x, player.y).distance_to((teacher.x, teacher.y))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.QUIT

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pygame.mixer.Sound.play(throw_sound)
                player_bullets.append(PlayerBullet(player.x, player.y, mouse_x, mouse_y))

    keys = pygame.key.get_pressed()

    #pygame.draw.rect(display, (255,255,255), (100-display_scroll[0], 100-display_scroll[1], 16, 16))


    if keys[pygame.K_e]:
        print("interact")
    if keys[pygame.K_a]:
        display_scroll[0] -= 5

        player.moving_left = True
        print("Distance from NPC:", distance)

        for bullet in player_bullets:
            bullet.x += 5
    if keys[pygame.K_d]:
        display_scroll[0] += 5.

        player.moving_right = True
        print("Distance from NPC:", distance)
        for bullet in player_bullets:
            bullet.x -= 5
    if keys[pygame.K_w]:
        display_scroll[1] -= 5
        for bullet in player_bullets:
            bullet.y += 5
    if keys[pygame.K_s]:
        display_scroll[1] += 5
        for bullet in player_bullets:
            bullet.y -= 5


    

##    for event in pygame.event.get():
##        if event.type == pygame.KEYUP:
##            if event.key == pygame.K_a or event.key == pygame.K_d:
##                
##                if event.type == pygame.KEYDOWN:
##                    if distance <= 45 and event.key == pygame.K_e:
##                        print("interact")
        
        

    player.main(display)
    teacher.main(display)

    for bullet in player_bullets:
        bullet.main(display)


    
    clock.tick(60)
    pygame.display.update()
