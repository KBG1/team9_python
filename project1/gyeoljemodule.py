import tkinter as tk                # for window
import tkinter.font as tkfont       # for font
from PIL import Image, ImageTk      # for image
import sqlite3 as sql3              # for DB
import string                       # for random code
import random                       # for random code
import uuid
import time                         # 사용x


# 기본 창 정보+프레임 전환하는 함수 #
class DemoPro(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)                    # 처음 실행하면 첫 페이지로 전환
        self.geometry("480x800+500+5")                  # 창 크기 및 위치; 제 노트북 기준으로 가운데인데 다른 컴퓨터 기준으로는 다를 것 같네요
        self.resizable(False, False)
        self.configure(bg="#ffffff")
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

    # 프레임 전환 함수 #
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


# 사용된 폰트 리스트 #
class Font:
    def __init__(self):
        self.title_font = tkfont.Font(family="맑은 고딕", size=24, weight="bold")
        self.font2 = tkfont.Font(family="맑은 고딕", size=16)


# 카드 관련 정보 #
class PersonalCard:
    # 카드 잔액; default=100만원
    card_balance = 1000000
    # 적립금
    rewards_point = 0
    # 최종 결제금액(할인 등 적용된)
    final_cost = 0


# 메뉴 관련 정보 #
class MenuInfo:
    # 메뉴코드-메뉴명
    menu_code = {10001: "빅맥", 10002: "맥너겟", 10003: "콜라"}
    # 메뉴코드-선택여부; 메뉴버튼 누르면 0->1, 선택창에서 이전이나 선택완료 누르면 1->0
    select_check = {10001: 0, 10002: 0, 10003: 0}
    # 메뉴코드-수량
    menu_quantity = {10001: 0, 10002: 0, 10003: 0}
    # 메뉴코드-개당 가격
    menu_price = {10001: 8000, 10002: 3000, 10003: 1500}
    # 주문 총액(할인 전)
    order_ttl = 0


# 쿠폰 관련 정보 #
class Coupon:
    # 쿠폰타입-할인 금액에 따른 쿠폰 종류
    coupon_type = {0: "전액", 1: "10%", 2: "30%", 3: "50%"}
    # 쿠폰타입-할인율
    discnt_price = {0: 1, 1: 0.1, 2: 0.3, 3: 0.5}


# 사용된 이미지 리스트 #
class ImageOpen:
    def __init__(self):
        # MainPage - 결제하기
        self.mv_pay_btn_img = Image.open('pic/button/mv_pay_btn.png')
        self.mv_pay_btn_img = self.mv_pay_btn_img.resize((100, 100))
        self.mv_pay_btn_img = ImageTk.PhotoImage(self.mv_pay_btn_img)
        # MainPage - 처음으로
        self.go_startp_btn_img = Image.open('pic/button/gomain.png')
        self.go_startp_btn_img = self.go_startp_btn_img.resize((100, 30))
        self.go_startp_btn_img = ImageTk.PhotoImage(self.go_startp_btn_img)
        # MainPage - 전체취소
        self.reset_btn_img = Image.open('pic/button/reset_cart.png')
        self.reset_btn_img = self.reset_btn_img.resize((150, 30))
        self.reset_btn_img = ImageTk.PhotoImage(self.reset_btn_img)
        # OrderCheckPage - 전체취소
        self.cc_btn_img = Image.open('pic/button/cc_btn.png')
        self.cc_btn_img = self.cc_btn_img.resize((200, 133))
        self.cc_btn_img = ImageTk.PhotoImage(self.cc_btn_img)
        # open_entry 함수(메뉴 선택창) - 이전
        self.go_back_btn_img = Image.open('pic/button/goback.png')
        self.go_back_btn_img = self.go_back_btn_img.resize((150, 50))
        self.go_back_btn_img = ImageTk.PhotoImage(self.go_back_btn_img)
        # open_entry 함수(메뉴 선택창) - 선택완료
        self.choose_btn_img = Image.open('pic/button/choose.png')
        self.choose_btn_img = self.choose_btn_img.resize((150, 50))
        self.choose_btn_img = ImageTk.PhotoImage(self.choose_btn_img)


