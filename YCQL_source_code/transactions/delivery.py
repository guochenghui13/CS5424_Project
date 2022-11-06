def delivery(session, W_ID, CARRIER_ID):
    DISTRICT_NO = 0

    while DISTRICT_NO < 10:
        DISTRICT_NO += 1

        # select the min o_id with carrier_id = null
        rows = session.execute("SELECT min(o_id) FROM \"order\" where o_w_id = {} AND o_d_id = {} AND o_carrier_id = -1;".format(W_ID, DISTRICT_NO))
        
        O_ID = -1
        for row in rows:
            O_ID = row.system_min_o_id
        
        # if order with carrier_id = null doesn't exist, skip and continue
        if O_ID == -1:
            continue

        rows = session.execute("SELECT o_c_id FROM \"order\" where o_w_id = {} AND o_d_id = {} AND o_id = {};".format(W_ID, DISTRICT_NO, O_ID))
        C_ID = -1
        for row in rows:
            C_ID = row.o_c_id

        if C_ID == -1:
            continue
        
        # update the carrier_id
        session.execute("UPDATE \"order\" SET o_carrier_id = {} WHERE o_w_id = {} AND o_d_id = {} AND o_id = {};".format(CARRIER_ID, W_ID, DISTRICT_NO, O_ID))


        # update the delivery_date
        rows = session.execute("SELECT ol_number, ol_amount FROM order_line WHERE ol_w_id = {} AND ol_d_id = {} AND ol_o_id = {};".format(W_ID, DISTRICT_NO, O_ID))

        amount = 0
        for row in rows:
            amount += row.ol_amount
            session.execute("UPDATE order_line SET ol_delivery_d = currenttimestamp() WHERE ol_w_id = {} AND ol_d_id = {} AND ol_o_id = {} AND ol_number = {};".format(W_ID, DISTRICT_NO, O_ID, row.ol_number))
        
        # update the customer
        rows = session.execute("SELECT c_balance, c_delivery_cnt FROM customer WHERE c_w_id = {} AND c_d_id = {} AND c_id = {}".format(W_ID, DISTRICT_NO, C_ID))

        c_balance, c_delivery_cnt = 0, 0
        for row in rows:
            c_balance = row.c_balance +  amount
            c_delivery_cnt = row.c_delivery_cnt + 1

        session.execute("UPDATE customer SET c_balance = {}, c_delivery_cnt = {} WHERE c_w_id = {} AND c_d_id = {} AND c_id = {};".format(c_balance, c_delivery_cnt, W_ID, DISTRICT_NO, O_ID, C_ID))

