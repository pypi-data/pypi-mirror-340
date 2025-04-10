import re

def sozlarga_bolish(matn):

    return re.findall(r'\b\w+\b', matn.lower())

def gaplarga_bolish(matn):

    return re.split(r'[.!?]+\s*', matn.strip())
