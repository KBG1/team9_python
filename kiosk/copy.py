"""모듈에 대한 설명 기재
"""
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.font as tkfont
import tkinter.scrolledtext as tkscroll
import tkinter.messagebox as tkmsgbox
import tkinter.ttk as ttk
import sqlite3
import string
import random
import os
import mandb
import menu
import card
import coupon
from mobile import Mobile
from page import Page
# try:
#     import MCDB
# except ImportError:
#     print("이미 DB가 생성되었습니다.\n")


class DecoDetail:   # 원래 폰트 이미지 넣으려고 한 건데 폰트는 그냥 내가 일일이 쓰는 게 나을 듯...
    def __init__(self):
        # image
        self.menu_image1: tk.Image


class MainWindow(tk.Tk, Mobile):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.geometry("450x810+500+0")
        self.resizable(False, False)
        self._frame = None
        mandb.clear_database()
        self.switch_frame(FrontPage)
        coupon.create_coupon()

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class FrontPage(tk.Frame):
    def __init__(self, master):
        super(FrontPage, self).__init__()

        self._frame1 = ttk.Frame(self, width=450, height=560, relief="solid")
        self._frame2 = ttk.Frame(self, width=450, height=250, relief="solid")

        self._frame1.pack()
        self._frame2.pack()
        self._frame1.propagate(False)    # 프레임 내부 위젯이 프레임 크기에 영향을 주지 않음.
        self._frame2.propagate(False)

        # frame1
        self._frame1_label1 = ttk.Label(self._frame1, text="광고 영상")
        self._frame1_label1.pack()

        # frame2
        self._frame2_button1 = ttk.Button(self._frame2, # relief="solid", bd=1, font=('나눔스퀘어_ac', 16),
                                          text="쿠폰 사용",
                                          command=lambda: master.switch_frame(CouponPage))
        self._frame2_button2 = ttk.Button(self._frame2, # relief="solid", bd=1, font=('나눔스퀘어_ac', 16),
                                          text="주문하기",
                                          command=lambda: master.switch_frame(WheretoEatPage))
        self._frame2_button3 = ttk.Button(self._frame2, # relief="solid", bd=1, font=('나눔스퀘어_ac', 9),
                                          text="언어")
        self._frame2_button4 = ttk.Button(self._frame2, # relief="solid", bd=1, font=('나눔스퀘어_ac', 9),
                                          text="도움기능")
        # TODO 언어, 도움기능 버튼 수정.

        self._frame2_button1.place(x=40, y=70, width=180, height=180)
        self._frame2_button2.place(x=240, y=70, width=180, height=70)
        self._frame2_button3.place(x=240, y=150, width=85, height=35)
        self._frame2_button4.place(x=335, y=150, width=85, height=35)


class WheretoEatPage(Page):
    def __init__(self, master):
        super(WheretoEatPage, self).__init__()

        # frame1
        self._frame1_label1 = ttk.Label(self.base_frame1, anchor="center",
                                        text="식사 방법을\n선택해 주세요",
                                        font=('나눔스퀘어_ac Bold', 24, "bold"))
        self._frame1_button1 = ttk.Button(self.base_frame1, # font=('나눔스퀘어_ac', 16),
                                          text="매장에서 식사",
                                          command=lambda: master.switch_frame(MainPage))
        self._frame1_button2 = ttk.Button(self.base_frame1, # font=('나눔스퀘어_ac', 16),
                                          text="테이크 아웃",
                                          command=lambda: master.switch_frame(MainPage))

        self._frame1_label1.place(x=0, y=150, width=450)
        self._frame1_button1.place(x=70, y=250, width=150, height=200)
        self._frame1_button2.place(x=230, y=250, width=150, height=200)


