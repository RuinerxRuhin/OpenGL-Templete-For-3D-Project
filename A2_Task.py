import random
import time
from OpenGL.GL import *  
from OpenGL.GLUT import *  
from OpenGL.GLU import *  

# --- Global coordinates

catchx=0
score = 0
paused=False
gameover=False
hera_x= random.randint(-220, 220)
hera_y = 180
speed=100
catchspeed=100
cheat=False
lasttime=time.time()
color = (random.uniform(0.3,1),
    random.uniform(0.3,1),
    random.uniform(0.3,1))
# ===== Function to draw a single point =====
def draw_points(x, y):   
    glBegin(GL_POINTS)  
    glVertex2f(x, y)    
    glEnd()                
 
def FindZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy > 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx > 0 and dy < 0:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy > 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx > 0 and dy < 0:
            zone = 6
    return zone

def convert_to_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y
    
def convert_from_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def midpoint_line(x1, y1, x2, y2):
    x1 = int(round(x1))
    y1 = int(round(y1))
    x2 = int(round(x2))
    y2 = int(round(y2))
    area = FindZone(x1, y1, x2, y2)
    x1, y1 = convert_to_zone0(x1, y1, area)
    x2, y2 = convert_to_zone0(x2, y2, area)
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    y = y1
    for x in range(x1, x2 + 1):
        newx,newy=convert_from_zone0(x,y,area)
        draw_points(newx, newy)
        if d>0:
            d+=incNE
            y+=1
        else:
            d+=incE

# ===== Set up 2D coordinate system =====
def setup_projection():
    glViewport(0, 0, 500, 500)  
    glMatrixMode(GL_PROJECTION) 
    glLoadIdentity()   
    glOrtho(-250, 250, -250, 250, 0.0, 1.0)  
    glMatrixMode(GL_MODELVIEW)   

def draw_cross():
    glColor3f(1, 0, 0)
    midpoint_line(195, 195, 240, 240)
    midpoint_line(195, 240, 240, 195)
    
def draw_play():
    glColor3f(1.0, 0.75, 0.0)
    midpoint_line(-10, 198, -10, 238)
    midpoint_line(10, 198, 10, 238)
    
def draw_pause():
    glColor3f(1.0, 0.75, 0.0)
    midpoint_line(-12, 198, -12, 238)
    midpoint_line(-12, 238, 18, 218) 
    midpoint_line(-12, 198, 18, 218) 

def draw_arrow():
    glColor3f(0.0, 0.9, 0.9)
    midpoint_line(-238, 218, -198, 218)
    midpoint_line(-238, 218, -220, 236)
    midpoint_line(-238, 218, -220, 200)
 
def draw_catch(x):
    if gameover:
        glColor3f(1, 0, 0)
    else:
        glColor3f(1, 1, 1)
    midpoint_line(x - 60, -210, x + 60, -210)
    midpoint_line(x-45, -225, x+45, -225)
    midpoint_line(x - 60, -210, x - 45, -225)
    midpoint_line(x + 60, -210, x + 45, -225)

def draw_diamond():
    glColor3f(*color)
    midpoint_line(hera_x,hera_y+15,
                  hera_x + 9,hera_y)
    midpoint_line(hera_x + 9,hera_y,
                  hera_x, hera_y - 15)
    midpoint_line(hera_x, hera_y - 15,
                  hera_x - 9, hera_y)
    midpoint_line(hera_x - 9, hera_y,
                  hera_x, hera_y + 15)
    
def has_collided(box1, box2):
    return (
        box1["x"] < box2["x"] + box2["width"] and
        box1["x"] + box1["width"] > box2["x"] and
        box1["y"] < box2["y"] + box2["height"] and
        box1["y"] + box1["height"] > box2["y"]
    )

def special_key_listener(key, x, y):
    global catchx
    if paused or gameover or cheat:
        return
    if key == GLUT_KEY_LEFT:
        if catchx>-185:
            catchx=catchx-9
    elif key == GLUT_KEY_RIGHT:
        if catchx<185:
            catchx=catchx+9
    glutPostRedisplay()

def animate():
    global hera_y
    global gameover
    global score
    global hera_x
    global speed
    global color
    global cheat
    global catchx
    global lasttime
    currenttime=time.time()
    deltatime=currenttime-lasttime
    lasttime=currenttime
    if deltatime>0.05:
        deltatime=0.05
    if paused or gameover:
        glutPostRedisplay()
        return
    if cheat:
        target=hera_x
        if target < -190:
            target = -190
        elif target > 190:
            target = 190 
        diff =target-catchx
        catchspeedcurrent=max(catchspeed,speed*2)
        move=catchspeedcurrent*deltatime
        if diff > 0:
            catchx =catchx + move
            if catchx > target:
                catchx = target
        if diff < 0:
            catchx =catchx - move
            if catchx < target:
                catchx = target
            
    hera_y -= speed*deltatime
    box1 = {
        "x": hera_x - 9,
        "y": hera_y - 15,
        "width": 18,
        "height": 30
    }
    box2 = {
        "x": catchx - 60,
        "y": -225,
        "width": 120,
        "height": 20
    }
    if has_collided(box1, box2):

        score += 1
        print("Score:", score)

        hera_x = random.randint(-220, 220)
        hera_y = 180

        speed += 10
        color = (
        random.uniform(0.3,1),
        random.uniform(0.3,1),
        random.uniform(0.3,1)
        )
        glutPostRedisplay()
        return
    
    elif hera_y < -265 and not gameover:
        gameover = True
        print("Game Over! Score:", score)
    glutPostRedisplay()
    
    
def keyboard_listener(key, x, y):
    global cheat

    if key==b'c' or key==b'C':
        cheat=not cheat

        if cheat==True:
            print("Cheat ON")
        else:
            print("Cheat OFF")

    glutPostRedisplay()
            
def mouse_listener(button, state, x, y):
    global paused
    global score
    global gameover
    global hera_x
    global hera_y
    global speed
    global color
    global lasttime
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        k = x - 250
        l = 250 - y
         # Cross button
        if 198 <= k <= 238 and 198 <= l <= 238:
            print("Goodbye! Score:", score)
            glutLeaveMainLoop()
            return
        if -20 <= k <= 20 and 195 <= l <= 240:
            paused = not paused 
            lasttime=time.time()      
        if -245<=k <=-190 and 195 <=l<=240:
            score=0
            gameover=False
            paused=False
            hera_x= random.randint(-220, 220)
            color = (
            random.uniform(0.3,1),
            random.uniform(0.3,1),
            random.uniform(0.3,1)
            )
            hera_y=180
            speed=100
            lasttime=time.time()
            print("Starting Over!")
        glutPostRedisplay()
# ===== Display callback =====
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
    glLoadIdentity()      
    setup_projection()   
    glPointSize(2)
    if paused:
        draw_play()
    else:
        draw_pause()
    draw_cross()
    draw_arrow()
    draw_diamond()
    draw_catch(catchx)    
    glutSwapBuffers()        


# ===== Main entry point =====
def main():
    global lasttime
    glutInit()    
    glutInitDisplayMode(GLUT_RGBA)       
    glutInitWindowSize(500, 500)       
    glutInitWindowPosition(550, 250)          
    glutCreateWindow(b"Catch the Diamonds!")   
    lasttime = time.time()
    glutDisplayFunc(display)           
    glutMouseFunc(mouse_listener)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMainLoop()            

# ===== Run the program =====
if __name__ == "__main__":
    main()