# DB 열기 - 수정 요망 #
class OpenDB:
    def __init__(self):
        # orderTable column: menuID/menuName/quantity/finalCost/updateTime
        # menuID: 메뉴코드, menuName: 메뉴명, quantity: 수량, finalCost: 수량*개당가격, updateTime: 최종업데이트시각
        self.order_DB = sql3.connect("orderDB")
        self.cur = self.order_DB.cursor()
        # couponTable column: couponID/menuName/type/discntPrice
        # couponID: 쿠폰코드, menuName: 메뉴명, type: 종류(기프티콘/할인), discntPrice: 할인금액
        self.coupon_DB = sql3.connect("couponDB")
        self.cur2 = self.coupon_DB.cursor()

    def create_coupon(self):    # 값이 들어가긴 하는데... 왜 리스트박스에 안 뜨지?
        num_of_coupons = 4
        sql = "INSERT INTO couponTable VALUES (?, ?, ?, ?)"
        for i in range(num_of_coupons):
            temp0 = uuid.uuid4()
            temp1 = random.choice(list(MenuInfo.menu_code.keys()))
            temp = MenuInfo.menu_code[temp1]
            temp2 = random.choice(list(Coupon.coupon_type.keys()))

            # 할인금액(할인되는 금액)
            temp3 = MenuInfo.menu_price[temp1] * Coupon.discnt_price[temp2]
            self.cur2.execute(sql, (str(temp0), temp, temp2, temp3))
            self.coupon_DB.commit()


# 공통 이용 클래스 상속 #
class Sharing(tk.Frame, Font, ImageOpen, OpenDB):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        Font.__init__(self)
        ImageOpen.__init__(self)
        OpenDB.__init__(self)


# 첫 화면 페이지 #
# 실질적으로 tk.Frame, Font, ImageOpen, OpenDB 클래스 상속합니다.
class StartPage(Sharing):
    def __init__(self, master):
        Sharing.__init__(self, master)

        # DB 초기화 - 창 껐다가 다시 켰을 때 초기화되게 #
        self.cur.execute("DELETE FROM orderTable")
        self.order_DB.commit()
        self.cur2.execute("DELETE FROM couponTable")
        self.coupon_DB.commit()

        # 쿠폰 생성 #
        self.create_coupon()

        # 프레임 리스트 #
        # 광고 프레임
        self.ad_frm = tk.Frame(self, width=480, height=550, relief="solid", bd=1)
        self.ad_frm.pack(fill="both", expand=True)
        self.ad_frm.propagate(False)
        # 버튼 프레임
        self.btn_frm = tk.Frame(self, width=480, height=250, relief="solid", bd=1)
        self.btn_frm.pack(fill="both", expand=True)
        self.btn_frm.propagate(False)

        # in button frame #
        tk.Button(self.btn_frm, text="쿠폰 사용", font=self.font2, relief="solid", bd=1,
                  command=lambda: master.switch_frame(CouponPage)).place(x=50, y=70, width=180, height=180)
        tk.Button(self.btn_frm, text="주문하기", font=self.font2, relief="solid", bd=1,
                  command=lambda: master.switch_frame(ForHerePage)).place(x=250, y=70, width=180, height=70)
        tk.Button(self.btn_frm, text="언어", font=self.font2, relief="solid", bd=1
                  ).place(x=250, y=150, width=85, height=35)
        tk.Button(self.btn_frm, text="도움 기능", font=self.font2, relief="solid", bd=1
                  ).place(x=345, y=150, width=85, height=35)


# 쿠폰 사용 페이지 #
class CouponPage(Sharing):
    def __init__(self, master):
        Sharing.__init__(self, master)
        
        # 프레임 리스트 #
        # 쿠폰창
        self.mobile = tk.Toplevel(app)
        self.mobile.geometry("300x500+180+20")
        # 안내메세지 프레임
        self.announce_frm = tk.Frame(self, width=480, height=150, relief="solid", bd=1)
        self.announce_frm.pack(fill="both", expand=True)
        self.announce_frm.propagate(False)
        # 이미지 프레임
        self.cp_img_frm = tk.Frame(self, width=480, height=550, relief="solid",bd=1)
        self.cp_img_frm.pack(fill="both", expand=True)
        self.announce_frm.propagate(False)
        # 입력 프레임
        self.entry_frm = tk.Frame(self, width=480, height=100, relief="solid", bd=1)
        self.entry_frm.pack(fill="both", expand=True)
        self.entry_frm.propagate(False)

        # in mobile window #
        tk.Label(self.mobile, text="사용 가능한 쿠폰", font=self.font2).pack()
        self.coupon_lb = tk.Listbox(self.mobile)
        self.coupon_lb.place(x=0, y=50, width=300, height=400)

        # in announce frame #
        tk.Label(self.announce_frm, text="쿠폰 번호를 입력해 주세요", font=self.title_font).pack()

        # in entry frame #
        self.ent = tk.Entry(self.entry_frm)
        self.ent.place(x=115, y=0, width=250, height=50)
        self.ok_btn = tk.Button(self.entry_frm, text="확인", command=lambda: self.check_coupon(str(self.ent.get())))
        self.ok_btn.place(x=215, y=50, width=50, height=30)

    def show_coupon(self):
        self.cur2.execute("SELECT * FROM couponTable")
        while True:
            couponlist = self.cur2.fetchone()
            if couponlist is None: break
            code = couponlist[2]
            self.coupon_lb.insert(0, "%s %s %s %d" % (couponlist[0], couponlist[1], Coupon.coupon_type[code], couponlist[3]))

    def check_coupon(self, ent):
        self.cur2.execute("SELECT couponID FROM couponTable")
        cp_code = self.cur2.fetchall()
        for code in cp_code:
            if code[0] == ent:
                print("Right")