class MainPage(Page):
    def __init__(self, master):
        super(MainPage, self).__init__()

        self._category = ttk.Frame(self.base_frame1, relief="solid")
        self._menulist = ttk.Frame(self.base_frame1, relief="solid")
        # self.menu_button_style = ttk.Style()
        # self.menu_button_style.map("menu.Button", width=90, height=130)

        self.coupon_button.configure(command=lambda: master.switch_frame(CouponPage))
        self.go_frontpage_button.configure(command=lambda: [self.cancel_everything(),
                                                            master.switch_frame(FrontPage)])
        self.balance_label.place(x=0, y=120, width=100, height=40)
        self._category.place(x=0, y=160, width=100, height=350)
        self._menulist.place(x=130, y=160, width=320, height=550)

        # frame1-base
        self.logo_image.place(x=0, y=0, width=100, height=100)
        self.coupon_button.place(x=45, y=0, width=85, height=100)

        # frame1-category
        self._category_buttons = []
        for i in range(7):
            place_y = i * 50
            button = ttk.Button(self._category, text="%s" % menu.menu_type_dict[i+1])
            button.place(x=0, y=place_y, width=100, height=50)
            self._category_buttons.append(button)

        for i in range(7):
            self._category_buttons[i].configure(command=lambda i=i: self._show_category(master, menu.menu_row_dict[i+1], 3, i+1))

        # frame1-menulist
        self._frame_canvas = ttk.Frame(self._menulist)
        self._frame_canvas.grid(row=0, column=0)
        self._frame_canvas.grid_rowconfigure(0, weight=1)
        self._frame_canvas.grid_columnconfigure(0, weight=1)
        self._frame_canvas.grid_propagate(False)
        self._canvas = tk.Canvas(self._frame_canvas)
        self._canvas.grid(row=0, column=0, sticky="news")
        self._menulist_buttons_frame = tk.Frame(self._canvas, bg="white")
        self._canvas.create_window(0, 0, window=self._menulist_buttons_frame, anchor="nw")

        # 카테고리 누르기 전에 뭔가 보였으면 하는데 안보이네... # TODO 보이도록 수정
        # self._main_image = tk.Label(self._menulist_buttons_frame, text="광고?추천?")
        # self._main_image.place(x=0, y=0)

        # frame2
        self._orderlist_button = ttk.Button(self.base_frame2, text="주문내역",
                                            command=lambda: master.switch_frame(OrderCheckPage))

        self.total_label.place(x=140, y=10, width=120, height=40)
        self._orderlist_button.place(x=270, y=10, width=140, height=40)

    def _show_category(self, master, row, col, type_num):
        self.clear_frame(self._menulist_buttons_frame, "grid")
        menu.select_table("1", type_num)
        menu_info = mandb.mc_cur.fetchall()
        self._scrolly = ttk.Scrollbar(self._frame_canvas, orient="vertical", command=self._canvas.yview)
        self._scrolly.grid(row=0, column=1, sticky="ns")
        self._canvas.configure(yscrollcommand=self._scrolly.set)
        self._menulist_buttons = [[ttk.Button() for j in range(col)] for i in range(row)]
        for i in range(0, row):
            for j in range(0, col):
                menu_num = row*col - (i*col+j) - 1
                if menu_info[menu_num][6] == 1:
                    self._menulist_buttons[i][j] = tk.Button(self._menulist_buttons_frame, width=12, height=7, wraplength=90,
                                                             text="%s\n\n\n￦%d %dKcal" % (menu_info[menu_num][1], menu_info[menu_num][4], menu_info[menu_num][5]),
                                                             command=lambda menu_num=menu_num: [menu.select_menu(menu_info[menu_num][0]),
                                                                                                master.switch_frame(MenuDetailPage)])
                    self._menulist_buttons[i][j].grid(row=i, column=j, sticky='news')

        self._menulist_buttons_frame.update_idletasks()
        self._frame_canvas.config(width=320, height=550)
        self._canvas.config(scrollregion=self._canvas.bbox("all"))
        # TODO 이미지도 카테고리별 리스트로 만들어서 개수 딱 맞춰 넣어야할 느낌..


