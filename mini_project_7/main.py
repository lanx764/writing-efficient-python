from memory_profiler import profile

@profile
def eager_squares():
    data = list(range(1_000_000))
    squared = [x ** 2 for x in data]
    return squared

@profile
def lazy_squares():
    data = range(1_000_000)
    squared = (x ** 2 for x in data)
    return list(squared)

eager = eager_squares()
lazy = lazy_squares()


# 1. the data list created with range and the new list squared that is being created
# 2. The generator expression adds no memory because it only stores only instructions, not data.
# 3. 106.5 MiB for eager. and 103.8 for lazy with the difference of 2.7