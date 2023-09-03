# Objective
# - Do the same setup as the previous question, but from 2015 draft and earlier
# - Players must qualify with All NBA/All Rookie team voting
# - These players must be limited before the 2015 season since the 
#   player must be able to base their career outcome by not counting 
#   the first four years of his career and track the three additional
#   seasons after their first four seasons in the league 
# - Build a model, predicting players drafted from 2018-2021
# - Predict a single career outcome for each player, but predict
#   by using the probability that each player falls into 

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Build a simple predictive model (e.g., Logistic Regression)
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# Load and preprocess data
player_stats = pd.read_csv('player_stats.csv')
awards_data = pd.read_csv('awards_data.csv')

# Filter data for players drafted in or before the 2015 season
train_data = player_stats[player_stats['draftyear'] <= 2015].copy()

# Merge player stats and awards data
merged_data = pd.merge(train_data, awards_data, on=['season', 'nbapersonid'], how='left')

# Define a function to determine career outcome based on provided criteria
def get_career_outcome(row):
    seasons_after_first_four = merged_data[
        (merged_data['nbapersonid'] == row['nbapersonid']) &
        (merged_data['season'] > row['draftyear'] + 3) &
        (merged_data['season'] >= 2015) & (merged_data['season'] <= 2021)
    ]
    
    elite = seasons_after_first_four[seasons_after_first_four[['All NBA First Team', 'All NBA Second Team', 'All NBA Third Team', 'Most Valuable Player_rk']].any(axis=1) |
                                  seasons_after_first_four['Defensive Player Of The Year_rk'].eq(1)]
    
    all_star = seasons_after_first_four[seasons_after_first_four['all_star_game'] == 'TRUE']
    
    starter = seasons_after_first_four[(seasons_after_first_four['games'] >= round(41 * (82/72))) |
                                       (seasons_after_first_four['mins'] >= round(2000 * (82/72)))]
    
    rotation = seasons_after_first_four[seasons_after_first_four['mins'] >= round(1000 * (82/72))]
    
    # Determine the player's best career outcome after the first four years
    if len(elite) >= 1:
        return 'Elite'
    elif len(all_star) >= 2:
        return 'All-Star'
    elif len(starter) >= 2:
        return 'Starter'
    elif len(rotation) >= 2:
        return 'Rotation'
    elif len(seasons_after_first_four) >= 2:
        return 'Roster'
    else:
        return 'Out of the League'

# Apply the get_career_outcome function to create the target variable
train_data['career_outcome'] = train_data.apply(get_career_outcome, axis=1)

# Display a summary of the career outcomes
career_outcomes_summary = Counter(train_data['career_outcome'])
# print(career_outcomes_summary)
# Print career outcomes summary in the desired format
print("------- Career Outcomes -------\n")
print(f"Elite: {career_outcomes_summary.get('Elite', 0)}")
print(f"All-Star: {career_outcomes_summary.get('All-Star', 0)}")
print(f"Starter: {career_outcomes_summary.get('Starter', 0)}")
print(f"Rotation: {career_outcomes_summary.get('Rotation', 0)}")
print(f"Roster: {career_outcomes_summary.get('Roster', 0)}")
print(f"Out of the League: {career_outcomes_summary.get('Out of the League', 0)}")


# Update the features list based on the available columns
features = ['mins', 'fgm', 'fga', 'fgp', 'fgm3', 'fga3', 'fgp3']  # Adjust this list based on your available columns
target = 'career_outcome'

# Split data into features (X) and target (y)
X = train_data[features]
y = train_data[target]

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Impute missing values and scale the data
imputer = SimpleImputer(strategy='mean')
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_imputed)
X_test_scaled = scaler.transform(X_test_imputed)

# Initialize and train the model
total_players = player_stats['player'].nunique()
model = LogisticRegression(max_iter=total_players, random_state=42)
model.fit(X_train_scaled, y_train)

# Predict career outcomes on the test set
y_pred = model.predict(X_test_scaled)

# Evaluate the model's accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy:.2%}")

# Filter data for players drafted in 2018-2021
test_data = player_stats[player_stats['draftyear'].isin(range(2018, 2022))].copy()

# Select features for the test data
X_test = test_data[features]

# Predict career outcomes for test data
X_test_imputed = imputer.transform(X_test)
X_test_scaled = scaler.transform(X_test_imputed)
test_predictions = model.predict(X_test_scaled)
test_predictions_proba = model.predict_proba(X_test_scaled)

# Convert predictions to a DataFrame
predictions_df = pd.DataFrame({'Player': test_data['player'], 'Predicted Outcome': test_predictions})

# Drop duplicates from the DataFrame (keep only the first occurrence of each player)
predictions_df = predictions_df.drop_duplicates(subset='Player', keep='first')

# Convert DataFrame to HTML table with a CSS class for hiding duplicates
predictions_table_html = predictions_df.to_html(index=False, classes='hide-duplicates')

# Print a success message
print("Predictions table generated successfully.")

# Define the full file path for the HTML predictions table
predictions_table_path = 'Part1/OpenEndedModelingQuestion/predictions_table.html'

# Initialize a set to keep track of processed players
seen_players = set()

# Open the existing HTML file in append mode
with open(predictions_table_path, 'a', encoding='utf-8') as f:
    # Write the new predictions HTML table to the file
    f.write(predictions_table_html)

    # Print a success message
    print("Predictions table saved successfully.")

    # Print predictions for selected players
    selected_players = ['Shai Gilgeous-Alexander', 'Zion Williamson', 'James Wiseman', 'Josh Giddey']
    print("\n------- Sample Outputs -------")

    for player, prediction, probabilities in zip(test_data['player'], test_predictions, test_predictions_proba):
        if player in selected_players and player not in seen_players:
            seen_players.add(player)
            elite_prob = f"{probabilities[0] * 100:.2f}%"
            all_star_prob = f"{probabilities[1] * 100:.2f}%"
            starter_prob = f"{probabilities[2] * 100:.2f}%"
            rotation_prob = f"{probabilities[3] * 100:.2f}%"
            roster_prob = f"{probabilities[4] * 100:.2f}%"
            out_of_league_prob = f"{(1 - sum(probabilities[:5])) * 100:.2f}%"
            print(f"\n{player}: Predicted Outcome - {prediction}, Probabilities - [Elite: {elite_prob}, All-Star: {all_star_prob}, Starter: {starter_prob}, Rotation: {rotation_prob}, Roster: {roster_prob}, Out of the League: {out_of_league_prob}]")

            # Append the player's information to the HTML table if not already present
            if player not in seen_players:
                seen_players.add(player)
                if player in selected_players:
                    # Add a CSS class to hide duplicate rows
                    predictions_table_html += f"<tr class='duplicate'><td>{player}</td><td>{prediction}</td></tr>\n"
                else:
                    predictions_table_html += f"<tr><td>{player}</td><td>{prediction}</td></tr>\n"

# Create a bar plot of predicted career outcomes
plt.figure(figsize=(8, 6))
sns.countplot(data=train_data, x='career_outcome', order=['Elite', 'All-Star', 'Starter', 'Rotation', 'Roster', 'Out of the League'])
plt.title('Distribution of Predicted Career Outcomes')
plt.xlabel('Career Outcome')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()