from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import os
import logging
import sys
import requests
import itertools
import pstats
import json
import pandas as pd
import numpy as np
from datetime import date, datetime
import cProfile

load_dotenv()

class PipelineConfig:
    def __init__(self):
        self.api_url = os.getenv("API_URL")
        self.api_key = os.getenv("API_KEY")
        self.budget_file = os.getenv("BUDGET_FILE")
        self.output_file = os.getenv("OUTPUT_FILE")
        self.log_file = os.getenv("LOG_FILE")
        self.max_retries = int(os.getenv("MAX_RETRIES"))

def validate_env(config):
    required = {
        "API_URL": config.api_url,
        "API_KEY": config.api_key,
        "BUDGET_FILE": config.budget_file,
        "OUTPUT_FILE": config.output_file,
        "LOG_FILE": config.log_file,
        "MAX_RETRIES": config.max_retries,
    }

    missing_variables = [key for key,val in required.items() if not val]

    if missing_variables:
        raise EnvironmentError(f"Missing required environment variables: '{', '.join(missing_variables)}'")

def get_logger(name,log_file):
    logger =logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(fmt='%(asctime)s | %(name)s | %(levelname)s | %(funcName)s | %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    rotating_handler = RotatingFileHandler(filename=log_file,maxBytes=1024 * 1024,backupCount=3)
    rotating_handler.setLevel(logging.DEBUG)
    rotating_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(rotating_handler)
    logger.propagate = False

    return logger

class PipelineError(Exception):
    pass

class APIError(PipelineError):
    pass

class ValidationError(PipelineError):
    pass

class TransformError(PipelineError):
    pass

def fetch_employees(config, logger):
    try:
        response1 = requests.get(config.api_url, headers={"x-api-key": config.api_key}, params={"page": 1})
        response1.raise_for_status()
        page1_records = response1.json()["data"]
        logger.info(f"Page 1 returned {len(page1_records)} records")

        response2 = requests.get(config.api_url, headers={"x-api-key": config.api_key}, params={"page": 2})
        response2.raise_for_status()
        page2_records = response2.json()["data"]
        logger.info(f"Page 2 returned {len(page2_records)} records")

    except requests.RequestException as e:
        raise APIError(f"Failed to fetch employees due to: {e}")

    all_records = itertools.chain(page1_records, page2_records)
    return all_records

def load_budgets(config, logger):
    try:
        with open(config.budget_file, "r") as f:
            budgets = json.load(f)
        logger.info(f"Successfully loaded budgets from {config.budget_file}")
        return budgets
    except FileNotFoundError:
        raise PipelineError(f"Budget file not found at path: {config.budget_file}")
    except json.decoder.JSONDecodeError as e:
        raise PipelineError(f"Budget file is malformed : {e}")

def validate_records(all_records,logger):
    required_fields = {"id", "email", "first_name", "last_name"}

    valid_records = []

    for record in all_records:
        missing_fields = required_fields.difference(record.keys())

        if missing_fields:
            logger.warning(f"The record with id : {record["id"]} was rejected due to missing fields: {missing_fields}")
            continue

        if "@" not in record["email"]:
            logger.warning(f"The record with id : {record["id"]} was rejected due to invalid email which doesnt have '@': {record['email']}")
            continue

        valid_records.append(record)

    return valid_records

def enrich_records(valid_records,budgets,logger):
    budget_keys = set(budgets.keys())
    department_names = list(budgets.keys())
    cycled_departments = itertools.cycle(department_names)

    enriched_records = []

    for record in valid_records:
        department = next(cycled_departments)

        record["department"] = department

        if department not in budget_keys:
            logger.warning(f"{department} not found in {budget_keys}")
            continue

        record["budget"] = budgets[department]["budget"]
        record["headcount_limit"] = budgets[department]["headcount_limit"]

        enriched_records.append(record)

    return enriched_records

def transform_records(enriched_records,logger):
    df = pd.DataFrame(enriched_records)
    before = len(df)

    df["full_name"] = df["first_name"] + " " + df["last_name"]
    df["email_domain"] = df["email"].str.split("@").str[1]
    df["salary"] = (df["budget"] / df["headcount_limit"]).round(2)
    df["salary_band"] = np.where(df["salary"] > 50000, "senior", "junior")
    df["ingestion_date"] = date.today().strftime("%Y-%m-%d")

    after = len(df)

    summary_df = df.groupby(["department","salary_band"]).agg(
        employee_count=("full_name","count"),
        average_salary=("salary","mean")).reset_index()

    logger.info(f"{before} records were entered and the final dataframe consists of {after}")

    return df,summary_df

def profile_transform(enriched_records,logger):
    profiler = cProfile.Profile()
    profiler.enable()

    df,summary_df = transform_records(enriched_records,logger)

    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats("cumtime")
    stats.print_stats(5)

    transformed = df,summary_df
    return transformed

def save_report(df,config,logger):
    try:
        df.to_csv(config.output_file,index=False)
        df_rows = len(df)
        logger.info(f"{df_rows} rows were written to {config.output_file}")
    except OSError as e:
        raise PipelineError(f"Writing of the dataframe to {config.output_file} failed: {e}")

def run_pipeline():
    config = PipelineConfig()
    validate_env(config)
    logger = get_logger("main", config.log_file)

    try:
        logger.info(f"Pipeline started : {datetime.now()}")

        employees = list(fetch_employees(config,logger))
        if not employees:
            raise PipelineError("The fetch employees function returned empty values")

        budgets = load_budgets(config,logger)
        if not budgets:
            raise PipelineError("The load budgets function returned empty values")

        valid_records = validate_records(employees,logger)
        if not valid_records:
            raise PipelineError("The validate records function returned empty values")

        enriched_records = enrich_records(valid_records,budgets,logger)
        if not enriched_records:
            raise PipelineError("The enrich records function returned empty values")

        df,summary_df = profile_transform(enriched_records,logger)
        if df.empty or summary_df.empty:
            raise PipelineError("The profile transform function returned empty values")

        save_report(df, config, logger)

    except PipelineError as e:
        logger.exception(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()


# PERFORMANCE THINKING

# 1. Which operation in transform_records would be most expensive at 1 million rows and why?
# the operation in the transform records that would be the most expensive would be the groupby because
# pandas will have to scan all 1 million rows for example it wants to group a certain string it will have to check
# all the rows till it gets to the 1000000 row before it stops the groupby operation then after it applies the count and mean operator also.

# 2. Why is converting the budgets dict keys to a set outside the loop better than inside?
# it is better because the set would be created once reducing the cost so instead of paying simultaneously you pay only once

# 3. What would break first in this pipeline at 10x the data volume?
# the fetch employees function breaks first because the data has already 10x and to get 10x of the data through fetching from api
# the code written in that function only fetched for 2 pages but for 10x it will need more than 2 pages

#  SUMMARY OF THE PIPELINE
# 1. What the pipeline does end to end?
# this pipeline creates a pipeline config class that gets all the required env needed from the .env file and stores it as an attribute
# then also validates the envs to check if any one is missing
# creates a logger that logs relevant infos in the pipeline and stores it in a log file it also creates a stream handler and rotating handler
# the stream handler is the one in charge of outputing the logs to the terminal
# while the rotating file handler is the one in charge of handling the file size of the log and output to the log file and
# the formatter is charge of how the log output is arranged and also uses propagate so the log messages wont be duplicated
# and also uses logger.handler which checks if handlers has been attached to the logger already
# then fetches 2 pages of the employees data needed and merged together
# also loads the budgets file which includes all budgets and department data which will be assigned to each employee
# then validates records meaning removing datas which have missing values and onlys using validated datas to continue th epupeline
# then enrich records by assigning required datas in the budgets json file to each employee
# then transform records by using the data we have from the employees to create new colums of some important infos
# then ranks every function called in the transform records and onl show the top 5 which are slowest 5 functions that ran in transform records
# then saves the final dataframe to the given csc
#
# 2. The decisions i made and why?
# One of the decisions i made was to summarise the dataframe by checking the salary mean and total counts of each department
# so as to see the department that pays well on average and check the number of employees in each department
#
# 3. What i would change if the data volume was 100x larger?
# if the data volume was 100x larger i will change the fetch_employee function by rewriting the code
# in order for the fetch to be fetching automatically until the required number it needs
# unlike this particular function i wrote if the data was 10x the pipeline would fail
# but  i will re write the function so it will be able to be comfortable with any amount of times it is to go and fetch data from the api
# unlike the previous function that as only be customed to run just twice











