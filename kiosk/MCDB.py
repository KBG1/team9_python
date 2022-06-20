import sqlite3


mc_con = sqlite3.connect("mcDB")
mc_cur = mc_con.cursor()

# 주문 및 쿠폰 테이블
mc_cur.execute("CREATE TABLE orders (menuID TEXT NOT NULL, menuName TEXT, quantity INT, finalCost INT, subto TEXT, updateTime TEXT DEFAULT(datetime('now','localtime')), coupon INT DEFAULT(0))")
mc_cur.execute("CREATE TABLE coupon (couponID TEXT PRIMARY KEY NOT NULL, menuID INT, menuName TEXT, Cost INT, DCrate INT, DCprice INT)")
# 카테고리별로 테이블 분류함
mc_cur.execute("CREATE TABLE menu (menuID TEXT PRIMARY KEY NOT NULL, menuName TEXT, category INT, menutype INT, price INT, calData INT, show INT)")
mc_cur.execute("CREATE TABLE sets (setID TEXT PRIMARY KEY NOT NULL, setName TEXT, category INT, menutype INT, price INT, calData INT)")

'''
menuID _ _ _ _ _ _

1 : menutype
2 : 카테고리 대분류코드
3 : 카테고리 소분류코드
4,5 : 상품순서코드(카테고리 내 순서의 역순으로 부여)
6 : 부속

menutype
- 일반메뉴 : A
- 세트메뉴 : B
- 부가메뉴 : C

카테고리 분류코드
- 추천메뉴 : 0
- 버거 : 1
- 해피스낵 : 2
- 사이드 : 3
- 커피 : 4
- 디저트 : 5
- 음료 : 6
- 해피밀 : 7

카테고리 내 분류코드 / 카테고리 내 분류코드가 바뀌면 제품번호 다시 1부터 ex) 1001...~1013 후 1101부터 시작
0, 1
디저트 : 0(아이스크림) 1(파이류)
드링크 : 0(음료) 1(맥카페)

'''
# 추천메뉴 - ?

# 버거 - 21개
mc_cur.execute("INSERT INTO menu VALUES('A10010', '햄버거', 1, 2, 2000, 265, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10020', '치즈버거', 1, 2, 2300, 317, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10030', '더블치즈버거', 1, 2, 4400, 478, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10040', '트리플치즈버거', 1, 2, 5600, 619, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10050', '쿼터파운더 치즈', 1, 2, 5200, 534, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10060', '더블 쿼터파운더 치즈', 1, 2, 7000, 769, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10070', '베이컨 토마토 디럭스', 1, 2, 5500, 545, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10080', '슈슈 버거', 1, 2, 4500, 432, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10090', '슈비 버거', 1, 2, 5500, 563, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10100', '불고기 버거', 1, 2, 2200, 409, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10110', '더블 불고기 버거', 1, 2, 4400, 636, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10120', '에그 불고기 버거', 1, 2, 3200, 492, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10130', '맥치킨', 1, 2, 3300, 483, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10140', '맥치킨 모짜렐라', 1, 2, 4800, 686, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10150', '빅맥', 1, 2, 4600, 583, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10160', '1955버거', 1, 2, 5700, 537, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10170', '맥스파이스 상하이 버거', 1, 2, 4600, 494, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10180', '필레 오 피쉬', 1, 2, 3500, 342, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10190', '더블 필레 오 피쉬', 1, 2, 5000, 481, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10200', '맥크리스피 클래식 버거', 1, 2, 5600, 584, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A10210', '맥크리스피 디럭스 버거', 1, 2, 6400, 594, 1)")

# 해피스낵 - 시즌별 인기메뉴 할인 - 9개
mc_cur.execute("INSERT INTO menu VALUES('A20010', '아이스 아메리카노 L', 2, 1, 2400, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A20020', '치즈버거', 2, 1, 2300, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A20030', '에그 불고기 버거', 2, 1, 2500, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A20040', '골든 모짜렐라 치즈스틱 2조각', 2, 1, 1500, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A20050', '필레 오 피쉬', 2, 1, 2500, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A20060', '소시지 스낵랩', 2, 1, 2400, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A20070', '체리 맥피즈 스프라이트 M', 2, 1, 1900, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A20080', '체리 맥피즈 코카-콜라 M', 2, 1, 1900, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A20090', '개수맞추기용', 2, 1, 1000, 0, 1)")

