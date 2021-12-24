import os
import winsound

import pygame


def no():
    winsound.PlaySound(os.path.join("sound", 'no_dear.wav'), winsound.SND_FILENAME)


def drink():
    winsound.PlaySound(os.path.join("sound", '1up.wav'), winsound.SND_FILENAME)


def intro(control):
    file = "D:\TheHarderTheyFall\TextAdventure\TextAdventure\sound\ "
    pygame.mixer.init()
    track = pygame.mixer.music.load('audio.mp3')
    if control == 'Play' or control == 'play':
        pygame.mixer.music.play()
    elif control == 'Pause' or control == 'pause':
        pygame.mixer.music.pause()

