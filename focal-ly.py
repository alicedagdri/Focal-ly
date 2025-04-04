#! /usr/bin/env python

import pygame, csv, random

from pygame.locals import (
        QUIT,
)


### CONSTANTS

LEFT = 1

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

GRID_WIDTH = 336
GRID_HEIGHT = 402

BORDER_THICKNESS = 2

HEADER_HEIGHT = 100

BUFFER_THICKNESS = 30

KEYBOARD_WIDTH = 536
KEYBOARD_HEIGHT = 158


### CLASSES

class Tile(pygame.sprite.Sprite):
        def __init__(self, ltr="blank"):
                super(Tile, self).__init__()
                self.dimensions = (50, 50)
                self.surf = pygame.transform.scale(pygame.image.load(f"graphics/default/{ltr}.png").convert(), self.dimensions)
                self.surf.set_colorkey((0,0,0))
                self.rect = self.surf.get_rect()
                self.letter = ltr
        def setRectCoordinates(self, x, y):
                self.rect = pygame.Rect(x, y, self.rect[2], self.rect[3])

class LetterKey(Tile):
        def __init__(self, ltr):
                super(LetterKey, self).__init__(ltr)
        def setColor(self, color):
                self.surf = pygame.transform.scale(pygame.image.load("graphics/%s/%s.png" % (color, self.letter)).convert(), self.dimensions)
                self.surf.set_colorkey((0,0,0))

class ControlKey(Tile):
        def __init__(self, ltr):
                super(ControlKey, self).__init__(ltr)
                self.dimensions = (100, 50)
                self.surf = pygame.transform.scale(pygame.image.load(f"graphics/default/{ltr}.png").convert(), self.dimensions)
                self.surf.set_colorkey((0,0,0))
                self.rect = self.surf.get_rect()

class InputKey(Tile):
        def __init__(self):
                super(InputKey, self).__init__()
                self.dimensions = (60,60)
                self.surf = pygame.transform.scale(pygame.image.load("graphics/blank.png").convert(), self.dimensions)
                self.surf.set_colorkey((0,0,0))
                self.rect = self.surf.get_rect()
        def setLetter(self, ltr):
                self.surf = pygame.transform.scale(pygame.image.load(f"graphics/default/{ltr}.png").convert(), (60,60))
                self.surf.set_colorkey((0,0,0))
                self.letter = ltr
        def setColor(self, color):
                self.surf = pygame.transform.scale(pygame.image.load(f"graphics/{color}/{self.letter}.png").convert(), (60, 60))
                self.surf.set_colorkey((0,0,0))


### FUNCTIONS

def init_grid():
        grid = dict()
        for i in range(1, 7):
                for j in range(1, nbchar+1):
                        grid[i*10+j] = InputKey()
                        x = ((SCREEN_WIDTH-GRID_WIDTH)/2)+6+66*(j-1)
                        y = HEADER_HEIGHT+BUFFER_THICKNESS+6+66*(i-1)
                        grid[i*10+j].setRectCoordinates(x, y)
                        screen.blit(grid[i*10+j].surf, grid[i*10+j].rect)
        pygame.display.flip()
        return grid
        
def init_keyboard():
        keyboard = dict()
        i = 0
        for ltr in ("a", "á", "e", "é", "i", "í", "o", "ó", "u", "ú"):
                keyboard[ltr] = LetterKey(ltr)
                x = ((SCREEN_WIDTH-KEYBOARD_WIDTH)/2)+54*i
                y = HEADER_HEIGHT + 2*BUFFER_THICKNESS + GRID_HEIGHT
                keyboard[ltr].setRectCoordinates(x, y)
                screen.blit(keyboard[ltr].surf, keyboard[ltr].rect)
                i+=1
        i = 0
        for ltr in ("b", "c", "d", "f", "g", "h", "l", "m", "n"):
                keyboard[ltr] = LetterKey(ltr)
                x = ((SCREEN_WIDTH-KEYBOARD_WIDTH)/2)+27+54*i
                y = HEADER_HEIGHT + 2*BUFFER_THICKNESS + GRID_HEIGHT + 54
                keyboard[ltr].setRectCoordinates(x, y)
                screen.blit(keyboard[ltr].surf, keyboard[ltr].rect)
                i+=1
        keyboard["tomhas"] = ControlKey("tomhas")
        x = ((SCREEN_WIDTH-KEYBOARD_WIDTH)/2)+31
        y = HEADER_HEIGHT + 2*BUFFER_THICKNESS + GRID_HEIGHT + 108
        keyboard["tomhas"].setRectCoordinates(x, y)
        screen.blit(keyboard["tomhas"].surf, keyboard["tomhas"].rect)
        i = 0
        for ltr in ("p", "r", "s", "t", "v"):
                keyboard[ltr] = LetterKey(ltr)
                x = ((SCREEN_WIDTH-KEYBOARD_WIDTH)/2)+135+54*i
                y = HEADER_HEIGHT + 2*BUFFER_THICKNESS + GRID_HEIGHT + 108
                keyboard[ltr].setRectCoordinates(x, y)
                screen.blit(keyboard[ltr].surf, keyboard[ltr].rect)
                i+=1
        keyboard["delete"] = ControlKey("delete")
        x = ((SCREEN_WIDTH-KEYBOARD_WIDTH)/2)+135+54*5
        y = HEADER_HEIGHT + 2*BUFFER_THICKNESS + GRID_HEIGHT + 108
        keyboard["delete"].setRectCoordinates(x, y)
        screen.blit(keyboard["delete"].surf, keyboard["delete"].rect)
        pygame.display.flip()
        return keyboard

