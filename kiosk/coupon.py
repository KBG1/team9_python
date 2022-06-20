import mandb
import random
import string

used = 0

def create_coupon():
    """무작위 문자열 쿠폰 생성.

    영어 대문자+숫자 6자리, 총 7자리의 무작위 문자열 코드를 생성한다.
    메뉴 코드 중 하나를 무작위로 선택한다.
    할인율을 10~100 중 5단위로 무작위 선택한다.
    무작위로 선택된 요소들을 결합한 쿠폰에 대한 정보를 couponDB에 추가한다.

    Notes:
        문자열 생성 방식은 바뀔 수 있습니다.
    """
    num_of_coupons = 8

    menu_list = []
    mandb.mc_cur.execute("SELECT * FROM menu")
    temp = mandb.mc_cur.fetchall()
    for menu in temp:
        if menu[0][0] == "A":
            menu_list.append(menu)
    mandb.mc_cur.execute("SELECT * FROM sets")
    temp2 = mandb.mc_cur.fetchall()
    for setmenu in temp2:
        menu_list.append(setmenu)

    sql = "INSERT INTO coupon VALUES (?, ?, ?, ?, ?, ?)"
    for i in range(num_of_coupons):
        random_ID = random.SystemRandom().choice(string.ascii_uppercase) + ''.join(random.SystemRandom().choice(string.digits) for _ in range(6))
        random_menu = random.choice(menu_list)
        DCrate = random.randrange(10, 101, 5) * 0.01
        DCprice = int(random_menu[4] * DCrate)
        mandb.mc_cur.execute(sql, (random_ID, random_menu[0], random_menu[1], random_menu[4], DCrate, DCprice))
        mandb.mc_db.commit()