# Objective: 
# Find average number of years experience in 2007 or later seasons for
# players to make All NBA First, Second, and Third teams by searching
# for players drafted in 2007 or later that eventually win at least one
# All NBA selection

# Features to add
#   - Have four choices of 1st team, 2nd team, 3rd team, and average of all teams
#   - Gather the data by checking when the player reached one of those 3 teams for 
#   - the first time in their careers to prevent duplicates

# Try to use Pandas, NumPy, Seaborn, and MatPlotLib

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.widgets import CheckButtons

# Load data
players_stats = pd.read_csv("player_stats.csv")
awards_data = pd.read_csv("awards_data.csv")

# Filter players who were drafted in 2007 or later
filtered_players_stats = players_stats[players_stats["draftyear"] >= 2007]

# Create a dictionary to store the year of the first All NBA selection for each player
first_all_nba_year = {}

# Iterate through each row in the awards data
for index, row in awards_data.iterrows():
    player_id = row["nbapersonid"]
    year = row["season"]
    if (
        (row["All NBA First Team"] == 1)
        | (row["All NBA Second Team"] == 1)
        | (row["All NBA Third Team"] == 1)
    ):
        if player_id not in first_all_nba_year:
            first_all_nba_year[player_id] = year

# Filter players who didn't win an All NBA selection
filtered_players_stats = filtered_players_stats[filtered_players_stats["nbapersonid"].isin(first_all_nba_year.keys())]

# Calculate the years of experience for each player
filtered_players_stats["first_all_nba_year"] = filtered_players_stats["nbapersonid"].map(first_all_nba_year)
filtered_players_stats["years_of_experience"] = (
    filtered_players_stats["first_all_nba_year"] - filtered_players_stats["draftyear"]
)

# Calculate the average number of years of experience to win the first All NBA selection
average_years_to_first_all_nba = filtered_players_stats.groupby("first_all_nba_year")[
    "years_of_experience"
].mean()

# Calculate the average years of experience for each All-NBA team (1st, 2nd, and 3rd teams)
average_1st_team = filtered_players_stats[filtered_players_stats["nbapersonid"].isin(awards_data[awards_data["All NBA First Team"] == 1]["nbapersonid"])].groupby("first_all_nba_year")["years_of_experience"].mean()
average_2nd_team = filtered_players_stats[filtered_players_stats["nbapersonid"].isin(awards_data[awards_data["All NBA Second Team"] == 1]["nbapersonid"])].groupby("first_all_nba_year")["years_of_experience"].mean()
average_3rd_team = filtered_players_stats[filtered_players_stats["nbapersonid"].isin(awards_data[awards_data["All NBA Third Team"] == 1]["nbapersonid"])].groupby("first_all_nba_year")["years_of_experience"].mean()

# Display the result for each season
print("Average number of years of experience to win first All NBA selection:\n")
for season in range(2007, 2022):
    avg_years_all_nba = average_years_to_first_all_nba.get(season, float("nan"))  # Use get method to handle missing data
    avg_years_1st_team = average_1st_team.get(season, float("nan"))
    avg_years_2nd_team = average_2nd_team.get(season, float("nan"))
    avg_years_3rd_team = average_3rd_team.get(season, float("nan"))
    
    avg_years_all_nba = 0 if pd.isna(avg_years_all_nba) else avg_years_all_nba
    avg_years_1st_team = 0 if pd.isna(avg_years_1st_team) else avg_years_1st_team
    avg_years_2nd_team = 0 if pd.isna(avg_years_2nd_team) else avg_years_2nd_team
    avg_years_3rd_team = 0 if pd.isna(avg_years_3rd_team) else avg_years_3rd_team
    
    print("{}: Average: {:.2f} | 1st Team: {:.2f} | 2nd Team: {:.2f} | 3rd Team: {:.2f}".format(
        season, avg_years_all_nba, avg_years_1st_team, avg_years_2nd_team, avg_years_3rd_team
    ))

# Visualize the distribution of years of experience
# plt.figure(figsize=(10, 6))
fig, ax = plt.subplots(figsize=(10, 6))

