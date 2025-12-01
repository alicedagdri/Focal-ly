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

TILE_WIDTH = 60

GRID_WIDTH = 336
GRID_HEIGHT = 402

BORDER_THICKNESS = 2

HEADER_HEIGHT = 100

BUFFER_THICKNESS = 30

KEYBOARD_WIDTH = 590
KEYBOARD_HEIGHT = 158


### CLASSES

class Tile(pygame.sprite.Sprite):
        def __init__(self, font="focally", ltr="blank"):
                super(Tile, self).__init__()
                self.dimensions = (50, 50)
                self.surf = pygame.transform.scale(pygame.image.load(f"graphics/{font}/default/{ltr}.png").convert(), self.dimensions)
                self.surf.set_colorkey((0,0,0))
                self.rect = self.surf.get_rect()
                self.letter = ltr
        def setRectCoordinates(self, x, y):
                self.rect = pygame.Rect(x, y, self.rect[2], self.rect[3])

class LetterKey(Tile):
        def __init__(self, font, ltr):
                super(LetterKey, self).__init__(font, ltr)
        def setColor(self, color, font):
                self.surf = pygame.transform.scale(pygame.image.load("graphics/%s/%s/%s.png" % (font, color, self.letter)).convert(), self.dimensions)
                self.surf.set_colorkey((0,0,0))

class ControlKey(Tile):
        def __init__(self, font, ltr):
                super(ControlKey, self).__init__(font, ltr)
                self.dimensions = (100, 50)
                self.surf = pygame.transform.scale(pygame.image.load(f"graphics/{font}/default/{ltr}.png").convert(), self.dimensions)
                self.surf.set_colorkey((0,0,0))
                self.rect = self.surf.get_rect()

class InputKey(Tile):
        def __init__(self):
                super(InputKey, self).__init__()
                self.dimensions = (60,60)
                self.surf = pygame.transform.scale(pygame.image.load("graphics/focally/blank.png").convert(), self.dimensions)
                self.surf.set_colorkey((0,0,0))
                self.rect = self.surf.get_rect()
        def setLetter(self, ltr, font):
                self.surf = pygame.transform.scale(pygame.image.load(f"graphics/{font}/default/{ltr}.png").convert(), (60,60))
                self.surf.set_colorkey((0,0,0))
                self.letter = ltr
        def setColor(self, color, font):
                self.surf = pygame.transform.scale(pygame.image.load(f"graphics/{font}/{color}/{self.letter}.png").convert(), (60, 60))
                self.surf.set_colorkey((0,0,0))


### FUNCTIONS

def getGridWidth():
        global nbchar
        return (6*(nbchar+1)+TILE_WIDTH*nbchar)

def init_grid():
        grid = dict()
        for i in range(1, 7):
                for j in range(1, nbchar+1):
                        grid[i*10+j] = InputKey()
                        x = ((SCREEN_WIDTH-getGridWidth())/2)+6+66*(j-1)
                        y = HEADER_HEIGHT+BUFFER_THICKNESS+6+66*(i-1)
                        grid[i*10+j].setRectCoordinates(x, y)
                        screen.blit(grid[i*10+j].surf, grid[i*10+j].rect)
        pygame.display.flip()
        return grid
        
