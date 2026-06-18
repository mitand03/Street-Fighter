import pygame

class PhysicsEntity:

    def __init__(self, game, e_type, pos, size, controls):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]  # Only used for specific effects like sliding
        self.controls = controls
        self.MovementX = [0, 0]  # Movement states for left (0) and right (1)
        self.facing_right=True

        # Jump attributes
        self.gravity_force = 1.2  # Gravity strength
        self.jump_velocity = 0  # Jumping velocity
        self.is_jumping = False
        self.ground_level = 350  # Ground level where the player should land

        # Slide-related attributes
        self.is_sliding = False
        self.slide_speed_boost = 4  # Speed boost while sliding
        self.slide_duration = 500  # Duration of the slide in milliseconds (1 second)
        self.slide_timer = 0  # Tracks the time when the slide starts
        self.extra_boost=1

        self.health = 100  # Player starts with full health
        self.defend_duration=500
        self.is_defending=False
        self.def_timer=0

        self.is_teleporting=False

    def update(self, movement=(0, 0)):
        
            # Regular movement (left/right)
            frame_movement = ((self.MovementX[1] - self.MovementX[0]) * self.game.speed, movement[1])

            # Add velocity only if sliding
            if self.is_sliding:
                frame_movement = (frame_movement[0] + self.velocity[0], frame_movement[1])

            # Apply movement
            self.pos[0] += frame_movement[0]
            self.pos[1] += frame_movement[1]

            #check boundaries for x axis
            if self.pos[0]<=0:
                self.pos[0]=0
            if self.pos[0]>=900:
                self.pos[0]=900

            # Handle jump mechanics
            if self.is_jumping:
                self.jump_velocity += self.gravity_force  # Increase downward velocity (gravity)
                self.pos[1] += self.jump_velocity  # Move the player in Y-axis

                # Check if the player has hit the ground
                if self.pos[1] >= self.ground_level:
                    self.pos[1] = self.ground_level  # Stop player at ground level
                    self.is_jumping = False  # Stop jumping
                    self.jump_velocity = 0  # Reset jump velocity

            # Handle sliding mechanics
            if self.is_sliding:
                current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
                # Check if the slide duration has ended
                if current_time - self.slide_timer > self.slide_duration:
                    self.is_sliding = False  # Stop sliding after the duration
                    self.velocity[0] = 0  # Reset velocity back to 0 (only during slide)
           
            
            if self.is_defending:
                current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
                # Check if the slide duration has ended
                if current_time - self.def_timer > self.defend_duration:
                    self.is_defending = False  # Stop sliding after the duration

            if self.is_teleporting:
                if self.pos[0]<450:
                    self.pos[0]=850
                    self.is_teleporting=False
                elif self.pos[0]>450:
                    self.pos[0]=100
                    self.is_teleporting=False
            
            if self.health<=0:
                self.MovementX=[0,0]
                self.is_jumping=False
                self.is_sliding=False
            


    def jump(self):
        if not self.is_jumping:  # Only jump if not already in the air
            self.is_jumping = True
            self.jump_velocity = -17  # Negative velocity to move upwards

    def slide(self):
        if not self.is_sliding :  # Only start sliding if not already sliding
            self.is_sliding = True
            if self.type=='ninja':
                if self.pos[1] < self.ground_level:
                    self.extra_boost=4
            else:
                self.extra_boost=3
            if self.facing_right:
                self.velocity[0] = self.slide_speed_boost*self.extra_boost
            else:
                self.velocity[0] = -self.slide_speed_boost*self.extra_boost
                  # Set the initial speed boost
            self.extra_boost=1
            self.slide_timer = pygame.time.get_ticks()  # Record the time the slide started

    


    def defend(self):
        if not self.is_defending:
            self.is_defending=True
            self.def_timer=pygame.time.get_ticks()

    def teleport(self):
        if not self.is_teleporting:
            self.is_teleporting=True

    def handle_input(self, event):
        """ Handle player-specific input. """
        if self.health>0:
            if event.type == pygame.KEYDOWN:
                if event.key == self.controls['right']:
                    self.MovementX[1] = 1  # Start moving right
                if event.key == self.controls['left']:
                    self.MovementX[0] = 1  # Start moving left
                if event.key == self.controls['jump']:
                    self.jump()  # Jump when key pressed
                if event.key == self.controls['slide']:
                    if self.type=='ninja':
                        self.slide()  # Slide when key pressed
                   
                
                    
            if event.type == pygame.KEYUP:
                if event.key == self.controls['right']:
                    self.MovementX[1] = 0  # Stop moving right
                if event.key == self.controls['left']:
                    self.MovementX[0] = 0  # Stop moving left


    def direction(self):
    # Check if the player is moving left or right
        if self.MovementX[1] > 0:  # Moving right
            self.facing_right = True
        elif self.MovementX[0] > 0:  # Moving left
            self.facing_right = False
        return self.facing_right
    

    def health_bar(self,screen, current_health, max_health, pos, width=180, height=40, border_width=5):
        # Calculate the current width based on the player's health (clamped so a hit that drops
        # health below 0 doesn't produce a negative-width rect)
        health_percentage = max(0, min(1, current_health / max_health))
        current_width = width * health_percentage

        # Draw the health bar (filled)
        health_rect = pygame.Rect(pos[0], pos[1], current_width, height)
        pygame.draw.rect(screen, 'green', health_rect)

        # Draw the border around the health bar
        border_rect = pygame.Rect(pos[0], pos[1], width, height)
        pygame.draw.rect(screen, 'black', border_rect, border_width)