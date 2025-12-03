import pygame
import random
import os
import sys

# --- CONFIGURATION ---
WIDTH, HEIGHT = 600, 700
COLORS = {
    "WHITE": (255, 255, 255), "BLACK": (0, 0, 0), "RED": (255, 0, 0),
    "BLUE": (0, 0, 255), "GREEN": (106, 170, 100), "YELLOW": (201, 180, 88), 
    "GRAY": (120, 124, 126), "LIGHT_GRAY": (211, 214, 218), "BG": (251, 252, 0)
}
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

class WordleGame:
    def __init__(self, word_length=5):
        # Init Pygame
        pygame.init()
        self.word_length = word_length
        self.rows = 6
        
        # Dynamic sizing based on word length
        self.tile_size = 60
        self.margin = 10
        self.screen_width = (self.tile_size + self.margin) * self.word_length + (self.margin * 3)
        self.screen_height = (self.tile_size + self.margin) * self.rows + 150 # Extra space for text
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(f"Wordle by Ming - {self.word_length} Letters")
        
        # Load Assets
        self.font = pygame.font.SysFont("sans-serif", 40)
        self.font_small = pygame.font.SysFont("sans-serif", 25)
        # self.icon = pygame.image.load(...) # Uncomment when you have the file
        
        # Game State
        self.clock = pygame.time.Clock()
        self.word_list = self.load_words(f"letter{self.word_length}.txt")
        self.reset_game()

    def load_words(self, filename):
        # Improved path handling
        path = os.path.join(BASE_PATH, "data", filename)
        if not os.path.exists(path):
            print(f"Warning: {path} not found. Using dummy words.")
            return ["apple", "mango", "berry"] if self.word_length == 5 else ["banana"]
            
        with open(path, 'r', encoding='utf-8') as f:
            return [line.strip().lower() for line in f if len(line.strip()) == self.word_length]

    def reset_game(self):
        self.target_word = random.choice(self.word_list)
        self.valid_words = set(self.word_list) # SET is faster for lookups
        self.guesses = [] # List of tuples: (word, [colors])
        self.current_guess = ""
        self.game_over = False
        self.won = False
        print(f"Target: {self.target_word}")

    def check_guess_logic(self, guess):
        """
        Pure logic: Returns a list of colors for the guess.
        Separating this allows your AI to use this function without graphics.
        """
        color = [COLORS["GRAY"]] * self.word_length
        cnt = {}        # target word char count
        
        # Count frequency of chars in target
        for char in self.target_word:
            cnt[char] = cnt.get(char, 0) + 1

        # 1. Check Greens (Correct position)
        for i, char in enumerate(guess):
            if char == self.target_word[i]:
                color[i] = COLORS["GREEN"]
                cnt[char] -= 1

        # 2. Check Yellows (Wrong position but exists)
        for i, char in enumerate(guess):
            if color[i] == COLORS["GRAY"]: # Only check if not already Green
                if char in cnt and cnt[char] > 0:
                    color[i] = COLORS["YELLOW"]
                    cnt[char] -= 1
                    
        return color

    def handle_input(self, event):
        if self.game_over:
            if event.key == pygame.K_SPACE: # Restart on Space
                self.reset_game()
            return

        if event.key == pygame.K_RETURN:
            if len(self.current_guess) == self.word_length:
                if self.current_guess in self.valid_words:
                    colors = self.check_guess_logic(self.current_guess)
                    self.guesses.append((self.current_guess, colors))
                    
                    if self.current_guess == self.target_word:
                        self.game_over = True
                        self.won = True
                    elif len(self.guesses) >= self.rows:
                        self.game_over = True
                    
                    self.current_guess = ""
                else:
                    print("Invalid word!") # You could add a UI shake effect here later
        
        elif event.key == pygame.K_BACKSPACE:
            self.current_guess = self.current_guess[:-1]
        
        elif event.unicode.isalpha() and len(self.current_guess) < self.word_length:
            self.current_guess += event.unicode.lower()

    def draw(self):
        self.screen.fill(COLORS["BG"])
        
        # Center the grid
        grid_width = self.word_length * (self.tile_size + self.margin) - self.margin
        start_x = (self.screen_width - grid_width) // 2
        start_y = 50

        for row in range(self.rows):
            for col in range(self.word_length):
                x = start_x + col * (self.tile_size + self.margin)
                y = start_y + row * (self.tile_size + self.margin)
                
                # Determine Color and Letter
                color = COLORS["LIGHT_GRAY"]
                letter = ""
                border_color = COLORS["GRAY"]
                
                # If this row is a submitted guess
                if row < len(self.guesses):
                    word, colors = self.guesses[row]
                    letter = word[col]
                    color = colors[col]
                    border_color = color # Border matches fill for colored tiles
                
                # If this row is the current typing row
                elif row == len(self.guesses):
                    color = COLORS["WHITE"]
                    if col < len(self.current_guess):
                        letter = self.current_guess[col]
                        
                        border_color = COLORS["BLACK"] # Active typing border
                    # else:
                    #     color = COLORS["BG"] # Empty slot
                
                # Draw Tile
                rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                # if color != COLORS["BG"]:
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, border_color, rect, 2)

                # Draw Letter
                if letter:
                    text = self.font.render(letter.upper(), True, COLORS["WHITE"] if row < len(self.guesses) else COLORS["BLACK"])
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)

        # Draw Game Over Message
        if self.game_over:
            msg = "You WIN! Press Space" if self.won else f"Lost: {self.target_word.upper()} (Space to Rst)"
            color = COLORS["GREEN"] if self.won else COLORS["RED"]
            text = self.font_small.render(msg, True, color)
            self.screen.blit(text, (self.screen_width//2 - text.get_width()//2, self.screen_height - 50))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    else:
                        self.handle_input(event)
            
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

# --- MAIN EXECUTION ---
# if __name__ == "__main2__":
#     # You can now easily start a 5 letter game, or 6, or 7!
#     # game = WordleGame(word_length=6) 
game = WordleGame(word_length=5)
game.run()