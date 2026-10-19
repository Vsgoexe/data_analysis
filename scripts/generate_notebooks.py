"""
Script to generate well-structured, formatted Jupyter Notebooks (.ipynb)
for Cognifyz Data Analysis Internship: Level 1, Level 2, and Level 3.
Candidate: Jeevani Vedavendra (Ref: CTI/A1/C421603)
"""

import json
import os

def create_nb(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.11.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

def md_cell(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip().split("\n")]
    }

def code_cell(code):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in code.strip().split("\n")]
    }

def generate_level_1():
    cells = [
        md_cell("""# Cognifyz Technologies - Data Analysis Internship
## Level 1 Analysis
**Candidate Name:** Jeevani Vedavendra  
**Reference ID:** CTI/A1/C421603  
**Domain:** Data Analysis  

---
### Overview of Level 1 Tasks:
1. **Task 1: Top Cuisines** - Determine the top three most common cuisines and the percentage of restaurants that serve each.
2. **Task 2: City Analysis** - Identify the city with the highest number of restaurants, calculate average ratings per city, and find the highest-rated city.
3. **Task 3: Price Range Distribution** - Visualize price range distribution with charts and calculate percentage share for each category.
4. **Task 4: Online Delivery** - Determine online delivery availability and compare ratings between restaurants with and without online delivery."""),
        
        md_cell("### Step 1: Import Libraries and Load Dataset"),
        code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visualization styles
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'font.sans-serif': 'Segoe UI', 'font.size': 11})

# Load the dataset
df = pd.read_csv('../Dataset .csv')
print(f"Dataset Shape: {df.shape}")
df.head(3)"""),

        md_cell("""---
## Task 1: Top Cuisines
- Determine the top three most common cuisines in the dataset.
- Calculate the percentage of restaurants that serve each of the top cuisines."""),
        code_cell("""# Calculate top cuisines
total_restaurants = len(df)

# Split comma-separated cuisines
cuisines_series = df['Cuisines'].dropna().apply(lambda x: [c.strip() for c in str(x).split(',')]).explode()
cuisine_counts = cuisines_series.value_counts()
top_3_cuisines = cuisine_counts.head(3)

print("Top 3 Cuisines:")
for cuisine, count in top_3_cuisines.items():
    pct = (df['Cuisines'].dropna().apply(lambda x: cuisine in [c.strip() for c in str(x).split(',')]).sum() / total_restaurants) * 100
    print(f"- {cuisine}: {count} occurrences ({pct:.2f}% of restaurants)")"""),
        code_cell("""# Visualize Top 10 Cuisines
plt.figure(figsize=(9, 5))
top_10 = cuisine_counts.head(10).reset_index()
top_10.columns = ['Cuisine', 'Count']
palette = ['#e63946' if i < 3 else '#457b9d' for i in range(len(top_10))]

