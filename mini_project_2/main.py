# it will show us that a list object is always larger than a generator object
# because a list keeps on storing while a generator gives a result and after been used it discards it


import sys

def read_errors_eager(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()

    error_lines = []
    for line in lines:
        if line.startswith("ERROR"):
            error_lines.append(line)

    return error_lines

def read_errors_lazy(filepath):
    with open(filepath, "r") as f:
        for line in f:
            if line.startswith("ERROR"):
                yield line

eager_result = read_errors_eager("pipeline.log")
print("These are the errors found in the function read_errors_eager:")
for line in eager_result:
    print(f"{line}")

lazy_result = read_errors_lazy("pipeline.log")
print("These are the errors line found in the function read_errors_lazy:")
for line in lazy_result:
    print(f"{line}")

size_of_v1 = sys.getsizeof(eager_result)
print(f"The size of function read_errors_eager is {size_of_v1}bytes")

lazy_result = read_errors_lazy("pipeline.log")
size_of_v2 = sys.getsizeof(lazy_result)
print(f"The size of function read_errors_lazy is {size_of_v2}bytes")