#works for either grid (idx is the ID) or keyboard tiles (idx is the letter)
def flipTile(dictionary, idx, color):
        global screen
        dictionary[idx].setColor(color)
        screen.blit(dictionary.get(idx).surf, dictionary.get(idx).rect)
        pygame.display.flip()

def writeTile(line, column, ltr):
        global grid, screen
        grid.get(line * 10 + column).setLetter(ltr)
        screen.blit(grid.get(line*10+column).surf, grid.get(line*10+column).rect)
        pygame.display.flip()

#max: line 476
def selectTarget(nbLetters):
        nbLetters = ((nbLetters - 5) % 3) + 5
        i = 1
        targetindex = random.randrange(1, 476)
        target = ""
        target_translation = ""
        with open('databases/targets.csv', newline='') as targets:
                csvlines = csv.reader(targets, delimiter=';', quotechar='|')
                for row in csvlines:
                        if i == targetindex:
                                if len(row[0]) == nbLetters:
                                        target = row[0]
                                        target_translation = row[1]
                                        break
                                else:
                                        targetindex+=1
                        else:
                                i+=1
        print(f"word picked: {target}, meaning {target_translation} (line {targetindex}).")
        return (target.lower(), target_translation.lower())

#returns false if the click was not on a key, returns the index (a string) otherwise
def onClickKeyboard(x, y):
        for k in keyboard:
                if keyboard[k].rect.collidepoint(x, y):
                        return k
        return False

def onKeyClicked(key, tile):
        global current_col, current_line, nbchar, input_word, target_word, target
        if current_col == nbchar and key == "tomhas":
                if isInDict("".join(input_word.values())):
                        won = checkLetters()
                        if won:
                                print("omg won")
                                endOfGame(won)
                        else:
                                current_line+=1
                                if current_line==7:
                                        print("cringe :(")
                                        endOfGame(won)
                                else:
                                        current_col = 0
                                        input_letters = dict()
                                        input_word = dict()
                                        target_word = init_target_word(target)
        elif current_col > 0 and key == "delete":
                writeTile(current_line, current_col, "blank")
                current_col-=1
        elif current_col < nbchar and key not in ("tomhas", "delete"):
                current_col+=1
                input_word[current_col] = key
                writeTile(current_line, current_col, key)
        else:
                sound_wrong = pygame.mixer.Sound("sounds/wrong.mp3")
                sound_wrong.play()
                pygame.time.wait(100)
                pygame.mixer.music.pause()
                pygame.time.wait(500)
                pygame.mixer.music.unpause()

def isInDict(word):
        global nbchar
        with open(f"databases/dict{nbchar}.csv", newline='') as dic:
                words = csv.reader(dic, delimiter=';', quotechar='|')
                for dicword in words:
                        if dicword[0].lower() == word:
                                return True
        sound_wrong = pygame.mixer.Sound("sounds/wrong.mp3")
        sound_wrong.play()
        pygame.time.wait(100)
        pygame.mixer.music.pause()
        pygame.time.wait(500)
        pygame.mixer.music.unpause()
        return False

def checkLetters():
        global nbchar, current_line, grid, keyboard, current_col, input_letters
        won = False
        tiles_colors = dict()
        tiles_colors = checkGreens(tiles_colors)
        if len(tiles_colors) == nbchar:
                won = True
        else:
                tiles_colors = checkYellows(tiles_colors)
                
        for idx in tiles_colors:
                if tiles_colors[idx] == "grey":
                        flipTile(keyboard, input_letters[idx-1], tiles_colors[idx])
        for idx in tiles_colors:
                if tiles_colors[idx] == "yellow":
                        flipTile(keyboard, input_letters[idx-1], tiles_colors[idx])
        for idx in tiles_colors:
                if tiles_colors[idx] == "green":
                        flipTile(keyboard, input_letters[idx-1], tiles_colors[idx])
                        
        for i in range(1, len(tiles_colors)+1):
                pygame.time.wait(250)
                flipTile(grid, current_line*10+i, tiles_colors[i])

        return won

