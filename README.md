# DatasetOutput Module

This module provides tools for extracting and processing GDP and Output Gap data for various countries, focusing on the Euro Zone and the US.

## Features:
1. **Imports:** 
   - Essential libraries like `pandas`, and `numpy``.
   - `Aux` class from `src.aux` module for auxiliary functionalities.

2. **DatasetOutput Class:**
   - Initializes with a base year set to 2015.
   - Provides methods for:
     - Changing the base year.
     - Fetching Eurozone GDP data.
     - Fetching US GDP data.
     - Constructing Eurozone Output Gap data.
     - Constructing US Output Gap data.
     - Fetching Eurozone Potential GDP data.
     - Fetching US Potential GDP data.
     - General GDP data fetching based on country.
     - General Potential GDP data fetching based on country.
     - General Output Gap data fetching based on country.

3. **Functionalities:**
   - Allows fetching of real or nominal GDP.
   - Utilises FRED API for data extraction.
   - Provides options for annual or quarterly data.
   - Supports a selection of countries including Spain, France, Germany, Italy, and the Euro Zone.

## How to Use:

1. Create an instance of the `DatasetOutput` class.
2. Utilise the various methods provided to fetch and process the data you need.