# 테이크아웃 여부 확인 페이지 #
class ForHerePage(Sharing):
    def __init__(self, master):
        Sharing.__init__(self, master)

        # 프레임 리스트 #
        # 안내메세지 프레임
        self.announce_frm = tk.Frame(self, width=480, height=200)
        self.announce_frm.pack(fill="both", expand=True)
        self.announce_frm.propagate(False)
        # 버튼 프레임
        self.btn_frm = tk.Frame(self, width=480, height=200)
        self.btn_frm.pack(fill="both", expand=True)
        self.btn_frm.propagate(False)
        # 기타 버튼 프레임
        self.etc_frm = tk.Frame(self, width=480, height=400)
        self.etc_frm.pack(fill="both", expand=True)
        self.etc_frm.propagate(False)

        # in announce frame #
        # 안내메세지 출력
        tk.Label(self.announce_frm, text="식사 방법을\n선택해 주세요", font=self.title_font).place(x=145, y=70)

        # in button frame #
        # 테이크아웃 여부 버튼 - 두 버튼 모두 누르면 MainPage로 프레임 전환
        tk.Button(self.btn_frm, text="매장에서 식사", font=self.font2, relief="solid", bd=1,
                  command=lambda: master.switch_frame(MainPage)).place(x=80, y=0, width=150, height=200)
        tk.Button(self.btn_frm, text="테이크 아웃", font=self.font2, relief="solid", bd=1,
                  command=lambda: master.switch_frame(MainPage)).place(x=250, y=0, width=150, height=200)


