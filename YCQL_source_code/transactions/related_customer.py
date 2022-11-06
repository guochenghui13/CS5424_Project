def related_customer(session, C_W_ID, C_D_ID, C_ID):
    
    c_orders = session.execute("SELECT o_id FROM \"order\" where o_w_id = {} and o_d_id = {} and o_c_id = {};".format(C_W_ID, C_D_ID, C_ID))

    c_item_set_list = []
    for c_order in c_orders:
        c_item_set = set()
        c_order_lines = session.execute("SELECT ol_i_id FROM order_line where ol_w_id = {} and ol_d_id = {} and ol_o_id = {};".format(C_W_ID, C_D_ID, c_order.o_id))
        for c_order_line in c_order_lines:
            c_item_set.add(c_order_line.ol_i_id)
        c_item_set_list.append(c_item_set)

    
    neighbours = set()
    for item_set in c_item_set_list:
        scores = {}
        for item in item_set:
            related_orders = session.execute("SELECT OL_W_ID, OL_D_ID, OL_O_ID FROM order_line where ol_i_id = {};".format(item))
            for wid, did, oid in related_orders:
                if wid == C_W_ID:
                    continue
                if (wid, did, oid) not in scores:
                    scores[(wid, did, oid)] = 0
                scores[(wid, did, oid)] += 1
        for identifier, score in scores.items():
            if score >= 2:
                wid, did, oid = identifier
                customers = session.execute("SELECT o_w_id, o_d_id, o_c_id FROM \"order\" where o_w_id = {} and o_d_id = {} and o_id = {};".format(wid, did, oid))
                customer = customers.one()
                neighbours.add((customer.o_w_id, customer.o_d_id, customer.o_c_id))
    
    # Print output
    # print("Customer <W_ID>, <D_ID>, <C_ID>")
    # print(f"{C_W_ID}, {C_D_ID}, {C_ID}")
    # print("Related customers <W_ID>, <D_ID>, <C_ID>")
    # for wid, did, oid in neighbours:
    #     print(f"{wid}, {did}, {oid}")

