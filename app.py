import streamlit as st
import random
import time
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Maze Runner Game",
    page_icon="🏃‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'maze': None,
        'player_pos': (0, 0),
        'game_over': False,
        'game_won': False,
        'moves': 0,
        'start_time': None,
        'users': {},
        'current_user': None,
        'leaderboard': [],
        'difficulty': 'Medium',
        'theme': 'Default',
        'sound_enabled': True,
        'high_score': float('inf'),
        'total_games': 0,
        'best_time': float('inf')
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

def is_valid_maze(maze):
    """Check if maze has a valid path from start to end using DFS"""
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

def generate_maze(rows=10, cols=10, difficulty='Medium'):
    """Generate a valid maze with different difficulty levels"""
    with st.spinner("🎲 Generating maze..."):
        # Adjust wall density based on difficulty
        wall_probability = {
            'Easy': 0.25,
            'Medium': 0.35,
            'Hard': 0.45,
            'Expert': 0.55
        }
        
        prob = wall_probability.get(difficulty, 0.35)
        max_attempts = 100
        
        for attempt in range(max_attempts):
            maze = [[1 if random.random() < prob else 0 for _ in range(cols)] for _ in range(rows)]
            maze[0][0] = 0  # Start position
            maze[rows - 1][cols - 1] = 0  # End position
            
            # Add some guaranteed paths to prevent impossible mazes
            if attempt > 20:  # After 20 attempts, be more lenient
                for i in range(rows):
                    if random.random() < 0.7:
                        maze[i][min(i, cols-1)] = 0
                
            if is_valid_maze(maze):
                return maze
        
        # Fallback: create a simple maze
        maze = [[0 for _ in range(cols)] for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                if random.random() < 0.2:
                    maze[i][j] = 1
        maze[0][0] = 0
        maze[rows - 1][cols - 1] = 0
        return maze

def get_theme_colors(theme):
    """Get color scheme based on selected theme"""
    themes = {
        'Default': {
            'wall': '#333333',
            'path': '#ffffff',
            'start': '#4CAF50',
            'goal': '#f44336',
            'player': '#2196F3',
            'border': '#333333'
        },
        'Dark': {
            'wall': '#1a1a1a',
            'path': '#2d2d2d',
            'start': '#00ff00',
            'goal': '#ff0000',
            'player': '#00bfff',
            'border': '#555555'
        },
        'Ocean': {
            'wall': '#0f4c75',
            'path': '#3282b8',
            'start': '#00ff7f',
            'goal': '#ff6b6b',
            'player': '#ffe66d',
            'border': '#0f4c75'
        },
        'Forest': {
            'wall': '#2d5016',
            'path': '#8bc34a',
            'start': '#4caf50',
            'goal': '#ff5722',
            'player': '#ffc107',
            'border': '#2d5016'
        }
    }
    return themes.get(theme, themes['Default'])

def display_maze():
    """Display maze with player position using HTML/CSS with theme support"""
    if st.session_state.maze is None:
        return
    
    maze = st.session_state.maze
    player_pos = st.session_state.player_pos
    rows, cols = len(maze), len(maze[0])
    theme_colors = get_theme_colors(st.session_state.theme)
    
    # Create HTML grid with enhanced styling
    html_content = f"""
    <style>
    .maze-container {{
        display: inline-block;
        border: 3px solid {theme_colors['border']};
        background: #f0f0f0;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin: 10px 0;
    }}
    .maze-row {{
        display: flex;
        margin: 0;
        padding: 0;
    }}
    .maze-cell {{
        width: 35px;
        height: 35px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        border: 1px solid #ddd;
        margin: 1px;
        border-radius: 3px;
        transition: all 0.2s ease;
    }}
    .wall {{ background-color: {theme_colors['wall']}; }}
    .path {{ background-color: {theme_colors['path']}; }}
    .start {{ background-color: {theme_colors['start']}; box-shadow: 0 0 10px {theme_colors['start']}; }}
    .goal {{ background-color: {theme_colors['goal']}; box-shadow: 0 0 10px {theme_colors['goal']}; }}
    .player {{ 
        background-color: {theme_colors['player']}; 
        box-shadow: 0 0 15px {theme_colors['player']};
        transform: scale(1.1);
        z-index: 10;
    }}
    .maze-cell:hover {{ transform: scale(1.05); }}
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
    """Move player in specified direction with enhanced feedback"""
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
                
                # Update personal records
                if total_time < st.session_state.best_time:
                    st.session_state.best_time = total_time
                if st.session_state.moves < st.session_state.high_score:
                    st.session_state.high_score = st.session_state.moves
                
                st.session_state.total_games += 1
                
                # Add to leaderboard
                if st.session_state.current_user:
                    st.session_state.leaderboard.append({
                        'user': st.session_state.current_user,
                        'moves': st.session_state.moves,
                        'time': total_time,
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                        'difficulty': st.session_state.difficulty
                    })
                    st.session_state.leaderboard.sort(key=lambda x: (x['moves'], x['time']))
        else:
            st.error("❌ Invalid move! Can't go through walls or out of bounds.")
            time.sleep(0.1)

def reset_game():
    """Reset the game state"""
    st.session_state.maze = None
    st.session_state.player_pos = (0, 0)
    st.session_state.game_over = False
    st.session_state.game_won = False
    st.session_state.moves = 0
    st.session_state.start_time = None

def get_difficulty_size(difficulty):
    """Get maze size based on difficulty"""
    sizes = {
        'Easy': 8,
        'Medium': 12,
        'Hard': 16,
        'Expert': 20
    }
    return sizes.get(difficulty, 10)

def display_game_stats():
    """Display comprehensive game statistics"""
    if st.session_state.maze is not None:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🚶 Moves", st.session_state.moves)
        
        with col2:
            if st.session_state.start_time:
                elapsed = time.time() - st.session_state.start_time
                st.metric("⏰ Time", f"{elapsed:.1f}s")
            else:
                st.metric("⏰ Time", "0.0s")
        
        with col3:
            st.metric("🎯 Difficulty", st.session_state.difficulty)

def display_leaderboard():
    """Display enhanced leaderboard with filtering"""
    st.subheader("🏆 Leaderboard")
    
    if st.session_state.leaderboard:
        # Filter options
        difficulty_filter = st.selectbox(
            "Filter by difficulty:",
            ["All"] + list(set([entry['difficulty'] for entry in st.session_state.leaderboard]))
        )
        
        filtered_board = st.session_state.leaderboard
        if difficulty_filter != "All":
            filtered_board = [entry for entry in st.session_state.leaderboard if entry['difficulty'] == difficulty_filter]
        
        # Display top 10
        for i, entry in enumerate(filtered_board[:10]):
            with st.container():
                # Medal emojis for top 3
                medals = ["🥇", "🥈", "🥉"]
                medal = medals[i] if i < 3 else f"#{i+1}"
                
                st.markdown(f"""
                **{medal} {entry['user']}**  
                🚶 Moves: {entry['moves']} | ⏰ Time: {entry['time']:.1f}s | 🎯 {entry['difficulty']}  
                📅 {entry['date']}
                """)
                st.divider()
    else:
        st.info("🎮 No games completed yet! Be the first to finish a maze!")

def main():
    """Main game application"""
    init_session_state()
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1>🏃‍♂️ Maze Runner Game</h1>
        <p style="font-size: 18px; color: #666;">Navigate through the maze to reach the goal!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for controls
    with st.sidebar:
        st.header("🎮 Game Controls")
        
        # User management
        st.subheader("👤 Player Profile")
        username = st.text_input("Enter your username:", key="username_input")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Register", type="secondary"):
                if username:
                    st.session_state.users[username] = {
                        "games_played": 0, 
                        "best_score": float('inf'),
                        "total_time": 0,
                        "join_date": datetime.now().strftime("%Y-%m-%d")
                    }
                    st.session_state.current_user = username
                    st.success(f"Welcome, {username}! 🎉")
                else:
                    st.error("Please enter a username")
        
        with col2:
            if st.button("🔑 Login", type="secondary"):
                if username in st.session_state.users:
                    st.session_state.current_user = username
                    st.success(f"Welcome back, {username}! 👋")
                else:
                    st.error("User not found. Please register first.")
        
        if st.session_state.current_user:
            st.info(f"🎮 Playing as: **{st.session_state.current_user}**")
        
        st.divider()
        
        # Game settings
        st.subheader("⚙️ Game Settings")
        
        # Difficulty selection
        st.session_state.difficulty = st.selectbox(
            "🎯 Difficulty:",
            ["Easy", "Medium", "Hard", "Expert"],
            index=1
        )
        
        # Theme selection
        st.session_state.theme = st.selectbox(
            "🎨 Theme:",
            ["Default", "Dark", "Ocean", "Forest"],
            index=0
        )
        
        # Custom maze size (override difficulty)
        custom_size = st.slider("📏 Custom Maze Size", 5, 25, get_difficulty_size(st.session_state.difficulty))
        
        # Game controls
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎲 New Maze", type="primary"):
                reset_game()
                st.session_state.maze = generate_maze(custom_size, custom_size, st.session_state.difficulty)
                st.session_state.start_time = time.time()
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset", type="secondary"):
                reset_game()
                st.rerun()
        
        st.divider()
        
        # Movement controls
        st.subheader("🕹️ Movement Controls")
        
        # Arrow button layout
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("⬆️", key="up", help="Move Up"):
                move_player('up')
                st.rerun()
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("⬅️", key="left", help="Move Left"):
                move_player('left')
                st.rerun()
        with col2:
            st.markdown("<div style='text-align: center; font-size: 24px;'>🧍</div>", unsafe_allow_html=True)
        with col3:
            if st.button("➡️", key="right", help="Move Right"):
                move_player('right')
                st.rerun()
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("⬇️", key="down", help="Move Down"):
                move_player('down')
                st.rerun()
        
        st.divider()
        
        # Game stats
        st.subheader("📊 Current Game")
        display_game_stats()
        
        # Personal records
        if st.session_state.total_games > 0:
            st.subheader("🏅 Personal Records")
            st.metric("🎮 Games Played", st.session_state.total_games)
            if st.session_state.high_score != float('inf'):
                st.metric("🏆 Best Score", f"{st.session_state.high_score} moves")
            if st.session_state.best_time != float('inf'):
                st.metric("⚡ Best Time", f"{st.session_state.best_time:.1f}s")
    
    # Main game area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.session_state.maze is None:
            st.markdown("""
            <div style="text-align: center; padding: 50px; background: #f0f0f0; border-radius: 10px; margin: 20px 0;">
                <h3>🎯 Ready to Play?</h3>
                <p>Click <strong>'New Maze'</strong> to generate a maze and start your adventure!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Game status
            if st.session_state.game_won:
                st.success("🎉 Congratulations! You've reached the goal!")
                st.balloons()
                total_time = time.time() - st.session_state.start_time if st.session_state.start_time else 0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🏁 Final Score", f"{st.session_state.moves} moves")
                with col2:
                    st.metric("⏱️ Time Taken", f"{total_time:.1f}s")
                with col3:
                    st.metric("🎯 Difficulty", st.session_state.difficulty)
                
                if st.button("🚀 Play Again", type="primary"):
                    reset_game()
                    st.rerun()
            
            # Display maze
            display_maze()
            
            # Game instructions
            st.markdown("""
            <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 20px 0;">
                <h4>🎮 How to Play:</h4>
                <ul>
                    <li>🚀 <strong>Start:</strong> Green square (top-left)</li>
                    <li>🏁 <strong>Goal:</strong> Red square (bottom-right)</li>
                    <li>🧍 <strong>Player:</strong> Blue square (your position)</li>
                    <li>🧱 <strong>Walls:</strong> Black squares (impassable)</li>
                    <li>⬜ <strong>Path:</strong> White squares (walkable)</li>
                </ul>
                <p><strong>Tip:</strong> Use the arrow buttons to move and try to reach the goal in minimum moves!</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        display_leaderboard()
        
        # Quick stats
        st.subheader("📈 Quick Stats")
        if st.session_state.current_user and st.session_state.current_user in st.session_state.users:
            user_games = [g for g in st.session_state.leaderboard if g['user'] == st.session_state.current_user]
            
            if user_games:
                st.metric("🎮 Your Games", len(user_games))
                best_game = min(user_games, key=lambda x: (x['moves'], x['time']))
                st.metric("🏆 Your Best", f"{best_game['moves']} moves")
                st.metric("⚡ Your Record", f"{best_game['time']:.1f}s")
            else:
                st.info("Complete your first game to see stats!")

if __name__ == "__main__":
    main()
