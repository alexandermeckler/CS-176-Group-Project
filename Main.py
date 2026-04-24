import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the data
df = pd.read_csv('nba.csv')

# Clean the data: drop missing values and duplicates
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

# Assuming the CSV has columns: 'Home Team', 'Away Team', 'Home Score', 'Away Score'
# Calculate home wins
df['Home Win'] = df['Home Score'] > df['Away Score']

# Group by home team to get home win percentage
home_stats = df.groupby('Home Team').agg(
    home_games=('Home Win', 'count'),
    home_wins=('Home Win', 'sum')
)
home_stats['Home Pct'] = home_stats['home_wins'] / home_stats['home_games']

# Group by away team to get away win percentage
away_stats = df.groupby('Away Team').agg(
    away_games=('Home Win', 'count'),  # since every game is an away game for the away team
    away_wins=('Home Win', lambda x: (~x).sum())  # away win if home didn't win
)
away_stats['Away Pct'] = away_stats['away_wins'] / away_stats['away_games']

# Combine into one dataframe
all_teams = pd.concat([home_stats[['Home Pct']], away_stats[['Away Pct']]], axis=1, join='outer')

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(all_teams['Home Pct'], all_teams['Away Pct'])
for team in all_teams.index:
    plt.text(all_teams.loc[team, 'Home Pct'], all_teams.loc[team, 'Away Pct'], team, fontsize=8)
plt.xlabel('Home Win Percentage')
plt.ylabel('Away Win Percentage')
plt.title('Home vs Away Win Percentage for NBA Teams')
plt.grid(True)
os.makedirs('graphs', exist_ok=True)
plt.savefig('graphs/home_vs_away_win_percentage.png')
plt.show()

# Save cleaned data
df.to_csv('nba_cleaned.csv', index=False)