# Cognifyz Technologies - Data Analysis Internship Final Report

**Candidate Name:** Jeevani Vedavendra  
**Internship Reference ID:** CTI/A1/C421603  
**Domain:** Data Analysis  
**Company:** Cognifyz Technologies  
**Dataset:** Zomato Global Restaurant Dataset (9,551 records, 21 attributes)  

---

## Executive Summary

This report documents the end-to-end data analysis performed for the Cognifyz Technologies Data Analysis Internship Program. While the program guidelines allowed completion of any 2 levels, **all three levels (Level 1, Level 2, and Level 3)** encompassing **11 specific tasks** were executed.

The dataset contains global restaurant information spanning 15 countries and numerous cities, with dense coverage in metropolitan hubs. Through exploratory data analysis, geographic plotting, correlation testing, and cross-tabulation, we uncovered critical commercial patterns governing restaurant popularity, service offerings, customer satisfaction, and pricing strategies.

---

## 🎯 Project Context: What, Why & Problems Solved

### 1. What Problem Is It Solving?
- **High Industry Mortality Rates:** Over 60% of independent restaurants close in their first operational year due to poor location choices, menu over-complication, and mispriced offerings.
- **Service Channel Misallocation:** Restaurants often misallocate capital by forcing delivery on fine-dining formats or failing to deploy table reservations in upscale venues.
- **Aggregator Saturation:** Hyper-competition in major metropolitan hubs (such as Delhi NCR representing 79% of listings) demands data-backed differentiation to avoid severe price and margin wars.
- **Social Proof Dynamics:** Understanding how voter velocity and platform reviews systematically drive customer trust and discovery.

### 2. What Is Happening? (Analytical Pipeline)
- **Ingestion & Normalization:** Ingested 9,551 global restaurant records across 21 columns, cleaned coordinate anomalies, and split multi-label cuisine strings.
- **Descriptive Profiling (Level 1):** Measured cuisine volume leaders, analyzed city-level rating distributions, categorized 4 price tiers, and compared delivery adoption.
- **Diagnostic & Spatial Modeling (Level 2):** Modeled rating distribution, analyzed 510+ multi-cuisine combinations, mapped geospatial density clusters, and evaluated consistency across 734 chain brands.
- **Prescriptive Deep Dives (Level 3):** Analyzed review sentiment keywords, established Pearson and Spearman correlation between votes and ratings ($r=0.41, \rho=0.85$), and cross-tabulated price tier against service channel adoption.

### 3. Why Is It Happening? (Economic & Behavioral Drivers)
- **Mass Staple vs Experiential Dining:** Comfort cuisines (North Indian/Chinese) secure high-frequency volume, while specialty cuisines (Japanese/Thai) capture premium pricing and superior customer ratings.
- **Delivery Unit Economics:** Online delivery peaks at Tier 2 casual dining (41.3%) where ticket sizes comfortably absorb delivery platform commission structures (20–30%) without compromising food presentation.
- **Reservation Utility in Upscale Dining:** Table booking surges to ~47% in Tiers 3 & 4 because reservations are critical for luxury demand forecasting and personalized dining experiences.

---

## Level 1: Foundations of Restaurant Data

### Task 1: Top Cuisines
**Objective:** Determine the top three most common cuisines and calculate the percentage of restaurants serving each.

#### Findings & Statistics:
A single restaurant often serves multiple cuisines separated by commas. Parsing individual culinary offerings revealed:
1. **North Indian:** 3,960 occurrences (**41.46%** of all restaurants)
2. **Chinese:** 2,735 occurrences (**28.61%** of all restaurants)
3. **Fast Food:** 1,986 occurrences (**20.79%** of all restaurants)
4. **Mughlai:** 995 occurrences (10.42%)
5. **Italian:** 764 occurrences (8.00%)

#### Visualization:
The visualization `outputs/level_1/top_cuisines.png` illustrates the top 10 cuisines, emphasizing the top 3 market leaders.

---

### Task 2: City Analysis
**Objective:** Identify the city with the highest restaurant density, compute average ratings per city, and discover the highest-rated dining markets.

#### Findings & Statistics:
- **Highest Volume:** **New Delhi** accounts for **5,473 restaurants (57.30%)**, followed by Gurgaon (1,118) and Noida (1,080). Together, the Delhi NCR region represents over 80% of the dataset.
- **Highest Average Ratings (Overall):**
  - Inner City (4.90 avg rating, 2 restaurants)
  - Quezon City (4.80 avg rating, 20 restaurants)
  - Makati City (4.65 avg rating, 22 restaurants)
  - Pasig City (4.40 avg rating, 3 restaurants)
- Among major metropolitan markets with >= 10 outlets, **Quezon City (4.80)** and **Makati City (4.65)** in the Philippines achieve the highest customer satisfaction levels.

#### Visualization:
`outputs/level_1/city_analysis.png` presents a side-by-side comparison of city volume vs. average quality rating.

