import requests
import json

# Load pincodes from a JSON file
def load_pincodes_from_json(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

# Load pincodes
json_file_path = 'broker-pre-staging.pincodes_master.json'  # Path to your JSON file
pincodes = load_pincodes_from_json(json_file_path)
print(f"Total pincodes fetched: {len(pincodes)}")

# API details
url = 'https://foyer.tataaig.com/quick-quote/create'
headers = {
    'x-api-key': '4GCHsYsrY5a1mNHtObLI01rqcFuO8PWq3eN5BeDQ',
    'Content-Type': 'application/json'
}

# Initialize the tiers dictionary
tiers = {
    "tiers": []
}

# Proxy configuration
proxies = {
    'http': 'http://proxy.corp.non-prod.oneassure.in:8181',
    'https': 'http://proxy.corp.non-prod.oneassure.in:8181',
}

# Function to save results to a JSON file
def save_results():
    with open('tiers_output_new.json', 'w') as json_file:
        json.dump(tiers, json_file, indent=4)

# Iterate through each pincode
for index, pincode_doc in enumerate(pincodes):
    pincode = pincode_doc['pincode']
    city = pincode_doc['city']
    
    print(f"Processing pincode: {pincode}, city: {city} (Index: {index + 1})")
    
    # Prepare request payload
    payload = {
        "lob": "Health",
        "businessType": "New Business",
        "prevPolicyEndDate": "",
        "portability": False,
        "tenure": 3,
        "typeOfProduct": "Retail",
        "isEmployee": False,
        "goGreen": False,
        "isParentsAlive": False,
        "planType": "Individual",
        "solId": "",
        "source": "TATA-AIG",
        "producerCode": "2094990000",
        "ipAddress": "1.2.3.4",  # Replace with actual IP if needed
        "isExistingCustomer": False,
        "branchLocation": "MUMBAI",
        "proposer": {
            "address": {
                "pincode": str(pincode)
            }
        },
        "memberDetails": [
            {
                "sumInsured": 1500000,
                "dob": "09/10/2021",  # Replace with actual DOB if needed
                "relationship": "Son 1",
                "deductible": 200000
            }
        ]
    }
    
    # Make API request
    print(f"Making API request for pincode: {pincode}")
    try:
        response = requests.post(url, headers=headers, json=payload, proxies=proxies)
        print(f"Received response for pincode: {pincode} with status code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if data.get("data") and "quotes" in data["data"] and data["data"]["quotes"]:
                quote = data["data"]["quotes"][0]  # Get the first quote
                
                if quote["productCode"] == "2847":
                    # Check the premium to classify tier
                    premium = quote["premium"]
                    tier_level = "tier-not-found"  # Default to not found
                    
                    if premium == 20904:
                        tier_level = "tier-1"
                    elif premium == 19989:
                        tier_level = "tier-2"
                    elif premium == 16475:
                        tier_level = "tier-3"

                    # Update tiers
                    tier_found = next((tier for tier in tiers["tiers"] if tier["level"] == tier_level), None)
                    if tier_found:
                        tier_found["cities"].append(city)
                        tier_found["pincodes"].append(pincode)
                    else:
                        tiers["tiers"].append({
                            "level": tier_level,
                            "cities": [city],
                            "pincodes": [pincode]
                        })
            else:
                # Handle case where no quotes are returned
                tier_level = "tier-not-found"
                tier_found = next((tier for tier in tiers["tiers"] if tier["level"] == tier_level), None)
                if tier_found:
                    tier_found["cities"].append(city)
                    tier_found["pincodes"].append(pincode)
                else:
                    tiers["tiers"].append({
                        "level": tier_level,
                        "cities": [city],
                        "pincodes": [pincode]
                    })
                print(f"No quotes available for pincode: {pincode}, added to tier-not-found")
        else:
            print(f"Request failed for pincode: {pincode} with status code: {response.status_code}")

        # Save results after each iteration
        save_results()

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while processing pincode: {pincode}. Error: {str(e)}")
    
    # Print progress
    print(f"Processed {index + 1}/{len(pincodes)} pincodes")

# Final save of results
save_results()
print("Data processing complete. Results saved to 'tiers_output_new.json'.")