# 메뉴 선택 페이지 #
class MainPage(Sharing):
    def __init__(self, master):
        Sharing.__init__(self, master)

        # 초기화 - 임시로 수정함. 뒤로가기 등에 대비해 다시 수정 필요 #
        MenuInfo.order_ttl = 0
        # 메뉴 선택창 열렸는지 체크하는 변수 #
        self.ent_open_check = 0

        # 프레임 리스트 #
        # 로고 프레임 - StartPage로 넘어가는 버튼 및 로고
        self.logo_frm = tk.Frame(self, width=480, height=100)
        self.logo_frm.grid(row=0, column=0, sticky="nswe")
        # 메뉴 버튼 프레임
        self.menu_btn_frm = tk.Frame(self, width=480, height=500, bg="#ffffff", relief="solid", bd=2)
        self.menu_btn_frm.grid(row=1, column=0, sticky="nswe")
        # 메뉴-카트 사이 빈 공간 프레임
        self.qu_frm = tk.Frame(self, width=480, height=50, relief="solid", bd=2)
        self.qu_frm.grid(row=2, column=0, sticky="nswe")
        # 카트 프레임 - 장바구니, 총액 정보, 전체취소, 결제하기 버튼
        self.cart_frm = tk.Frame(self, width=480, height=100, relief="solid", bd=2)
        self.cart_frm.grid(row=3, column=0, sticky="nswe")
        # 카드잔액 프레임
        self.card_frm = tk.Frame(self, width=480, height=50, relief="solid", bd=2)
        self.card_frm.grid(row=4, column=0, sticky="nswe")

        # in logo frame #
        # 처음으로 버튼 - StartPage로 프레임 전환
        self.go_startp_btn = tk.Button(self.logo_frm, image=self.go_startp_btn_img, relief="flat", bd=0,
                                       command=lambda: [self.reset_cart(), master.switch_frame(StartPage)])
        self.go_startp_btn.place(x=20, y=50, width=100, height=30)

        # in menu button frame #
        # 메뉴 버튼 - 각 버튼 누르면 메뉴 세부사항 선택창 열림
        tk.Button(self.menu_btn_frm, text="빅맥\n8000원", bg="#ffffff", relief="ridge", bd=1,
                  command=lambda: self.open_entry(10001)).place(x=0, y=0, width=160, height=133)
        tk.Button(self.menu_btn_frm, text="맥너겟\n3000원", bg="#ffffff", relief="ridge", bd=1,
                  command=lambda: self.open_entry(10002)).place(x=160, y=0, width=160, height=133)
        tk.Button(self.menu_btn_frm, text="콜라\n1500원", bg="#ffffff", relief="ridge", bd=1,
                  command=lambda: self.open_entry(10003)).place(x=320, y=0, width=160, height=133)

        # in cart frame #
        # 장바구니
        self.cart_lbox = tk.Listbox(self.cart_frm, width=60, height=5)
        self.cart_lbox.place(x=0, y=0, width=280, height=100)
        # 총액 정보란
        tk.Label(self.cart_frm, text="총액", font=self.font2).place(x=280, y=0)
        self.ttlprice_lb = tk.Listbox(self.cart_frm, relief="flat", bd=0)
        self.ttlprice_lb.place(x=280, y=30, width=120, height=50)
        self.ttlprice_lb.insert(0, "￦ %d" % MenuInfo.order_ttl)
        # 전체취소 버튼 - DB, 장바구니, 총액 리셋
        tk.Button(self.cart_frm, image=self.reset_btn_img, relief="flat", bd=0,
                  command=self.reset_cart).place(x=280, y=70, width=120, height=30)
        # 결제하기 버튼 - OrderCheckPage로 프레임 전환
        tk.Button(self.cart_frm, image=self.mv_pay_btn_img, relief="flat", bd=0,
                  command=lambda: master.switch_frame(OrderCheckPage)).place(x=400, y=0, width=80, height=100)

        # in menu frame #
        # 카드 잔액 정보
        tk.Label(self.card_frm, text="카드 잔액: %d 원" % PersonalCard.card_balance).pack()

    # 총액 계산 #
    def calcul_sum(self):
        MenuInfo.order_ttl = 0
        # DB에서 finalCost 받아옴
        self.cur.execute("SELECT finalCost FROM orderTable")
        # DB에 존재하는 finalCost 모두 더해서 총액 계산
        while True:
            cost = self.cur.fetchone()
            if cost is None: break
            MenuInfo.order_ttl = MenuInfo.order_ttl + cost[0]
        # 총액 정보란 표시 업데이트
        self.ttlprice_lb.delete(0, "end")
        self.ttlprice_lb.insert(0, "￦ %d" % MenuInfo.order_ttl)

    # 메뉴 세부사항 선택창 띄우기 #
    def open_entry(self, code):
        MenuInfo.select_check[code] = 1
        # 메뉴 세부사항 선택창 
        entry_tk = tk.Toplevel(app)
        entry_tk.geometry("480x600+500+120")
        # 메뉴 사진란
        tk.Button(entry_tk, text="메뉴사진", relief="flat").place(x=25, y=30, width=100, height=100)
        tk.Label(entry_tk, text="%s" % MenuInfo.menu_code[code]).place(x=150, y=30)
        # 메뉴 수량 입력란; default=1
        ent = tk.Entry(entry_tk)
        ent.place(x=150, y=100, width=30)
        ent.insert(0, "1")
        # 메뉴 수량 [+] 버튼; 수량 + 1
        plus_btn = tk.Button(entry_tk, text="+", relief="ridge", command=lambda: incordec("plus"))
        plus_btn.place(x=190, y=100, width=20, height=20)
        # 메뉴 수량 [-] 버튼; 수량 - 1
        minus_btn = tk.Button(entry_tk, text="-", relief="ridge", command=lambda: incordec("minus"))
        minus_btn.place(x=120, y=100, width=20, height=20)
        # (메뉴 수량 * 개당가격) 보여줌
        price_lb = tk.Listbox(entry_tk, relief="flat", bd=0)
        price_lb.place(x=400, y=100, width=100, height=15)
        price_lb.insert(0, "￦ %d" % (MenuInfo.menu_price[code] * int(ent.get())))
        # 선택완료 버튼 - DB에 정보 입력, 장바구니 업데이트, 총액 정보란 업데이트 및 선택창 닫음
        tk.Button(entry_tk, image=self.choose_btn_img, relief="flat", bd=0,
                  command=lambda: [self.enter_orderDB(int(ent.get())), self.enter_cart(), self.calcul_sum(),
                                   tk_destroy()]).place(x=280, y=520, width=150, height=50)
        # 이전 버튼 - 선택창 닫음
        tk.Button(entry_tk, image=self.go_back_btn_img, relief="flat", bd=0,
                  command=lambda: tk_destroy()).place(x=70, y=520, width=150, height=50)

        # [+], [-] 버튼 작동 함수 #
        def incordec(op):
            num = int(ent.get())
            if op == "plus":
                ent.delete(0, "end")
                ent.insert(0, "%d" % (num + 1))
                price_lb.delete(0, "end")
                price_lb.insert(0, "￦ %d" % (MenuInfo.menu_price[code] * int(ent.get())))
            elif op == "minus":
                if num <= 1:
                    return
                ent.delete(0, "end")
                ent.insert(0, "%d" % (num - 1))
                price_lb.delete(0, "end")
                price_lb.insert(0, "￦ %d" % (MenuInfo.menu_price[code] * int(ent.get())))

        # 선택창 닫기 함수 #
        def tk_destroy():
            MenuInfo.select_check[code] = 0
            entry_tk.destroy()

    # 장바구니 업데이트 함수 #
    def enter_cart(self):
        # 장바구니 내용 초기화
        self.cart_lbox.delete(0, "end")
        # DB에서 menuName, quantity 최종업데이트시간순(오름차순)으로 받아와서 장바구니에 추가
        self.cur.execute("SELECT menuName, quantity FROM orderTable ORDER BY datetime(updateTime) ASC")
        while True:
            data = self.cur.fetchone()
            if data is None: break
            self.cart_lbox.insert(0, "메뉴: %s 수량: %d\n" % (data[0], data[1]))

    # DB 추가/수정 함수 #
    def enter_orderDB(self, quantity):
        # DB에서 menuID 받아옴
        self.cur.execute("SELECT menuID FROM orderTable")
        rows = self.cur.fetchall()
        for code in MenuInfo.select_check.keys():
            # 현재 선택되어 있는 메뉴에 대하여
            if MenuInfo.select_check[code] == 1:
                for row in rows:
                    # DB에 이미 존재하는 메뉴면 입력 개수만큼 quantity 더하고 fianlCost 수정해서 업데이트
                    if row[0] == code:
                        MenuInfo.menu_quantity[code] = MenuInfo.menu_quantity[code] + quantity
                        ttlprice = MenuInfo.menu_price[code] * MenuInfo.menu_quantity[code]
                        sql = "UPDATE orderTable SET quantity = ?, finalCost = ?,\
                               updateTime = datetime('now', 'localtime') WHERE menuID = ?"
                        self.cur.execute(sql, (MenuInfo.menu_quantity[code], ttlprice, code))
                        self.order_DB.commit()
                        return
                # DB에 존재하지 않는 메뉴면 새로 추가
                mncode = code
                mnname = MenuInfo.menu_code[code]
                MenuInfo.menu_quantity[code] = quantity
                ttlprice = MenuInfo.menu_price[code] * quantity
                sql = "INSERT INTO orderTable(menuID, menuName, quantity, finalCost) VALUES(?, ?, ?, ?)"
                vals = (mncode, mnname, quantity, ttlprice)
                self.cur.execute(sql, vals)
                self.order_DB.commit()
                return

    # DB, 장바구니, 총액 정보란 초기화 #
    def reset_cart(self):
        # DB 초기화
        self.cur.execute("DELETE FROM orderTable")
        self.order_DB.commit()
        # 장바구니 초기화
        self.cart_lbox.delete(0, "end")
        # 총액 정보 초기화
        MenuInfo.order_ttl = 0
        self.ttlprice_lb.delete(0, "end")
        self.ttlprice_lb.insert(0, "￦ %d" % MenuInfo.order_ttl)
        # 메뉴 수량 초기화
        for code in MenuInfo.menu_quantity.keys():
            MenuInfo.menu_quantity[code] = 0


