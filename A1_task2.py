from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
BOX_MIN, BOX_MAX = -250, 250          
background_color = (0.0, 0.0, 0.0)    
points = []                           
speed = 0.01                          
freeze = False
blink = False
see_blink = True
latest_blink = 0                   
BLINK_GAP = 500                


def coordinate(x, y):
    a = x - (WINDOW_WIDTH / 2)
    b = (WINDOW_HEIGHT / 2) - y
    return a, b


def draw_point(x, y, size):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def draw_each_points():
    for p in points:
        x, y, dx, dy, color, visible = p
        if blink and not see_blink:
            glColor3f(*background_color)
        else:
            glColor3f(*color)
        draw_point(x, y, 6)


def spread_point(x, y):
    dx = random.choice([-1.0, 1.0])
    dy = random.choice([-1.0, 1.0])
    color = (random.random(), random.random(), random.random())

    if x < BOX_MIN:
        x = BOX_MIN
    elif x > BOX_MAX:
        x = BOX_MAX
    if y < BOX_MIN:
        y = BOX_MIN
    elif y > BOX_MAX:
        y = BOX_MAX

    points.append([x, y, dx, dy, color, True])


def keyboard_listener(key, x, y):
    global freeze
    if key == b' ':
        freeze = not freeze
    glutPostRedisplay()


def special_key_listener(key, x, y):
    global speed
    if freeze:
        return
    if key == GLUT_KEY_UP:
        speed *= 1.1
        speed = min(speed, 50.0)
    elif key == GLUT_KEY_DOWN:
        speed /= 1.5
        speed = max(speed, 0.001)
    glutPostRedisplay()


def mouse_listener(button, state, x, y):
    global blink
    if freeze:
        return
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        gx, gy = coordinate(x, y)
        spread_point(gx, gy)
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blink = not blink
    glutPostRedisplay()


def setup_projection():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -250, 250, 0, 1)
    glMatrixMode(GL_MODELVIEW)


def display():
    glClearColor(*background_color, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    draw_each_points()
    glutSwapBuffers()


def move_points():
    for p in points:
        p[0] += p[2] * speed
        p[1] += p[3] * speed

        if p[0] > BOX_MAX:
            p[0] = BOX_MAX
            p[2] = -p[2]
        elif p[0] < BOX_MIN:
            p[0] = BOX_MIN
            p[2] = -p[2]
        if p[1] > BOX_MAX:
            p[1] = BOX_MAX
            p[3] = -p[3]
        elif p[1] < BOX_MIN:
            p[1] = BOX_MIN
            p[3] = -p[3]


def update_blink():
    global see_blink, latest_blink
    now = glutGet(GLUT_ELAPSED_TIME)
    if now - latest_blink >= BLINK_GAP:
        see_blink = not see_blink
        latest_blink = now


def animate():
    if not freeze:
        move_points()
        if blink:
            update_blink()
    glutPostRedisplay()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(700, 200)
    glutCreateWindow(b"A1_task2")

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)

    glutMainLoop()


if __name__ == "__main__":
    main()
    
