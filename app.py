import streamlit as st
import random
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Maze Runner Game",
    page_icon="🏃‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'maze' not in st.session_state:
    st.session_state.maze = None
if 'player_pos' not in st.session_state:
    st.session_state.player_pos = (0, 0)
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'game_won' not in st.session_state:
    st.session_state.game_won = False
if 'moves' not in st.session_state:
    st.session_state.moves = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []

def is_valid_maze(maze):
    """Check if maze has a valid path from start to end"""
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

def generate_maze(rows=10, cols=10):
    """Generate a valid maze"""
    with st.spinner("Generating maze..."):
        while True:
            maze = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]
            maze[0][0] = 0  # Start position
            maze[rows - 1][cols - 1] = 0  # End position
            if is_valid_maze(maze):
                return maze

def display_maze():
    """Display maze with player position using HTML/CSS"""
    if st.session_state.maze is None:
        return
    
    maze = st.session_state.maze
    player_pos = st.session_state.player_pos
    rows, cols = len(maze), len(maze[0])
    
    # Create HTML grid
    html_content = """
    <style>
    .maze-container {
        display: inline-block;
        border: 2px solid #333;
        background: #f0f0f0;
        padding: 10px;
        border-radius: 10px;
    }
    .maze-row {
        display: flex;
        margin: 0;
        padding: 0;
    }
    .maze-cell {
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        border: 1px solid #ddd;
        margin: 1px;
    }
    .wall { background-color: #333; }
    .path { background-color: #fff; }
    .start { background-color: #4CAF50; }
    .goal { background-color: #f44336; }
    .player { background-color: #2196F3; }
    </style>
    <div class="maze-container">
    """
    
    for i in range(rows):
        html_content += '<div class="maze-row">'
        for j in range(cols):
            cell_class = "maze-cell "
            cell_content = ""
            
            if (i, j) == player_pos:
                cell_class += "player"
                cell_content = "🧍"
            elif (i, j) == (rows - 1, cols - 1):
                cell_class += "goal"
                cell_content = "🏁"
            elif (i, j) == (0, 0):
                cell_class += "start"
                cell_content = "🚀"
            elif maze[i][j] == 1:
                cell_class += "wall"
                cell_content = "🧱"
            else:
                cell_class += "path"
                cell_content = "⬜"
            
            html_content += f'<div class="{cell_class}">{cell_content}</div>'
        html_content += '</div>'
    
    html_content += '</div>'
    st.markdown(html_content, unsafe_allow_html=True)

