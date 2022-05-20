import tkinter as tk
import tkinter.font as tkfont
from PIL import Image, ImageTk
import sqlite3 as sql3
import time


# base window #
class DemoPro(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
        self.geometry("600x800+450+5")
        self.resizable(False, False)
        self.configure(bg="#ffffff")
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


# used font list #
class Font:
    def __init__(self):
        self.title_font = tkfont.Font(family="맑은 고딕", size=24, weight="bold")
        self.font2 = tkfont.Font(family="맑은 고딕", size=16)

# card information #
class PersonalCard: # 뭔가 편집해야 하는 건 아닐까...
    card_balance = 1000000  # default card balance
    rewards_point = 0
    final_cost = 0


# menu information #
class MenuInfo:
    # the name of menu
    menu_code = {10001: "빅맥", 10002: "맥너겟", 10003: "콜라"}
    # if the menu is selected or not(if button clicked)
    select_check = {10001: 0, 10002: 0, 10003: 0}
    # the quantity of menu
    menu_quantity = {10001: 0, 10002: 0, 10003: 0}
    # the price of menu
    menu_price = {10001: 8000, 10002: 3000, 10003: 1500}
    # the total cost of order
    order_ttl = 0


# used image list #
class ImageOpen:
    def __init__(self):
        self.mv_pay_btn_img = Image.open('pic/button/mv_pay_btn.png')
        self.mv_pay_btn_img = self.mv_pay_btn_img.resize((100, 100))
        self.mv_pay_btn_img = ImageTk.PhotoImage(self.mv_pay_btn_img)
        self.cc_btn_img = Image.open('pic/button/cc_btn.png')
        self.cc_btn_img = self.cc_btn_img.resize((200, 133))
        self.cc_btn_img = ImageTk.PhotoImage(self.cc_btn_img)
        self.go_startp_btn_img = Image.open('pic/button/gomain.png')
        self.go_startp_btn_img = self.go_startp_btn_img.resize((100, 30))
        self.go_startp_btn_img = ImageTk.PhotoImage(self.go_startp_btn_img)
        self.go_back_btn_img = Image.open('pic/button/goback.png')
        self.go_back_btn_img = self.go_back_btn_img.resize((150, 50))
        self.go_back_btn_img = ImageTk.PhotoImage(self.go_back_btn_img)
        self.choose_btn_img = Image.open('pic/button/choose.png')
        self.choose_btn_img = self.choose_btn_img.resize((150, 50))
        self.choose_btn_img = ImageTk.PhotoImage(self.choose_btn_img)
        self.reset_btn_img = Image.open('pic/button/reset_cart.png')
        self.reset_btn_img = self.reset_btn_img.resize((150, 30))
        self.reset_btn_img = ImageTk.PhotoImage(self.reset_btn_img)


# used database list #
class OpenDB:
    def __init__(self):
        # orderTable column: menuID/menuName/quantity/finalCost/updateTime
        self.order_DB = sql3.connect("orderDB")
        self.cur = self.order_DB.cursor()


class Sharing(tk.Frame, Font, ImageOpen, OpenDB):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        Font.__init__(self)
        ImageOpen.__init__(self)
        OpenDB.__init__(self)


# 첫 화면 페이지 #
class StartPage(Sharing):
    def __init__(self, master):
        Sharing.__init__(self, master)

        self.cur.execute("DELETE FROM orderTable")
        self.order_DB.commit()

        # used frame list #
        self.ad_frm = tk.Frame(self, width=600, height=600, relief="solid", bd=2)
        self.ad_frm.pack(fill="both", expand=True)
        self.ad_frm.propagate(False)
        self.placetoeat_frm = tk.Frame(self, width=600, height=200, relief="solid", bd=2)
        self.placetoeat_frm.pack(fill="both", expand=True)
        self.placetoeat_frm.propagate(False)

        # in place to eat frame #
        tk.Button(self.placetoeat_frm, text="매장에서 먹을래요", font=self.font2, relief="flat",
                  command=lambda: master.switch_frame(MainPage)).place(x=0, y=40, width=300, height=100)
        tk.Button(self.placetoeat_frm, text="포장해서 갈게요", font=self.font2, relief="flat",
                  command=lambda: master.switch_frame(MainPage)).place(x=300, y=40, width=300, height=100)


# 메뉴 선택 페이지 #
class MainPage(Sharing):
    def __init__(self, master):
        Sharing.__init__(self, master)

        # used variable list #
        self.ent_open_check = 0

        # used frame list #
        self.logo_frm = tk.Frame(self, width=600, height=100)
        self.logo_frm.grid(row=0, column=0, sticky="nswe")
        self.menu_btn_frm = tk.Frame(self, width=600, height=500, bg="#ffffff", relief="solid", bd=2)
        self.menu_btn_frm.grid(row=1, column=0, sticky="nswe")
        self.qu_frm = tk.Frame(self, width=600, height=50, relief="solid", bd=2)
        self.qu_frm.grid(row=2, column=0, sticky="nswe")
        self.cart_frm = tk.Frame(self, width=600, height=100, relief="solid", bd=2)
        self.cart_frm.grid(row=3, column=0, sticky="nswe")
        self.menu_frm = tk.Frame(self, width=600, height=50, relief="solid", bd=2)
        self.menu_frm.grid(row=4, column=0, sticky="nswe")

        # in logo frame #
        self.go_startp_btn = tk.Button(self.logo_frm, image=self.go_startp_btn_img, relief="flat", bd=0,
                                       command=lambda: master.switch_frame(StartPage))
        self.go_startp_btn.place(x=20, y=50, width=100, height=30)

        # in menu button frame #
        # if press menu button, a new window for detail will appear
        tk.Button(self.menu_btn_frm, text="빅맥\n8000원", bg="#ffffff", relief="ridge", bd=1,
                  command=lambda: self.open_entry(10001)).place(x=0, y=0, width=200, height=133)
        tk.Button(self.menu_btn_frm, text="맥너겟\n3000원", bg="#ffffff", relief="ridge", bd=1,
                  command=lambda: self.open_entry(10002)).place(x=200, y=0, width=200, height=133)
        tk.Button(self.menu_btn_frm, text="콜라\n1500원", bg="#ffffff", relief="ridge", bd=1,
                  command=lambda: self.open_entry(10003)).place(x=400, y=0, width=200, height=133)

        # in cart frame #
        self.cart_lbox = tk.Listbox(self.cart_frm, width=60, height=5)
        self.cart_lbox.place(x=0, y=0, width=350, height=100)
        tk.Label(self.cart_frm, text="총액", font=self.font2).place(x=350, y=0)
        self.ttlprice_lb = tk.Listbox(self.cart_frm, font=self.font2, relief="flat", bd=0)
        self.ttlprice_lb.place(x=350, y=30, width=100, height=30)
        self.ttlprice_lb.insert(0, "￦ %d" % MenuInfo.order_ttl)
        # if press "전체취소" button, the cart will become empty and the orderlist will be clear
        tk.Button(self.cart_frm, image=self.reset_btn_img, relief="flat", bd=0,
                  command=self.reset_cart).place(x=350, y=70, width=150, height=30)
        # if press "주문내역" button, the cart will become empty and go to payment select page
        tk.Button(self.cart_frm, image=self.mv_pay_btn_img, relief="flat", bd=0,
                  command=lambda: master.switch_frame(OrderCheckPage)).place(x=500, y=0, width=100, height=100)

        # in menu frame #
        tk.Label(self.menu_frm, text="카드 잔액: %d 원" % PersonalCard.card_balance).pack()

    def calcul_sum(self):
        MenuInfo.order_ttl = 0
        self.cur.execute("SELECT finalCost FROM orderTable")
        while True:
            cost = self.cur.fetchone()
            if cost is None: break
            MenuInfo.order_ttl = MenuInfo.order_ttl + cost[0]
        self.ttlprice_lb.delete(0, "end")
        self.ttlprice_lb.insert(0, "￦ %d" % MenuInfo.order_ttl)

    def open_entry(self, code):
        MenuInfo.select_check[code] = 1 # check what menu is selected
        entry_tk = tk.Toplevel(app)
        entry_tk.geometry("500x600+500+120")
        tk.Button(entry_tk, text="메뉴사진", relief="flat").place(x=25, y=30, width=100, height=100)
        tk.Label(entry_tk, text="%s" % MenuInfo.menu_code[code]).place(x=150, y=30)
        ent = tk.Entry(entry_tk)
        ent.place(x=150, y=100, width=30)
        ent.insert(0, "1")
        plus_btn = tk.Button(entry_tk, text="+", relief="ridge", command=lambda: incordec("plus"))
        plus_btn.place(x=190, y=100, width=20, height=20)
        minus_btn = tk.Button(entry_tk, text="-", relief="ridge", command=lambda: incordec("minus"))
        minus_btn.place(x=120, y=100, width=20, height=20)
        price_lb = tk.Listbox(entry_tk, relief="flat", bd=0)
        price_lb.place(x=400, y=100, width=100, height=15)
        price_lb.insert(0, "￦ %d" % (MenuInfo.menu_price[code] * int(ent.get())))
        # if press "선택완료" button, the window will be closed and the selected menu will be added to cart #
        tk.Button(entry_tk, image=self.choose_btn_img, relief="flat", bd=0,
                  command=lambda: [self.enter_orderDB(int(ent.get())), self.enter_cart(), self.calcul_sum(),
                                   tk_destroy()]).place(x=280, y=520, width=150, height=50)
        # if press "취소" button, the window will be just closed #
        tk.Button(entry_tk, image=self.go_back_btn_img, relief="flat", bd=0,
                  command=lambda: tk_destroy()).place(x=70, y=520, width=150, height=50)

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

        def tk_destroy():
            for code in MenuInfo.select_check.keys():
                if MenuInfo.select_check[code] == 1:
                    MenuInfo.select_check[code] = 0
            entry_tk.destroy()

    def enter_cart(self):
        self.cart_lbox.delete(0, "end")
        self.cur.execute("SELECT menuName, quantity FROM orderTable ORDER BY datetime(updateTime) ASC")
        while True:
            data = self.cur.fetchone()
            if data is None: break
            self.cart_lbox.insert(0, "메뉴: %s 수량: %d\n" % (data[0], data[1]))

    def enter_orderDB(self, quantity):
        self.cur.execute("SELECT menuID FROM orderTable")
        rows = self.cur.fetchall()
        for code in MenuInfo.select_check.keys():
            if MenuInfo.select_check[code] == 1:
                for row in rows:
                    if row[0] == code:
                        MenuInfo.menu_quantity[code] = MenuInfo.menu_quantity[code] + quantity
                        ttlprice = MenuInfo.menu_price[code] * MenuInfo.menu_quantity[code]
                        sql = "UPDATE orderTable SET quantity = ?, finalCost = ?,\
                               updateTime = datetime('now', 'localtime') WHERE menuID = ?"
                        self.cur.execute(sql, (MenuInfo.menu_quantity[code], ttlprice, code))
                        self.order_DB.commit()
                        MenuInfo.select_check[code] = 0
                        return
                mncode = code
                mnname = MenuInfo.menu_code[code]
                MenuInfo.menu_quantity[code] = quantity
                ttlprice = MenuInfo.menu_price[code] * quantity
                sql = "INSERT INTO orderTable(menuID, menuName, quantity, finalCost) VALUES(?, ?, ?, ?)"
                vals = (mncode, mnname, quantity, ttlprice)
                self.cur.execute(sql, vals)
                self.order_DB.commit()
                MenuInfo.select_check[code] = 0
                return

    def reset_cart(self):
        self.cur.execute("DELETE FROM orderTable")
        self.order_DB.commit()
        self.cart_lbox.delete(0, "end")
        MenuInfo.order_ttl = 0
        self.ttlprice_lb.delete(0, "end")
        self.ttlprice_lb.insert(0, "￦ %d" % MenuInfo.order_ttl)
        for code in MenuInfo.menu_quantity.keys():
            MenuInfo.menu_quantity[code] = 0
        MenuInfo.order_ttl = 0


# 주문내역 페이지 #
class OrderCheckPage(Sharing):
    def __init__(self, master):
        Sharing.__init__(self, master)

        # used frame list #
        self.orderlist_frm = tk.Frame(self, width=600, height=600, relief="solid", bd=2)
        self.orderlist_frm.pack(fill="both", expand=True)
        self.orderlist_frm.propagate(False)
        self.announce_frm = tk.Frame(self, width=600, height=100, relief="solid", bd=2)
        self.announce_frm.pack(fill="both", expand=True)
        self.announce_frm.propagate(False)
        self.mv_btn_frm = tk.Frame(self, width=600, height=100, relief="solid", bd=2)
        self.mv_btn_frm.pack(fill="both", expand=True)
        self.mv_btn_frm.propagate(False)

        # in orderlist frame #
        self.show_orderlist()

        # in announce frame #
        self.ordercost = tk.Label(self.announce_frm, text="합계          %d" % MenuInfo.order_ttl,
                                  width=600, height=100, font=self.font2)
        self.ordercost.pack()

        # in move button frame #
        # 다음 #
        tk.Button(self.mv_btn_frm, image=self.mv_pay_btn_img,
                  command=lambda: master.switch_frame(PaymentPage)).place(x=300, y=0, width=100, height=100)
        # 이전 #
        tk.Button(self.mv_btn_frm, text="이전",
                  command=lambda: [master.switch_frame(MainPage)]).place(x=200, y=0, width=100, height=100)
        # 전체취소 #
        tk.Button(self.mv_btn_frm, image=self.cc_btn_img,
                  command=lambda: master.switch_frame(MainPage)).place(x=100, y=0, width=100, height=100)

    def show_orderlist(self):
        tk.Label(self.orderlist_frm, text="주문", font=self.title_font).place(x=30, y=10)
        order_lbox = tk.Listbox(self.orderlist_frm, width=60, height=5, font=self.font2, relief="flat", bd=0)
        order_lbox.place(x=150, y=80, width=350, height=100)
        self.cur.execute("SELECT menuID, menuName, quantity FROM orderTable ORDER BY datetime(updateTime) ASC")
        rows = self.cur.fetchall()
        for menu in rows:
            cc_btn = tk.Button(self.orderlist_frm, text="취소", command=lambda: cc_menu(menu[0]),
                               relief="ridge", borderwidth=1)
            cc_btn.place(x=30, y=90, width=80, height=20)
            order_lbox.insert(0, "%s %d" % (menu[1], menu[2]))

        def cc_menu(code):
            sql = "DELETE FROM orderTable WHERE menuID = ?"
            self.cur.execute(sql, (code,))
            self.order_DB.commit()
            order_lbox.delete(0)


# 결제수단 선택 페이지 #
class PaymentPage(Sharing):
    def __init__(self, master):
        Sharing.__init__(self, master)

        # used frame list #
        self.announce_frm = tk.Frame(self, width=600, height=150, relief="solid", bd=1)
        self.announce_frm.pack(fill="both", expand=True)
        self.announce_frm.propagate(False)
        self.select_btn_frm = tk.Frame(self, width=600, height=650, relief="solid", bd=1)
        self.select_btn_frm.pack(fill="both", expand=True)
        self.select_btn_frm.propagate(False)

        # in announce frame #
        tk.Label(self.announce_frm, text="결제 방법을 선택해 주세요", font=self.title_font).place(x=120, y=50)

        # in select button frame #
        tk.Button(self.select_btn_frm, text="카드 결제\nCARD PAYMENT", font=self.font2,
                  command=lambda: master.switch_frame(DisCountPage)).place(x=75, y=20, width=150, height=150)
        tk.Button(self.select_btn_frm, text="모바일 상품권\nMOBILE GIFT CARD", font=self.font2,
                  command=lambda: master.switch_frame(DisCountPage)).place(x=225, y=20, width=150, height=150)

# 할인수단 선택 페이지 #
class DisCountPage(Sharing):
    def __init__(self, master):
        Sharing.__init__(self, master)

        # used frame list #
        self.chs_discnt_frm = tk.Frame(self, width=600, height=667, relief="solid", bd=1)
        self.chs_discnt_frm.pack(fill="both", expand=True)
        self.chs_discnt_frm.propagate(False)
        self.etc_frm = tk.Frame(self, width=600, height=133, relief="solid", bd=1)
        self.etc_frm.pack(fill="both", expand=True)
        self.etc_frm.propagate(False)

        # in choose discount method frame #
        self.opt1 = tk.Button(self.chs_discnt_frm, text="적립금", command=lambda: master.switch_frame(DisCountRewards))
        self.opt1.place(x=0, y=0, width=300, height=333)
        self.opt2 = tk.Button(self.chs_discnt_frm, text="쿠폰", command=lambda: master.switch_frame(DisCountCoupon))
        self.opt2.place(x=300, y=0, width=300, height=333)
        self.opt3 = tk.Button(self.chs_discnt_frm, text="멤버십 포인트",
                              command=lambda: master.switch_frame(DisCountRewards))
        self.opt3.place(x=0, y=333, width=300, height=333)
        self.opt4 = tk.Button(self.chs_discnt_frm, text="없음(그냥 결제)", width=27, height=4,
                              command=lambda: [self.pay_sequence(), master.switch_frame(ReceiptPage)])
        self.opt4.place(x=300, y=333, width=300, height=333)

        # in etc frame #
        tk.Button(self.etc_frm, text="첫 화면으로\n(결제 취소)",
                  command=lambda: [master.switch_frame(MainPage)]).place(x=200, y=666, width=200, height=133)

    def pay_sequence(self):
        self.cur.execute("SELECT finalCost FROM orderTable")
        cost_list = self.cur.fetchall()
        for cost_data in cost_list:
            PersonalCard.final_cost = PersonalCard.final_cost + cost_data[0]
        PersonalCard.card_balance = PersonalCard.card_balance - PersonalCard.final_cost
        PersonalCard.rewards_point = PersonalCard.final_cost * 0.01


class DisCountRewards(Sharing):
    def __init__(self, master):
        Sharing.__init__(self, master)

        # used frame list #
        self.announce_frm = tk.Frame(self, width=600, height=667, relief="solid", bd=1)
        self.announce_frm.pack(fill="both", expand=True)
        self.announce_frm.propagate(False)
        self.btn_frm = tk.Frame(self, width=600, height=133, relief="solid", bd=1)
        self.btn_frm.pack(fill="both", expand=True)
        self.btn_frm.propagate(False)

        # in announce frame #
        self.announce1 = tk.Label(self.announce_frm, text="적립금을 사용해 할인하시겠습니까?")
        self.announce1.place(x=0, y=0, width=600, height=30)
        self.announce2 = tk.Label(self.announce_frm, text="적립금 %d point" % PersonalCard.rewards_point)
        self.announce2.place(x=0, y=30, width=600, height=30)
        if PersonalCard.rewards_point < 5000:
            self.announce4 = tk.Label(self.announce_frm, text="적립금이 5000점 미만이므로 사용할 수 없습니다.")
            self.announce4.place(x=0, y=90, width=600, height=30)
        else:
            self.announce3 = tk.Label(self.announce_frm,
                                      text="할인 후 결제 금액 %d" % (MenuInfo.order_ttl - PersonalCard.rewards_point))
            self.announce3.place(x=0, y=60, width=600, height=30)

        # in button frame #
        if PersonalCard.rewards_point < 5000:
            self.button1 = tk.Button(self.btn_frm, text="사용하기", state=tk.DISABLED)
            self.button1.place(x=300, y=0, width=200, height=133)
        else:
            self.button1 = tk.Button(self.btn_frm, text="사용하기", command=lambda: self.pay_sequence(master))
            self.button1.place(x=300, y=0, width=200, height=133)
        self.button2 = tk.Button(self.btn_frm, text="취소", command=lambda: master.switch_frame(DisCountPage))
        self.button2.place(x=100, y=0, width=200, height=133)

    def pay_sequence(self, master):
        self.cur.execute("SELECT finalCost FROM orderTable")
        cost_list = self.cur.fetchall()
        for cost_data in cost_list:
            PersonalCard.final_cost = PersonalCard.final_cost + cost_data[0]
        PersonalCard.final_cost = PersonalCard.final_cost - PersonalCard.rewards_point
        PersonalCard.card_balance = PersonalCard.card_balance - PersonalCard.final_cost
        PersonalCard.rewards_point = 0
        PersonalCard.rewards_point = PersonalCard.final_cost * 0.01
        master.switch_frame(ReceiptPage)


class DisCountCoupon(Sharing): # DisCountPage 상속으로는 어떻게 못 하나?
    def __init__(self, master):
        Sharing.__init__(self, master)

        # used frame list #
        self.logo_frm = tk.Frame(self, width=600, height=100, bg="#ffc100", relief="solid", bd=2)
        self.logo_frm.pack(fill="both", expand=True)
        self.logo_frm.propagate(False)
        self.announce_frm = tk.Frame(self, width=600, height=100, relief="solid", bd=1)
        self.announce_frm.pack(fill="both", expand=True)
        self.announce_frm.propagate(False)
        self.btn_frm = tk.Frame(self, width=600, height=600, relief="solid", bd=1)
        self.btn_frm.pack(fill="both", expand=True)
        self.btn_frm.propagate(False)

        # in announce frame #
        self.announce1 = tk.Label(self.announce_frm, text="사용하실 쿠폰을 선택해 주세요.")
        self.announce1.place(x=0, y=0, width=600, height=30)

        # in button frame #
        self.button1 = tk.Button(self.btn_frm, text="10% 할인", command=lambda: self.pay_sequence(master))
        self.button1.place(x=100, y=100, width=200, height=200)
        self.button2 = tk.Button(self.btn_frm, text="30% 할인", command=lambda: self.pay_sequence(master))
        self.button2.place(x=300, y=100, width=200, height=200)
        self.button3 = tk.Button(self.btn_frm, text="50% 할인", command=lambda: self.pay_sequence(master))
        self.button3.place(x=100, y=300, width=200, height=200)
        self.button4 = tk.Button(self.btn_frm, text="제품 기프티콘", command=lambda: self.pay_sequence(master))
        self.button4.place(x=300, y=300, width=200, height=200)
        self.cc_button = tk.Button(self.btn_frm, text="뒤로", command=lambda: master.switch_frame(PaymentPage))
        self.cc_button.place(x=300, y=300, width=200, height=200)

    def pay_sequence(self, master):
        self.cur.execute("SELECT finalCost FROM orderTable")
        cost_list = self.cur.fetchall()
        for cost_data in cost_list:
            PersonalCard.final_cost = PersonalCard.final_cost + cost_data[0]
        if PersonalCard.rewards_point < 5000: # if rewards point is over 5000, you can use it for discount
            print("5000점 미만 작동확인\n")
            self.announce4.place(x=0, y=90, width=600, height=30)
            self.button1.place_forget()
        else:
            print("5000점 이상 작동확인\n")
            PersonalCard.final_cost = PersonalCard.final_cost - PersonalCard.rewards_point
            PersonalCard.card_balance = PersonalCard.card_balance - PersonalCard.final_cost
            PersonalCard.rewards_point = 0
            PersonalCard.rewards_point = PersonalCard.final_cost * 0.01
            master.switch_frame(ReceiptPage)


class DisCountMembership(DisCountPage):
    def __init__(self, master):
        DisCountPage.__init__(self, master)
        self.announce1 = tk.Label(self.announce_frm, text="사용할 멤버십 선택")


class ReceiptPage(Sharing):
    def __init__(self, master):
        Sharing.__init__(self, master)

        # used frame list #
        self.summary_frm = tk.Frame(self, width=600, height=300, relief="solid", bd=2)
        self.summary_frm.pack(fill="both", expand=True)
        self.summary_frm.propagate(False)
        self.etc_frm = tk.Frame(self, width=600, height=100, relief="solid", bd=2)
        self.etc_frm.pack(fill="both", expand=True)
        self.etc_frm.propagate(False)

        # in summary frame #
        tk.Label(self.summary_frm, text="결제가 완료되었습니다.\n", font=self.title_font).pack()
        tk.Label(self.summary_frm, text="주문한 상품을 잘 받아가시길 바랍니다.\n", font=self.font2).pack()

        # in etc frame #
        self.mv_main_btn = tk.Button(self.etc_frm, text="첫 화면으로",
                                     command=lambda: [self.clear_DB(), master.switch_frame(MainPage)])
        self.mv_main_btn.pack(side="left")
        self.show_rcpt_btn = tk.Button(self.etc_frm, text="영수증 보기",
                                       command=self.new_tk_receipt)
        self.show_rcpt_btn.pack(side="left")

    def new_tk_receipt(self):
        receipt_tk = tk.Toplevel(app)
        receipt_tk.geometry("500x600+500+120")
        tk.Label(receipt_tk, text="영수증", font=self.title_font).pack()
        tk.Label(receipt_tk, text="주문 항목", font=self.font2).pack()
        tk.Label(receipt_tk, text="메뉴     수량     가격", font=self.font2).pack()
        tk.Label(receipt_tk, text="=========================", font=self.font2).pack()
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

    def clear_DB(self):
        self.cur.execute("DELETE FROM orderTable")
        self.order_DB.commit()
        self.order_DB.close()
        PersonalCard.final_cost = 0
        MenuInfo.order_ttl = 0


# 창 닫을 때 데이터베이스 초기화 어떻게 해야 할지 모르겠어서 다시 열면 전체취소 눌러줘야함..
# 아니면 첫 화면으로 돌아갔다가 끄거나..
app = DemoPro()
app.mainloop()