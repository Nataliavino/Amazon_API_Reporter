Brief Description:
This project is a set of Python scripts designed to automate the retrieval, processing, and analysis of data from Amazon Advertising and Amazon Seller Center APIs. The scripts cover tasks such as generating reports, downloading data, and updating Google Sheets with relevant information.

Key Features:

Amazon Advertising Report:

Fetches advertising data using the Amazon Advertising API.
Downloads reports, processes them, and stores the information locally.
Integrates with Google Sheets to update daily and 30-day advertising metrics.
Amazon Seller Report:

Retrieves sales and traffic reports from the Amazon Seller Center API.
Manages report generation, download, and processing for Seller Center data.
Updates Google Sheets with daily sales and traffic metrics and ASIN-specific information.
Google Sheets Integration:

Utilizes the Google Sheets API for seamless interaction with Google Sheets.
Modular functions for adding rows to Google Sheets for different types of data.
Supports deletion of rows based on specified criteria.
File Structure:

main.py: The main script orchestrating the execution of advertising and seller reports.
amazon_seller.py, amazon_seller_token.py: Modules for handling Amazon Seller Center reports and access tokens.
get_report.py, get_token.py: Modules for managing Amazon Advertising reports and access tokens.
google_sheet.py: Module for interacting with Google Sheets and updating data.
