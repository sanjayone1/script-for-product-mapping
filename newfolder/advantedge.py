import json
import requests

# Function to load pincodes from a JSON file
def load_pincodes_from_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        pincodes = [item['pincode'] for item in data if 'pincode' in item]
    return pincodes

# Load pincodes from the JSON file
json_file_path = 'broker-pre-staging.pincodes_master.json'  # Path to your JSON file
pincodes = load_pincodes_from_json(json_file_path)

# API endpoint and headers
url = 'https://abacus.careinsurance.com/religare_api/api/web/v1/abacus/partner?formattype=json'
headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.IntcImFwaV9rZXlcIjpcIkw4RDA3dldDWDJXM0NrVGpoMG0ydjc1MmlFUi01cjM0XCIsXCJlbWFpbFwiOlwib25laW5zdXJlQGNhcmVoZWFsdGhpbnN1cmFuY2UuY29tXCIsXCJleHBpcmVfdGltZVwiOjE3MjkyNDQxMDZ9Ig.uh-luiheN8tHS2m-0oRePbE4zMw916VxlpUs6zBA9UY',
    'Content-Type': 'application/json',
    'Cookie': 'BIGipServerABACUSPROD_443_pool=570514186.47873.0000; BIGipServerABACUSPROD_443_pool=570514186.47873.0000'
}

# Prepare to store results in a file
output_file = 'pincode_zones_newest-care-supreme.json'

# Write an opening bracket for the JSON array
with open(output_file, 'w') as json_file:
    json_file.write('[\n')  # Start of JSON array

print(f"Total pincodes to process: {len(pincodes)}")

# Iterate through all pincodes
for pincode in pincodes:
    print(f"Processing pincode: {pincode}")  # Debug print for current pincode

    # Prepare the payload with the current pincode
    payload = {
        "postedField": {
            "field_1": 1,
            "field_2": 10,
            "field_3": 22,
            "field_4": "1 Year",
            "field_9": "Individual",
            "field_10": 0,
            "field_54": str(pincode),  # Use the current pincode
            "field_WB": 1,
            "field_35": 1,
            "field_NCB": 1,
            "field_AHC": 1,
            "outPutField": "field_8"
        },
        "partnerId": "797199",
        "abacusId": "3105"
    }

    # Make the API request
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Response status code: {response.status_code}")  # Debug print for status code

        if response.status_code == 200:
            data = response.json()
            if data.get('status') and 'inputFields' in data.get('data', {}):
                # Extract zone from the response
                for field in data['data']['inputFields']:
                    if field['fieldName'] == 'field_54':
                        zone = field.get('zone', 'Not Found')  # Safely get the zone
                        result = {'pincode': pincode, 'zone': zone}

                        # Write the result to the JSON file
                        with open(output_file, 'a') as json_file:
                            json.dump(result, json_file)
                            json_file.write(',\n')  # Write a comma and newline for the next entry

                        print(f"Zone for pincode {pincode}: {zone}")  # Debug print for zone
                        break
            else:
                print(f"Unexpected response structure for pincode {pincode}")
        else:
            print(f"Error fetching data for pincode {pincode}: {response.status_code}")
            print(f"Response content: {response.content}")  # Log the response content for debugging
    except Exception as e:
        print(f"Exception occurred while fetching pincode {pincode}: {e}")

# Write closing bracket for the JSON array
with open(output_file, 'a') as json_file:
    json_file.write(']\n')  # End of JSON array

print("Pincode zones saved to pincode_zones_newest-care-supreme.json")
