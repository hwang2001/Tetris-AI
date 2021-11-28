import random
import pygame
import sys
import threading
import datetime as datetime
from TetrisSettings import *
import TetrisUtils as TUtils


class Tetrisv2:
    def __init__(self):
        # Scores
        self.score = 0.0
        self.lines = 0
        self.high_score = 0.0
        self.high_score_lines = 0
        self.fitness = 0.0

        # Initialize display stuff
        if HAS_DISPLAY:
            self.log("Initializing system...", 3)
            pygame.init()
            pygame.font.init()

            self.screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
            self.log("Screen size set to: (" + str(SCREEN_WIDTH) + ", " + str(SCREEN_HEIGHT) + ")", 2)
            self.obs_size = GRID_ROW_COUNT * GRID_COL_COUNT  # would be + 1 if you are using the next block

            # PyGame configurations
            # blocks mouse motion events
            pygame.event.set_blocked(pygame.MOUSEMOTION)

            # Initialize game-related attributes
            self.init_game()

            # Setup callback functions
            self.on_score_changed_callbacks = []

            # Start the game
            self.start()


    def init_game(self):
        self.log("Initializing game...", 2)

        #models whether game is active and pieeces are dropping, etc
        self.active = True
        #moddls whether game is paused
        self.paused = False

        # Board is an 2D array of integers
        #self.board =
        self.reset_board()

        # Calculate grid size
        self.grid_size = int(SCREEN_HEIGHT / GRID_ROW_COUNT)
        self.log("Tetris grid size calculated to: " + str(self.grid_size), 2)

        # Keyboard integration
        # http://thepythongamebook.com/en:glossary:p:pygame:keycodes

        #need to add "Z" rotate
        self.key_actions = {
            "ESCAPE": self.toggle_pause,
            "LEFT": lambda: self.move_tile(-1),
            "RIGHT": lambda: self.move_tile(1),
            "DOWN": lambda: self.drop(False),
            "SPACE": lambda: self.drop(True),
            "UP": self.rotate_tile,
            "TAB": self.swap_tile
        }

        # Tile generation
        self.generate_tile_bank()
        self.spawn_tile()

        # Score
        self.score = 0
        self.lines = 0
        self.fitness = 0.0


    def start(self):
        pass;

    def update(self):
        pass;

    def draw(self):
        pass;
    
    def draw_tiles(self, matrix, offsets=(0,0), outline_only=False):
        pass;
    
    def draw_next_tile(self, offsets):
        pass;

    def spawn_tile(self):
        self.tile = self.get_next_tile(pop=True)
        self.tile_shape = TILE_SHAPES.get(self.tile)[:]
        self.tile_x = int(GRID_COL_COUNT / 2 - len(self.tile_shape[0]) / 2)
        self.tile_y = 0

    def get_next_tile(self, pop=False):
        if not self.tile_bank:
            self.generate_tile_bank()
        
        if not pop:
            return self.tile_bank[0]
        else:
            return self.tile_bank.pop(0)

    def drop(self, instant=False):
        if not self.active or self.paused:
            return

        if instant:
            destination = TUtils.get_effective_height(self.board, self.tile_shape, (self.tile_x), (self.tile_y))
            self.score += PER_STEP_SCORE_GAIN * (destination - self.tile_y)
            self.tile_y = destination + 1
        else:
            self.tile_y += 1
            self.score += PER_STEP_SCORE_GAIN

        #if no collision happens when you drop it without the instant, function is done!
        if not TUtils.check_collision(self.board, self.tile_shape, (self.tile_x, self.tile_y)) and not instant:
            return

        #but if there is collision, then you gotta add piece to the board and spawn new one
        self.add_tile_to_board()
        self.calculate_scores()
        self.spawn_tile()



    

    #move tile based on delta, either -1 or +1
    def move_tile(self, delta):
        if not self.active or self.paused:
            return
        
        new_x = self.tile_x + delta
        #clamping, make sure new_x isn't off the grid)
        # if ((new_x + len(self.tile_shape[0])) > GRID_COL_COUNT) or ((new_x < 0)):
        #     new_x = self.tile_x
        new_x = max(0, min(new_x, GRID_COL_COUNT - len(self.tile_shape[0])))

        #make sure new position isn't colliding with any current blocks
        if TUtils.check_collision(self.board, self.tile_shape, (new_x, self.tile_y)):
            return

        self.tile_x = new_x


    def rotate_tile(self, pseudo=False):
        if not self.active or self.paused:
            return False, self.tile_x, self.tile_shape
        new_shape = TUtils.get_rotated_tile(self.tile_shape)
        temp_x = self.tile_x
        
        #if rotating piece makes it out of bounds
        if (self.tile_x + len(new_shape[0]) > GRID_COL_COUNT):
            temp_x = GRID_COL_COUNT - len(new_shape[0])
        
        if TUtils.check_collision(self.board, new_shape, (temp_x, self.tile_y)):
            return False, self.tile_x, self.tile_shape
        
        if not pseudo:
            self.tile_x = temp_x;
            self.tile_shape = new_shape;
            
        return True, temp_x, new_shape
            
    
    def swap_tile(self, pseudo=False):
        pass;

    def calculate_scores(self):
        score_count = 0
        row = 0
        while 0 == 0:
            if row >= len(self.board):
                break
            if 0 in self.board[row]:
                row += 1
                continue
            #delete filled row
            del self.board[row]
            #insert empty row at tpo to maintain board size
            self.board.insert(0, [0] * GRID_COL_COUNT)
            score_count += 1
            
            
        # Calculate fitness score
        # self.fitness = TUtils.get_fitness_score(self.board)
        # If cleared nothing, early return
        if score_count == 0:
            return
        # Calculate total score based on algorithm
        total_score = MULTI_SCORE_ALGORITHM(score_count)
        
        # Callback not sure of this
        for callback in self.on_score_changed_callbacks:
            callback(self.score, self.score + total_score)

        self.score += total_score
        self.lines += score_count
        self.log("Cleared " + str(score_count) + " rows with score " + str(total_score), 3)
        
        # Calculate game speed
        pygame.time.set_timer(pygame.USEREVENT + 1, SPEED_DEFAULT if not SPEED_SCALE_ENABLED else int(
            max(50, SPEED_DEFAULT - self.score * SPEED_SCALE)))

    def add_tile_to_board(self):
        for cy, row in enumerate(self.tile_shape):
            for cx, val in enumerate(row):
                if val == 0:
                    continue
                self.board[cy + self.tile_y - 1][min(cx + self.tile_x, 9)] = val
    
    def reset(self):
        self.log("Resetting game...", 2)
        #Calcualte high score
        if self.score > self.high_score:
            self.high_score = self.score
        if self.lines > self.high_score_lines:
            self.high_score_lines = self.lines

        #Reset
        self.init_game()
        return self.board[:]

    def reset_board(self):
        # self.board = [None] * GRID_ROW_COUNT
        # for i in range(GRID_ROW_COUNT):
        #     self.board[i] = GRID_COL_COUNT * [0]

        self.board = [[0] * GRID_COL_COUNT for _ in range(GRID_ROW_COUNT)]

    def toggle_pause(self):
        if not self.active:
            self.reset()
            self.paused = False
            return
        self.paused = not self.paused
        self.log(("Pausing" if self.paused else "Resuming") + " game...", 2)

    def quit(self):
        sys.exit();

    def generate_tile_bank(self):
        self.tile_bank = list(TILE_SHAPES.keys())
        random.shuffle(self.tile_bank)

    def print_board(self, flattened=False):
        pass;

    def log(self, message, level):
        if MIN_DEBUG_LEVEL > level:
            return

        #current_time becomes string that cuts off the last 4 digits of the %f
        current_time = datetime.now().strftime("%H:%M:%S:%f")[:-4]
        print(f"[{level}] {current_time} >> {message}")

    
if __name__ == "__main__":
    print("Hello world!")
    # User testing (AKA play game)
    HAS_DISPLAY = True
    STEP_ACTION = False
    Tetrisv2()
    print("Goodbye world!")

   