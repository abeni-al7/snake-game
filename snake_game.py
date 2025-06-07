import sys
import random
import winsound  # for sound effects on Windows
from OpenGL.GL import glColor3f, glRectf, glBegin, glVertex2f, glEnd, glClear, glClearColor, GL_COLOR_BUFFER_BIT, GL_LINES, glMatrixMode, GL_PROJECTION, GL_MODELVIEW, glLoadIdentity, glRasterPos2f
from OpenGL.GLUT import glutInit, glutInitDisplayMode, GLUT_DOUBLE, GLUT_RGB, glutInitWindowSize, glutInitWindowPosition, glutCreateWindow, glutDisplayFunc, glutKeyboardFunc, glutSpecialFunc, glutTimerFunc, glutMainLoop, glutSwapBuffers, glutSetWindowTitle, glutPostRedisplay, glutBitmapCharacter, GLUT_BITMAP_HELVETICA_18, GLUT_KEY_UP, GLUT_KEY_DOWN, GLUT_KEY_LEFT, GLUT_KEY_RIGHT
from OpenGL.GLU import gluOrtho2D

# Game settings
window_width = 600
window_height = 600
grid_size = 20
cell_size = window_width // grid_size

# Game state variables
snake = []
direction = (1, 0)
apple = None
score = 0
game_over = False
started = False  # game start flag
base_interval = 100  # will be set by difficulty selection
paused = False  # pause flag
game_won = False  # win flag

# high score persistence
highscore_file = "highscore.txt"
highscore = 0


