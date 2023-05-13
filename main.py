import pygame
from pygame.math import Vector2
import os
from pygame import mixer
import button
import random
import csv
import random


#intalize the pygame
mixer.init()
pygame.init()
pygame.font.init()
#sets the fps
clock =pygame.time.Clock()
fps=60


SCREEN_WUDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300
screen = pygame.display.set_mode((SCREEN_WUDTH, SCREEN_HEIGHT))


BLACK=(0,0,0)
def bg():
    screen.fill((255,191,0))
    draw_background()


def the_end():
    the_end=pygame.image.load('DinoAssets/death fade/the end.png').convert_alpha()
    the_end=pygame.transform.scale(the_end,(800,640))
    screen.blit(the_end,(0,0))


def menu_bg():
    menu_background=pygame.image.load('DinoAssets/background/Background.png').convert_alpha()
    menu_background=pygame.transform.scale(menu_background,(800,640))
    screen.blit(menu_background,(0,0))



def draw_background():
    screen.fill(GREEN)
    width = blue_img.get_width()
    for x in range(6):
        screen.blit(blue_img, ((x*width)-bg_scroll*.5,0))
        screen.blit(tree,((x*width)-bg_scroll * .7,SCREEN_HEIGHT-tree.get_height()-250))
        screen.blit(tree2,((x*width)-bg_scroll * .8,SCREEN_HEIGHT-tree2.get_height()-250))
        screen.blit(water,((x*width)-bg_scroll * .9,SCREEN_HEIGHT-water.get_height()-00))
        screen.blit(logs,((x*width)-bg_scroll * 1,SCREEN_HEIGHT-logs.get_height()-00))

#function to reset level
def reset_level():
    enemy_group.empty()
    item_group.empty()
    exit_group.empty()
    lava_group.empty()
    decor_group.empty()
    exit_group.empty()
    
    #level reset
    data=[]
    for row in range(ROWS):
        r=[-1]*COLLUMNS
        data.append(r)
    return data
    


#game variables
GRAVITY= 0.75
ROWS=16
COLLUMNS=150
SCROLL_THRESH=200
TILE_SIZE= SCREEN_HEIGHT // ROWS
TILE_TYPES=24
screen_scroll=0
start_game=False
#scroll=0
bg_scroll=0
level=0
MAX_LEVELS=2
start_intro=False

#load ui
sound=pygame.image.load('DinoAssets/better with sound.png').convert_alpha()
play_button=pygame.image.load('DinoAssets/ui/tile001.png').convert_alpha()
exit_button=pygame.image.load('DinoAssets/ui/tile052.png').convert_alpha()
play_music=pygame.image.load('DinoAssets/ui/tile012.png').convert_alpha()
stop_music=pygame.image.load('DinoAssets/ui/tile049.png').convert_alpha()
restart_button=pygame.image.load('DinoAssets/ui/tile003.png').convert_alpha()
title=pygame.image.load('DinoAssets/logo.png').convert_alpha()

#load image
#loads the game's background
blue_img=pygame.image.load('DinoAssets/background/1.png').convert_alpha()
blue_img=pygame.transform.scale(blue_img,(800+300,320))
tree=pygame.image.load('DinoAssets/background/2.png').convert_alpha()
tree=pygame.transform.scale(tree,(800+300,500))
tree2=pygame.image.load('DinoAssets/background/3.png').convert_alpha()
tree2=pygame.transform.scale(tree2,(800+300,500))
water=pygame.image.load('DinoAssets/background/4.png').convert_alpha()
water=pygame.transform.scale(water,(800+300,1200))
logs=pygame.image.load('DinoAssets/background/5.png').convert_alpha()
logs=pygame.transform.scale(logs,(800+300,500))

#store tile in a list
img_list=[]
for x in range(TILE_TYPES):
    img=pygame.image.load(f'DinoAssets/tile/{x}.png')
    img =pygame.transform.scale(img,(TILE_SIZE,TILE_SIZE))
    img_list.append(img)
#pickup items
#health apple
health_apple_img=pygame.image.load('DinoAssets/items_boxes/apple.png').convert_alpha()
#amour plate
amour_plate_img=pygame.image.load('DinoAssets/items_boxes/amor.png').convert_alpha()
amour_size=pygame.transform.scale(amour_plate_img,(30,50))
#speed necklace
speed_necklace_img=pygame.image.load('DinoAssets/items_boxes/faster.png').convert_alpha()
necklace_size=pygame.transform.scale(speed_necklace_img,(30,50))
item_boxes= {
    'Health': health_apple_img,
    'Happy Time': amour_plate_img,
    'Speed' : speed_necklace_img
}