line_all_nba, = ax.plot(average_years_to_first_all_nba.index, average_years_to_first_all_nba.values, marker='o', label='Average')
line_1st_team, = ax.plot(average_1st_team.index, average_1st_team.values, marker='o', label='1st Team')
line_2nd_team, = ax.plot(average_2nd_team.index, average_2nd_team.values, marker='o', label='2nd Team')
line_3rd_team, = ax.plot(average_3rd_team.index, average_3rd_team.values, marker='o', label='3rd Team')

# Calculate and display the overall, 1st, 2nd and 3rd average
overall_avg = average_years_to_first_all_nba.mean()
average_1st_team = filtered_players_stats[filtered_players_stats["nbapersonid"].isin(awards_data[awards_data["All NBA First Team"] == 1]["nbapersonid"])].groupby("first_all_nba_year")["years_of_experience"].mean()
average_2nd_team = filtered_players_stats[filtered_players_stats["nbapersonid"].isin(awards_data[awards_data["All NBA Second Team"] == 1]["nbapersonid"])].groupby("first_all_nba_year")["years_of_experience"].mean()
average_3rd_team = filtered_players_stats[filtered_players_stats["nbapersonid"].isin(awards_data[awards_data["All NBA Third Team"] == 1]["nbapersonid"])].groupby("first_all_nba_year")["years_of_experience"].mean()

print("\nOverall Average: {:.2f}".format(overall_avg))
print("Average years of experience for 1st Team: {:.2f}".format(average_1st_team.mean()))
print("Average years of experience for 2nd Team: {:.2f}".format(average_2nd_team.mean()))
print("Average years of experience for 3rd Team: {:.2f}".format(average_3rd_team.mean()))
    # print(f"{season}: {avg:.2f}")
    
# print("\nAverage years of experience for 2nd Team:\n")
# for season, avg in average_2nd_team.items():
#     print(f"{season}: {avg:.2f}")
    
# print("\nAverage years of experience for 3rd Team:\n")
# for season, avg in average_3rd_team.items():
#     print(f"{season}: {avg:.2f}")

# Annotate the plot with average values
# def annotate_average(ax, label, avg_values):
#     for year, avg in avg_values.items():
#         if not pd.isna(avg):
#             ax.annotate(f"{label} Avg: {avg:.2f}", xy=(year, avg), xytext=(-30, 8), textcoords="offset points", color="black", fontsize=8)

# annotate_average(ax, 'All NBA', average_years_to_first_all_nba)
# annotate_average(ax, '1st Team', average_1st_team)
# annotate_average(ax, '2nd Team', average_2nd_team)
# annotate_average(ax, '3rd Team', average_3rd_team)
# annotate_average(ax, 'Overall', {year: overall_avg for year in range(2007, 2022)})

# sns.lineplot(
#     x=average_years_to_first_all_nba.index.astype(int),
#     y=average_years_to_first_all_nba.values,
#     marker='o',
#     label='All NBA'
# )
# sns.lineplot(
#     x=average_1st_team.index.astype(int),
#     y=average_1st_team.values,
#     marker='o',
#     label='1st Team'
# )
# sns.lineplot(
#     x=average_2nd_team.index.astype(int),
#     y=average_2nd_team.values,
#     marker='o',
#     label='2nd Team'
# )
# sns.lineplot(
#     x=average_3rd_team.index.astype(int),
#     y=average_3rd_team.values,
#     marker='o',
#     label='3rd Team'
# )
plt.xlabel("Year")
plt.ylabel("Average Years of Experience")
plt.title("Average Years of Experience to First All NBA Selection (2007-2021)")
plt.legend()

# Create checkboxes
rax = plt.axes([0.3, 0.6, 0.15, 0.3], aspect='equal')
check = CheckButtons(rax, ['Average', '1st Team', '2nd Team', '3rd Team'], [True, True, True, True])

# Function to update line visibility
def update_lines(label):
    lines = {'Average': line_all_nba, '1st Team': line_1st_team, '2nd Team': line_2nd_team, '3rd Team': line_3rd_team}
    for team_label, line in lines.items():
        if label == team_label:
            line.set_visible(not line.get_visible())
    
    plt.draw()

check.on_clicked(update_lines)

# Set labels, title, and legend
# plt.xlabel("Year")
# plt.ylabel("Average Years of Experience")
# plt.title("Average Years of Experience to First All NBA Selection (2007-2021)")
# plt.legend()

plt.show()




# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Load data
# players_stats = pd.read_csv("Datasets/player_stats.csv")
# awards_data = pd.read_csv("Datasets/awards_data.csv")

