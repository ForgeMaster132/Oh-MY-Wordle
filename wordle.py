import pygame
import sys
import random
from word_lists import list_of_words, list_of_guessable_words_that_cant_be_answers

BLOCK_SIZE = 100
BLOCK_GAP = 5
COLS = 5
ROWS = 6
SCREEN_WIDTH = COLS * (BLOCK_SIZE + BLOCK_GAP) - BLOCK_GAP
SCREEN_HEIGHT = ROWS * (BLOCK_SIZE + BLOCK_GAP) - BLOCK_GAP


pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

pygame.display.set_caption('Oh MY Wordle')

color_correct_spot = pygame.Color('chartreuse4')
color_correct = pygame.Color('yellow')
color = pygame.Color('grey')

def reset_board():
    """Create a fresh game board and return the blocks and starting position."""
    position = 0
    blocks = []
    screen.fill((0, 0, 0))
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(
                col * (BLOCK_SIZE + BLOCK_GAP),
                row * (BLOCK_SIZE + BLOCK_GAP),
                BLOCK_SIZE,
                BLOCK_SIZE,
            )
            pygame.draw.rect(screen, color, rect)
            blocks.append(rect)
    return blocks, position


def determine_block(position, blocks):
    """Return the block at the given position."""
    return blocks[position]


def evaluate_guess(blocks, random_word_array, letters_guessed, row_counter):
    """Color the guess based on accuracy and return (playing, won)."""
    correct_counter = 0
    row_start = row_counter * COLS
    for idx, guess in enumerate(letters_guessed):
        rect = determine_block(row_start + idx, blocks)
        if guess == random_word_array[idx]:
            pygame.draw.rect(screen, color_correct_spot, rect)
            correct_counter += 1
        elif guess in random_word_array:
            pygame.draw.rect(screen, color_correct, rect)
        else:
            pygame.draw.rect(screen, color, rect)
        text = font.render(guess.upper(), True, (0, 0, 0))
        screen.blit(text, rect.center)
    return correct_counter != COLS, correct_counter == COLS

while True:
    player_won = False
    playing = True
    font = pygame.font.SysFont('Arial', 40)
    blocks,position = reset_board()
    row_counter = 0
    random_number = random.randint(0,len(list_of_words)-1)
    random_word = list_of_words[random_number]
    random_word_array = []
    random_word_array = list(random_word)
    letters_guessed = []


    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    guess = "".join(letters_guessed)
                    if guess in list_of_words or guess in list_of_guessable_words_that_cant_be_answers:
                        if position == (row_counter + 1) * COLS:
                            playing, player_won = evaluate_guess(blocks, random_word_array, letters_guessed, row_counter)
                            row_counter += 1
                            letters_guessed = []
                            if row_counter == ROWS:
                                playing = False
                elif event.key == pygame.K_BACKSPACE and letters_guessed:
                    position -= 1
                    row_start = row_counter * COLS
                    if position < row_start:
                        position = row_start
                    pygame.draw.rect(screen, color, determine_block(position, blocks))
                    letters_guessed.pop()
                elif pygame.K_a <= event.key <= pygame.K_z and row_counter < ROWS:
                    row_limit = (row_counter + 1) * COLS
                    if position < row_limit:
                        letter = chr(event.key)
                        text = font.render(letter.upper(), True, (0, 0, 0))
                        screen.blit(text, determine_block(position, blocks).center)
                        letters_guessed.append(letter)
                        position += 1

        pygame.display.update()
    if player_won:
        print("Winner!")
    else:
        print("Loser!")
    
    print(random_word)

    end_game = False

    while not end_game:
        for event in pygame.event.get():
            # if user types QUIT then the screen will close
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    end_game = True
                    break
