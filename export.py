import csv

def export_to_csv(data, filename):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data['headers'])  # Column headers
            writer.writerows(data['rows'])  # Data rows
        print(f"Report successfully exported to {filename}!")
    except Exception as e:
        print("Error while exporting:", e)