# # Filter players who were drafted in 2007 or later
# filtered_players_stats = players_stats[players_stats["draftyear"] >= 2007]

# # Create a dictionary to store the year of the first All NBA selection for each player
# first_all_nba_year = {}

# # Iterate through each row in the awards data
# for index, row in awards_data.iterrows():
#     player_id = row["nbapersonid"]
#     year = row["season"]
#     if (
#         (row["All NBA First Team"] == 1)
#         or (row["All NBA Second Team"] == 1)
#         or (row["All NBA Third Team"] == 1)
#     ):
#         # Check if player ID and year combination is already in the dictionary
#         if (player_id, year) not in first_all_nba_year:
#             first_all_nba_year[(player_id, year)] = year

# # Filter players who didn't win an All NBA selection
# filtered_players_stats = filtered_players_stats[
#     filtered_players_stats["nbapersonid"].isin([player_id for (player_id, year) in first_all_nba_year.keys()])
# ]

# # Calculate the years of experience for each player
# filtered_players_stats["first_all_nba_year"] = filtered_players_stats["nbapersonid"].map(
#     {player_id: year for (player_id, year) in first_all_nba_year.keys()}
# )
# filtered_players_stats["years_of_experience"] = (
#     filtered_players_stats["first_all_nba_year"] - filtered_players_stats["draftyear"]
# )

# # Calculate the average number of years of experience to win the first All NBA selection
# average_years_to_first_all_nba = filtered_players_stats.groupby("first_all_nba_year")[
#     "years_of_experience"
# ].mean()

# # Display the result for each season
# print("Average number of years of experience to win first All NBA selection:")
# for season in range(2007, 2022):
#     avg_years = average_years_to_first_all_nba.get(season, float("nan"))
#     if pd.isna(avg_years):
#         print("{}: N/A".format(season))
#     else:
#         print("{}: {:.2f}".format(season, avg_years))

# # Calculate and display the overall average
# overall_avg = average_years_to_first_all_nba.mean()
# print("\nOverall Average: {:.2f}".format(overall_avg))

# # Visualize the distribution of years of experience
# plt.figure(figsize=(10, 6))
# sns.barplot(
#     x=average_years_to_first_all_nba.index.astype(int),
#     y=average_years_to_first_all_nba.values,
# )
# plt.xlabel("Year")
# plt.ylabel("Average Years of Experience")
# plt.title("Average Years of Experience to First All NBA Selection (2007-2021)")

# # Add x-axis ticks and labels for years 2007 and 2008
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Load data
# players_stats = pd.read_csv("Datasets/player_stats.csv")
# awards_data = pd.read_csv("Datasets/awards_data.csv")

# # Filter players who were drafted in 2007 or later
# filtered_players_stats = players_stats[players_stats["draftyear"] >= 2007]

# # Create a dictionary to store the year of the first All NBA selection for each player
# first_all_nba_year = {}

# # Iterate through each row in the awards data
# for index, row in awards_data.iterrows():
#     player_id = row["nbapersonid"]
#     year = row["season"]
#     if (
#         (row["All NBA First Team"] == 1)
#         | (row["All NBA Second Team"] == 1)
#         | (row["All NBA Third Team"] == 1)
#     ):
#         if player_id not in first_all_nba_year:
#             first_all_nba_year[player_id] = year

# # Filter players who didn't win an All NBA selection
# filtered_players_stats = filtered_players_stats[filtered_players_stats["nbapersonid"].isin(first_all_nba_year.keys())]

# # Calculate the years of experience for each player
# filtered_players_stats["first_all_nba_year"] = filtered_players_stats["nbapersonid"].map(first_all_nba_year)
# filtered_players_stats["years_of_experience"] = (
#     filtered_players_stats["first_all_nba_year"] - filtered_players_stats["draftyear"]
# )

# # Calculate the average number of years of experience to win the first All NBA selection
# average_years_to_first_all_nba = filtered_players_stats.groupby("first_all_nba_year")[
#     "years_of_experience"
# ].mean()

# # Create a new DataFrame for years 2007 and 2008 with zero values
# years_2007_2008 = pd.DataFrame({
#     "years_of_experience": [0, 0],
# }, index=[2007, 2008])

