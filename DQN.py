import tensorflow as tf
import numpy as np
from collections import deque
import random

# DQN 신경망 모델 구성
class DQN:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)  # Experience Replay를 위한 메모리
        self.gamma = 0.95  # 할인 요인
        self.epsilon = 1.0  # 탐험 및 활용을 결정하는 epsilon 값
        self.epsilon_decay = 0.995  # 탐험 정도를 감소시키는 값
        self.epsilon_min = 0.01  # epsilon의 최소값
        self.learning_rate = 0.001  # 학습률
        self.model = self.build_model()  # DQN 모델 생성
        self.target_model = self.build_model()  # 타깃 네트워크 생성

    def build_model(self):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(tf.keras.layers.Dense(24, activation='relu'))
        model.add(tf.keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = self.target_model.predict(state)
            if done:
                target[0][action] = reward
            else:
                Q_future = max(self.target_model.predict(next_state)[0])
                target[0][action] = reward + self.gamma * Q_future
            self.model.fit(state, target, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())


# DQN 학습
def dqn_train(env, episodes, batch_size):
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = DQN(state_size, action_size)
    for episode in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        done = False
        time = 0
        while not done:
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            time += 1
            if done:
                print(f"Episode: {episode+1}, Time: {time}")
                agent.update_target_model()
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
