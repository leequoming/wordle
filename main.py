import pygame 
import random
import os

# init pygame 
pygame.init()

#
WIDTH, HEIGHT = 600, 700
WHITE, BLACK, RED, BLUE, GREEN, YELLOW, GRAY = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (200, 200, 200)
base_path = os.path.dirname(os.path.abspath(__file__))  # folder of main.py

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle")
icon_path = os.path.join(base_path, "asset", "icon.svg.png")        # add asset folder then icon file path
gameIcon = pygame.image.load(icon_path)
pygame.display.set_icon(gameIcon)

font = pygame.font.SysFont("arial", 40)
font_small = pygame.font.SysFont("arial", 25)

RUNNING = True

def run():
    while RUNNING:
        print("Game running...")


if __name__ == "__main__":
    run()

