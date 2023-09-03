# Objective:
#   - Use the rebounding_data csv file to predict a team's next game
#   offensive rebounding percentage from prior games
#   - Single game = (# of Off_reb) / (# of Off_reb chances)
#   - Multiple games = (total of Off_reb) / (total of Off_reb chances)
#   - Calculate OKC's predicted Off_reb percent in GAME 81

import pandas as pd
# import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
rebounding_data = pd.read_csv('team_rebounding_data_22.csv')

# Filter data for OKC (Oklahoma City Thunder)
okc_data = rebounding_data[rebounding_data['team'] == 'OKC']

# Calculate average offensive rebounding percent
average_oreb_pct = okc_data['offensive_rebounds'].sum() / okc_data['off_rebound_chances'].sum()

# Print the calculated average
print("Average Offensive Rebound Percent for OKC:", '{:.1%}'.format(average_oreb_pct))

# Predict offensive rebound percent for game 81 using the average
predicted_oreb_pct = average_oreb_pct

print("Predicted Offensive Rebound Percent for Game 81:", '{:.1%}'.format(predicted_oreb_pct))

# Visualize the data using Seaborn and Matplotlib
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

# Exclude game 82 from the plot
okc_data_no_game_82 = okc_data[okc_data['game_number'] != 82]
sns.lineplot(x=okc_data_no_game_82['game_number'], y=okc_data_no_game_82['oreb_pct'], label='OKC Offensive Rebound %')

# Add a vertical line for game 81
game_81_x = okc_data[okc_data['game_number'] == 81]['game_number'].values[0]
plt.axvline(x=game_81_x, color='g', linestyle=':', label='Game 81')

plt.title("OKC for 81 Games")
plt.xlabel("Number of Games")
plt.ylabel("Offensive Rebound % per Game")
plt.legend()
plt.show()


# import pandas as pd

# # Load data from CSV files
# player_stats = pd.read_csv('Datasets/player_stats.csv')
# rebounding_data = pd.read_csv('Datasets/team_rebounding_data_22.csv')

# # Calculate total offensive rebounds and offensive rebound chances for games 1-80
# games_1_to_80 = rebounding_data[rebounding_data['team'] == 'OKC'].iloc[:80]
# total_offensive_rebounds = games_1_to_80['offensive_rebounds'].sum()
# total_off_rebound_chances = games_1_to_80['off_rebound_chances'].sum()

# # Calculate the average offensive rebounding percentage for games 1-80
# average_off_rebound_pct = total_offensive_rebounds / total_off_rebound_chances

# # Predict OKC's offensive rebound percentage for game 81
# predicted_off_rebound_pct_game_81 = average_off_rebound_pct

# # Print the predicted offensive rebound percentage for game 81 in percentage format
# print("Predicted Offensive Rebound Percentage for Game 81:", "{:.1%}".format(predicted_off_rebound_pct_game_81))