# 주문내역 페이지 #
class OrderCheckPage(Sharing):
    def __init__(self, master):
        Sharing.__init__(self, master)

        # 프레임 리스트 #
        # 주문내역 프레임
        self.orderlist_frm = tk.Frame(self, width=480, height=480, relief="solid", bd=2)
        self.orderlist_frm.pack(fill="both", expand=True)
        self.orderlist_frm.propagate(False)
        # 안내메세지 프레임
        self.announce_frm = tk.Frame(self, width=480, height=100, relief="solid", bd=2)
        self.announce_frm.pack(fill="both", expand=True)
        self.announce_frm.propagate(False)
        # 버튼 프레임
        self.mv_btn_frm = tk.Frame(self, width=480, height=100, relief="solid", bd=2)
        self.mv_btn_frm.pack(fill="both", expand=True)
        self.mv_btn_frm.propagate(False)

        # in orderlist frame #
        # 주문내역 출력
        self.show_orderlist()

        # in announce frame #
        # 총액 정보란
        self.ordercost = tk.Label(self.announce_frm, text="합계          %d" % MenuInfo.order_ttl,
                                  width=480, height=100, font=self.font2)
        self.ordercost.pack()

        # in move button frame #
        # 다음 버튼 - PaymentPage로 프레임 전환
        tk.Button(self.mv_btn_frm, image=self.mv_pay_btn_img,
                  command=lambda: master.switch_frame(PaymentPage)).place(x=300, y=0, width=100, height=100)
        # 이전 버튼 - MainPage로 프레임 전환, MainPage의 장바구니랑 총액 정보란 업데이트(미구현)
        tk.Button(self.mv_btn_frm, text="이전",
                  command=lambda: [master.switch_frame(MainPage)]).place(x=200, y=0, width=100, height=100)
        # 전체취소 버튼 - DB, 장바구니, 총액 정보 등 초기화(미구현)
        tk.Button(self.mv_btn_frm, image=self.cc_btn_img,
                  command=lambda: master.switch_frame(MainPage)).place(x=100, y=0, width=100, height=100)

    # 주문내역 출력 함수 #
    def show_orderlist(self):
        # '주문' 텍스트
        tk.Label(self.orderlist_frm, text="주문", font=self.title_font).place(x=30, y=10)
        # 주문내역 리스트(장바구니랑 메커니즘 비슷함)
        order_lbox = tk.Listbox(self.orderlist_frm, width=60, height=5, font=self.font2, relief="flat", bd=0)
        order_lbox.place(x=150, y=80, width=350, height=100)
        self.cur.execute("SELECT menuID, menuName, quantity FROM orderTable ORDER BY datetime(updateTime) ASC")
        rows = self.cur.fetchall()
        for menu in rows:
            # 각각의 주문내역 옆 취소 버튼 누르면 해당 주문내역은 DB 및 리스트에서 삭제되게.. 구현하고 싶었음(미구현)
            cc_btn = tk.Button(self.orderlist_frm, text="취소", command=lambda: cc_menu(menu[0]),
                               relief="ridge", borderwidth=1)
            cc_btn.place(x=30, y=90, width=80, height=20)
            # DB에서 SELECT한 정보들 입력
            order_lbox.insert(0, "%s %d" % (menu[1], menu[2]))

        # 주문내역 옆 취소 버튼(미구현)
        def cc_menu(code):
            sql = "DELETE FROM orderTable WHERE menuID = ?"
            self.cur.execute(sql, (code,))
            self.order_DB.commit()
            order_lbox.delete(0)


