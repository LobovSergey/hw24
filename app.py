import os
from dataclasses import dataclass
from typing import Optional, Union

from flask import Flask, request, render_template

from utils import data_processing

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@dataclass
class Data:
    file_name: str
    cmd1: str
    value1: Optional[str, int]
    cmd2: str
    value2: Optional[str, int]


@app.post("/perform_query/", method=["POST"])
def perform_query():
    try:
        data: Data = request.json
    except Exception as e:
        return f'no data {e}'

    try:
        file_path = os.path.join(DATA_DIR, data.file_name)
    except TypeError:
        return f'Не передан аргумент "file_name"', 400

    try:
        cmd1 = data.cmd1
        cmd2 = data.cmd2
        val1 = data.value1
        val2 = data.value2
    except FileNotFoundError:
        return f'File {data.file_name} does not exist', 400

    with open(file_path, 'r', encoding='UTF-8') as file:
        data_file = file.read().rstrip().split('\n')
        first_response = data_processing(command=cmd1, value=val1, data=data_file)
        second_response = data_processing(command=cmd2, value=val2, data=first_response)

    # добавить команду regex
    # добавить типизацию в проект, чтобы проходила утилиту mypy app.py