# 사이드 - 18개
mc_cur.execute("INSERT INTO menu VALUES('A30010', '케이준 소스', 3, 1, 300, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A30020', '스위트 앤 사워 소스', 3, 1, 300, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A30030', '스위트 칠리 소스', 3, 1, 300, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A30040', '스트링치즈', 3, 1, 1600, 50, 1)")
mc_cur.execute("INSERT INTO menu VALUES('C30050', '후렌치 후라이', 3, 3, 1700, 332, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A30051', '후렌치 후라이 S', 3, 1, 1000, 216, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A30052', '후렌치 후라이 M', 3, 1, 1700, 332, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A30053', '후렌치 후라이 L', 3, 1, 2300, 408, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A30060', '맥스파이시 치킨텐더 4조각', 3, 1, 4900, 352, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A30070', '맥스파이시 치킨텐더 2조각', 3, 1, 2500, 176, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A30080', '골든 모짜렐라 치즈스틱 4조각', 3, 1, 4000, 319, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A30090', '골든 모짜렐라 치즈스틱 2조각', 3, 1, 2200, 159, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A30100', '맥너겟 10조각', 3, 1, 4500, 427, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A30110', '맥너겟 6조각', 3, 1, 2500, 256, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A30120', '맥너겟 4조각', 3, 1, 1800, 171, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A30130', '소시지 스낵랩', 3, 1, 2100, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A30140', '상하이 치킨 스낵랩', 3, 1, 2000, 276, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A30150', '코울슬로', 3, 1, 2200, 200, 1)")

# 커피-맥카페 - 15개
mc_cur.execute("INSERT INTO menu VALUES('C40030', '아메리카노', 4, 3, 2200, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A40031', '아메리카노 S', 4, 1, 2200, 11, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40032', '아메리카노 M', 4, 1, 2200, 12, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40033', '아메리카노 L', 4, 1, 2200, 15, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C40040', '디카페인 아메리카노', 4, 3, 2300, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A40041', '디카페인 아메리카노 S', 4, 1, 2300, 8, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40042', '디카페인 아메리카노 M', 4, 1, 2300, 12, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40043', '디카페인 아메리카노 L', 4, 1, 2300, 11, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C40050', '아이스 아메리카노', 4, 3, 2200, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A40051', '아이스 아메리카노 M', 4, 1, 2200, 9, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40052', '아이스 아메리카노 L', 4, 1, 2200, 10, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C40060', '디카페인 아이스 아메리카노', 4, 3, 2300, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A40061', '디카페인 아이스 아메리카노 M', 4, 1, 2300, 8, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40062', '디카페인 아이스 아메리카노 L', 4, 1, 2300, 10, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C40070', '카페라떼', 4, 3, 2500, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A40071', '카페라떼 S', 4, 1, 2500, 103, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40072', '카페라떼 M', 4, 1, 2500, 149, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40073', '카페라떼 L', 4, 1, 2500, 194, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C40080', '디카페인 카페라떼', 4, 3, 2600, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A40081', '디카페인 카페라떼 S', 4, 1, 2600, 104, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40082', '디카페인 카페라떼 M', 4, 1, 2600, 150, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40083', '디카페인 카페라떼 L', 4, 1, 2600, 190, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C40090', '아이스 카페라떼', 4, 3, 2500, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A40091', '아이스 카페라떼 M', 4, 1, 2500, 108, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40092', '아이스 카페라떼 L', 4, 1, 2500, 133, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C40100', '디카페인 아이스 카페라떼', 4, 3, 0, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A40101', '디카페인 아이스 카페라떼 M', 4, 1, 2600, 114, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40102', '디카페인 아이스 카페라떼 L', 4, 1, 2600, 133, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C40110', '드립 커피', 4, 3, 1500, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A40111', '드립 커피 S', 4, 1, 1500, 7, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40112', '드립 커피 M', 4, 1, 1500, 10, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40113', '드립 커피 L', 4, 1, 1500, 12, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C40120', '아이스 드립 커피', 4, 3, 1000, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A40121', '아이스 드립 커피 M', 4, 1, 1000, 10, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40122', '아이스 드립 커피 L', 4, 1, 1000, 14, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C40130', '카푸치노', 4, 3, 2500, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A40131', '카푸치노 S', 4, 1, 2500, 68, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40132', '카푸치노 M', 4, 1, 2500, 93, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40133', '카푸치노 L', 4, 1, 2500, 120, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C40140', '디카페인 카푸치노', 4, 3, 2600, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A40141', '디카페인 카푸치노 S', 4, 1, 2600, 67, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40142', '디카페인 카푸치노 M', 4, 1, 2600, 89, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40143', '디카페인 카푸치노 L', 4, 1, 2600, 120, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C40150', '바닐라 라떼', 4, 3, 2500, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A40151', '바닐라 라떼 M', 4, 1, 2500, 227, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40152', '바닐라 라떼 L', 4, 1, 2500, 323, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C40160', '아이스 바닐라 라떼', 4, 3, 2600, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A40161', '아이스 바닐라 라떼 M', 4, 1, 2600, 186, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A40162', '아이스 바닐라 라떼 L', 4, 1, 2600, 263, 0)")
# 일반메뉴
mc_cur.execute("INSERT INTO menu VALUES('A40010', '에스프레소', 4, 1, 1500, 0, 1)")
# mc_cur.execute("INSERT INTO menu VALUES('A40020', '디카페인 에스프레소', 4, 1, 1600, 0, 1)")

