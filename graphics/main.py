import pygame
import sys
import math
import ptext
import time
import mathcode
from time import sleep
from threading import Thread
global interact_man
import os
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

book_image = pygame.image.load("graphics/taskitems/Questionmark.png")
textbook_image = pygame.image.load("graphics/taskitems/book1.png")
pygame.display.set_icon(book_image)
pygame.display.set_caption("math game bing chilling")
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
doSpeechBook = False
teacherTalk = False
kidTalk = False
debugSet = False
clear = lambda: os.system('cls') #on Windows System

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
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
#Teacher
class Teacher:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def main(self, display):
        display.blit(pygame.transform.scale(teacher_image, (72, 72)), (100-display_scroll[0], 100-display_scroll[1]))


#The lil child
class Classmate:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x + 20, self.y, 28, 60)
    def main(self, display):
        display.blit(pygame.transform.scale(child_image, (32, 58)), (-100-display_scroll[0], -100-display_scroll[1]))
      
    
class Textbook:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def main(self, display):
        display.blit(pygame.transform.scale(textbook_image, (20, 25)), (800-display_scroll[0], 300-display_scroll[1]))
        
class Arrow:
    def __init__(self, x, y, width, height):
        self.x = player.x
        self.y = player.y + 20
        self.width = width
        self.height = height
        self.angle = math.atan2(y-player.y, x-player.x)
    def main(self, display):
        global degs
        rotated_arrow = (pygame.transform.rotate(arrow_image, degs))
        if kidTalk == False:
            rotated_and_scaled = (pygame.transform.scale(rotated_arrow, (0,0)))
        elif kidTalk == True:
            rotated_and_scaled = (pygame.transform.scale(rotated_arrow, (20,20)))

        display.blit(rotated_and_scaled, (player.x, player.y - 30))
        

#Not actually a bullet, thats just what the class is called.
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
#Poor attempt at a "debug mode".
def debug():
    global debugSet
    debugSet = not debugSet
    print(debugSet)

    if debugSet:
        for letter in badtimerlol:
            ptext.draw("Debug mode active!", (360, 227), width=10, fontname="text/dialogue.ttf", fontsize=50)
            clear()
            pygame.display.update()
    if not debugSet:
        for letter in badtimerlol:
            ptext.draw("Debug mode deactive!", (360, 227), width=10, fontname="text/dialogue.ttf", fontsize=50)
            pygame.display.update()
    
        



        
    



#defining stuff
player = Player(400, 300, 32, 32)
teacher = Teacher(300, 300, 32, 32)
classmate = Classmate(-100, -100, 32, 32)
textbook = Textbook(-100, -100, 32, 32)
arrow = Arrow(player.x, player.y, 32, 32)
display_scroll = [0,0]


#Dialogue system
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
                        #Skip the dialogue
                        print("rip bozo i dont remember asking")
                        #clear()
                        doText == False
                        pygame.display.update()
                        return
    #man is literally talking
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
                #arrow.main(display)
                kidtask()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        #Skips dialogue
                        print("rip bozo i dont remember asking")
                        doKidText == False
                        kidTask = True
                        kidtask()
                        pygame.display.update()
                        return
            pygame.display.update()
#When you talk to the kid he wants you to do a task.
def kidtask():
    global kidTask
    letterx = 25
    lettery = 100
    
    if kidTask == True and doKidText == False:
        pygame.draw.rect(display, red, (100,100,20,20))
        for letter in kidtaskspeech:
            letterx += 10
            pygame.time.wait(50)
            ptext.draw(kidtaskspeech, (letterx, 100), fontname="text/dialogue.ttf", fontsize=15)
            
            print("find the book")
        #book_image = pygame.image.load("graphics/taskitems/book1.png")
        pygame.display.update()
    


#When a button is pressed, move
def keypress():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        display_scroll[0] -= 4
        player.moving_left = True
        #print("Distance from NPC:", distance)
        interact = False
        for bullet in player_bullets:
            bullet.x += 5
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        display_scroll[0] += 4
        player.moving_right = True
        #print("Distance from NPC:", distance)
        interact = False
        for bullet in player_bullets:
            bullet.x -= 5
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        display_scroll[1] -= 5
        #print("Distance from NPC:", distance)
        interact = False
        for bullet in player_bullets:
            bullet.y += 5
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        display_scroll[1] += 5
        #print("Distance from NPC:", distance)
        interact = False
        for bullet in player_bullets:
            bullet.y -= 5