# 결제수단 선택 페이지 #
class PaymentPage(Sharing):
    def __init__(self, master):
        Sharing.__init__(self, master)

        # 프레임 리스트 #
        # 안내메세지 프레임
        self.announce_frm = tk.Frame(self, width=480, height=150, relief="solid", bd=1)
        self.announce_frm.pack(fill="both", expand=True)
        self.announce_frm.propagate(False)
        # 버튼 프레임
        self.select_btn_frm = tk.Frame(self, width=480, height=650, relief="solid", bd=1)
        self.select_btn_frm.pack(fill="both", expand=True)
        self.select_btn_frm.propagate(False)

        # in announce frame #
        # 안내메세지 출력
        tk.Label(self.announce_frm, text="결제 방법을 선택해 주세요", font=self.title_font).place(x=120, y=50)

        # in select button frame #
        # 카드 결제 버튼 - DisCountPage로 프레임 전환
        tk.Button(self.select_btn_frm, text="카드 결제\nCARD PAYMENT", font=self.font2,
                  command=lambda: master.switch_frame(DisCountPage)).place(x=75, y=20, width=150, height=150)
        # 모바일 상품권 버튼 - 쿠폰 관련 Page로 프레임 전환(미구현), 현재는 DisCountPage로 프레임 전환
        tk.Button(self.select_btn_frm, text="모바일 상품권\nMOBILE GIFT CARD", font=self.font2,
                  command=lambda: master.switch_frame(DisCountPage)).place(x=225, y=20, width=150, height=150)

# 할인수단 선택 페이지 #
class DisCountPage(Sharing):
    def __init__(self, master):
        Sharing.__init__(self, master)

        # 프레임 리스트 #
        # 할인수단 선택 버튼 프레임
        self.chs_discnt_frm = tk.Frame(self, width=480, height=667, relief="solid", bd=1)
        self.chs_discnt_frm.pack(fill="both", expand=True)
        self.chs_discnt_frm.propagate(False)
        # 기타 버튼 프레임
        self.etc_frm = tk.Frame(self, width=480, height=133, relief="solid", bd=1)
        self.etc_frm.pack(fill="both", expand=True)
        self.etc_frm.propagate(False)

        # in choose discount method frame #
        # 적립금 버튼 - DisCountReWards로 프레임 전환
        self.opt1 = tk.Button(self.chs_discnt_frm, text="적립금", command=lambda: master.switch_frame(DisCountRewards))
        self.opt1.place(x=0, y=0, width=240, height=333)
        # 없음(그냥 결제) 버튼 - 결제 진행, ReceiptPage로 프레임 전환
        self.opt2 = tk.Button(self.chs_discnt_frm, text="없음(그냥 결제)", width=27, height=4,
                              command=lambda: self.pay_sequence(master))
        self.opt2.place(x=240, y=0, width=240, height=333)

        # in etc frame #
        # 첫 화면으로 버튼 - MainPage로 프레임 전환
        tk.Button(self.etc_frm, text="첫 화면으로\n(결제 취소)",
                  command=lambda: [master.switch_frame(MainPage)]).place(x=200, y=666, width=200, height=133)

    # 결제 진행 함수 - 수정 요망 #
    def pay_sequence(self, master):
        # DB에서 finalCost 불러와서 전부 더하고 최종 결제금액->PersonalCard.final_cost
        # 카드 잔액에서 최종 결제금액만큼 제함->PersonalCard.card_balance
        # 적립금 1% 적립->PersonalCard.rewards_point
        self.cur.execute("SELECT finalCost FROM orderTable")
        cost_list = self.cur.fetchall()
        for cost_data in cost_list:
            PersonalCard.final_cost = PersonalCard.final_cost + cost_data[0]
        print("작동확인\n")
        if PersonalCard.card_balance >= PersonalCard.final_cost:
            print("정상결제 작동확인\n")
            PersonalCard.card_balance = PersonalCard.card_balance - PersonalCard.final_cost
            PersonalCard.rewards_point = PersonalCard.final_cost * 0.01
            master.switch_frame(ReceiptPage)
        else:
            print("금액부족 작동확인\n")
            Error_tk = tk.Toplevel(app)
            Error_tk.geometry("400x100+540+350")
            Error_msg = tk.Label(Error_tk, text="금액이 부족합니다.\n")
            Error_msg.pack()
            master.switch_frame(StartPage)


