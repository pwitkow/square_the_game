import turtle
import numpy as np
import itertools as itr
import glob
import os
import random

import pygame
import time




class Pen(turtle.Turtle): 
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape('square')
        self.color('blue')
        self.penup()
        self.speed(10)
        
class Treasure(turtle.Turtle): 
    
    def __init__(self, value, goal_index):
        turtle.Turtle.__init__(self)
        self.shape('square')
        self.color('yellow')
        self.penup()
        self.speed(0)
        
        self.goal_index=goal_index
        self.value=value
        self.found=False
        
    def destroy(self):
        
        self.goto(2000, 2000)
        self.hideturtle()
        self.found=True
        
    
        
class Player(turtle.Turtle): 
   
    def __init__(self, walls):
        turtle.Turtle.__init__(self)
        self.shape('square')
        self.color('green')
        self.penup()
        self.speed(0)
        
        self.walls=list(walls)
        self.start_pos=(0,0)
        
    
    def move_up(self):
        x_move=self.xcor()
        y_move=self.ycor()+24
        if (x_move, y_move) not in self.walls:
            self.goto(x_move, y_move)
    
    def move_down(self):
        x_move=self.xcor()
        y_move=self.ycor()-24
        
        if (x_move, y_move) not in self.walls:
            self.goto(x_move, y_move)
    
    def move_left(self):
        x_move=self.xcor()-24
        y_move=self.ycor()
        
        if (x_move, y_move) not in self.walls:
            self.goto(x_move, y_move)
        
    def move_right(self):
        x_move=self.xcor()+24
        y_move=self.ycor()
        
        if (x_move, y_move) not in self.walls:
            self.goto(x_move, y_move)
    

    def detect_collision(self, object): 
        
        if (object.xcor(), object.ycor()) == (self.xcor(), self.ycor()):
            
            if type(object).__name__ == 'Treasure':

                object.destroy()
                
                return(object.goal_index, object.value)
            
            elif type(object).__name__ == 'Enemy':
                
                self.goto(self.start_pos[0], self.start_pos[1])
            
            
class Enemy(turtle.Turtle):
    
    def __init__(self, walls):
        turtle.Turtle.__init__(self)
        self.shape('square')
        self.color('red')
        self.penup()
        self.speed(0)
        
        self.walls=list(walls)
        self.direction=np.random.choice(['left', 'right', 'up','down'])
        self.direction_mapping={'left':(-24, 0), 'right':(24, 0),'up':(0, 24), 'down':(0,-24)}
        

    
    def move(self):
        
        new_x=self.xcor() + self.direction_mapping[self.direction][0]
        new_y=self.ycor() + self.direction_mapping[self.direction][1]
        
        if (new_x, new_y) not in self.walls:
            self.goto(new_x, new_y)
        else:
            #loop to make the direction only those the arent selected now
            self.direction=np.random.choice([i for i in ['left', 'right', 'up','down'] if i!= self.direction])
        
        turtle.ontimer(self.move, t=random.randint(100, 200))
    
    def destroy(self):
        self.goto(2000, 2000)
        self.clear()
    

    
