# Objective:
# Data Cleaning Interlude
# Find the Career Outcomes for each player by the following
#   1. Elite (Won any All NBA 1st, 2nd, 3rd, MVP, or DPOY)
#   2. All-Star (Selected as All-Star)
#   3. Starter (Started at least 41 games or played 2000 minutes)
#   4. Rotation (Played at least 1000 minutes)
#   5. Roster (Played at least one minute, but not met any of the top 4 outcomes)
#   6. Out of league (No longer in the NBA)

# Try to use Pandas, NumPy, Seaborn, and MatPlotLib

import pandas as pd
# import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load data from CSV files
player_stats = pd.read_csv('player_stats.csv')
awards_data = pd.read_csv('awards_data.csv')

# Calculate adjusted minutes and games started for lockout and shortened seasons
def adjust_minutes(row):
    #if row['season'] == 2011:
    #    return row['mins'] * (82/66)
    if row['season'] in [2019, 2020]:
        return round(row['mins'] * (82/72))
    else:
        return row['mins']

def adjust_games_start(row):
    if row['season'] in [2019, 2020]:
        return round(row['games_start'] * (82/72))
    else:
        return row['games_start']

player_stats['adjusted_minutes'] = player_stats.apply(adjust_minutes, axis=1)
player_stats['adjusted_games_start'] = player_stats.apply(adjust_games_start, axis=1)

# Filter data for players from the 2010 draft
players_2010_draft = player_stats[player_stats['draftyear'] == 2010].copy()

# Merge player stats and awards data
merged_data = pd.merge(players_2010_draft, awards_data, on=['season', 'nbapersonid'], how='left')

# Define a function to determine a player's career outcome
def get_career_outcome(row):
    seasons_after_first_four = merged_data[
        (merged_data['nbapersonid'] == row['nbapersonid']) &
        (merged_data['season'] > row['draftyear'] + 3) &
        (merged_data['season'] >= 2015) & (merged_data['season'] <= 2021)
    ]
    
    elite = seasons_after_first_four[seasons_after_first_four[['All NBA First Team', 'All NBA Second Team', 'All NBA Third Team', 'Most Valuable Player_rk']].any(axis=1) |
                                  seasons_after_first_four['Defensive Player Of The Year_rk'].eq(1)]
    
    all_star = seasons_after_first_four[seasons_after_first_four['all_star_game'] == 'TRUE']
    
    starter = seasons_after_first_four[(seasons_after_first_four['adjusted_games_start'] >= round(41 * (82/72))) |
                                       (seasons_after_first_four['adjusted_minutes'] >= round(2000 * (82/72)))]
    
    rotation = seasons_after_first_four[seasons_after_first_four['adjusted_minutes'] >= round(1000 * (82/72))]
    
    # Fetch the number of seasons to trace the player's best career outcome after their 4 years in the NBA
    if len(elite) >= 1:
        return 'Elite'
    elif len(all_star) >= 2:  # Adjusted this line to require at least two All-Star seasons
        return 'All-Star'
    elif len(starter) >= 2:
        return 'Starter'
    elif len(rotation) >= 2:
        return 'Rotation'
    elif len(seasons_after_first_four) >= 2:
        return 'Roster'
    else:
        return 'Out of the League'

# Apply the function to each player's data
players_2010_draft['career_outcome'] = players_2010_draft.apply(get_career_outcome, axis=1)

# Group by player and select the best career outcome
best_career_outcomes = players_2010_draft.groupby('nbapersonid')['career_outcome'].max()

# Define the desired order of career outcomes
outcome_order = ['Elite', 'All-Star', 'Starter', 'Rotation', 'Roster', 'Out of the League']

# Count the number of players in each career outcome bucket
career_outcome_counts = best_career_outcomes.value_counts().reindex(outcome_order).fillna(0)

# Print the career outcome counts
print("Career Outcome Counts:")
for outcome, count in career_outcome_counts.items():
    print(f"{outcome}: {count} players.")

# Plot the results using Seaborn and Matplotlib
sns.set(style='whitegrid', rc={"lines.linewidth": 1.5})
sns.set_context("talk", rc={"font.size": 10})
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=career_outcome_counts.index, y=career_outcome_counts.values, palette='viridis')
plt.title('2010 NBA Draft Players Best Career Outcome from 2015-2021')
plt.xlabel('Career Outcome')
plt.ylabel('Number of Players')
plt.xticks(rotation=45)
# plt.bar_label(ax.containers[0])

# Add tooltips to display player names on hover
def hover(event):
    plt.clf()
    sns.set(style='whitegrid')
    ax = sns.barplot(x=career_outcome_counts.index, y=career_outcome_counts.values, palette='viridis')
    plt.title('2010 NBA Draft Players Best Career Outcome from 2015-2021')
    plt.xlabel('Career Outcome')
    plt.ylabel('Number of Players')
    plt.xticks(rotation=45)
    plt.bar_label(ax.containers[0])
    if event.xdata is not None:
        index = int(event.xdata)
        outcome = career_outcome_counts.index[index]
        players_in_category = players_2010_draft[players_2010_draft['career_outcome'] == outcome]['player']
        players_in_category = players_in_category.drop_duplicates()  # Drop duplicate names
        plt.annotate('\n'.join(players_in_category), (index, career_outcome_counts[outcome]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=10)
    plt.tight_layout(pad=0)  # Set pad to 0 to remove tight layout warning
    plt.draw()

fig = plt.gcf()
fig.canvas.mpl_connect('motion_notify_event', hover)

# Display the plot
plt.show()

# Plot the results using Seaborn and Matplotlib
# sns.set(style='whitegrid')
# plt.figure(figsize=(10, 6))
# sns.barplot(x=career_outcome_counts.index, y=career_outcome_counts.values, palette='viridis')
# plt.title('2010 NBA Draft Players Best Career Outcome from 2015-2021')
# plt.xlabel('Career Outcome')
# plt.ylabel('Number of Players')
# plt.xticks(rotation=45)
# plt.tight_layout()

# # Display the plot
# plt.show()