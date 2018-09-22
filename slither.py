#continue from 18
import pygame
import time
import random

pygame.init()   

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0, 155,0)

display_width = 800
display_height = 600
 
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Slither')

pygame.display.update()  # updates the entire thing unless region is mentioned
icon = pygame.image.load('apple.png')
pygame.display.set_icon (icon)

image = pygame.image.load('snakehead.png')
appleimage = pygame.image.load('apple.png')
clock = pygame.time.Clock()

AppleThickness = 30 
block_size = 20
FPS =15


direction = "right"

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 75)

def pause():
     paused = True
     message_to_screen("Paused", black, -100, size ="large")
     message_to_screen("Press C to Continue or Q to quit", black,25, size ="small")
     pygame.display.update()
     while paused:
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

               if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                         paused = False

                    elif event.key == pygame.K_q:
                         pygame.quit()
                         quit()
               

              
               clock.tick(5)
def score(score):
     text = smallfont.render("Score: "+str(score), True, black)
     gameDisplay.blit(text, [0,0])
     
def randAppleGen():
     randAppleX = round(random.randrange(0, display_width-AppleThickness))
     randAppleY = round(random.randrange(0, display_height-AppleThickness ))
     return randAppleX, randAppleY


def game_intro():
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                     pygame.quit()
                     quit()
        gameDisplay.fill(white)
        message_to_screen("Welcome to Slither", green, -100, "large")
        message_to_screen("The aim is to eat red apples", black, 30)
        message_to_screen("More apples you eat, the longer you get", black, 70)
        message_to_screen("If you run into yourself, or the edges, you die", black, 110)
        message_to_screen("Press C to continue, P to pause or Q to quit", black, 180)

        pygame.display.update()
        clock.tick(15)
        
def snake(block_size, snakeList) :

     if direction == "right":
         head = pygame.transform.rotate(image, 270)

     if direction == "left":
         head = pygame.transform.rotate(image, 90)

     if direction == "up":
         head = image

     if direction == "down":
         head = pygame.transform.rotate(image, 180)
         
     gameDisplay.blit(head, (snakeList[-1][0],snakeList[-1][1]))
     for XnY in snakeList[:-1]:
         pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],block_size,block_size])  # x y width height

def text_objects(text, color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface,textSurface.get_rect()

def message_to_screen(msg,color, y_displace =0,size = "small"):
    textSurface , textRect = text_objects(msg,color,size)
    textRect.center = (display_width/2), (display_height/2) + y_displace
    gameDisplay.blit(textSurface,textRect)
    
def gameLoop():
    global direction
    direction = "right"
    gameExit = False
    gameOver = False

    lead_x =display_width/2
    lead_y =display_height/2
    
    lead_x_change =10
    lead_y_change =0

    snakeList = []  #the exiting snake remains and then new is created when its called
    snakeLength = 1


    randAppleX, randAppleY = randAppleGen()
    while not gameExit:
        if gameOver == True:
            message_to_screen("Game Over ", red,y_displace=  -20,size = "large")
            message_to_screen("Press c to continue or q to quit", black, y_displace= 50)

            pygame.display.update()

             
        while gameOver == True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False

                    if event.key == pygame.K_c:
                        gameLoop()
        for event  in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change =0#if we dont make this zero it seems as if we are moving diagonally
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change =0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change =0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change =0
                elif event.key == pygame.K_p:
                     pause()
            #if event.type == pygame.KEYUP:
               # if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                #    lead_x_change = 0

   
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(white)  #clearing , faster

        
        #pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])

        gameDisplay.blit(appleimage, (randAppleX, randAppleY))

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len (snakeList) > snakeLength:  #everytime the list increments by 1 so we decrement by 1 by deleting the first element 
            del snakeList[0]

        for eachSegment in snakeList[:-1] : # till -1 means till end 
            if eachSegment == snakeHead:
                gameOver = True
        snake(block_size,snakeList)

        score(snakeLength-1)

        pygame.display.update()


        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:
            if(lead_y > randAppleY and lead_y < randAppleY + AppleThickness):
                 randAppleX, randAppleY = randAppleGen()
                 snakeLength += 1
            elif( lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness):
                 randAppleX, randAppleY = randAppleGen()
                 snakeLength += 1
            
        clock.tick(FPS)

    pygame.quit()

    quit()
game_intro()
gameLoop()
