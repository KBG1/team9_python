import mandb

def select_menu(code):
    """
    If you press the button in <MainPage>, the menu associated with the button is added to the list <selected>.
    So a single item will be added to the list.
    Args:
        code: to distinguish which menu button you pressed

    Returns: None

    """
    selected.append([code, getinfo("price", code)])
    print(selected[0][0])

def select_table(menutype, category):
    """
    Select table and bring all data in it.
    Args:
        menutype:
        category:

    Returns:

    """
    if menutype == "A":
        if category == 1:
            sql = "SELECT * FROM menu WHERE category = 1"
        elif category == 2:
            sql = "SELECT * FROM menu WHERE category = 2"
        elif category == 3:
            sql = "SELECT * FROM menu WHERE category = 3"
        elif category == 4:
            sql = "SELECT * FROM menu WHERE category = 4"
        elif category == 5:
            sql = "SELECT * FROM menu WHERE category = 5"
        elif category == 6:
            sql = "SELECT * FROM menu WHERE category = 6"
        elif category == 7:
            sql = "SELECT * FROM menu WHERE category = 7"
    elif menutype == "B":
        if category == 1:
            sql = "SELECT * FROM sets WHERE category = 1"
        if category == 3:
            sql = "SELECT * FROM sets WHERE category = 3"
    else:
        if category == 1:
            sql = "SELECT * FROM menu WHERE category = 1 AND show = 1"
        elif category == 2:
            sql = "SELECT * FROM menu WHERE category = 2 AND show = 1"
        elif category == 3:
            sql = "SELECT * FROM menu WHERE category = 3 AND show = 1"
        elif category == 4:
            sql = "SELECT * FROM menu WHERE category = 4 AND show = 1"
        elif category == 5:
            sql = "SELECT * FROM menu WHERE category = 5 AND show = 1"
        elif category == 6:
            sql = "SELECT * FROM menu WHERE category = 6 AND show = 1"
        elif category == 7:
            sql = "SELECT * FROM menu WHERE category = 7 AND show = 1"
    mandb.mc_cur.execute(sql)

def getinfo(get, code):
    select_table(code[0], int(code[1]))
    menu_info = mandb.mc_cur.fetchall()
    for info in menu_info:
        if info[0] == code:
            if get == "name":
                return info[1]
            elif get == "category":
                return info[2]
            elif get == "type":
                return info[3]  # or code[0]
            elif get == "price":
                return info[4]
            elif get == "cal":
                return info[5]
            else:
                return

def total_to_pay():
    costsum = 0
    sql = "SELECT finalCost FROM orders WHERE subto is NULL"
    mandb.mc_cur.execute(sql)
    amounts = mandb.mc_cur.fetchall()
    for amount in amounts:
        costsum += amount[0]
    print(costsum)
    return costsum

def add_cart(ent):
    sql1 = "SELECT * FROM orders WHERE coupon = 0"
    mandb.mc_cur.execute(sql1)
    order_info = mandb.mc_cur.fetchall()
    # DB에 이미 존재하는 메뉴면 해당 사항 지우고 업데이트
    for order in order_info:
        if order[0] == selected[0][0]:
            sql2 = "DELETE FROM orders WHERE menuID = ?"
            mandb.mc_cur.execute(sql2, (order[0],))
            ent += order[2]
    costsum = ent * getinfo("price", selected[0][0])
    sql = "INSERT INTO orders(menuID, menuName, quantity, finalCost) VALUES(?, ?, ?, ?)"
    val = (selected[0][0], getinfo("name", selected[0][0]), ent, costsum)
    mandb.mc_cur.execute(sql, val)
    mandb.mc_db.commit()
    add_sub_cart(ent)

def add_sub_cart(ent):
    sql1 = "SELECT * FROM orders WHERE subto = ?"
    mandb.mc_cur.execute(sql1, (selected[0][0],))
    order_info = mandb.mc_cur.fetchall()
    for i in range(1, len(selected)):
        costsum = ent * selected[i][1]
        for order in order_info:
            if order[0] == selected[i][0]:
                sql2 = "DELETE FROM orders WHERE menuID = ? AND subto = ?"
                mandb.mc_cur.execute(sql2, (order[0], selected[0][0],))
                ent += order[2]
                costsum += order[3]
        sql = "INSERT INTO orders(menuID, menuName, quantity, finalCost, subto) VALUES(?, ?, ?, ?, ?)"
        val = (selected[i][0], getinfo("name", selected[i][0]), ent, costsum, selected[0][0])
        mandb.mc_cur.execute(sql, val)
        mandb.mc_db.commit()

def setmenu():
    """
    Change the list item to a <set> thing.
    selected[0] is changed to the <set> version of the menu,
    and side/drink menu are added to the list with their <set> cost.
    Returns: None

    """
    selected[0][0] = 'B' + selected[0][0][1:]
    selected.append(['A30052', 0])
    selected.append(['A60102', 0])
    print(selected[1][0][0])

def setlarge():
    selected[1][0] = 'A30053'
    selected[2][0] = 'A60103'

def getextra(num, code):
    """
    Calculate the extra cost by changing the default value of the menu.
    Returns: extra cost

    """
    extra = getinfo("price", code) - getinfo("price", selected[num][0])
    if extra > 0:
        return extra
    else:
        return 0

def changemenu(num, code):
    """
    Change the side/drink menu in the <set> and the list.
    selected[1][0]/selected[2][0] is changed to the menu code which was selected by user.
    selected[1][1]/selected[2][1] is changed to the extra cost compared to original one.
    The changes also apply to the database.
    Args:
        num: to choose the index of list (side or drink)
        code: to know user's menu selection

    Returns: None

    """
    mandb.mc_cur.execute("SELECT menuID FROM orders WHERE menuID = ? AND subto = ?", (selected[num][0], selected[0][0],))
    orig = mandb.mc_cur.fetchone()
    extra = getextra(num, code)
    selected[num] = [code, extra]
    sql = "UPDATE orders SET menuID = ?, menuName = ?, finalCost = ? WHERE menuID = ? AND subto = ?"
    val = (code, getinfo("name", code), extra, orig[0], selected[0][0])
    mandb.mc_cur.execute(sql, val)
    mandb.mc_db.commit()
    mandb.mc_cur.execute("SELECT finalCost FROM orders WHERE menuID = ?", (selected[0][0],))
    orig = mandb.mc_cur.fetchone()
    sql = "UPDATE orders SET finalCost = ? WHERE menuID = ?"
    val = (orig[0]+extra, selected[0][0],)
    mandb.mc_cur.execute(sql, val)
    mandb.mc_db.commit()


menu_type_dict = {1: '버거', 2: '해피스낵', 3: '사이드', 4: '커피', 5: '디저트', 6: '음료', 7: '해피밀'}
menu_row_dict = {1: 7, 2: 3, 3: 5, 4: 5, 5: 5, 6: 5, 7: 1}
selected = []
burger_set_side = ['A30090', 'B30050']
burger_set_drink = ['A60102', 'A60122', 'A60112', 'A60102', 'A60072', 'A60062', 'A40121', 'A40091', 'A40051', 'A40161',
                    'A60030', 'A60040', 'A60050', 'A60020', 'A60010']

