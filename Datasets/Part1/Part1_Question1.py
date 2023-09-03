# Objective: 
# Find average number of points in 2007-2021 seasons for
# All NBA First, Second, and Third teams, as well as players that made
# the All-Star Game

# Try to use Pandas, NumPy, Seaborn, and MatPlotLib

import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
from matplotlib.widgets import CheckButtons

# Load data
players_stats = pd.read_csv("player_stats.csv")
awards_data = pd.read_csv("awards_data.csv")

# Filter data for the specified seasons (2007-2021)
filter_stats = players_stats[(players_stats['season'] >= 2007) & (players_stats['season'] <= 2021)]

# Identify players who made All-Star Game and All NBA teams
all_star_players = awards_data[awards_data['all_star_game'] == 1]['nbapersonid']
all_nba_1st_team_players = awards_data[awards_data['All NBA First Team'] == 1]['nbapersonid']
all_nba_2nd_team_players = awards_data[awards_data['All NBA Second Team'] == 1]['nbapersonid']
all_nba_3rd_team_players = awards_data[awards_data['All NBA Third Team'] == 1]['nbapersonid']

# Filter player stats data to include only the identified players
all_star_stats = filter_stats[filter_stats['nbapersonid'].isin(all_star_players)]
all_nba_1st_team_stats = filter_stats[filter_stats['nbapersonid'].isin(all_nba_1st_team_players)]
all_nba_2nd_team_stats = filter_stats[filter_stats['nbapersonid'].isin(all_nba_2nd_team_players)]
all_nba_3rd_team_stats = filter_stats[filter_stats['nbapersonid'].isin(all_nba_3rd_team_players)]

# Group player stats by 'nbapersonid' and 'season', and calculate the average points
avg_points_all_star = all_star_stats.groupby(['season'])['points'].sum() / all_star_stats.groupby(['season'])['games'].sum()
avg_points_1st_team = all_nba_1st_team_stats.groupby(['season'])['points'].sum() / all_nba_1st_team_stats.groupby(['season'])['games'].sum()
avg_points_2nd_team = all_nba_2nd_team_stats.groupby(['season'])['points'].sum() / all_nba_2nd_team_stats.groupby(['season'])['games'].sum()
avg_points_3rd_team = all_nba_3rd_team_stats.groupby(['season'])['points'].sum() / all_nba_3rd_team_stats.groupby(['season'])['games'].sum()

# Display average points per game for each category in the terminal
# Utilized zip as a way to align the season and average points to output on the same line and
# have the lists/tuples correspond correctly while utilizing the csv files
print("Average Points per Game for All-Star Players:")
for season, avg_points in zip(avg_points_all_star.index, avg_points_all_star):
    print(f"Season {season}: {avg_points:.2f}")

print("\nAverage Points per Game for All NBA First Team Players:")
for season, avg_points in zip(avg_points_1st_team.index, avg_points_1st_team):
    print(f"Season {season}: {avg_points:.2f}")

print("\nAverage Points per Game for All NBA Second Team Players:")
for season, avg_points in zip(avg_points_2nd_team.index, avg_points_2nd_team):
    print(f"Season {season}: {avg_points:.2f}")

print("\nAverage Points per Game for All NBA Third Team Players:")
for season, avg_points in zip(avg_points_3rd_team.index, avg_points_3rd_team):
    print(f"Season {season}: {avg_points:.2f}")

# Calculate the total average for all seasons combined
total_avg_all_star = avg_points_all_star.mean()
total_avg_1st_team = avg_points_1st_team.mean()
total_avg_2nd_team = avg_points_2nd_team.mean()
total_avg_3rd_team = avg_points_3rd_team.mean()

# Display the total average of all seasons combined for each category
print("\nTotal Average Points per Game for 1st Team: {:.2f}".format(total_avg_1st_team))
print("Total Average Points per Game for 2nd Team: {:.2f}".format(total_avg_2nd_team))
print("Total Average Points per Game for 3rd Team: {:.2f}".format(total_avg_3rd_team))
print("Total Average Points per Game for All-Star: {:.2f}".format(total_avg_all_star))

# Create a figure and axis for the plot
plt.figure(figsize=(10, 6))
ax = plt.gca()

# Plot the average points per game for each category with line plots
line_all_star, = plt.plot(avg_points_all_star.index, avg_points_all_star.values, label='All Star')
line_1st_team, = plt.plot(avg_points_1st_team.index, avg_points_1st_team.values, label='1st Team')
line_2nd_team, = plt.plot(avg_points_2nd_team.index, avg_points_2nd_team.values, label='2nd Team')
line_3rd_team, = plt.plot(avg_points_3rd_team.index, avg_points_3rd_team.values, label='3rd Team')

# Customize axis labels and title
ax.set_xlabel('Season')
ax.set_ylabel('Average Points per Game')
ax.set_title('Average Points per Game for All-Star and All NBA Teams (2007-2021)')

# Add a legend
ax.legend(loc='upper left')

# Display the plot
plt.tight_layout()

# Create checkboxes to control visibility of distribution lines
rax = plt.axes([0.85, 0.65, 0.1, 0.15])
labels = ('All Star', '1st Team', '2nd Team', '3rd Team')
visibility = [line_all_star.get_visible(), line_1st_team.get_visible(), line_2nd_team.get_visible(), line_3rd_team.get_visible()]
check_buttons = CheckButtons(rax, labels, visibility)

def func(label):
    if label == 'All Star':
        line_all_star.set_visible(not line_all_star.get_visible())
    elif label == '1st Team':
        line_1st_team.set_visible(not line_1st_team.get_visible())
    elif label == '2nd Team':
        line_2nd_team.set_visible(not line_2nd_team.get_visible())
    elif label == '3rd Team':
        line_3rd_team.set_visible(not line_3rd_team.get_visible())
    plt.draw()  # Redraw the plot to reflect changes

# Connect the CheckButtons to the function
check_buttons.on_clicked(func)

plt.show() # Used to display the GUI/graph