def move_player(direction):
    """Move player in specified direction"""
    if st.session_state.game_over or st.session_state.game_won:
        return
    
    current_pos = st.session_state.player_pos
    maze = st.session_state.maze
    rows, cols = len(maze), len(maze[0])
    
    directions = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }
    
    if direction in directions:
        dx, dy = directions[direction]
        new_x, new_y = current_pos[0] + dx, current_pos[1] + dy
        
        # Check bounds and walls
        if (0 <= new_x < rows and 0 <= new_y < cols and maze[new_x][new_y] == 0):
            st.session_state.player_pos = (new_x, new_y)
            st.session_state.moves += 1
            
            # Check if reached goal
            if (new_x, new_y) == (rows - 1, cols - 1):
                st.session_state.game_won = True
                end_time = time.time()
                total_time = end_time - st.session_state.start_time
                
                # Add to leaderboard
                if st.session_state.current_user:
                    st.session_state.leaderboard.append({
                        'user': st.session_state.current_user,
                        'moves': st.session_state.moves,
                        'time': total_time,
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.session_state.leaderboard.sort(key=lambda x: (x['moves'], x['time']))
        else:
            st.warning("Invalid move! You can't go through walls or out of bounds.")

def reset_game():
    """Reset the game state"""
    st.session_state.maze = None
    st.session_state.player_pos = (0, 0)
    st.session_state.game_over = False
    st.session_state.game_won = False
    st.session_state.moves = 0
    st.session_state.start_time = None

def main():
    st.title("🏃‍♂️ Maze Runner Game")
    st.markdown("Navigate through the maze to reach the goal!")
    
    # Sidebar for user management and game controls
    with st.sidebar:
        st.header("🎮 Game Controls")
        
        # User registration/login
        st.subheader("👤 Player")
        username = st.text_input("Enter your username:", key="username_input")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Register"):
                if username:
                    st.session_state.users[username] = {"games_played": 0, "best_score": float('inf')}
                    st.session_state.current_user = username
                    st.success(f"Welcome, {username}!")
                else:
                    st.error("Please enter a username")
        
        with col2:
            if st.button("Login"):
                if username in st.session_state.users:
                    st.session_state.current_user = username
                    st.success(f"Welcome back, {username}!")
                else:
                    st.error("User not found. Please register first.")
        
        if st.session_state.current_user:
            st.info(f"Current player: {st.session_state.current_user}")
        
        st.divider()
        
        # Game controls
        st.subheader("🎯 Game Setup")
        maze_size = st.slider("Maze Size", 5, 15, 10)
        
        if st.button("🎲 Generate New Maze", type="primary"):
            reset_game()
            st.session_state.maze = generate_maze(maze_size, maze_size)
            st.session_state.start_time = time.time()
            st.rerun()
        
        if st.button("🔄 Reset Game"):
            reset_game()
            st.rerun()
        
        st.divider()
        
        # Movement controls
        st.subheader("🕹️ Movement")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            if st.button("⬆️", key="up"):
                move_player('up')
                st.rerun()
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("⬅️", key="left"):
                move_player('left')
                st.rerun()
        with col2:
            st.write("🧍")
        with col3:
            if st.button("➡️", key="right"):
                move_player('right')
                st.rerun()
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("⬇️", key="down"):
                move_player('down')
                st.rerun()
        
        st.divider()
        
        # Game stats
        st.subheader("📊 Game Stats")
        if st.session_state.maze is not None:
            st.metric("Moves", st.session_state.moves)
            if st.session_state.start_time:
                elapsed = time.time() - st.session_state.start_time
                st.metric("Time", f"{elapsed:.1f}s")
    
    # Main game area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.session_state.maze is None:
            st.info("Click 'Generate New Maze' to start playing!")
        else:
            # Game status
            if st.session_state.game_won:
                st.success("🎉 Congratulations! You've reached the goal!")
                st.balloons()
                total_time = time.time() - st.session_state.start_time if st.session_state.start_time else 0
                st.metric("Final Score", f"{st.session_state.moves} moves in {total_time:.1f}s")
            elif st.session_state.game_over:
                st.error("Game Over! Try again.")
            
            # Display maze
            display_maze()
            
            # Instructions
            st.markdown("""
            **How to play:**
            - 🚀 Start position (green)
            - 🏁 Goal position (red)  
            - 🧍 Your position (blue)
            - 🧱 Walls (black)
            - ⬜ Open path (white)
            
            Use the arrow buttons in the sidebar to move around!
            """)
    
    with col2:
        st.subheader("🏆 Leaderboard")
        if st.session_state.leaderboard:
            for i, entry in enumerate(st.session_state.leaderboard[:10]):
                with st.container():
                    st.write(f"**#{i+1} {entry['user']}**")
                    st.write(f"Moves: {entry['moves']}")
                    st.write(f"Time: {entry['time']:.1f}s")
                    st.write(f"Date: {entry['date']}")
                    st.divider()
        else:
            st.info("No games completed yet!")
        
        st.subheader("📈 Player Stats")
        if st.session_state.current_user and st.session_state.current_user in st.session_state.users:
            user_stats = st.session_state.users[st.session_state.current_user]
            user_games = [g for g in st.session_state.leaderboard if g['user'] == st.session_state.current_user]
            
            st.metric("Games Played", len(user_games))
            if user_games:
                best_game = min(user_games, key=lambda x: (x['moves'], x['time']))
                st.metric("Best Score", f"{best_game['moves']} moves")
                st.metric("Best Time", f"{best_game['time']:.1f}s")

if __name__ == "__main__":
    main()
