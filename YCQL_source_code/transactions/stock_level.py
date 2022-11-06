def stock_level(session, W_ID, D_ID, T, L):

    # compute the next available order number D NEXT O ID for district
    rows = session.execute("SELECT d_next_o_id FROM district WHERE D_W_ID = {} AND D_ID = {};".format(W_ID, D_ID))
    N = rows.one().d_next_o_id

    # compute the set of items from the last L orders for district
    rows = session.execute("SELECT ol_i_id FROM order_line WHERE ol_d_id = {} and ol_w_id = {} AND ol_o_id >= {} and ol_o_id < {};".format(D_ID, W_ID, N-L, N))
    item_ids = list(set([row.ol_i_id for row in rows]))

    # Output the total number of items where its stock quantity is below the threshold;
    cnt = 0
    for item_id in item_ids:
        rows = session.execute("SELECT s_quantity FROM stock WHERE s_w_id = {} AND s_i_id = {};".format(W_ID, item_id))
        if rows.one().s_quantity < T:
            cnt += 1

    print(cnt)