def reset_game():
    global snake, direction, apple, score, game_over
    global game_won
    snake = [(grid_size // 2, grid_size // 2)]
    direction = (1, 0)
    apple = place_apple()
    score = 0
    game_over = False
    game_won = False


def place_apple():
    positions = set((x, y) for x in range(grid_size) for y in range(grid_size)) - set(snake)
    return random.choice(list(positions))


def draw_rect(x, y, color):
    glColor3f(*color)
    glRectf(x * cell_size,
            y * cell_size,
            x * cell_size + cell_size,
            y * cell_size + cell_size)


def draw_grid():
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_LINES)
    for i in range(grid_size + 1):
        # vertical lines
        glVertex2f(i * cell_size, 0)
        glVertex2f(i * cell_size, window_height)
        # horizontal lines
        glVertex2f(0, i * cell_size)
        glVertex2f(window_width, i * cell_size)
    glEnd()


def draw_text(x, y, text, color=(1.0, 1.0, 1.0)):
    glColor3f(*color)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    if not started:
        # show difficulty selection menu (1-9 levels, 0=10)
        draw_text(window_width/2 - 150, window_height/2 + 20, "Select difficulty level:")
        draw_text(window_width/2 - 150, window_height/2,   "Keys 1-9: Levels 1-9 (slow to fast)")
        draw_text(window_width/2 - 150, window_height/2 - 20, "Level 0 (the hardest)")
        # credits
        draw_text(window_width/2 - 100, window_height/2 - 60, "Built by:")
        draw_text(window_width/2 - 100, window_height/2 - 80, "Abenezer Alebachew")
        draw_text(window_width/2 - 100, window_height/2 - 100, "Dejen Achenef")
        draw_text(window_width/2 - 100, window_height/2 - 120, "Hailegebrel Yalember")
        draw_text(window_width/2 - 100, window_height/2 - 140, "Daniot Mihrete")
        draw_text(window_width/2 - 100, window_height/2 - 160, "Eyu Dawit")
        glutSwapBuffers()
        return
    if game_over:
        # show game over message
        draw_text(window_width/2 - 100, window_height/2 + 10, f"Game Over! Score: {score}", color=(5.0,0.2,0.2))
        glutSwapBuffers()
        return
    if game_won:
        # show win message
        draw_text(window_width/2 - 100, window_height/2 + 10, f"You Won! Score: {score}", color=(0.2,1.0,0.2))
        glutSwapBuffers()
        return
    if paused:
        # show paused message
        draw_text(window_width/2 - 100, window_height/2, "Paused - Press P to resume", color=(1.0,1.0,0.0))
        glutSwapBuffers()
        return
    # update window title with current score
    glutSetWindowTitle(f"Snake Game - Score: {score}".encode('ascii'))
    # draw background grid
    draw_grid()
    # draw apple
    draw_rect(apple[0], apple[1], (1.0, 0.0, 0.0))
    # draw snake
    for i, pos in enumerate(snake):
        color = (0.0, 1.0, 0.0) if i > 0 else (0.0, 0.8, 0.0)
        draw_rect(pos[0], pos[1], color)
    # draw score text
    draw_text(5, window_height - 20, f"Score: {score}")
    # draw high score at top-right
    draw_text(window_width - 150, window_height - 20, f"High Score: {highscore}")
    glutSwapBuffers()


def timer(v):
    global game_over, score, apple, direction, paused, highscore
    # pause or end conditions
    if not started or paused or game_over:
        return
    head = snake[0]
    new_head = (head[0] + direction[0], head[1] + direction[1])
    # collision with walls or itself
    if (
        new_head[0] < 0 or new_head[0] >= grid_size or
        new_head[1] < 0 or new_head[1] >= grid_size or
        new_head in snake
    ):
        # vibration sound for game over
        play_gameover_sound()
        # update high score if needed
        if score > highscore:
            highscore = score
            save_highscore()
        game_over = True
        glutPostRedisplay()  # immediately show Game Over screen
        print(f"Game Over! Score: {score}")
        # return to menu after delay
        glutTimerFunc(1500, back_to_menu, 0)
        return
    # move snake
    snake.insert(0, new_head)
    if new_head == apple:
        score += 1
        winsound.Beep(1000, 100)  # beep on eating apple
        apple = place_apple()
        # check win condition: filled entire grid
        max_score = 397
        if score == max_score:
            highscore = score
            save_highscore()
            global game_won
            game_won = True
            glutPostRedisplay()
            # return to menu after short delay
            glutTimerFunc(3000, back_to_menu, 0)
            return
    else:
        snake.pop()
    glutPostRedisplay()
    # dynamic speed: increase difficulty as score rises
    interval = max(50, base_interval - score * 2)
    glutTimerFunc(interval, timer, 0)


def keyboard(key, x, y):
    global direction, started, base_interval, paused
    # toggle pause
    if key in (b'p', b'P') and started and not game_over:
        paused = not paused
        if not paused:
            glutTimerFunc(base_interval, timer, 0)
        glutPostRedisplay()
        return
    # select difficulty (1-9, 0=10)
    if not started and key in tuple(str(i).encode() for i in range(1,10)) + (b'0',):
        ks = key.decode()
        level = 10 if ks == '0' else int(ks)
        # base_interval from 250ms (level1) down to 70ms (level10)
        base_interval = 250 - (level-1)*20
        started = True
        reset_game()
        glutTimerFunc(base_interval, timer, 0)
        return
    if key == b"\x1b":  # ESC
        sys.exit()
    mapping = {
        b'w': (0, 1), b's': (0, -1),
        b'a': (-1, 0), b'd': (1, 0)
    }
    if key in mapping:
        dx, dy = mapping[key]
        if (dx, dy) != (-direction[0], -direction[1]):
            direction = (dx, dy)


def special_input(key, x, y):
    global direction
    mapping = {
        GLUT_KEY_UP: (0, 1),
        GLUT_KEY_DOWN: (0, -1),
        GLUT_KEY_LEFT: (-1, 0),
        GLUT_KEY_RIGHT: (1, 0)
    }
    if key in mapping:
        dx, dy = mapping[key]
        if (dx, dy) != (-direction[0], -direction[1]):
            direction = (dx, dy)


def reshape(w, h):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def back_to_menu(v):
    global started
    reset_game()
    started = False
    glutPostRedisplay()


def load_highscore():
    global highscore
    try:
        with open(highscore_file, 'r') as f:
            highscore = int(f.read())
    except:
        highscore = 0


def save_highscore():
    with open(highscore_file, 'w') as f:
        f.write(str(highscore))


def play_gameover_sound():
    """Play a vibration-like sound pattern on game over."""
    # alternating beeps to simulate vibration
    for freq, duration in [(400, 100), (600, 100)] * 5:
        winsound.Beep(freq, duration)


def main():
    global apple
    load_highscore()
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Snake Game")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    reshape(window_width, window_height)
    reset_game()
    load_highscore()  # load high score at start
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_input)
    # initial timer will start after difficulty selection
    glutMainLoop()


if __name__ == "__main__":
    main()
