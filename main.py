import pygame
import random
import os
import sys

from uihelper import *
from firebase_login import *

# Config
WIDTH, HEIGHT = 700, 800
COLORS = {
	"WHITE": (255, 255, 255), "BLACK": (0, 0, 0), "RED": (255, 0, 0),
	"BLUE": (0, 0, 255), "GREEN": (106, 170, 100), "YELLOW": (201, 180, 88), 
	"GRAY": (120, 124, 126), "LIGHT_GRAY": (211, 214, 218), "BG": (251, 252, 255)
}
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
FONT = "sans-serif"
class WordleGame:
	def __init__(self, word_length=5, db_manager=None):
		# Init 
		pygame.init()
		self.word_length = word_length
		self.row = 6
		self.col = word_length
		self.db_manager = db_manager
		
		# Dynamic sizing
		self.tile_size = 80
		self.margin = 15
		self.screen_width = (self.tile_size + self.margin) * self.col + (self.margin * 5)		# dynamic width based on word length
		self.screen_height = (self.tile_size + self.margin) * self.row + 250 # spacing from the top
		
		# Setup screen
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))	# dynamic
		pygame.display.set_caption(f"Wordle by Ming - {self.word_length} Letters")

		# Font 
		self.font = pygame.font.SysFont(FONT, 40)
		self.font_small = pygame.font.SysFont(FONT, 25)
		self.icon = pygame.image.load(os.path.join(BASE_PATH, "asset", "icon.png")) #icon

		# Game State
		self.clock = pygame.time.Clock()
		self.word_list = self.load_words(f"letter{self.word_length}.txt")
		self.reset_game()		# always reset game on init

	def load_words(self, filename):
		path = os.path.join(BASE_PATH, "data", filename)
		if not os.path.exists(path):
			print(f"Warning: {path} not found. Exiting...")
			exit(1)
		with open(path, 'r', encoding='utf-8') as f:
			return [line.strip().lower() for line in f if len(line.strip()) == self.word_length] # add word to list only if correct length

	def reset_game(self):
		self.target_word = random.choice(self.word_list)
		self.valid_words = set(self.word_list) # for lookup
		self.guesses = [] 				# list of tuples (word, [colors])
		self.current_guess = ""
		self.game_over = False
		self.won = False
		print(f"Target: {self.target_word}")

	def check_guess_logic(self, guess):
		color = [COLORS["GRAY"]] * self.word_length
		cnt = {}        # target word char count
		
		for char in self.target_word:
			cnt[char] = cnt.get(char, 0) + 1 
			# cnt.get(char, 0) returns 0 if char not in cnt

		for i, char in enumerate(guess):
			if char == self.target_word[i]:
				color[i] = COLORS["GREEN"]
				cnt[char] -= 1

		for i, char in enumerate(guess):
			if color[i] == COLORS["GRAY"]: # Only check if not green
				if char in cnt and cnt[char] > 0:
					color[i] = COLORS["YELLOW"]
					cnt[char] -= 1

		return color
	
	def handle_input(self, event):
		if self.game_over:
			if event.key == pygame.K_SPACE: 
				self.reset_game()
			return
		if event.key == pygame.K_RETURN:
			if len(self.current_guess) == self.word_length:
				if self.current_guess in self.valid_words:
					color = self.check_guess_logic(self.current_guess)
					self.guesses.append((self.current_guess, color))
					
					if self.current_guess == self.target_word:
						self.game_over = True
						self.won = True
						self.db_manager.save_game(self.target_word, True, len(self.guesses)+1, f"{self.word_length}-char")
					elif len(self.guesses) >= self.row:
						self.game_over = True
						self.db_manager.save_game(self.target_word, False, 6, f"{self.word_length}-char")
					self.current_guess = ""
				else:
					print("Invalid word!") # could add UI shake effect here 
		elif event.key == pygame.K_BACKSPACE:
			self.current_guess = self.current_guess[:-1]
		elif event.unicode.isalpha() and len(self.current_guess) < self.word_length:
			self.current_guess += event.unicode.lower()
			print("inpur:", event.unicode.lower())

	def draw(self):
		self.screen.fill(COLORS['BG'])

		grid_width = self.word_length * (self.tile_size + self.margin) - self.margin	# row*tile_size + (row-1)*margin
		start_x = (self.screen_width - grid_width) // 2
		start_y = 50

		for r in range(self.row):
			for c in range(self.col):
				x = start_x + c * (self.tile_size + self.margin)
				y = start_y + r * (self.tile_size + self.margin)
				rect = pygame.Rect(x, y, self.tile_size, self.tile_size) # square rect
				
				# default val
				color = COLORS["LIGHT_GRAY"]
				letter = ""
				border_color = COLORS["GRAY"]

				# if submitted guess
				if r < len(self.guesses):
					word, color = self.guesses[r]
					letter = word[c]
					color = color[c]
					border_color = color
				
				# if typing
				elif r == len(self.guesses):
					color = COLORS["WHITE"]
					if c < len(self.current_guess):
						letter = self.current_guess[c]
						# color = COLORS["WHITE"]
						border_color = COLORS["BLACK"]
					# else:
					#     color = COLORS["BG"] # Empty slot, almost same color as white

				# draw tile
				rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
				# if color != COLORS["BG"]:
				pygame.draw.rect(self.screen, color, rect)
				pygame.draw.rect(self.screen, border_color, rect, 2)

				# draw Letter
				if letter:
					text = self.font.render(letter.upper(), True, COLORS["WHITE"] if r < len(self.guesses) else COLORS["BLACK"])
					# if not current guess then color white else black
					text_rect = text.get_rect(center=rect.center)
					self.screen.blit(text, text_rect)

		# gameover
		if self.game_over:
			msg = "You Win! Press SPACE to play again." if self.won else f"You Lose! Word was '{self.target_word.upper()}'. Press SPACE to play again."
			text = self.font.render(msg, True, COLORS["GREEN"] if self.won else COLORS["RED"]) # font small
			text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height - 100))
			self.screen.blit(text, text_rect)
		
		pygame.display.flip()
	
	def run(self):
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				elif event.type == pygame.KEYDOWN:
					self.handle_input(event)
			
			self.draw()
			self.clock.tick(60) # 60 FPS
		# pygame.quit()
		# sys.exit()

				

