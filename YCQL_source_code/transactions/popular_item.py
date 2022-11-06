def popular_item(session, W_ID, D_ID, L):

    rows = session.execute("SELECT d_next_o_id FROM district WHERE D_W_ID = {} AND D_ID = {};".format(W_ID, D_ID))
    # print(rows.one() )
    N = rows.one().d_next_o_id

    last_orders = list(session.execute("SELECT o_id, o_entry_d, o_c_id FROM \"order\" WHERE o_w_id = {} AND o_d_id = {} AND o_id >= {} AND o_id < {};".format(W_ID, D_ID, N-L, N)))
    order_count = len(last_orders)
    
    set_item = set()
    map_item = {}
    orders_data = []

    for order in last_orders:
        rows = session.execute("SELECT max(ol_quantity) FROM order_line WHERE ol_w_id = {} AND ol_d_id = {} AND ol_o_id = {} ;".format(W_ID, D_ID, order.o_id))
        # print(rows.one().system_max_ol_quantity )

        item_highest_quantity = rows.one().system_max_ol_quantity
        if item_highest_quantity == None:
            continue
        
        popular_items = session.execute("SELECT ol_i_id, ol_quantity FROM order_line WHERE ol_w_id = {} AND ol_d_id = {} AND ol_o_id = {} AND ol_quantity = {};".format(W_ID, D_ID, order.o_id, item_highest_quantity))
        
        items_data = []
        for item in popular_items:
            set_item.add(item.ol_i_id)
            ol_i_names = session.execute("SELECT i_name FROM item WHERE i_id = {};".format(item.ol_i_id))
            ol_i_name = ol_i_names.one()
            if item.ol_i_id in map_item:
                map_item[item.ol_i_id]['count'] += 1
            else:
                map_item[item.ol_i_id] = {
                    'name': ol_i_name,
                    'count': 1
                }
            items_data.append({
                'quantity': item.ol_quantity,
                'item_name': ol_i_name,
            })

            customers = session.execute("SELECT c_first, c_middle, c_last FROM customer WHERE c_w_id = {} AND c_d_id = {} AND c_id = {};".format(W_ID, D_ID, order.o_c_id))

        orders_data.append({
            'order': order,
            'customer': customers.one(),
            'items': items_data
        })

    items_percentage = []
    for item_id in set_item:
        items_percentage.append({
            'name': map_item[item_id]['name'],
            'percentage': float(map_item[item_id]['count']) / order_count
        })
    
    result = {
        'w_id': W_ID,
        'd_id': D_ID,
        'last_order_count': L,
        'order': orders_data,
        'item_percentage': items_percentage
    }


    # print(result)
