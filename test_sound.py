import pygame
from time import sleep


pygame.mixer.init()  # Initialize the mixer module.
sound = pygame.mixer.Sound('Audacity/7-scan-QR-Code.wav')  # Load a sound.
sound.set_volume(1)
sound.play()
sleep(1)
# sound.stop()
