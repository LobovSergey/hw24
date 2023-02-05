import re
from typing import List, Optional


def data_processing(command: str, value: Optional[str], data: List[str]) -> List[str]:
    if command == "filter":
        return [string for string in data if value in string]
    elif command == "map":
        return [string.split(' ')[int(value) - 1] for string in data]
    elif command == "unique":
        return list(set(data))
    elif command == "sort":
        if value == "desc":
            return sorted(data, reverse=True)
        else:
            return sorted(data, reverse=False)
    elif command == "limit":
        return data[:int(value)]
    elif command == 'regex':
        return [string for string in data if re.compile(value).search(string)]
