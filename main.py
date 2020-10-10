import pygame
import random                              #for randomisation
import math                                #for distance calculations
from pygame import mixer                   #for adding wav and mp3 files 

 # initialize the pygame
pygame.init()

 # create the screen
screen=pygame.display.set_mode((800,600))

#background
backgroundimg=pygame.image.load("background.png")   #image is loaded in a respective variable
mixer.music.load("background.wav")                  #we are using music func here so that we can play our song in a loop 
mixer.music.play(-1)                                #-1 makes the song play in a loop

#title and icon
pygame.display.set_caption("Space Invader")        #title of the game
icon=pygame.image.load("icon.png")                 #game icon
pygame.display.set_icon(icon)                      #to display icon

#player
playerimg=pygame.image.load("player.png")
playerx=370                                        #x coordinates
playery=500                                        #y coordinates
playerx_change=0                                   #declared for movement 


#score 
score_value=0                                      #variable which carries our score
font = pygame.font.Font("freesansbold.ttf",17)     #the font in which our score is showed and the size   
textx=5                                            #x coordinate for the score
texty=5                                            # y coordinate for the score

def show_score(x,y):                                                                #dunction to show score  
    score = font.render("score :" + str(score_value), True , (255,255,255))         #we are rendering our text and changing the datatype of score to string so that we can print followed by rgb values 
    screen.blit(score,(x,y))                                                        #we are showing score at given coordinates 


#game over text
over_font=pygame.font.Font("freesansbold.ttf",50)                      #the font im which our game over text is going to be printed followed by size 

def game_over_text():                                                  #function defined for showing game over 
    over_text=over_font.render("GAME OVER", True , (255,255,255))      #rendering our game over text followed by RGB values 
    screen.blit(over_text,(250,300))                                   #showing our text at given coordinates 
    noiceimg=pygame.image.load("noice.png") 
    screen.blit(noiceimg,(500,50))


def player(x,y):                         #function for placing image of player 
    screen.blit(playerimg,(x,y))         #showing the image for respective coordinates 


#multiple enemies
enemyimg=[]                              #  list for enemy images 
enemyx=[]                                #  list for enemy x coordinates
enemyy=[]                                #  list for enemy y coordinates
enemyx_change=[]                         #  list for enemy change x coordinates
enemyy_change=[]                         #  list for enem  change y coordinates
num_of_enemies=6                         #  no of enemies to be spawned 

#enemy
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("ufo.png"))   #loading our enemy picture 
    enemyx.append(random.randint(0,735))            #randomint so that the enemy gets spawn in an random location #(x coordinates)
    enemyy.append(random.randint(50,150))           # for y coordinates
    enemyx_change.append(1.75)                      #for initial movement 
    enemyy_change.append(35)                        #moves towards the spaceship when it reaches the boundaries/limits


def enemy(x,y,i):                                   #function for placing enemy image
    screen.blit(enemyimg[i],(x,y))


#bullet
bulletimg=pygame.image.load("bullet.png")          #bullet image is loaded
bulletx=0                                          #bullet coordinate x is initialised to 0
bullety=500                                        #bullet y coordinate is initialised to 500 so it is same as spaceship
bulletx_change=0                           
bullety_change=5                                   #the rate at which we want the bullet to go up
bullet_state="ready"                               #state of bullet

def fire_bullet(x,y):                              #function for firing the bullet
    global bullet_state                            #we called bulletstate as global so that it can be accessed from outside 
    bullet_state="fire"                            #bulletstate is changed to fire 
    screen.blit(bulletimg,(x+16,y+10))             #bullet image is added to the screen and x+16 so that the bullet comes from the centre of the space ship and y+10 so it creates a effect that the bullet is released from the tip of spaceship

def iscollision(enemyx,enemyy,bulletx,bullety):    #function for collision
    a=(enemyx-bulletx)                             #x1-x2                      
    b=(enemyy-bullety)                             #y1-y2 
    distance=math.sqrt(a**2 + b**2)                #so we are basically using the math formula for calculating the distances btw 2 points (square root((x1-x2)**2+(y1-y2)**2))
    if distance<27:                                #if the distance is less than 27 px we are calling it as a collision
        return True 
    else:
        return False    
        

