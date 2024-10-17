import requests
import json
import uuid
import pandas as pd
import time

def token():
    url = "https://janus.icicilombard.com/generate-jwt-token"
    payload = 'grant_type=password&username=ProstInsure&password=3jAsLBnaLGk2sWU&scope=esbhealth&client_id=ProstInsure&client_secret=Zm3GOH3E7lofyUmRCyZo7eJdaP3y351pao7pSJ1IDNwAr23LFGFH2Z66x70eCPGG'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.json()["access_token"]

def getZone(city, state, access_token):
    zone_url = "https://janus.icicilombard.com/health/ilservices/health/v1/generic/getzonedetail"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {access_token}"
    }
    
    correlationId = str(uuid.uuid1())

    payload = json.dumps({
        "City": city,
        "State": state,
        "ProductCode": 3837,
        "CorrelationId": correlationId
    })

    response = requests.post(zone_url, headers=headers, data=payload)
    
    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")
    
    response_data = response.json()
    return response_data.get("zone").strip()

# Main execution
if __name__ == "__main__":
    # Read city and state from CSV file
    csv_file = "matching_pincodes.csv"  # Update this with the path to your CSV file
    df = pd.read_csv(csv_file)

    # Initialize structures for storing zone mappings and errors
    zones_mapping = {
        "tiers": [
            {"level": "tier-1", "cities": [], "pincodes": []},
            {"level": "tier-2", "cities": [], "pincodes": []},
            {"level": "tier-3", "cities": [], "pincodes": []},
            {"level": "tier-4", "cities": [], "pincodes": []},
            {"level": "tier-not-found", "cities": [], "pincodes": []}
        ]
    }

    errors_log = []

    # Open JSON file for writing
    with open("zone_mappings.json", "w") as json_file, open("error_log.json", "w") as error_file:
        # Initialize a counter for processed pincodes
        processed_count = 0

        # Iterate through each row in the DataFrame
        for index, row in df.iterrows():
            city = row['CITYDISTRICT']  # Update this to your actual column name for city
            state = row['STATE']        # Update this to your actual column name for state
            pincode = row['PINCODE']    # Update this to your actual column name for pincode

            # Print the current city, state, and pincode being checked
            print(f"Checking city: {city}, state: {state}, pincode: {pincode}")

            try:
                # Generate token
                access_token = token()
                
                time.sleep(1)
                
                # Get zone for the current city and state
                zone = getZone(city, state, access_token)
                
                # Print the zone obtained
                print(f"Obtained zone for {city}, {state}: {zone}")
                
                # Determine the tier based on the zone
                if zone == "Zone A":
                    tier = zones_mapping["tiers"][0]  # tier-1
                elif zone == "Zone B":
                    tier = zones_mapping["tiers"][1]  # tier-2
                elif zone == "Zone C":
                    tier = zones_mapping["tiers"][2]  # tier-3
                elif zone == "Zone D":
                    tier = zones_mapping["tiers"][3]  # tier-4
                else:
                    tier = zones_mapping["tiers"][4]  # tier-not-found

                # Append city and pincode to the appropriate tier
                tier["cities"].append(city)
                tier["pincodes"].append(pincode)

            except Exception as e:
                # Log the error and the corresponding pincode
                error_info = {
                    "pincode": pincode,
                    "city": city,
                    "state": state,
                    "error": str(e)
                }
                errors_log.append(error_info)
                print(f"Error processing {pincode}: {str(e)}")
                continue  # Skip to the next iteration

            # Write the updated zones mapping to the JSON file after each iteration
            json_file.seek(0)  # Move the cursor to the beginning of the file
            json.dump(zones_mapping, json_file, indent=4)
            json_file.truncate()  # Remove any remaining old data

            # Increment the counter
            processed_count += 1
            
            # Print the processed count
            print(f"Processed {processed_count}/{len(df)} pincodes.")

            # Sleep for a short duration to avoid overwhelming the server
            time.sleep(1)  # Adjust the duration as necessary (in seconds)

        # Write the errors to the error log JSON file
        if errors_log:
            json.dump(errors_log, error_file, indent=4)
        
    print("Zone mappings saved to zone_mappings.json")
    print("Errors saved to error_log.json")
