import sqlite3
import os

print("open_database called.\n")
mc_db = sqlite3.connect(os.path.abspath('./mcDB'))
mc_cur = mc_db.cursor()

def clear_database():
    sql = "DELETE FROM orders"
    sql2 = "DELETE FROM coupon"
    mc_cur.execute(sql)
    mc_cur.execute(sql2)
    mc_db.commit()

def close_database():
    mc_db.close()
    mc_db.close()