# 디저트
# 아이스크림
mc_cur.execute("INSERT INTO menu VALUES('A50010', '베리스트로베리 맥플러리', 5, 1, 2500, 325, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A50020', '허쉬 프레첼 맥플러리', 5, 1, 2900, 400, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A50030', '오레오 맥플러리', 5, 1, 2500, 348, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A50040', '딸기 오레오 맥플러리', 5, 1, 2500, 320, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A50050', '초코 오레오 맥플러리', 5, 1, 2500, 404, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A50060', '오레오 아포가토', 5, 1, 3000, 247, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A50070', '아이스크림콘', 5, 1, 700, 154, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A50080', '초코콘', 5, 1, 900, 230, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A50090', '스트로베리콘', 5, 1, 900, 140, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A50100', '초코 선데이 아이스크림', 5, 1, 1500, 339, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A50110', '딸기 선데이 아이스크림', 5, 1, 1500, 292, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A50120', '바닐라 선데이 아이스크림', 5, 1, 1500, 0, 1)")
# 파이
mc_cur.execute("INSERT INTO menu VALUES('A51010', '애플 파이', 5, 1, 1200, 236, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A51020', '콘파이 파이', 5, 1, 1200, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A51030', '블루베리 파이', 5, 1, 1200, 0, 1)")
# mc_cur.execute("INSERT INTO menu VALUES('A51040', '타로 파이', 5, 1, 1200, 0, 1)")
# mc_cur.execute("INSERT INTO menu VALUES('A51050', '리치초콜릿 파이', 5, 1, 1200, 0, 1)")

