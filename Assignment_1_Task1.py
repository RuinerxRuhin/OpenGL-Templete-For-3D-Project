#Assignment_1_Task_1

from OpenGL.GL import * 
from OpenGL.GLUT import *  
from OpenGL.GLU import *  
import random
# --- Global coordinates of the point ---

WINDOW_WIDTH, WINDOW_HEIGHT = 1800, 1800
LEFT, RIGHT, BOTTOM, TOP = -300, 1800, -300, 500
L,R,B,T=620,1000,200,450
WO = 690 #Window Left
WO1 = 760
WO2 = 320
WO3 = 380
WR = 880 #Window Right
WR1 = 950
WR2 = 320
WR3 = 380
DL = 775 #Dorja
DR = 865
DB = 200
DT = 330
RL = 520 #Roof
RR = 1080
RA = 800
RY = 760
RAIN = 100
rain = []
Day= 0.0
   
# ===== Function to draw a single point =====
def draw_shapes():
    glBegin(GL_TRIANGLES)
    glColor3f(0.39, 0.27, 0.18)
    glVertex2d(LEFT,BOTTOM)
    glVertex2d(RIGHT,BOTTOM)
    glVertex2d(RIGHT,TOP)
    glVertex2d(LEFT,BOTTOM)
    glVertex2d(RIGHT,TOP)
    glVertex2d(LEFT,TOP)
    glEnd()

def draw_home():
    glBegin(GL_TRIANGLES)        
    glColor3f(0.85, 0.78, 0.69)

    glVertex2d(L,B)
    glVertex2d(R,B)
    glVertex2d(R,T)

    glVertex2d(L,B)
    glVertex2d(R,T)
    glVertex2d(L,T)
    glEnd()
    
def draw_grass():
    glBegin(GL_TRIANGLES)  
    glColor3f(0.35, 0.85, 0.35)   # Grass green
    
    for x in range(0, 1800, 50):
        glColor3f(0.20, 0.65, 0.20)
        glVertex2f(x, 400)

        glColor3f(0.15, 0.15, 0.15)
        glVertex2f(x + 25, 470)

        glColor3f(0.20, 0.65, 0.20)
        glVertex2f(x + 50, 400)
  
    glEnd()
 
def draw_ayna():
    glBegin(GL_TRIANGLES)

    glColor3f(0.35, 0.70, 1.00) 

# ---------- Left Window ----------
    glVertex2d(WO, WO2)
    glVertex2d(WO1, WO2)
    glVertex2d(WO1, WO3)

    glVertex2d(WO, WO2)
    glVertex2d(WO1, WO3)
    glVertex2d(WO, WO3)

# ---------- Right Window ----------
    glVertex2d(WR, WR2)
    glVertex2d(WR1, WR2)
    glVertex2d(WR1, WR3)

    glVertex2d(WR, WR2)
    glVertex2d(WR1, WR3)
    glVertex2d(WR, WR3)
    
    glColor3f(0.50, 0.20, 0.70)

    glVertex2d(RL, T)
    glVertex2d(RR, T)
    glVertex2d(RA, RY) 

    glEnd()    
    
def draw_jalna():
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2d((WO + WO1) / 2, WO2)
    glVertex2d((WO + WO1) / 2, WO3)
    glVertex2d(WO, (WO2 + WO3) / 2)
    glVertex2d(WO1, (WO2 + WO3) / 2)
    
    #Right
    
    glVertex2d((WR + WR1) / 2, WR2)
    glVertex2d((WR + WR1) / 2, WR3)
    glVertex2d(WR, (WR2 + WR3) / 2)
    glVertex2d(WR1, (WR2 + WR3) / 2)
    glEnd()
 
def draw_dorja():
    glBegin(GL_TRIANGLES)
    glColor3f(0.75, 0.10, 0.10) 
    glVertex2d(DL, DB)
    glVertex2d(DR, DB)
    glVertex2d(DR, DT)
    glVertex2d(DL, DB)
    glVertex2d(DR, DT)
    glVertex2d(DL, DT)
    
    glEnd()    
    
def draw_axes():
    glLineWidth(1)
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 0.0)

    glVertex2d(L,B)
    glVertex2d(R,B)

    glVertex2d(R,B)
    glVertex2d(R,T)

    glVertex2d(L,T)
    glVertex2d(R,T)

    glVertex2d(L,B)
    glVertex2d(L,T)

    glEnd()
    
def draw_border():
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2d(DR, DB)
    glVertex2d(DR, DT)
    glVertex2d(DL, DT)
    glVertex2d(DR, DT)
    glVertex2d(DL, DB)
    glVertex2d(DL, DT)
    glEnd()    
    
def draw_button():
    glPointSize(6)
    glBegin(GL_POINTS)
    glColor3f(0, 0, 0.0) 
    glVertex2d(850, 260)
    glEnd()

 
for i in range(RAIN):
    rain.append([
    random.randint(-350, 1800), 
    random.randint(250, 1800) 
    ])
    
rain_direction = 0     
def draw_rain():
    glColor3f(0.30, 0.55, 0.85)
    glLineWidth(4)
    glBegin(GL_LINES)
    
    for x, y in rain:
        glVertex2d(x, y)
        glVertex2d(x + rain_direction * 7 , y - 40)  
    glEnd()   

def animate():
    for drop in rain:
        drop[1] -= 10
        drop[0] += rain_direction * 0.3
        if drop[1]<-300:
            drop[1] = 1800
            drop[0] = random.randint(-350, 1800)
    glutPostRedisplay()
    
def special_key_listener(key, x, y):
    global rain_direction
    if key == GLUT_KEY_LEFT:
        rain_direction = max(rain_direction - 1, -6)

    elif key == GLUT_KEY_RIGHT: 
            rain_direction =min(rain_direction + 1, 7)
    glutPostRedisplay()
    
def keyboard_listener(key, x, y):
    global Day
    if key == b'd':                #DAY
        Day = min(1.0, Day + 0.25)

    elif  key == b'n':                #Night
        Day = max(0,Day-0.25)
    glutPostRedisplay()    
    
        
def setup_projection():
    glViewport(0,0, WINDOW_WIDTH, WINDOW_HEIGHT) 
    glMatrixMode(GL_PROJECTION) 
    glLoadIdentity() 
    glOrtho(0.0, 1800, 0.0, 1800, -1, 1.0) 
    glMatrixMode(GL_MODELVIEW) 

def display():
    glClearColor(Day,Day,Day,1) 
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
    glLoadIdentity()    
    setup_projection()
    draw_axes() 
    draw_shapes()
    draw_grass()
    draw_home()   
    draw_ayna() 
    draw_jalna()
    draw_dorja()
    draw_border()
    draw_button() 
    draw_rain()                     
    glutSwapBuffers()   

def main():
    glutInit()                 
    glutInitDisplayMode(GLUT_RGBA)  
    glutInitWindowSize(1400, 900)  
    glutInitWindowPosition(90, 180) 
    glutCreateWindow(b"Assignment 1: Task 1")  
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener) #Din/Raat Change
    glutSpecialFunc(special_key_listener) #Bristi Change
    glutMainLoop() 

if __name__ == "__main__":
    main()