#game loop
running=True                                          # we declared a varible to run pygame
while running:                                        # it gets executed as variable is true
    # fill((R,G,B))    
    screen.fill((0,0,0))                              # to change the background colour

    #backgroung image
    screen.blit(backgroundimg,(0,0))                  #background is added 404kb

    for event in pygame.event.get():                  #anything we do in pygame is called an event 
        if event.type==pygame.QUIT:                   #if we want to close pygame then we have to stop the while loop
            running=False                             # so if we press "X" on margins it makes the variable false hence stopping the loop

        # key allotments
        if event.type==pygame.KEYDOWN:                #keydown in the sense "key is pressed"
            if event.key==pygame.K_a:                 #(K_a == key a on keyboard) key is assigned to move the image left 
                 playerx_change=-3                    #if we press key a then the image is moved left by 0.3 
            if event.key==pygame.K_d:                 #(K_d == key a on keyboard) key is assigned to move the image right 
                playerx_change=3                      #if we press key d then the image is moved right by 0.3
            if event.key==pygame.K_SPACE:             #if spacebar is pressed then the firebullet function is called 
                if bullet_state is "ready":           #if the state of bullet is read then we fire it
                    bsound=mixer.Sound("laser.wav")   #loading bullet SOUND(we are using sound instead of music coz we dont want it to play in loops )
                    bsound.play()                     #playing the sound 
                    bulletx=playerx                   #so the initial x coordinate for the bullet is spaceship location
                    fire_bullet(bulletx,bullety)      #bullet is fired by calling this fucntion
                 
        if event.type==pygame.KEYUP:                  #keyup in the sense "key is left"
            if event.key==pygame.K_a or event.key==pygame.K_d:  
                 playerx_change=0                     #when the key is not pressed then the movement is zero


    playerx+=playerx_change                           #the change of position from ideal spwan position
    if playerx<=0:                                    #we are creating boundries for the image it can even go into -ve x cordinates so we stop it here 
        playerx=0                                     #what we do here is if x goes into -ve values then it is brought back to zero..where the process is insanely fast and not visible to human eye 
    elif playerx>=736:                                #its the same thing here but when image reaches 800 x cordinate then we get it back to 736
        playerx=736                                   #so why 736? image size is 64x64 pixels so (800-64)pixels


    #enemy movement
    for i in range(num_of_enemies):                  #for loop is called here coz we want to refer to all the enemies in the lsit

        #game over
        if enemyy[i]>=450:                           #game over when the enemies y coordinates touch 450 point
            for j in range(num_of_enemies):          #we called another loop here coz we want move the enemies of our visibility  
                enemyy[j]=2000                       #so we gave it a value of 2000 which is not visible to us and creating empty space for our game over text
            game_over_text()                         #game over function is called
            break                                    #we stop our loop here 


        enemyx[i]+=enemyx_change[i]                  #change of enemy position from ideal spwan position
        if enemyx[i]<=0:                             #when enemy touches the min limit of x axis
            enemyx_change[i]=1.75                    #we want him to move towards the max limit of x axis
            enemyy[i]+=enemyy_change[i]              #we want him to also get closer to the spaceship
        elif enemyx[i]>=736:                         #when enemy touches the max of x axis
            enemyx_change[i]=-1.75                   #we want him to move towards min limit of x axis
            enemyy[i]+=enemyy_change[i]              #we want him to move towards the spaceship by closing of the distance

        #collision
        collision=iscollision(enemyx[i],enemyy[i],bulletx,bullety) 
        if collision:                                                 #if collision is true then
            collisionsound=mixer.Sound("explosion.wav")               #sound when our collision takes place
            collisionsound.play()                                     #sound is played
            bullety=500                                               #when collision takes place we want the bullet to comeback to our shapeship y coordinate 
            bullet_state="ready"                                      #we change the bullet state so that it is ready to fire again
            score_value+=1                                            # for every collision score increases by 1
            enemyx[i]=random.randint(0,735)                           #randomint so that the enemy gets spawn in an random location #(x coordinates)
            enemyy[i]=random.randint(10,200)                          #for y coordinates
         
        enemy(enemyx[i],enemyy[i],i)                                  #we want our all enemies to appear so we call this function

    #bullet respwan
    if bullety<=0:                                  #if we dont give this statement our bullet goes into -ve y cordinates
        bullety=500                                 #if our bullet touches 0 or -ve value on y axis then it is brought back to ship 
        bullet_state="ready"                        #so we with this line we make our bullet ready to fire 
    if bullet_state is 'fire':                      #when we press spacebar the bulletstate is changed to fire
        fire_bullet(bulletx,bullety)                #when bullet state is fire then we fire the bullet using this function
        bullety-=bullety_change                     #we want the bullet to move towards up i.e towards the min limit of y axis creating the bullet travel        

    player(playerx,playery)                         #image is placed with this function    
    show_score(textx,texty)                         #score is showed using this function
    pygame.display.update()                         #this updates the things on screnn right from background colour to the image positional changes 