# 음료 - 15개
# 부가메뉴
# 쉐이크는 m사이즈만 존재
# 그 외 음료는 기본m사이즈에 사이즈업시 +-500원씩 적용
mc_cur.execute("INSERT INTO menu VALUES('C60060', '자두 칠러', 6, 3, 2700, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A60061', '자두 칠러 S', 6, 1, 2000, 143, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A60062', '자두 칠러 M', 6, 1, 2700, 198, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A60063', '자두 칠러 L', 6, 1, 3700, 292, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C60070', '애플망고 칠러', 6, 3, 2700, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A60071', '애플망고 칠러 S', 6, 1, 2000, 178, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A60072', '애플망고 칠러 M', 6, 1, 2700, 251, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A60073', '애플망고 칠러 L', 6, 1, 3700, 389, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C60080', '제주 한라봉 칠러', 6, 3, 2700, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A60081', '제주 한라봉 칠러 S', 6, 1, 2000, 165, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A60082', '제주 한라봉 칠러 M', 6, 1, 2700, 236, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A60083', '제주 한라봉 칠러 L', 6, 1, 3700, 365, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C60090', '코카-콜라', 6, 3, 1300, 108, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A60091', '코카-콜라 S', 6, 1, 800, 101, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A60092', '코카-콜라 M', 6, 1, 1300, 143, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A60093', '코카-콜라 L', 6, 1, 1800, 198, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C60100', '코카-콜라 제로', 6, 3, 1300, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A60101', '코카-콜라 제로 S', 6, 1, 800, 0, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A60102', '코카-콜라 제로 M', 6, 1, 1300, 0, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A60103', '코카-콜라 제로 L', 6, 1, 1800, 0, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C60110', '스프라이트', 6, 3, 1300, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A60111', '스프라이트 S', 6, 1, 800, 106, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A60112', '스프라이트 M', 6, 1, 1300, 149, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A60113', '스프라이트 L', 6, 1, 1800, 206, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C60120', '환타', 6, 3, 1300, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A60121', '환타 S', 6, 1, 800, 44, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A60122', '환타 M', 6, 1, 1300, 62, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A60123', '환타 L', 6, 1, 1800, 86, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C60130', '체리 맥피즈 스프라이트', 6, 3, 1900, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A60131', '체리 맥피즈 스프라이트 M', 6, 1, 1900, 224, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A60132', '체리 맥피즈 스프라이트 L', 6, 1, 2400, 327, 0)")
mc_cur.execute("INSERT INTO menu VALUES('C60140', '체리 맥피즈 코카-콜라', 6, 3, 1900, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A60141', '체리 맥피즈 코카-콜라 M', 6, 1, 1900, 220, 0)")
mc_cur.execute("INSERT INTO menu VALUES('A60142', '체리 맥피즈 코카-콜라 L', 6, 1, 2400, 321, 0)")
# 일반메뉴
mc_cur.execute("INSERT INTO menu VALUES('A60010', '생수', 6, 1, 1200, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A60020', '우유', 6, 1, 1500, 125, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A60030', '바닐라 쉐이크 M', 6, 1, 2500, 344, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A60040', '딸기 쉐이크 M', 6, 1, 2500, 350, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A60050', '초코 쉐이크 M', 6, 1, 2500, 344, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A60060', '개수맞추기용', 6, 1, 2000, 0, 1)")

# 해피밀
mc_cur.execute("INSERT INTO menu VALUES('A70010', '해피밀 에그 맥머핀', 7, 1, 3500, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A70020', '해피밀 베이컨 에그 맥머핀', 7, 1, 3800, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A70030', '해피밀 소시지 에그 맥머핀', 7, 1, 3800, 0, 1)")
mc_cur.execute("INSERT INTO menu VALUES('A70040', '해피밀 핫케익 2조각', 7, 1, 3800, 0, 1)")

'''# 맥모닝
mc_cur.execute("INSERT INTO menu VALUES('핫케익', 2300, 0, 5001)")
mc_cur.execute("INSERT INTO menu VALUES('핫케익 2조각', 2300, 0, 5001)")
mc_cur.execute("INSERT INTO menu VALUES('핫케익 3조각', 3000, 0, 5002)")
mc_cur.execute("INSERT INTO menu VALUES('디럭스 브렉퍼스트', 4800, 0, 5003)")
mc_cur.execute("INSERT INTO menu VALUES('상하이 치킨 스낵랩', 1500, 0, 5005)")
mc_cur.execute("INSERT INTO menu VALUES('소시지 에그 맥머핀', 3000, 0, 5006)")
mc_cur.execute("INSERT INTO menu VALUES('소시지 에그 맥머핀 콤보', 3400, 0, 5007)")
mc_cur.execute("INSERT INTO menu VALUES('베이컨 에그 맥머핀', 3000, 0, 5009)")
mc_cur.execute("INSERT INTO menu VALUES('베이컨 에그 맥머핀 콤보', 3400, 0, 5010)")
mc_cur.execute("INSERT INTO menu VALUES('에그 맥머핀', 2500, 0, 5012)")
mc_cur.execute("INSERT INTO menu VALUES('에그 맥머핀 콤보', 2900, 0, 5013)")
mc_cur.execute("INSERT INTO menu VALUES('치킨 치즈 머핀', 3200, 0, 5015)")
mc_cur.execute("INSERT INTO menu VALUES('베이컨 토마토 에그 머핀', 3600, 0, 5017)")
mc_cur.execute("INSERT INTO menu VALUES('소시지 토마토 에그 소프트 번', 3800, 0, 5019)")
mc_cur.execute("INSERT INTO menu VALUES('베이컨 토마토 에그 소프트 번', 3600, 0, 5021)")
'''