#player action
moving_left = False
moving_right = False
moving_down = False
#creates the screen
#screen=pygame.display.set_mode((800,600))

#background color  
Background=(150, 56, 141)
BLACK=(0,0,0)
WHITE=(255,255,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (64, 95, 186)

#Title and Icon of the game
pygame.display.set_caption("DinoGame")

font=pygame.font.SysFont("arial.ttf", 30)
#draws the text
def draw_text(text, font, text_col,x,y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))



#stop the trailing

#class to make characters or npc IMPORTANT
class Characters(pygame.sprite.Sprite):
    #function that creates the characters
    def __init__(self,character_type,x,y,scale,speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.character_type=character_type
        self.speed=speed
        self.direction=1
        self.max_speed=7
        self.jump=False
        self.health=10
        self.max_health=10
        self.max_health = self.health
        self.in_air= True
        self.flip=False
        self.velocity_y=0
        self.animation_list=[]
        self.index=0
        self.action=0
        self.update_time=pygame.time.get_ticks()
        #ai variables
        self.move_counter=0
        self.idling=False
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idle_counter=0
        self.speaking=False
        
        #load  all images for the players
        animation_types= ['idle','move','kick','crouch','hurt']
        for animation in animation_types:
            temp_list=[]
            #this counts the number of files in a folder
            num_of_png =len(os.listdir(f'DinoAssets/characters/{self.character_type}/dinosaur/{animation}'))
            for i in range(num_of_png):
                img = pygame.image.load(f'DinoAssets/characters/{self.character_type}/dinosaur/{animation}/{i}.png').convert_alpha()
                img= pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            
           
        self.image=self.animation_list[self.action][self.index]
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        self.width=self.image.get_width()
        self.height=self.image.get_height()
        
    def update(self):
        self.update_animation()
        self.check_alive()



#the funtion moves the characters
    def move(self, moving_left, moving_right):
        #reset movement var
        screen_scroll=0
        dx=0
        dy=0
        #moves the characters left or right
        if moving_left:
            dx=-self.speed
            self.flip=True
            self.direction= -1

        if moving_right:
            dx= self.speed
            self.flip = False
            self.direction = 1

        #jump
        if self.jump==True and self.in_air == False:
            self.velocity_y = -11
            self.jump=False
            self.in_air=True

        #gravity
        self.velocity_y += GRAVITY
        if self.velocity_y > 10:
            self.velocity_y
        dy += self.velocity_y

        #check for collision
        for tile in world.obstacle_list:
            #check for x collision
            if tile[1].colliderect(self.rect.x+dx,self.rect.y,self.width,self.height):
                dx=0
            #check for y collision
            if tile[1].colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
                #check if below the ground
                if self.velocity_y<0:
                    self.velocity_y=0
                    dy=tile[1].bottom-self.rect.top
                #check if above the ground
                elif self.velocity_y>=0:
                    self.velocity_y=0
                    self.in_air=False
                    dy=tile[1].top-self.rect.bottom


        #exit collision
        lvl_done=False
        if pygame.sprite.spritecollide(self,exit_group, False):
            lvl_done=True

             
        #lava collision
        if pygame.sprite.spritecollide(self,lava_group, False):
            self.health=0
          #chech if fallen off the map
        if self.rect.bottom> SCREEN_HEIGHT:
            self.health=0
        #check if going off the edge of the screen
        if self.character_type=='player_1':
            if self.rect.left + dx <0 or self.rect.right + dx > SCREEN_WUDTH:
                dx=0
        #updates the rectangle postiton
        self.rect.x += dx
        self.rect.y += dy

        #update scroll based on player position
        if self.character_type=='player_1':
            if (self.rect.right > SCREEN_WUDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WUDTH)\
                 or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x-=dx
                screen_scroll=-dx
			   
        return screen_scroll, lvl_done


    def ai(self):
        if abs(player.rect.x-self.rect.x)<100:
            self.speaking=True
        else:
            self.speaking=False
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)#0: idle
                self.idling = True
                self.idle_counter = 50
            #check if the ai in near the player
            if self.vision.colliderect(player.rect):
                #stop running and face the player
                self.update_action(0)#0: idle
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True  
                    else:
                        ai_moving_right = False
                    
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)#1: run
                    self.move_counter += 1
                    #update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idle_counter -= 1
                    if self.idle_counter <= 0:
                        self.idling = False
        #scroll
        self.rect.x +=screen_scroll



    def update_animation(self):
        #updates the animation
        ANIMATION_COOLDOWN=100
        self.image = self.animation_list[self.action][self.index]
        #check if enough time has passed
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.index +=1
        #loops the animations
        if self.index >= len(self.animation_list[self.action]):
            if self.action == 5:
                self.index= len(self.animation_list[self.action])-1
            else:
                self.index=0


    def update_action(self, new_action):
        #checks for the new animations
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.index = 0
            self.update_time=pygame.time.get_ticks()
    
   
        


    def check_alive(self):
        if self.health <=0:
            self.health=0
            self.speed=0
            self.alive= False
            self.update_action(4)
           
