#Using menu in pygame
import os
import sys
import pygame as p 
import subprocess
# import ChessMain

p.init()

HEIGHT = WIDTH = 500

screen = p.display.set_mode([HEIGHT, WIDTH])

p.display.set_caption("Menu")
bot = 0
fps = 60
timer = p.time.Clock()
main_menu = False 
# show_options = False  # Variable to control the display of the options

font = p.font.Font("freesansbold.ttf", 24)
menu_command = 0 
playClicked = False

class Button:
   def __init__(self,txt,pos):  
     self.text = txt
     self.pos = pos
     self.button = p.rect.Rect((self.pos[0], self.pos[1]), (260,40))


   def draw(self):
        btn = p.draw.rect(screen , 'light gray', self.button , 0 ,5)
        p.draw.rect(screen , 'dark gray', self.button , 5 ,5)

        text = font.render(self.text , True, 'black')
        screen.blit(text, (self.pos[0] + 15, self.pos[1] + 7))

   def check_clicked(self):    
         if self.button.collidepoint(p.mouse.get_pos()) and p.mouse.get_pressed()[0]:
            return True 
         else:
            return False

def draw_game():
    button = Button("Main Menu",(230, 450))
    button.draw()

    return button.check_clicked()      

def draw_menu():
    command = 0
    p.draw.rect(screen , 'black' , [100,100,300,300]) 
    # exit menu button 
    menu_btn = Button('Exit Menu' , (120 ,350))
    btn1 = Button('Play' , (120 ,180), )

    btn2 = Button('Options' , (120 ,240))
    btn3 = Button('Rules' , (120 ,292))
        
    global playClicked
    if playClicked == True:
        Tp = Button('Two Players' , (120 ,240))
        Comp = Button('v/s computer' , (120 ,292))

        Tp.draw()
        Comp.draw()
        if Tp.check_clicked():
            global bot
            bot = 1
            # print(bot)
            # subprocess.run(['python', 'ChessMain.py'])
            # subprocess.Popen([sys.executable, 'ChessMain.py'])
            quit_event = p.event.Event(p.QUIT)
            p.event.post(quit_event)
            # p.quit()            

        if Comp.check_clicked():
            bot = 2
            quit_event = p.event.Event(p.QUIT)
            p.event.post(quit_event)
            # p.quit()            

    else:    
        menu_btn.draw()
        btn1.draw()
        btn2.draw()
        btn3.draw()
    if menu_btn.check_clicked():
        command = 1 

    if btn1.check_clicked():
        # subprocess.run(['python', 'ChessMain.py'])
        # btn2 = Button('Two Players' , (120 ,240))
        # btn3 = Button('Computer' , (120 ,292))
        # btn2.draw()
        # btn3.draw()
        command = 2  
        
        playClicked = True
        
        # return False

    if btn2.check_clicked():
        command = 3  

    if btn3.check_clicked():
        command = 4
    return command
    # # return not menu_btn.check_clicked() 

# def draw(self):
#     pass

run = True

while run:
    screen.fill('light blue')
    timer.tick(fps)    
    if main_menu:
        menu_command = draw_menu()
        # if menu_command > 0:  
        #  main_menu = False
    else:
       main_menu =  draw_game()
    #    if menu_command > 1: 
    #         text = font.render(f'Button {menu_command - 1} was clicked!', True , 'black')
    #         screen.blit(text, (100,200))

    
    # if playClicked == True:
    #     btn1 = Button('Two Players' , (120 ,240))
    #     btn2 = Button('v/s computer' , (120 ,292))

    #     btn1.draw()
    #     btn2.draw()

    for event in p.event.get():
        if event.type == p.QUIT:
            print("Closing menu")
            run = False


    # if event.type == BUTTON_PRESSED:
    #          if event.ui_element == btn2:
    #         # Run the chess.py file
    #              subprocess.run(['python', 'ChessMain.py'])   
    #              run = False



    p.display.flip()
p.quit()            

















''' 9 '''




# import pygame as p

# p.init()

# HEIGHT = WIDTH = 500
# screen = p.display.set_mode([HEIGHT, WIDTH])
# p.display.set_caption("Menu")

# fps = 60
# timer = p.time.Clock()
# main_menu = True  # Start with the main menu being displayed
# temp = False  # Variable to control the display of the options
# font = p.font.Font("freesansbold.ttf", 24)

# class Button:
#     def __init__(self, txt, pos):
#         self.text = txt
#         self.pos = pos
#         self.button = p.rect.Rect((self.pos[0], self.pos[1]), (260, 40))

#     def draw(self):
#         p.draw.rect(screen, 'light gray', self.button, 0, 5)
#         p.draw.rect(screen, 'dark gray', self.button, 5, 5)
#         text = font.render(self.text, True, 'black')
#         screen.blit(text, (self.pos[0] + 15, self.pos[1] + 7))

#     def check_clicked(self):
#         if self.button.collidepoint(p.mouse.get_pos()) and p.mouse.get_pressed()[0]:
#             return True
#         return False

# def draw_game():
#     button = Button("Main Menu", (230, 450))
#     button.draw()
#     return button.check_clicked()

# def draw_menu():
#     p.draw.rect(screen, 'black', [100, 100, 300, 300])
#     menu_btn = Button('Exit Menu', (120, 350))
#     btn1 = Button('Play', (120, 180))
#     btn2 = Button('Options', (120, 240))
#     btn3 = Button('Rules', (120, 292))

#     menu_btn.draw()
#     btn1.draw()
#     btn2.draw()
#     btn3.draw()

#     if menu_btn.check_clicked():
#         return 1

#     if btn1.check_clicked():
#         global temp
#         temp = True  # Set temp to True to trigger the display of new buttons
#         return 2

#     if btn2.check_clicked():
#         return 3

#     if btn3.check_clicked():
#         return 4

#     return 0

# run = True
# while run:
#     screen.fill('light blue')
#     timer.tick(fps)

#     if main_menu:
#         menu_command = draw_menu()
#         if menu_command > 0:
#             main_menu = False
#     elif temp:
#         # Draw the "Two Players" and "v/s Computer" buttons
#         btn1 = Button('Two Players', (120, 240))
#         btn2 = Button('v/s Computer', (120, 292))
#         back_btn = Button('Back to Main Menu', (120, 350))

#         btn1.draw()
#         btn2.draw()
#         back_btn.draw()

#         if back_btn.check_clicked():
#             temp = False
#             main_menu = True
#     else:
#         main_menu = draw_game()

#     for event in p.event.get():
#         if event.type == p.QUIT:
#             run = False

#     p.display.flip()

# p.quit()