# 세트구성
burger_set = {
    "side": [
        "A30050",
        "A30090",
        "B30050"
    ],
    "drink": []
}
# 버거
mc_cur.execute("INSERT INTO sets VALUES('B10010', '햄버거-세트', 1, 2, 3400, 0)")
mc_cur.execute("INSERT INTO sets VALUES('B10020', '치즈버거-세트', 1, 2, 3700, 0)")
mc_cur.execute("INSERT INTO sets VALUES('B10030', '더블치즈버거-세트', 1, 2, 5800, 0)")
mc_cur.execute("INSERT INTO sets VALUES('B10040', '트리플치즈버거-세트', 1, 2, 7000, 0)")
mc_cur.execute("INSERT INTO sets VALUES('B10050', '쿼터파운더 치즈-세트', 1, 2, 6600, 0)")
mc_cur.execute("INSERT INTO sets VALUES('B10060', '더블 쿼터파운더 치즈-세트', 1, 2, 8400, 0)")
mc_cur.execute("INSERT INTO sets VALUES('B10070', '베이컨 토마토 디럭스-세트', 1, 2, 6900, 0)")
mc_cur.execute("INSERT INTO sets VALUES('B10080', '슈슈 버거-세트', 1, 2, 5900, 0)")
mc_cur.execute("INSERT INTO sets VALUES('B10090', '슈비 버거-세트', 1, 2, 6900, 0)")
mc_cur.execute("INSERT INTO sets VALUES('B10100', '불고기 버거-세트', 1, 2, 3600, 0)")
mc_cur.execute("INSERT INTO sets VALUES('B10110', '더블 불고기 버거-세트', 1, 2, 5800, 0)")
mc_cur.execute("INSERT INTO sets VALUES('B10120', '에그 불고기 버거-세트', 1, 2, 4600, 0)")
mc_cur.execute("INSERT INTO sets VALUES('B10130', '맥치킨-세트', 1, 2, 4700, 0)")
mc_cur.execute("INSERT INTO sets VALUES('B10140', '맥치킨 모짜렐라-세트', 1, 2, 6200, 0)")
mc_cur.execute("INSERT INTO sets VALUES('B10150', '빅맥-세트', 1, 2, 6000, 0)")
mc_cur.execute("INSERT INTO sets VALUES('B10160', '1955버거-세트', 1, 2, 7100, 0)")
mc_cur.execute("INSERT INTO sets VALUES('B10170', '맥스파이스 상하이 버거-세트', 1, 2, 6000, 0)")
mc_cur.execute("INSERT INTO sets VALUES('B10180', '필레 오 피쉬-세트', 1, 2, 4900, 0)")
mc_cur.execute("INSERT INTO sets VALUES('B10190', '더블 필레 오 피쉬-세트', 1, 2, 6400, 0)")
mc_cur.execute("INSERT INTO sets VALUES('B10200', '맥크리스피 클래식 버거-세트', 1, 2, 7000, 916)")
mc_cur.execute("INSERT INTO sets VALUES('B10210', '맥크리스피 디럭스 버거-세트', 1, 2, 7800, 927)")
# 사이드
mc_cur.execute("INSERT INTO sets VALUES('B30050', '후렌치 후라이 M + 골든 모짜렐라 치즈스틱 2조각', 3, 2, 3900, 548)")

# 해피스낵

# 해피밀

'''# 맥모닝
mc_cur.execute("INSERT INTO sets VALUES(B?????, '디럭스 브렉퍼스트 세트', 5800, 0, 5004)")
mc_cur.execute("INSERT INTO sets VALUES(B?????, '소시지 에그 맥머핀 세트', 4000, 0, 5008)")
mc_cur.execute("INSERT INTO sets VALUES(B?????, '베이컨 에그 맥머핀 세트', 4000, 0, 5011)")
mc_cur.execute("INSERT INTO sets VALUES(B?????, '에그 맥머핀 세트', 3500, 0, 5014)")
mc_cur.execute("INSERT INTO sets VALUES(B?????, '치킨 치즈 머핀 세트', 4200, 0, 5016)")
mc_cur.execute("INSERT INTO sets VALUES(B?????, '베이컨 토마토 에그 머핀 세트', 4500, 0, 5018)")
mc_cur.execute("INSERT INTO sets VALUES(B?????, '소시지 토마토 에그 소프트 번 세트', 4800, 0, 5020)")
mc_cur.execute("INSERT INTO sets VALUES(B?????, '베이컨 토마토 에그 소프트 번 세트', 4600, 0, 5022)")
'''


mc_con.commit()
mc_con.close()