class MenuDetailPage(Page):
    def __init__(self, master):
        super(MenuDetailPage, self).__init__()

        self._frame1_button1 = ttk.Button(self.base_frame1, text="주문 확인하기", state="DISABLED")
        self.go_frontpage_button.configure(command=lambda: [self.cancel_everything(),
                                                            master.switch_frame(FrontPage)])

        self.order_sequence(master)

    def order_sequence(self, master):
        """
        Display the Select Details window, which varies by category.
        Args:
            master: for the last step of each sequence, back to <MainPage>

        Returns: None

        """
        category = menu.getinfo("category", menu.selected[0][0])
        print(category)
        if category == 1:
            self._show_step(master, category)

        else:
            self._order_popup(master, category)

    def _order_popup(self, master, category):
        """
        If you choose a single item, you can change the quantity by this popup window.
        Args:
            master: to switch frame to <MainPage>
            category: to distinguish which category doesn't have any <set>

        Returns: None

        """
        win = tk.Toplevel(master)
        # TODO x버튼 비활성화하거나 없애버리기(가능하면)
        win.geometry("300x500+575+150")
        win_label1 = tk.Label(win, text="%s" % menu.menu_type_dict[category], relief="solid", bd=1)
        win_label2 = tk.Label(win, text="이미지", relief="solid", bd=1)
        win_label3 = tk.Label(win, text="%s\n￦%d %dKcal" % (menu.getinfo("name", menu.selected[0][0]),
                                                            menu.getinfo("price", menu.selected[0][0]),
                                                            menu.getinfo("cal", menu.selected[0][0])))
        win_entry1 = ttk.Entry(win)
        win_entry1.insert(0, "1")   # default값 설정
        win_plusbutton = ttk.Button(win, text="+", command=lambda: operate("+"))
        win_minusbutton = ttk.Button(win, text="-", command=lambda: operate("-"))
        win_button3 = ttk.Button(win, text="장바구니 추가",
                                 command=lambda: [menu.add_cart(int(win_entry1.get())),
                                                  win.destroy(), self.update_total_label(), menu.selected.clear(),
                                                  master.switch_frame(MainPage)])

        win_label1.place(x=0, y=10, width=75, height=30)
        win_label2.place(x=75, y=60, width=150, height=150)
        win_label3.place(x=0, y=220, width=300)
        win_entry1.place(x=50, y=375, width=200, height=30)
        win_plusbutton.place(x=250, y=375, width=30, height=30)
        win_minusbutton.place(x=20, y=375, width=30, height=30)
        win_button3.place(x=0, y=425, width=300, height=75)

        def operate(oper):
            """
            The [+] button increases the number of <entry> by 1.
            The [-] button decreases the number of <entry> by 1.
            Args:
                oper: to distinguish which operator button you pressed

            Returns: None

            """
            ent = int(win_entry1.get())
            if oper == "+":
                ent += 1
                win_entry1.delete(0, "end")
                win_entry1.insert(0, str(ent))
                win_label3.configure(text="%s\n￦%d %dKcal" % (menu.getinfo("name", menu.selected[0][0]),
                                                              menu.getinfo("price", menu.selected[0][0]) * ent,
                                                              menu.getinfo("cal", menu.selected[0][0]) * ent))
            elif oper == "-":
                if ent <= 1: return
                ent -= 1
                win_entry1.delete(0, "end")
                win_entry1.insert(0, str(ent))
                win_label3.configure(text="%s\n￦%d %dKcal" % (menu.getinfo("name", menu.selected[0][0]),
                                                              menu.getinfo("price", menu.selected[0][0]) * ent,
                                                              menu.getinfo("cal", menu.selected[0][0]) * ent))
            else: return

    def _show_step(self, master, category):
        """
        Display the screen for selecting a single item or <set>.
        Args:
            master: for the last step of the sequence
            category: to distinguish whether a set menu is in the category or not

        Returns: None

        """
        menudetailpage_label1 = tk.Label(self.base_frame1,
                                         text="%s" % menu.getinfo("name", menu.selected[0][0]))
        menudetailpage_label2 = tk.Label(self.base_frame1, relief="solid", bd=1, font=('나눔스퀘어_ac Bold', 16),
                                         text="세트로 주문하시겠습니까?")
        menudetailpage_button1 = tk.Button(self.base_frame1, relief="solid", bd=1, font=('나눔스퀘어_ac', 16),
                                           text="(세트 이미지)\n세트 선택",
                                           command=lambda: [self.clear_frame(self.base_frame1, "place"),
                                                            menu.setmenu(), menu.add_cart(1),
                                                            self._show_step2(master)])
        menudetailpage_button2 = tk.Button(self.base_frame1, relief="solid", bd=1, font=('나눔스퀘어_ac', 16),
                                           text="(세트 이미지)\n단품 선택\n￦%d %dKcal" %
                                                (menu.getinfo("price", menu.selected[0][0]),
                                                 menu.getinfo("cal", menu.selected[0][0])),
                                           command=lambda: self._order_popup(master, category))
        menudetailpage_button3 = ttk.Button(self.base_frame1,
                                            text="취소",
                                            command=lambda: [self.cancel_everything(), master.switch_frame(MainPage)])

        self.logo_image.place(x=0, y=0, width=100, height=100)
        menudetailpage_label1.place(x=100, y=0, width=350, height=100)
        menudetailpage_label2.place(x=0, y=100, width=450, height=100)
        menudetailpage_button1.place(x=40, y=200, width=180, height=250)
        menudetailpage_button2.place(x=230, y=200, width=180, height=250)
        menudetailpage_button3.place(x=40, y=470, width=370, height=30)

    def _show_step2(self, master):
        """
        Display the screen for selecting <set> or <large set>.
        Args:
            master: for the last step of the sequence

        Returns: None

        """
        menudetailpage_label1 = ttk.Label(self.base_frame1, text="%s" % menu.selected[0][0])

        step2_button2 = tk.Button(self.base_frame1, wraplength=90,
                                  text="%s\n￦%d %dKcal" % (menu.getinfo("name", menu.selected[0][0]),
                                                           menu.getinfo("price", menu.selected[0][0]),
                                                           menu.getinfo("cal", menu.selected[0][0])),
                                  command=lambda: [self.clear_frame(self.base_frame1, "place"),
                                                   self._show_step3(master, "general")])
        step2_button3 = tk.Button(self.base_frame1, wraplength=90,
                                  text="%s-라지\n￦%d %dKcal" % (menu.getinfo("name", menu.selected[0][0]),
                                                              menu.getinfo("price", menu.selected[0][0]) + 600,
                                                              menu.getinfo("cal", menu.selected[0][0]) + 131),
                                  command=lambda: [self.clear_frame(self.base_frame1, "place"),
                                                   self._show_step3(master, "large")])

        self.logo_image.place(x=0, y=0, width=100, height=100)
        self._frame1_button1.place(x=0, y=200, width=100, height=60)
        menudetailpage_label1.place(x=100, y=0, width=350, height=100)
        step2_button2.place(x=130, y=160, width=90, height=130)
        step2_button3.place(x=225, y=160, width=90, height=130)

    def _show_step3(self, master, settype):
        """
        Display the side menu selection screen for the <set>.
        Args:
            master: for the last step of the sequence
            settype: to distinguish set or large set

        Returns: None

        """
        menudetailpage_label1 = ttk.Label(self.base_frame1,
                                          text = "%s\n￦%d %dKcal" % (menu.getinfo("name", menu.selected[0][0]),
                                                                     menu.getinfo("price", menu.selected[0][0]),
                                                                     menu.getinfo("cal", menu.selected[0][0])))
        step3_button1 = tk.Button(self.base_frame1, wraplength=90,
                                  text="%s\n%dKcal" % (menu.getinfo("name", menu.selected[1][0]),
                                                       menu.getinfo("cal", menu.selected[1][0])),
                                  command=lambda: [self.clear_frame(self.base_frame1, "place"),
                                                   self._show_step4(master, "general")])
        step3_button2 = tk.Button(self.base_frame1, wraplength=90,
                                  text="%s\n+￦%d %dKcal" % (menu.getinfo("name", menu.burger_set_side[0]),
                                                            menu.getextra(1, menu.burger_set_side[0]),
                                                            menu.getinfo("cal", menu.burger_set_side[0])),
                                  command=lambda: [self.clear_frame(self.base_frame1, "place"),
                                                   menu.changemenu(1, menu.burger_set_side[0]),
                                                   self._show_step4(master, "general")])
        step3_button3 = tk.Button(self.base_frame1, wraplength=90,
                                  text="%s\n+￦%d %dKcal" % (menu.getinfo("name", menu.burger_set_side[1]),
                                                            menu.getextra(1, menu.burger_set_side[0]),
                                                            menu.getinfo("cal", menu.burger_set_side[1])),
                                  command=lambda: [self.clear_frame(self.base_frame1, "place"),
                                                   menu.changemenu(1, menu.burger_set_side[1]),
                                                   self._show_step4(master, "general")])
        if settype == "large":
            menudetailpage_label1.configure(text = "%s-라지세트\n￦%d %dKcal" % (menu.getinfo("name", menu.selected[0][0]),
                                            menu.getinfo("price", menu.selected[0][0]) + 600,
                                            menu.getinfo("cal", menu.selected[0][0]) + 131))
            step3_button1.configure()
            step3_button2.configure()
            step3_button3.configure()

        step3_label1 = ttk.Label(self.base_frame1, text="세트메뉴 사이드를 선택하세요")

        self.logo_image.place(x=0, y=0, width=100, height=100)
        self._frame1_button1.place(x=0, y=320, width=100, height=60)
        menudetailpage_label1.place(x=100, y=0, width=350, height=100)
        step3_label1.place(x=130, y=70)
        step3_button1.place(x=130, y=160, width=90, height=130)
        step3_button2.place(x=225, y=160, width=90, height=130)
        step3_button3.place(x=320, y=160, width=90, height=130)

    def _show_step4(self, master, settype):
        """
        Display the drink menu selection for the <set>.
        Args:
            master: for the last step of the sequence
            settype: to distinguish set or large set

        Returns: None

        """
        def _show_category(row, col):
            _scrolly = ttk.Scrollbar(_frame_canvas, orient="vertical", command=_canvas.yview)
            _scrolly.grid(row=0, column=1, sticky="ns")
            _canvas.configure(yscrollcommand=_scrolly.set)
            _drinklist_buttons = [[ttk.Button() for j in range(col)] for i in range(row)]
            for i in range(0, row):
                for j in range(0, col):
                    menu_num = i*col+j
                    _drinklist_buttons[i][j] = tk.Button(_drinklist_buttons_frame, width=12, height=7,
                                                         wraplength=90,
                                                         text="%s\n+￦%d %dKcal" % (
                                                             menu.getinfo("name", menu.burger_set_drink[menu_num]),
                                                             menu.getextra(2, menu.burger_set_drink[menu_num]),
                                                             menu.getinfo("cal", menu.burger_set_drink[menu_num])),
                                                         command=lambda menu_num=menu_num:
                                                         [menu.changemenu(2, menu.burger_set_drink[menu_num]),
                                                          menu.selected.clear(), master.switch_frame(OrderCheckPage)])
                    _drinklist_buttons[i][j].grid(row=i, column=j, sticky='news')

            _drinklist_buttons_frame.update_idletasks()
            _frame_canvas.config(width=320, height=550)
            _canvas.config(scrollregion=_canvas.bbox("all"))
            # TODO 이미지도 카테고리별 리스트로 만들어서 개수 딱 맞춰 넣어야할 느낌..

        menudetailpage_label1 = ttk.Label(self.base_frame1,
                                          text = "%s\n￦%d %dKcal" % (menu.getinfo("name", menu.selected[0][0]),
                                                                     menu.getinfo("price", menu.selected[0][0]),
                                                                     menu.getinfo("cal", menu.selected[0][0])))
        step3_button2 = tk.Button(self.base_frame1, wraplength=90,
                                  text="%s\n%dKcal" % (menu.getinfo("name", menu.selected[2][0]), menu.getinfo("cal", menu.selected[2][0])),
                                  command=lambda: [self.clear_frame(self.base_frame1, "place"),
                                                   self._show_step4(master, "general")])

        _drinklist = ttk.Frame(self.base_frame1, relief="solid")
        _drinklist.place(x=130, y=160, width=320, height=550)

        # frame1-drinklist
        _frame_canvas = ttk.Frame(_drinklist)
        _frame_canvas.grid(row=0, column=0)
        _frame_canvas.grid_rowconfigure(0, weight=1)
        _frame_canvas.grid_columnconfigure(0, weight=1)
        _frame_canvas.grid_propagate(False)
        _canvas = tk.Canvas(_frame_canvas)
        _canvas.grid(row=0, column=0, sticky="news")
        _drinklist_buttons_frame = tk.Frame(_canvas, bg="white")
        _canvas.create_window(0, 0, window=_drinklist_buttons_frame, anchor="nw")

        _show_category(5, 3)

        self._frame1_button1.place(x=0, y=320, width=100, height=60)

    def _show_step5(self, master):
        return

    def cancel_everything(self):
        menu.selected.clear()