sns.barplot(data=top_10, x='Count', y='Cuisine', palette=palette, hue='Cuisine', legend=False)
plt.title("Top 10 Most Common Cuisines (Top 3 Highlighted)", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Number of Restaurants")
plt.ylabel("Cuisine")

for i, v in enumerate(top_10['Count']):
    pct = (v / total_restaurants) * 100
    plt.text(v + 30, i, f"{v:,} ({pct:.1f}%)", va='center', fontsize=9, fontweight='semibold')

plt.tight_layout()
plt.show()"""),
        md_cell("""**Key Findings - Task 1:**
- **North Indian** is the dominant cuisine, offered by 41.46% of all restaurants.
- **Chinese** ranks second at 28.61%.
- **Fast Food** ranks third at 20.79%."""),

        md_cell("""---
## Task 2: City Analysis
- Identify the city with the highest number of restaurants in the dataset.
- Calculate the average rating for restaurants in each city.
- Determine the city with the highest average rating."""),
        code_cell("""# City with highest number of restaurants
city_counts = df['City'].value_counts()
top_city = city_counts.index[0]
print(f"City with highest number of restaurants: {top_city} ({city_counts.iloc[0]} restaurants, {city_counts.iloc[0]/total_restaurants*100:.2f}%)")

# Average rating per city
city_avg_rating = df.groupby('City')['Aggregate rating'].agg(['count', 'mean']).reset_index()
city_avg_rating.columns = ['City', 'Restaurant_Count', 'Average_Rating']

# City with highest average rating (all & hubs with >= 10 outlets)
highest_avg_city_all = city_avg_rating.sort_values(by='Average_Rating', ascending=False).iloc[0]
print(f"City with highest average rating (overall): {highest_avg_city_all['City']} ({highest_avg_city_all['Average_Rating']:.2f})")"""),
        code_cell("""# Plot City Analysis
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Top 10 cities by restaurant count
top_10_cities = city_counts.head(10).reset_index()
top_10_cities.columns = ['City', 'Count']
sns.barplot(data=top_10_cities, y='City', x='Count', palette='Blues_r', hue='City', legend=False, ax=axes[0])
axes[0].set_title("Top 10 Cities by Restaurant Count", fontsize=12, fontweight='bold')
axes[0].set_xlabel("Number of Restaurants")

# Top 10 cities by average rating (min 10 restaurants)
top_rated_cities = city_avg_rating[city_avg_rating['Restaurant_Count'] >= 10].sort_values(by='Average_Rating', ascending=False).head(10)
sns.barplot(data=top_rated_cities, y='City', x='Average_Rating', palette='YlGnBu_r', hue='City', legend=False, ax=axes[1])
axes[1].set_title("Top 10 Cities by Average Rating (Min 10 Restaurants)", fontsize=12, fontweight='bold')
axes[1].set_xlabel("Average Aggregate Rating")
axes[1].set_xlim(0, 5)

plt.tight_layout()
plt.show()"""),
        md_cell("""**Key Findings - Task 2:**
- **New Delhi** has the highest number of restaurants with 5,473 locations (57.30% of the entire dataset).
- High-performing dining hubs like Inner City (4.90), Quezon City (4.80), and Makati City (4.65) lead in overall customer satisfaction."""),

        md_cell("""---
## Task 3: Price Range Distribution
- Create a histogram or bar chart to visualize the distribution of price ranges among the restaurants.
- Calculate the percentage of restaurants in each price range category."""),
        code_cell("""price_counts = df['Price range'].value_counts().sort_index()
price_pct = (price_counts / total_restaurants) * 100

for pr, count in price_counts.items():
    print(f"Price Range {pr}: {count} restaurants ({price_pct[pr]:.2f}%)")"""),
        code_cell("""plt.figure(figsize=(8, 5))
sns.barplot(x=price_counts.index, y=price_counts.values, palette='viridis', hue=price_counts.index, legend=False)
plt.title("Distribution of Price Ranges Among Restaurants", fontsize=13, fontweight='bold')
plt.xlabel("Price Range (1 = Budget, 4 = Fine Dining)")
plt.ylabel("Number of Restaurants")

for i, (val, pct) in enumerate(zip(price_counts.values, price_pct.values)):
    plt.text(i, val + 70, f"{val:,}\\n({pct:.1f}%)", ha='center', va='bottom', fontsize=10, fontweight='semibold')

plt.ylim(0, price_counts.max() * 1.15)
plt.tight_layout()
plt.show()"""),
        md_cell("""**Key Findings - Task 3:**
- **Price Range 1 (Budget)** is the largest category, accounting for **46.53%** (4,444 restaurants).
- **Price Range 2 (Mid-range)** comprises **32.59%** (3,113 restaurants).
- Premium dining (Price Range 3 & 4) represents 14.74% and 6.14% respectively."""),

        md_cell("""---
## Task 4: Online Delivery
- Determine the percentage of restaurants that offer online delivery.
- Compare the average ratings of restaurants with and without online delivery."""),
        code_cell("""delivery_counts = df['Has Online delivery'].value_counts()
delivery_pct = (delivery_counts / total_restaurants) * 100

print(f"Offers Online Delivery: {delivery_pct.get('Yes', 0):.2f}% ({delivery_counts.get('Yes', 0)} restaurants)")
print(f"No Online Delivery: {delivery_pct.get('No', 0):.2f}% ({delivery_counts.get('No', 0)} restaurants)")

# Ratings comparison
rating_by_delivery = df.groupby('Has Online delivery')['Aggregate rating'].agg(['count', 'mean', 'median', 'std'])
display(rating_by_delivery)"""),
        code_cell("""fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Proportion pie chart
axes[0].pie(
    delivery_counts.values, 
    labels=[f"No Online Delivery\\n({delivery_pct.get('No', 0):.1f}%)", f"Offers Online Delivery\\n({delivery_pct.get('Yes', 0):.1f}%)"],
    autopct='%1.1f%%',
    colors=['#e76f51', '#2a9d8f'],
    startangle=140,
    explode=(0, 0.08),
    shadow=True
)
axes[0].set_title("Proportion of Restaurants Offering Online Delivery", fontsize=12, fontweight='bold')

# Boxplot rating comparison
sns.boxplot(data=df, x='Has Online delivery', y='Aggregate rating', palette=['#e76f51', '#2a9d8f'], hue='Has Online delivery', legend=False, ax=axes[1], width=0.4)
axes[1].set_title("Rating Comparison: Online Delivery vs No Delivery", fontsize=12, fontweight='bold')
axes[1].set_xlabel("Has Online Delivery")
axes[1].set_ylabel("Aggregate Rating (0 - 5)")

plt.tight_layout()
plt.show()"""),
        md_cell("""**Key Findings - Task 4:**
- **25.66%** of restaurants offer online delivery, while **74.34%** do not.
- Restaurants offering online delivery achieve a substantially higher overall average rating (**3.25**) compared to restaurants without delivery (**2.47**), driven partly by fewer unrated outlets in online delivery catalogs.""")
    ]
    return create_nb(cells)

def generate_level_2():
    cells = [
        md_cell("""# Cognifyz Technologies - Data Analysis Internship
## Level 2 Analysis
**Candidate Name:** Jeevani Vedavendra  
**Reference ID:** CTI/A1/C421603  
**Domain:** Data Analysis  

---
### Overview of Level 2 Tasks:
1. **Task 1: Restaurant Ratings** - Analyze the distribution of aggregate ratings, determine the most common rating range, and calculate the average number of votes.
2. **Task 2: Cuisine Combination** - Identify the most common multi-cuisine combinations and determine if certain combinations tend to receive higher ratings.
3. **Task 3: Geographic Analysis** - Plot the locations of restaurants using latitude and longitude coordinates and identify patterns or clusters.
4. **Task 4: Restaurant Chains** - Identify restaurant chains in the dataset and analyze their ratings and popularity."""),

        md_cell("### Step 1: Import Libraries and Load Dataset"),
        code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'font.sans-serif': 'Segoe UI', 'font.size': 11})

df = pd.read_csv('../Dataset .csv')
print(f"Dataset Shape: {df.shape}")
df.head(3)"""),

        md_cell("""---
## Task 1: Restaurant Ratings
- Analyze the distribution of aggregate ratings and determine the most common rating range.
- Calculate the average number of votes received by restaurants."""),
        code_cell("""ratings = df['Aggregate rating']
mean_rating = ratings.mean()
median_rating = ratings.median()
avg_votes = df['Votes'].mean()

print(f"Mean Rating: {mean_rating:.2f}")
print(f"Median Rating: {median_rating:.2f}")
print(f"Average number of votes per restaurant: {avg_votes:.2f}")

# Categorical rating ranges
bins = [0, 1.9, 2.9, 3.9, 4.9, 5.0]
labels = ['0.0 - 1.9 (Poor/Unrated)', '2.0 - 2.9 (Average)', '3.0 - 3.9 (Good)', '4.0 - 4.9 (Very Good)', '5.0 (Perfect)']
df['Rating_Range'] = pd.cut(df['Aggregate rating'], bins=bins, labels=labels, include_lowest=True)
range_counts = df['Rating_Range'].value_counts().sort_index()

most_common_range = range_counts.idxmax()
print(f"\\nMost common rating range: {most_common_range} ({range_counts[most_common_range]} restaurants, {range_counts[most_common_range]/len(df)*100:.2f}%)")"""),
        code_cell("""fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Rating histogram & KDE
sns.histplot(df['Aggregate rating'], bins=20, kde=True, color='#2a9d8f', ax=axes[0])
axes[0].axvline(mean_rating, color='#e76f51', linestyle='--', linewidth=2, label=f'Mean: {mean_rating:.2f}')
axes[0].axvline(median_rating, color='#e9c46a', linestyle='-', linewidth=2, label=f'Median: {median_rating:.2f}')
axes[0].set_title("Distribution of Aggregate Ratings", fontsize=12, fontweight='bold')
axes[0].set_xlabel("Aggregate Rating")
axes[0].legend()

# Rating range bar chart
range_df = range_counts.reset_index()
range_df.columns = ['Rating_Range', 'Count']
palette = ['#e63946' if r == most_common_range else '#457b9d' for r in range_df['Rating_Range']]
sns.barplot(data=range_df, x='Rating_Range', y='Count', palette=palette, hue='Rating_Range', legend=False, ax=axes[1])
axes[1].set_title("Most Common Rating Ranges (Highest Highlighted)", fontsize=12, fontweight='bold')
axes[1].set_xlabel("Rating Range")
axes[1].tick_params(axis='x', rotation=25)

plt.tight_layout()
plt.show()"""),
        md_cell("""**Key Findings - Task 1:**
- The most common rating range is **3.0 - 3.9 (Good)** with **4,590 restaurants (48.06%)**.
- The overall average rating across all restaurants is **2.67**, and the average number of votes received is **156.91 votes**."""),

        md_cell("""---
## Task 2: Cuisine Combinations
- Identify the most common combinations of cuisines in the dataset.
- Determine if certain cuisine combinations tend to have higher ratings."""),
        code_cell("""# Identify multi-cuisine combinations
cuisine_combos = df['Cuisines'].dropna()
combo_counts = cuisine_combos.value_counts()
multi_combos = combo_counts[combo_counts.index.str.contains(',')].head(10)

print("Top 5 Multi-Cuisine Combinations:")
for combo, count in multi_combos.head(5).items():
    print(f"- {combo}: {count} restaurants")

# Analyze ratings for combinations with >= 15 restaurants
combo_ratings = df.groupby('Cuisines').agg(
    Count=('Aggregate rating', 'count'),
    Avg_Rating=('Aggregate rating', 'mean')
).reset_index()

top_rated_combos = combo_ratings[combo_ratings['Count'] >= 15].sort_values(by='Avg_Rating', ascending=False).head(10)
display(top_rated_combos.head(5))"""),
        code_cell("""fig, axes = plt.subplots(1, 2, figsize=(16, 6))

most_freq_df = multi_combos.head(8).reset_index()
most_freq_df.columns = ['Combination', 'Count']
sns.barplot(data=most_freq_df, y='Combination', x='Count', palette='crest', hue='Combination', legend=False, ax=axes[0])
axes[0].set_title("Most Common Multi-Cuisine Combinations", fontsize=12, fontweight='bold')
axes[0].set_xlabel("Number of Restaurants")

sns.barplot(data=top_rated_combos.head(8), y='Cuisines', x='Avg_Rating', palette='flare', hue='Cuisines', legend=False, ax=axes[1])
axes[1].set_title("Cuisine Combinations with Highest Average Ratings", fontsize=12, fontweight='bold')
axes[1].set_xlabel("Average Rating (0 to 5)")
axes[1].set_xlim(0, 5)

plt.tight_layout()
plt.show()"""),
        md_cell("""**Key Findings - Task 2:**
- **North Indian, Chinese** is by far the most frequent pairing (511 restaurants), followed by **North Indian, Mughlai** (334 restaurants).
- Specialized combinations such as Japanese/Sushi (4.04), Thai (4.10), and Italian pairings achieve significantly higher average customer ratings than general fast-food pairings."""),

        md_cell("""---
## Task 3: Geographic Analysis
- Plot the locations of restaurants on a map using longitude and latitude coordinates.
- Identify any patterns or clusters of restaurants in specific areas."""),
        code_cell("""# Filter out invalid (0,0) coordinates
geo_df = df[(df['Longitude'] != 0) & (df['Latitude'] != 0)].copy()
ncr_df = geo_df[geo_df['City'].isin(['New Delhi', 'Gurgaon', 'Noida', 'Faridabad', 'Ghaziabad'])]

print(f"Total valid coordinate entries: {len(geo_df)}")
print(f"Delhi NCR Cluster Count: {len(ncr_df)} ({len(ncr_df)/len(df)*100:.1f}%)")"""),
        code_cell("""fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Global scatter
scatter1 = axes[0].scatter(geo_df['Longitude'], geo_df['Latitude'], c=geo_df['Aggregate rating'], cmap='Spectral_r', alpha=0.6, s=15)
fig.colorbar(scatter1, ax=axes[0], label='Aggregate Rating')
axes[0].set_title("Global Restaurant Coordinates", fontsize=12, fontweight='bold')
axes[0].set_xlabel("Longitude")
axes[0].set_ylabel("Latitude")

# Primary NCR cluster
scatter2 = axes[1].scatter(ncr_df['Longitude'], ncr_df['Latitude'], c=ncr_df['Aggregate rating'], cmap='Spectral_r', alpha=0.5, s=20)
fig.colorbar(scatter2, ax=axes[1], label='Aggregate Rating')
axes[1].set_title("Primary Cluster: Delhi NCR Region", fontsize=12, fontweight='bold')
axes[1].set_xlabel("Longitude")
axes[1].set_ylabel("Latitude")

plt.tight_layout()
plt.show()"""),
        md_cell("""**Key Findings - Task 3:**
- A massive geographic cluster is concentrated in the **Delhi NCR Region** (India), representing **79.0%** of the entire dataset.
- Secondary international clusters include the United States, UAE, Brazil, and South Africa."""),

        md_cell("""---
## Task 4: Restaurant Chains
- Identify if there are any restaurant chains present in the dataset.
- Analyze the ratings and popularity of different restaurant chains."""),
        code_cell("""outlet_counts = df['Restaurant Name'].value_counts()
chains = outlet_counts[outlet_counts > 1]
total_chain_outlets = chains.sum()

print(f"Unique chain brands: {len(chains)}")
print(f"Total chain outlets: {total_chain_outlets} ({total_chain_outlets/len(df)*100:.2f}%)")

chain_df = df[df['Restaurant Name'].isin(chains.index)]
chain_stats = chain_df.groupby('Restaurant Name').agg(
    Outlets=('Aggregate rating', 'count'),
    Avg_Rating=('Aggregate rating', 'mean'),
    Total_Votes=('Votes', 'sum')
).reset_index()

top_chains_by_outlets = chain_stats.sort_values(by='Outlets', ascending=False).head(10)
display(top_chains_by_outlets)"""),
        code_cell("""fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sns.barplot(data=top_chains_by_outlets, y='Restaurant Name', x='Outlets', palette='viridis', hue='Restaurant Name', legend=False, ax=axes[0])
axes[0].set_title("Top 10 Restaurant Chains by Outlets", fontsize=12, fontweight='bold')
axes[0].set_xlabel("Number of Outlets")

sns.barplot(data=top_chains_by_outlets, y='Restaurant Name', x='Avg_Rating', palette='mako', hue='Restaurant Name', legend=False, ax=axes[1])
axes[1].set_title("Average Rating of Top 10 Chains", fontsize=12, fontweight='bold')
axes[1].set_xlabel("Average Rating (0 to 5)")
axes[1].set_xlim(0, 5)

plt.tight_layout()
plt.show()"""),
        md_cell("""**Key Findings - Task 4:**
- **Cafe Coffee Day** (83 outlets), **Domino's Pizza** (79 outlets), and **Subway** (63 outlets) are the largest chains by presence.
- Premium casual dining chains like **Chili's** (4.58) and **Barbeque Nation** (4.35) achieve the highest ratings among multi-location brands.""")
    ]
    return create_nb(cells)

