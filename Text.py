import time
current_time_ids = time.time()
aa1 = {}  # 辞書を使うよ！
aaa1 = set()
bbb2 = set()
gg1 = (1, 2, 3 ,4 , 5 , 10 , 15)  # ทูเพิล
gg2 = (4, 5, 6 ,7, 8 ,9)  # ทูเพิล

# เพิ่มตัวเลขจาก gg1 เข้า aaa1
for num in gg1:
    aaa1.add(num)

# เพิ่มตัวเลขจาก gg2 เข้า bbb2
for num in gg2:
    bbb2.add(num)

print(aaa1 - bbb2)  # 差集合
print(aaa1 & bbb2)  # 差集合

# track_id = 1 , 2 , 3, 4,5
# aa1[track_id] = current_time_ids
# print(aa1)