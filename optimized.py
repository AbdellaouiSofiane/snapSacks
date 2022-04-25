import csv
import sys; sys.setrecursionlimit(10000)
from decimal import Decimal
from datetime import datetime


FILE_PATH = 'test-data.csv'
MAX_PORTFOLIO_VALUE = 500


def get_data(file):
    with open(file) as csv_file:
        reader = csv.DictReader(csv_file)
        return [row for row in reader]


def timer(func):
    """Decorator for calculating function's execution time"""
    def wrapper():
        start_time = datetime.now()
        func()
        end_time = datetime.now()
        print("run-time:", (end_time - start_time).seconds, "s")
    return wrapper


def knapsack(shares_price_list, shares_profit_list, portfolio_value, nb_shares, matrix):
  
    # Base case
    if nb_shares == 0 or portfolio_value == 0:
        return 0

    # Skip if already computed
    if matrix[nb_shares][portfolio_value] != -1:
        return matrix[nb_shares][portfolio_value]

    # If share price greater than portfolio_value then exclude that share.
    if shares_price_list[nb_shares - 1] > portfolio_value:
        matrix[nb_shares][portfolio_value] = knapsack(
            shares_price_list,
            shares_profit_list,
            portfolio_value,
            nb_shares-1,
            matrix
        )
        return matrix[nb_shares][portfolio_value]

    # We compute the portfolio profit in case we choose to keep the share
    profits_with_share = (
        shares_profit_list[nb_shares - 1]
        + knapsack(
            shares_price_list,
            shares_profit_list,
            portfolio_value - shares_price_list[nb_shares - 1],
            nb_shares - 1,
            matrix
        )
    )

    # We compute the portfolio profit in case we choose to discard the share
    profits_without_share = knapsack(
        shares_price_list,
        shares_profit_list,
        portfolio_value,
        nb_shares - 1,
        matrix
    )

    # We return the best choice
    matrix[nb_shares][portfolio_value] = max(profits_with_share, profits_without_share)
    return matrix[nb_shares][portfolio_value]


@timer
def main():

    # Extract the data from the csv file
    data = get_data(FILE_PATH)
    nb_shares = len(data)

    # Constract a list of share prices (in cents)
    shares_name_list = [row['name'] for row in data]

    # Constract a list of share prices (in cents)
    shares_price_list = [
        int(float(row['price']) * 100) for row in data
    ]

    # Constract a list of share profits
    shares_profit_list = [
        Decimal(row['price']) * Decimal(row['profit']) / Decimal("100")
        for row in data
    ]

    # Init a matrix of dimension (nb_shares, MAX_PORTFOLIO_VALUE(in cents))
    matrix = [
        [
            -1 for i in range(MAX_PORTFOLIO_VALUE * 100 + 1)
        ] for j in range(nb_shares + 1)
    ]

    # Compute max portfolio profits
    max_profit = knapsack(
        shares_price_list,
        shares_profit_list,
        MAX_PORTFOLIO_VALUE * 100,
        nb_shares, matrix
    )
    print(f"Max portfolio profits: {max_profit}$")

    # Retrive and display chosen shares
    weight = MAX_PORTFOLIO_VALUE * 100
    for i in range(nb_shares, 0, -1):
        if max_profit <= 0:
            break
        if max_profit == matrix[i - 1][weight]:
            continue
        print(shares_name_list[i - 1])

        max_profit -= shares_profit_list[i - 1]
        weight -= shares_price_list[i - 1]


if __name__ == '__main__':
    main()
