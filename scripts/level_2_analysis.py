"""
Cognifyz Technologies - Data Analysis Internship
Level 2 Analysis
Candidate: Jeevani Vedavendra (Ref: CTI/A1/C421603)

Tasks Covered:
- Task 1: Restaurant Ratings
- Task 2: Cuisine Combination
- Task 3: Geographic Analysis
- Task 4: Restaurant Chains
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'font.sans-serif': 'Segoe UI', 'font.size': 11})

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "level_2")
os.makedirs(OUTPUT_DIR, exist_ok=True)

DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "Dataset .csv")

def run_level_2():
    print("=" * 60)
    print("COGNIFYZ DATA ANALYSIS INTERNSHIP - LEVEL 2 ANALYSIS")
    print("Candidate: Jeevani Vedavendra | Ref: CTI/A1/C421603")
    print("=" * 60)

    df = pd.read_csv(DATASET_PATH)
    total_restaurants = len(df)
    print(f"Dataset successfully loaded. Total records: {total_restaurants}\n")

    # ----------------------------------------------------
    # TASK 1: RESTAURANT RATINGS
    # ----------------------------------------------------
    print("-" * 50)
    print("TASK 1: RESTAURANT RATINGS")
    print("-" * 50)
    
    # Rating distribution stats
    ratings = df['Aggregate rating']
    mean_rating = ratings.mean()
    median_rating = ratings.median()
    avg_votes = df['Votes'].mean()
    
    # Rating range bins (e.g. 0-1, 1-2, 2-3, 3-4, 4-5)
    bins = [0, 1.9, 2.9, 3.9, 4.9, 5.0]
    labels = ['0.0 - 1.9 (Poor/Unrated)', '2.0 - 2.9 (Average)', '3.0 - 3.9 (Good)', '4.0 - 4.9 (Very Good)', '5.0 (Perfect)']
    df['Rating_Range'] = pd.cut(df['Aggregate rating'], bins=bins, labels=labels, include_lowest=True)
    range_counts = df['Rating_Range'].value_counts().sort_index()
    most_common_range = range_counts.idxmax()
    
    print(f"Overall Mean Rating: {mean_rating:.2f}")
    print(f"Overall Median Rating: {median_rating:.2f}")
    print(f"Average number of votes per restaurant: {avg_votes:.2f} votes")
    print("\nRating Range Distribution:")
    for rng, count in range_counts.items():
        pct = (count / total_restaurants) * 100
        print(f" - {rng}: {count} restaurants ({pct:.2f}%)")
    print(f"\nMost common rating range: {most_common_range} with {range_counts[most_common_range]} restaurants")

    # Plot Restaurant Ratings
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Left: Histogram & KDE
    sns.histplot(df['Aggregate rating'], bins=20, kde=True, color='#2a9d8f', ax=axes[0])
    axes[0].axvline(mean_rating, color='#e76f51', linestyle='--', linewidth=2, label=f'Mean: {mean_rating:.2f}')
    axes[0].axvline(median_rating, color='#e9c46a', linestyle='-', linewidth=2, label=f'Median: {median_rating:.2f}')
    axes[0].set_title("Distribution of Aggregate Ratings", fontsize=12, fontweight='bold')
    axes[0].set_xlabel("Aggregate Rating (0.0 to 5.0)")
    axes[0].set_ylabel("Count")
    axes[0].legend()
    
    # Right: Categorical Rating Range Bar Chart
    range_df = range_counts.reset_index()
    range_df.columns = ['Rating_Range', 'Count']
    palette = ['#e63946' if r == most_common_range else '#457b9d' for r in range_df['Rating_Range']]
    sns.barplot(data=range_df, x='Rating_Range', y='Count', palette=palette, hue='Rating_Range', legend=False, ax=axes[1])
    axes[1].set_title("Most Common Rating Ranges (Highest Highlighted)", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("Rating Category")
    axes[1].set_ylabel("Number of Restaurants")
    axes[1].tick_params(axis='x', rotation=25)
    for i, v in enumerate(range_df['Count']):
        pct = (v / total_restaurants) * 100
        axes[1].text(i, v + 80, f"{v:,}\n({pct:.1f}%)", ha='center', va='bottom', fontsize=9, fontweight='semibold')
    axes[1].set_ylim(0, range_df['Count'].max() * 1.18)

    plt.tight_layout()
    fig_path = os.path.join(OUTPUT_DIR, "rating_distribution.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Chart saved: {fig_path}\n")

    # ----------------------------------------------------
    # TASK 2: CUISINE COMBINATIONS
    # ----------------------------------------------------
    print("-" * 50)
    print("TASK 2: CUISINE COMBINATIONS")
    print("-" * 50)
    
    # Multi-cuisine combinations
    cuisine_combos = df['Cuisines'].dropna()
    combo_counts = cuisine_combos.value_counts()
    
    # Most common cuisine combinations (with >1 cuisine listed)
    multi_combos = combo_counts[combo_counts.index.str.contains(',')].head(10)
    print("Top 5 most common cuisine combinations:")
    for combo, count in multi_combos.head(5).items():
        print(f" - {combo}: {count} restaurants")

    # Check if certain cuisine combinations tend to have higher ratings
    # Group by combination for combinations with at least 15 restaurants to ensure statistical validity
    combo_ratings = df.groupby('Cuisines').agg(
        Count=('Aggregate rating', 'count'),
        Avg_Rating=('Aggregate rating', 'mean'),
        Avg_Votes=('Votes', 'mean')
    ).reset_index()
    
    top_rated_combos = combo_ratings[combo_ratings['Count'] >= 15].sort_values(by='Avg_Rating', ascending=False).head(10)
    lowest_rated_combos = combo_ratings[combo_ratings['Count'] >= 15].sort_values(by='Avg_Rating', ascending=True).head(5)
    
    print("\nTop 5 highest rated cuisine combinations (min 15 restaurants):")
    for _, row in top_rated_combos.head(5).iterrows():
        print(f" - {row['Cuisines']}: {row['Avg_Rating']:.2f} avg rating ({row['Count']} restaurants)")

    # Plot Cuisine Combinations
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Left: Most frequent combinations
    most_freq_df = multi_combos.head(8).reset_index()
    most_freq_df.columns = ['Combination', 'Count']
    sns.barplot(data=most_freq_df, y='Combination', x='Count', palette='crest', hue='Combination', legend=False, ax=axes[0])
    axes[0].set_title("Most Common Multi-Cuisine Combinations", fontsize=12, fontweight='bold')
    axes[0].set_xlabel("Number of Restaurants")
    for i, v in enumerate(most_freq_df['Count']):
        axes[0].text(v + 5, i, f"{v:,}", va='center', fontsize=9)

    # Right: Highest rated combinations
    sns.barplot(data=top_rated_combos.head(8), y='Cuisines', x='Avg_Rating', palette='flare', hue='Cuisines', legend=False, ax=axes[1])
    axes[1].set_title("Cuisine Combinations with Highest Average Ratings (Min 15 Outlets)", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("Average Rating (0 to 5)")
    axes[1].set_xlim(0, 5)
    for i, v in enumerate(top_rated_combos.head(8)['Avg_Rating']):
        axes[1].text(v + 0.05, i, f"{v:.2f}", va='center', fontsize=9, fontweight='semibold')

    plt.tight_layout()
    fig_path = os.path.join(OUTPUT_DIR, "cuisine_combinations.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Chart saved: {fig_path}\n")

    # ----------------------------------------------------
    # TASK 3: GEOGRAPHIC ANALYSIS
    # ----------------------------------------------------
    print("-" * 50)
    print("TASK 3: GEOGRAPHIC ANALYSIS")
    print("-" * 50)
    
    # Filter valid coordinates (excluding 0, 0 which are default placeholders)
    geo_df = df[(df['Longitude'] != 0) & (df['Latitude'] != 0)].copy()
    print(f"Restaurants with valid coordinates: {len(geo_df)} / {len(df)}")
    
    # Delhi NCR cluster (majority of the dataset is in India - New Delhi, Gurgaon, Noida)
    ncr_df = geo_df[(geo_df['City'].isin(['New Delhi', 'Gurgaon', 'Noida', 'Faridabad', 'Ghaziabad']))]
    print(f"Restaurants in National Capital Region (NCR) cluster: {len(ncr_df)} ({len(ncr_df)/len(df)*100:.1f}%)")

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Left: Global Restaurant Scatter Plot
    scatter1 = axes[0].scatter(
        geo_df['Longitude'], 
        geo_df['Latitude'], 
        c=geo_df['Aggregate rating'], 
        cmap='Spectral_r', 
        alpha=0.6, 
        s=15, 
        edgecolor='none'
    )
    fig.colorbar(scatter1, ax=axes[0], label='Aggregate Rating')
    axes[0].set_title("Global Restaurant Distribution by Longitude & Latitude", fontsize=12, fontweight='bold')
    axes[0].set_xlabel("Longitude")
    axes[0].set_ylabel("Latitude")

    # Right: Major Cluster Focus (Delhi NCR Region)
    scatter2 = axes[1].scatter(
        ncr_df['Longitude'], 
        ncr_df['Latitude'], 
        c=ncr_df['Aggregate rating'], 
        cmap='Spectral_r', 
        alpha=0.5, 
        s=20, 
        edgecolor='none'
    )
    fig.colorbar(scatter2, ax=axes[1], label='Aggregate Rating')
    axes[1].set_title("Primary Geographic Cluster: Delhi NCR Region", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("Longitude")
    axes[1].set_ylabel("Latitude")

    plt.tight_layout()
    fig_path = os.path.join(OUTPUT_DIR, "geographic_distribution.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Chart saved: {fig_path}\n")

    # ----------------------------------------------------
    # TASK 4: RESTAURANT CHAINS
    # ----------------------------------------------------
    print("-" * 50)
    print("TASK 4: RESTAURANT CHAINS")
    print("-" * 50)
    
    # Restaurant chains: restaurants that have more than 1 outlet
    outlet_counts = df['Restaurant Name'].value_counts()
    chains = outlet_counts[outlet_counts > 1]
    total_chain_outlets = chains.sum()
    print(f"Number of unique restaurant chain brands (>1 location): {len(chains)}")
    print(f"Total outlets operated by chains: {total_chain_outlets} ({total_chain_outlets/total_restaurants*100:.2f}%)")

    # Chain performance analysis
    chain_names = chains.index.tolist()
    chain_df = df[df['Restaurant Name'].isin(chain_names)]
    
    chain_stats = chain_df.groupby('Restaurant Name').agg(
        Outlets=('Aggregate rating', 'count'),
        Avg_Rating=('Aggregate rating', 'mean'),
        Total_Votes=('Votes', 'sum'),
        Avg_Votes=('Votes', 'mean')
    ).reset_index()

    top_chains_by_outlets = chain_stats.sort_values(by='Outlets', ascending=False).head(10)
    print("\nTop 5 Restaurant Chains by Outlets:")
    for _, row in top_chains_by_outlets.head(5).iterrows():
        print(f" - {row['Restaurant Name']}: {row['Outlets']} outlets | Avg Rating: {row['Avg_Rating']:.2f} | Total Votes: {int(row['Total_Votes']):,}")

    # Top chains by rating (with at least 5 outlets)
    top_rated_chains = chain_stats[chain_stats['Outlets'] >= 5].sort_values(by='Avg_Rating', ascending=False).head(10)
    print("\nTop 5 Restaurant Chains by Average Rating (min 5 outlets):")
    for _, row in top_rated_chains.head(5).iterrows():
        print(f" - {row['Restaurant Name']}: {row['Avg_Rating']:.2f} avg rating ({row['Outlets']} outlets)")

    # Plot Restaurant Chains
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Left: Top chains by outlet count
    sns.barplot(data=top_chains_by_outlets, y='Restaurant Name', x='Outlets', palette='viridis', hue='Restaurant Name', legend=False, ax=axes[0])
    axes[0].set_title("Top 10 Restaurant Chains by Number of Outlets", fontsize=12, fontweight='bold')
    axes[0].set_xlabel("Number of Outlets")
    for i, v in enumerate(top_chains_by_outlets['Outlets']):
        axes[0].text(v + 1, i, f"{v}", va='center', fontsize=9, fontweight='semibold')

    # Right: Comparison of ratings for top chains
    sns.barplot(data=top_chains_by_outlets, y='Restaurant Name', x='Avg_Rating', palette='mako', hue='Restaurant Name', legend=False, ax=axes[1])
    axes[1].set_title("Average Rating of Top 10 Chains by Outlets", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("Average Rating (0 to 5)")
    axes[1].set_xlim(0, 5)
    for i, v in enumerate(top_chains_by_outlets['Avg_Rating']):
        axes[1].text(v + 0.05, i, f"{v:.2f}", va='center', fontsize=9, fontweight='semibold')

    plt.tight_layout()
    fig_path = os.path.join(OUTPUT_DIR, "restaurant_chains.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Chart saved: {fig_path}\n")

    print("=" * 60)
    print("LEVEL 2 ANALYSIS COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_level_2()
