# import json
# import requests
# from pymongo import MongoClient

# # MongoDB connection
# client = MongoClient('mongodb://oneassure-admin:0N3455ur3@localhost:27017/') 
# db = client['oneassure']  
# collection = db['pincode_master']  


# url = 'https://abacus.careinsurance.com/religare_api/api/web/v1/abacus/partner?formattype=json'
# headers = {
#     'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.IntcImFwaV9rZXlcIjpcIkw4RDA3dldDWDJXM0NrVGpoMG0ydjc1MmlFUi01cjM0XCIsXCJlbWFpbFwiOlwib25laW5zdXJlQGNhcmVoZWFsdGhpbnN1cmFuY2UuY29tXCIsXCJleHBpcmVfdGltZVwiOjE3MjgxMjM4NTV9Ig.x5lcIjWTA8I_JrRNgb1ysoMONjIQlwfjo0V_KYX0PCs',
#     'Content-Type': 'application/json',
#     'Cookie': 'BIGipServerABACUSPROD_443_pool=570514186.47873.0000; BIGipServerABACUSPROD_443_pool=570514186.47873.0000'
# }

# proxy_url = "proxy.corp.oneassure.in"
# proxy_port = 8181
# proxies = {
#     "http": f"http://{proxy_url}:{proxy_port}",
#     "https": f"http://{proxy_url}:{proxy_port}"
# }

# # Prepare to store results
# results = []

# # Get all pincodes from the MongoDB collection
# pincode_cursor = collection.find()
# pincode_count = collection.count_documents({})

# print(f"Total pincodes to process: {pincode_count}")

# # Iterate through all pincodes
# for document in pincode_cursor:
#     pincode = document['pincode']
#     print(f"Processing pincode: {pincode}")  # Debug print for current pincode
    
#     # Prepare the payload with the current pincode
#     payload = {
#         "postedField": {
#             "field_1": 1,
#             "field_2": 25,
#             "field_3": "25 - 35 years",
#             "field_4": "1 Year",
#             "field_9": "Individual",
#             "field_10": 0,
#             "field_54": str(pincode),  # Use the current pincode
#             "field_NS": "Resident of India",
#             "field_NCB": 1,
#             "field_43": 0,
#             "field_34": 0,
#             "field_SS": 0,
#             "field_35": 0,
#             "field_AHC": 0,
#             "field_CS": 0,
#             "field_GC": "Not Applicable",
#             "field_CPW": 0,
#             "outPutField": "field_8"
#         },
#         "partnerId": "354",
#         "abacusId": "6141"
#     }
    
#     # Make the API request using the proxy
#     try:
#         response = requests.post(url, headers=headers, json=payload, proxies=proxies)
#         print(f"Response status code: {response.status_code}")  # Debug print for status code

#         if response.status_code == 200:
#             data = response.json()
#             if data['status'] and 'inputFields' in data['data']:
#                 # Extract zone from the response
#                 for field in data['data']['inputFields']:
#                    if field['fieldName'] == 'field_54':
#                         zone = field.get('zone', 'Not Found')  # Safely get the zone
#                         result = {'pincode': pincode, 'zone': zone}
                        
#                         # Append to the results file
#                         with open('pincode_zones.json', 'w') as json_file:
#                             json_file.seek(-1, 2)  # Move to the end of the file
#                             json_file.write(f', {json.dumps(result)}]')  # Append new result

#                         print(f"Zone for pincode {pincode}: {zone}")  # Debug print for zone
#                         break
#             else:
#                 print(f"Unexpected response structure for pincode {pincode}")
#         else:
#             print(f"Error fetching data for pincode {pincode}: {response.status_code}")
#             print(f"Response content: {response.content}") 
#     except Exception as e:
#         print(f"Exception occurred while fetching pincode {pincode}: {e}")

# # with open('pincode_zones.json', 'w') as json_file:
# #     json.dump(results, json_file, indent=4)

# print("Pincode zones saved to pincode_zones.json")








# import json
# import requests
# from pymongo import MongoClient

# # MongoDB connection
# client = MongoClient('mongodb://oneassure-admin:0N3455ur3@localhost:27017/') 
# db = client['oneassure']  
# collection = db['pincode_master']  

# # API endpoint and headers
# url = 'https://abacus.careinsurance.com/religare_api/api/web/v1/abacus/partner?formattype=json'
# headers = {
#     'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.IntcImFwaV9rZXlcIjpcIkw4RDA3dldDWDJXM0NrVGpoMG0ydjc1MmlFUi01cjM0XCIsXCJlbWFpbFwiOlwib25laW5zdXJlQGNhcmVoZWFsdGhpbnN1cmFuY2UuY29tXCIsXCJleHBpcmVfdGltZVwiOjE3MjgxMjM4NTV9Ig.x5lcIjWTA8I_JrRNgb1ysoMONjIQlwfjo0V_KYX0PCs',
#     'Content-Type': 'application/json',
#     'Cookie': 'BIGipServerABACUSPROD_443_pool=570514186.47873.0000; BIGipServerABACUSPROD_443_pool=570514186.47873.0000'
# }

