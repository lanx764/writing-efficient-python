# Writing Efficient Python Code

A structured learning project covering how to write efficient, production-grade Python code for data engineering pipelines.

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

## Project — HR Analytics ETL Pipeline

A multi-stage HR analytics pipeline that fetches employee data from the ReqRes API, enriches it with department budget data, validates and cleans records, applies vectorised transformations, profiles the transform stage, and writes the final report to CSV.

**Topics integrated:** Core Python, File Handling, Pandas, Datetime, JSON, Functions and Pipelines, ETL/ELT Concepts, Data Formats, Reshaping, APIs, Error Handling, OOP, Environment Variables, Logging, Writing Efficient Python

**Efficiency techniques demonstrated:**
- `itertools.chain` for lazy combination of API pages
- Set lookup for O(1) field validation
- `itertools.cycle` for department assignment
- Fully vectorised Pandas transformations — no `.apply()`, no loops
- `np.where` for conditional column assignment
- `cProfile` and `pstats` for transform stage profiling

---

## How to Run the Project

**Prerequisites:**
- Python 3.10+
- Install dependencies: `pip install pandas numpy requests python-dotenv memory-profiler`

**Setup:**
1. Navigate to the `hr_analytics_etl_pipeline` folder
2. Create a `.env` file using `.env.example` as a template
3. Add your ReqRes API key to the `.env` file

**Run:**
```bash
python main.py
```

**Output:**
- `employee_report.csv` — final transformed employee data
- `pipeline.log` — full pipeline log with rotating file handler

---

## Notes

- `.env` is excluded from version control via `.gitignore` — never commit API keys
- `*.csv` output files are excluded from version control
- All configuration lives in `PipelineConfig` — no hardcoded values anywhere in the pipeline