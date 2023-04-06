import json
import os
import sys
from datetime import datetime

#FIRST LINE HAS TO BE THE NAME
#THEN INTRO
#THEN EVERYTHING ELSE

def read_chunk(file):
  chunk = ''
  eof = True
  
  for line in file:
      if (line.startswith('Seção') or  
          line.startswith('CAPÍTULO') or 
          line.startswith('Art.')) :
            eof = False
            break
      else :
        chunk += line.strip() + ' '
  
  if eof:
     line = 'eof'     
  
  return chunk,line

def parse_regulation(file_path):
    parsed_regulation = []

    with open(file_path, 'r') as f:
        
        ######title
        regulation_name = f.readline().strip()
        
        ######intro
        intro, line = read_chunk(f)
        
        parsed_regulation = [
          {
            "name": regulation_name,
            "chapter" : "Introdução",
            "section" : "",
            "article" : "",
            "content" : intro
          }
        ]

        line_start = line.split()[0]
        
        regulation_element = {
            "name": regulation_name,
            "chapter" : "",
            "section" : "",
            "article" : "",
            "content" : ""
          }

        def chapter(regulation_element, current_line):
            first_line = current_line.strip() + ' '
            
            chunk, line = read_chunk(f)
            
            chunk = first_line + chunk

            chapter = chunk[len("CAPÍTULO"):].strip() #removes redundant "CAPÍTULO"

            print("CAPÍTULO: "+ chapter)

            new_element = {
              "name": regulation_element["name"],
              "chapter" : "",
              "section" : "",
              "article" : "",
              "content" : ""
            }

            line_start = line.split()[0]
            new_chapter = regulation_element["chapter"] != chapter 
            if regulation_element["chapter"] == '' : 
              regulation_element["chapter"] = chapter
              options[line_start](regulation_element,line)
            elif new_chapter:
              new_element["chapter"] = chapter
              parsed_regulation.append(new_element)
              options[line_start](new_element,line)
            else:
              options[line_start](regulation_element,line)  
                        
        def section(regulation_element, current_line):
            first_line = current_line.strip() + ' '
            chunk, line = read_chunk(f)
            chunk = first_line + chunk
            section = chunk[len("SEÇÃO"):].strip()

            print("SEÇÃO: "+ section)
            
            new_element = {
                "name": regulation_element["name"],
                "chapter" : regulation_element["chapter"],
                "section" : "",
                "article" : "",
                "content" : ""
              }


            line_start = line.split()[0]
            new_section = regulation_element["section"] != section
            if regulation_element["section"] == '': 
              regulation_element["section"] = section
              options[line_start](regulation_element,line)
            elif new_section:
              new_element["section"] = section
              parsed_regulation.append(new_element)
              options[line_start](new_element,line)
            else:
              options[line_start](regulation_element,line)  

        def article(regulation_element, current_line):
            article = current_line.split()[1]
            current_line = current_line[(len('Art. ') + len(article) + 1):]

            chunk, line = read_chunk(f)
            chunk = current_line + chunk
            
            new_element = {
              "name": regulation_element["name"],
              "chapter" : regulation_element["chapter"],
              "section" : regulation_element["section"],
              "article" : regulation_element["article"],
              "content" : ""
            }

            line_start = line.split()[0]

            new_article = regulation_element["article"] != article
            if regulation_element["article"] == '' : 
              regulation_element["article"] = article
              regulation_element["content"] = chunk
              parsed_regulation.append(regulation_element)
              options[line_start](regulation_element,line)
            elif new_article:
              new_element["article"] = article
              new_element["content"] = chunk
              parsed_regulation.append(new_element)
              options[line_start](new_element,line)
            else:
              print('Artigo Duplicado, deve ser treta!')
              breakpoint()
              options[line_start](new_element,line)
        
        def finish_parse(regulation_element,current_line):
          return 

        options = {
            "CAPÍTULO": chapter,
            "Seção": section,
            "Art.": article,
            "eof": finish_parse
          }

        options[line_start](regulation_element,line)

        return parsed_regulation

# Get the input file name from command line arguments
if len(sys.argv) < 2:
  print("Usage: python script.py input_file.html")
  sys.exit(1)

if not sys.argv[1].endswith('txt'):
  print('file needs to be a txt')
  sys.exit(1)

input_file = sys.argv[1]

parent_dir = os.path.dirname(os.getcwd())
input_path = os.path.join(parent_dir, "files/txt/")
output_path = os.path.join(parent_dir, "files/json/")

print('starting txt to json: ' + input_file)

regulation_array = parse_regulation(input_path + input_file)

#Construct the output file name
output_file = os.path.splitext(input_file)[0] + ".json"

# Write the paragraphs to a json file
with open(output_path + output_file, 'w', encoding='utf-8') as f:
    # write the JSON object to the file
    json.dump(regulation_array, f, ensure_ascii=False)

print('finished txt to json: ' + input_file)