#workingg on this 1/9/2023
    # function that prints the characters or npc onto the screen
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        if self.speaking:
            dialogue_list = [
                "Hello, adventurer!",
                "Beware of what lies ahead.",
                "The treasure is hidden deep within the forest.",
                "You have come far, but your journey is not over yet.",
                "I sense danger lurking in the shadows.",
                "The key to success is perseverance.",
                "You possess great potential.",
                "Remember, bravery is the mark of a true hero.",
                "May your path be filled with fortune and glory!",
                "Farewell, and good luck!",
                "Why did the dinosaur go to the dentist? Because it had a fossil cavity!",
                "How do you ask a dinosaur to lunch? Tea, Rex?",
                "What do you call a dinosaur with an extensive vocabulary? A thesaurus!",
                "Why don't you ever hear a pterodactyl using the bathroom? Because they have silent pees!",
                "Why did the T-Rex cross the road? Chickens hadn't evolved yet!",
                "What do you call a sleeping dinosaur? A dino-snore!",
                "What do you call a dinosaur that's a noisy sleeper? A Bronto-snore-us!",
                "What kind of dinosaur loves to sleep? A stega-snore-us!",
                "Why don't dinosaurs ever forget anything? Because they always have their 'thinks' together!",
                "How does a dinosaur send messages? By using a dino-saurce!"
                ]
            if not hasattr(self, "current_dialogue"):
                self.current_dialogue = random.choice(dialogue_list)
                self.dialogue_timer = 0
            draw_speech(screen, self.current_dialogue, (255, 255, 255), (0, 0, 0), self.rect.midtop, 25)
            self.dialogue_timer += 1
            if self.dialogue_timer >= 120:  # Change dialogue every 2 seconds (assuming 60 FPS)
                self.current_dialogue = random.choice(dialogue_list)
                self.dialogue_timer = 0
            self.speaking = False

    


    




 
class World():
    def __init__(self):
        self.obstacle_list=[]

    def process_data(self,data):
        self.level_length = len(data[0])
        #iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >=0:
                    img=img_list[tile]
                    img_rect=img.get_rect()
                    img_rect.x=x * TILE_SIZE
                    img_rect.y=y * TILE_SIZE
                    tile_data=(img,img_rect)
                    if tile >=0 and tile <=6:
                        self.obstacle_list.append(tile_data)
                    elif tile == 7:
                        lava=Lava(img, x * TILE_SIZE,y * TILE_SIZE)
                        lava_group.add(lava)
                    elif tile >= 11 and tile <= 18:#decorations
                        decoration=Decoration(img, x * TILE_SIZE,y * TILE_SIZE)
                        decor_group.add(decoration)
                    elif tile == 19:#player
                        player= Characters('player_1',x * TILE_SIZE,y * TILE_SIZE, 2, 5)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                        #healthbar=heart_updates()
                    elif tile ==8:#red dino
                        enemy= Characters('enemy_3',x * TILE_SIZE,y * TILE_SIZE, 1.70, 2)
                        enemy_group.add(enemy)
                    elif tile == 9:#green dino
                        enemy= Characters('enemy_2',x * TILE_SIZE,y * TILE_SIZE, 1.70, 2)
                        enemy_group.add(enemy)
                    elif tile == 10:#blue dino 3
                        enemy= Characters('enemy_1',x * TILE_SIZE,y * TILE_SIZE, 1.70, 2)
                        enemy_group.add(enemy)
                    elif tile==22:#dragon fruit
                        item=ItemsBox('Health', x * TILE_SIZE,y * TILE_SIZE)
                        item_group.add(item)
                    elif tile== 23:
                        item=ItemsBox('Happy Time', x * TILE_SIZE,y * TILE_SIZE)
                        item_group.add(item)
                    elif tile== 21:
                        item=ItemsBox('Speed', x * TILE_SIZE,y * TILE_SIZE)
                        item_group.add(item)
                    elif tile ==20:#exit
                        exit=Exit(img, x * TILE_SIZE,y * TILE_SIZE)
                        exit_group.add(exit)
        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0]+=screen_scroll
            screen.blit(tile[0],tile[1])