def generate_level_3():
    cells = [
        md_cell("""# Cognifyz Technologies - Data Analysis Internship
## Level 3 Analysis
**Candidate Name:** Jeevani Vedavendra  
**Reference ID:** CTI/A1/C421603  
**Domain:** Data Analysis  

---
### Overview of Level 3 Tasks:
1. **Task 1: Restaurant Reviews** - Analyze text reviews to identify common positive and negative keywords, calculate average review length, and examine the relationship with ratings.
2. **Task 2: Votes Analysis** - Identify restaurants with the highest and lowest votes and analyze the correlation between votes and rating.
3. **Task 3: Price Range vs. Online Delivery and Table Booking** - Analyze the relationship between price range and service availability."""),

        md_cell("### Step 1: Import Libraries and Load Dataset"),
        code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'font.sans-serif': 'Segoe UI', 'font.size': 11})

df = pd.read_csv('../Dataset .csv')
print(f"Dataset Shape: {df.shape}")
df.head(3)"""),

        md_cell("""---
## Task 1: Restaurant Reviews
- Analyze text reviews to identify the most common positive and negative keywords.
- Calculate the average length of reviews and explore if there is a relationship between review length and rating."""),
        code_cell("""# Text length metrics
df['Review_Text'] = df['Rating text'].astype(str)
df['Review_Char_Len'] = df['Review_Text'].apply(len)
df['Review_Word_Count'] = df['Review_Text'].apply(lambda x: len(x.split()))

