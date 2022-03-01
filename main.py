import pygame
import sys
import math
import ptext
import time
from time import sleep
from threading import Thread
global interact_man

pygame.init()
#changing the cursor to a crosshair
pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
width = 800
height = 600
#stuff
display = pygame.display.set_mode((800,600))
game_surf = pygame.surface.Surface((width, height))
clock = pygame.time.Clock()
#sounds
throw_sound = pygame.mixer.Sound("throw.mp3")
#images, fonts, etc
player_walk_images = [pygame.image.load("graphics/run1.png"), pygame.image.load("graphics/run2.png"), pygame.image.load("graphics/run3.png"), pygame.image.load("graphics/run4.png")]
player_idle_images = [pygame.image.load("graphics/idle/idle.png"), pygame.image.load("graphics/idle/idle1.png"), pygame.image.load("graphics/idle/idle2.png"), pygame.image.load("graphics/idle/idle4.png"), pygame.image.load("graphics/idle/idle5.png"), pygame.image.load("graphics/idle/idle6.png"), pygame.image.load("graphics/idle/idle7.png")]
teacher_image = pygame.image.load("graphics/teacher.png")
bubble_image = pygame.image.load("graphics/speech.png")
child_image = pygame.image.load("graphics/child.png")
myfont = pygame.font.SysFont("monospace", 15)
arrow_image = pygame.image.load("graphics/arrow.png")
interact_man = False
#colour definitions
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
blue     = (  20,  90, 150)
green    = (   0, 255,   0)
dkgreen  = (   0, 100,   0)
red      = ( 200,  60,   60)
purple   = (0xBF,0x0F,0xB5)
brown    = (0x55,0x33,0x00)

#Dialogue
dialogue = "Hey there! Welcome to the game!         "
kidDialogue = "Hey you! I lost my homework. Can you help me find it?     "
kidtaskspeech = "Find the book!"
badtimerlol = "A A A A A A A A A A A A A A A A A AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
#Deciding if things are true
doSpeechMan = False
doSpeechKid = False
teacherTalk = False
debugSet = False


#player class
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
        self.hitbox = (self.x + 20, self.y, 28, 60)
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
    
def debug():
    global debugSet
    debugSet = not debugSet
    print(debugSet)

    if debugSet:
        for letter in badtimerlol:
            ptext.draw("Debug mode active!", (360, 227), width=10, fontname="text/dialogue.ttf", fontsize=50)
            pygame.display.update()
    if not debugSet:
        for letter in badtimerlol:
            ptext.draw("Debug mode deactive!", (360, 227), width=10, fontname="text/dialogue.ttf", fontsize=50)
            pygame.display.update()
    
        




        
    
 ##def interactman():
##    interact_man = True
##    if event.type == pygame.KEYDOWN:
##        if event.key == pygame.K_r:
##            interact_man = False
##    while interact_man:
##        #
##        pygame.display.update()
##        if distance >= 25:
##            interact_man = False


#defining stuff
player = Player(400, 300, 32, 32)
teacher = Teacher(300, 300, 32, 32)
classmate = Classmate(-100, -100, 32, 32)
display_scroll = [0,0]



def speaking():
    
    global doText
    global doKidText
    global kidTask
    if doText:
        display.fill((0,0,255))
        display.blit(pygame.transform.scale(teacher_image, (500,500)), (150,200))
        letterx = 100
        lettery = 100
        letter1 = len(dialogue)
        
        for letter in dialogue:
            letterx += 20
            pygame.time.wait(50)
            print(letter)
            ptext.draw(letter, (letterx, 100), fontname="text/dialogue.ttf", fontsize=30)
            pygame.display.update()
            doText = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        print("did not ask")
                        doText == False
                        pygame.display.update()
                        return
            #label = myfont.render(letter, 1, (255,255,0))
            #display.blit(label, (letterx, 100))
    if doKidText:
        display.fill((0,0,255))
        display.blit(pygame.transform.scale(child_image, (500,500)), (150,200))
        letterx = 25
        lettery = 100
        for letter in kidDialogue:
            letterx += 13
            pygame.time.wait(50)
            print(letter)
            ptext.draw(letter, (letterx, 100), width=10, fontname="text/dialogue.ttf", fontsize=20)
            print(letterx)
            if letterx == 779:
                doKidText = False
                kidTask = True
                kidtask()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        print("did not ask")
                        doKidText == False
                        pygame.display.update()
                        return
            pygame.display.update()
def kidtask():
    letterx = 25
    lettery = 100
    if kidTask == True and doKidText == False:
        pygame.draw.rect(display, red, (100,100,20,20))

        for letter in kidtaskspeech:
            letterx += 10
            pygame.time.wait(50)
            ptext.draw(kidtaskspeech, (letterx, 100), fontname="text/dialogue.ttf", fontsize=15)
        
            print("find the book")
        pygame.display.update()
    




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



#Main loop
while True:
    
    
    doText = False
    doKidText = False
    keypress()
    display.fill((0,0,255))
    distance = pygame.math.Vector2(player.x, player.y).distance_to((teacher.x, teacher.y))
    distancekid = pygame.math.Vector2(player.x, player.y).distance_to((classmate.x, classmate.y))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pygame.mixer.Sound.play(throw_sound)
                player_bullets.append(PlayerBullet(player.x, player.y, mouse_x, mouse_y))
                print(mouse_x, mouse_y)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F2:
                debug()
        if distance <= 25 and display_scroll[1] <= -135 and display_scroll[1] >= -250:
            print("scroll from man:", display_scroll[1])
            doSpeechMan = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    doText = True
                    print("interact")
                    teacherTalk = True
        if distance >= 25 and display_scroll[1] >= -135 and display_scroll[1] <= -250:
            doText = False
            doSpeechMan = False

        
        if distancekid <= 535 and distancekid >= 500 and display_scroll[1] >= -500 and display_scroll[1] <= -320 and teacherTalk == False:
            print("not yet")
        if distancekid <= 535 and distancekid >= 500 and display_scroll[1] >= -500 and display_scroll[1] <= -320 and teacherTalk == True:
            print("distance from child", distancekid)
            print("scroll:", display_scroll[1])
            doSpeechKid = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    doKidText = True
                    print("wassup my diggety dog")
        else:
            doSpeechKid = False

                

    if doSpeechMan:
        
        display.blit(pygame.transform.scale(bubble_image, (72, 72)), (50-display_scroll[0], 75-display_scroll[1]))
        ptext.draw("Press E", (60-display_scroll[0], 90-display_scroll[1]), color="black", fontname="text/Pixel-y14Y.ttf", fontsize=10)

    if doSpeechKid:
        display.blit(pygame.transform.scale(bubble_image, (72, 72)), (-150-display_scroll[0], -130-display_scroll[1]))
        ptext.draw("Press E", (-140-display_scroll[0], -115-display_scroll[1]), color="black", fontname="text/Pixel-y14Y.ttf", fontsize=10)
    
    speaking()
    #pygame.display.update()
    

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
    
