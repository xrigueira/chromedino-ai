import os
import sys
import neat
import math
import random
import pygame

# Initialize pygame
pygame.init()

# Set up global constantes
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Import images of dinosaur
RUNNING = [pygame.image.load(os.path.join('Assets/Dino', 'DinoRun1.png')), pygame.image.load(os.path.join('Assets/Dino', 'DinoRun2.png'))]

JUMPING = pygame.image.load(os.path.join('Assets/Dino', 'DinoJump.png'))

BG = pygame.image.load(os.path.join('Assets/Other', 'Track.png'))

FONT = pygame.font.Font('freesansbold.ttf', 20)

# Import the images of the obtacles
SMALL_CACTUS = [pygame.image.load(os.path.join('Assets/Cactus', 'SmallCactus1.png')), pygame.image.load(os.path.join('Assets/Cactus', 'SmallCactus2.png')), pygame.image.load(os.path.join('Assets/Cactus', 'SmallCactus3.png'))]

LARGE_CACTUS = [pygame.image.load(os.path.join('Assets/Cactus', 'LargeCactus1.png')), pygame.image.load(os.path.join('Assets/Cactus', 'LargeCactus2.png')), pygame.image.load(os.path.join('Assets/Cactus', 'LargeCactus3.png'))]

# Create a class for the dinosaur
class Dinosaur:
    
    # Set up constants
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5
    
    def __init__(self, img=RUNNING[0]):
        
        self.image = img
        
        # Set it to running by default
        self.dino_run = True
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL
        
        # To get the coordinates
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(), img.get_height())
        
        # Color for the hit boxes
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        self.step_index = 0 # to loop over the images of the dinosaur and make it look like it is running
        
    def update(self):
        
        # Check the state
            if self.dino_run:
                
                self.run()
                
            if self.dino_jump:
                
                self.jump()
            
        # Reset the state index
            if self.step_index >= 10:
                
                self.step_index = 0
        
    def jump(self):
        
        self.image = JUMPING
        
        if self.dino_jump:
            
            self.rect.y -= self.jump_vel * 4
            
            self.jump_vel -= 0.8
        
        if self.jump_vel <= -self.JUMP_VEL:
            
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VEL
    
    def run(self):
        
        # Make images display sequentially
        self.image = RUNNING[self.step_index // 5]
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1
            
    def draw(self, SCREEN):
        
        # Display image on the screen
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        
        # Draw the hit box
        pygame.draw.rect(SCREEN, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
        
        # Add line of sight
        for obstacle in obstacles:
            pygame.draw.line(SCREEN, self.color, (self.rect.x + 54, self.rect.y + 12), obstacle.rect.center, 2)

# Create a class for the obstacles
class Obstacle:
    
    def __init__(self, image, number_of_cacti):
        
        self.image = image
        self.type = number_of_cacti
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
    
    def update(self):
        
        self.rect.x -= game_speed # get the game speed
        
        if self.rect.x < -self.rect.width: # if it reaches the left -> delete
            
            obstacles.pop()
    
    def draw(self, SCREEN):
        
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 325

class LargeCastus(Obstacle):
    
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 300

# Remove the dinosaurs the run into an obstacle
def remove(index):
    
    dinosaurs.pop(index)
    # Remove also the genome and nets of those dinos that collide
    ge.pop(index)
    nets.pop(index)

# Define distance function
def distance(pos_a, pos_b):
    
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    
    return math.sqrt(dx**2+dy**2)

def eval_genomes(genomes, config):
    
    global game_speed, x_pos_bg, y_pos_bg, obstacles, dinosaurs, ge, nets, points
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    
    clock = pygame.time.Clock()
    points = 0
    
    dinosaurs = [] # Create object of the class dinosaur
    obstacles = []
    ge = [] # Store info on every dinosaur
    nets = [] # Store the nets
    
    for genome_id, genome in genomes:
        
        dinosaurs.append(Dinosaur())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
    
    # Get the score
    def score():
        
        global points, game_speed
        
        points += 1
        
        if points % 100 == 0:
            
            game_speed += 1
        
        text = FONT.render(f'Points:  {str(points)}', True, (0, 0, 0))
        SCREEN.blit(text, (950, 50))
    
    def statistics():
        
        global dinosaurs, game_speed, ge
        text_1 = FONT.render(f'Dinosaurs Alive:  {str(len(dinosaurs))}', True, (0, 0, 0))
        text_2 = FONT.render(f'Generation:  {pop.generation+1}', True, (0, 0, 0))
        text_3 = FONT.render(f'Game Speed:  {str(game_speed)}', True, (0, 0, 0))

        SCREEN.blit(text_1, (50, 450))
        SCREEN.blit(text_2, (50, 480))
        SCREEN.blit(text_3, (50, 510))
    
    def backgroud():
        
        global x_pos_bg, y_pos_bg
        
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        
        if x_pos_bg <= -image_width:
            
            x_pos_bg = 0
            
        x_pos_bg -= game_speed
    
    
    run = True
    # Main loop
    while run:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                
                pygame.quit()
                sys.exit()
        
        # Reset the screen
        SCREEN.fill((255, 255, 255))
        
        # Update and draw the dinosaur on the screen
        for dinosaur in dinosaurs:
            dinosaur.update()
            dinosaur.draw(SCREEN)
        
        if len(dinosaurs) == 0:
            
            break
        
        # Generate cacti on the screen
        if len(obstacles) == 0:
            
            rand_int = random.randint(0, 1)
            
            if rand_int == 0:
                
                obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))
            
            elif rand_int == 1:
                
                obstacles.append(LargeCastus(LARGE_CACTUS, random.randint(0, 2)))
        
        # Apply draw and update functions on all the obstacles
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            
            # Remove dinosaur if it collides
            for i, dinosaur in enumerate(dinosaurs):
                if dinosaur.rect.colliderect(obstacle.rect):
                    ge[i].fitness -= 1 # Decrease the level of fitness of those who colide
                    remove(i)
        
        # # Get user input to jump
        # user_input = pygame.key.get_pressed()
        
        for i, dinosaur in enumerate(dinosaurs):
            
            # Pass the inputs of each dinosaur
            output = nets[i].activate((dinosaur.rect.y, distance((dinosaur.rect.x, dinosaur.rect.y), obstacle.rect.midtop)))
            
            # If output is bigger than 0.5 and it is not currently jumping -> jump
            if output[0] > 0.5 and dinosaur.rect.y == dinosaur.Y_POS:
                
                dinosaur.dino_jump = True
                dinosaur.dino_run = False
            
            # if user_input[pygame.K_SPACE]:
                
            #     dinosaur.dino_jump = True
            #     dinosaur.dino_run = False
        
        score()
        backgroud()
        statistics()
        clock.tick(30) # 30 is the number of frames per second
        pygame.display.update()

# NEAT
def run(config_path):
    
    global pop
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Add population of dinosaurs
    pop = neat.Population(config)
    pop.run(eval_genomes, 50) # fitness functions, looks at how far they go

if __name__ == '__main__':
    
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    
    run(config_path)
        