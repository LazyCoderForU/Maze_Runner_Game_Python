# Maze Runner Game

## 📝 Description
The Maze Runner Game is an interactive web-based game where players navigate through a randomly generated maze to reach the goal. It is built using a microservices architecture with FastAPI for the backend and a modern web interface for the frontend.

### Key Features
- **Random Maze Generation**: Each maze is randomly generated and validated to ensure a valid path exists.
- **Interactive Gameplay**: Players can use arrow keys or on-screen buttons to navigate the maze.
- **Real-Time Feedback**: Provides feedback for invalid moves and congratulates the player upon reaching the goal.
- **Modern UI**: Clean and responsive design for an enhanced user experience.

---

## 🚀 Installation

### Prerequisites
- Python 3.10 or later
- Docker and Docker Compose

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/maze-runner-game.git
   cd maze-runner-game
   ```
2. Build and start the application:
   ```bash
   docker-compose up --build
   ```
3. Access the game in your browser:
   [http://localhost:5000](http://localhost:5000)

---

## 📦 Usage

### Running the Game
1. Start the application:
   ```bash
   docker-compose up
   ```
2. Navigate to [http://localhost:5000](http://localhost:5000) in your browser.
3. Use arrow keys or on-screen buttons to navigate the maze.
4. Reach the goal (`G`) to complete the game.

### Stopping the Application
Press `Ctrl+C` in the terminal and run:
```bash
docker-compose down
```

---

## 🖼️ Screenshots / Demo
![Maze Runner Game Screenshot](path/to/screenshot.png)

---

## 🧠 Tech Stack / Built With
- **Languages**: Python, JavaScript
- **Frameworks**: FastAPI, python-socketio
- **Frontend**: HTML, CSS
- **Containerization**: Docker, Docker Compose
- **Version Control**: Git

---

## 📂 Project Structure
```
.
├── docker-compose.yml
├── Dockerfile.game_logic
├── Dockerfile.real_time_updates
├── Dockerfile.user_interaction
├── game_logic.py
├── real_time_updates.py
├── user_interaction.py
├── templates/
│   ├── index.html
│   ├── styles.css
│   ├── script.js
├── myvenv/
│   ├── Scripts/
│   ├── Lib/
│   ├── Include/
```

---

## 🙌 Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Submit a pull request.

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
- [Deployed Application](http://example.com)
- [API Documentation](http://example.com/api-docs)

## Teaching Notes: Building the Maze Runner Game from Scratch

### **Objective**
Teach students how to build a web-based interactive game using Python, FastAPI, Docker, and modern web technologies. The project will demonstrate the use of microservices architecture, containerization, and frontend-backend integration.

---

### **Lesson Plan**

#### **1. Introduction to the Project**
- Explain the objective of the Maze Runner Game:
  - A player navigates through a randomly generated maze to reach the goal.
  - The game uses FastAPI for backend logic and HTML/CSS/JavaScript for the frontend.
  - Docker is used for containerization, and the project follows a microservices architecture.

#### **2. Setting Up the Environment**
- **Install Python**: Ensure Python 3.10 or later is installed.
- **Set Up a Virtual Environment**:
  ```bash
  python -m venv myvenv
  source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate
  ```
- **Install FastAPI and Dependencies**:
  ```bash
  pip install fastapi uvicorn[standard] python-socketio[asgi] jinja2
  ```

#### **3. Backend Development**
- **Game Logic Service**:
  - Create `game_logic.py` to handle maze generation, player movement, and game completion logic.
  - Implement random maze generation with validation to ensure a valid path exists.
  - Use FastAPI to expose APIs for maze generation and player movement.

- **User Interaction Service**:
  - Create `user_interaction.py` to manage user registration and login (optional for this project).

- **Real-Time Updates Service**:
  - Create `real_time_updates.py` to enable real-time updates using python-socketio and FastAPI (optional for this project).

#### **4. Frontend Development**
- **HTML Structure**:
  - Create `index.html` to serve as the main game interface.
  - Use a grid layout to represent the maze.

- **CSS Styling**:
  - Add `styles.css` for modern and responsive design.
  - Style the maze, player, and goal cells for better visual appeal.

- **JavaScript Logic**:
  - Add `script.js` to handle player movement and integrate with backend APIs.
  - Use `fetch` to dynamically load the maze and update the game state.

#### **5. Containerization with Docker**
- **Create Dockerfiles**:
  - Write separate Dockerfiles for each microservice (`game-logic`, `user-interaction`, `real-time-updates`).
  - Use Python base images and install necessary dependencies.

- **Set Up Docker Compose**:
  - Write `docker-compose.yml` to orchestrate the services.
  - Map ports for each service to the host machine.

#### **6. Running the Application**
- **Build and Start the Containers**:
  ```bash
  docker-compose up --build
  ```
- **Access the Game**:
  - Open [http://localhost:5000](http://localhost:5000) in a browser to play the game.

#### **7. Testing and Debugging**
- Test the maze generation to ensure a valid path exists.
- Test player movement and game completion logic.
- Debug any issues with containerization or API integration.

#### **8. Deployment (Optional)**
- Deploy the application to a cloud platform (e.g., AWS, Azure, or Google Cloud).
- Use Docker images for easy deployment.

---