---

### Task 3: Price Range Distribution
**Objective:** Visualize price range distribution across restaurants and compute percentage representation.

#### Findings & Statistics:
| Price Range Tier | Meaning | Restaurant Count | Percentage Share |
|---|---|---|---|
| **Tier 1** | Budget / Value | 4,444 | 46.53% |
| **Tier 2** | Mid-Range Casual | 3,113 | 32.59% |
| **Tier 3** | Upscale Casual | 1,408 | 14.74% |
| **Tier 4** | Luxury / Fine Dining | 586 | 6.14% |

**Insight:** Over **79.1%** of all restaurants operate within budget to mid-range price points (Tiers 1 & 2), highlighting the mass-market orientation of the dining ecosystem.

#### Visualization:
`outputs/level_1/price_range_distribution.png` provides the categorical distribution and percentages.

---

### Task 4: Online Delivery Analysis
**Objective:** Determine the percentage of restaurants offering online delivery and compare ratings.

#### Findings & Statistics:
- **Online Delivery Available:** 2,451 restaurants (**25.66%**)
- **No Online Delivery:** 7,100 restaurants (**74.34%**)

#### Rating Comparison:
| Category | Mean Rating (All) | Median Rating | Std Dev | Mean Rating (Rated > 0 Only) |
|---|---|---|---|---|
| **No Delivery** | 2.47 | 3.1 | 1.64 | 3.47 |
| **Has Delivery** | 3.25 | 3.4 | 0.84 | 3.38 |

**Insight:** While the aggregate mean for delivery-enabled restaurants appears higher (3.25 vs 2.47), this is largely because 2,148 unrated (0.0 rating) outlets in the dataset almost exclusively lack online delivery. Among active, rated establishments, dine-in-only establishments score slightly higher (3.47 vs 3.38).

#### Visualization:
`outputs/level_1/online_delivery_comparison.png` displays both the proportional breakdown and boxplot distributions.

---

## Level 2: Advanced Patterns & Spatial Clustering

### Task 1: Restaurant Ratings
**Objective:** Analyze the distribution of aggregate ratings, determine the most common rating bracket, and compute average votes.

#### Findings & Statistics:
- **Overall Mean Rating:** 2.67 (Median: 3.20, Std: 1.52)
- **Average Votes per Restaurant:** 156.91 votes
- **Rating Range Breakdown:**
  - 0.0 - 1.9 (Poor / Not Rated): 2,151 restaurants (22.52%)
  - 2.0 - 2.9 (Average): 1,430 restaurants (14.97%)
  - **3.0 - 3.9 (Good) [Most Common]:** **4,590 restaurants (48.06%)**
  - 4.0 - 4.9 (Very Good): 1,380 restaurants (14.45%)

#### Visualization:
`outputs/level_2/rating_distribution.png` provides the KDE density curve and categorical histogram.

---

### Task 2: Cuisine Combinations
**Objective:** Identify the most common multi-cuisine combinations and evaluate if specific pairings achieve superior ratings.

#### Findings & Statistics:
- **Top 5 Multi-Cuisine Combinations:**
  1. North Indian, Chinese: 511 restaurants
  2. North Indian, Mughlai: 334 restaurants
  3. North Indian, Mughlai, Chinese: 197 restaurants
  4. Bakery, Desserts: 170 restaurants
  5. Pizza, Fast Food: 131 restaurants
- **Highest Rated Cuisines/Combinations (min 15 outlets):**
  - Specialized Indian Fine Dining: 4.25 avg rating
  - Thai: 4.10 avg rating
  - Japanese, Sushi: 4.04 avg rating
  - Pizza, Italian: 3.67 avg rating

**Insight:** Specialized cultural cuisines command significantly higher customer appreciation than generic multi-cuisine menus.

#### Visualization:
`outputs/level_2/cuisine_combinations.png` compares combination counts with their average ratings.

---

### Task 3: Geographic Analysis
**Objective:** Plot restaurant coordinates and analyze spatial clustering.

#### Findings & Statistics:
- Valid coordinate entries: 9,052 out of 9,551 records.
- **Primary Spatial Cluster:** The Delhi National Capital Region (NCR) contains **7,550 restaurants (79.0%)**.
- Secondary clusters span major global hubs including the UAE (Dubai, Abu Dhabi), United States, Singapore, the Philippines, and South Africa.

#### Visualization:
`outputs/level_2/geographic_distribution.png` visualizes both global coordinates and a zoomed spatial heatmap of the NCR cluster.

---

### Task 4: Restaurant Chains
**Objective:** Identify multi-outlet restaurant chains and examine their performance and vote popularity.

