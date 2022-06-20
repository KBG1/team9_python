import tkinter as tk
import tkinter.ttk as ttk
import menu
import card
import mandb
import coupon

class Page(tk.Frame):
    """
    Attributes:
        base_frame1: 페이지상 상단 프레임
        base_frame2: 페이지상 하단 프레임
    """

    def __init__(self):
        super(Page, self).__init__()

        self.base_frame1 = ttk.Frame(self, width=450, height=710, relief="solid")
        self.base_frame2 = ttk.Frame(self, width=450, height=100, relief="solid")

        self.base_frame1.pack()
        self.base_frame2.pack()
        self.base_frame1.propagate(False)
        self.base_frame2.propagate(False)

        self.logo_image = ttk.Label(self.base_frame1, text="로고 이미지", relief="solid")
        self.balance_label = ttk.Label(self.base_frame1, text="잔액: %d원" % card.balance)
        self.coupon_button = ttk.Button(self.base_frame2, text="원래QR코드\n(미구현)")
        self.go_frontpage_button = ttk.Button(self.base_frame2, text="처음으로")
        self.help_button = ttk.Button(self.base_frame2, text="도움기능")  # font=('나눔스퀘어_ac', 9))
        self.total_label = tk.Label(self.base_frame2, relief="flat", bd=0, font=('나눔스퀘어_ac', 16),
                                    text="￦%d" % menu.total_to_pay())

        # 필요한 페이지에서만 선택적으로 구현; 위치 변경 가능
        # self.logo_image.place(x=0, y=0, width=100, height=100)
        # self.balance_label.place(x=0, y=120)
        # self.coupon_button.place(x=45, y=0, width=85, height=100)
        # self.total_label.place(x=140, y=10, width=120, height=40)
        self.go_frontpage_button.place(x=170, y=60, width=115, height=30)
        self.help_button.place(x=295, y=60, width=115, height=30)

    def cancel_everything(self):
        mandb.clear_database()  # TODO 데이터베이스 수정한거 반영
        menu.selected.clear()
        coupon.used = 0

    def update_total_label(self):
        self.total_label.configure(text="￦%d" % menu.total_to_pay())

    def clear_frame(self, frame, placetype):
        if placetype == "grid":
            widget = frame.grid_slaves()
            for i in widget:
                i.destroy()
        if placetype == "place":
            widget = frame.place_slaves()
            for i in widget:
                i.place_forget()