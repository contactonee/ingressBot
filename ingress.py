import cv2
from PIL import ImageGrab
import win32api
import win32gui
import win32con
import time
import math

class node:
    posX = 0
    posY = 0
    edges = []

    def __init__(self, x, y, inToGo):
        self.posX = x
        self.posY = y
        self.edges = inToGo        
nodes = [
node(110, 17, [5, 6, 7, 1, 10]),
node(205, 70, [7, 8, 2]),
node(205, 180, [3, 7, 8]),
node(110, 235, [4, 8, 9, 10]),
node(16, 181, [5, 6, 9]),
node(16, 70, [6, 9]),
node(63, 100, [7, 9, 10]),
node(157, 100, [8, 10]),
node(157, 154, [9, 10]),
node(63, 154, [10]),
node(110, 126, [])]

# Edges
e = [0] * 11
for i in range(11):
    e[i] = [0] * 11

# Power of vertices
pw = [0] * 11
# Start point
st = -1
path = []
hexagon = cv2.imread("hexagon.png")
rd = cv2.imread("ready.png")
# Edge
wh = cv2.imread("edge.png")
wh = cv2.cvtColor(wh, cv2.COLOR_BGR2HSV)
_, wh = cv2.threshold(wh, -1, 255, cv2.THRESH_BINARY)

win32gui.SetForegroundWindow(win32gui.FindWindow(None, "Andy"))
time.sleep(2)

def updateScreen():
    screen = ImageGrab.grab()
    screen.save("screen.png", "png")
    screen = cv2.imread("screen.png")
    main = screen[200:590, 512:853]
    main = cv2.resize(main, (220, 220 * main.shape[0] / main.shape[1]))
    main = cv2.cvtColor(main, cv2.COLOR_BGR2HSV)
    _, main = cv2.threshold(main, 0, 255, cv2.THRESH_BINARY)
    return (screen, main)
def getNumHexs():
    row = screen[53:97, 581:788]
    x, y = row.shape[0:2]
    row = cv2.resize(row, (35 * y / x, 35))
    max_val = 1
    cnt = 0
    while(max_val > 0.6):
        res = cv2.matchTemplate(row, hexagon, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        cv2.rectangle(row, max_loc, (max_loc[0] + 30, max_loc[1] + 35), 0, -1)
        if max_val > 0.6:
            cnt += 1
    return cnt
def getPath(main):
    def midpoint(a, b):
        return (a.posX + b.posX) / 2, (a.posY + b.posY) / 2
    def checkLine(a, b):
        a = nodes[a]
        b = nodes[b]
        x, y = midpoint(a, b)
        temp = node(x, y, [])
        x1, y1 = midpoint(temp, a)
        x2, y2 = midpoint(temp, b)
        x = main[y-2:y+2, x-2:x+2]
        x1 = main[y1-2:y1+2, x1-2:x1+2]
        x2 = main[y2-2:y2+2, x2-2:x2+2]
        res = 0
        res += cv2.minMaxLoc(cv2.matchTemplate(x, wh, cv2.TM_CCORR_NORMED))[1]
        if a == 6 and b == 7:
            if res > 0.8:
                return 1
            else:
                return 0
        res += cv2.minMaxLoc(cv2.matchTemplate(x1, wh, cv2.TM_CCORR_NORMED))[1]
        res += cv2.minMaxLoc(cv2.matchTemplate(x2, wh, cv2.TM_CCORR_NORMED))[1]
        if res > 2.5:
            return 1
        else:
            return 0
    # Edges
    e = [0] * 11
    for i in range(11):
        e[i] = [0] * 11

    # Power of vertices
    pw = [0] * 11
    # Start point
    st = -1
    
    # Find edges and determine powers
    for i in range(0, 11):
        for j in nodes[i].edges:
            if checkLine(i, j):
                e[i][j] = 1
                e[j][i] = 1
                pw[i] += 1
                pw[j] += 1
                print i, j
        if st < 0 and pw[i] > 0:
            st = i
        if pw[i] == 1:
            st = i
    path = []
    qu = [st]
    while len(qu) > 0:
        v = qu[len(qu) - 1]
        if pw[v] > 0:
            for i in range(0, 11):
                if e[v][i] == 1:
                    e[v][i] = 0
                    e[i][v] = 0
                    pw[v] -= 1
                    pw[i] -= 1
                    qu.append(i)
                    break
        else:
            path.append(v)
            qu.pop()
            
    return path
#Press on portal
win32api.SetCursorPos((680,480))
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
time.sleep(2)
#Hold "hack"
# 780 380
win32api.SetCursorPos((780,380))
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
time.sleep(2.5)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
screen, main = updateScreen()
val = cv2.minMaxLoc(cv2.matchTemplate(main, rd, cv2.TM_CCORR_NORMED))[1]
print val
while val < 0.6:
    screen, main = updateScreen()
    val = cv2.minMaxLoc(cv2.matchTemplate(main , rd, cv2.TM_CCORR_NORMED))[1]
    print val

hexs = getNumHexs()
glyph = [0] * hexs
time.sleep(2.4)

gl = [] * 10
for i in range(0, hexs):
    screen, main = updateScreen()
    last = main
    val = cv2.minMaxLoc(cv2.matchTemplate(main, last, cv2.TM_CCORR_NORMED))[1]
    print val
    while val > 0.9:
        last = main
        screen, main = updateScreen()
        val = cv2.minMaxLoc(cv2.matchTemplate(main , last, cv2.TM_CCORR_NORMED))[1]
        print val
    time.sleep(0.5)
    gl[i] = main
    glyph[i] = getPath(main)

print glyph
# win32gui.SetForegroundWindow(win32gui.FindWindow(None, "ingressTestPaint.png - Paint"))
time.sleep(3)
for i in range(0, hexs):
    win32api.SetCursorPos((int(nodes[glyph[i][0]].posX * 1.5 + 512), int(nodes[glyph[i][0]].posY * 1.5+ 200)))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    for j in range(1, len(glyph[i])):
        win32api.SetCursorPos((int(nodes[glyph[i][j]].posX * 1.5 + 512), int(nodes[glyph[i][j]].posY * 1.5 + 200)))
        time.sleep(0.3)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.8)
for i in range(len(gl)):
    cv2.imshow(str(i), gl[i])
cv2.waitKey()
cv2.destroyAllWindows()