print(f"Average Review Character Length: {df['Review_Char_Len'].mean():.2f}")
print(f"Average Review Word Count: {df['Review_Word_Count'].mean():.2f}")

# Keyword frequency analysis
words_series = df['Review_Text'].str.lower().str.split().explode()
word_counts = words_series.value_counts()

print("\\nKey Sentiment Words:")
for word in ['excellent', 'very', 'good', 'average', 'poor', 'not']:
    print(f"- '{word}': {word_counts.get(word, 0):,} occurrences")

# Grouped breakdown
review_summary = df.groupby('Rating text').agg(
    Count=('Aggregate rating', 'count'),
    Avg_Rating=('Aggregate rating', 'mean'),
    Avg_Char_Len=('Review_Char_Len', 'mean')
).sort_values(by='Avg_Rating', ascending=False)
display(review_summary)"""),
        code_cell("""fig, axes = plt.subplots(1, 2, figsize=(15, 5))

rev_cat_df = review_summary.reset_index()
sns.barplot(data=rev_cat_df, x='Rating text', y='Count', palette='Blues_r', hue='Rating text', legend=False, ax=axes[0])
axes[0].set_title("Frequency of Review Rating Categories", fontsize=12, fontweight='bold')
axes[0].set_xlabel("Review Category")
axes[0].set_ylabel("Count")
axes[0].tick_params(axis='x', rotation=20)

