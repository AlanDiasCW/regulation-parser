#txt -> parse -> json -> summarize(?) -> new_csv
#embedd new csv.

#read merged.
#read plk.

#add csv to merged
#update indexes from pkl 

import os
import sys
import csv
import subprocess
import pandas as pd
import pickle

def combine_embeddings(existing_embeddings, new_embeddings):
  combined_embeddings = {}
  for idx, embedding in existing_embeddings.items():
      combined_embeddings[idx] = embedding
  for idx, embedding in new_embeddings.items():
      combined_embeddings[idx + len(existing_embeddings)] = embedding
  return combined_embeddings

# Get the input file name from command line arguments
if len(sys.argv) < 2:
  print("Usage: python script.py input_file.txt")
  sys.exit(1)

if not sys.argv[1].endswith('txt'):
  print('file needs to be a txt')
  sys.exit(1)

input_file = sys.argv[1]

#breakpoint()

root_dir = os.getcwd()
parent_dir = os.path.dirname(os.getcwd())
files_path = os.path.join(parent_dir, "files")
txt_path = os.path.join(parent_dir, "files/txt/")
csv_path = os.path.join(parent_dir, "files/csv/")
json_path = os.path.join(parent_dir, "files/json/")


#subprocess.call(['python', 'parse_regulation.py', input_file])

base_file_name = os.path.splitext(input_file)[0] 
json_file = base_file_name + '.json'

#subprocess.call(['python', 'summarize_parsed_regulation.py', json_file])

summarized_json = 'summary.' + json_file
subprocess.call(['python', 'parsed_regulation_to_csv.py', summarized_json])

breakpoint()

csv_file = 'summary.' + base_file_name + '.csv'
#Embedd
subprocess.call(['python', 'csv_to_embeddings.py', csv_path + csv_file])

##get embedded 
os.chdir(root_dir)

#breakpoint()
new_embeddigns = []
with open(files_path + '/'+ 'summary.pkl', 'rb') as f:
    new_embeddings = pickle.load(f)

#breakpoint()

##current_csv = pd.read_csv(files_path + '/'+ 'merged.csv')
with open(files_path + '/' + 'merged.pkl', 'rb') as f:
    # Load the object from the file
    document_embeddings = pickle.load(f)

#breakpoint()    
files_list = []
files_list.append(files_path + '/'+ 'merged.csv')
files_list.append(csv_path + csv_file)

csv_contents = []
# read contents of csv files with each name and append to csv_contents
for csv_name in files_list:
  with open(csv_name, "r") as csv_file:
      csv_reader = csv.reader(csv_file)
      for row in csv_reader:
        print(row)
        csv_contents.append(row)

#breakpoint()

os.chdir(root_dir)
with open('new_merged.csv', "w") as csv_output_file:
    csv_writer = csv.writer(csv_output_file)
    csv_writer.writerows(csv_contents)

#breakpoint()

output_file = 'new_merged.pkl'
final_embeddings = combine_embeddings(document_embeddings, new_embeddings)

pickle.dump(final_embeddings,open(output_file, "wb"))





