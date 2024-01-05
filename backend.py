import mysql.connector
import timeit
"""
require: mysql-connector-python
"""

mydb = mysql.connector.connect(host="cnpm-ittn.mysql.database.azure.com",
                               user="tuecm",
                               password="12345cmt#",
                               database="mydb")

print(mydb)

cursor = mydb.cursor()
cursor.execute("show tables")
col_info = {}
for x in cursor.fetchall():
  """#print(x[0])
    command = f"select * from {x[0]} where NULL"
    #print(command)
    cursor.execute(command)
    #print(cursor.description)
    count_col[x[0]] = len(cursor.description)
    cursor.fetchall()"""
  command = f"show columns from {x[0]}"
  cursor.execute(command)
  col_info[x[0]] = [(x[0], x[3]) for x in cursor.fetchall()]
  #print(col_info[x[0]])


def commit():
  # luu cac thay doi cua database
  mydb.commit()


def create(table_name, value, position=None):
  # Tao record moi trong bang table_name (co the nhieu record)
  # value la LIST cac record
  # position la cac cot co gia tri them vao hoac None neu them het cac cot
  # chua commit data
  command = "insert into {} {} values ({})".format(
      table_name, f"({','.join(position)})" if position else "",
      ("%s," * len(position if position else col_info[table_name]))[:-1])
  #print(command)
  if (len(value) == 0):
    return
  cursor.executemany(command, value)


def modify(table_name, position, value, primary_key, index):
  # thay doi 1 record trong bang table_name tai position voi gia tri value
  # index dinh danh cho record can thay doi theo primary_key
  # chua commit data
  """command = f"update {table_name} set "
    flag = 0
    for x in zip(position, value):
        if not flag:
            flag = 1
        else:
            command += ','
        command += f"{x[0]} = '{x[1]}' "
        #print(x[0], x[1])
    command += f"where {primary_key} = '{index}'"""
  list_change = [f"{x[0]} = '{x[1]}'" for x in zip(position, value)]
  command = f"update {table_name} set {','.join(list_change)} where {primary_key} = '{index}'"
  #print(command)
  cursor.execute(command)


def delete(table_name, conditions):
  # xoa 1 record khoi bang table_name thoa man tap cac conditions
  # chua commit data
  """command = f"delete from {table_name} where "
    flag = 0
    for x in conditions:
        if flag:
            command += " and "
        else :
            flag = 1
        command += x"""
  command = "delete from {} {}".format(
      table_name,
      "where " + ' and '.join([(x[1].replace("$", x[0]))
                               for x in conditions]) if conditions else "")
  #print(command)
  cursor.execute(command)


def join_all(table_name):
  if len(table_name) == 0:
    return -1
  flag = [-1] * len(table_name)

  def find(x):
    if flag[x] < 0:
      return x
    flag[x] = find(flag[x])
    return flag[x]

  ans = [f"{x}" for x in table_name]
  for id, x in enumerate(table_name):
    list_name = {v[0] for v in col_info[x]}
    for pos, y in enumerate(table_name):
      if pos == id:
        break
      if find(id) == find(pos):
        continue
      for name in col_info[y]:
        if name[0] in list_name:
          ans[find(
              pos
          )] += f" join ({ans[find(id)]}) on {x}.{name[0]} = {y}.{name[0]} "
          flag[find(id)] = find(pos)
          break
  return ans[find(0)]


#print(join_all(["tai_khoan", "nhan_khau", "ho_gd"]))


def show(table_name,
         column_name=None,
         conditions=None,
         group_by=None,
         special_column_name=None,
         condition_aggressive=None,
         sort_by=None,
         limit=None,
         isLower=False):
  """
    tim kiem du lieu trong LIST bang table_name
    column_name: cac cot in ra trong bang ket qua
    conditions: LIST bien dieu kien va dieu kien chon. (thay the ten bien bang $)
    ex: (id <= 4) -> bien dk = id, dk = ($ <= 4)
    special_column_name: LIST cac ten dac biet (cac ham tinh toan)
    ex: a * b voi ten c la ten cot ket qua -> special_column_name = ["a", "b"], "{} * {}", "c"
    group_by: gop theo bien nao
    condition_aggressive: tuong tu conditions nhung dung voi aggressive
    sort_by: sap xep theo bien nao
    limit: gioi han so record trong bang ket qua
    """
  prefix = {"*": "*", "": ""}

  def find(x):
    x = x.lower()
    if x in prefix:
      return prefix[x]
    for table in table_name:
      #print(table, col_info[table])
      if x in [x[0].lower() for x in col_info[table]]:
        prefix[x] = f"{table}.{x}"
        return prefix[x]
    assert (False)

  full_column_name = [find(x) for x in column_name
                      if x] if column_name else []  # cho phep trong
  #full_column_name = [f"allin.{x}" for x in column_name]
  """print(f"top {limit}" if limit else "fail")
    print(','.join(full_column_name))
    print(join_all(table_name))
    print(','.join(conditions))
    print(f"order by {sort_by}" if sort_by else "fail")"""
  command = "select {} from ({}) {} {} {} {} {}"
  all_table = join_all(table_name)
  command = command.format(
      ','.join(full_column_name + ([
          x[1].format(*(find(y) for y in x[0])) + f" as {x[2]}" if x[2] else ""
          for x in special_column_name
      ] if special_column_name else [])),
      all_table,
      "where " +
      ' and '.join([x[1].replace("$", find(x[0]))
                    for x in conditions]) if conditions else "",
      f"group by {find(group_by)}" if group_by else "",
      "having " + ' and '.join([
          x[1].replace(
              "$", x[0]
          )  # toi co tinh bo find(x[0]) vi having co the yeu cau func(x)
          for x in condition_aggressive
      ]) if condition_aggressive else "",
      f"order by {find(sort_by)}" if sort_by else "",
      f"limit {limit}" if limit else "")
  print(command)
  cursor.execute(command)
  """for x in cursor:
        print(x)"""
  return [
      dict(
          zip([
              x[0].lower() if isLower and isinstance(x[0], str) else x[0]
              for x in cursor.description
          ], x)) for x in cursor.fetchall()
  ]


"""
create("loai_phong", [("1","vip", "100", "100000")])
create("ho_gd", [("1", "onlooker", "1", "777", "1")])
cursor.execute("select * from ho_gd")
for x in cursor:
    print(x)"""
#value = show(["tai_khoan", "ho_gd"], [], [("id_tai_khoan","$ between 1 and 7"), ("id_ho","$ =1")], limit = 2, sort_by="id_tai_khoan")
#show(["tai_khoan"], ["mat_khau"], group_by="mat_khau", condition_aggressive=[("", "count(*) > 1")],limit = 100, sort_by="")
#print(value)
