import csv
import requests
from bs4 import BeautifulSoup
import sys

def get_total_pages(disease_query, data_count):
    url = f"https://www.disgenet.org/browser/0/1/4/{disease_query}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    pagination = soup.find("ul", class_="pagination")
    if pagination:
        last_page_link = pagination.find_all("li")[-2].a["href"]
        last_page_number = int(last_page_link.split("/")[-2])
        return last_page_number
    else:
        return 1

def get_disease_variants(disease_query, data_count):
    all_variants = []
    total_pages = get_total_pages(disease_query, data_count)

    for page in range(1, total_pages + 1):
        url = f"https://www.disgenet.org/browser/0/1/4/{disease_query}/0/{data_count}/{page}/_a/_b./snpid/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="table-striped")

        if table:
            rows = table.find_all("tr")
            for row in rows[1:]:
                cells = row.find_all("td")
                if len(cells) >= 14:
                    variant_cell = cells[0]
                    variant_link = variant_cell.find("a")
                    if variant_link:
                        variant_id = variant_link.text.strip()
                        variant = f"dbSNP: {variant_id}"
                    else:
                        variant = "N/A"
                    gene = cells[3].text.strip() if cells[3].text.strip() else "MISSING GENE"
                    n_diseases = cells[4].text.strip()
                    chr_ = cells[7].text.strip() 
                    position = cells[8].text.strip()
                    consequence = cells[9].text.strip()
                    alleles = cells[10].text.strip()
                    score_vda = cells[14].text.strip()  
                    all_variants.append([variant, gene, n_diseases, chr_, position, consequence, alleles, score_vda])
        else:
            print("Table not found on page {}.".format(page))

    all_variants.sort(key=lambda x: float(x[-1]), reverse=True)

    return all_variants

def export_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Variant', 'Gene', 'N. diseases v', 'Chr', 'Position', 'Consequence', 'Alleles', 'Score vda'])
        writer.writerows(data)

def read_umls_ids_from_file(filename):
    with open(filename, 'r') as file:
        umls_ids = [line.strip() for line in file]
    return umls_ids

def search_diseases_from_file(input_filename, data_count):
    umls_ids = read_umls_ids_from_file(input_filename)
    all_processed = True
    no_data_ids = []
    for umls_id in umls_ids:
        print(f"Searching for disease with UMLS ID: {umls_id}")
        all_variants = get_disease_variants(umls_id, data_count)
        if all_variants:
            filename = f"{umls_id}_variants.csv"
            export_to_csv(all_variants, filename)
            print(f"Data exported to {filename} successfully!")
        else:
            print("No data found.")
            no_data_ids.append(umls_id)
        all_processed = False

    if all_processed:
        print("All CSV files processed. Completed!")
        sys.exit()

    if no_data_ids:
        with open("No_Data_Found.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['UMLS_ID'])
            writer.writerows([[umls_id] for umls_id in no_data_ids])

if __name__ == "__main__":
    print("Select the number of output data:")
    print("1. 25")
    print("2. 50")
    print("3. 100")
    print("4. 200")
    print("5. Custom")
    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        data_count = 25
    elif choice == "2":
        data_count = 50
    elif choice == "3":
        data_count = 100
    elif choice == "4":
        data_count = 200
    elif choice == "5":
        data_count = int(input("Enter the custom number of data: "))
    else:
        print("Invalid choice. Using default value of 25.")
        data_count = 25
    input_filename = "umcl_id_1.csv"
    search_diseases_from_file(input_filename, data_count)
