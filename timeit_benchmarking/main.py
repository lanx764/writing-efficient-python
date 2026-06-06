import timeit

# The real reason is this: every time Python calls .append() in the loop,
# it has to look up the append method on the list object, then call it as a function,
# then return from it. That method lookup and function call overhead happens 1000 times.
# That is pure Python interpreter overhead on every single iteration.
# A list comprehension is implemented at the C level inside Python's interpreter.
# It does not call .append() at all — it builds the list directly using an internal bytecode instruction called LIST_APPEND which bypasses the Python method lookup entirely.
# That is why it is faster — less Python interpreter overhead per item.

def squared_list():
    loop_list = []
    for num in range(1000):
        loop_list.append(num**2)

result1 = timeit.timeit(
    stmt=lambda: squared_list(),
    number=5000
)

result2 = timeit.timeit(
    stmt="[num**2 for num in range(1000)]",
    setup="pass",
    number=5000
)

print(f"Average time per run : {result1 / 5000:.6f}s")
print(f"Average time per run : {result2 / 5000:.6f}s")

result3 = timeit.repeat(
    stmt=lambda: squared_list(),
    number=5000,
    repeat=5
)

result4 = timeit.repeat(
    stmt="[num**2 for num in range(1000)]",
    number=5000,
    repeat=5
)

print(result3)
print(min(result3))

print(result4)
print(min(result4))


