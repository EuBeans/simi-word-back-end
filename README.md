# My approach to coding a version of Contexto

I'm currently working on coding my own version of Contexto, inspired by the Brazilian game of the same name. While the game mechanics are similar to the original, I'm approaching the development process in my own unique way.

1. **Customized word sets:** Rather than using pre-determined word sets, I'm creating my own custom sets to add a personal touch to the game. This way, I can tailor the game to specific themes or interests.

2. **Flexibility in game play:** While the original game uses a fixed structure for the game play, I'm building in flexibility to allow for different types of games. This way, players can choose the game play that best suits their preferences.

3. **Simplified user interface:** To make the game more accessible to all players, I'm working on a simplified user interface that is easy to navigate and understand.

4. **Scoring system:** In order to add an element of competition to the game, I'm developing a scoring system that will allow players to compare their scores with other players.

Overall, my goal is to create a fun, engaging, and personalized version of Contexto that players will enjoy playing. While I'm drawing inspiration from the original game, I'm excited to put my own unique spin on it.




### **Customized word sets**
Here are a few examples of different types of customized word sets for my version of Contexto:


1. **Themed word sets:** Create word sets that are themed around specific topics or interests, such as sports, animals, or movies.

2. **Regional word sets:** Create word sets that are specific to different regions or countries, using words that are commonly used in those areas.

3. **Educational word sets:** Create word sets that are focused on educational topics, such as science, history, or literature.

4. **Custom user word sets:** Allow users to create their own word sets by inputting their own words, allowing for a more personalized and unique gameplay experience.



### **Flexibility in game play**
Here are a few different types of gameplay you could consider implementing in your version of Contexto:

1. **Timed mode:** In this mode, players are given a set amount of time (e.g. 60 seconds) to guess as many words as they can. Each correct guess earns a point, and the player with the most points at the end of the time limit wins.

2. **Multiplayer mode:** This mode allows two or more players to compete against each other in real-time. Each player takes turns guessing words, and the player with the most correct guesses at the end of the game wins.

3. **Team mode:** In this mode, players are divided into teams and take turns guessing words. Each correct guess earns a point for the team, and the team with the most points at the end of the game wins.

4. **Challenge mode:** In this mode, players are given increasingly difficult words to guess. Each correct guess earns a point, and players must continue to guess words until they reach a set score or until they miss a word. The player with the highest score at the end of the game wins.




## Backend Architecture

- **Framework**: Flask is a popular micro web framework for building RESTful APIs with Python. It provides a simple and flexible routing system for defining API endpoints and is well-suited for small to medium-sized projects.

- **Database**: PostgreSQL is a popular relational database management system that is well-suited for handling large amounts of data. It provides features like concurrency control and data integrity, and has good support for ACID transactions.

- **ORM**: SQLAlchemy is a popular Python library for interacting with relational databases. It provides an ORM (Object-Relational Mapping) system that allows you to interact with your database using Python classes and objects, making it easy to write queries and manipulate data.

- **Authentication and Authorization**: Flask-Login is a popular extension for handling user authentication and authorization in Flask. It provides an easy-to-use system for managing user sessions, and integrates with Flask's built-in authentication system to handle user login and logout.

- **WebSockets**: Flask-SocketIO is a popular extension for handling WebSockets in Flask. It provides a simple and flexible system for implementing real-time communication between clients and servers, which is useful for implementing features like multiplayer and team modes in your game.

- **Caching**: Flask-Caching is a popular extension for caching data in Flask. It provides a simple and flexible system for caching data to improve performance and reduce database load.

## Frontend Architecture

- **Framework**: React is a popular JavaScript library for building user interfaces. It provides a component-based architecture that makes it easy to build complex UIs using small, reusable components.

- **State Management**: Redux is a popular JavaScript library for managing application state. It provides a centralized store for managing state, and provides a simple and consistent way to update and retrieve state.

- **Styling**: CSS modules is a popular system for styling React components. It allows you to define styles locally for each component, which makes it easy to manage styles and avoid naming conflicts.

- **API communication**: Axios is a popular JavaScript library for making HTTP requests from the browser. It provides a simple and consistent API for making requests to your backend API, and allows you to easily handle responses and errors.

Overall, this architecture provides a solid foundation for building a scalable and efficient game. Using Flask with PostgreSQL for the backend and React with Redux for the frontend allows you to build a responsive and dynamic user interface, while providing a reliable and scalable backend for handling game data and user authentication.

### Terminal commands
Note: make sure you have `pip` and `virtualenv` installed.

    Initial installation: make install

    To run test: make tests

    To run application: make run

    To run all commands at once : make all

Make sure to run the initial migration commands to update the database.
    
    > python manage.py db init

    > python manage.py db migrate --message 'initial database migration'

    > python manage.py db upgrade


### Viewing the app ###

    Open the following url on your browser to view swagger documentation
    http://127.0.0.1:5000/


### Using Postman ####

    Authorization header is in the following format:

    Key: Authorization
    Value: "token_generated_during_login"

    For testing authorization, url for getting all user requires an admin token while url for getting a single
    user by public_id requires just a regular authentication.
