import os
import csv

# Go to the "files" directory
parent_dir = os.path.dirname(os.getcwd())
input_path = os.path.join(parent_dir, "files/csv/")
output_path = os.path.join(parent_dir, "files")
os.chdir(input_path)


# Get a list of all the files in the directory
files_list = os.listdir()

# Remove duplicates based on the filename without extension
#unique_files = []
#for file in files_list:
#    name, ext = os.path.splitext(file)
#    if name not in unique_files:
#        unique_files.append(name)

# Sort the list of unique filenames
#unique_files.sort()

#############################################################################
# create an empty list to store csv file contents
csv_contents = []

# read contents of csv files with each name and append to csv_contents
for csv_name in files_list:
  with open(csv_name, "r") as csv_file:
      csv_reader = csv.reader(csv_file)
      for row in csv_reader:
        print(row)
        csv_contents.append(row)

os.chdir(output_path)
with open('merged.csv', "w") as csv_output_file:
    csv_writer = csv.writer(csv_output_file)
    csv_writer.writerows(csv_contents)

##############################################################################



