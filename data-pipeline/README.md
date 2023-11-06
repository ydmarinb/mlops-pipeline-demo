# Data Cleaning and Quality Assessment Repository

## Overview

This repository contains code for processing, cleaning, and assessing the quality of data files. The workflow is designed to take input files placed in the `raw_data` folder, check against a processing history to avoid duplicates, evaluate data quality, clean the data, re-assess the data quality, and save the improved data version to the `clean_data` folder.

## How It Works

1. **Input**: Place your raw data files (currently supporting `.csv` formats) into the `raw_data` folder.
2. **Validation**: The script checks the `historial.txt` file to determine if the data file has already been processed.
3. **Quality Assessment**: If the file is new, it evaluates the data quality before cleaning.
4. **Data Cleaning**: Performs cleaning operations on the data, such as standardizing addresses and correcting known data inconsistencies.
5. **Quality Re-assessment**: Evaluates the data quality post-cleaning.
6. **Output**: If the new data quality score is better, the cleaned data is saved to the `clean_data` folder. If not, it is saved with a prefix indicating lower quality.



