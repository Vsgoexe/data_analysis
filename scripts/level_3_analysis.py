"""
Cognifyz Technologies - Data Analysis Internship
Level 3 Analysis
Candidate: Jeevani Vedavendra (Ref: CTI/A1/C421603)

Tasks Covered:
- Task 1: Restaurant Reviews
- Task 2: Votes Analysis
- Task 3: Price Range vs. Online Delivery and Table Booking
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'font.sans-serif': 'Segoe UI', 'font.size': 11})

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "level_3")
os.makedirs(OUTPUT_DIR, exist_ok=True)

DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "Dataset .csv")

def run_level_3():
    print("=" * 60)
    print("COGNIFYZ DATA ANALYSIS INTERNSHIP - LEVEL 3 ANALYSIS")
    print("Candidate: Jeevani Vedavendra | Ref: CTI/A1/C421603")
    print("=" * 60)

    df = pd.read_csv(DATASET_PATH)
    total_restaurants = len(df)
    print(f"Dataset successfully loaded. Total records: {total_restaurants}\n")

    # ----------------------------------------------------
    # TASK 1: RESTAURANT REVIEWS
    # ----------------------------------------------------
    print("-" * 50)
    print("TASK 1: RESTAURANT REVIEWS ANALYSIS")
    print("-" * 50)
    
    # Review text analysis on 'Rating text'
    # Calculate word length and character length
    df['Review_Text'] = df['Rating text'].astype(str)
    df['Review_Char_Len'] = df['Review_Text'].apply(len)
    df['Review_Word_Count'] = df['Review_Text'].apply(lambda x: len(x.split()))
    
    avg_char_len = df['Review_Char_Len'].mean()
    avg_word_count = df['Review_Word_Count'].mean()
    
    print(f"Average review text character length: {avg_char_len:.2f} characters")
    print(f"Average review text word count: {avg_word_count:.2f} words")
    
    # Positive and negative keywords analysis
    # Tokenize words in Rating text
    words_series = df['Review_Text'].str.lower().str.split().explode()
    word_counts = words_series.value_counts()
    
    positive_keywords = ['excellent', 'very', 'good']
    negative_keywords = ['poor', 'average', 'not']
    
    print("\nKeywords frequency in Review Rating Text:")
    print("Positive Keywords:")
    for kw in positive_keywords:
        print(f" - '{kw}': {word_counts.get(kw, 0):,} occurrences")
        
    print("Negative / Critical Keywords:")
    for kw in negative_keywords:
        print(f" - '{kw}': {word_counts.get(kw, 0):,} occurrences")

    # Relationship between review length and rating
    corr_char_rating = df['Review_Char_Len'].corr(df['Aggregate rating'])
    corr_word_rating = df['Review_Word_Count'].corr(df['Aggregate rating'])
    print(f"\nCorrelation between Review Character Length and Rating: {corr_char_rating:.4f}")
    print(f"Correlation between Review Word Count and Rating: {corr_word_rating:.4f}")

    # Breakdown by rating category
    review_by_rating = df.groupby('Rating text').agg(
        Count=('Aggregate rating', 'count'),
        Avg_Rating=('Aggregate rating', 'mean'),
        Avg_Char_Len=('Review_Char_Len', 'mean')
    ).sort_values(by='Avg_Rating', ascending=False)
    print("\nReview metrics grouped by Rating Category:")
    print(review_by_rating.to_string())

    # Plot Review Analysis
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Left: Distribution of review text categories
    rev_cat_df = review_by_rating.reset_index()
    palette = ['#2a9d8f', '#48cae4', '#52b788', '#f4a261', '#e76f51', '#adb5bd']
    sns.barplot(data=rev_cat_df, x='Rating text', y='Count', palette='Blues_r', hue='Rating text', legend=False, ax=axes[0])
    axes[0].set_title("Frequency of Rating Text Categories", fontsize=12, fontweight='bold')
    axes[0].set_xlabel("Rating Review Category")
    axes[0].set_ylabel("Count")
    axes[0].tick_params(axis='x', rotation=20)
    for i, v in enumerate(rev_cat_df['Count']):
        axes[0].text(i, v + 50, f"{v:,}", ha='center', fontsize=9, fontweight='semibold')
    axes[0].set_ylim(0, rev_cat_df['Count'].max() * 1.15)

    # Right: Average Rating vs Review Character Length
    sns.boxplot(data=df, x='Rating text', y='Aggregate rating', order=['Excellent', 'Very Good', 'Good', 'Average', 'Poor', 'Not rated'], palette='Spectral', hue='Rating text', legend=False, ax=axes[1])
    axes[1].set_title("Aggregate Rating Distribution Across Review Categories", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("Review Text Category")
    axes[1].set_ylabel("Aggregate Rating (0 - 5)")
    axes[1].tick_params(axis='x', rotation=20)

    plt.tight_layout()
    fig_path = os.path.join(OUTPUT_DIR, "review_text_analysis.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Chart saved: {fig_path}\n")

    # ----------------------------------------------------
    # TASK 2: VOTES ANALYSIS
    # ----------------------------------------------------
    print("-" * 50)
    print("TASK 2: VOTES ANALYSIS")
    print("-" * 50)
    
    max_votes_val = df['Votes'].max()
    min_votes_val = df['Votes'].min()
    
    max_vote_restaurants = df[df['Votes'] == max_votes_val]
    min_vote_restaurants = df[df['Votes'] == min_votes_val]
    
    print(f"Maximum votes received: {max_votes_val:,}")
    print(f"Restaurant(s) with highest votes:")
    for _, r in max_vote_restaurants.iterrows():
        print(f" - {r['Restaurant Name']} in {r['City']} ({r['Votes']:,} votes, Rating: {r['Aggregate rating']})")

    print(f"\nMinimum votes received: {min_votes_val}")
    print(f"Number of restaurants with lowest votes (0 votes): {len(min_vote_restaurants)} restaurants")
    print("Sample restaurants with 0 votes:")
    for _, r in min_vote_restaurants.head(3).iterrows():
        print(f" - {r['Restaurant Name']} in {r['City']} (Rating: {r['Aggregate rating']})")

    # Correlation between votes and rating
    corr_votes_rating = df['Votes'].corr(df['Aggregate rating'])
    spearman_corr, _ = stats.spearmanr(df['Votes'], df['Aggregate rating'])
    print(f"\nPearson correlation between Votes and Rating: {corr_votes_rating:.4f}")
    print(f"Spearman rank correlation between Votes and Rating: {spearman_corr:.4f}")

    # Correlation excluding unrated 0.0 restaurants
    rated_df = df[df['Aggregate rating'] > 0]
    corr_rated_only = rated_df['Votes'].corr(rated_df['Aggregate rating'])
    print(f"Pearson correlation for rated restaurants (Rating > 0): {corr_rated_only:.4f}")

    # Plot Votes vs Rating
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Left: Scatter plot with regression line (All restaurants)
    sns.regplot(data=df, x='Votes', y='Aggregate rating', scatter_kws={'alpha': 0.3, 'color': '#2a9d8f'}, line_kws={'color': '#e76f51', 'linewidth': 2}, ax=axes[0])
    axes[0].set_title(f"Votes vs. Aggregate Rating (All Data, r = {corr_votes_rating:.2f})", fontsize=12, fontweight='bold')
    axes[0].set_xlabel("Number of Votes")
    axes[0].set_ylabel("Aggregate Rating (0 - 5)")

    # Right: Scatter plot with log-scaled votes for rated restaurants
    sns.regplot(data=rated_df, x=np.log1p(rated_df['Votes']), y='Aggregate rating', scatter_kws={'alpha': 0.3, 'color': '#457b9d'}, line_kws={'color': '#e63946', 'linewidth': 2}, ax=axes[1])
    axes[1].set_title("Log(Votes + 1) vs. Aggregate Rating (Rated Restaurants)", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("Log(Votes + 1)")
    axes[1].set_ylabel("Aggregate Rating")

    plt.tight_layout()
    fig_path = os.path.join(OUTPUT_DIR, "votes_vs_rating.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Chart saved: {fig_path}\n")

    # ----------------------------------------------------
    # TASK 3: PRICE RANGE VS. ONLINE DELIVERY AND TABLE BOOKING
    # ----------------------------------------------------
    print("-" * 50)
    print("TASK 3: PRICE RANGE VS. ONLINE DELIVERY & TABLE BOOKING")
    print("-" * 50)
    
    # Cross-tabulation normalized by price range row percentages
    delivery_crosstab = pd.crosstab(df['Price range'], df['Has Online delivery'], normalize='index') * 100
    booking_crosstab = pd.crosstab(df['Price range'], df['Has Table booking'], normalize='index') * 100
    
    print("Percentage offering Online Delivery by Price Range:")
    print(delivery_crosstab.round(2).to_string())
    
    print("\nPercentage offering Table Booking by Price Range:")
    print(booking_crosstab.round(2).to_string())

    # Combined summary dataframe
    summary_services = pd.DataFrame({
        'Price_Range': [1, 2, 3, 4],
        'Online_Delivery_Pct': [delivery_crosstab.loc[pr, 'Yes'] for pr in [1, 2, 3, 4]],
        'Table_Booking_Pct': [booking_crosstab.loc[pr, 'Yes'] for pr in [1, 2, 3, 4]]
    })
    print("\nSummary Comparison across Price Ranges:")
    print(summary_services.to_string(index=False))

    # Plot Price Range vs Services
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Left: Grouped Bar Chart of Services Availability
    x = np.arange(len(summary_services))
    width = 0.35
    axes[0].bar(x - width/2, summary_services['Online_Delivery_Pct'], width, label='Online Delivery', color='#2a9d8f')
    axes[0].bar(x + width/2, summary_services['Table_Booking_Pct'], width, label='Table Booking', color='#e76f51')
    axes[0].set_title("Service Availability by Price Range", fontsize=12, fontweight='bold')
    axes[0].set_xlabel("Price Range (1 = Lowest, 4 = Highest)")
    axes[0].set_ylabel("Percentage of Restaurants Offering Service (%)")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels([f"Tier {pr}" for pr in summary_services['Price_Range']])
    axes[0].legend()
    axes[0].set_ylim(0, 60)
    for i in range(len(summary_services)):
        axes[0].text(i - width/2, summary_services['Online_Delivery_Pct'][i] + 1, f"{summary_services['Online_Delivery_Pct'][i]:.1f}%", ha='center', fontsize=9, fontweight='semibold')
        axes[0].text(i + width/2, summary_services['Table_Booking_Pct'][i] + 1, f"{summary_services['Table_Booking_Pct'][i]:.1f}%", ha='center', fontsize=9, fontweight='semibold')

    # Right: Stacked view for Table Booking across Price Ranges
    booking_pct_df = booking_crosstab.reset_index()
    axes[1].bar(booking_pct_df['Price range'], booking_pct_df['Yes'], color='#e76f51', label='Has Table Booking', alpha=0.9)
    axes[1].bar(booking_pct_df['Price range'], booking_pct_df['No'], bottom=booking_pct_df['Yes'], color='#adb5bd', label='No Table Booking', alpha=0.6)
    axes[1].set_title("Table Booking Availability Across Price Ranges (100% Stacked)", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("Price Range Tier")
    axes[1].set_ylabel("Percentage (%)")
    axes[1].legend(loc='upper left')
    for i, row in booking_pct_df.iterrows():
        axes[1].text(row['Price range'], row['Yes'] / 2, f"{row['Yes']:.1f}%", ha='center', va='center', color='white', fontweight='bold', fontsize=10)

    plt.tight_layout()
    fig_path = os.path.join(OUTPUT_DIR, "price_vs_delivery_booking.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Chart saved: {fig_path}\n")

    print("=" * 60)
    print("LEVEL 3 ANALYSIS COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_level_3()
