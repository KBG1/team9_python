import mandb
import menu

balance = 1000000
rewards = 0

def total_without_dc():
    costsum = 0
    sql = "SELECT * FROM orders"
    mandb.mc_cur.execute(sql)
    orderlist = mandb.mc_cur.fetchall()
    for order in orderlist:
        if order[4] is None:
            costsum += menu.getinfo("price", order[0]) * order[2]
        else:
            costsum += order[3] * order[2]
    return costsum