import csv
from decimal import Decimal
import itertools

FILE_PATH = 'test.csv'
MAX_PORTFOLIO_VALUE = 500


def get_data(file):
    with open(file) as csv_file:
        reader = csv.DictReader(csv_file)
        return [row for row in reader]


def get_total_cost(vector, data):
    return sum(
        Decimal(stock['price'])
        for index, stock in enumerate(data)
        if int(vector[index])
    )


def get_total_profit(vector, data):
    return sum(
        Decimal(stock['price']) * Decimal(stock['profit']) / Decimal("100")
        for index, stock in enumerate(data)
        if int(vector[index])
    )


def get_best_portfolio(data):
    porftolio = {}
    for portfolio_weights in itertools.product('01', repeat=len(data)):
        total_cost = get_total_cost(portfolio_weights, data)
        if total_cost > MAX_PORTFOLIO_VALUE:
            continue
        total_profit = get_total_profit(portfolio_weights, data)

        if total_profit > porftolio.get('profit', 0):
            porftolio['cost'] = total_cost
            porftolio['profit'] = total_profit
            porftolio['weights'] = portfolio_weights

    return porftolio


def display_portfolio_composition(data, portfolio):
    print("portfolio composition:")
    for index, stock in enumerate(data):
        if int(portfolio['weights'][index]):
            print('\t', stock['name'])
    print('Total cost: ', portfolio['cost'])
    print('Total profit: ', portfolio['profit'])


def main():
    data = get_data(FILE_PATH)
    best_portfolio = get_best_portfolio(data)
    display_portfolio_composition(data, best_portfolio)


if __name__ == '__main__':
    main()