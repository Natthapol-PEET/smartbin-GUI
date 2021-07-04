import pygame
from threading import Thread

pygame.mixer.init()
stop_threads = False

def play_sound(file):
    p = Thread(target=start_sound, args=(file,))
    p.start()
    

def start_sound(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy() == True:
        continue



def play_video_create(file):
    global stop_threads 
    stop_threads  = False
    video_create = Thread(target=start_video, args=(file, lambda : stop_threads,))
    video_create.start()

def start_video(file, stop):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy() == True:
        print(stop())
        if stop():
            break
    
def stop_video_create():
    global stop_threads 
    stop_threads  = True