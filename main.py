import pickle
import time
from pywinauto import Application
import win32gui
import os
import pyautogui
import sys
import math

#StrangeClouds@protonmail.com
# alot of this is untested.
#if not using impact ur gonna have to change the #s
# using win32 instead of pyautogui for alot of it because I was already familiar with win32 when I started but needed autogui for scancodes
# made this in like 20 minutes so dont complain abt quality I know some of it is janky I just didn't wanna commit alot of time
# input your username im too lazy to write something that finds it
user = ''
version = 'your version what else would this be ffs'
# made previous logs so that when u run your program again it can go back to what it was doing
# if this feature will trigger baritone to finish a project instantly and you rely on a baritone ouput then change the sleep time after checking a line in f_trail

#To Do:
#save older vars for program resets and shit

time.sleep(5) # switch to mc after starting
pyautogui.FAILSAFE = True #this makes it so if u move ur cursor to the edge of your screen after an autogui activation the program will stop


class f_trail():
    def __init__(self):
        self.line_dict = {}

    def func_insert(self, mem_and_key):
        for item in mem_and_key:
            self.line_dict[item[0]] = item[1]

    def start(self, logfile="C:/Users/%s/AppData/Roaming/.minecraft/logs/latest.log"%(user)):
        thefile = open(logfile, 'r')
        thefile.seek(0, os.SEEK_END)

        while True:
            line = thefile.readline()
            if not line:
                time.sleep(0.1) # keeping this here cause it saves resources but there are cases where you can miss stuff because of this (if baritone sends something right after u input a cmd)
                continue
            try:
                print(line[11:])
                self.line_dict[line[11:]]()
            except KeyError:
                continue


class mc_interact():
    def __init__(self):
        self.minecraft_handle = Application(backend='win32').connect(title='Minecraft 1.12.2', visible_only=False)
        self.main_window = self.minecraft_handle.top_window()
    def type(self, text):
        pyautogui.press('y')
        time.sleep(.1)
        self.main_window.type_keys(text , with_spaces = True)
        self.main_window.type_keys('{ENTER}')
        time.sleep(.1)

    def callback(self, hwnd, extra):
        if win32gui.GetWindowText(hwnd) == 'Minecraft %s'%(version): #change this if u use a differnt version of mc... nvm ill just put a var at the top for yall
            rect = win32gui.GetWindowRect(hwnd)
            self.dim_dict = {
                'x': rect[0],
                'y': rect[1],
                'w': rect[2] - rect[0],
                'h': rect[3] - rect[1]
            }
        else:
            pass

    def win_dims(self):
        win32gui.EnumWindows(self.callback, None)
        return self.dim_dict

    def inventory(self, slot=1, drop='none', type_='normal', exit=True, enter=False):
        self.win_ratio()
        if enter is True:
            pyautogui.type('e')
        if type_ == 'normal':
            y = 585 * self.ratio_y + (math.floor((slot-1)/9)) * (35 * self.ratio_h)
            x = 815 * self.ratio_x + ((slot-1)%9) * (36 * self.ratio_w)
        elif type_ == 'single_chest':
            y = 585 * self.ratio_y + (math.floor((slot - 1) / 9)) * (35 * self.ratio_h)
            x = 815 * self.ratio_x + ((slot - 1) % 9) * (36 * self.ratio_w)
        elif type_ == 'double_chest':
            y = 640 * self.ratio_y + (math.floor((slot-1) / 9)) * (35 * self.ratio_h)
            x = 815 * self.ratio_x + ((slot - 1) % 9) * (36 * self.ratio_w)
        if exit is True:
            pyautogui.press('esc')

        pyautogui.moveTo(x, y)
        if str(type(drop)) == "<class 'int'>":
            for i in range(drop):
                pyautogui.press('q')
        elif drop == 'all':
            pyautogui.hotkey('ctrl', 'q', interval=.05)
        elif drop == 'transfer':
            pyautogui.keyDown('shift')
            time.sleep(.025)
            pyautogui.mouseDown()
            time.sleep(.025)
            pyautogui.mouseUp()
            time.sleep(.025)
            pyautogui.keyUp('shift')

# Probably works for windows that keep their ratios (i havent bothered to test it); when resized deffo doesnt because the inv ratios arent affected by the games window ratios
# Use BorderlessMinecraft and just click on the window and then refresh to get rid of impacts thing where it keeps the window only one size when not in fullscreen
#if its offscreen just assumes default
    def win_ratio(self):
        if pyautogui.onScreen(mci.win_dims()['x'], mci.win_dims()['y']) is False:
            self.ratio_w = 860
            self.ratio_h = 509
            self.ratio_x = 533
            self.ratio_y = 300
        else:
            self.ratio_w = 860 / mci.win_dims()['w']
            self.ratio_h = 509 / mci.win_dims()['h']
            self.ratio_x = 533 / mci.win_dims()['x']
            self.ratio_y = 300 / mci.win_dims()['y']

#variable is stored as a dictionary in binary format its rlly easy that way
class log_class():
    def __init__(self):
        with open('log.txt', 'rb') as file:
            self.log = pickle.load(file)
        self.edit('log of the log log', self.log) # LOG INCEPTION
        #for when u resume the program so baritone doesnt skip tasks
        #should probably write something so that on startup it temporarily changes sleep time after reading lines from the mc log file but i wont because i dont feel like it
        #so if you have this enabled and stop and let baritone complete its current project after turning off the program your gonna probably have some issues lol
        #sucks to be u
        #also by have this enabled i mean u didnt comment this out and dont worry I probably mention this in the readme


    def edit(self,key, data):
        self.log[key] = data
        with open('log.txt', 'wb') as file:
            pickle.dump(self.log, file)

    def read(self, key):
        try:
            return self.log[key]
        except KeyError as err:
            print(err)
            self.edit(key, '')

    def reset(self): #useful for debugging
        with open('log.txt', 'wb') as file:
            pickle.dump({}, file)

    def i_dont_feel_like_naming_this_rn(self):
        with open('log.txt', 'wb') as file:
            pickle.dump((self.read('log of the log log')).pop('log of the log log'), file) # RIP log inception the logs will rise again one day also

mci = mc_interact()
ft = f_trail()
log = log_class()

'''
This will probably be in the readme but if your like me and never read those then let me explain how to actually add functions and shit
so u can func_insert from function trails then u give it a list of tuples containing the dictionary key (the message in chat it should look for)
and the memory address of the function
the dating is removed from the log btw so dont worry abt it
check example file that should clear things up
also feel free to email me with questions or whatever (StrangePaths@protonmail.com)




'''