# # Proxy settings
# proxy_url = "proxy.corp.oneassure.in"
# proxy_port = 8181
# proxies = {
#     "http": f"http://{proxy_url}:{proxy_port}",
#     "https": f"http://{proxy_url}:{proxy_port}"
# }

# # Prepare to store results
# results_file_path = 'pincode_zones.json'

# # Initialize the results file
# with open(results_file_path, 'w') as json_file:
#     json_file.write('[]')  # Start with an empty JSON array

# # Get the total count of pincodes from the MongoDB collection
# pincode_count = collection.count_documents({})
# print(f"Total pincodes to process: {pincode_count}")

# # Iterate through all pincodes
# for document in collection.find():
#     pincode = document['pincode']
#     print(f"Processing pincode: {pincode}")  # Debug print for current pincode
    
#     # Prepare the payload with the current pincode
#     payload = {
#         "postedField": {
#             "field_1": 1,
#             "field_2": 25,
#             "field_3": "25 - 35 years",
#             "field_4": "1 Year",
#             "field_9": "Individual",
#             "field_10": 0,
#             "field_54": str(pincode),  # Use the current pincode
#             "field_NS": "Resident of India",
#             "field_NCB": 1,
#             "field_43": 0,
#             "field_34": 0,
#             "field_SS": 0,
#             "field_35": 0,
#             "field_AHC": 0,
#             "field_CS": 0,
#             "field_GC": "Not Applicable",
#             "field_CPW": 0,
#             "outPutField": "field_8"
#         },
#         "partnerId": "354",
#         "abacusId": "6141"
#     }
    
#     # Make the API request using the proxy
#     try:
#         response = requests.post(url, headers=headers, json=payload, proxies=proxies)
#         print(f"Response status code: {response.status_code}")  # Debug print for status code

#         if response.status_code == 200:
#             data = response.json()
#             if data['status'] and 'inputFields' in data['data']:
#                 # Extract zone from the response
#                 for field in data['data']['inputFields']:
#                     if field['fieldName'] == 'field_54':
#                         zone = field.get('zone', 'Not Found')  # Safely get the zone
#                         result = {'pincode': pincode, 'zone': zone}
                        
#                         # Append to the results file
#                         with open(results_file_path, 'r+') as json_file:
#                             json_file.seek(-1, 2)  # Move to the end of the file
#                             json_file.write(f', {json.dumps(result)}]')  # Append new result

#                         print(f"Zone for pincode {pincode}: {zone}")  # Debug print for zone
#                         break
#             else:
#                 print(f"Unexpected response structure for pincode {pincode}")
#         else:
#             print(f"Error fetching data for pincode {pincode}: {response.status_code}")
#             print(f"Response content: {response.content}")  # Log the response content for debugging
#     except Exception as e:
#         print(f"Exception occurred while fetching pincode {pincode}: {e}")

# print("Pincode zones processing completed.")
# import json
# import requests
# from pymongo import MongoClient

# # MongoDB connection
# client = MongoClient('mongodb://oneassure-admin:0N3455ur3@localhost:27017/') 
# db = client['oneassure']  
# collection = db['pincode_master']  


# url = 'https://abacus.careinsurance.com/religare_api/api/web/v1/abacus/partner?formattype=json'
# headers = {
#     'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.IntcImFwaV9rZXlcIjpcIkw4RDA3dldDWDJXM0NrVGpoMG0ydjc1MmlFUi01cjM0XCIsXCJlbWFpbFwiOlwib25laW5zdXJlQGNhcmVoZWFsdGhpbnN1cmFuY2UuY29tXCIsXCJleHBpcmVfdGltZVwiOjE3MjgxMjM4NTV9Ig.x5lcIjWTA8I_JrRNgb1ysoMONjIQlwfjo0V_KYX0PCs',
#     'Content-Type': 'application/json',
#     'Cookie': 'BIGipServerABACUSPROD_443_pool=570514186.47873.0000; BIGipServerABACUSPROD_443_pool=570514186.47873.0000'
# }

# proxy_url = "proxy.corp.oneassure.in"
# proxy_port = 8181
# proxies = {
#     "http": f"http://{proxy_url}:{proxy_port}",
#     "https": f"http://{proxy_url}:{proxy_port}"
# }

# # Prepare to store results
# results = []

