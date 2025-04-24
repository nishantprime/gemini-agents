from google import genai
from pydantic import BaseModel
import enum
import os

client = genai.Client(api_key= 'Replace with your api key')   # enter api key

query = input('give an order -> ')

class Task(enum.Enum):
  CREATEFOLDER = "create_folder"
  CREATETEXTFILE = "create_txt"

class actions(BaseModel):
    step_num: int 
    action: Task
    entity_name: str
    path: str
    content: str

response = client.models.generate_content(
    model= 'gemini-2.0-flash',
    contents = '''You are a file managing assistant. You are to understand the user's request and give out a list of commands in order,
                        which will attain the expected results. You can create folders, text files. For creations, give the name for the object, path (local=./)
                        , dont pass extentions. and for generation of text files, give some content too. In case of no content needed, pass None. \n\n assigment = ''' + query,
    config={
        'response_mime_type': 'application/json',
        'response_schema': list[actions]
    }

    )

commands: list[actions] = response.parsed


def txt_file(path_,name,content):
    n = os.path.join(path_, name.replace(' ','_') + '.txt')
    with open(n, 'w') as f:
        f.write(content)

def make_folder(path,name):
    os.mkdir(path + name.replace(' ','_'))

    

for c in commands:
    print(c)
    if c.action == Task.CREATEFOLDER:
        if not input(f'press enter to confirm action - create folder, {c.path}{c.entity_name}'):
            make_folder(c.path,c.entity_name)
        else:
            if input('Enter "n" to stop further actions: ').lower() == 'n':
                break
    elif c.action == Task.CREATETEXTFILE:
        if not input(f'press enter to confirm action - create text file, {c.path}{c.entity_name}'):
            txt_file(c.path,c.entity_name,c.content)
        else:
            if input('Enter "n" to stop further actions: ').lower() == 'n':
                break
