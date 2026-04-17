# 🐼 Python Analytics Classifier (Pandas ETL)

A lightweight, robust Python ETL (Extract, Transform, Load) script built with `pandas` and `re` (RegEx). This tool automates the categorization of raw, unstructured web analytics exports into standardized business dimensions for enterprise reporting.

## 🚀 The Problem & The Solution
**The Problem:** Enterprise web analytics platforms (like Google Analytics or Adobe Analytics) often export raw URLs and generic page types that are too granular or messy for executive dashboards. Manually mapping tens of thousands of rows to specific product lines, business units, or funnel stages in Excel is highly error-prone and time-consuming.

**The Solution:** This script ingests raw `.csv` exports, applies complex regex pattern-matching against URL paths and custom dimensions, and generates a normalized dataset with clean, high-level business categories (e.g., mapping a messy `/webapp/1234` URL to a clean `Landing Pages` category).

## 🧠 Core Engineering Skills Demonstrated
* **Data Manipulation with Pandas:** Leverages the `pandas` library for efficient parsing and transformation of large tabular datasets (`low_memory=False` optimization).
* **Advanced Pattern Matching (Regex):** Uses complex regular expressions to identify substrings, standardize localized URLs (e.g., `en_us.html`, `fr_fr.html`), and route data through intricate conditional logic trees.
* **ETL Pipeline Architecture:** Demonstrates a clear Extraction (reading CSVs), Transformation (applying business logic via `df.apply`), and Loading (dynamic file naming and exporting) workflow.
* **Data Normalization & Sanitization:** Cleans proprietary or broken URL strings and reconstructs absolute URLs from relative paths.

## 💻 How It Works

The script processes the raw data row-by-row and applies three distinct layers of categorization:
1. **Primary Category:** Sorts URLs into high-level site architecture buckets (e.g., *Homepage, Support, Corporate, PDP*).
2. **Secondary Category:** A deeper, product-specific routing logic that maps hardware, software, and services to specific business units.
3. **Normalized Page Type:** Cleans up messy analytics tracking variables into standardized UI templates.

## 🛠️ Setup & Execution

**1. Install Dependencies**
Ensure you have Python installed, then install the required `pandas` library:
```bash
pip install -r requirements.txt