# # Get all pincodes from the MongoDB collection
# pincode_cursor = collection.find()
# pincode_count = collection.count_documents({})

# print(f"Total pincodes to process: {pincode_count}")

# # Iterate through all pincodes
# for document in pincode_cursor:
#     pincode = document['pincode']
#     print(f"Processing pincode: {pincode}")  # Debug print for current pincode
    
#     # Prepare the payload with the current pincode
#     payload = {
#         "postedField": {
#             "field_1": 1,
#             "field_2": 25,
#             "field_3": "25 - 35 years",
#             "field_4": "1 Year",
#             "field_9": "Individual",
#             "field_10": 0,
#             "field_54": str(pincode),  # Use the current pincode
#             "field_NS": "Resident of India",
#             "field_NCB": 1,
#             "field_43": 0,
#             "field_34": 0,
#             "field_SS": 0,
#             "field_35": 0,
#             "field_AHC": 0,
#             "field_CS": 0,
#             "field_GC": "Not Applicable",
#             "field_CPW": 0,
#             "outPutField": "field_8"
#         },
#         "partnerId": "354",
#         "abacusId": "6141"
#     }
    
#     # Make the API request using the proxy
#     try:
#         response = requests.post(url, headers=headers, json=payload, proxies=proxies)
#         print(f"Response status code: {response.status_code}")  # Debug print for status code

#         if response.status_code == 200:
#             data = response.json()
#             if data['status'] and 'inputFields' in data['data']:
#                 # Extract zone from the response
#                 for field in data['data']['inputFields']:
#                    if field['fieldName'] == 'field_54':
#                         zone = field.get('zone', 'Not Found')  # Safely get the zone
#                         result = {'pincode': pincode, 'zone': zone}
                        
#                         # Append to the results file
#                         with open('pincode_zones.json', 'w') as json_file:
#                             json_file.seek(-1, 2)  # Move to the end of the file
#                             json_file.write(f', {json.dumps(result)}]')  # Append new result

#                         print(f"Zone for pincode {pincode}: {zone}")  # Debug print for zone
#                         break
#             else:
#                 print(f"Unexpected response structure for pincode {pincode}")
#         else:
#             print(f"Error fetching data for pincode {pincode}: {response.status_code}")
#             print(f"Response content: {response.content}") 
#     except Exception as e:
#         print(f"Exception occurred while fetching pincode {pincode}: {e}")

# # with open('pincode_zones.json', 'w') as json_file:
# #     json.dump(results, json_file, indent=4)

# print("Pincode zones saved to pincode_zones.json")







# import json
# import requests
# from pymongo import MongoClient

# # MongoDB connection
# client = MongoClient('mongodb://oneassure-admin:0N3455ur3@localhost:27017/') 
# db = client['oneassure']  
# collection = db['pincode_master'] 

# # API endpoint and headers
# url = 'https://abacus.careinsurance.com/religare_api/api/web/v1/abacus/partner?formattype=json'
# headers = {
#     'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.IntcImFwaV9rZXlcIjpcIkw4RDA3dldDWDJXM0NrVGpoMG0ydjc1MmlFUi01cjM0XCIsXCJlbWFpbFwiOlwib25laW5zdXJlQGNhcmVoZWFsdGhpbnN1cmFuY2UuY29tXCIsXCJleHBpcmVfdGltZVwiOjE3MjgxMjM4NTV9Ig.x5lcIjWTA8I_JrRNgb1ysoMONjIQlwfjo0V_KYX0PCs',
#     'Content-Type': 'application/json',
#     'Cookie': 'BIGipServerABACUSPROD_443_pool=570514186.47873.0000; BIGipServerABACUSPROD_443_pool=570514186.47873.0000'
# }

# # Proxy settings
# proxy_url = "proxy.corp.oneassure.in"
# proxy_port = 8181
# proxies = {
#     "http": f"http://{proxy_url}:{proxy_port}",
#     "https": f"http://{proxy_url}:{proxy_port}"
# }

# # Prepare to store results
# results = []

# # Get the total count of pincodes from the MongoDB collection
# pincode_count = collection.count_documents({})
# print(f"Total pincodes to process: {pincode_count}")

# # Iterate through all pincodes
# for document in collection.find():
#     pincode = document['pincode']
#     print(f"Processing pincode: {pincode}")  # Debug print for current pincode
    
