"""
Cognifyz Technologies - Data Analysis Internship
Level 1 Analysis
Candidate: Jeevani Vedavendra (Ref: CTI/A1/C421603)

Tasks Covered:
- Task 1: Top Cuisines
- Task 2: City Analysis
- Task 3: Price Range Distribution
- Task 4: Online Delivery
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Set style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'font.sans-serif': 'Segoe UI', 'font.size': 11})

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "level_1")
os.makedirs(OUTPUT_DIR, exist_ok=True)

DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "Dataset .csv")

def run_level_1():
    print("=" * 60)
    print("COGNIFYZ DATA ANALYSIS INTERNSHIP - LEVEL 1 ANALYSIS")
    print("Candidate: Jeevani Vedavendra | Ref: CTI/A1/C421603")
    print("=" * 60)

    df = pd.read_csv(DATASET_PATH)
    total_restaurants = len(df)
    print(f"Dataset successfully loaded. Total records: {total_restaurants}\n")

    # ----------------------------------------------------
    # TASK 1: TOP CUISINES
    # ----------------------------------------------------
    print("-" * 50)
    print("TASK 1: TOP CUISINES")
    print("-" * 50)
    
    # Split cuisines since multiple cuisines can be comma-separated
    cuisines_series = df['Cuisines'].dropna().apply(lambda x: [c.strip() for c in str(x).split(',')]).explode()
    cuisine_counts = cuisines_series.value_counts()
    top_3_cuisines = cuisine_counts.head(3)
    
    # Also calculate percentage of restaurants serving each of the top cuisines
    print("Top 3 most common cuisines:")
    top_cuisines_data = []
    for cuisine, count in top_3_cuisines.items():
        # Check in how many restaurants this cuisine appears
        pct = (df['Cuisines'].dropna().apply(lambda x: cuisine in [c.strip() for c in str(x).split(',')]).sum() / total_restaurants) * 100
        top_cuisines_data.append({'Cuisine': cuisine, 'Count': count, 'Percentage': pct})
        print(f" - {cuisine}: {count} occurrences ({pct:.2f}% of restaurants)")
    
    # Plot Top Cuisines
    fig, ax = plt.subplots(figsize=(8, 5))
    top_10 = cuisine_counts.head(10).reset_index()
    top_10.columns = ['Cuisine', 'Count']
    palette = ['#e63946' if i < 3 else '#457b9d' for i in range(len(top_10))]
    sns.barplot(data=top_10, x='Count', y='Cuisine', palette=palette, ax=ax)
    ax.set_title("Top 10 Most Common Cuisines (Top 3 Highlighted in Red)", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Number of Restaurants")
    ax.set_ylabel("Cuisine")
    for i, v in enumerate(top_10['Count']):
        pct = (v / total_restaurants) * 100
        ax.text(v + 30, i, f"{v:,} ({pct:.1f}%)", va='center', fontsize=10, fontweight='semibold')
    ax.set_xlim(0, top_10['Count'].max() * 1.15)
    plt.tight_layout()
    fig_path = os.path.join(OUTPUT_DIR, "top_cuisines.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Chart saved: {fig_path}\n")

    # ----------------------------------------------------
    # TASK 2: CITY ANALYSIS
    # ----------------------------------------------------
    print("-" * 50)
    print("TASK 2: CITY ANALYSIS")
    print("-" * 50)
    
    city_counts = df['City'].value_counts()
    top_city = city_counts.index[0]
    top_city_count = city_counts.iloc[0]
    top_city_pct = (top_city_count / total_restaurants) * 100
    print(f"City with the highest number of restaurants: {top_city} with {top_city_count} restaurants ({top_city_pct:.2f}%)")

    # Average rating for restaurants in each city
    city_avg_rating = df.groupby('City')['Aggregate rating'].agg(['count', 'mean']).reset_index()
    city_avg_rating.columns = ['City', 'Restaurant_Count', 'Average_Rating']
    
    # City with highest average rating (filtering for cities with >= 5 restaurants for statistical relevance, and absolute highest)
    highest_avg_city_all = city_avg_rating.sort_values(by='Average_Rating', ascending=False).iloc[0]
    print(f"City with the highest average rating (overall): {highest_avg_city_all['City']} ({highest_avg_city_all['Average_Rating']:.2f} rating, {highest_avg_city_all['Restaurant_Count']} restaurants)")

    # Plot City Analysis
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Left: Top 10 cities by restaurant count
    top_10_cities = city_counts.head(10).reset_index()
    top_10_cities.columns = ['City', 'Count']
    sns.barplot(data=top_10_cities, y='City', x='Count', palette='Blues_r', ax=axes[0])
    axes[0].set_title("Top 10 Cities by Restaurant Count", fontsize=12, fontweight='bold')
    axes[0].set_xlabel("Number of Restaurants")
    for i, v in enumerate(top_10_cities['Count']):
        axes[0].text(v + 50, i, f"{v:,}", va='center', fontsize=9)
        
    # Right: Top 10 cities by average rating (with min 10 restaurants to show significant hubs)
    min_restaurants = 10
    top_rated_cities = city_avg_rating[city_avg_rating['Restaurant_Count'] >= min_restaurants].sort_values(by='Average_Rating', ascending=False).head(10)
    sns.barplot(data=top_rated_cities, y='City', x='Average_Rating', palette='YlGnBu_r', ax=axes[1])
    axes[1].set_title(f"Top 10 Cities by Average Rating (Min {min_restaurants} Restaurants)", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("Average Aggregate Rating (0 to 5)")
    axes[1].set_xlim(0, 5)
    for i, v in enumerate(top_rated_cities['Average_Rating']):
        axes[1].text(v + 0.05, i, f"{v:.2f}", va='center', fontsize=9, fontweight='semibold')

    plt.tight_layout()
    fig_path = os.path.join(OUTPUT_DIR, "city_analysis.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Chart saved: {fig_path}\n")

    # ----------------------------------------------------
    # TASK 3: PRICE RANGE DISTRIBUTION
    # ----------------------------------------------------
    print("-" * 50)
    print("TASK 3: PRICE RANGE DISTRIBUTION")
    print("-" * 50)
    
    price_counts = df['Price range'].value_counts().sort_index()
    price_pct = (price_counts / total_restaurants) * 100
    
    print("Price range distribution:")
    for pr, count in price_counts.items():
        print(f" - Price Range {pr}: {count} restaurants ({price_pct[pr]:.2f}%)")

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = sns.barplot(x=price_counts.index, y=price_counts.values, palette='viridis', ax=ax)
    ax.set_title("Distribution of Price Ranges Among Restaurants", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Price Range (1 = Budget, 4 = Fine Dining)", fontsize=11)
    ax.set_ylabel("Number of Restaurants", fontsize=11)
    for i, (val, pct) in enumerate(zip(price_counts.values, price_pct.values)):
        ax.text(i, val + 60, f"{val:,}\n({pct:.1f}%)", ha='center', va='bottom', fontsize=10, fontweight='semibold')
    ax.set_ylim(0, price_counts.max() * 1.18)
    plt.tight_layout()
    fig_path = os.path.join(OUTPUT_DIR, "price_range_distribution.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Chart saved: {fig_path}\n")

    # ----------------------------------------------------
    # TASK 4: ONLINE DELIVERY
    # ----------------------------------------------------
    print("-" * 50)
    print("TASK 4: ONLINE DELIVERY ANALYSIS")
    print("-" * 50)
    
    delivery_counts = df['Has Online delivery'].value_counts()
    delivery_pct = (delivery_counts / total_restaurants) * 100
    yes_pct = delivery_pct.get('Yes', 0.0)
    no_pct = delivery_pct.get('No', 0.0)
    
    print(f"Percentage offering Online Delivery: {yes_pct:.2f}% ({delivery_counts.get('Yes', 0)} restaurants)")
    print(f"Percentage NOT offering Online Delivery: {no_pct:.2f}% ({delivery_counts.get('No', 0)} restaurants)")

    # Compare average ratings
    rating_by_delivery = df.groupby('Has Online delivery')['Aggregate rating'].agg(['count', 'mean', 'median', 'std']).reset_index()
    print("\nRating comparison by online delivery availability:")
    print(rating_by_delivery.to_string(index=False))

    # Also compare ratings excluding unrated restaurants (Aggregate rating > 0)
    rated_df = df[df['Aggregate rating'] > 0]
    rating_by_delivery_rated = rated_df.groupby('Has Online delivery')['Aggregate rating'].agg(['count', 'mean', 'median', 'std']).reset_index()
    print("\nRating comparison (excluding 0.0 unrated restaurants):")
    print(rating_by_delivery_rated.to_string(index=False))

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Pie chart of online delivery
    axes[0].pie(
        delivery_counts.values, 
        labels=[f"No Online Delivery\n({no_pct:.1f}%)", f"Offers Online Delivery\n({yes_pct:.1f}%)"],
        autopct='%1.1f%%',
        colors=['#e76f51', '#2a9d8f'],
        startangle=140,
        explode=(0, 0.08),
        shadow=True,
        textprops={'fontsize': 11, 'fontweight': 'semibold'}
    )
    axes[0].set_title("Proportion of Restaurants Offering Online Delivery", fontsize=12, fontweight='bold')

    # Box plot comparing ratings
    sns.boxplot(data=df, x='Has Online delivery', y='Aggregate rating', palette=['#e76f51', '#2a9d8f'], ax=axes[1], width=0.4)
    axes[1].set_title("Rating Comparison: Online Delivery vs No Delivery", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("Has Online Delivery", fontsize=11)
    axes[1].set_ylabel("Aggregate Rating (0 - 5)", fontsize=11)
    # Add means as text
    for i, has_del in enumerate(['No', 'Yes']):
        mean_val = rating_by_delivery[rating_by_delivery['Has Online delivery'] == has_del]['mean'].values[0]
        axes[1].scatter(i, mean_val, color='yellow', s=60, zorder=5, edgecolor='black')
        axes[1].text(i + 0.15, mean_val, f"Mean: {mean_val:.2f}", fontweight='bold', fontsize=10, va='center')

    plt.tight_layout()
    fig_path = os.path.join(OUTPUT_DIR, "online_delivery_comparison.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Chart saved: {fig_path}\n")

    print("=" * 60)
    print("LEVEL 1 ANALYSIS COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_level_1()
