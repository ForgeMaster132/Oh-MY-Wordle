import pygame
import sys
import random
from word_lists import list_of_words, list_of_guessable_words_that_cant_be_answers

# visual configuration
BLOCK_SIZE = 80
BLOCK_GAP = 5
COLS = 5
ROWS = 6
SCREEN_WIDTH = COLS * (BLOCK_SIZE + BLOCK_GAP) - BLOCK_GAP
SCREEN_HEIGHT = ROWS * (BLOCK_SIZE + BLOCK_GAP) - BLOCK_GAP

# colours
COLOR_BG = pygame.Color("#121213")
COLOR_BORDER = pygame.Color("#3a3a3c")
COLOR_CORRECT_SPOT = pygame.Color("#6aaa64")
COLOR_CORRECT = pygame.Color("#c9b458")
COLOR_ABSENT = pygame.Color("#3a3a3c")
TEXT_COLOR = pygame.Color("white")

# drawing configuration
BORDER_RADIUS = 8
BORDER_WIDTH = 3


pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Oh MY Wordle")


def display_end_popup(player_won, answer):
    """Show a popup with the result of the game."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(COLOR_BG)
    screen.blit(overlay, (0, 0))

    popup_w, popup_h = 400, 200
    popup_rect = pygame.Rect(
        (SCREEN_WIDTH - popup_w) // 2,
        (SCREEN_HEIGHT - popup_h) // 2,
        popup_w,
        popup_h,
    )
    pygame.draw.rect(
        screen,
        COLOR_BG,
        popup_rect,
        border_radius=BORDER_RADIUS,
    )
    pygame.draw.rect(
        screen,
        COLOR_BORDER,
        popup_rect,
        width=BORDER_WIDTH,
        border_radius=BORDER_RADIUS,
    )

    title_font = pygame.font.SysFont("freesansbold", 60)
    small_font = pygame.font.SysFont("freesansbold", 30)
    title_text = title_font.render(
        "Winner!" if player_won else "Loser!", True, TEXT_COLOR
    )
    title_rect = title_text.get_rect(center=(popup_rect.centerx, popup_rect.top + 60))
    screen.blit(title_text, title_rect)

    word_text = small_font.render(
        f"The word was {answer.upper()}", True, TEXT_COLOR
    )
    word_rect = word_text.get_rect(center=(popup_rect.centerx, popup_rect.top + 110))
    screen.blit(word_text, word_rect)

    prompt_text = small_font.render(
        "Press any key to play again", True, TEXT_COLOR
    )
    prompt_rect = prompt_text.get_rect(
        center=(popup_rect.centerx, popup_rect.bottom - 30)
    )
    screen.blit(prompt_text, prompt_rect)

    pygame.display.update()

def reset_board():
    """Create a fresh game board and return the blocks and starting position."""
    position = 0
    blocks = []
    screen.fill(COLOR_BG)
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(
                col * (BLOCK_SIZE + BLOCK_GAP),
                row * (BLOCK_SIZE + BLOCK_GAP),
                BLOCK_SIZE,
                BLOCK_SIZE,
            )
            pygame.draw.rect(
                screen,
                COLOR_BORDER,
                rect,
                width=BORDER_WIDTH,
                border_radius=BORDER_RADIUS,
            )
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
            fill = COLOR_CORRECT_SPOT
            correct_counter += 1
        elif guess in random_word_array:
            fill = COLOR_CORRECT
        else:
            fill = COLOR_ABSENT
        pygame.draw.rect(
            screen, fill, rect, border_radius=BORDER_RADIUS
        )
        pygame.draw.rect(
            screen, fill, rect, width=BORDER_WIDTH, border_radius=BORDER_RADIUS
        )
        text = font.render(guess.upper(), True, TEXT_COLOR)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
    return correct_counter != COLS, correct_counter == COLS

while True:
    player_won = False
    playing = True
    font = pygame.font.SysFont("freesansbold", 60)
    blocks, position = reset_board()
    row_counter = 0
    random_number = random.randint(0, len(list_of_words) - 1)
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
                    rect = determine_block(position, blocks)
                    pygame.draw.rect(
                        screen, COLOR_BG, rect, border_radius=BORDER_RADIUS
                    )
                    pygame.draw.rect(
                        screen,
                        COLOR_BORDER,
                        rect,
                        width=BORDER_WIDTH,
                        border_radius=BORDER_RADIUS,
                    )
                    letters_guessed.pop()
                elif pygame.K_a <= event.key <= pygame.K_z and row_counter < ROWS:
                    row_limit = (row_counter + 1) * COLS
                    if position < row_limit:
                        letter = chr(event.key)
                        rect = determine_block(position, blocks)
                        text = font.render(letter.upper(), True, TEXT_COLOR)
                        text_rect = text.get_rect(center=rect.center)
                        screen.blit(text, text_rect)
                        letters_guessed.append(letter)
                        position += 1

        pygame.display.update()

    display_end_popup(player_won, random_word)

    end_game = False

    while not end_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                end_game = True
                break
