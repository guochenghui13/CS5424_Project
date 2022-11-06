def top_balance(session):

    # select all customers
    customers = session.execute("SELECT c_w_id, c_d_id, C_FIRST, C_MIDDLE, C_LAST,  C_BALANCE FROM customer ;")
    # sort customers according to their balance
    sorted_customers = sorted(customers, key=lambda x: x.c_balance, reverse=True)

    # output the related information on top-10 customers
    for customer in sorted_customers[:10]:
        # print("Name of customer:", customer.c_first, customer.c_middle, customer.c_last)
        # print("Balance of customer's outstanding payment", customer.c_balance)

        w_names = session.execute("SELECT w_name FROM warehouse where w_id = {};".format(customer.c_w_id))
        d_names = session.execute("SELECT d_name FROM district where d_w_id = {} and d_id = {};".format(customer.c_w_id, customer.c_d_id))
        # print('Warehouse name of customer', w_names.one().w_name)
        # print('District name of customer:', d_names.one().d_name)