class HealthBar():
	def __init__(self, x, y, health, max_health):
		self.x = x
		self.y = y
		self.health = health
		self.max_health = max_health

	def draw(self, health):
		#update with new health
		self.health = health
		#calculate health ratio
		ratio = self.health / self.max_health
		pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
		pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

   
class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self) 
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    def update(self):
        self.rect.x +=screen_scroll

class Lava(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self) 
        self.image=img
        self.rect=self.image.get_rect()
        self.rect.midtop=(x+TILE_SIZE//2, y+(TILE_SIZE-self.image.get_height())) 
    def update(self):
        self.rect.x +=screen_scroll

  
class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self) 
        self.image=img
        self.rect=self.image.get_rect()
        self.rect.midtop=(x+TILE_SIZE//2, y+(TILE_SIZE-self.image.get_height()))  
    def update(self):
        self.rect.x +=screen_scroll


class ItemsBox(pygame.sprite.Sprite):
    
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop =(x+TILE_SIZE//2, y + (TILE_SIZE - self.image.get_height()))
        #self.rect=self.rect.inflate_ip(-20,-10)


    def update(self):
        self.rect.x +=screen_scroll
        #check if player has picked up the items
        if pygame.sprite.collide_rect(self, player):
           
            #check the kind of box
            if self.item_type=='Health':
                player.health +=5
                if player.health>player.max_health:
                    player.health =player.max_health
                #print (player.health)
            elif self.item_type == 'Speed': 
                    LIMIT_SPEED=10
                    speed_enchancer=1.2
                    player.speed=player.speed*speed_enchancer
                    if player.speed>LIMIT_SPEED:
                        player.speed=player.max_speed
            elif self.item_type == "Happy Time":
                player.max_health=15
                player.health=10
                #print(player.health)
    
        #delete items when picked up
            self.kill() 
       
#text bubbles
def draw_speech(screen, text, text_color, bg_color, pos, size):
        font=pygame.font.SysFont(None,size)
        text_surface=font.render(text, True, text_color)
        text_rect=text_surface.get_rect(midbottom=pos)

        #background
        bg_rect=text_rect.copy()
        bg_rect.inflate_ip(10,10)

        #Frame
        frame_rect=bg_rect.copy()
        frame_rect.inflate(4,4)

        pygame.draw.rect(screen, text_color, frame_rect)
        pygame.draw.rect(screen,bg_color,bg_rect)
        screen.blit(text_surface, text_rect)


class ScreenFade():
    def __init__(self, direction, color, speed):
        self.direction=direction
        self.color=color
        self.speed=speed
        self.fade_counter=0
        


    def fade(self):
        fade_complete=False
        self.fade_counter +=self.speed
        if self.direction==1:
            pygame.draw.rect(screen, self.color, (0 - self.fade_counter, 0, SCREEN_WUDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (SCREEN_WUDTH // 2 + self.fade_counter, 0, SCREEN_WUDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (0, 0 - self.fade_counter, SCREEN_WUDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.color, (0, SCREEN_HEIGHT // 2 +self.fade_counter, SCREEN_WUDTH, SCREEN_HEIGHT))

        if self.direction==2:
            pygame.draw.rect(screen, self.color,(0,0,SCREEN_WUDTH, 0+ self.fade_counter))
        if self.fade_counter >= SCREEN_WUDTH:
            fade_complete=True 


        return fade_complete

intro_fade=ScreenFade(1, BLACK,4)
level_fade= ScreenFade(2,BLACK,4)
death_fade=ScreenFade(2,RED,4)

#load in music/sound effects
pygame.mixer.music.load('DinoAssets/music/Super Mario RPG - Forest Maze.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1,0.0,5000)
jump_fx=pygame.mixer.Sound('DinoAssets/music/208956309.mp3')
jump_fx.set_volume(.5)
bruh_fx=pygame.mixer.Sound('DinoAssets/death fade/bruh.mp3')
bruh_fx.set_volume(10)
play_bruh=True
#create buttons
play_button=button.Button(SCREEN_WUDTH//3-130,SCREEN_HEIGHT//1.3,play_button,4)
exit_button=button.Button(SCREEN_WUDTH//1.4,SCREEN_HEIGHT//1.3,exit_button,4)
restart_button=button.Button(SCREEN_WUDTH//2,SCREEN_HEIGHT//1.3,restart_button,4)
title=button.Button(SCREEN_WUDTH//6.5,SCREEN_HEIGHT//13,title,10)
play_music=button.Button(SCREEN_WUDTH//60,SCREEN_HEIGHT//18,play_music,2)
stop_music=button.Button(SCREEN_WUDTH//15,SCREEN_HEIGHT//18,stop_music,2)
sound=button.Button(SCREEN_WUDTH//5.5,SCREEN_HEIGHT/2,sound,5)

m=0
def music():
    global m
    if m==0:
        bruh_fx.play
        music.play(loops=-1)
        m=1
#create sprite group
enemy_group=pygame.sprite.Group()       
item_group=pygame.sprite.Group()
exit_group=pygame.sprite.Group()
lava_group=pygame.sprite.Group()
decor_group=pygame.sprite.Group()




#create empyty tile list
world_data=[]
for row in range(ROWS):
    r=[-1]*COLLUMNS
    world_data.append(r)
#load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			world_data[x][y] = int(tile)


world=World()
player, health_bar = world.process_data(world_data)


run=True
while run:


    #fps
    clock.tick(fps)
    #bg()
    if start_game==False:
       #draw menu
       menu_bg()
       title.draw(screen)
       sound.draw(screen)
       #add button
       if play_button.draw(screen):
            start_game=True
            
       if exit_button.draw(screen):
            run=False
        
    else:
        draw_background()
        #draw world map
        world.draw()
        #show health
        health_bar.draw(player.health)


        #player
        player.update()
        player.draw()
    

        #npc / enemy
        for enemy in enemy_group:   
            enemy.ai()
            enemy.update()
            enemy.draw()
        
        if play_music.draw(screen):
            pygame.mixer.music.unpause() 
            pygame.mixer.unpause()
        if stop_music.draw(screen):
            pygame.mixer.pause()
            pygame.mixer.music.pause()



        #draws and updates the groups onto the screen
        item_group.update()
        decor_group.update()
        lava_group.update()
        exit_group.update()
        item_group.draw(screen)
        decor_group.draw(screen)
        lava_group.draw(screen)
        exit_group.draw(screen)
        #heart_updates()
        if start_intro==True:
            if intro_fade.fade():
                start_intro=False
                intro_fade.fade_counter=0
        
        #update player action
        if player.alive:
            if moving_down==True:
                player.update_action(3)

            elif moving_left or moving_right:
            #action 1 means run
                player.update_action(1)
            else:
            #action 0 means idle
                player.update_action(0)
            screen_scroll, lvl_done= player.move(moving_left, moving_right)
            #print(lvl_done)
            bg_scroll -=screen_scroll
            #check if level is completed
            if lvl_done:
                start_intro=True
                level +=1
                bg_scroll=0
                world_data=reset_level()
                if level <=MAX_LEVELS:
                    #load in level data and create world
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world=World()
                    player, health_bar = world.process_data(world_data)

        else:
            screen_scroll=0
            if death_fade.fade():
                if restart_button.draw(screen):
                    death_fade.fade_counter=0
                    start_intro=True
                    bg_scroll=0
                    world_data=reset_level()
                    #load in level data and create world
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world=World()
                    player, health_bar = world.process_data(world_data)

        if level>2:
            start_intro=True
            player.speed=0
            the_end()
           
#events
    for event in pygame.event.get():
        #quit game
        if event.type ==pygame.QUIT:
            run = False
         #keyboard presses
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_a and player.alive:
                moving_left = True
            if event.key ==pygame.K_d and player.alive:
                moving_right = True
            if event.key ==pygame.K_w and player.alive:
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_ESCAPE:
                run=False
            if event.key == pygame.K_s and player.alive:
                moving_down=True
           
           


        
        #keyboard button relased
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_a:
                moving_left = False
            if event.key ==pygame.K_d:
                moving_right = False
            if event.key ==pygame.K_s:
                moving_down = False
           

        


    pygame.display.update()


pygame.quit()




