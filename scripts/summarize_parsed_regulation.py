import os
import json
import csv
import sys
import textwrap

####################################################
import openai
from dotenv import load_dotenv, find_dotenv

# Load environment keys from .env
load_dotenv(find_dotenv())

openai.api_key = os.environ.get('OPENAI_API_KEY')

COMPLETIONS_MODEL = "text-davinci-003"
MAX_MODEL_LEN = 4000 #2049
MAX_COMPLETION_LEN = 500
MAX_SECTION_LEN = MAX_MODEL_LEN - MAX_COMPLETION_LEN

COMPLETIONS_API_PARAMS = {
    "temperature": 0.2,
    "max_tokens": MAX_COMPLETION_LEN, #The max_tokens parameter sets an upper bound on how many tokens the API will return
    "model": COMPLETIONS_MODEL,
}
####################################################

# Get the input file name from command line arguments
if len(sys.argv) < 2:
  print("Usage: python script.py input_file.json")
  sys.exit(1)

if not sys.argv[1].endswith('json'):
  print('file needs to be a json')
  sys.exit(1)


root_dir = os.getcwd()
parent_dir = os.path.dirname(os.getcwd())
input_path = os.path.join(parent_dir, "files/json/")
output_path = os.path.join(parent_dir, "files/json/")

input_file = sys.argv[1]

# # Open the JSON file for reading
with open(input_path+input_file, 'r') as json_file:
  data = json.load(json_file)
  
output_file = 'summary.' + input_file 

parsed_file = []
# Open the CSV file for writing
for item in data:
    header = "Resuma o TEXTO, é importante manter todos os números de artigos/capítulos/seções, exceto no caso de 'as instituições referidas no art.' que pode ser susbtituido por apenas 'as instituições'. Procure trazer exatamente o mesmo significado, mas com menos palavras. TEXTO: "
    content = item["content"]
    
    prompt = header + content
    response = openai.Completion.create(
        prompt=prompt,
        **COMPLETIONS_API_PARAMS
    )

    print("content: " + item["content"] + '\n')
    
    item["summary"] = response["choices"][0]["text"].strip(" \n")
    print("summary:" + item["summary"] + '\n')
    
with open(output_path + output_file, 'w', encoding='utf-8') as f:
  json.dump(data, f, ensure_ascii=False)
          
###################################################




