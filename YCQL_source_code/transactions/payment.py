from decimal import *

def payment(session, C_W_ID, C_D_ID, C_ID, PAYMENT):
    customer, warehouse, district = {}, {}, {}

    # select the customer
    # rows = session.execute("SELECT c_first, c_middle, c_last, c_street_1, c_street_2, c_city, c_state, c_zip, c_phone, c FROM customer WHERE c_w_id = {} AND c_d_id = {} AND c_id = {};".format(C_W_ID, C_D_ID, C_ID))
    rows = session.execute("SELECT * FROM customer WHERE c_w_id = {} AND c_d_id = {} AND c_id = {};".format(C_W_ID, C_D_ID, C_ID))
    
    for row in rows:
        customer = row

    # select the district
    rows = session.execute("SELECT d_street_1, d_street_2, d_city, d_state, d_zip, d_ytd FROM district WHERE d_w_id = {} AND d_id = {};".format(C_W_ID, C_D_ID))
    for row in rows:
        district = row

    # select the customer
    rows = session.execute("SELECT w_street_1, w_street_2, w_city, w_state, w_zip, w_ytd FROM warehouse WHERE w_id = {};".format(C_W_ID))
    for row in rows:
        warehouse = row


    # update the warehouse w_ytd
    new_w_ytd = warehouse.w_ytd + Decimal(PAYMENT)
    session.execute("UPDATE warehouse SET w_ytd = {} WHERE w_id = {};".format(new_w_ytd, C_W_ID))
    # update the district d_ytd
    new_d_ytd = district.d_ytd + Decimal(PAYMENT)
    session.execute("UPDATE district SET d_ytd = {} WHERE d_w_id = {} AND d_id = {};".format(new_d_ytd, C_W_ID, C_D_ID))
    # update the customer
    new_c_ytd_payment = customer.c_ytd_payment + float(PAYMENT)
    new_c_balance = customer.c_balance - Decimal(PAYMENT)
    new_c_payment_cnt = customer.c_payment_cnt + 1
    session.execute("UPDATE customer SET c_balance = {}, c_ytd_payment = {}, c_payment_cnt = {} WHERE c_w_id = {} AND c_d_id = {} AND c_id = {};".format(new_c_balance, new_c_ytd_payment, new_c_payment_cnt, C_W_ID, C_D_ID, C_ID))

    # output
    print(warehouse)
    print(district)
    print(customer)
    print(PAYMENT)
