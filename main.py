import pygame 
import random
import os
import sys
import bisect 

# init pygame 
pygame.init()

#
WIDTH, HEIGHT = 600, 700
WHITE, BLACK, RED, BLUE, GREEN, YELLOW, GRAY, LIGHT_GRAY, SUPER_L_GRAY = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (200, 200, 200), (240, 240, 240), (251, 252, 255)
TEXT_COLOR = BLACK

base_path = os.path.dirname(os.path.abspath(__file__))  # folder of main.py

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle by Ming")
icon_path = os.path.join(base_path, "asset", "icon.svg.png")        # add asset folder then icon file path
gameIcon = pygame.image.load(icon_path)
pygame.display.set_icon(gameIcon)

font = pygame.font.SysFont("arial", 40)
font_small = pygame.font.SysFont("arial", 25)

# filename = "letter5.txt"
def choose_word(filename = "letter5.txt"):
	file_path = os.path.join(base_path, "data", filename)           # full path to letter5.txt
	words = []
	print(file_path)
	with open(file_path, 'r', encoding='utf-8') as file:
		content = file.read()
		# print(content.splitlines())
		words = [line.strip() for line in content.splitlines() if line.strip()]

	return words

def is_valid_word(targetWord, wordlist):
	try:
		index = bisect.bisect_left(wordlist, targetWord)
		return index < len(wordlist) and wordlist[index] == targetWord
	except Exception as e:
		print(f"Error in is_valid_word: {e}")
		return False	

wordlist = choose_word()
targetWord = random.choice(wordlist)
print(f"Word of the day is: {targetWord}")
RUNNING = True
row, col = 6,5
margin, tile_size = 10, 60      # margin between tiles and size of each tile
gameover = False        # stop the game when true (lose after 6 round or win)
win = False
guesses = []            # list of guessed words
mp = [0]*26
bg_grid = [[LIGHT_GRAY for _ in range(col)] for _ in range(row)]
current = ""
clock = pygame.time.Clock()

for ch in targetWord:
	mp[ord(ch)-ord('a')] += 1

def run():
	global RUNNING, gameover, win, current      # make them modifiable inside the function
	while RUNNING:
		# print("Game running...")
		screen.fill(SUPER_L_GRAY)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:    # press esc to quit
					pygame.quit()
					sys.exit()  
				elif not gameover:
					if event.key == pygame.K_RETURN:
						# print("Enter pressed")
						if len(current) == col:
							if not is_valid_word(current, wordlist):
								print(f"{current} is not a valid targetWord.")
								continue
							print(f"Submitted word: {current}")
							guesses.append(current)                 # add to guessed words
							temp_mp = mp.copy()
							for k,ch in enumerate(current):
								if ch == targetWord[k]:
									bg_grid[len(guesses)-1][k] = GREEN
									temp_mp[ord(ch)-ord('a')] -= 1
							for k,ch in enumerate(current):
								if bg_grid[len(guesses)-1][k] != GREEN and temp_mp[ord(ch)-ord('a')] > 0:
									bg_grid[len(guesses)-1][k] = YELLOW
									temp_mp[ord(ch)-ord('a')] -= 1
								elif bg_grid[len(guesses)-1][k] == LIGHT_GRAY:
									bg_grid[len(guesses)-1][k] = GRAY
							if current == targetWord:
								win = True
								gameover = True
								print("You win!")
							elif len(guesses) == row:
								gameover = True

							current = ""  # reset after submit
					elif event.key == pygame.K_BACKSPACE:
						print("Backspace pressed")
						if len(current) > 0:
							current = current[:-1]      # remove last character
							print(f"Current word: {current}")
					elif event.unicode.isalpha() and len(event.unicode) == 1 and len(current) < col:
						print(f"Key pressed: {event.unicode}")
						current += event.unicode.lower()
		# # Draw board 
		for r in range(row):
			for c in range(col):
				x = c*(tile_size + margin) + (WIDTH - col*tile_size - (col-1)*margin)//2      # center the board by plus side margin to 0, tile + margin, 2*(tile + margin), 3*(tile + margin), ...
				y = r*(tile_size + margin) + 50     # +50 to spacing from top

				letter = ""
				LETTER_BG = bg_grid[r][c]            # background color of letter
				LETTER_BG_BORDER = LETTER_BG if LETTER_BG != LIGHT_GRAY else GRAY
				if r < len(guesses):
					letter = guesses[r][c]
				elif r == len(guesses) and c < len(current):
					letter = current[c]

					
				rect = pygame.Rect(x, y, tile_size, tile_size)
				pygame.draw.rect(screen, LETTER_BG, rect)
				pygame.draw.rect(screen, LETTER_BG_BORDER, rect, 2)   # border

				if letter:
					text_surface = font.render(letter.upper(), True, TEXT_COLOR)
					text_rect = text_surface.get_rect(center=rect.center)				# rect defined above of the tile
					screen.blit(text_surface, text_rect)
		if gameover:
			msg = "You Win!" if win else f"You lose! The word was {targetWord.upper()}"
			# print(msg)
			msg_surface = font.render(msg, True, BLACK)
			msg_rect = msg_surface.get_rect(center=(WIDTH//2, HEIGHT - 100))	# choose coord for center of msg_surface
			screen.blit(msg_surface, msg_rect)
				

		pygame.display.flip()
		clock.tick(60) 


if __name__ == "__main__":
	try:
		run()
	except Exception as e:
		print(f"Error: {e}")
		pygame.quit()
		sys.exit()