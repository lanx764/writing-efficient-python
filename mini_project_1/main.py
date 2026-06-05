import time
import random

# the reason why v2 is faster is because it uses hash to search which just jump straight to what it is searchinfg for unlike v1 which check each and every value in the list which makes it slower

currency_pool = ["USD", "EUR", "GBP", "NGN", "XYZ", "ABC", "DEF", "KES", "ZAR", "QQQ"]

valid_currencies = ["USD", "EUR", "GBP", "JPY", "NGN", "KES", "ZAR", "CAD", "AUD", "CHF"]

def filter_valid_transactions_v1(transactions,valid_currencies):
    valid_transactions_v1 = []
    for transaction in transactions:
        if transaction["currency"] in valid_currencies:
            valid_transactions_v1.append(transaction)
    return valid_transactions_v1

def filter_valid_transactions_v2(transactions,valid_currencies):
    valid_transactions_v2 = []
    valid_currencies_set = set(valid_currencies)
    for transaction in transactions:
        if transaction["currency"] in valid_currencies_set:
            valid_transactions_v2.append(transaction)
    return valid_transactions_v2

large_fake_transactions = []
for num in range(1,100001):
    large_fake_transactions.append({"id" : num ,"currency" : random.choice(currency_pool),"amount" : random.randint(1,1001)})

start_v1 = time.perf_counter()
v1_result = filter_valid_transactions_v1(large_fake_transactions,valid_currencies)
end_v1 = time.perf_counter()
time_taken_v1 = end_v1 - start_v1


start_v2 = time.perf_counter()
v2_result = filter_valid_transactions_v2(large_fake_transactions,valid_currencies)
end_v2 = time.perf_counter()
time_taken_v2 = end_v2 - start_v2

print(v1_result)
print(v2_result)
print(f"time taken for version 1 was : {time_taken_v1} seconds and found {len(v1_result)} valid transactions")
print(f"time taken for version 2 was :{time_taken_v2} seconds and found {len(v2_result)} valid transactions")