class OrderCheckPage(Page):
    def __init__(self, master):
        super(OrderCheckPage, self).__init__()

        self._button1 = ttk.Button(self.base_frame2, text="추가주문",
                                   command=lambda: master.switch_frame(MainPage))
        self._button2 = ttk.Button(self.base_frame2, text="주문완료",
                                   command=lambda: master.switch_frame(PaymentPage))

        self.go_frontpage_button.configure(command=lambda: [self.cancel_everything(),
                                                            master.switch_frame(FrontPage)])
        self.coupon_button.place(x=45, y=60, width=85, height=40)
        self._button1.place(x=45, y=0, width=115, height=50)
        self._button2.place(x=170, y=0, width=240, height=50)

        sql = "SELECT * FROM orders"
        mandb.mc_cur.execute(sql)
        orders = mandb.mc_cur.fetchall()
        self._innerwindow_list = []
        i = 0
        for order in orders:
            if order[4] is None:
                i += 1
                temp = ttk.PanedWindow(self.base_frame1)
                self._label1 = tk.Label(temp, wraplength=150,
                                        text="%s\n%dkcal" % (order[1], menu.getinfo("cal", order[0])))
                self._button1 = ttk.Button(temp, text="취소",
                                           command=lambda i=i, order=order: self.cancel_order(i-1, order))
                self._entry1 = ttk.Entry(temp)
                self._entry1.insert(0, "%d" % order[2])  # default값 설정
                self._plusbutton = ttk.Button(temp, text="+", command=lambda: operate("+"))
                self._minusbutton = ttk.Button(temp, text="-", command=lambda: operate("-"))
                self._label2 = ttk.Label(temp, text="W%d" % order[3])

                self._innerwindow_list.append(temp)
                temp.place(x=0, y=i*100, width=450, height=100)
                self._label1.place(x=100, y=0, width=150, height=100)
                self._button1.place(x=0, y=30, width=100, height=40)
                self._entry1.place(x=300, y=35, width=40, height=30)
                self._plusbutton.place(x=340, y=35, width=30, height=30)
                self._minusbutton.place(x=270, y=35, width=30, height=30)
                self._label2.place(x=380, y=30, height=40)

        def operate(oper):
            ent = int(self._entry1.get())
            if oper == "+":
                ent += 1
            elif oper == "-":
                if ent <= 1: return
                ent -= 1
            else: return
            self._entry1.delete(0, "end")
            self._entry1.insert(0, str(ent))
            sql = "UPDATE orders SET quantity = ?, finalCost = ? WHERE menuID = ?"
            val = (ent, order[3]+(ent-order[2])*menu.getinfo("price", order[0]), order[0])
            mandb.mc_cur.execute(sql, val)
            mandb.mc_db.commit()
            self._label1.configure(text="%s\n%dkcal" % (order[1], ent*menu.getinfo("cal", order[0])))
            self._label2.configure(text="W%d" % (order[3]+(ent-order[2])*menu.getinfo("price", order[0])))

    def cancel_order(self, num, order):
        sql = "DELETE FROM orders WHERE menuID = ?"
        mandb.mc_cur.execute(sql, (order[0],))
        mandb.mc_db.commit()
        self._innerwindow_list[num].place_forget()
        for i in range(num+1, len(self._innerwindow_list)):
            self._innerwindow_list[i].place_forget()
            self._innerwindow_list[i].place(x=0, y=i*100, width=450, height=100)



