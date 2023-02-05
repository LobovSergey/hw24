import os

from dataclasses import dataclass
from typing import Any, Optional, Type

import marshmallow_dataclass

from flask import Flask, request, render_template
from marshmallow import Schema

from utils import data_processing

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@dataclass
class Data:
    file_name: str
    cmd1: str
    value1: Optional[str]
    cmd2: str
    value2: Optional[str]


@app.post("/perform_query/")
def perform_query() -> tuple[str, int]:
    try:
        response: Optional[Any] = request.json
        DataSchema: Type[Schema] = marshmallow_dataclass.class_schema(Data)
        data: Data = DataSchema().load(response)

    except Exception:
        return f'no data file', 400

    file_path = os.path.join(DATA_DIR, data.file_name)

    try:
        command_1 = data.cmd1
        command_2 = data.cmd2
        value_1 = data.value1
        value_2 = data.value2
    except TypeError:
        return f'Unsupprted types', 400

    try:
        with open(file_path, 'r', encoding='UTF-8') as file:
            data_file = file.read().rstrip().split('\n')
            first_response = data_processing(command=command_1, value=value_1, data=data_file)
            second_response = data_processing(command=command_2, value=value_2, data=first_response)
        return render_template('response.html', data_file=second_response), 200

    except FileNotFoundError:
        return f'File {data.file_name} does not exist', 400


if __name__ == "__main__":
    app.run(debug=True)
