import random
import numpy as np
from collections import deque
import tensorflow as tf
from tensorflow.keras import layers
import setting.Ball_class

# Define the DQN class
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)  # Replay memory
        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_decay = 0.995  # Exploration decay rate
        self.epsilon_min = 0.01  # Minimum exploration rate
        self.learning_rate = 0.001  # Learning rate
        self.model = self.build_model()  # Q-network
        self.target_model = self.build_model()  # Target network
        self.update_target_model()

    def build_model(self):
        model = tf.keras.Sequential()
        model.add(layers.Dense(64, activation='relu', input_shape=self.state_size))
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))
        return model

    def update_target_model(self):
        # Update the target network with the weights from the Q-network
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        # Store the experience in the replay memory
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        # Choose an action based on the epsilon-greedy policy
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])

    def replay(self, batch_size):
        # Update the Q-network using a mini-batch of experiences from the replay memory
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.target_model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        # Load the model weights from a file
        self.model.load_weights(name)

    def save(self, name):
        # Save the model weights to a file
        self.model.save_weights(name)


# Define the game environment
class BilliardGame:
    def __init__(self, ball1_pos, ball2_pos, ball3_pos):
        # Initialize the game environment
        self.ball_sum_pos = [ball1_pos, ball2_pos, ball3_pos]
        

    def get_state(self):
        # Get the current state of the game
        state = np.zeros((len(self.ball_sum_pos), 2))  # Each ball has (x, y) coordinates
        for i, ball in enumerate(self.ball_sum_pos):
            state[i] = [ball.x, ball.y]
        return state

    def get_action_size(self):
        # Get the size of the action space (initial speed(1 ~ 250), theta(0 ~ 36), left or right spin)
        return 25 * 37 * 7

    def take_action(self, action):
        # Take an action in the game environment
        pass

    def get_reward(self):
        # Get the reward for the current state
        pass

    def is_done(self):
        # Check if the game is done
        pass


# Initialize the game environment and DQN agent
env = BilliardGame()
state_size = env.get_state_size()
action_size = env.get_action_size()
agent = DQNAgent(state_size, action_size)
batch_size = 10000


# Training loop
for episode in range(1000):
    state = env.get_state()
    done = False
    while not done:
        # Select an action and take it in the environment
        action = agent.act(state)
        next_state, reward, done = env.take_action(action)

        # Store the experience in the replay memory
        agent.remember(state, action, reward, next_state, done)

        # Transition to the next state
        state = next_state

        if done:
            # Update the target network every few episodes
            if episode % 10 == 0:
                agent.update_target_model()
            break

        # Train the agent by replaying experiences from the replay memory
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)

    # Save the model weights
    if episode % 100 == 0:
        agent.save("model_weights.h5")