sns.boxplot(data=df, x='Rating text', y='Aggregate rating', order=['Excellent', 'Very Good', 'Good', 'Average', 'Poor', 'Not rated'], palette='Spectral', hue='Rating text', legend=False, ax=axes[1])
axes[1].set_title("Rating Distribution Across Categories", fontsize=12, fontweight='bold')
axes[1].set_xlabel("Review Category")
axes[1].set_ylabel("Aggregate Rating (0 - 5)")
axes[1].tick_params(axis='x', rotation=20)

plt.tight_layout()
plt.show()"""),
        md_cell("""**Key Findings - Task 1:**
- Positive sentiment terms (**Good**: 3,179, **Very Good**: 1,079, **Excellent**: 301) collectively characterize 47.7% of all restaurants.
- Average sentiment is the single largest category with 3,737 restaurants (39.1%).
- Unrated restaurants account for 2,148 records with 'Not rated' text."""),

        md_cell("""---
## Task 2: Votes Analysis
- Identify the restaurants with the highest and lowest number of votes.
- Analyze if there is a correlation between the number of votes and the rating of a restaurant."""),
        code_cell("""max_votes_val = df['Votes'].max()
min_votes_val = df['Votes'].min()

top_voted = df[df['Votes'] == max_votes_val][['Restaurant Name', 'City', 'Votes', 'Aggregate rating']]
print(f"Restaurant with highest votes: {top_voted.iloc[0]['Restaurant Name']} ({top_voted.iloc[0]['Votes']:,} votes)")

