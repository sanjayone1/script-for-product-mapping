import requests
import json

# Load pincodes from a JSON file
with open('broker-pre-staging.pincodes_master.json', 'r') as json_file:
    pincodes = json.load(json_file)

# API details
url = 'https://proxy.oneassure.in/hdfc-optima-prod-quote/'
headers = {
    'MerchantKey': 'PRIBERGO',
    'SecretToken': 'PRIB@4931',
    'Content-Type': 'application/json'
}

# Initialize the tiers dictionary
tiers = {
    "tiers": []
}

# Print total pincodes fetched
print(f"Total pincodes fetched: {len(pincodes)}")

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
        "ConfigurationParam": {
            "AgentCode": "PRI00001"
        },
        "PlanName": "OptimaSecure",
        "PlanType": "Family",
        "InsuredDetail": [
            {
                "InsuredRelation": "Self",
                "InsuredAge": 25
            },
            {
                "InsuredRelation": "Wife",
                "InsuredAge": 23
            }
        ],
        "PinCode": str(pincode),
        "PolicyTenure": "1",
        "SumInsured": "1000000",
        "Deductible": "0",
        "IsLoyaltyDiscountOpted": False
    }
    
    # Make API request
    print(f"Making API request for pincode: {pincode}")
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Received response for pincode: {pincode} with status code: {response.status_code}")
        
        if response.status_code == 406:
            # Handle specific error response for invalid pincode
            data = response.json()
            if data.get("Data") and any(error['Key'] == "PinCodeInValidError" for error in data["Data"]):
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
                print(f"Invalid pincode for pincode: {pincode}, added to tier-not-found")
            continue  # Skip further processing for this pincode

        if response.status_code == 200:
            data = response.json()
            if data.get("Data") and "PremiumDetails" in data["Data"] and data["Data"]["PremiumDetails"]:
                premium_detail = data["Data"]["PremiumDetails"][0]
                policy_tenure = premium_detail["Tenure"]
                deductible = premium_detail["Deductible"]
                total_final_premium = premium_detail["TotalFinalPremium"]
                
                # Determine tier
                tier_level = "tier-not-found"
                if policy_tenure == 1 and deductible == 0.0:
                    if total_final_premium == 23742.0:
                        tier_level = "tier-1"
                    elif total_final_premium == 20031.0:
                        tier_level = "tier-2"
                    else:
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
                # Case where the response is 200 but does not contain expected data
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
                print(f"Unexpected data format for pincode: {pincode}, added to tier-not-found")
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
