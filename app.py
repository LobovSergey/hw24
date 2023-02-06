import os

from dataclasses import dataclass
from typing import  List

import marshmallow_dataclass

from flask import Flask, request, render_template


from utils import data_processing

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CMD = ('filter', 'map', 'unique', 'sort', 'limit', 'regex')


@dataclass
class Data:
    file_name: str
    cmd1: str
    value1: str
    cmd2: str
    value2: str


@app.post("/perform_query/")
def perform_query() -> tuple[str, int]:
    try:
        data_schema = marshmallow_dataclass.class_schema(Data)
        data: Data = data_schema().load(data=request.json)
    except Exception:
        return f'no data', 400

    try:
        command_1 = data.cmd1
        command_2 = data.cmd2
        value_1 = data.value1
        value_2 = data.value2
    except TypeError:
        return 'No command', 400

    if command_1 and command_2 not in CMD:
        return f'Unsupprted types', 400

    try:
        file_path = os.path.join(DATA_DIR, data.file_name)
        with open(file_path, 'r', encoding='UTF-8') as file:
            data_file: List[str] = file.read().rstrip().split('\n')
            first_response = data_processing(command=command_1, value=value_1, data=data_file)
            second_response = data_processing(command=command_2, value=value_2, data=first_response)
        return render_template('response.html', data_file=second_response), 200

    except FileNotFoundError:
        return f'File {data.file_name} does not exist', 400


if __name__ == "__main__":
    app.run(debug=True)
