import pygame 
import random

# init pygame 
pygame.init()

#
WIDTH, HEIGHT = 600, 700
WHITE, BLACK, RED, BLUE, GREEN, YELLOW, GRAY = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (200, 200, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle")


font = pygame.font.SysFont("arial", 40)
font_small = pygame.font.SysFont("arial", 25)


# def main():
#     print("Hello from wordle!")


# if __name__ == "__main__":
#     main()