# --- MAIN EXECUTION ---
# if __name__ == "__main__":
# 	game = WordleGame()
# 	game.run() 
class MenuSystem:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 700))
        pygame.display.set_caption("Ming Wordle - Login")
        self.db = FirebaseManager()
        self.state = "LOGIN" # Options: LOGIN, MENU, GAME
        
        # Login Elements
        self.email_input = TextInput(150, 200, 300, 50, "Email")
        self.pass_input = TextInput(150, 270, 300, 50, "Password")
        self.btn_login = Button(150, 350, 140, 50, "Login", self.do_login)
        self.btn_signup = Button(310, 350, 140, 50, "Sign Up", self.do_signup)
        
        # Menu Elements
        self.btn_5 = Button(200, 200, 200, 60, "5 Letters", lambda: self.start_game(5))
        self.btn_6 = Button(200, 280, 200, 60, "6 Letters", lambda: self.start_game(6))
        self.btn_7 = Button(200, 360, 200, 60, "7 Letters", lambda: self.start_game(7))
        self.status_msg = "Please Login"

    def do_login(self):
        email = self.email_input.text
        password = self.pass_input.text
        if self.db.login(email, password):
            self.state = "MENU"
        else:
            self.status_msg = "Login Failed"

    def do_signup(self):
        email = self.email_input.text
        password = self.pass_input.text
        if self.db.signup(email, password):
            self.state = "MENU"
        else:
            self.status_msg = "Signup Failed"

    def start_game(self, length):
        # Launch the game with the selected length
        game = WordleGame(length, self.db)
        game.run()
        # When run() finishes (ESC pressed), we are back here
        self.screen = pygame.display.set_mode((600, 700)) # Reset screen size

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.fill((240, 240, 240))
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                if self.state == "LOGIN":
                    self.email_input.handle_event(event)
                    self.pass_input.handle_event(event)
                    self.btn_login.handle_event(event)
                    self.btn_signup.handle_event(event)
                elif self.state == "MENU":
                    self.btn_5.handle_event(event)
                    self.btn_6.handle_event(event)
                    self.btn_7.handle_event(event)

            # Drawing
            if self.state == "LOGIN":
                self.email_input.draw(self.screen)
                self.pass_input.draw(self.screen)
                self.btn_login.draw(self.screen)
                self.btn_signup.draw(self.screen)
                
                msg = pygame.font.SysFont(FONT, 20).render(self.status_msg, True, (255, 0, 0))
                self.screen.blit(msg, (250, 420))
                
            elif self.state == "MENU":
                title = pygame.font.SysFont(FONT, 40).render(f"Welcome {self.db.email.split('@')[0]}!", True, (0,0,0))
                self.screen.blit(title, (50, 50))
                
                # Show Stats
                stats = self.db.get_stats()
                stat_surf = pygame.font.SysFont(FONT, 20).render(stats, True, (50, 50, 50))
                self.screen.blit(stat_surf, (50, 100))

                self.btn_5.draw(self.screen)
                self.btn_6.draw(self.screen)
                self.btn_7.draw(self.screen)

            pygame.display.flip()
            clock.tick(30)

if __name__ == "__main__":
    app = MenuSystem()
    app.run()