def init_keyboard():
        global lang, accessible_mode
        keyboard = dict()
        if lang == "irish":
                font = "access_irish" if accessible_mode else "focally"
                i = 0.5
                for ltr in ("a", "á", "e", "é", "i", "í", "o", "ó", "u", "ú"):
                        keyboard[ltr] = LetterKey(font, ltr)
                        x = ((SCREEN_WIDTH-KEYBOARD_WIDTH)/2)+54*i
                        y = HEADER_HEIGHT + 2*BUFFER_THICKNESS + GRID_HEIGHT
                        keyboard[ltr].setRectCoordinates(x, y)
                        screen.blit(keyboard[ltr].surf, keyboard[ltr].rect)
                        i+=1
                i = 1
                for ltr in ("b", "c", "d", "f", "g", "h", "l", "m", "n"):
                        keyboard[ltr] = LetterKey(font, ltr)
                        x = ((SCREEN_WIDTH-KEYBOARD_WIDTH)/2)+54*i
                        y = HEADER_HEIGHT + 2*BUFFER_THICKNESS + GRID_HEIGHT + 54
                        keyboard[ltr].setRectCoordinates(x, y)
                        screen.blit(keyboard[ltr].surf, keyboard[ltr].rect)
                        i+=1
                keyboard["enter"] = ControlKey(font, "enter")
                x = ((SCREEN_WIDTH-KEYBOARD_WIDTH)/2)+58
                y = HEADER_HEIGHT + 2*BUFFER_THICKNESS + GRID_HEIGHT + 108
                keyboard["enter"].setRectCoordinates(x, y)
                screen.blit(keyboard["enter"].surf, keyboard["enter"].rect)
                i = 3
                for ltr in ("p", "r", "s", "t", "v"):
                        keyboard[ltr] = LetterKey(font, ltr)
                        x = ((SCREEN_WIDTH-KEYBOARD_WIDTH)/2)+54*i
                        y = HEADER_HEIGHT + 2*BUFFER_THICKNESS + GRID_HEIGHT + 108
                        keyboard[ltr].setRectCoordinates(x, y)
                        screen.blit(keyboard[ltr].surf, keyboard[ltr].rect)
                        i+=1
                keyboard["delete"] = ControlKey(font, "delete")
                x = ((SCREEN_WIDTH-KEYBOARD_WIDTH)/2)+162+54*5
                y = HEADER_HEIGHT + 2*BUFFER_THICKNESS + GRID_HEIGHT + 108
                keyboard["delete"].setRectCoordinates(x, y)
                screen.blit(keyboard["delete"].surf, keyboard["delete"].rect)
        else:
                font = "access_welsh" if accessible_mode else "geirio"
                i = 0
                keyboard["enter"] = ControlKey(font, "enter")
                x = ((SCREEN_WIDTH-KEYBOARD_WIDTH)/2)+31
                y = HEADER_HEIGHT + 2*BUFFER_THICKNESS + GRID_HEIGHT
                keyboard["enter"].setRectCoordinates(x, y)
                screen.blit(keyboard["enter"].surf, keyboard["enter"].rect)
                i = 0
                for ltr in ("a", "â", "e", "ê", "i", "î"):
                        keyboard[ltr] = LetterKey(font, ltr)
                        x = ((SCREEN_WIDTH-KEYBOARD_WIDTH)/2)+135+54*i
                        y = HEADER_HEIGHT + 2*BUFFER_THICKNESS + GRID_HEIGHT
                        keyboard[ltr].setRectCoordinates(x, y)
                        screen.blit(keyboard[ltr].surf, keyboard[ltr].rect)
                        i+=1
                keyboard["delete"] = ControlKey(font, "delete")
                x = ((SCREEN_WIDTH-KEYBOARD_WIDTH)/2)+135+54*i
                y = HEADER_HEIGHT + 2*BUFFER_THICKNESS + GRID_HEIGHT
                keyboard["delete"].setRectCoordinates(x, y)
                screen.blit(keyboard["delete"].surf, keyboard["delete"].rect)
                i = 0
                for ltr in ("o", "ô", "u", "û", "w", "ŵ", "y", "ŷ", "b", "c"):
                        keyboard[ltr] = LetterKey(font, ltr)
                        x = ((SCREEN_WIDTH-KEYBOARD_WIDTH)/2)+27+54*i
                        y = HEADER_HEIGHT + 2*BUFFER_THICKNESS + GRID_HEIGHT + 54
                        keyboard[ltr].setRectCoordinates(x, y)
                        screen.blit(keyboard[ltr].surf, keyboard[ltr].rect)
                        i+=1
                i = 0
                for ltr in ("d", "f", "g", "h", "l", "m", "n", "p", "r", "s", "t"):
                        keyboard[ltr] = LetterKey(font, ltr)
                        x = ((SCREEN_WIDTH-KEYBOARD_WIDTH)/2)+54*i
                        y = HEADER_HEIGHT + 2*BUFFER_THICKNESS + GRID_HEIGHT + 108
                        keyboard[ltr].setRectCoordinates(x, y)
                        screen.blit(keyboard[ltr].surf, keyboard[ltr].rect)
                        i+=1
        pygame.display.flip()
        return keyboard

