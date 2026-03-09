import marshal
import dis
import sys

pyc_file = r"E:\8th Sem\MAJOR\Documind\training_intent\__pycache__\split_dataset.cpython-311.pyc"

with open(pyc_file, "rb") as f:
    f.read(16)  # skip header
    code = marshal.load(f)

dis.dis(code)