#     # Prepare the payload with the current pincode
#     payload = {
#         "postedField": {
#             "field_1": 1,
#             "field_2": 25,
#             "field_3": "25 - 35 years",
#             "field_4": "1 Year",
#             "field_9": "Individual",
#             "field_10": 0,
#             "field_54": str(pincode),  # Use the current pincode
#             "field_NS": "Resident of India",
#             "field_NCB": 1,
#             "field_43": 0,
#             "field_34": 0,
#             "field_SS": 0,
#             "field_35": 0,
#             "field_AHC": 0,
#             "field_CS": 0,
#             "field_GC": "Not Applicable",
#             "field_CPW": 0,
#             "outPutField": "field_8"
#         },
#         "partnerId": "354",
#         "abacusId": "6141"
#     }
    
#     # Make the API request using the proxy
#     try:
#         response = requests.post(url, headers=headers, json=payload, proxies=proxies)
#         print(f"Response status code: {response.status_code}")  # Debug print for status code

#         if response.status_code == 200:
#             data = response.json()
#             if data['status'] and 'inputFields' in data['data']:
#                 # Extract zone from the response
#                 for field in data['data']['inputFields']:
#                     if field['fieldName'] == 'field_54':
#                         zone = field.get('zone', 'Not Found')  # Safely get the zone
#                         result = {'pincode': pincode, 'zone': zone}
#                         results.append(result)  # Append result to the list
#                         print(f"Zone for pincode {pincode}: {zone}")  # Debug print for zone
#                         break
#             else:
#                 print(f"Unexpected response structure for pincode {pincode}")
#         else:
#             print(f"Error fetching data for pincode {pincode}: {response.status_code}")
#             print(f"Response content: {response.content}")  # Log the response content for debugging
#     except Exception as e:
#         print(f"Exception occurred while fetching pincode {pincode}: {e}")

# # Save results to a JSON file at once
# with open('pincode_zones.json', 'w') as json_file:
#     json.dump(results, json_file, indent=4)

# print("Pincode zones saved to pincode_zones.json")


import json
import requests
from pymongo import MongoClient

# MongoDB connection
client = MongoClient('mongodb://oneassure-admin:0N3455ur3@localhost:27017/') 
db = client['oneassure']  
collection = db['pincodes_master'] 

# API endpoint and headers
url = 'https://abacus.careinsurance.com/religare_api/api/web/v1/abacus/partner?formattype=json'
headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.IntcImFwaV9rZXlcIjpcIkw4RDA3dldDWDJXM0NrVGpoMG0ydjc1MmlFUi01cjM0XCIsXCJlbWFpbFwiOlwib25laW5zdXJlQGNhcmVoZWFsdGhpbnN1cmFuY2UuY29tXCIsXCJleHBpcmVfdGltZVwiOjE3MjkyNDQxMDZ9Ig.uh-luiheN8tHS2m-0oRePbE4zMw916VxlpUs6zBA9UY',
    'Content-Type': 'application/json',
    'Cookie': 'BIGipServerABACUSPROD_443_pool=570514186.47873.0000; BIGipServerABACUSPROD_443_pool=570514186.47873.0000'
}

# Proxy settings
proxy_url = "proxy.corp.oneassure.in"
proxy_port = 8181
proxies = {
    "http": f"http://{proxy_url}:{proxy_port}",
    "https": f"http://{proxy_url}:{proxy_port}"
}

# Prepare to store results in a file
output_file = 'pincode_zones_newest-care-supreme.json'

# Write an opening bracket for the JSON array
with open(output_file, 'w') as json_file:
    json_file.write('[\n')  # Start of JSON array

# Get the total count of pincodes from the MongoDB collection
pincode_count = collection.count_documents({})
print(f"Total pincodes to process: {pincode_count}")

# Iterate through all pincodes
for idx, document in enumerate(collection.find()):
    pincode = document['pincode']
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

    # payload = {
    #     "postedField": {
    #         "field_1": 1,
    #         "field_2": 25,
    #         "field_3": "25 - 35 years",
    #         "field_4": "1 Year",
    #         "field_9": "Individual",
    #         "field_10": 0,
    #         "field_54": str(pincode),  # Use the current pincode
    #         "field_NS": "Resident of India",
    #         "field_NCB": 1,
    #         "field_43": 0,
    #         "field_34": 0,
    #         "field_SS": 0,
    #         "field_35": 0,
    #         "field_AHC": 0,
    #         "field_CS": 0,
    #         "field_GC": "Not Applicable",
    #         "field_CPW": 0,
    #         "outPutField": "field_8"
    #     },
    #     "partnerId": "354",
    #     "abacusId": "6141"
    # }
    
    # Make the API request using the proxy
    try:
        response = requests.post(url, headers=headers, json=payload, proxies=proxies)
        print(f"Response status code: {response.status_code}")  # Debug print for status code

        if response.status_code == 200:
            data = response.json()
            if data['status'] and 'inputFields' in data['data']:
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

print("Pincode zones saved to pincode_zones.json")
