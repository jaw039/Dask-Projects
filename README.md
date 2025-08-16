# DSC 102 — PA0 & PA1 Overview

This repository contains two course projects that work with large review and product datasets from the class data bundle. The goal is to practice **data wrangling at scale** using **Dask**: single-machine in PA0 and multi-machine in PA1.

## Contents

### PA0 — Build a Users Table (Single-Machine Dask)
- **Objective**: Aggregate the reviews dataset to create one row per user (`reviewerID`).
- **Tasks**:
  - Compute:
    - `number_products_rated`: Count of distinct items a user rated.
    - `avg_ratings`: Average star rating given by the user.
    - `reviewing_since`: The earliest review year for the user.
    - `helpful_votes`, `total_votes`: Totals parsed from the review "helpful" field.
  - Output: A JSON file with one record per user (line-delimited JSON).

### PA1 — Data Quality & Consistency Checks (Distributed Dask)
- **Objective**: Use both **reviews** and **products** datasets to answer the following questions:
  1. Percentage of missing values per column in **reviews**.
  2. Percentage of missing values per column in **products**.
  3. Pearson correlation between **price** and **rating** (after numeric cleanup).
  4. Summary statistics for **price** (mean, standard deviation, median, min, max).
  5. Product counts by **super-category** (first element of the nested `categories` list), sorted in descending order.
  6. Check for "dangling" references from `reviews.asin` that do **not** exist in `products.asin` (return 1 if yes, else 0).
  7. Check for "dangling" references in `products.related.*` IDs that do **not** exist in `products.asin` (return 1 if yes, else 0).
- **Output**: A small JSON file with answers for Q1–Q7.

## Technical Details

- **Tools**: Python, Pandas, and **Dask**.
- **Execution**:
  - PA0 runs on a single machine.
  - PA1 is designed for a small Dask cluster (e.g., the class AWS AMI with workers).
- **Data**: Large raw data files are **not** tracked in Git. Add them locally or read from S3 as per class instructions.

## Repository Structure

```
.
├── pa0/                  # PA0 code and notebooks
├── pa1/                  # PA1 code and notebooks
└── README.md
```

## Usage Instructions

- **For Viewing**: This repository serves as a course portfolio piece. Check the `pa0/` and `pa1/` folders for code/notebooks and the `results/` folder for produced JSON answers.
- **For Running**:
  1. Ensure the class data paths are set correctly (local files or S3).
  2. Run PA0 first, followed by PA1.
- **Note**: No private data is included in this repository.