# 적립금 사용 페이지 #
class DisCountRewards(Sharing):
    def __init__(self, master):
        Sharing.__init__(self, master)

        # 프레임 리스트 #
        # 안내메시지 프레임
        self.announce_frm = tk.Frame(self, width=480, height=667, relief="solid", bd=1)
        self.announce_frm.pack(fill="both", expand=True)
        self.announce_frm.propagate(False)
        # 버튼 프레임
        self.btn_frm = tk.Frame(self, width=480, height=133, relief="solid", bd=1)
        self.btn_frm.pack(fill="both", expand=True)
        self.btn_frm.propagate(False)

        # in announce frame #
        # 안내메세지 출력
        self.announce1 = tk.Label(self.announce_frm, text="적립금을 사용해 할인하시겠습니까?")
        self.announce1.place(x=0, y=0, width=480, height=30)
        self.announce2 = tk.Label(self.announce_frm, text="적립금 %d point" % PersonalCard.rewards_point)
        self.announce2.place(x=0, y=30, width=480, height=30)
        # 적립금이 5000점 미만인 경우 안내메세지 출력
        if PersonalCard.rewards_point < 5000:
            self.announce4 = tk.Label(self.announce_frm, text="적립금이 5000점 미만이므로 사용할 수 없습니다.")
            self.announce4.place(x=0, y=90, width=480, height=30)
        # 적립금이 5000점 이상인 경우 할인 후 결제 금액 출력
        else:
            # 적립금이 결제 금액 이상인 경우
            if PersonalCard.rewards_point >= MenuInfo.order_ttl:
                self.announce3 = tk.Label(self.announce_frm,
                                          text="할인 후 결제 금액 %d" % 0)
                self.announce3.place(x=0, y=60, width=480, height=30)
            # 결제 금액이 적립금 이상인 경우
            else:
                self.announce3 = tk.Label(self.announce_frm,
                                          text="할인 후 결제 금액 %d" % (MenuInfo.order_ttl - PersonalCard.rewards_point))
                self.announce3.place(x=0, y=60, width=480, height=30)

        # in button frame #
        # 사용하기 버튼 - 적립금이 5000점 미만인 경우 버튼 비활성화
        if PersonalCard.rewards_point < 5000:
            self.button1 = tk.Button(self.btn_frm, text="사용하기", state=tk.DISABLED)
            self.button1.place(x=300, y=0, width=200, height=133)
        # 적립금이 5000점 이상인 경우 활성화, 결제 진행
        else:
            self.button1 = tk.Button(self.btn_frm, text="사용하기", command=lambda: self.pay_sequence(master))
            self.button1.place(x=300, y=0, width=200, height=133)
        # 취소 버튼 - DisCountPage로 프레임 전환
        self.button2 = tk.Button(self.btn_frm, text="취소", command=lambda: master.switch_frame(DisCountPage))
        self.button2.place(x=100, y=0, width=200, height=133)

    # 결제 진행 함수 #
    def pay_sequence(self, master):
        # DB에서 finalCost 불러와서 전부 더하고 적립금만큼 제한 최종 결제금액->PersonalCard.final_cost
        # 카드 잔액에서 최종 결제금액만큼 제함->PersonalCard.card_balance
        # 적립금 1% 적립->PersonalCard.rewards_point
        self.cur.execute("SELECT finalCost FROM orderTable")
        cost_list = self.cur.fetchall()
        for cost_data in cost_list:
            PersonalCard.final_cost = PersonalCard.final_cost + cost_data[0]
        print("작동확인\n")
        # 적립금과 총액 크기 비교해서 계산
        if PersonalCard.final_cost >= PersonalCard.rewards_point:
            print("비교 작동확인\n")
            PersonalCard.final_cost = PersonalCard.final_cost - PersonalCard.rewards_point
            PersonalCard.rewards_point = 0
        else:
            print("비교2 작동확인\n")
            PersonalCard.rewards_point = PersonalCard.rewards_point - PersonalCard.final_cost
            PersonalCard.final_cost = 0
        # 최종 결제
        if PersonalCard.card_balance >= PersonalCard.final_cost:
            print("정상결제 작동확인\n")
            PersonalCard.card_balance = PersonalCard.card_balance - PersonalCard.final_cost
            PersonalCard.rewards_point = PersonalCard.rewards_point + PersonalCard.final_cost * 0.01
            master.switch_frame(ReceiptPage)
        else:
            print("금액부족 작동확인\n")
            Error_tk = tk.Toplevel(app)
            Error_msg = tk.Label(Error_tk, text="금액이 부족합니다.\n")
            Error_msg.pack()
            master.switch_frame(StartPage)