# # Calculate the average number of years of experience to win the first All NBA selection
# # average_years_to_first_all_nba = filtered_players_stats.groupby("first_all_nba_year")[
# #     "years_of_experience"
# # ].mean()

# # Replace NaN values with 0
# # average_years_to_first_all_nba = average_years_to_first_all_nba.fillna(-1)

# # Display the result for each season
# print("Average number of years of experience to win first All NBA selection:")
# for season in range(2007, 2022):
#     avg_years = average_years_to_first_all_nba.get(season, float("nan"))  # Use get method to handle missing data
#     if pd.isna(avg_years):
#         print("{}: N/A".format(season))
#     else:
#         print("{}: {:.2f}".format(season, avg_years))  # .2f = two decimal places of the number

# # Calculate and display the overall average
# overall_avg = average_years_to_first_all_nba.mean()
# print("\nOverall Average: {:.2f}".format(overall_avg))

# # Visualize the distribution of years of experience
# plt.figure(figsize=(10, 6))
# sns.barplot(
#     x=average_years_to_first_all_nba.index.astype(int),
#     y=average_years_to_first_all_nba.values,
# )
# plt.xlabel("Year")
# plt.ylabel("Average Years of Experience")
# plt.title("Average Years of Experience to First All NBA Selection (2007-2021)")

# # Add x-axis ticks and labels for years 2007 and 2008
# plt.tight_layout()
# plt.show()

# ---------------------------------------------------------------------------------------------------------


# Objective: 
# Find average number of years experience in 2007 or later seasons for
# players to make All NBA First, Second, and Third teams by searching
# for players drafted in 2007 or later that eventually win at least one
# All NBA selection

# Try to use Pandas, NumPy, Seaborn, and MatPlotLib

# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Load data
# players_stats = pd.read_csv("player_stats.csv")
# awards_data = pd.read_csv("awards_data.csv")

# # Filter data for players who were drafted in 2007 or later and made All NBA selections between 2007 and 2021
# filtered_awards = awards_data[
#     (
#         (awards_data["All NBA First Team"] == 1)
#         | (awards_data["All NBA Second Team"] == 1)
#         | (awards_data["All NBA Third Team"] == 1)
#     )
#     & (awards_data["season"] >= 2007)  # All NBA selections from 2007 onwards
# ]

# # Filter players who were drafted in 2007 or later
# filtered_players_stats = players_stats[players_stats["draftyear"] >= 2007]

# # Create a dictionary to store the year of the first All NBA selection for each player
# first_all_nba_year = {}

# # Iterate through each row in the filtered awards data
# for index, row in filtered_awards.iterrows():
#     player_id = row["nbapersonid"]
#     year = row["season"]
#     if player_id not in first_all_nba_year:
#         first_all_nba_year[player_id] = year

# # Calculate the years of experience for each player
# filtered_players_stats["first_all_nba_year"] = filtered_players_stats["nbapersonid"].map(first_all_nba_year)
# filtered_players_stats["years_of_experience"] = (
#     filtered_players_stats["season"] - filtered_players_stats["draftyear"]
# )

# # Filter out players who didn't win an All NBA selection
# filtered_players_stats = filtered_players_stats[filtered_players_stats["first_all_nba_year"].notna()]

# # Calculate the average number of years of experience to win the first All NBA selection
# average_years_to_first_all_nba = filtered_players_stats.groupby("first_all_nba_year")[
#     "years_of_experience"
# ].mean()

# # Display the result for each season
# print("Average number of years of experience to win first All NBA selection:")
# for season in range(2007, 2022):
#     avg_years = average_years_to_first_all_nba.get(season, float("nan"))  # Use get method to handle missing data
#     print("{}: {:.2f}".format(season, avg_years))  # .2f = two decimal places of the number

# # Calculate and display the overall average
# overall_avg = average_years_to_first_all_nba.mean()
# print("\nOverall Average: {:.2f}".format(overall_avg))

# # Visualize the distribution of years of experience
# plt.figure(figsize=(10, 6))
# sns.barplot(
#     x=average_years_to_first_all_nba.index.astype(int),
#     y=average_years_to_first_all_nba.values,
# )
# plt.xlabel("Year")
# plt.ylabel("Average Years of Experience")
# plt.title("Average Years of Experience to First All NBA Selection (2007-2021)")
# plt.tight_layout()
# plt.show()
