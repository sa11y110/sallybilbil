import pygame
import asyncio
import random
import sys

import os

#----Initiate pygame 
pygame.init()

#-------Clock
clock = pygame.time.Clock()

#------Game active status for restart 
gaktiv = True 

#--------Screen w, h
dis_width = 380
dis_height = 640

#-----Width and Height for Enemy
x = (dis_width * 0.14)
y = (dis_height * 0.75)

#-----Main speed for Player and Enemy
speed = 3

#----Screen
screen = pygame.display.set_mode((dis_width, dis_height))

#----Caption for pygame window 
pygame.display.set_caption("Testtest")

#-----Game over
font = pygame.font.Font(None,74) 
gameover = font.render("Game Over", True, (255,0,0)) #---Renders font 
moving_left =False #----False so usage och if true func is avaliable 
moving_right =False

#------Player 
bilimg = pygame.image.load("img/bil racer.png")
bilimg = pygame.transform.scale(bilimg, (150,150)) # img size
bilimg_rect = bilimg.get_rect(topleft=(150,150)) #hitbox

bilbox = bilimg_rect.inflate(-80,-17) # hitbox size!! 


RED = (255,0,0) #----Color for hitbox 

#Button 
main_font = pygame.font.SysFont("purisa", 50) #--Font


#CLASSES ---------------------------------

#---Background class 
class Bg():
    def __init__(self, screen):
        self.screen = screen

        #---- Loading and Scaling img
        self.image = pygame.image.load("img/bakgrund.jpg")
        self.image = pygame.transform.scale(self.image, (dis_width, dis_height))
        
        #----Two postitions on img for "scrolling down effect"
        self.y1 = 0
        self.y2 = -dis_height  # pos sec img on first img 

    def update(self, speed):
        #---scrolling speed
        self.y1 += speed
        self.y2 += speed

        #---reseting pos 
        if self.y1 >= dis_height:
            self.y1 = -dis_height

        if self.y2 >= dis_height:
            self.y2 = -dis_height

    def draw(self):
        #---Draw background 
        self.screen.blit(self.image, (0, self.y1))
        self.screen.blit(self.image, (0, self.y2))

#----Enemy class 
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Enemy,self).__init__() #--calls base class
        self.image = pygame.image.load("img/e/kon-kon.png") 
        self.image = pygame.transform.scale(self.image, (200, 200)) #--img scale 
        self.rect = self.image.get_rect(center=(x,y)) #--hitbox 
        self.box = self.rect.inflate(-170,-170)#--hitbox size
        self.speed = 3 #--enemy speed

    def update(self):
        self.rect.y += self.speed + speed #--moving down "scrolling down effect"
        self.box.center = self.rect.center #--hitbox

        if self.rect.y > dis_height: #-- reset at top if not on screen
            self.rect.y = -self.rect.height 
            self.rect.x = random.randint(0, dis_width - self.rect.width) #--rand x pos
            

        
        
     #---Draws enemy and hitbox to screen
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, RED, self.box, 2)
        
    
#---Button class 
class button():
    def __init__(self, image, x_pos, y_pos, text_input):
        self.image = image
        self.x_pos = x_pos 
        self.y_pos = y_pos 
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
         

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
    
    #--change color to green if mouse hovers over if not show text as white
    def changeColor(self, position):
       if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
           self.text = main_font.render(self.text_input, True, "green")

       else:
           self.text = main_font.render(self.text_input, True, "white")


button_surface = pygame.image.load("img/e/8bitbutton.png")
button_surface = pygame.transform.scale(button_surface,(600, 600))

button = button(button_surface, 195,200, "Play Again?")
#Clicked 
def clicked(event,position):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if position[0] in range(button.rect.left, button.rect.right) and position[1] in range(button.rect.top, button.rect.bottom):
            reset_game()


#--Reset game
def reset_game():
    #Recalling each variable 
    global x,y, speed, cone, timer, gaktiv
    x = dis_width * 0.14
    y = dis_height * 0.75
    speed = 3
    timer = pygame.time.get_ticks()
    gaktiv = True

    cone.empty()
    spacing = 170

    for i in range(3): # Cone random spawn
        enemy_x = random.randint(0, dis_width - 100)
        enemy_y = i * -spacing 
        enemy = Enemy(enemy_x, enemy_y)
        cone.add(enemy)

#Objects 
bgimg = Bg(screen)
#Enemy object 
cone = pygame.sprite.Group()
#Spacing between cones
spacing = 170


for i in range(3): # Cone random spawn
    enemy_x = random.randint(0, dis_width - 100)
    enemy_y = i * -spacing 
    enemy = Enemy(enemy_x, enemy_y)
    cone.add(enemy)

timer = pygame.time.get_ticks()
#main 

#--async def to make pygbag executable ---main
async def main():
    #recalling movements 
    global x, moving_left, moving_right, gaktiv
    run = True
    while run:
        # Fps 
        clock.tick(60)
        #Check if code is working
        print(os.getcwd())
        print(os.listdir())
    
    #timer
        tid = pygame.time.get_ticks() - timer
        
        #bg update
        bgimg.update(speed)

        #button updt
        button.update()
        button.changeColor(pygame.mouse.get_pos())
        


        #player movement
        if moving_left and x > 0:
            x -= speed
        if moving_right and x < dis_width-bilimg.get_width():
            x += speed
        #background
        screen.fill((255,255,255))

        #draws background
        bgimg.draw()
        if gaktiv:
            cone.update()

            cone.draw(screen)
            
            bilimg_rect.topleft = (x,y)
            bilbox.center = bilimg_rect.center
            screen.blit(bilimg, bilimg_rect)
            pygame.draw.rect(screen, RED, bilbox,2)
            
            #--Collision 
            for enemy in cone:
                enemy.draw(screen)
                if bilbox.colliderect(enemy.box):
                    gaktiv = False
                    screen.blit(gameover, ((dis_width - gameover.get_width()) // 2, (dis_height - gameover.get_height()) // 2))
                    pygame.display.flip()
                
        else: 
            button.update()
                    
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
             run = False
             pygame.display.quit()
             sys.exit()

            if gaktiv:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        moving_left = True
                    if event.key == pygame.K_RIGHT:
                        moving_right = True


                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        moving_left = False
                    if event.key == pygame.K_RIGHT:
                        moving_right = False
            else: 
                clicked(event, pygame.mouse.get_pos())



        #---Update display 
        pygame.display.update()   
        await asyncio.sleep(0)
        if not run:
            pygame.quit() 
        


    pygame.quit()
    sys.exit()

asyncio.run(main())