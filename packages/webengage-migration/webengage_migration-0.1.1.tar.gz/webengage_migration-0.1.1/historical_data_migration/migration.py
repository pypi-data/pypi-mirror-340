import csv
import json
import tempfile
import os
import requests
import time
import argparse
from datetime import datetime

def process_csv_and_send_batches(type, filename, datacenter, license_code):
    print("🔄 Step 1: Preparing JSON to the file...!")
    col_length=0
    custom_name=""
    json_obj={}
    # Step 1: Process CSV and write JSONs to new column in temp file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, newline='', encoding='utf-8') as temp_output:
        with open(filename, mode='r', encoding='utf-8-sig', newline='') as original_file:
            reader = csv.reader(original_file)
            writer = csv.writer(temp_output)

            header = next(reader)
            new_header = ["converted JSON"] + header
            writer.writerow(new_header)

            for row in reader:
                if type=="events":
                    col_length=3
                    custom_name="eventData"    
                    json_obj = {
                        header[0]: row[0],
                        header[1]: row[1],
                        header[2]: row[2],
                        "eventData": {}
                    }
                    for i in range(col_length, len(header)):
                       json_obj[f"{custom_name}"][header[i]] = datatype(row[i])


                if type=="users":
                    col_length=11    
                    custom_name="attributes"
                    json_obj={
                        header[0]: row[0],
                        header[1]: row[1],
                        header[2]: row[2],
                        header[3]: birthDate(row[3]),
                        header[4]: row[4],
                        header[5]: row[5],
                        header[6]: row[6],
                        header[7]: row[7],
                        header[8]: row[8],
                        header[9]: row[9],
                        header[10]: row[10]        
                    }
                    if len(header) > 11:
                        json_obj["attributes"] = {}
                        for i in range(col_length, len(header)):
                            json_obj[f"{custom_name}"][header[i]] = datatype(row[i])
                    
                json_str = json.dumps(json_obj, indent=2)  
                writer.writerow([json_str] + row)

    # Updating the CSV with JSOn data
    os.replace(temp_output.name, filename)
    print(f"✅ JSON creation complete: {filename}")

    print("\n🚀 Step 2: Sending data in batches to WebEngage...!")

    # Step 2: Read the new file and send events in batches
    send_json_batches_from_csv(type, filename, datacenter, license_code)

def send_json_batches_from_csv(type, csv_filename, datacenter, licence_code):


    apikey = input("Please enter your API Key: ")

    if datacenter=="default":
        url = f"https://api.webengage.com/v1/accounts/{licence_code}/bulk-{type}"
    else:
        url = f"https://api.{datacenter}.webengage.com/v1/accounts/{licence_code}/bulk-{type}"
    
    headers = {
        'Authorization': f'Bearer {apikey}',
        'Content-Type': 'application/json'
    }

    batch_size = 25
    current_batch = []
    row_numbers = []
    total_batches = 0

    with open(csv_filename, mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        
        next(reader)    # skipping the header row
        row_number = 1

        for row in reader:
            row_number += 1
            json_str = row[0].strip()
            
            if not json_str:
                print(f"⚠️ Skipping row {row_number} - empty JSON")
                continue

            try:
                event = json.loads(json_str)
                current_batch.append(event)
                row_numbers.append(row_number)
            except json.JSONDecodeError as e:
                print(f"⚠️ Skipping row {row_number} due to JSON decode error: {e}")
                continue
            
            if len(current_batch) == batch_size:
                total_batches += 1
                send_batch(type, current_batch, row_numbers, url, headers, total_batches)
                current_batch = []
                row_numbers = []
                time.sleep(0.15)  # ~6.6 requests/sec = 396 req/min (safe)

        # Final leftover batch
        if current_batch:
            total_batches += 1
            send_batch(type, current_batch, row_numbers, url, headers, total_batches)

    print(f"\n✅ All batches processed successfully. Total sent: {total_batches}")

def send_batch(type, batch, row_numbers, url, headers, batch_number):
    payload = {f"{type}": batch}
   
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200 or response.status_code == 201:
            print(f"✅ Batch {batch_number} with rows {row_numbers} sent successfully.")
        else:
            print(f"❌ Batch {batch_number} failed with status code {response.status_code}. Trying individual rows...")
            # Try sending each row individually
            for i, single_event in enumerate(batch):
                row_num = row_numbers[i]
                single_payload = {f"{type}": [single_event]}
                try:
                    r = requests.post(url, headers=headers, data=json.dumps(single_payload))
                    if r.status_code == 200 or r.status_code == 201:
                        print(f"   ✅ Row {row_num} sent successfully.")
                    else:
                        print(f"   ❌ Row {row_num} failed with status {r.status_code}: {r.text}")
                except Exception as e:
                    print(f"   ❌ Row {row_num} failed due to error: {e}")

    except Exception as e:
        print(f"❌ Batch {batch_number} (rows {row_numbers}) failed due to error: {e}")


def datatype(value):
        value = value.strip()
        if value.lower() == 'true':
            return True
        if value.lower() == 'false':
            return False
        
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value  # keep as string
            

def birthDate(value):
    value=value.strip()

    if value=="":
        return ""
    else:
        date_obj = datetime.strptime(value.strip(), "%d-%m-%Y")
        return f"{date_obj.strftime("%Y-%m-%d")}T11:11:00-0800"


def main():
    parser = argparse.ArgumentParser(description="Migrate historical data to WebEngage for the provided license code and datacenter.")

    parser.add_argument("-f", "--filename", required=True, help="CSV filename with extension.")
    parser.add_argument("-d", "--datacenter", default="default", help="(optional) provide datacenter, default set to global.")
    parser.add_argument("-lc", "--license_code", required=True, help="WebEngage account license code.")
    parser.add_argument("--migrate", choices=["users", "events"], required=True, help="use this flag to start the migration.")

    args = parser.parse_args()

    if args.migrate in ["users", "events"]:
        process_csv_and_send_batches(args.migrate, args.filename, args.datacenter, args.license_code)    
    else:
        print("❌ Migration not started. Use --migrate to initiate the migration.")

if __name__=="__main__":
    main()
