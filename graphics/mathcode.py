import pygame
import math
import random


def bookmath():
    numbera = random.randint(1,10)
    numberb = random.randint(1,10)
    print("PROBLEM: ", numbera, " + ", numberb, " = ?")
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                print("1")
            if event.key == pygame.K_2:
                print("2")
            if event.key == pygame.K_3:
                print("3")
            if event.key == pygame.K_4:
                print("4")
            if event.key == pygame.K_5:
                print("5")
            if event.key == pygame.K_6:
                print("6")
            if event.key == pygame.K_7:
                print("7")
            if event.key == pygame.K_8:
                print("8")
            if event.key == pygame.K_9:
                print("9")
