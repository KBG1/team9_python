import mandb
import tkinter as tk
import tkinter.ttk as ttk

class Mobile:
    def __init__(self):
        self.mobile_tk = tk.Toplevel()
        self.mobile_tk.geometry("400x600+80+20")

        self.coupon_table = None

        self.rewards_button = ttk.Button(self.mobile_tk, text="적립금", command=self.rewards_screen)
        self.coupon_button = ttk.Button(self.mobile_tk, text="쿠폰", command=self.coupon_screen)
        self.rewards_button.pack()
        self.coupon_button.pack()

    def rewards_screen(self):
        def add_coupon():
            return

        _button1 = ttk.Button(self.mobile_tk, text="")

    def coupon_screen(self):
        self.mobile_tk_label1 = ttk.Label(self.mobile_tk, text="사용 가능한 쿠폰")
        self.coupon_table = ttk.Treeview(self.mobile_tk, columns=["쿠폰코드", "적용메뉴", "할인율", "할인금액"],
                                         displaycolumns=["쿠폰코드", "적용메뉴", "할인율", "할인금액"])

        self.mobile_tk_label1.pack()
        self.coupon_table.place(x=0, y=50, width=400, height=400)

        self.set_table()
        # .mobile_tk.protocol("WM_DELETE_WINDOW", .show_coupon)

    def set_table(self):
        """쿠폰 정보표의 구성."""
        self.coupon_table.column("#0", width=100, anchor="center")
        self.coupon_table.heading("#0", text="쿠폰코드", anchor="center")
        self.coupon_table.column("#1", width=150, anchor="center")
        self.coupon_table.heading("#1", text="적용메뉴", anchor="center")
        self.coupon_table.column("#2", width=50, anchor="center")
        self.coupon_table.heading("#2", text="할인율", anchor="center")
        self.coupon_table.column("#3", width=100, anchor="center")
        self.coupon_table.heading("#3", text="할인금액", anchor="center")
        self.insert_data()

    def insert_data(self):
        """데이터베이스에 생성된 쿠폰 데이터를 쿠폰 정보표에 삽입."""
        mandb.mc_cur.execute("SELECT * FROM coupon")
        couponlist = mandb.mc_cur.fetchall()
        for coupon in couponlist:
            self.coupon_table.insert('', 'end', text=coupon[0], iid=coupon[0],
                                     values=(coupon[2], str(int(coupon[4] * 100)) + "%", coupon[5]))
