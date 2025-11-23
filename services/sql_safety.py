import re

def is_safe(query):
    dangerous = [
        r"DROP\s+TABLE",
        r"DELETE\s+FROM",
        r"TRUNCATE",
        r"ALTER\s+TABLE",
        r"UPDATE\s+\w+\s+SET\s+(?!.*WHERE)",
        r"INSERT\s+INTO\s+\w+\s+VALUES"
    ]

    for rule in dangerous:
        if re.search(rule, query, re.IGNORECASE):
            return False
    return True
