import os as os 
import subprocess
#import parse_regulation as parse_regulation 

root_dir = os.getcwd()
parent_dir = os.path.dirname(os.getcwd())
files_path = os.path.join(parent_dir, "files")
txt_path = os.path.join(parent_dir, "files/txt/")
csv_path = os.path.join(parent_dir, "files/csv/")
json_path = os.path.join(parent_dir, "files/json/")

os.chdir(txt_path)
txt_list = os.listdir()

os.chdir(root_dir)
for file in txt_list:
  #Call the Python script 'script2.py' and pass the argument 'hello' to it
  subprocess.call(['python', 'parse_regulation.py', file])    

os.chdir(json_path)
json_list = os.listdir()

os.chdir(root_dir)
for file in json_list:
  #Call the Python script 'script2.py' and pass the argument 'hello' to it
  subprocess.call(['python', 'parsed_regulation_to_csv.py', file])

os.chdir(root_dir)
subprocess.call(['python', 'merge_csvs.py'])


merged_file = files_path + '/' + "merged.csv"
subprocess.call(['python', 'csv_to_embeddings.py', merged_file])