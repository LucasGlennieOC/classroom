import pygame
import sys
import math
import ptext
import time

global interact_man

pygame.init()
#changing the cursor to a crosshair
pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
#stuff
display = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
#sounds
throw_sound = pygame.mixer.Sound("throw.mp3")
#images
player_walk_images = [pygame.image.load("graphics/run1.png"), pygame.image.load("graphics/run2.png"), pygame.image.load("graphics/run3.png"), pygame.image.load("graphics/run4.png")]
player_idle_images = [pygame.image.load("graphics/idle/idle.png"), pygame.image.load("graphics/idle/idle1.png"), pygame.image.load("graphics/idle/idle2.png"), pygame.image.load("graphics/idle/idle4.png"), pygame.image.load("graphics/idle/idle5.png"), pygame.image.load("graphics/idle/idle6.png"), pygame.image.load("graphics/idle/idle7.png")]
teacher_image = pygame.image.load("graphics/teacher.png")
bubble_image = pygame.image.load("graphics/speech.png")
child_image = pygame.image.load("graphics/child.png")

interact_man = False





class Player:
    def __init__(self, x, y, width, height):
        #damn thats a lot of self
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_count = 0
        self.idle_count = 0
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
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
            if self.moving_up:
                self.y += 2
                display.blit(pygame.transform.scale(player_walk_images[self.animation_count//4], (32, 42)), (self.x, self.y))
            elif self.moving_down:
                self.y -= 2
                display.blit(pygame.transform.scale(player_walk_images[self.animation_count//4], (32, 42)), (self.x, self.y))
        elif self.moving_left:
            self.x -= 2
            display.blit(pygame.transform.scale(pygame.transform.flip(player_walk_images[self.animation_count//4], True, False), (32, 42)), (self.x, self.y))
            if self.moving_up:
                self.y += 2
                display.blit(pygame.transform.scale(pygame.transform.flip(player_walk_images[self.animation_count//4], True, False), (32, 42)), (self.x, self.y))
            elif self.moving_down:
                self.y -= 2
                display.blit(pygame.transform.scale(pygame.transform.flip(player_walk_images[self.animation_count//4], True, False), (32, 42)), (self.x, self.y))
        elif self.moving_up:
            self.y += 2
            display.blit(pygame.transform.scale(pygame.transform.flip(player_walk_images[self.animation_count//4], True, False), (32, 42)), (self.x, self.y))
        elif self.moving_down:
            self.y -= 2
            display.blit(pygame.transform.scale(pygame.transform.flip(player_walk_images[self.animation_count//4], True, False), (32, 42)), (self.x, self.y))

        else:
            display.blit(pygame.transform.scale(player_idle_images[self.idle_count//8], (32, 42)), (self.x, self.y))
        #pygame.draw.rect(display, (255, 0, 0), (self.x, self.y, self.width, self.height))
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

class Teacher:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def main(self, display):
        display.blit(pygame.transform.scale(teacher_image, (72, 72)), (100-display_scroll[0], 100-display_scroll[1]))


class Classmate:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def main(self, display):
        display.blit(pygame.transform.scale(child_image, (45, 45)), (-100-display_scroll[0], -100-display_scroll[1]))
      
    


    
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
    


def interactman():
    interact_man = True
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            interact_man = False
    while interact_man:
        ptext.draw("bing chilling", (20, 100), fontname="text/Pixel-y14Y.ttf", fontsize=60)
        pygame.display.update()
        if distance >= 25:
            interact_man = False


#defining stuff
player = Player(400, 300, 32, 32)
teacher = Teacher(300, 300, 32, 32)
classmate = Classmate(-100, -100, 32, 32)
display_scroll = [0,0]

def keypress():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        display_scroll[0] -= 4
        player.moving_left = True
        print("Distance from NPC:", distance)
        interact = False
        for bullet in player_bullets:
            bullet.x += 5
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        display_scroll[0] += 4
        player.moving_right = True
        print("Distance from NPC:", distance)
        interact = False
        for bullet in player_bullets:
            bullet.x -= 5
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        display_scroll[1] -= 5
        #player.moving_up = True
        print("Distance from NPC:", distance)
        interact = False
        for bullet in player_bullets:
            bullet.y += 5
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        display_scroll[1] += 5
        #player.moving_down = True
        print("Distance from NPC:", distance)
        interact = False
        for bullet in player_bullets:
            bullet.y -= 5

player_bullets = []

doText = False
doSpeechMan = False
doSpeechKid = False

#Main loop
while True:
    keypress()
    display.fill((0,0,255))
    distance = pygame.math.Vector2(player.x, player.y).distance_to((teacher.x, teacher.y))
    distancekid = pygame.math.Vector2(player.x, player.y).distance_to((classmate.x, classmate.y))
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if doText:
        ptext.draw("bing chilling", (20, 100), fontname="text/Pixel-y14Y.ttf", fontsize=60)
    if doSpeechMan:
        display.blit(pygame.transform.scale(bubble_image, (72, 72)), (50-display_scroll[0], 75-display_scroll[1]))
    if doSpeechKid:
        display.blit(pygame.transform.scale(bubble_image, (72, 72)), (-150-display_scroll[0], -130-display_scroll[1]))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pygame.mixer.Sound.play(throw_sound)
                player_bullets.append(PlayerBullet(player.x, player.y, mouse_x, mouse_y))
        if event.type == pygame.KEYDOWN:
            if distance <= 25:
                doSpeechMan = True
                if event.key == pygame.K_e:
                    doText = True
                    print("interact")
            if distance >= 25:
                doText = False
                doSpeechMan = False
                pygame.display.update()
            if distancekid <= 550 and distancekid >= 500:
                doSpeechKid = True
                if event.key == pygame.K_e:
                    print("wassup my diggety dog")
            else:
                doSpeechKid = False
                pygame.display.update()
                

                        
        pygame.display.update()
    

    #pygame.draw.rect(display, (255,255,255), (100-display_scroll[0], 100-display_scroll[1], 16, 16))


##Key presses such as movement    

##    for bullet in player_bullets:
##            
##        if bullet.sprite.collide_rect(teacher):
##            print("collided")



##
##    

##    
##                

        
        
#epic
    player.main(display)
    teacher.main(display)
    classmate.main(display)
    for bullet in player_bullets:
        bullet.main(display)


    
    clock.tick(60)
    pygame.display.update()
