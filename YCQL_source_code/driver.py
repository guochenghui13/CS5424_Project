import sys
import time

from cassandra.cluster import Cluster

from transactions.payment import payment
from transactions.delivery import delivery
from transactions.new_order import new_order
from transactions.order_status import order_status
from transactions.top_balance import top_balance
from transactions.stock_level import stock_level
from transactions.related_customer import related_customer
from transactions.popular_item import popular_item

from decimal import *


def main():
    xact_file_name = sys.argv[1]

    cluster = Cluster(['192.168.48.249'])
    session = cluster.connect(keyspace="cs4224n_ycql")
    session.default_timeout = 360

    with open(xact_file_name) as xact_file:
        lines = xact_file.readlines()

        start_time = int(time.time())
        transactions_count = 0


        for (i, line) in enumerate(lines):

            try:
                values = line.strip().split(',')

                transactions_count += 1

                if transactions_count % 5000 == 0:
                    print(transactions_count)
                    print(int(time.time()) - start_time)

                if values[0] == 'N':
                    ITEM_NUMBER, SUPPLIER_WAREHOUSE, QUANTITY = [], [], []
                    NUM_ITEMS = int(values[4])
                    for j in range(i + 1, i + NUM_ITEMS + 1):
                        item_values = lines[j].strip().split(',')
                        ITEM_NUMBER.append(int(item_values[0]))
                        SUPPLIER_WAREHOUSE.append(int(item_values[1]))
                        QUANTITY.append(Decimal(item_values[2]))

                    new_order(session, int(values[2]), int(values[3]), int(values[1]), int(values[4]), ITEM_NUMBER, SUPPLIER_WAREHOUSE, QUANTITY)

                elif values[0] == 'P':
                    payment(session, int(values[1]), int(values[2]), int(values[3]), values[4])

                elif values[0] == 'D':
                    delivery(session, int(values[1]), int(values[2]))

                elif values[0] == 'O':
                    order_status(session, int(values[1]), int(values[2]), int(values[3]))

                elif values[0] == 'S':
                    stock_level(session, int(values[1]), int(values[2]), int(values[3]), int(values[4]))

                elif values[0] == 'I':
                    popular_item(session, int(values[1]), int(values[2]), int(values[3]))

                elif values[0] == 'T':
                    top_balance(session)
                
                elif values[0] == 'R':
                    related_customer(session, int(values[1]), int(values[2]), int(values[3]))

                else:
                    transactions_count -= 1
                    continue

            except Exception as e:
                print(e)

        end_time = int(time.time())
        execution_time = end_time - start_time
        throughput = 0.0
        throughput = transactions_count / execution_time

        print(transactions_count)
        print(execution_time)
        print(throughput)

    






if __name__ == "__main__":
    main()