#works for either grid (idx is the ID) or keyboard tiles (idx is the letter)
def flipTile(dictionary, idx, color):
        global screen, accessible_mode, lang
        if accessible_mode:
                font = "access_welsh" if lang == "welsh" else "access_irish"
        else:
                font = "geirio" if lang == "welsh" else "focally"
        dictionary[idx].setColor(color, font)
        screen.blit(dictionary.get(idx).surf, dictionary.get(idx).rect)
        pygame.display.flip()

def writeTile(line, column, ltr):
        global grid, screen, accessible_mode, lang
        if accessible_mode:
                font = "access_welsh" if lang == "welsh" else "access_irish"
        else:
                font = "geirio" if lang == "welsh" else "focally"
        grid.get(line * 10 + column).setLetter(ltr, font)
        screen.blit(grid.get(line*10+column).surf, grid.get(line*10+column).rect)
        pygame.display.flip()

#max: line 476
def selectTarget(nbLetters):
        global lang
        nbLetters = ((nbLetters - 5) % 3) + 5
        if lang == "irish":
                i = 1
                targetindex = random.randrange(1, 476)
                target = ""
                target_translation = ""
                with open(f"databases/{lang}/targets.csv", newline='') as targets:
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
        else:
                i = 1
                targetindex = random.randrange(1, 50)
                target = ""
                target_translation = ""
                with open(f"databases/{lang}/target{nbLetters}.csv", newline='') as targets:
                        csvlines = csv.reader(targets, delimiter=',', quotechar='|')
                        for row in csvlines:
                                if i == targetindex:
                                        target = row[0]
                                        target_translation = row[1]
                                        break
                                else:
                                        i+=1
        print(f"word picked: {target}, meaning {target_translation} (line {targetindex}).")
        return (target.lower(), target_translation.lower())

#returns false if the click was not on a key, returns the index (a string) otherwise
def onClickKeyboard(x, y):
        if is_game_on:
                for k in keyboard:
                        if keyboard[k].rect.collidepoint(x, y):
                                return k
        return False

def onKeyClicked(key, tile):
        global current_col, current_line, nbchar, input_word, target_word, target
        if current_col == nbchar and key == "enter":
                if isInDict("".join(input_word.values())):
                        won = checkLetters()
                        if won:
                                endOfGame(won)
                        else:
                                current_line+=1
                                if current_line==7:
                                        endOfGame(won)
                                else:
                                        current_col = 0
                                        input_letters = dict()
                                        input_word = dict()
                                        target_word = init_target_word(target)
        elif current_col > 0 and key == "delete":
                writeTile(current_line, current_col, "blank")
                current_col-=1
        elif current_col < nbchar and key not in ("enter", "delete"):
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
        global nbchar, lang
        with open(f"databases/{lang}/dict{nbchar}.csv", newline='') as dic:
                words = csv.reader(dic, delimiter=';', quotechar='|')
                for dicword in words:
                        if dicword[0].lower().replace('\x00','') == word.lower():
                                return True
        sound_wrong = pygame.mixer.Sound("sounds/wrong.mp3")
        sound_wrong.play()
        pygame.time.wait(100)
        pygame.mixer.music.pause()
        pygame.time.wait(500)
        pygame.mixer.music.unpause()
        print(word)
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

def play_music():
        pygame.mixer.init()
        music = pygame.mixer.music.load("sounds/ambient_music.mp3")
        pygame.mixer.music.play(-1)

def toggle_sound():
        global is_sound_on
        is_sound_on = not is_sound_on
        if is_sound_on:
                play_music()