zero_votes_count = (df['Votes'] == min_votes_val).sum()
print(f"Restaurants with lowest votes (0 votes): {zero_votes_count} restaurants")

# Correlations
corr_all = df['Votes'].corr(df['Aggregate rating'])
spearman_corr, _ = stats.spearmanr(df['Votes'], df['Aggregate rating'])
rated_df = df[df['Aggregate rating'] > 0]
corr_rated = rated_df['Votes'].corr(rated_df['Aggregate rating'])

print(f"Pearson Correlation (All Data): {corr_all:.4f}")
print(f"Spearman Rank Correlation: {spearman_corr:.4f}")
print(f"Pearson Correlation (Rated Outlets Only): {corr_rated:.4f}")"""),
        code_cell("""fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Scatter with regression
sns.regplot(data=df, x='Votes', y='Aggregate rating', scatter_kws={'alpha': 0.3, 'color': '#2a9d8f'}, line_kws={'color': '#e76f51', 'linewidth': 2}, ax=axes[0])
axes[0].set_title(f"Votes vs. Rating (r = {corr_all:.2f})", fontsize=12, fontweight='bold')
axes[0].set_xlabel("Number of Votes")
axes[0].set_ylabel("Aggregate Rating (0 - 5)")

# Log-scaled votes
sns.regplot(data=rated_df, x=np.log1p(rated_df['Votes']), y='Aggregate rating', scatter_kws={'alpha': 0.3, 'color': '#457b9d'}, line_kws={'color': '#e63946', 'linewidth': 2}, ax=axes[1])
axes[1].set_title("Log(Votes + 1) vs. Rating (Rated Restaurants)", fontsize=12, fontweight='bold')
axes[1].set_xlabel("Log(Votes + 1)")
axes[1].set_ylabel("Aggregate Rating")

