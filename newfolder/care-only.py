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
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.IntcImFwaV9rZXlcIjpcIkw4RDA3dldDWDJXM0NrVGpoMG0ydjc1MmlFUi01cjM0XCIsXCJlbWFpbFwiOlwib25laW5zdXJlQGNhcmVoZWFsdGhpbnN1cmFuY2UuY29tXCIsXCJleHBpcmVfdGltZVwiOjE3Mjk1NzUwNjh9Ig.aHhHqnc42FcYinyKuj2uAsipK31m7bJAAeqpwy7Z87s',
    'Content-Type': 'application/json',
    'Cookie': 'BIGipServerABACUSPROD_443_pool=570514186.47873.0000; BIGipServerABACUSPROD_443_pool=570514186.47873.0000'
}

# Proxy configuration
proxies = {
    'http': 'http://proxy.corp.non-prod.oneassure.in:8181',
    'https': 'http://proxy.corp.non-prod.oneassure.in:8181',
}

# Prepare to store results and errors in separate files
output_file = 'pincode_zones_newest-care-only.json'
error_file = 'pincode_errors_zones_newest-care-only.json'

# Write an opening bracket for the JSON array
with open(output_file, 'w') as json_file:
    json_file.write('[\n')  # Start of JSON array

# Initialize a list to collect errors
error_list = []

print(f"Total pincodes to process: {len(pincodes)}")

# Iterate through all pincodes
for pincode in pincodes:
    print(f"Processing pincode: {pincode}")  # Debug print for current pincode

    # Prepare the updated payload with the current pincode
    payload = {
        "postedField": {
            "field_1": 1,
            "field_2": 10,
            "field_3": "18 - 24 years",
            "field_4": "1 Year",
            "field_9": "Individual",
            "field_10": 0,
            "field_54": str(pincode),
            "field_35": 0,
            "field_CS": 0,
            "field_43": 0,
            "field_UA": 0,
            "field_EDC": 0,
            "field_OPD_SI": 0,
            "field_CPW": 0,
            "field_NCB": 0,
            "outPutField": "field_8"
        },
        "partnerId": "797199",
        "abacusId": "3472"
    }

    # Make the API request
    try:
        response = requests.post(url, headers=headers, json=payload, proxies=proxies)
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
        # Log the error with the pincode
        error_list.append({'pincode': pincode, 'error': str(e)})

# Write closing bracket for the JSON array
with open(output_file, 'a') as json_file:
    json_file.write(']\n')  # End of JSON array

# Write errors to a separate JSON file
with open(error_file, 'w') as json_file:
    json.dump(error_list, json_file)

print("Pincode zones saved to pincode_zones_newest-care-only.json")
print(f"Errors saved to {error_file}")