class PaymentPage(Page):
    def __init__(self, master):
        super(PaymentPage, self).__init__()

        self._frame1_label1 = ttk.Label(self.base_frame1, text="결제 방법을 선택해 주세요")
        self._frame1_button1 = ttk.Button(self.base_frame1, text="카드 결제\nCARD PAYMENT",
                                          command=lambda: self.pay_sequence(master))
        self._frame1_button2 = ttk.Button(self.base_frame1, text="모바일 상품권\nMOBILE GIFT CARD",
                                          command=lambda: master.switch_frame(CouponPage), state=tk.DISABLED)

        self.go_frontpage_button.place_forget()
        self._frame1_label1.place(x=60, y=50)
        self._frame1_button1.place(x=75, y=100, width=150, height=150)
        self._frame1_button2.place(x=225, y=100, width=150, height=150)

    def pay_sequence(self, master):
        total_to_pay = menu.total_to_pay()
        if total_to_pay <= card.balance:
            card.balance -= total_to_pay
            card.rewards = total_to_pay // 100 * 5
            master.switch_frame(ResultPage)
        else:
            tkmsgbox.showinfo(title="안내", message="카드 잔액이 부족합니다.")
            master.switch_frame(FrontPage)


class CouponPage(Page):
    def __init__(self, master):
        super(CouponPage, self).__init__()

        self._frame1_label1 = ttk.Label(self.base_frame1, text="쿠폰 번호를 입력해 주세요")
        # TODO 쿠폰 이미지 추가하기.
        self._frame1_entry1 = tk.Entry(self.base_frame1)
        self._frame1_button1 = tk.Button(self.base_frame1, text="확인",
                                         command=lambda: self.check_coupon(master, str(self._frame1_entry1.get())))

        self.go_frontpage_button.configure(text="메뉴화면으로", command=lambda: master.switch_frame(MainPage))
        self._frame1_label1.place(y=100)
        self._frame1_entry1.place(x=115, y=500, width=250, height=50)
        self._frame1_button1.place(x=215, y=550, width=50, height=30)

    def check_coupon(self, master, ent):
        """
        If coupon ID is same as entry, add coupon menu to cart
        Args:
            master: to go <MainPage>
            ent: entry.get()

        Returns: None

        """
        mandb.mc_cur.execute("SELECT * FROM coupon")
        coupon_info = mandb.mc_cur.fetchall()
        for coup in coupon_info:
            if coup[0] == ent and coupon.used == 0:
                coupon.used = 1
                sql = "INSERT INTO orders(menuID, menuName, quantity, finalCost, coupon) VALUES(?, ?, ?, ?, ?)"
                val = (coup[1], coup[2] + " - 쿠폰", 1, coup[3]-coup[5], 1)
                mandb.mc_cur.execute(sql, val)
                mandb.mc_db.commit()
                Mobile.coupon_table.delete(ent)
                master.switch_frame(MainPage)
                return
        # 일치하는 쿠폰이 없을 경우 메세지 출력
        if coupon.used == 1:
            tkmsgbox.showinfo(title="안내", message="쿠폰은 주문당 한번만 사용가능합니다.")
            self._frame1_entry1.delete(0, "end")
        else:
            tkmsgbox.showinfo(title="안내", message="쿠폰이 존재하지 않습니다.")
            self._frame1_entry1.delete(0, "end")


