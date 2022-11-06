def new_order(session, W_ID, D_ID, C_ID, NUM_ITEMS, ITEM_NUMBER, SUPPLIER_WAREHOUSE, QUANTITY):
    W_TAX = 0
    rows = session.execute("SELECT w_tax FROM warehouse WHERE w_id = {};".format(W_ID))
    for row in rows:
        W_TAX = row.w_tax

    C_DISCOUNT = 0
    rows = session.execute("SELECT c_discount FROM customer WHERE c_w_id = {} AND c_d_id = {} AND c_id = {};".format(W_ID, D_ID, C_ID))
    for row in rows:
        C_DISCOUNT = row.c_discount    

    # select and update the d_next_o_id
    D_NEXT_O_ID = -1
    D_TAX = 0
    rows = session.execute("SELECT d_next_o_id, d_tax FROM district WHERE d_w_id = {} AND d_id = {};".format(W_ID, D_ID))
    for row in rows:
        D_NEXT_O_ID = row.d_next_o_id + 1
        D_TAX = row.d_tax
    
    session.execute("UPDATE district SET d_next_o_id = {} WHERE d_w_id = {} AND d_id = {};".format(D_NEXT_O_ID, W_ID, D_ID))
    D_NEXT_O_ID = D_NEXT_O_ID - 1

    # Create a new order
    O_ALL_LOCAL = 1
    for warehouse in SUPPLIER_WAREHOUSE:
        if warehouse != W_ID:
            O_ALL_LOCAL = 0
            break

    session.execute("INSERT INTO \"order\" (o_id, o_d_id, o_w_id, o_c_id, o_entry_d, o_carrier_id, o_ol_cnt, o_all_local) VALUES ({}, {}, {}, {}, currenttimestamp(), -1, {}, {});".format(D_NEXT_O_ID, D_ID, W_ID, C_ID, NUM_ITEMS, O_ALL_LOCAL))

    # Initialize TOTAL AMOUNT = 0
    TOTAL_AMOUNT = 0

    # update the stock
    for i in range(NUM_ITEMS):
        S_QUANTITY, S_YTD, S_ORDER_CNT, S_REMOTE_CNT = 0, 0, 0, 0
        rows = session.execute("SELECT s_quantity, s_ytd, s_order_cnt, s_remote_cnt FROM stock WHERE s_w_id = {} AND s_i_id = {};".format(SUPPLIER_WAREHOUSE[i], ITEM_NUMBER[i]))
        for row in rows:
            S_QUANTITY = row.s_quantity
            S_YTD = row.s_ytd
            S_ORDER_CNT = row.s_order_cnt
            S_REMOTE_CNT = row.s_remote_cnt
        
        ADJUSTED_QTY = S_QUANTITY - QUANTITY[i]
        if ADJUSTED_QTY < 10:
            ADJUSTED_QTY += 100

        S_YTD += QUANTITY[i]

        S_ORDER_CNT += 1

        if SUPPLIER_WAREHOUSE[i] != W_ID:
            S_REMOTE_CNT += 1
        

        session.execute("UPDATE stock SET s_quantity = {}, s_ytd = {}, s_order_cnt = {}, s_remote_cnt = {} WHERE s_w_id = {} AND s_i_id = {};".format(S_QUANTITY, S_YTD, S_ORDER_CNT, S_REMOTE_CNT, SUPPLIER_WAREHOUSE[i], ITEM_NUMBER[i]))
    
        # create a new order line
        I_PRICE = 0
        rows = session.execute("SELECT i_price FROM item WHERE i_id = {}".format(ITEM_NUMBER[i]))
        for row in rows:
            I_PRICE = row.i_price
        
        ITEM_AMOUNT = QUANTITY[i] * I_PRICE
        TOTAL_AMOUNT += ITEM_AMOUNT

        session.execute("INSERT INTO order_line (ol_o_id, ol_d_id, ol_w_id, ol_number, ol_i_id, ol_supply_w_id, ol_quantity, ol_amount, ol_dist_info) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, \'{}\');".format(D_NEXT_O_ID, D_ID, W_ID, i + 1, ITEM_NUMBER[i], SUPPLIER_WAREHOUSE[i], QUANTITY[i], ITEM_AMOUNT, "S_DIST_" + str(D_ID)))

    # calculate the TOTAL AMOUNT
    TOTAL_AMOUNT = TOTAL_AMOUNT * (1 + D_TAX + W_TAX) * (1 - C_DISCOUNT)
    # print(TOTAL_AMOUNT)
