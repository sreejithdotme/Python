import requests
from bs4 import BeautifulSoup
import csv
from tabulate import tabulate

def search_clinvar_by_rsid(rsid):
    url = f"https://www.ncbi.nlm.nih.gov/clinvar/?term={rsid}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            condition_rows = soup.find_all('tr', {'class': 'germline-cond-col'})
            if condition_rows:
                data = []
                for row in condition_rows:
                    cells = row.find_all('td')
                    condition = cells[0].text.strip()
                    classification = cells[1].text.strip()
                    variation_record = cells[4].text.strip()
                    data.append([rsid, condition, classification, variation_record])
                return data
            else:
                return None
        else:
            print(f"Failed to retrieve search results for rsID '{rsid}'. Status code:", response.status_code)
            return None
    except requests.RequestException as e:
        print("Error:", e)
        return None

def read_rsids_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def export_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["rsID", "Condition", "Classification", "Variation record"])
        writer.writerows(data)

def main():
    rsids = read_rsids_from_file('Rsid.csv')

    all_data = []
    for rsid in rsids:
        data = search_clinvar_by_rsid(rsid)
        if data:
            all_data.extend(data)

    if all_data:
        export_to_csv(all_data, 'clinvar_data.csv')
        print("Data exported to clinvar_data.csv successfully!")
    else:
        print("No data found.")

if __name__ == "__main__":
    main()
