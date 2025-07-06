# Maze Runner Game

## 📝 Description
The Maze Runner Game is an interactive web-based game built with Streamlit where players navigate through a randomly generated maze to reach the goal. Features user registration, leaderboards, and real-time gameplay.

### Key Features
- **Random Maze Generation**: Each maze is randomly generated and validated to ensure a valid path exists
- **Interactive Gameplay**: Players can use arrow buttons to navigate the maze
- **User Management**: Register and login to track your progress
- **Leaderboard**: Compete with others and track your best scores
- **Real-Time Stats**: Track moves and time during gameplay
- **Modern UI**: Clean and responsive Streamlit interface

---

## 🚀 Installation

### Prerequisites
- Python 3.10 or later
- Docker and Docker Compose (optional)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/maze-runner-game.git
   cd maze-runner-game
   ```

2. **Option 1: Run with Python**
   ```bash
   # Create virtual environment
   python -m venv myvenv
   
   # Activate virtual environment
   # Windows:
   myvenv\Scripts\activate
   # macOS/Linux:
   source myvenv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run the app
   streamlit run app.py
   ```

3. **Option 2: Run with Docker**
   ```bash
   docker-compose up --build
   ```

4. Access the game in your browser:
   - Python: [http://localhost:8501](http://localhost:8501)
   - Docker: [http://localhost:8501](http://localhost:8501)

---

## 📦 Usage

### Running the Game
1. **With Python:**
   ```bash
   streamlit run app.py
   ```

2. **With Docker:**
   ```bash
   docker-compose up
   ```

3. **Playing the Game:**
   - Enter your username and register/login
   - Click "Generate New Maze" to start
   - Use arrow buttons to navigate
   - Reach the goal (🏁) to win!

### Stopping the Application
- **Python**: Press `Ctrl+C` in the terminal
- **Docker**: Press `Ctrl+C` and run `docker-compose down`

---

## 🎮 Game Controls
- **⬆️ ⬇️ ⬅️ ➡️**: Move player
- **🎲 Generate New Maze**: Create a new random maze
- **🔄 Reset Game**: Reset current game state
- **Maze Size Slider**: Adjust difficulty (5x5 to 15x15)

---

## 🧠 Tech Stack / Built With
- **Language**: Python
- **Framework**: Streamlit
- **Containerization**: Docker, Docker Compose
- **Version Control**: Git

---

## 📂 Project Structure
```
.
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── docker-compose.yml        # Docker compose configuration
├── Dockerfile.game_logic     # Docker configuration
├── README.md                # Project documentation
└── myvenv/                  # Virtual environment
```

---

## 🏆 Features

### Game Features
- **Maze Generation**: Algorithmically generated mazes with guaranteed solutions
- **Player Movement**: Smooth navigation with collision detection
- **Win Condition**: Reach the goal to complete the maze
- **Move Counter**: Track efficiency with move counting
- **Timer**: Race against time for better scores

### User Features
- **User Registration**: Create an account to save progress
- **User Login**: Return to continue your gaming journey
- **Personal Stats**: View your gaming statistics
- **Leaderboard**: Compete with other players globally

### Technical Features
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: Live game state management
- **Session Management**: Persistent user sessions
- **Error Handling**: Robust error handling and user feedback

---

## 🙌 Contributing
Contributions are welcome! To contribute:
1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Commit your changes and push them to your fork
4. Submit a pull request

---

## 📄 License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 👨‍💻 Author
- **Your Name**
- GitHub: [yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

---

## 🌐 Links
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Deployed Application](http://example.com)

---

## 🚀 Deployment

### Deploy to Streamlit Cloud
1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io/)
3. Connect your GitHub repository
4. Deploy with one click!

### Deploy to Heroku
1. Create a `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
2. Deploy using Heroku CLI or GitHub integration

---

## 📚 Algorithm Details

### Maze Generation
The maze generation uses a randomized approach with validation:
1. Generate random 2D array with walls (1) and paths (0)
2. Ensure start (0,0) and goal (n-1,n-1) are paths
3. Validate path exists using Depth-First Search (DFS)
4. Regenerate if no valid path found

### Path Validation
Uses DFS algorithm to ensure solvability:
- Start from position (0,0)
- Explore all possible paths
- Check if goal position (n-1,n-1) is reachable
- Return true if path exists, false otherwise

---

## 🎯 Future Enhancements
- [ ] Multiple difficulty levels
- [ ] Different maze generation algorithms
- [ ] Multiplayer support
- [ ] Power-ups and obstacles
- [ ] Mobile app version
- [ ] Sound effects and animations
- [ ] Tournament mode
- [ ] Social features (friend challenges)

---

## 🐛 Known Issues
- None currently reported

---

## 📞 Support
If you encounter any issues or have questions:
1. Check the existing issues on GitHub
2. Create a new issue with detailed description
3. Contact the maintainers

---

## 🎉 Acknowledgments
- Thanks to the Streamlit team for the amazing framework
- Inspired by classic maze games
- Community feedback and contributions