#### Findings & Statistics:
- **Chain Outlets Identified:** 734 chain brands operating **2,839 outlets (29.72% of total)**.
- **Top 5 Chains by Branch Count:**
  1. **Cafe Coffee Day:** 83 outlets | Mean Rating: 2.42 | 2,428 votes
  2. **Domino's Pizza:** 79 outlets | Mean Rating: 2.74 | 6,643 votes
  3. **Subway:** 63 outlets | Mean Rating: 2.91 | 6,124 votes
  4. **Green Chick Chop:** 51 outlets | Mean Rating: 2.67 | 964 votes
  5. **McDonald's:** 48 outlets | Mean Rating: 3.34 | 5,291 votes
- **Top Rated Chains (min 5 locations):**
  - **Chili's:** 4.58 avg rating (5 outlets)
  - **Farzi Cafe:** 4.37 avg rating (6 outlets)
  - **Barbeque Nation:** 4.35 avg rating (26 outlets)
  - **Punjab Grill:** 4.34 avg rating (5 outlets)

#### Visualization:
`outputs/level_2/restaurant_chains.png` contrasts chain network size against customer ratings.

---

## Level 3: Deep Dives & Statistical Modeling

### Task 1: Restaurant Reviews
**Objective:** Analyze review text keywords, evaluate length metrics, and examine the relationship between review length and rating.

#### Findings & Statistics:
- Text field: `Rating text` ("Excellent", "Very Good", "Good", "Average", "Poor", "Not rated")
- **Average Character Length:** 7.02 characters (Average Word Count: 1.34 words)
- **Keyword Distribution:**
  - Positive: "Good" (3,179), "Very Good" (1,079), "Excellent" (301)
  - Neutral / Critical: "Average" (3,737), "Poor" (186), "Not rated" (2,148)
- Correlation between Character Length and Rating is -0.48 (due to the 9-character label "Not rated" representing 0.0 rating). Within rated categories, character and descriptor complexity strongly align with sentiment tiers.

#### Visualization:
`outputs/level_3/review_text_analysis.png` presents category counts and rating boxplots.

---

### Task 2: Votes Analysis
**Objective:** Identify outlets with extreme vote counts and model the statistical correlation between votes and rating.

#### Findings & Statistics:
- **Highest Votes:** **Toit** (Bangalore) with **10,934 votes** and an Aggregate Rating of **4.8**.
- **Lowest Votes:** 1,094 restaurants recorded 0 votes (all corresponding to unrated 0.0 ratings).
- **Statistical Correlation:**
  - Pearson correlation across full dataset: **r = 0.3137** (p < 0.001)
  - Pearson correlation among rated restaurants: **r = 0.4090** (p < 0.001)
  - Spearman rank correlation: **rho = 0.8462** (p < 0.001)

**Insight:** Popularity and customer rating exhibit a strong monotonic relationship. Outlets that provide superior dining experiences generate viral word-of-mouth and customer engagement.

#### Visualization:
`outputs/level_3/votes_vs_rating.png` shows regression fits for linear and log-transformed vote counts.

---

### Task 3: Price Range vs. Online Delivery & Table Booking
**Objective:** Analyze service availability across price tiers and determine if premium restaurants are more likely to offer these features.

#### Findings & Statistics:
| Price Range | Online Delivery Availability (%) | Table Booking Availability (%) |
|---|---|---|
| **Tier 1 (Budget)** | 15.77% | **0.02%** |
| **Tier 2 (Mid-range)** | **41.31%** | 7.68% |
| **Tier 3 (Upscale)** | 29.19% | **45.74%** |
| **Tier 4 (Luxury)** | 9.04% | **46.76%** |

#### Strategic Inferences:
1. **Table Booking:** Strictly concentrated in Tier 3 and Tier 4 restaurants (~46% availability), virtually absent in budget dining (0.02%).
2. **Online Delivery:** Follows an inverted U-curve. It peaks in Tier 2 casual dining (41.31%) where delivery logistics are most commercially viable, and drops sharply to 9.04% in Tier 4 luxury dining where ambiance and experiential service are paramount.

#### Visualization:
`outputs/level_3/price_vs_delivery_booking.png` provides grouped and 100% stacked bar visualizations.

---

## Conclusion & Business Recommendations

1. **Strategic Menu Formulation:** While North Indian and Chinese cuisines provide reliable mass-market volume, specialty cuisine segments (Thai, Japanese, Italian) achieve superior consumer ratings and command higher price margins.
2. **Delivery Optimization:** Mid-tier restaurants (Tier 2) are the sweet spot for online delivery partnerships. Quick-service and casual dining formats can maximize revenue by streamlining delivery dispatch.
3. **Table Booking Deployment:** Upscale and luxury operators should prioritize seamless digital reservation systems, as nearly 50% of high-end patrons expect table reservations.
4. **Brand Quality Management for Chains:** Rapid geographic expansion without stringent quality control degrades customer ratings, as evidenced by lower average scores among mass-market fast food chains compared to curated premium dining chains.

---

*Report prepared and submitted by:*  
**Jeevani Vedavendra**  
Internship Ref: CTI/A1/C421603  
Cognifyz Technologies Data Analysis Internship
