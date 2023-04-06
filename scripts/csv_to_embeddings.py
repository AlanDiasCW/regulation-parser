import sys
import pandas as pd
import openai
import pickle
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')

if len(sys.argv) < 2:
  print('Usage: python csv_to_embeddings.py input.csv')
  sys.exit(1)

if not sys.argv[1].endswith('csv'):
  print('file needs to be a csv')
  sys.exit(1)

input_file = sys.argv[1]
df = pd.read_csv(input_file)

#DOC_EMBEDDINGS_MODEL = "text-search-curie-doc-001" 
DOC_EMBEDDINGS_MODEL = "text-embedding-ada-002"

def get_embedding(text, model):
    print(text)
    result = openai.Embedding.create(model=model,input=text)
    return result["data"][0]["embedding"]

def compute_doc_embeddings(df):
    #Create an embedding for each row in the dataframe using the OpenAI Embeddings API.
    #Return a dictionary that maps between each embedding vector and the index of the row that it corresponds to.
    return {
        #idx: get_embedding(row.content.replace("\n", " "),DOC_EMBEDDINGS_MODEL) for idx, row in df.iterrows()
        idx: get_embedding(row[0].replace("\n", " "),DOC_EMBEDDINGS_MODEL) for idx, row in df.iterrows()
    }

document_embeddings = compute_doc_embeddings(df)

output_file = input_file.split('.')[0] + '.pkl'

pickle.dump(document_embeddings,open(output_file, "wb"))