def endOfGame(won):
        global keyboard_rect, target, target_translation, is_game_on, lang, accessible_mode
        if accessible_mode:
                font = "access_welsh" if lang == "welsh" else "access_irish"
        else:
                font = "geirio" if lang=="welsh" else "focally"
        displayedword = ("Maith thú féin" if won else "Is mairg") if lang == "irish" else ("Llongyfarchion" if won else "Dyna rhy ddrwg")
        displayedl1 = f"{displayedword}! Today's word was {target}."
        displayedl2 = f"Meaning: {target_translation}."
        displayedl3 = "To hear the pronunciation, visit:"
        displayedl4 = f"https://www.teanglann.ie/en/fuaim/{target}" if lang == "irish" else f"https://www.howtopronounce/welsh/{target}"
        selectedfont = pygame.font.Font(("fonts/Ring of Kerry.otf" if font == "focally" else ("fonts/UncialAntiqua.ttf" if font == "geirio" else "fonts/Lora.ttf")), (16 if font=="focally" else (20 if font=="geirio" else 24)))
        messageZone = pygame.transform.scale(pygame.image.load(f"graphics/messageZone.png").convert(), (604,174))
        messageZone.set_colorkey((0,0,0))
        screen.blit(messageZone, keyboard_rect)
        label1 = selectedfont.render(displayedl1, 1, (255, 255, 255))
        label2 = selectedfont.render(displayedl2, 1, (255, 255, 255))
        label3 = selectedfont.render(displayedl3, 1, (255, 255, 255))
        label4 = selectedfont.render(displayedl4, 1, (255, 255, 255))
        screen.blit(label1, ((270 if lang == "irish" and not accessible_mode else 290), 564))
        screen.blit(label2, ((400 if lang == "irish" and not accessible_mode else 420), 604))
        screen.blit(label3, ((310 if lang == "irish" and not accessible_mode else 330), 644))
        screen.blit(label4, ((250 if lang == "irish" and not accessible_mode else 270), 684))
        pygame.display.flip()
        is_game_on = False

#is mairg: too bad

def select_lang():
        global screen, lang
        lora = pygame.font.Font("fonts/Lora.ttf", 48)
        header = lora.render("Select language", 1, (255,255,255))
        screen.blit(header, ((SCREEN_WIDTH/2)-180, BUFFER_THICKNESS))
        irishflag = pygame.transform.scale(pygame.image.load(f"graphics/irish.png").convert(), (200,100))
        irishflag.set_colorkey((0,0,0))
        irishrect = pygame.Rect(((SCREEN_WIDTH/2)-BUFFER_THICKNESS-200), (2*BUFFER_THICKNESS+58), 200, 100)
        screen.blit(irishflag, irishrect)
        welshflag = pygame.transform.scale(pygame.image.load(f"graphics/welsh.png").convert(), (200,120))
        irishflag.set_colorkey((0,0,0))
        welshrect = pygame.Rect(((SCREEN_WIDTH/2)+BUFFER_THICKNESS), (2*BUFFER_THICKNESS+48), 200, 120)
        screen.blit(welshflag, welshrect)
        pygame.display.flip()
        running_select = True
        while running_select:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                running_select = False
                        elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
                                if irishrect.collidepoint(pygame.mouse.get_pos()):
                                        lang = "irish"
                                        running_select = False
                                elif welshrect.collidepoint(pygame.mouse.get_pos()):
                                        lang = "welsh"
                                        running_select = False
        if lang == "unknown":
                pygame.quit()
        else:
                select_nbchar()

def select_nbchar():
        global screen, nbchar
        lora = pygame.font.Font("fonts/Lora.ttf", 48)
        header = lora.render("Select number of letters", 1, (255,255,255))
        screen.blit(header, ((SCREEN_WIDTH/2)-260, (4*BUFFER_THICKNESS+168)))
        btn5 = pygame.transform.scale(pygame.image.load(f"graphics/5.png").convert(), (100,100))
        btn5.set_colorkey((0,0,0))
        rect5 = pygame.Rect(((SCREEN_WIDTH/2)-150-2*BUFFER_THICKNESS), (5*BUFFER_THICKNESS+216), 100, 100)
        screen.blit(btn5, rect5)
        btn6 = pygame.transform.scale(pygame.image.load(f"graphics/6.png").convert(), (100,100))
        btn6.set_colorkey((0,0,0))
        rect6 = pygame.Rect(((SCREEN_WIDTH/2)-50), (5*BUFFER_THICKNESS+216), 100, 100)
        screen.blit(btn6, rect6)
        btn7 = pygame.transform.scale(pygame.image.load(f"graphics/7.png").convert(), (100,100))
        btn7.set_colorkey((0,0,0))
        rect7 = pygame.Rect(((SCREEN_WIDTH/2)+50+2*BUFFER_THICKNESS), (5*BUFFER_THICKNESS+216), 100, 100)
        screen.blit(btn7, rect7)
        pygame.display.flip()
        running_select2 = True
        while running_select2:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                running_select2 = False
                        elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
                                if rect5.collidepoint(pygame.mouse.get_pos()):
                                        nbchar = 5
                                        running_select2 = False
                                elif rect6.collidepoint(pygame.mouse.get_pos()):
                                        nbchar = 6
                                        running_select2 = False
                                elif rect7.collidepoint(pygame.mouse.get_pos()):
                                        nbchar = 7
                                        running_select2 = False
        if nbchar == 0:
                pygame.quit()
        else:
                select_font()

