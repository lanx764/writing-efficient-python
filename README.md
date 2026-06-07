# Writing Efficient Python Code

A structured learning project covering how to write efficient, production-grade 
Python code for data engineering pipelines.

---

## Topics Covered

- Big O notation and data structure selection (list vs set vs dict)
- Memory efficiency with generators and lazy evaluation
- Itertools for composable, memory-efficient iteration
- Built-in functions (map, filter, zip, enumerate) and Pandas vectorisation
- Profiling tools: timeit, cProfile, memory_profiler

---

## Mini Projects

| Folder | What it covers |
|---|---|
| `list_vs_set_lookup_performance` | Benchmarks list vs set membership lookup and demonstrates O(1) hashing vs O(n) linear search |
| `generators_and_lazy_evaluation` | Compares eager file loading vs lazy generator-based reading and measures memory difference |
| `itertools_chain_islice_batched` | Uses itertools.chain, islice, and batched to process multi-region records lazily |
| `map_filter_and_pandas_vectorisation` | Applies map and filter for lazy transformation and uses vectorised Pandas operations instead of loops |
| `timeit_benchmarking` | Benchmarks for loop vs list comprehension using timeit.timeit and timeit.repeat |
| `cprofile_pipeline_profiling` | Profiles a four-stage pipeline using cProfile and pstats to identify the bottleneck function |
| `memory_profiler_comparison` | Compares line-by-line memory usage of eager vs lazy approaches using memory_profiler |

---

## Combined Project

The combined project for this topic has its own dedicated repository:
[HR Analytics ETL Pipeline](https://github.com/lanx764/hr-analytics-etl-pipeline)