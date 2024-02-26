import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Function to determine field goal percentage based on student ID
def determine_percentage(student_id):
    last_two_digits = int(str(student_id)[-2:])
    if 30 <= last_two_digits <= 70:
        return last_two_digits
    elif last_two_digits > 70:
        return last_two_digits - 30
    else:
        return last_two_digits + 30

# Function to define sequence length and streak rules
def define_rules(p_value, third_digit):
    if 60 <= p_value <= 70:
        seq_length = 40
        streak_length = 3 if third_digit % 2 == 0 else 4
    elif 40 <= p_value <= 59:
        seq_length = 50
        streak_length = 2 if third_digit % 2 == 0 else 3
    else:
        seq_length = 60
        streak_length = 2 if third_digit % 2 == 0 else 3
    return seq_length, streak_length

# Function to generate Bernoulli sequences
def generate_sequences(p, length):
    return [1 if random.random() < p / 100 else 0 for _ in range(length)]

# Function to identify streaks and calculate probabilities
def calculate_probabilities(sequence, streak_length):
    probabilities = []
    for i in range(len(sequence) - streak_length):
        if all(sequence[i + j] == 1 for j in range(streak_length)):
            probabilities.append(sequence[i + streak_length])
    return len(probabilities), probabilities.count(1) / len(probabilities) if len(probabilities) > 0 else None

# Main function to simulate the project
def simulate_project(student_id):
    p = determine_percentage(student_id)
    third_digit = int(str(student_id)[-3])
    seq_length, streak_length = define_rules(p, third_digit)
    
    num_samples = 10000
    probabilities = []

    with open("Suhanee_sequence.txt", "w", encoding='utf8') as file:
        for _ in range(num_samples):
            sequence = generate_sequences(p, seq_length)
            file.write(''.join(map(str, sequence)) + '\n')
            streak_count, probability = calculate_probabilities(sequence, streak_length)
        
        # Discard sequences with no observed streaks
            if probability is not None:
                probabilities.append(probability)

    # Convert list of probabilities to NumPy array
    probabilities = np.array(probabilities)

    # Calculate descriptive statistics
    descriptive_stats = {
        'Mean': np.mean(probabilities),
        'Q1': np.percentile(probabilities, 25),
        'Q3': np.percentile(probabilities, 75),
        'Std Deviation': np.std(probabilities)
    }

    # Print descriptive statistics
    print("Descriptive Statistics:")
    print(descriptive_stats)

    # Visualization (optional): Create a histogram or boxplot of probabilities
    # Example using pandas and matplotlib
    df = pd.DataFrame(probabilities, columns=['Probabilities'])
    df.plot(kind='hist', bins=10, title='Distribution of Probabilities')
    # or df.plot(kind='box', title='Boxplot of Probabilities')
    plt.show()
    

# Run the simulation with your student ID
simulate_project()
