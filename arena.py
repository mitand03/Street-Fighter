import pygame
from scripts.shortcut import *
from scripts.sprite_manager import load_sprite_sequence,load_sprite_sequence2
import sys
from scripts.entities import PhysicsEntity
from scripts.powers import Sphere
import random

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        #Sounds
        self.jump_sound = pygame.mixer.Sound('Sounds/hook.mp3')
        self.hit_sound = pygame.mixer.Sound('Sounds/hit.mp3')


        # Set up the screen (width, height)
        self.screen = pygame.display.set_mode((900, 480))
        pygame.display.set_caption("Arena")
        self.running = False
        self.speed = 6  # player speed
        self.font = pygame.font.Font(None, 36)
        self.fight_surf = self.font.render('FIGHT', True, (50,50,50))
        self.fight_surf = pygame.transform.rotozoom(self.fight_surf,1,2)
        self.fight_rect=self.fight_surf.get_rect(center=(self.screen.get_width()/2,self.screen.get_height()/2-120))
        self.defend_cooldown=2000
        self.last_def_time=0
        self.teleport_cooldown=2500
        self.dash_cooldown=4500

        self.last_tel_time=0
        self.last_dash_time=0

        self.bot_mode=False
        self.bot_mode2=False


         # Add bot action interval
        self.bot_action_cooldown = 1000  # Time between bot actions in milliseconds
        self.last_bot_action_time = 0

        # Player 1 controls (WASD)
        player1_controls = {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'jump': pygame.K_w,
            'slide': pygame.K_s,
            'throw': pygame.K_e
        }

        # Player 2 controls (Arrow keys)
        player2_controls = {
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'jump': pygame.K_UP,
            'slide': pygame.K_KP2,
            'throw': pygame.K_SLASH,
        }

        # Setup ninja
        self.index = 0
        self.player = PhysicsEntity(self, 'ninja', (200, 350), (8, 16),player1_controls)
        self.player_run_list=[]
        self.player_idle_list=[]
        self.player_attack_list=[]
        self.facing_right=True

        #setup knight
        self.index2 = 0
        self.player2 = PhysicsEntity(self, 'knight', (800, 350), (8, 16),player2_controls)
        self.player2_run_list=[]
        self.player2_idle_list=[]
        self.player2_attack_list=[]

        #throw attributes
        self.is_throwing=False
        self.throw_duration=250
        self.throw_duration2=500

        self.throw_start_time=0
        self.throw_start_time2=0

        self.last_throw_time=0
        self.last_throw_time2=0

        self.cooldown=500
        self.cooldown2=1000
        self.is_throwing2=False


        #map
        self.map_surf=pygame.image.load("graphics/map/bg_volcano.png")
        self.map_rect=self.map_surf.get_rect(center=(500,100))
        self.ground_surf=pygame.image.load("graphics/map/groud.png")
        self.ground_surf = pygame.transform.rotozoom(self.ground_surf, 1, 2)
        self.ground_rect=self.ground_surf.get_rect(center=(200,410))
        self.start_backround=pygame.image.load('graphics/map/backround.png')
        self.start_backround = pygame.transform.scale(self.start_backround, (900, 480))
        self.start_backround_rect=self.start_backround.get_rect(center=(self.screen.get_width()/2,self.screen.get_height()/2))

        #start screen
        self.player_start=pygame.image.load('graphics/ninja/png/Jump_Throw__000.png')
        self.player_start=pygame.transform.rotozoom(self.player_start,1,1.3)
        self.player_start_rect=self.player_start.get_rect(center=(180,200))  
        self.player2_start=pygame.image.load('graphics/knight/png/JumpAttack (5).png')
        self.player2_start=pygame.transform.rotozoom(self.player2_start,1,1.1)
        self.player2_start=pygame.transform.flip(self.player2_start,True,False)
        self.player2_start_rect=self.player2_start.get_rect(center=(720,200))  


        

        #end screen
        self.win_text1 = self.font.render('NINJA WON', True, (50,50,50))
        self.win_text1 = pygame.transform.rotozoom(self.win_text1,1,2)
        self.WIN_rect1=self.win_text1.get_rect(center=(self.screen.get_width()/2,self.screen.get_height()/2-120))

        self.win_text2 = self.font.render('KNIGHT WON', True, (50,50,50))
        self.win_text2 = pygame.transform.rotozoom(self.win_text2,1,2)
        self.WIN_rect2=self.win_text2.get_rect(center=(self.screen.get_width()/2,self.screen.get_height()/2-120))

        self.again = self.font.render('PLAY AGAIN', True, 'red')
        self.again = pygame.transform.rotozoom(self.again,1,2)
        self.again_rect=self.again.get_rect(center=(self.screen.get_width()/2,self.screen.get_height()/2))





        # list of throwables
        self.knifes=[]   
        self.swords=[]

        # Load the images for ninja
        self.idle_sprites = load_sprite_sequence('graphics/ninja/png', 'Idle__', 10)
        self.attack_sprites=load_sprite_sequence('graphics/ninja/png', 'Attack__', 10)
        self.player_jump = load_ninja('Jump__003.png')
        self.run_sprites = load_sprite_sequence('graphics/ninja/png', 'Run__', 10)
        self.die=load_ninja('Dead__004.png')
        self.player_slide=load_ninja('Slide__000.png')
        self.player_throw1=load_ninja('Throw__000.png')        
        self.player_throw2=load_ninja('Throw__003.png') 
        self.dash=load_ninja('Dash.png')
        self.face1=pygame.image.load('graphics/ninja/png/face1.png')
        self.face1=pygame.transform.rotozoom(self.face1,1,0.2)
        self.face1_rect=self.face1.get_rect(center=(40,40))

        #load the images for knight
        self.idle_sprites2=load_sprite_sequence2('graphics/knight/png','Idle',10) 
        self.player2_jump=load_knight('Jump (6).png')
        self.run_sprites2=load_sprite_sequence2('graphics/knight/png','Run', 10)  
        self.attack_sprites2=load_sprite_sequence2('graphics/knight/png','Attack', 10)
        self.die2=load_knight('Dead (5).png')
        self.defend=load_knight('Def (1).png')
        self.player2_dash=load_knight('dash.png')
        self.player2_dash=pygame.transform.rotozoom(self.player2_dash,1,1.3)
        self.face2=pygame.image.load('graphics/knight/png/face2.png')
        self.face2=pygame.transform.rotozoom(self.face2,1,0.2)
        self.face2=pygame.transform.flip(self.face2,True,False)
        self.face2_rect=self.face2.get_rect(center=(870,40))   
        self.shield=pygame.image.load('graphics/knight/png/shield.png')
        self.shield=pygame.transform.rotozoom(self.shield,1,0.3)
        self.shield_rect=self.shield.get_rect(center=(870,150))   







        
        # Create lists for idle animation for ninja
        for i in range(10):
             self.player_run_list.append(self.run_sprites[i])
             self.player_idle_list.append(self.idle_sprites[i])
             self.player_attack_list.append(self.attack_sprites[i])
        self.player_throw_list=[self.player_throw1,self.player_throw2]
        self.player_SURF = self.player_idle_list[self.index]
        self.player_rect = self.player_SURF.get_rect(center=self.player.pos)


        # Create lists for idle animation for knight
        for i in range(10):
             self.player2_idle_list.append(self.idle_sprites2[i])
             self.player2_run_list.append(self.run_sprites2[i])
             self.player2_attack_list.append(self.attack_sprites2[i])
        self.player2_SURF=self.player2_idle_list[self.index2]
        self.player2_rect = self.player2_SURF.get_rect(center=self.player2.pos)

    def bot_input(self):
        """Simulate random input for Player 2 (Knight) when in bot mode."""
        if self.player2.health>0:
            current_time = pygame.time.get_ticks()
            if self.player2.pos[0]>600:
                self.player2.MovementX=[1,0]
            elif self.player2.pos[0]<100:
                self.player2.MovementX=[0,1]
            else:
                self.player2.MovementX=[0,0]
            # Ensure actions happen at intervals, not continuously
            if current_time - self.last_bot_action_time >= self.bot_action_cooldown:
                self.last_bot_action_time = current_time

                # Randomly choose an action: move left, move right, jump, defend, or throw
                actions = [ 'jump', 'throw','slide', 'defend']
                action = random.choice(actions)

                
                if action == 'jump':
                    if not self.player2.is_jumping:
                        self.player2.jump()
                elif action == 'throw':
                    self.throw_sword() 
                elif action == 'slide':
                    self.player2.slide()
                     # Throw sword action
                elif action == 'defend':
                    self.defense()

    def bot_input2(self):
        """Simulate random input for Player 2 (Knight) when in bot mode."""
        if self.player.health>0:
            current_time = pygame.time.get_ticks()
            if self.player.pos[0]>600:
                self.player.MovementX=[1,0]
            elif self.player.pos[0]<100:
                self.player.MovementX=[0,1]
            else:
                self.player.MovementX=[0,0]
            # Ensure actions happen at intervals, not continuously
            if current_time - self.last_bot_action_time >= self.bot_action_cooldown:
                self.last_bot_action_time = current_time

                # Randomly choose an action: move left, move right, jump, defend, or throw
                actions = [ 'jump', 'throw','throw','throw', 'slide','teleport']
                action = random.choice(actions)

                
                if action == 'jump':
                    if not self.player.is_jumping:
                        self.player.jump()
                elif action == 'throw':
                    self.throw_knife()  # Throw sword action
                elif action == 'slide':
                    if not self.player.is_sliding:
                        self.player.slide()
                elif action=='teleport':
                    self.teleporting()

    def reset(self):
        self.player.pos=[100,self.player.ground_level]
        self.player2.pos=[800,self.player2.ground_level]
        self.player.health=100
        self.player2.health=100
        self.player.MovementX=[0,0]
        self.player2.MovementX=[0,0]
        self.player.is_jumping=False
        self.player2.is_jumping=False
        self.player.is_sliding=False
        self.player2.is_sliding=False
        self.player.is_defending=False
        self.player2.is_defending=False
        self.is_throwing=False
        self.is_throwing2=False
        self.knifes=[]
        self.swords=[]

    def collision(self):
        if self.player2_rect.colliderect(self.player_rect) and self.player2.is_sliding:
            self.player.health-=30
            
    
    def timers(self,text,x,y):
        timer = self.font.render(f'{text}', True, (250,0,0))
        timer = pygame.transform.rotozoom(timer,1,2)
        timer_rect=timer.get_rect(center=(x,y))
        self.screen.blit(timer,timer_rect)


    def animation(self, num, player_list, is_player2=False):
        if is_player2:
            self.index2 += num
            if self.index2 >= len(player_list):
                self.index2 = 0
            return player_list[int(self.index2)]
        else:
            self.index += num
            if self.index >= len(player_list):
                self.index = 0
            return player_list[int(self.index)]
    
    def defense(self):
        current_time = pygame.time.get_ticks()
        if (current_time - self.last_def_time >= self.defend_cooldown) and (self.player2.MovementX==[0,0]) and not self.player2.is_jumping:
            self.player2.defend()
            self.last_def_time=current_time

    
    def teleporting(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_tel_time >= self.teleport_cooldown:
            self.player.teleport()
            self.last_tel_time=current_time
    def dashing(self):
            current_time = pygame.time.get_ticks()
            if (current_time - self.last_dash_time >= self.dash_cooldown) and not self.player2.is_jumping and (self.player2.MovementX!=[0,0]):
                self.player2.slide()
                self.last_dash_time=current_time

            


    def throw_knife(self):

        current_time = pygame.time.get_ticks()
        if current_time - self.last_throw_time >= self.cooldown:
        # Create a new sphere when the player throws one
            player_pos = self.player.pos.copy()
            new_knife = Sphere(pos=player_pos, speed=30,type='knife')  # You can adjust speed
            if self.player.pos[0]>self.player2.pos[0]:
                new_knife.speed=-new_knife.speed
            self.knifes.append(new_knife)
            self.is_throwing=True
            self.throw_start_time=pygame.time.get_ticks()

            self.last_throw_time=current_time
            
            
    def update_knifes(self):
        for knife in self.knifes[:]:
            knife.update()
            knife_rect = pygame.Rect(knife.pos[0], knife.pos[1], 30, 10)  # Adjust size based on knife image

            # Check collision with player 2 (Knight)
            if knife_rect.colliderect(self.player2_rect) and not self.player2.is_defending:
                self.hit_sound.play()
                self.knifes.remove(knife)  # Remove the knife on collision
                self.player2.health-=10
            else:
                knife.render(self.screen, knife.pos, 'Kunai.png')
            

            if knife.is_expired():
                self.knifes.remove(knife)


    def throw_sword(self):

        current_time = pygame.time.get_ticks()
        if current_time - self.last_throw_time2 >= self.cooldown2:
        # Create a new sphere when the player throws one
            player2_pos = self.player2.pos.copy()
            new_sword = Sphere(pos=player2_pos, speed=30,type='sword')  # You can adjust speed
            if self.player2.pos[0]<self.player.pos[0]:
                new_sword.speed=-new_sword.speed
            self.swords.append(new_sword)
            self.is_throwing2=True
            self.throw_start_time2=pygame.time.get_ticks()

            self.last_throw_time2=current_time

    def update_swords(self):
        # Update and render spheres, and remove expired ones with a copy in order not to modify the origianl while itirating over it
        for sword in self.swords[:]:
            sword.update()
            sword_rect = pygame.Rect(sword.pos[0], sword.pos[1], 30, 10)  # Adjust size based on knife image
            if sword_rect.colliderect(self.player_rect):
                self.hit_sound.play()
                self.swords.remove(sword)
                self.player.health-=30
            sword.render(self.screen, sword.pos,'SWORD.png')
            if sword.is_expired():
                self.swords.remove(sword)



    def run(self):
        
        while True:
            mouse_pos=pygame.mouse.get_pos()

            if not self.running:
                 self.screen.fill((30,89,139))
                 self.screen.blit(self.start_backround,self.start_backround_rect)
                 self.screen.blit(self.player_start,self.player_start_rect)
                 self.screen.blit(self.player2_start,self.player2_start_rect)
                 if self.fight_rect.collidepoint(mouse_pos):
            # Draw the button with a different color when hovered
                    pygame.draw.rect(self.screen, (50, 0, 100), self.fight_rect.inflate(2, 2))  # Yellow background

                 self.screen.blit(self.fight_surf,self.fight_rect)

                 for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # Quit when window is closed
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.fight_rect.collidepoint(mouse_pos):
                            
                            self.running = True

            else:

                # Fill the screen with a background color
                self.screen.fill('white')
                self.screen.blit(self.map_surf,self.map_rect)
                self.screen.blit(self.ground_surf,self.ground_rect)
                current_time = pygame.time.get_ticks()

                # Check for events (keyboard, mouse, etc.)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # Quit when window is closed
                        sys.exit()

                    self.player.handle_input(event)
                    self.player2.handle_input(event)


                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e and self.player.health>0:
                            self.throw_knife()
                        if event.key==pygame.K_KP0 and self.player2.health>0:
                            self.throw_sword()
                        if event.key==pygame.K_KP3:
                            self.defense()
                        if event.key==pygame.K_KP2:
                            self.dashing()
                        if event.key==pygame.K_f:
                            self.teleporting()
                        if event.key==pygame.K_SPACE:
                            self.bot_mode=True
                        if event.key==pygame.K_b:
                            self.bot_mode2=True
                        
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if (self.player.health<=0 or self.player2.health<=0) and self.again_rect.collidepoint(mouse_pos):
                            self.reset()
                            

                # update the sphere pos
                self.update_knifes()
                self.update_swords()

                # Update player position based on movement (Right - Left)
                self.player.update()
                self.player2.update()


                # Update the player's rectangle position to match the entity's position
                self.player_rect = self.player_SURF.get_rect(center=self.player.pos)
                self.player2_rect=self.player2_SURF.get_rect(center=self.player2.pos)

                
                #animations for ninja
                if self.is_throwing:
                    self.player_SURF=self.animation(0.2,self.player_throw_list)
                    current_time=pygame.time.get_ticks()
                    if current_time-self.throw_start_time>self.throw_duration:
                        self.is_throwing=False
                else:
                    if ((self.player.MovementX[1] != 0 or self.player.MovementX[0] != 0) and not self.player.is_jumping and not self.player.is_sliding ):  # If moving left or right
                        self.player_SURF=self.animation(0.6,self.player_run_list)
                        # Running animation
                    elif self.player.is_sliding and self.player.is_jumping:
                        self.player_SURF=self.dash
                    elif self.player.is_jumping:  # If jumping
                        self.player_SURF = self.player_jump  # Switch to jump animation
                    elif self.player.is_sliding:
                        self.player_SURF=self.player_slide
                    elif self.player.health<=0:
                        self.player_SURF=self.die
                        self.screen.blit(self.win_text2,self.WIN_rect2)
                        self.screen.blit(self.again,self.again_rect)
                    else:  # If not moving or jumping, play idle animation
                        self.player_SURF= self.animation(0.7,self.player_idle_list)  # Idle animation
                if not self.player.direction():
                    self.player_SURF = pygame.transform.flip(self.player_SURF, True, False)

                    #animations for knight
                
                if self.is_throwing2:
                    self.player2_SURF=self.animation(0.2,self.player2_attack_list)
                    current_time=pygame.time.get_ticks()
                    if current_time-self.throw_start_time2>self.throw_duration2:
                        self.is_throwing2=False
                    
                else:
                    if ((self.player2.MovementX[1] != 0 or self.player2.MovementX[0] != 0) and not self.player2.is_jumping ):  # If moving left or right
                            self.player2_SURF=self.animation(0.6,self.player2_run_list,is_player2=True)  # Running animation
                    elif self.player2.is_jumping:  # If jumping
                            self.player2_SURF = self.player2_jump  # Switch to jump animation
                    
                    elif self.player2.health<=0:
                        self.player2_SURF=self.die2
                        self.screen.blit(self.win_text1,self.WIN_rect1)
                        self.screen.blit(self.again,self.again_rect)

                        
                    elif self.player2.is_defending and not self.player2.is_jumping:
                        self.player2_SURF=self.defend
                    else:  # If not moving or jumping, play idle animation
                            self.player2_SURF= self.animation(0.7,self.player2_idle_list,is_player2=True)  # Idle animation
                if  not self.player2.direction():
                            self.player2_SURF = pygame.transform.flip(self.player2_SURF, True, False)
                if self.player2.is_sliding:
                        self.player2_SURF=self.player2_dash
                        if  not self.player2.direction():
                            self.player2_SURF = pygame.transform.flip(self.player2_SURF, True, False)

                        

                #set bot mode on
                if self.bot_mode:
                    self.bot_input()
                if self.bot_mode2:
                    self.bot_input2()

                self.collision()
                if current_time - self.last_def_time > 2000:
                    self.screen.blit(self.shield,self.shield_rect)



                #when dead
                if self.player.health<=0:
                    self.is_throwing=False
                if self.player2.health<=0:
                    self.is_throwing2=False



                # Draw the player on the screen
                self.screen.blit(self.player_SURF, self.player_rect)
                self.screen.blit(self.player2_SURF,self.player2_rect)
                #draw stats
                self.player.health_bar(self.screen,self.player.health, 100, (20, 40))     # Player 1 health bar
                self.player2.health_bar(self.screen,self.player2.health, 100, (710, 40))   # Player 2 health bar

                self.screen.blit(self.face1,self.face1_rect)
                self.screen.blit(self.face2,self.face2_rect)

           

            # Update the display
            pygame.display.flip()

            # Limit the frame rate to 60 FPS
            pygame.time.Clock().tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()