player_bullets = []


run = True
#Main loop
while run:
    
    global degs
    
    doText = False
    doKidText = False
    kidTask = False
    bookPress = False
    
    keypress()
    display.fill((0,0,255))
    distance = pygame.math.Vector2(player.x, player.y).distance_to((teacher.x, teacher.y))
    distancekid = pygame.math.Vector2(player.x, player.y).distance_to((classmate.x, classmate.y))
    distancebook = pygame.math.Vector2(player.x, player.y).distance_to((textbook.x, textbook.y))
    dx,dy = arrow.x-(800-display_scroll[0]),(player.y-30)-(300-display_scroll[1])

    rads = math.atan2(dx,dy)
    degs = (math.degrees(rads))
    degs = int(degs)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    

    #Quits the game when exit application
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
            run = False
        #Throws a ball. Not sure why.
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pygame.mixer.Sound.play(throw_sound)
                player_bullets.append(PlayerBullet(player.x, player.y, mouse_x, mouse_y))
                #print("Mouse coords: ", mouse_x, mouse_y)
                #print("Scroll: ", display_scroll[0], display_scroll[1])
                #print("Distance from book: ", distancebook)
                print("kidTask: ", kidTask)
                
        #Debug mode (that doesn't work). Used to assist in development.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F2:
                debug()
    #Detecting if the player is within a suitable range to interact.
    if distance <= 25 and display_scroll[1] <= -135 and display_scroll[1] >= -250:
        doSpeechMan = True
        #print("scroll from man:", display_scroll[1])
        pygame.time.delay(30)
        for event in pygame.event.get():
            #If e is pressed interact
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    doText = True
                    print("interact")
                    teacherTalk = True
        
    #If you are too far away you can't interact.
    else:
        doText = False
        doSpeechMan = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    #You must talk to the teacher before the kid.
                    if distancekid <= 535 and distancekid >= 500 and display_scroll[1] >= -500 and display_scroll[1] <= -320 and teacherTalk == False:
                        print("not yet")
    #Detects if player is within range to interact.
    if distancekid <= 535 and distancekid >= 500 and display_scroll[1] >= -500 and display_scroll[1] <= -320 and teacherTalk == True:
        doSpeechKid = True
        #print("distance from child", distancekid)
        #print("scroll:", display_scroll[1])
        pygame.time.delay(30)
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    doKidText = True
                    print("wassup my diggety dog")
                    kidTalk = True
    if distancebook <= 760 and distancebook >= 720 and display_scroll[1] >= -40 and display_scroll[1] <= 40 and kidTalk == True:
        #print("distance from book", distancebook)
        #print("scroll:", display_scroll[1])
        pygame.time.delay(30)
        doSpeechBook = True
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    bookPress = True
                    print("BOOK COLLECTED")
                    mathcode.bookmath()
    else:
        doSpeechKid = False

        

                
    #Creates speech bubbles allowing player to know when they are within interaction range.
    if doSpeechMan:
        
        display.blit(pygame.transform.scale(bubble_image, (72, 72)), (50-display_scroll[0], 75-display_scroll[1]))
        ptext.draw("Press E", (60-display_scroll[0], 90-display_scroll[1]), color="black", fontname="text/Pixel-y14Y.ttf", fontsize=10)

    if doSpeechKid:
        display.blit(pygame.transform.scale(bubble_image, (72, 72)), (-150-display_scroll[0], -130-display_scroll[1]))
        ptext.draw("Press E", (-140-display_scroll[0], -115-display_scroll[1]), color="black", fontname="text/Pixel-y14Y.ttf", fontsize=10)
    if doSpeechBook:
        display.blit(pygame.transform.scale(bubble_image, (72, 72)), (730-display_scroll[0], 265-display_scroll[1]))
        ptext.draw("Press E", (740-display_scroll[0], 280-display_scroll[1]), color="black", fontname="text/Pixel-y14Y.ttf", fontsize=10)
    
    speaking()
    #pygame.display.update()
    

    #pygame.draw.rect(display, (255,255,255), (100-display_scroll[0], 100-display_scroll[1], 16, 16))


        
        
#Displaying all this stuff
    player.main(display)
    teacher.main(display)
    classmate.main(display)
    textbook.main(display)
    arrow.main(display)
    for bullet in player_bullets:
        bullet.main(display)


    #Supposedly setting the fps to 60
    clock.tick(60)
    pygame.display.update()
    