# 결제완료 페이지 #
class ReceiptPage(Sharing):
    def __init__(self, master):
        Sharing.__init__(self, master)

        # 프레임 리스트 #
        # 안내메세지 프레임
        self.summary_frm = tk.Frame(self, width=480, height=300, relief="solid", bd=2)
        self.summary_frm.pack(fill="both", expand=True)
        self.summary_frm.propagate(False)
        # 기타 버튼 프레임
        self.etc_frm = tk.Frame(self, width=480, height=100, relief="solid", bd=2)
        self.etc_frm.pack(fill="both", expand=True)
        self.etc_frm.propagate(False)

        # in summary frame #
        # 안내메세지 출력
        tk.Label(self.summary_frm, text="결제가 완료되었습니다.\n", font=self.title_font).pack()
        tk.Label(self.summary_frm, text="주문한 상품을 잘 받아가시길 바랍니다.\n", font=self.font2).pack()

        # in etc frame #
        # 첫 화면으로 버튼 - StartPage로 프레임 전환
        self.mv_main_btn = tk.Button(self.etc_frm, text="첫 화면으로",
                                     command=lambda: [self.clear_DB(), master.switch_frame(StartPage)])
        self.mv_main_btn.pack(side="left")
        # 영수증 보기 버튼 - 결제 관련 세부사항 출력
        self.show_rcpt_btn = tk.Button(self.etc_frm, text="영수증 보기",
                                       command=self.new_tk_receipt)
        self.show_rcpt_btn.pack(side="left")

    # 영수증 출력 함수 #
    def new_tk_receipt(self):
        # 영수증창 띄움
        receipt_tk = tk.Toplevel(app)
        receipt_tk.geometry("500x480+500+120")
        # 세부사항 출력
        tk.Label(receipt_tk, text="영수증", font=self.title_font).pack()
        tk.Label(receipt_tk, text="주문 항목", font=self.font2).pack()
        tk.Label(receipt_tk, text="메뉴     수량     가격", font=self.font2).pack()
        tk.Label(receipt_tk, text="=========================", font=self.font2).pack()
        # DB에서 정보 받아와서 띄움
        self.cur.execute("SELECT menuName, quantity, finalCost FROM orderTable")
        while True:
            row = self.cur.fetchone()
            if row is None:
                break
            tk.Label(receipt_tk, text="%s     %d     %d" % (row[0], row[1], row[2]), font=self.font2).pack()
        tk.Label(receipt_tk, text="=========================", font=self.font2).pack()
        tk.Label(receipt_tk, text="총액     %d 원" % MenuInfo.order_ttl, font=self.font2).pack()
        tk.Label(receipt_tk, text="할인 금액        %d 원" % (MenuInfo.order_ttl - PersonalCard.final_cost),
                 font=self.font2).pack()
        tk.Label(receipt_tk, text="결제 금액        %d 원" % PersonalCard.final_cost, font=self.font2).pack()
        tk.Label(receipt_tk, text="카드 잔액        %d 원" % PersonalCard.card_balance, font=self.font2).pack()
        tk.Label(receipt_tk, text="적립금      %d point" % PersonalCard.rewards_point, font=self.font2).pack()

    # 프로그램 작동하면서 변경되었던 사항들 초기화 #
    def clear_DB(self):
        self.cur.execute("DELETE FROM orderTable")
        self.order_DB.commit()
        self.order_DB.close()
        self.cur2.execute("DELETE FROM couponTable")
        self.coupon_DB.commit()
        self.coupon_DB.close()
        PersonalCard.final_cost = 0
        MenuInfo.order_ttl = 0


app = DemoPro()
app.mainloop()