def order_status(session, C_W_ID, C_D_ID, C_ID):
    customer, order = {}, {}

    # select the customer
    rows = session.execute("SELECT c_first, c_middle, c_last, c_balance FROM customer WHERE c_w_id = {} AND c_d_id = {} AND c_id = {};".format(C_W_ID, C_D_ID, C_ID))
    for row in rows:
        customer = row
    
    print(customer.c_first, customer.c_middle, customer.c_last, customer.c_balance)

    # select the order
    rows = session.execute("SELECT max(o_id) FROM \"order\" WHERE o_w_id = {} AND o_d_id = {} AND o_c_id = {};".format(C_W_ID, C_D_ID, C_ID))
    O_ID = -1
    for row in rows:
        O_ID = row.system_max_o_id

    if O_ID == -1:
        return

    rows = session.execute("SELECT o_entry_d, o_carrier_id FROM \"order\" WHERE o_w_id = {} AND o_d_id = {} AND o_id = {}".format(C_W_ID, C_D_ID, O_ID))
    for row in rows:
        order = row
    
    print(O_ID, order.o_entry_d, order.o_carrier_id)


    # select the orderlines
    rows = session.execute("SELECT ol_i_id, ol_supply_w_id, ol_quantity, ol_amount, ol_delivery_d FROM order_line WHERE ol_w_id = {} AND ol_d_id = {} AND ol_o_id = {}".format(C_W_ID, C_D_ID, O_ID))
    for row in rows:
        print(row.ol_i_id, row.ol_supply_w_id, row.ol_quantity, row.ol_amount, row.ol_delivery_d)
