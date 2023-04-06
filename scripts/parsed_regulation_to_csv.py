import os
import json
import csv
import sys
import textwrap

# Get the input file name from command line arguments
if len(sys.argv) < 2:
  print("Usage: python script.py input_file.json")
  sys.exit(1)

if not sys.argv[1].endswith('json'):
  print('file needs to be a json')
  sys.exit(1)


root_dir = os.getcwd()
parent_dir = os.path.dirname(os.getcwd())
files_path = os.path.join(parent_dir, "files")
input_path = os.path.join(parent_dir, "files/json/")
output_path = os.path.join(parent_dir, "files/csv/")

input_file = sys.argv[1]


# # Open the JSON file for reading
with open(input_path+input_file, 'r') as json_file:
    # Load the JSON data from the file
    data = json.load(json_file)

output_file = os.path.splitext(input_file)[0] + ".csv"

output_file = output_path + output_file

# Open the CSV file for writing
with open(output_file, 'w', newline='') as csv_file:
    # Create a CSV writer object
    writer = csv.writer(csv_file)

    # Loop through each JSON element in the array
    for item in data:
        # Serialize the JSON object to a string in the specified format
        #item["chunks"] = textwrap.wrap(item["content"], width=900)
        item["chunks"] = textwrap.wrap(item["summary"], width=900)
        
        for element in item["chunks"]:
          name = item["name"] if item['name'] != '' else ''
          chapter = ', capítulo: ' + item['chapter'] if item['chapter'] != '' else ''
          section = ', seção: ' + item['section'] if item['section'] != '' else ''
          article = ', art: ' + item['article'] + element if item['article'] != '' else element  
          json_string = name + chapter + section + article
          # Write the string to the CSV file
          writer.writerow([json_string])