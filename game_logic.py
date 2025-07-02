from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def is_valid_maze(maze):
    rows, cols = len(maze), len(maze[0])
    start, goal = (0, 0), (rows - 1, cols - 1)

    def dfs(x, y, visited):
        if (x, y) == goal:
            return True
        visited.add((x, y))
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0 and (nx, ny) not in visited:
                if dfs(nx, ny, visited):
                    return True
        return False

    return dfs(start[0], start[1], set())

@app.get("/generate-maze")
def generate_maze():
    rows, cols = 10, 10
    while True:
        maze = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]
        maze[0][0] = 0
        maze[rows - 1][cols - 1] = 0
        if is_valid_maze(maze):
            break
    return JSONResponse({"maze": maze})

@app.post("/move")
async def move_player(request: Request):
    data = await request.json()
    position = data.get("position")
    finish_position = [9, 9]
    if position == finish_position:
        return JSONResponse({"status": "Game completed!", "position": position, "finished": True})
    return JSONResponse({"status": "Player moved", "position": position, "finished": False})