def select_font():
        global screen, lang, accessible_mode
        lora = pygame.font.Font("fonts/Lora.ttf", 48)
        header = lora.render("Select font", 1, (255,255,255))
        screen.blit(header, ((SCREEN_WIDTH/2)-120, (7*BUFFER_THICKNESS+316)))
        celtic = pygame.transform.scale(pygame.image.load(f"graphics/celtic_{lang}.png").convert(), (200,100))
        celtic.set_colorkey((0,0,0))
        celticrect = pygame.Rect(((SCREEN_WIDTH/2)-200-BUFFER_THICKNESS), (8*BUFFER_THICKNESS+364), 200, 100)
        screen.blit(celtic, celticrect)
        legible = pygame.transform.scale(pygame.image.load(f"graphics/legible.png").convert(), (200,100))
        legible.set_colorkey((0,0,0))
        legiblerect = pygame.Rect(((SCREEN_WIDTH/2)+BUFFER_THICKNESS), (8*BUFFER_THICKNESS+364), 200, 100)
        screen.blit(legible, legiblerect)
        pygame.display.flip()
        doquit = False
        running_select3 = True
        while running_select3:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                running_select3 = False
                                doquit = True
                        elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
                                if celticrect.collidepoint(pygame.mouse.get_pos()):
                                        running_select3 = False
                                elif legiblerect.collidepoint(pygame.mouse.get_pos()):
                                        accessible_mode = True
                                        running_select3 = False
        if doquit:
                pygame.quit()

### MAIN

is_game_on = True
accessible_mode = False
is_sound_on = True
sound_volume = 100

current_line = 1
current_col = 0
nbchar = 0
input_letters = ""

input_word = dict()
target_word = dict()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((135, 152, 106))

lang = "unknown"
select_lang()
print(lang)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((135, 152, 106))
ringofkerry = pygame.font.Font(("fonts/Lora.ttf" if accessible_mode else ("fonts/Ring of Kerry.otf" if lang=="irish" else "fonts/UncialAntiqua.ttf")), 48)
title = ringofkerry.render(("Focal.ly" if lang == "irish" else "Geir.io"), 1, (255,255,255))
screen.blit(title, ((SCREEN_WIDTH/2)-(140 if not accessible_mode and lang == "irish" else 90), BUFFER_THICKNESS))
pygame.display.flip()

gridBorder = pygame.Surface((getGridWidth()+BORDER_THICKNESS*2,GRID_HEIGHT+BORDER_THICKNESS*2))
gridBorder.fill((255, 255, 255))
screen.blit(gridBorder, ((SCREEN_WIDTH-getGridWidth())/2-BORDER_THICKNESS, HEADER_HEIGHT+BUFFER_THICKNESS-BORDER_THICKNESS))

gridZone = pygame.Surface((getGridWidth(), GRID_HEIGHT))
gridZone.fill((149, 165, 141))
screen.blit(gridZone, ((SCREEN_WIDTH-getGridWidth())/2, HEADER_HEIGHT+BUFFER_THICKNESS))

#keyboardZone = pygame.Surface((KEYBOARD_WIDTH+8*BORDER_THICKNESS, KEYBOARD_HEIGHT+8*BORDER_THICKNESS))
keyboard_rect = pygame.Rect(((SCREEN_WIDTH-KEYBOARD_WIDTH)/2-4*BORDER_THICKNESS, HEADER_HEIGHT+GRID_HEIGHT+2*BUFFER_THICKNESS-4*BORDER_THICKNESS), (KEYBOARD_WIDTH+8*BORDER_THICKNESS, KEYBOARD_HEIGHT+8*BORDER_THICKNESS)) 
#keyboardZone.fill((0,0,0))
#screen.blit(keyboardZone, keyboard_rect)

pygame.display.flip()

play_music()

(target, target_translation) = selectTarget(nbchar)
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



        
