-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
1: Disease Variants Data Scraper
This script scrapes disease variant information from the DisGeNET database based on UMLS CUI IDs provided in a file. It processes the data and exports it to CSV files.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Key Features:
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Retrieves the total number of pages for a disease query.
Scrapes variant information including dbSNP ID, gene, number of diseases, chromosome, position, consequence, alleles, and Score VDA.
Sorts the variants by Score VDA in descending order.
Exports the data to CSV files.
Handles multiple UMLS CUI IDs from an input file and exports results individually.
Logs UMLS IDs with no data into a separate CSV file.
Usage:

Run the script.
Enter the number of data entries to retrieve per page (e.g., 25, 50, 100, 200, or a custom number).
Ensure the input file umcl_id_1.csv contains the UMLS CUI IDs.
The results are saved in CSV files named after each UMLS CUI ID.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
2: Single Disease Variant Scraper
This script retrieves disease variant information for a single disease query from the DisGeNET database, based on user input.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Key Features:
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Retrieves the total number of pages for a disease query.
Scrapes variant information including dbSNP ID, gene, number of diseases, chromosome, position, consequence, alleles, and Score VDA.
Sorts the variants by Score VDA in ascending order.
Exports the data to a CSV file.
Usage:

Run the script.
Enter the disease UMLS CUI ID.
Select the number of data entries to retrieve per page (e.g., 25, 50, 100, 200, or a custom number).
The results are saved in a CSV file named after the UMLS CUI ID.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------------------------------------------------------------------------------------
3: ClinVar RSID Searcher
This script searches ClinVar for genetic variant information based on a list of RSIDs provided in a file, and exports the results to a CSV file.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Key Features:
------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Searches ClinVar for each RSID.
Retrieves and stores information about the condition, classification, and variation record.
Exports the combined results for all RSIDs to a CSV file.
Usage:

Ensure the input file Rsid.csv contains the list of RSIDs.
Run the script.
The results are saved in clinvar_data.csv.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