class ResultPage(Page):
    def __init__(self, master):
        super(ResultPage, self).__init__()
        # TODO 처음으로 버튼 크기/위치 변경해서 place

        self._receipt = 0
        self._frame1_label1 = ttk.Label(self.base_frame1, text="주문이 완료되었습니다.")
        self._frame1_button1 = ttk.Button(self.base_frame1, text="영수증 보기",
                                          command=self._show_receipt())

        self.go_frontpage_button.configure(command=lambda: [self.cancel_everything(),
                                                            master.switch_frame(FrontPage)])
        self._frame1_label1.place(x=200, y=0, width=450, height=50)
        self._frame1_button1.place(x=200, y=50, width=100, height=50)

        print(card.balance)

    def _show_receipt(self):
        def danga():
            if order[4] is None:
                return menu.getinfo("price", order[0])
            else:
                return order[3] / order[2]

        def geumek():
            if order[6] == 0:
                return danga() * order[2]
            else:
                return order[3] * order[2]

        def set_table():
            """쿠폰 정보표의 구성."""
            receipt_table.column("#0", width=150, anchor="center")
            receipt_table.heading("#0", text="제품명", anchor="center")
            receipt_table.column("#1", width=150, anchor="center")
            receipt_table.heading("#1", text="단가", anchor="center")
            receipt_table.column("#2", width=50, anchor="center")
            receipt_table.heading("#2", text="수량", anchor="center")
            receipt_table.column("#3", width=100, anchor="center")
            receipt_table.heading("#3", text="금액", anchor="center")

        def insert_data():
            receipt_table.insert('', 'end', text=order[1], values=(int(danga()), order[2], int(geumek())))

        if self._receipt == 0:
            receipt_tk = tk.Toplevel(Demo)
            receipt_tk.geometry("500x480+500+120")
            # 세부사항 출력
            # DB에서 정보 받아와서 띄움
            mandb.mc_cur.execute("SELECT * FROM orders")
            orders = mandb.mc_cur.fetchall()
            receipt_table = ttk.Treeview(receipt_tk, columns=["제품명", "단가", "수량", "금액"],
                                         displaycolumns=["제품명", "단가", "수량", "금액"])
            set_table()

            tk.Label(receipt_tk, text="영수증").grid(row=0, column=0)
            tk.Label(receipt_tk, text="거래일:%s" % orders[0][5]).grid(row=1, column=0)
            for order in orders:
                insert_data()
                receipt_table.grid(row=2, column=0)
            tk.Label(receipt_tk, text="총액     %d 원" % card.total_without_dc()).grid(row=3, column=0)
            tk.Label(receipt_tk, text="할인 금액        %d 원" % (card.total_without_dc() - menu.total_to_pay())).grid(row=4, column=0)
            tk.Label(receipt_tk, text="결제 금액        %d 원" % menu.total_to_pay()).grid(row=5, column=0)
            tk.Label(receipt_tk, text="카드 잔액        %d 원" % card.balance).grid(row=6, column=0)
            tk.Label(receipt_tk, text="적립금      %d point" % card.rewards).grid(row=7, column=0)
            self._receipt = 1


Demo = MainWindow()
Mobile = Mobile()
Demo.mainloop()