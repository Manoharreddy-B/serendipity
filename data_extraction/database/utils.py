def convert_transaction_to_list(transactions):
    result = {}
    for transaction in transactions:
        uid, uname, email, sid, sname, qty, typ, value = transaction
        transaction_details = {
                'stockName': sname,
                'qty': qty,
                'type': typ,
                'value': value,
        }
        if(uid in result):
            result[uid]['stocks'].append(transaction_details)
        else:
            details = {
            'uid' : uid,
            'name' : uname,
            'email' : email,
            'stocks' : [transaction_details]
            }
            result[uid] = details
              
    return list(result.values())