class maze_game():

    def __init__(self, num_level, keys=['Up', 'Down', 'Right', 'Left']):
        
        #set the number of levels for the game as a subset of the number in levels directory for 
        #easy contorl of the game length
        self.levels=[np.genfromtxt(level, delimiter=',') for num, level in enumerate(glob.glob('levels/level*.csv')) if num < num_level]
        self.goals=[open(goal , 'r').read() for num, goal in enumerate(glob.glob('levels/goal*.txt')) if num < num_level]
        self.walls=[]
        
        
        self.goal_word=' '.join(self.goals)
        #collected letter
        self.letter_indexes=list(range(len(self.goal_word)))
        self.used_indexes=[]

        self.collected_letters=['_' for z in range(len(self.goal_word))]
    
    def setup_maze(self, level, pen, player, treasures, enemies):
    
        #create a list of coordiantes to interate over
        coordinates=itr.product(range(level.shape[0]), range(level.shape[1]))
        for x,y in coordinates:
        
            cor_value=level[x][y]
        
            screen_x = -288 + (x*24)
            screen_y = 288 - (y*24)
        
        
            if cor_value==1.0:
                pen.goto(screen_x, screen_y)
                pen.stamp()
                
                self.walls.append((screen_x, screen_y))
        
            if cor_value==2:
                player.start_pos=(screen_x, screen_y)
                player.goto(screen_x, screen_y)
                
        
        #set treasure coordinates
        tx, ty = np.where(level==3)
        
        for tcor in range(len(tx)):
            
            st_x= -288 + (tx[tcor]*24)
            st_y = 288 - (ty[tcor]*24)
           
            treasures[tcor].goto(st_x, st_y)
           
           
        ex, ey = np.where(level==4)
        
        for ecor in range(len(ex)):
            
            se_x= -288 + (ex[ecor]*24)
            se_y = 288 - (ey[ecor]*24)
           
            enemies[ecor].goto(se_x, se_y)
           

            

    def run_game(self):
        

            

        for ilvl, level in enumerate(self.levels):
                        
            wn=turtle.Screen()
            wn.setup(700, 700)
            wn.tracer(0)
            pen=Pen()
        
            
            #wn.bgcolor('Black')

            turtle.write(arg="Level " + str(ilvl+1), move=False, align="center", font=("Arial", 40, "normal"))
            
            for i in range(10):
                wn.update()

            time.sleep(5)
            wn.clear()
            
            if ilvl==0:
                
                turtle.write(arg="Collect Treasure Sqaures\nto Complete the Word", move=False, align="center", font=("Arial", 40, "normal"))
            
                for i in range(10):
                    wn.update()

                time.sleep(5)
                wn.clear()
            
            col_letters=''.join(self.collected_letters)
            
            turtle.write(arg=col_letters, move=False, align="center", font=("Arial", 40, "normal"))
            
            for i in range(10):
                wn.update()
            time.sleep(5)
            wn.clear()
            
            print self.collected_letters
            #find walls for player initation
            x_wall , y_wall = np.where(level==1)
            walls=list(zip(-288 + (x_wall*24),  288 - (y_wall*24)))
            
            num_treasures, _ = np.where(level==3)
            num_enemies, _ = np.where(level==4)
            
           
            
            player=Player(walls)
            
            possible_indexes=[idx for idx in self.letter_indexes if not idx in self.used_indexes]

            level_letters=np.random.choice(possible_indexes, len(num_treasures), replace=True)

            self.used_indexes.extend(level_letters)
            

            #add the treasure components and mark with the letter values,indexes in the word
            #so the the player class can track what it collect
            treasures=[Treasure(value=self.goal_word[i], goal_index=i) for i in level_letters]
            enemies=[Enemy(walls) for i in range(len(num_enemies))]
            
            
            #set controls 
            turtle.listen()
            turtle.onkey(player.move_up, 'Up')
            turtle.onkey(player.move_down, 'Down')
            turtle.onkey(player.move_right, 'Right')
            turtle.onkey(player.move_left, 'Left')
            
            self.setup_maze(level, pen, player, treasures, enemies)
            
            
            for en in enemies:
                en.move()

            while True:
            
                for tr in treasures:
                    t=player.detect_collision(tr)
                    if t:
                        self.collected_letters[t[0]]=t[1]
                    
                for en in enemies:
                    
                    player.detect_collision(en)
                    
                
                #check to see if all the treasures have been found
                
                tresure_test=np.array([t.found for t in treasures])
                
                if tresure_test.all():
                    
                    for en in enemies:
                        en.destroy()
                    
                    wn.clear()
                    wn.bye()
                    break
                    
                wn.update()
        
        print(self.collected_letters)


game=maze_game(num_level=6)
game.run_game()

             