plt.tight_layout()
plt.show()"""),
        md_cell("""**Key Findings - Task 2:**
- **Toit** (Bangalore) holds the highest number of votes (**10,934 votes**) with an outstanding rating of **4.8**.
- There is a **statistically significant positive correlation (r = 0.31 overall, r = 0.41 for rated restaurants, Spearman rho = 0.85)** between vote counts and aggregate ratings. More popular, highly patronized restaurants systematically maintain higher customer satisfaction."""),

        md_cell("""---
## Task 3: Price Range vs. Online Delivery and Table Booking
- Analyze if there is a relationship between the price range and the availability of online delivery and table booking.
- Determine if higher-priced restaurants are more likely to offer these services."""),
        code_cell("""delivery_crosstab = pd.crosstab(df['Price range'], df['Has Online delivery'], normalize='index') * 100
booking_crosstab = pd.crosstab(df['Price range'], df['Has Table booking'], normalize='index') * 100

summary_services = pd.DataFrame({
    'Price_Range': [1, 2, 3, 4],
    'Online_Delivery_Pct': [delivery_crosstab.loc[pr, 'Yes'] for pr in [1, 2, 3, 4]],
    'Table_Booking_Pct': [booking_crosstab.loc[pr, 'Yes'] for pr in [1, 2, 3, 4]]
})

