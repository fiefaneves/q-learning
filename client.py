import connection as cn
import numpy as np
import random
import os

# Define actions
ACTIONS = ["left", "right", "jump"]

# Q-Learning Parameters
ALPHA = 0.1  # Learning rate
GAMMA = 0.97  # Discount factor
EPSILON_START = 1.0  # Initial epsilon for epsilon-greedy
EPSILON_END = 0.01  # Minimum epsilon
EPSILON_DECAY = 0.95  # Decay rate for epsilon after each
EPISODES = 1000 # Number of training episodes
LOOPS_LIMIT = 10  # Maximum number of loops per episode
EP_TESTS = 20  # Number of tests to evaluate the trained policy

# Total number of states (24 platforms * 4 directions)
NUM_STATES = 24 * 4

# Filename for manipulate Q-table
FILENAME = "resultado.txt"

class QLearningAgent:
    def __init__(self, alpha, gamma, epsilon_start, epsilon_end, epsilon_decay, episodes, actions, loops_limit):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.episodes = episodes
        self.actions = actions
        self.loops_limit = loops_limit
        self.q_table = self.loadQTable()

    # Load the Q-table from a file
    def loadQTable(self):
        if os.path.exists(FILENAME):
            with open(FILENAME, 'r') as file:
                lines = file.readlines()
            loaded_q_table = []
            for line in lines:
                values = list(map(float, line.strip().split()))
                if len(values) == len(ACTIONS):
                    loaded_q_table.append(values)
            
            print(f"Q-table loaded from {FILENAME}.")
            return np.array(loaded_q_table)

    # Save the Q-table to the file
    def saveQTable(self):
        try:
            with open(FILENAME, 'w') as file:
                for row in self.q_table:
                    file.write(" ".join(map(str, row)) + "\n")
            print(f"Q-table saved to {FILENAME}.")
        except Exception as e:
            print(f"Error saving Q-table: {e}")

    # Update the Q-value for the given state-action pair based on the received reward and next state
    def updateQValue(self, state, action, reward, next_state):
        action_index = ACTIONS.index(action)
        best_next_action = np.max(self.q_table[next_state])
        td_target = reward + self.gamma * best_next_action
        td_error = td_target - self.q_table[state][action_index]
        self.q_table[state][action_index] += self.alpha * td_error

    # Choose an random action to explore or the best action to exploit
    def chooseAction(self, state):
        if random.random() < self.epsilon:
            return random.choice(ACTIONS)
        else:
            return ACTIONS[np.argmax(self.q_table[state])]

    # Decay epsilon after each episode to reduce exploration over time
    def epsilonDecayStep(self):
        if self.epsilon > self.epsilon_end:
            self.epsilon *= self.epsilon_decay
            # print(f"Epsilon decayed to {self.epsilon:.4f}")

    # Check if the episode is complete based on the received reward
    def isEpisodeComplete(self, reward):
        if reward == 300:
            print("Episode complete with reward 300. Sucess!")
            return True
        elif reward == -100:
            print("Episode complete with reward -100. Failure!")
            return True
        return False

    # Train the Q-learning agent using the specified socket connection
    # This method runs multiple episodes, updating the Q-table based on the actions taken and rewards received
    def trainAgent(self, socket):
        print("Starting training...")
        sucess_count = 0

        # Run through the specified number of episodes
        for episode in range(self.episodes):
            print(f"Episode {episode + 1}/{self.episodes}")
            state = random.randint(0, NUM_STATES - 1) # Randomly select an initial state
            done = False
            loop_count = 0 # Loop counter to prevent infinite loops

            # Loop until the episode is complete or the loop limit is reached
            while not done:
                # Choose an action based on the current state
                action = self.chooseAction(state) 

                # Get the next state and reward from the environment using the chosen action
                next_state_str, reward_str = cn.get_state_reward(socket, action) 
                next_state = int(next_state_str, 2)
                reward = float(reward_str)

                done = self.isEpisodeComplete(reward) # Check if the episode is complete based on the received reward
                loop_count += 1
                if not done and loop_count >= self.loops_limit: # Check if the loop limit is reached
                    print(f"Loop limit reached ({self.loops_limit}).")
                    done = True # Force end of episode due to loop limit

                # Update the Q-value
                self.updateQValue(state, action, reward, next_state)
                state = next_state

                # Check if the reward indicates success to count successful episodes at the end
                if reward == 300:
                    sucess_count += 1
            
            # Decay epsilon after each episode to reduce exploration and encourage exploitation
            self.epsilonDecayStep()
            print(f"End of episode {episode + 1}. Epsilon: {self.epsilon:.4f}")
        
        print("Training complete. Saving Q-table...")
        self.saveQTable()
        print(f"Total successful episodes: {(sucess_count/self.episodes)* 100:.2f}%")

    # Test the learned policy by running multiple episodes and evaluating the success rate
    def testPolicy(self, socket, ep_tests):
        total_sucess = 0

        # Run through the specified number of test episodes
        for test in range(ep_tests):
            print(f"Test {test + 1}/{ep_tests}")
            state = random.randint(0, NUM_STATES - 1)
            done = False

            while not done:
                # Choose the best action based on the learned Q-table
                action_index = np.argmax(self.q_table[state])
                action = self.actions[action_index]

                # Get the next state and reward from the environment
                next_state_str, reward_str = cn.get_state_reward(socket, action)
                next_state = int(next_state_str, 2)
                reward = float(reward_str)

                # Check if the episode is complete based on the received reward
                done = self.isEpisodeComplete(reward)
                state = next_state

                # Count successful tests based on the received reward
                if reward == 300:
                    total_sucess += 1
        print(f"Testing complete. Total successful tests: {(total_sucess/ep_tests) * 100:.2f}%")

if __name__ == "__main__":
    # Create a socket connection
    socket = cn.connect(2037)

    # Get the current directory and define the result file path
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    result_path = os.path.join(curr_dir, FILENAME)

    # Initialize the Q-learning agent
    agent = QLearningAgent(
        alpha=ALPHA,
        gamma=GAMMA,
        epsilon_start=EPSILON_START,
        epsilon_end=EPSILON_END,
        epsilon_decay=EPSILON_DECAY,
        episodes=EPISODES,
        actions=ACTIONS,
        loops_limit=LOOPS_LIMIT,
    )

    # Train the agent
    # agent.trainAgent(socket)

    # Test the learned policy
    ep_tests = EP_TESTS
    agent.testPolicy(socket, ep_tests)