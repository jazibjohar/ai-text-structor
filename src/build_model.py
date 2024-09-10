import json
from pydantic_core import from_json
from pydantic import  Field, create_model
from typing import Annotated



def load_json(file_path):
    with open(file_path) as json_data:
        d = json.load(json_data)
        json_data.close()
        return d

def build_pydantic_model(attributes):
    obj = from_json(json.dumps(attributes), allow_partial=True)
    annotated_fields = {}
    for key, value in obj.items():
        annotated_fields[key] = Annotated[type(value), Field(description=value)]
    DynamicModel = create_model('DynamicModel', **annotated_fields)    
    return DynamicModel