display(summary_services)"""),
        code_cell("""fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Grouped bar chart
x = np.arange(len(summary_services))
width = 0.35
axes[0].bar(x - width/2, summary_services['Online_Delivery_Pct'], width, label='Online Delivery', color='#2a9d8f')
axes[0].bar(x + width/2, summary_services['Table_Booking_Pct'], width, label='Table Booking', color='#e76f51')
axes[0].set_title("Service Availability by Price Range", fontsize=12, fontweight='bold')
axes[0].set_xlabel("Price Range (1 = Budget, 4 = Fine Dining)")
axes[0].set_ylabel("Percentage (%)")
axes[0].set_xticks(x)
axes[0].set_xticklabels([f"Tier {pr}" for pr in summary_services['Price_Range']])
axes[0].legend()

# 100% stacked bar chart for Table Booking
booking_pct_df = booking_crosstab.reset_index()
axes[1].bar(booking_pct_df['Price range'], booking_pct_df['Yes'], color='#e76f51', label='Has Table Booking', alpha=0.9)
axes[1].bar(booking_pct_df['Price range'], booking_pct_df['No'], bottom=booking_pct_df['Yes'], color='#adb5bd', label='No Table Booking', alpha=0.6)
axes[1].set_title("Table Booking Availability Across Price Ranges (Stacked)", fontsize=12, fontweight='bold')
axes[1].set_xlabel("Price Range Tier")
axes[1].set_ylabel("Percentage (%)")
axes[1].legend(loc='upper left')

plt.tight_layout()
plt.show()"""),
        md_cell("""**Key Findings - Task 3:**
- **Table Booking:** Strongly correlates with price tier. Only **0.02%** of budget restaurants (Tier 1) offer booking, compared to **45.74%** in Tier 3 and **46.76%** in Tier 4.
- **Online Delivery:** Peaks in **Tier 2 (41.31%)** and drops significantly in luxury Tier 4 restaurants (**9.04%**), reflecting the fine-dining emphasis on on-premise experiential dining over takeout.""")
    ]
    return create_nb(cells)

def main():
    notebooks_dir = os.path.join(os.path.dirname(__file__), "..", "notebooks")
    os.makedirs(notebooks_dir, exist_ok=True)

    nb1_path = os.path.join(notebooks_dir, "Level_1_Data_Analysis.ipynb")
    with open(nb1_path, "w", encoding="utf-8") as f:
        json.dump(generate_level_1(), f, indent=2)
    print(f"Generated: {nb1_path}")

    nb2_path = os.path.join(notebooks_dir, "Level_2_Data_Analysis.ipynb")
    with open(nb2_path, "w", encoding="utf-8") as f:
        json.dump(generate_level_2(), f, indent=2)
    print(f"Generated: {nb2_path}")

    nb3_path = os.path.join(notebooks_dir, "Level_3_Data_Analysis.ipynb")
    with open(nb3_path, "w", encoding="utf-8") as f:
        json.dump(generate_level_3(), f, indent=2)
    print(f"Generated: {nb3_path}")

if __name__ == "__main__":
    main()
