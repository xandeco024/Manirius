import pygame
import time
from Utilities import *

verminVibes = "Fonts/Vermin Vibes 1989.ttf"
kenneyPixel = "Fonts/Kenney Pixel.ttf"

class UI():
    def __init__(self, player, gameManager, clock, screen):
        self.player = player
        self.clock = clock
        self.screen = screen
        self.gameManager = gameManager

        self.hud = HUD(self)

    def Update(self):
        self.hud.Update()

class HUD():
    def __init__(self, ui):
        self.player = ui.player
        self.gameManager = ui.gameManager
        self.startTimer = 100

    def StartTimer(self):
        self.startTimer = time.Time()

    def DrawTime(self):
        elapsedTime = time.Time() - self.startTimer
        DrawText(str(elapsedTime), kenneyPixel, 30, (255, 255, 255), self.ui.screen, 100, 100)

    def DrawSpeed(self):
        pass

    def Update(self):
        pass