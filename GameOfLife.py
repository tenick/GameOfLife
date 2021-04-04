from tkinter import *
import threading

# Rules:
# 1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# 2. Any live cell with two or three live neighbours lives on to the next generation.
# 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
# 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.


def draw_grid():
    for x in range(int(1500 / 10)):
        c.create_line(x * 10, 0, x * 10, 1000, fill="green")
    for x in range(int(1000 / 10)):
        c.create_line(0, x * 10, 1500, x * 10, fill="green")


def next_gen():
    global grid, rectangles, grid_copy, rectangles_copy
    grid_copy = [row[:] for row in grid]
    rectangles_copy = [row[:] for row in rectangles]
    for row in range(100):
        for col in range(150):
            check_cell_state(row, col)
    grid = [row[:] for row in grid_copy]
    rectangles = [row[:] for row in rectangles_copy]


def check_cell_state(row, col):
    if grid[row][col]:
        live_cell_next_gen(row, col)
    else:
        dead_cell_next_gen(row, col)


def neighbor_count(row, col):
    neighbors = 0
    try:
        if grid[row-1][col]:  # N
            neighbors += 1
    except Exception:
        pass
    try:
        if grid[row-1][col+1]:  # NE
            neighbors += 1
    except Exception:
        pass
    try:
        if grid[row][col+1]:  # E
            neighbors += 1
    except Exception:
        pass
    try:
        if grid[row+1][col+1]:  # SE
            neighbors += 1
    except Exception:
        pass
    try:
        if grid[row+1][col]:  # S
            neighbors += 1
    except Exception:
        pass
    try:
        if grid[row-1][col-1]:  # SW
            neighbors += 1
    except Exception:
        pass
    try:
        if grid[row][col-1]:  # W
            neighbors += 1
    except Exception:
        pass
    try:
        if grid[row+1][col-1]:  # NW
            neighbors += 1
    except Exception:
        pass
    return neighbors


def live_cell_next_gen(row, col):
    neighbors = neighbor_count(row, col)
    if neighbors < 2:
        draw_cell(row, col)
    #elif 2 <= neighbors <= 3:
    #    grid_copy[row][col] = True  # not really needed but just added it for comprehensibility
    elif neighbors > 3:
        draw_cell(row, col)


def dead_cell_next_gen(row, col):
    neighbors = neighbor_count(row, col)
    if neighbors == 3:
        draw_cell(row, col)


def draw_cell(row, col):
    if not grid[row][col]:
        rectangles_copy[row][col] = c.create_rectangle(col*10, row*10, col*10+10, row*10+10, fill="lightgreen")
        grid_copy[row][col] = True
    else:
        c.delete(rectangles[row][col])
        grid_copy[row][col] = False


def click(event):
    row = event.y//10
    col = event.x//10
    if not grid[row][col]:
        rectangles[row][col] = c.create_rectangle(col*10, row*10, col*10+10, row*10+10, fill="lightgreen")
        grid[row][col] = True
    else:
        c.delete(rectangles[row][col])
        grid[row][col] = False


def auto_generation():
    global start_auto_gen
    if start_auto_gen:
        next_gen()
        auto_generation()
    else:
        start_auto_gen = False


def start_gen_btn():
    global start_auto_gen
    start_auto_gen = True
    start_next_gen_btn.config(state=DISABLED)
    threading.Thread(target=auto_generation).start()


def stop_gen_btn():
    global start_auto_gen
    start_next_gen_btn.config(state=NORMAL)
    start_auto_gen = False


def mouse_wheel(event):
    x = event.delta/120
    if x < 0:
        c.scale(ALL, event.x, event.y, 0.9, 0.9)
    else:
        c.scale(ALL, event.x, event.y, 1.1, 1.1)


grid = [[False for x in range(150)] for y in range(100)]
grid_copy = [[False for x2 in range(150)] for y2 in range(100)]
rectangles = [[0 for a in range(150)] for b in range(100)]
rectangles_copy = [[0 for a2 in range(150)] for b2 in range(100)]

start_auto_gen = False


root = Tk()
root.geometry("1800x1005")
root.configure(bg="black")

c = Canvas(root, width=1500, height=1000, bg="black")  # 150 x 100 canvas
c.bind("<Button-1>", click)
c.bind("<MouseWheel>", mouse_wheel)
draw_grid()
c.place(x=0, y=0)
# r = c.create_rectangle(0, 0, 15, 15, fill="lightgreen")  # 1485, 0, 1500, 15 - upper right most cell
# draw_cell(0, 99)  # row, col

start_next_gen_btn = Button(root, width=10, height=2, text="Start", command=start_gen_btn)
start_next_gen_btn.place(x=1600)
stop_next_gen_btn = Button(root, width=10, height=2, text="Stop", command=stop_gen_btn)
stop_next_gen_btn.place(x=1700)


root.mainloop()