def checkGreens(tiles_colors):
        global nbchar, input_word, target_word, input_letters
        input_letters = "".join(input_word.values())
        for i in range(1, nbchar+1):
                if input_word[i] == target_word[i]:
                        tiles_colors[i] = "green"
                        input_word.pop(i)
                        target_word.pop(i)
        return tiles_colors

def checkYellows(tiles_colors):
        global nbchar, input_word, target_word
        for i in range(1, nbchar+1):
                if i in input_word:
                        for j in range(1, nbchar+1):
                                if j in target_word:
                                        if input_word[i] == target_word[j]:
                                                tiles_colors[i] = "yellow"
                                                target_word.pop(j)
                        input_word.pop(i)
        for idx in range(1, nbchar+1):
                if idx in tiles_colors:
                        pass
                else:
                        tiles_colors[idx] = "grey"
        return tiles_colors

def init_target_word(target):
        t_w = dict()
        for i in range(1, len(target)+1):
                t_w[i] = target[i-1]
        return t_w

def endOfGame(won):
        global keyboard_rect, target, target_translation
        displayedword = "Maith thú féin" if won else "Is mairg"
        displayedl1 = f"{displayedword}! Today's word was {target}."
        displayedl2 = f"Meaning: {target_translation}."
        displayedl3 = "To hear the pronunciation, visit:"
        displayedl4 = f"https://www.teanglann.ie/en/fuaim/{target}"
        ringofkerry = pygame.font.Font("fonts/Ring of Kerry.otf", 16)
        messageZone = pygame.transform.scale(pygame.image.load(f"graphics/messageZone.png").convert(), (552,174))
        messageZone.set_colorkey((0,0,0))
        screen.blit(messageZone, keyboard_rect)
        label1 = ringofkerry.render(displayedl1, 1, (255, 255, 255))
        label2 = ringofkerry.render(displayedl2, 1, (255, 255, 255))
        label3 = ringofkerry.render(displayedl3, 1, (255, 255, 255))
        label4 = ringofkerry.render(displayedl4, 1, (255, 255, 255))
        screen.blit(label1, (264, 564))
        screen.blit(label2, (394, 604))
        screen.blit(label3, (304, 644))
        screen.blit(label4, (244, 684))
        pygame.display.flip()

#is mairg: too bad

### MAIN

current_line = 1
current_col = 0
nbchar = 5
input_letters = ""

input_word = dict()
target_word = dict()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((135, 152, 106))

ringofkerry = pygame.font.Font("fonts/Ring of Kerry.otf", 48)
title = ringofkerry.render("Focal-ly", 1, (255,255,255))
screen.blit(title, ((SCREEN_WIDTH/2)-148, BUFFER_THICKNESS))
pygame.display.flip()

gridBorder = pygame.Surface((GRID_WIDTH+BORDER_THICKNESS*2,GRID_HEIGHT+BORDER_THICKNESS*2))
gridBorder.fill((255, 255, 255))
screen.blit(gridBorder, ((SCREEN_WIDTH-GRID_WIDTH)/2-BORDER_THICKNESS, HEADER_HEIGHT+BUFFER_THICKNESS-BORDER_THICKNESS))

gridZone = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
gridZone.fill((149, 165, 141))
screen.blit(gridZone, ((SCREEN_WIDTH-GRID_WIDTH)/2, HEADER_HEIGHT+BUFFER_THICKNESS))

#keyboardZone = pygame.Surface((KEYBOARD_WIDTH+8*BORDER_THICKNESS, KEYBOARD_HEIGHT+8*BORDER_THICKNESS))
keyboard_rect = pygame.Rect(((SCREEN_WIDTH-KEYBOARD_WIDTH)/2-4*BORDER_THICKNESS, HEADER_HEIGHT+GRID_HEIGHT+2*BUFFER_THICKNESS-4*BORDER_THICKNESS), (KEYBOARD_WIDTH+8*BORDER_THICKNESS, KEYBOARD_HEIGHT+8*BORDER_THICKNESS)) 
#keyboardZone.fill((0,0,0))
#screen.blit(keyboardZone, keyboard_rect)

pygame.display.flip()

pygame.mixer.init()
music = pygame.mixer.music.load("sounds/ambient_music.mp3")
pygame.mixer.music.play(-1)

(target, target_translation) = selectTarget(5)
target_word = init_target_word(target)

grid = init_grid()

keyboard = init_keyboard()


running = True
while running:

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
                elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
                        if keyboard_rect.collidepoint(pygame.mouse.get_pos()):
                                k = onClickKeyboard(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                                if k:
                                        onKeyClicked(k, keyboard.get(k))
                                        


        pygame.display.flip()

pygame.quit()



        
