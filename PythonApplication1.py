import pygame
import random
import math
from pygame.locals import *
import collections




class keyboard_tiles:

    #initialize pygame and the needed variables
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((300, 640), RESIZABLE)
        pygame.display.set_caption('Keyboard Tiles')
        #pygame.font.init()
        self.font = pygame.font.SysFont("arial bold", 60)
        #self.background = pygame.Surface(self.screen.get_size())
        #self.background = self.background.convert()
        #self.background.fill((250, 250, 250))
        self.clock = pygame.time.Clock()
        
        #load up the images
        file = "blue.png"
        self.blue_tile_image = pygame.image.load(file).convert_alpha()
        file = "purple.png"
        self.purple_tile_image = pygame.image.load(file).convert_alpha()
        file = "gray.png"
        self.gray_tile_image = pygame.image.load(file).convert_alpha()
        file = "dblue.png"
        self.dblue_tile_image = pygame.image.load(file).convert_alpha()
        file = "top_bar.png"
        self.top_bar_image = pygame.image.load(file).convert_alpha()
        file = "you_lose.png"
        self.you_lose_image = pygame.image.load(file).convert_alpha()
        
        #variable for if the game is running
        self.running = True

        #create a board instance
        self.board = board()

        #create a timer
        self.timer = 0
        self.time_left = 10

        #initialize score
        self.score = 0
        self.score_multiplier = 1
        self.timer_running = False

        #render some fonts for the bottom labels
        self.label1 = self.font.render("Z", 1, (255, 255, 255))
        self.label2 = self.font.render("X", 1, (255, 255, 255))
        self.label3 = self.font.render("C", 1, (255, 255, 255))
        self.label4 = self.font.render("<", 1, (255, 255, 255))
        self.label5 = self.font.render(">", 1, (255, 255, 255))
        self.label6 = self.font.render("?", 1, (255, 255, 255))

    def draw(self):

        #draw the top bar
        self.screen.blit(self.top_bar_image, (0, 0))

        #draw the tiles
        for row in self.board.list:
            
            for cell in row:
                if cell.type is 'purple':
                    if cell.true_y == 565:
                        self.screen.blit(self.blue_tile_image, (cell.true_x, cell.true_y))
                    elif cell.true_y == 470:
                        self.screen.blit(self.dblue_tile_image, (cell.true_x, cell.true_y))
                    else:
                        self.screen.blit(self.purple_tile_image, (cell.true_x, cell.true_y))
                else:
                    self.screen.blit(self.gray_tile_image, (cell.true_x, cell.true_y))
               
        #draw the labels at the bottom
        self.screen.blit(self.label1, (12, 585))
        self.screen.blit(self.label2, (62, 585))
        self.screen.blit(self.label3, (112, 585))
        self.screen.blit(self.label4, (162, 585))
        self.screen.blit(self.label5, (212, 585))
        self.screen.blit(self.label6, (262, 585))

        #draw the timer and score
        #render the score
        font_used = pygame.font.SysFont("arial bold", 50)
        score_font = font_used.render(str(self.score), 1, (255, 255, 255))
        #display the score
        self.screen.blit(score_font, (6,4))
        #render the timer
        timer_font = font_used.render(str(self.time_left), 1, (255, 255, 255))
        #draw the timer
        self.screen.blit(timer_font, (250,4))

        #draw the loss message
        if self.running is False:
            
            self.screen.blit(self.you_lose_image, (50, 250))
            

        #flip dat shit
        pygame.display.flip()

    def game_lost(self):
       
        self.continuing = True

        while self.continuing:
            self.clock.tick(60)
            self.draw()
            for event in pygame.event.get():
                 #user hits the X
                    
                if event.type == pygame.QUIT:
                    self.running = False
                    #pygame.quit()
                #otherwise we can check for key presses
                elif event.type == KEYDOWN:
                    self.continuing = False

    #checks for user input
    def update(self):
        #update the timer
        if self.timer_running is True:
            self.time_left = 10 -((pygame.time.get_ticks() - self.timer) / 1000)

        

        #checking for input....
        for event in pygame.event.get():
                    #user hits the X
                    if event.type == pygame.QUIT:
                        self.running = False
                        pygame.quit()
                    #otherwise we can check for key presses
                    elif event.type == KEYDOWN:
                        #z
                        if event.key == K_z:
                            self.check(0)
                            self.board.update()
                        #x
                        elif event.key == K_x:
                            self.check(1)
                            self.board.update()
                        #c
                        elif event.key == K_c:
                            self.check(2)
                            self.board.update()
                        #<
                        elif event.key == K_COMMA:
                            self.check(3)
                            self.board.update()
                        #>
                        elif event.key == K_PERIOD:
                            self.check(4)
                            self.board.update()
                        #?
                        elif event.key == K_SLASH:
                            self.check(5)
                            self.board.update()

         #end the game if out of time
        if self.time_left <= 0:
             self.running = False
                
    #checks if the user did it right or if hes retarded        
    def check(self, cellnumber):
        
        if self.board.list[0][cellnumber].type is not 'purple':
            print "fail"
            self.running = False
        else:
            if self.score == 0:
                self.timer = pygame.time.get_ticks()
                self.timer_running = True

            self.score += 100*self.score_multiplier
            self.score_multiplier += 1
            
    #this is the function for the main loop
    #self.running is an instance variable, can be changed by other methods
    def main(self):
        self.__init__()
        while self.running:
            #try:
            self.clock.tick(60)
            self.update()
            self.draw()
            #except:
                #raise
        self.game_lost()
        self.main()
        pygame.quit()

#Class classic is a game mode to define the score, and has a timer.
class classic:

    def __init__(self, seconds):
        pass
        self.score = 0
        self.time = seconds

#tile is one of the square things lol
class tile:

    #initialize the square, will be drawn by the draw method
    def __init__(self, (x, y), type):

        self.type = type

        self.true_x = x  

        self.true_y = y  

        #this changes the values (duh lol)
    def update(self, new_x, new_y):

        self.true_x = new_x

        self.true_y = new_y

#board is a list of rows, which are a list of tile objects
class board:

    #initializing a board with correct values
    def __init__(self):
        #this is a list containing rows
        self.list = []
        
        for i in range(565, 0, -75):
            #print i
            self.list.append(self.gen_row(i))   

    #create a row, takes the y coordinate, returns a list of tiles (a row)
    def gen_row(self, y):
        
        rand = random.randint(0,5)

        row = []

        #creates 1 purple and 1 gray
        for i in range(0, 300, 50):
            if (i/50) == rand:
                row.append(tile((i, y), 'purple'))
            else:
                row.append(tile((i, y), 'gray'))
        
        return row

    #this will shove back all the rows, delete the un neccesary one, and create a new row at the bottom
    def update(self):

        temp = []
       
        for i in range(0, len(self.list), 1):
            if self.list[i][0].true_y < 525:
                temp.append(self.list[i])
        
        temp.append(self.gen_row(-35))
        for row in temp:
            for cell in row:
                cell.true_y += 75
        
        #for testing
        #for i in temp:
            #print i[0].true_y

        self.list = temp

#make an instance of the game
game = keyboard_tiles()
#start the game
game.main()
    
