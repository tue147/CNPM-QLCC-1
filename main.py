from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from backend import *
import random
import json
import datetime

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
app.secret_key = 'bruh dark lmao'


@app.route('/')
def main():
  return render_template('home.html')


@app.route('/login')
def login():
  try:
    if 'id' in session:
      return redirect('/admin' if session['admin'] else '/user')
  except:
    pass
  return render_template('login.html', error={'error_code': ""})


@app.route('/logout')
def logout():
  try:
    session.pop('id', None)
    session.pop('admin', None)
  except:
    pass
  return redirect('/')


@app.route('/api/login', methods=['POST'])
def login_verify():
  username = request.form.get('username')
  password = request.form.get('password')
  print(username, password, request.form)
  try:
    find_account = show(['tai_khoan'], ['*'],
                        [('ten_dang_nhap', f'$ = "{username}"'),
                         ('mat_khau', f'$ = "{password}"')])
    if len(find_account) != 1:
      print("failed")
      return render_template(
          'login.html',
          error={'error_code': 'Tài khoản hoặc mật khẩu không tồn tại'})
    else:
      print("success", find_account)
      # print(acc)
      session['id'] = find_account[0]['ID_TAI_KHOAN']
      session['admin'] = find_account[0]['ADMIN']
      if session['admin']:
        #return render_template('admin.html', user={'user':'admin'})
        return redirect('/admin')
      else:
        #return render_template('user.html', user={'user':'user'})
        return redirect('/user')

  except:
    return render_template('error.html')


@app.route('/register')
def register():
  return 1


@app.route('/ADMIN/add')
def add_account():
  return render_template('form_taikhoan.html',
                         taikhoan={
                             'title': 'Thêm Tài Khoản',
                             'func': 'add',
                             'form_name': 'Account Form'
                         })


@app.route('/ADMIN/update')
def update_account():
  return render_template('form_taikhoan.html',
                         taikhoan={
                             'title': 'Update Tài Khoản',
                             'func': 'update',
                             'form_name': 'Account Form'
                         })


@app.route('/ADMIN/delete')
def delete_account():
  return render_template('form_delete.html',
                         format={
                             'title': 'Xóa tài khoản',
                             'class': 'ADMIN',
                             'name': 'ID_TAI_KHOAN',
                             'label': 'ID tài khoản'
                         })


@app.route('/ADMIN/<func>/apply', methods=['POST'])
def account_apply(func):
  if func == 'add':
    # insert taikhoan
    data = request.form
    print(data)
    values = [data.get(key) for key in data]
    values = [
        0 if item == 'User' else 1 if item == 'Admin' else item
        for item in values
    ]
    check = True
    while check:
      id_taikhoan = random.randint(1, 99999999)
      taikhoan = show(['tai_khoan'], ['*'],
                      [('id_tai_khoan', f'$ = {id_taikhoan}')])
      if len(taikhoan) == 0:
        check = False
    values.insert(0, id_taikhoan)
    print((values))
    # values.append('test')
    try:
      create('tai_khoan', [tuple(values)])
    except:
      return render_template('error.html')
    # commit()
    return render_template('submit_confirmation.html')

  elif func == "delete":
    data = request.form
    id = data.get('ID_TAI_KHOAN')
    print(id)
    find_account = show(['tai_khoan'], ['*'], [('ID_TAI_KHOAN', f'$ = {id}')])
    if len(find_account) == 1:
      delete('tai_khoan', conditions=[(id, "ID_TAI_KHOAN = $")])
      # commit()
      return render_template('submit_confirmation.html')
    else:
      return render_template('error.html')

  elif func == "update":
    data = request.form
    print(data)
    tendangnhap = data.get('TEN_DANG_NHAP')
    data = {k: v for k, v in data.items()}
    # check ten dang nhap
    account = show(['tai_khoan'], ['*'],
                   [('ten_dang_nhap', f'$ = "{tendangnhap}"')])
    id_taikhoan = -1
    if len(account) != 1:
      return render_template('error.html')
    else:
      id_taikhoan = account[0]['ID_TAI_KHOAN']

    if data['ADMIN'] == 'Admin':
      data['ADMIN'] = 1
    else:
      data['ADMIN'] = 0
    print(data)
    modify('tai_khoan',
           position=data.keys(),
           value=data.values(),
           index=id_taikhoan,
           primary_key="ID_TAI_KHOAN")
    # commit()
    return render_template('submit_confirmation.html')

  else:
    return render_template("error.html")


@app.route('/api/ADMIN/history')
def admin_history():
  return redirect('/admin')


@app.route('/api/USER/history')
def user_history():
  return redirect('/user')


@app.route('/admin')
def admin():
  data_tk = show(
      ['tai_khoan'],
      ['*'],
  )
  #print(data_hk)
  return render_template('admin.html',
                         user={
                             'user': 'admin',
                             'USER': 'ADMIN',
                             'data': data_tk
                         })


@app.route('/user')
def user():
  return render_template('user.html', user={'user': 'user', 'USER': 'USER'})


'''
Ho Khau
'''


@app.route('/api/HK/history')
def HK_history():
  try:
    if 'id' in session:
      if session['admin']:
        data_hk = show(['lich_su_ho_gd'], ['*'])
        return render_template('main_HK_history.html',
                               user={
                                   'user': 'admin',
                                   'USER': 'HK',
                                   'data': data_hk,
                               })  # update for admin
      else:
        data_hk = show(['lich_su_ho_gd'], ['*'],
                       conditions=[('id_tai_khoan', f'$ = {session["id"]}')])
        return render_template('main_HK_history.html',
                               user={
                                   'user': 'user',
                                   'USER': 'HK',
                                   'data': data_hk
                               })  # update for user
  except:
    pass
  return redirect('/login')  # if something wrong: redirect to login


@app.route('/api/HK')
def HK():
  # top 100 du lieu trong database
  # all data = [ { ...} ]
  try:
    if 'id' in session:
      if session['admin']:
        data_hk = show(['ho_gd'], ['*'])
        return render_template('main_hokhau.html',
                               user={
                                   'user': 'admin',
                                   'USER': 'HK',
                                   'data': data_hk,
                               })  # update for admin
      else:
        data_hk = show(['ho_gd'], ['*'],
                       conditions=[('id_tai_khoan', f'$ = {session["id"]}')])
        return render_template('main_hokhau.html',
                               user={
                                   'user': 'user',
                                   'USER': 'HK',
                                   'data': data_hk
                               })  # update for user
  except:
    pass
  return redirect('/login')  # if something wrong: redirect to login


@app.route('/api/HK/add')
def HK_add():
  stt = show(['lich_su_ho_gd'],
             special_column_name=[(['stt'], "max({})", "max_stt")],
             column_name=[None])
  return render_template('form_hokhau.html',
                         hokhau={
                             'title':
                             'Thêm Hộ Khẩu',
                             'func':
                             'add',
                             'form_name':
                             'Household Form',
                             'stt': (stt[0]['max_stt'] +
                                     1) if stt[0]['max_stt'] else 1,
                         })


@app.route('/api/HK/update')
def HK_update():
  stt = show(['lich_su_ho_gd'],
             special_column_name=[(['stt'], "max({})", "max_stt")],
             column_name=[None])
  return render_template('form_hokhau.html',
                         hokhau={
                             'title':
                             'Thay đổi Hộ Khẩu',
                             'func':
                             'update',
                             'form_name':
                             'Household Form',
                             'stt': (stt[0]['max_stt'] +
                                     1) if stt[0]['max_stt'] else 1,
                         })


@app.route('/api/HK/delete')
def HK_delete():
  return render_template('form_delete.html',
                         format={
                             'title': 'Xóa Hộ Khẩu',
                             'class': 'api/HK',
                             'name': 'ID Hộ',
                             'label': 'ID Hộ'
                         })


@app.route('/api/HK/<func>/apply', methods=['post'])
def HK_apply(func):
  data = request.form

  if func == "add":
    # insert ho khau
    data = request.form
    print(data)
    values = [data.get(key) for key in data]
    values = [
        0 if item == 'standard' else 1 if item == 'deluxe' else item
        for item in values
    ]
    find_idtk = show(['tai_khoan'], ['ID_TAI_KHOAN'],
                     [('ID_TAI_KHOAN', f'$ = {values[3]}')])
    values.append("Add")
    values_without_history = values.copy()
    values_without_history.pop()  # remove type
    values_without_history.pop()  # remove date
    values_without_history.remove(values_without_history[0])  # remove stt
    print((values))
    print(find_idtk)
    if len(find_idtk) != 1:
      return render_template('error.html')
    try:
      create('ho_gd', [tuple(values_without_history)])
      create('lich_su_ho_gd', [tuple(values)])
    except:
      return render_template('error.html')
    # commit()
    return render_template('submit_confirmation.html')

  elif func == "update":
    data = request.form
    print(data)
    id = data.get('ID_HO')
    data = {k: v for k, v in data.items()}
    data['LOAI_SUA_DOI'] = 'Update'
    if data['LOAI_PHONG'] == 'standard':
      data['LOAI_PHONG'] = 0
    else:
      data['LOAI_PHONG'] = 1
    values = [data.get(key) for key in data]
    print(values)
    data_without_history = data.copy()
    del data_without_history['NGAY_SUA_DOI']
    del data_without_history['LOAI_SUA_DOI']
    del data_without_history['stt']
    del data_without_history['ID_HO']
    find_hogd = show(['ho_gd'], ['*'], [('ID_HO', f'$ = {id}')])
    find_idtk = show(['tai_khoan'], ['ID_TAI_KHOAN'],
                     [('ID_TAI_KHOAN', f'$ = {data["ID_TAI_KHOAN"]}')])
    if len(find_hogd) == 1 and len(find_idtk) == 1:
      try:
        modify('ho_gd',
               position=data_without_history.keys(),
               value=data_without_history.values(),
               index=id,
               primary_key="ID_HO")
        create('lich_su_ho_gd', [tuple(values)])
      except:
        return render_template('error.html')
      # commit()
      return render_template('submit_confirmation.html')
    else:
      return render_template('error.html')

  elif func == "delete":
    id = data.get('ID Hộ')
    time = data.get('NGAY_THAY_DOI')
    print(id)
    find_account = show(['ho_gd'], ['*'], [('id_ho', f'$ = {id}')])
    if len(find_account) == 1:
      try:
        stt = show(['lich_su_ho_gd'],
                   special_column_name=[(['stt'], "max({})", "max_stt")],
                   column_name=[None])
        delete('ho_gd', conditions=[(id, "ID_HO = $")])
        values = [(stt[0]['max_stt'] + 1) if stt[0]['max_stt'] else 1,
                  find_account[0]['ID_HO'], find_account[0]['CHU_HO'],
                  find_account[0]['ID_TAI_KHOAN'], find_account[0]['SO_PHONG'],
                  find_account[0]['LOAI_PHONG'], time, "Delete"]
        create('lich_su_ho_gd', [tuple(values)])
        # commit()
      except:
        return render_template('error.html')
      return render_template('submit_confirmation.html')
    else:
      return render_template("error.html")

  else:
    return render_template("error.html")


@app.route('/api/getFormID_HO')
def get_form_idHo():
  idHo = request.args.get('idHo')
  data = show(['ho_gd'], ['*'], [('ID_HO', f'$ = {idHo}')])
  print(data)
  if len(data) == 1:
    if data[0]['LOAI_PHONG'] == 0:
      data[0]['LOAI_PHONG'] = 'standard'
    else:
      data[0]['LOAI_PHONG'] = 'deluxe'
    return jsonify(
        chuHo=data[0]['CHU_HO'],
        idTaiKhoan=data[0]['ID_TAI_KHOAN'],
        soPhong=data[0]['SO_PHONG'],
        loaiPhong=data[0]['LOAI_PHONG'],
    )
  else:
    response = jsonify({"error": "ID Hộ không tồn tại!"})
    response.status_code = 404  # Set the status code to indicate not found
    return response


'''
Nhan khau 
'''


@app.route('/api/NK/history')
def NK_history():
  try:
    if 'id' in session:
      if session['admin']:
        data_nk = show(['lich_su_nhan_khau'], ['*'])
        for x in data_nk:
          x['NGAY_SINH'] = x['NGAY_SINH'].isoformat()
        return render_template('main_NK_history.html',
                               user={
                                   'user': 'admin',
                                   'USER': 'NK',
                                   'data': data_nk,
                               })  # update for admin
      else:
        list_hogd = show(['ho_gd'], ['id_ho'],
                         conditions=[('id_tai_khoan', f'$ = {session["id"]}')])
        data_nk = None
        if len(list_hogd) != 0:
          data_nk = show(
              ['lich_su_nhan_khau'], ['*'],
              conditions=[
                  ('id_ho',
                   f'$ in ({",".join([str(x["id_ho"]) for x in list_hogd])})')
              ])
        return render_template('main_NK_history.html',
                               user={
                                   'user': 'user',
                                   'USER': 'NK',
                                   'data': data_nk
                               })  # update for user
  except:
    pass
  return redirect('/login')  # if something wrong: redirect to login


@app.route('/api/NK')
def NK():
  try:
    if 'id' in session:
      if session['admin']:
        data_nk = show(['nhan_khau'], ['*'])
        for x in data_nk:
          x['NGAY_SINH'] = x['NGAY_SINH'].isoformat()
        return render_template('main_nhankhau.html',
                               user={
                                   'user': 'admin',
                                   'USER': 'NK',
                                   'data': data_nk,
                               })  # update for admin
      else:
        list_hogd = show(['ho_gd'], ['id_ho'],
                         conditions=[('id_tai_khoan', f'$ = {session["id"]}')])
        data_nk = None
        if len(list_hogd) != 0:
          data_nk = show(
              ['nhan_khau'], ['*'],
              conditions=[
                  ('id_ho',
                   f'$ in ({",".join([str(x["id_ho"]) for x in list_hogd])})')
              ])

        return render_template('main_nhankhau.html',
                               user={
                                   'user': 'user',
                                   'USER': 'NK',
                                   'data': data_nk
                               })  # update for user
  except:
    pass
  return redirect('/login')  # if something wrong: redirect to login


@app.route('/api/NK/add')
def NK_add():
  stt = show(['lich_su_nhan_khau'],
             special_column_name=[(['stt'], "max({})", "max_stt")],
             column_name=[None])
  print(stt)
  return render_template('form_nhankhau.html',
                         nhankhau={
                             'title':
                             'Thêm Nhân Khẩu',
                             'func':
                             'add',
                             'form_name':
                             'Resident Form',
                             'stt': (stt[0]['max_stt'] +
                                     1) if stt[0]['max_stt'] else 1,
                         })


@app.route('/api/NK/update')
def NK_update():
  stt = show(['lich_su_nhan_khau'],
             special_column_name=[(['stt'], "max({})", "max_stt")],
             column_name=[None])
  print(stt)
  return render_template('form_nhankhau.html',
                         nhankhau={
                             'title':
                             'Thay đổi Nhân Khẩu',
                             'func':
                             'update',
                             'form_name':
                             'Resident Form',
                             'stt': (stt[0]['max_stt'] +
                                     1) if stt[0]['max_stt'] else 1,
                         })


@app.route('/api/NK/delete')
def NK_delete():
  return render_template('form_delete.html',
                         format={
                             'title': 'Xóa Nhân Khẩu',
                             'class': 'api/NK',
                             'name': 'CCCD',
                             'label': 'CCCD'
                         })


@app.route('/api/NK/<func>/apply', methods=['post'])
def NK_apply(func):
  data = request.form

  if func == "add":
    # insert nhan khau
    data = request.form
    print(data)
    values = [data.get(key) for key in data]
    values = [
        1 if item == 'Yes' else 0 if item == 'No' else item for item in values
    ]
    values.append("Add")
    values_without_history = values.copy()
    values_without_history.pop()  # remove type
    values_without_history.pop()  # remove date
    values_without_history.remove(values_without_history[0])  # remove stt
    id_ho = show(['ho_gd'], ['id_ho'],
                 [('ID_HO', f'$ = {values_without_history[-1]}')])
    print(id_ho)
    if len(id_ho) != 1:
      return render_template('error.html')
    #   values.append('test')
    try:
      create('nhan_khau', [tuple(values_without_history)])
      create('lich_su_nhan_khau', [tuple(values)])
    except:
      return render_template('error.html')
    # commit()
    return render_template('submit_confirmation.html', form=values)

  elif func == "update":
    data = request.form
    print(data)
    id = data.get('CCCD')
    data = {k: v for k, v in data.items()}
    data["LOAI_SUA_DOI"] = "Update"
    if data['TINH_TRANG_CU_TRU'] == 'Yes':
      data['TINH_TRANG_CU_TRU'] = 1
    else:
      data['TINH_TRANG_CU_TRU'] = 0
    values = [data.get(key) for key in data]
    data_without_history = data.copy()
    del data_without_history['NGAY_SUA_DOI']
    del data_without_history['LOAI_SUA_DOI']
    del data_without_history['stt']
    del data_without_history['CCCD']
    find_cccd = show(['nhan_khau'], ['*'], [('cccd', f'$ = {id}')])
    id_ho = show(['ho_gd'], ['id_ho'], [('ID_HO', f'$ = {data["ID_HO"]}')])
    print(values)
    print(data_without_history)
    try:
      if len(find_cccd) == 1 and len(id_ho) == 1:
        modify('nhan_khau',
               position=data_without_history.keys(),
               value=data_without_history.values(),
               index=id,
               primary_key="CCCD")
        create('lich_su_nhan_khau', [tuple(values)])
        # commit()
        return render_template('submit_confirmation.html')
      else:
        return render_template('error.html')
    except:
      return render_template('error.html')

  elif func == "delete":
    id = data.get('CCCD')
    time = data.get('NGAY_THAY_DOI')
    print(id)
    find_people = show(['nhan_khau'], ['*'], [('cccd', f'$ = {id}')])
    if len(find_people) == 1:
      stt = show(['lich_su_nhan_khau'],
                 special_column_name=[(['stt'], "max({})", "max_stt")],
                 column_name=[None])
      delete('nhan_khau', conditions=[(id, "CCCD = $")])
      values = [(stt[0]['max_stt'] + 1) if stt[0]['max_stt'] else 1,
                find_people[0]['CCCD'], find_people[0]['HO_TEN'],
                find_people[0]['NGAY_SINH'], find_people[0]['QUAN_HE'],
                find_people[0]['TINH_TRANG_CU_TRU'], find_people[0]['ID_HO'],
                time, "Delete"]
      create('lich_su_nhan_khau', [tuple(values)])
      # commit()
      return render_template('submit_confirmation.html')
    else:
      return render_template("error.html")

  else:
    return render_template("error.html")


@app.route('/api/getFormCCCD')
def get_form_CCCD():
  cccd = request.args.get('cccd')
  data = show(['nhan_khau'], ['*'], [('CCCD', f'$ = {cccd}')])
  print(data)
  if len(data) == 1:
    if data[0]['TINH_TRANG_CU_TRU'] == 0:
      data[0]['TINH_TRANG_CU_TRU'] = 'No'
    else:
      data[0]['TINH_TRANG_CU_TRU'] = 'Yes'
    data[0]['NGAY_SINH'] = data[0]['NGAY_SINH'].isoformat()
    print(data)
    return jsonify(hoTen=data[0]['HO_TEN'],
                   ngaySinh=data[0]['NGAY_SINH'],
                   quanHe=data[0]['QUAN_HE'],
                   tinhTrangCuTru=data[0]['TINH_TRANG_CU_TRU'],
                   idHo=data[0]['ID_HO'])
  else:
    response = jsonify({"error": "ID Hộ không tồn tại!"})
    response.status_code = 404  # Set the status code to indicate not found
    return response


'''
Thu chi
'''


@app.route('/api/TC/history')
def TC_history():
  return redirect('/api/TC')


@app.route('/api/TC')
def TC():
  # try:
  if 'id' in session:
    if session['admin']:
      data_tc = show(['thu_chi'], ['*'])
      print(data_tc)
      return render_template('main_thuchi.html',
                             user={
                                 'user': 'admin',
                                 'USER': 'TC',
                                 'data': data_tc
                             })  # update for admin
    else:
      list_hogd = show(['ho_gd'], ['id_ho'],
                       conditions=[('id_tai_khoan', f'$ = {session["id"]}')])
      data_tc = None
      if len(list_hogd) != 0:
        data_tc = show(
            ['thu_chi'], ['*'],
            conditions=[
                ('ID_HO',
                 f'$ = {",".join([str(x["id_ho"]) for x in list_hogd])}')
            ])
      return render_template('main_thuchi.html',
                             user={
                                 'user': 'user',
                                 'USER': 'TC',
                                 'data': data_tc
                             })  # update for user
  # except:
  #   pass
  return redirect('/login')  # if something wrong: redirect to login


@app.route('/api/TC/add')
def TC_add():
  stt = show(['thu_chi'],
             special_column_name=[(['stt'], "max({})", "max_stt")],
             column_name=[None])
  print(stt)
  return render_template('form_thuchi.html',
                         thuchi={
                             'title': 'Thêm Khoản Thu',
                             'func': 'add',
                             'form_name': 'Payment Form',
                             'stt': (stt[0]['max_stt'] +1) if stt[0]['max_stt'] else 1,
                         })


@app.route('/api/TC/update')
def TC_update():
  stt = show(['thu_chi'],
             special_column_name=[(['stt'], "max({})", "max_stt")],
             column_name=[None])
  print(stt)
  return render_template('form_thuchi.html',
                         thuchi={
                             'title': 'Thay đổi Khoản Thu',
                             'func': 'update',
                             'form_name': 'Payment Form',
                             'stt': (stt[0]['max_stt'] +1) if stt[0]['max_stt'] else 1,
                         })


@app.route('/api/TC/delete')
def TC_delete():
  return render_template('form_delete.html',
                         format={
                             'title': 'Xóa Khoản Thu',
                             'class': 'api/TC',
                             'name': 'STT',
                             'label': 'STT'
                         })


@app.route('/api/TC/<func>/apply', methods=['post'])
def TC_apply(func):
  data = request.form

  if func == "add":
    # insert nhan khau
    data = request.form
    print(data)
    values = [data.get(key) for key in data]
    values.remove(values[2])  # remove name of fee
    #   values.append('test')
    print(values)
    try:
      create('thu_chi', [tuple(values)])
    except:
      return render_template('error.html')
    # commit()
    return render_template('submit_confirmation.html', form=values)

  elif func == "update":
    data = request.form
    print(data)
    id = data.get('STT')
    data = {
        k: v
        for k, v in data.items() if (k != 'STT' and k != 'TEN_DICH_VU')
    }
    print(data)
    find_stt = show(['thu_chi'], ['*'], [('stt', f'$ = {id}')])
    if len(find_stt) == 1:
      modify('thu_chi',
             position=data.keys(),
             value=data.values(),
             index=id,
             primary_key="STT")
      # commit()
      return render_template('submit_confirmation.html')
    else:
      return render_template('error.html')

  elif func == "delete":
    id = data.get('STT')
    print(id)
    find_account = show(['thu_chi'], ['*'], [('STT', f'$ = {id}')])
    if len(find_account) == 1:
      delete('thu_chi', conditions=[(id, "STT = $")])
      # commit()
      return render_template('submit_confirmation.html')
    else:
      return render_template("error.html")

  else:
    return render_template("error.html")


@app.route('/api/getPrice')
def get_price():
  id_dich_vu = request.args.get('idDichVu')
  id_ho = request.args.get('idHo')
  print(id_dich_vu)
  # data = show(['dich_vu', 'thu_chi'], ['don_gia', 'ten_dich_vu'],
  #             [('ID_DICH_VU', f'$ = {id_dich_vu}')],
  #             special_column_name=[(['so_luong',
  #                                    'gia_tien'], "{} * {}", "total")])
  data = show(['dich_vu'], ['don_gia', 'ten_dich_vu'],
              [('ID_DICH_VU', f'$ = {id_dich_vu}')])
  max_stt = show(table_name=["thu_chi"],
                 special_column_name=[(['stt'], "max({})", "max_stt")],
                 column_name=[None])
  check_id_ho = show(['ho_gd'], ['id_ho'], [('ID_HO', f'$ = {id_ho}')])
  print(data)
  print(max_stt)
  if len(data) == 1 and len(check_id_ho) == 1:
    # return jsonify(price=data[0]['total'], name=data[0]['ten_dich_vu'])
    return jsonify(price=data[0]['don_gia'],
                   name=data[0]['ten_dich_vu'],
                   stt=max_stt[0]['max_stt'] + 1)
  else:
    response = jsonify({"error": "Dịch vụ hoặc Hộ gia đình không tồn tại!"})
    response.status_code = 404  # Set the status code to indicate not found
    return response


@app.route('/api/getFormSTT')
def get_form_stt():
  stt = request.args.get('stt')
  data = show(['thu_chi'], ['*'], [('stt', f'$ = {stt}')])
  print(data)
  if len(data) == 1:
    ten_dich_vu = show(['dich_vu'], ['ten_dich_vu'],
                       [('ID_DICH_VU', f'$ = {data[0]["ID_DICH_VU"]}')])
    print(ten_dich_vu)
    return jsonify(giaTien=data[0]['GIA_TIEN'],
                   tenDichVu=ten_dich_vu[0]['ten_dich_vu'],
                   idDichVu=data[0]['ID_DICH_VU'],
                   idHo=data[0]['ID_HO'],
                   soLuong=data[0]['SO_LUONG'],
                   daThu=data[0]['DA_THU'])
  else:
    response = jsonify({"error": "STT không tồn tại!"})
    response.status_code = 404  # Set the status code to indicate not found
    return response


'''
Dich Vu
'''


@app.route('/api/DV/history')
def DV():
  try:
    if 'id' in session:
      if session['admin']:
        data_dv = show(['lich_su_dich_vu'], ['*'])
        print(data_dv)
        return render_template('main_DV_history.html',
                               user={
                                   'user': 'admin',
                                   'USER': 'DV',
                                   'data': data_dv
                               })  # update for admin
      else:
        data_dv = show(['lich_su_dich_vu'], ['*'])
        return render_template('main_DV_history.html',
                               user={
                                   'user': 'user',
                                   'USER': 'DV',
                                   'data': data_dv
                               })  # update for user
  except:
    pass
  return redirect('/login')  # if something wrong: redirect to login


@app.route('/api/DV')
def DV_history():
  try:
    if 'id' in session:
      if session['admin']:
        data_dv = show(['dich_vu'], ['*'])
        print(data_dv)
        return render_template('main_dichvu.html',
                               user={
                                   'user': 'admin',
                                   'USER': 'DV',
                                   'data': data_dv
                               })  # update for admin
      else:
        data_dv = show(['dich_vu'], ['*'])
        return render_template('main_dichvu.html',
                               user={
                                   'user': 'user',
                                   'USER': 'DV',
                                   'data': data_dv
                               })  # update for user
  except:
    pass
  return redirect('/login')  # if something wrong: redirect to login


@app.route('/api/DV/add')
def DV_add():
  stt = show(['lich_su_dich_vu'],
             special_column_name=[(['stt'], "max({})", "max_stt")],
             column_name=[None])
  print(stt)
  id_dich_vu = show(['dich_vu'],
                    special_column_name=[(['ID_DICH_VU'], "max({})",
                                          "max_iddv")],
                    column_name=[None])
  print(id_dich_vu)
  return render_template(
      'form_dichvu.html',
      dichvu={
          'title':
          'Thêm Dịch Vụ',
          'func':
          'add',
          'form_name':
          'Service Form',
          'stt': (stt[0]['max_stt'] + 1) if stt[0]['max_stt'] else 1,
          'idDichVu':
          (id_dich_vu[0]['max_iddv'] + 1) if id_dich_vu[0]['max_iddv'] else 1,
      })


@app.route('/api/DV/update')
def DV_update():
  stt = show(['lich_su_dich_vu'],
             special_column_name=[(['stt'], "max({})", "max_stt")],
             column_name=[None])
  print(stt)
  return render_template('form_dichvu.html',
                         dichvu={
                             'title':
                             'Thay đổi Dịch Vụ',
                             'func':
                             'update',
                             'form_name':
                             'Service Form',
                             'stt': (stt[0]['max_stt'] +
                                     1) if stt[0]['max_stt'] else 1,
                         })


@app.route('/api/DV/delete')
def DV_delete():
  return render_template('form_delete.html',
                         format={
                             'title': 'Xóa Dịch Vụ',
                             'class': 'api/DV',
                             'name': 'ID_DICH_VU',
                             'label': 'ID_DICH_VU'
                         })


@app.route('/api/DV/<func>/apply', methods=['post'])
def DV_apply(func):
  data = request.form

  if func == "add":
    # insert nhan khau
    data = request.form
    print(data)
    values = [data.get(key) for key in data]
    values = [
        0 if item == 'tuNguyen' else 1 if item == 'batBuoc' else item
        for item in values
    ]
    values.append("Add")
    values_without_history = values.copy()
    values_without_history.pop()  # remove type
    values_without_history.pop()  # remove date
    values_without_history.remove(values_without_history[0])  # remove stt
    #   values.append('test')
    print(values)
    print(values_without_history)
    try:
      create('dich_vu', [tuple(values_without_history)])
      create('lich_su_dich_vu', [tuple(values)])
    except:
      return render_template('error.html')
    # commit()
    return render_template('submit_confirmation.html', form=values)

  elif func == "update":
    data = request.form
    id = data.get('ID_DICH_VU')
    data = {k: v for k, v in data.items()}
    data["LOAI_SUA_DOI"] = "Update"
    if data['BAT_BUOC'] == 'batBuoc':
      data['BAT_BUOC'] = 1
    else:
      data['BAT_BUOC'] = 0
    data_without_history = data.copy()
    del data_without_history['NGAY_SUA_DOI']
    del data_without_history['LOAI_SUA_DOI']
    del data_without_history['stt']
    del data_without_history['ID_DICH_VU']
    values = [data.get(key) for key in data]
    print(data)
    print(data_without_history)
    find_dich_vu = show(['dich_vu'], ['*'], [('ID_DICH_VU', f'$ = {id}')])
    try:
      if len(find_dich_vu) == 1:
        modify('dich_vu',
               position=data_without_history.keys(),
               value=data_without_history.values(),
               index=id,
               primary_key="ID_DICH_VU")
        create('lich_su_dich_vu', [tuple(values)])
        # commit()
        return render_template('submit_confirmation.html')
      else:
        return render_template('error.html')
    except:
      return render_template('error.html')

  elif func == "delete":
    id = data.get('ID_DICH_VU')
    time = data.get('NGAY_THAY_DOI')
    print(id)
    find_service = show(['dich_vu'], ['*'], [('ID_DICH_VU', f'$ = {id}')])
    if len(find_service) == 1:
      stt = show(['lich_su_dich_vu'],
                 special_column_name=[(['stt'], "max({})", "max_stt")],
                 column_name=[None])
      delete('dich_vu', conditions=[(id, "ID_DICH_VU = $")])
      values = [(stt[0]['max_stt'] + 1) if stt[0]['max_stt'] else 1,
                find_service[0]['ID_DICH_VU'], find_service[0]['TEN_DICH_VU'],
                find_service[0]['don_gia'], find_service[0]['BAT_BUOC'], time,
                "Delete"]
      create('lich_su_dich_vu', [tuple(values)])
      # commit()
      return render_template('submit_confirmation.html')
    else:
      return render_template("error.html")

  else:
    return render_template("error.html")


@app.route('/api/getFormID_DICH_VU')
def get_form_id_dich_vu():
  id_dv = request.args.get('idDichVu')
  data = show(['dich_vu'], ['*'], [('ID_DICH_VU', f'$ = {id_dv}')])
  print(data)
  if len(data) == 1:
    if data[0]['BAT_BUOC'] == 0:
      data[0]['BAT_BUOC'] = 'tuNguyen'
    else:
      data[0]['BAT_BUOC'] = 'batBuoc'
    print(data)
    return jsonify(tenDichVu=data[0]['TEN_DICH_VU'],
                   donGia=data[0]['don_gia'],
                   batBuoc=data[0]['BAT_BUOC'])
  else:
    response = jsonify({"error": "ID dịch vụ không tồn tại!"})
    response.status_code = 404  # Set the status code to indicate not found
    return response


'''
Report
'''


@app.route('/api/RP/history')
def RP_history():
  return redirect('/api/RP')


@app.route('/api/RP')
def RP():
  try:
    if 'id' in session:
      if session['admin']:
        data_rp = show(['report'], ['*'])
        print(data_rp)
        return render_template('main_report.html',
                               user={
                                   'user': 'admin',
                                   'USER': 'RP',
                                   'data': data_rp
                               })  # update for admin
      else:
        data_rp = show(['report'], ['*'],
                       conditions=[('ID_TAI_KHOAN', f'$ = {session["id"]}')])
        return render_template('main_report.html',
                               user={
                                   'user': 'user',
                                   'USER': 'RP',
                                   'data': data_rp
                               })  # update for user
  except:
    pass
  return redirect('/login')  # if something wrong: redirect to login


@app.route('/api/RP/add')
def RP_add():
  stt = show(['report'],
             special_column_name=[(['stt'], "max({})", "max_stt")],
             column_name=[None])
  print(stt)
  return render_template('form_report.html',
                         report={
                             'title':
                             'Thêm Report',
                             'func':
                             'add',
                             'form_name':
                             'Report Form',
                             'stt': (stt[0]['max_stt'] +
                                     1) if stt[0]['max_stt'] else 1,
                         })


@app.route('/api/RP/update')
def RP_update():
  return render_template('form_report.html',
                         report={
                             'title': 'Thêm Report',
                             'func': 'update',
                             'form_name': 'Report Form',
                             'stt': " ",
                         })


@app.route('/api/RP/delete')
def RP_delete():
  return render_template('form_delete.html',
                         format={
                             'title': 'Xóa Report',
                             'class': 'api/RP',
                             'name': 'STT',
                             'label': 'STT'
                         })


@app.route('/api/RP/<func>/apply', methods=['post'])
def RP_apply(func):
  data = request.form
  if func == "add":
    values = [data.get(key) for key in data]
    values.insert(1, session['id'])
    print(values)
    # try:
    create('report', [tuple(values)])
    # commit()
    return render_template('submit_confirmation.html')
    # except:
    #   return render_template('error.html')

  elif func == "update":
    id = data.get('STT')
    data = {k: v for k, v in data.items() if k != 'STT'}
    data["ID_TAI_KHOAN"] = session['id']
    print(data)
    find_stt = show(['report'], ['STT'], [('STT', f'$ = {id}')])
    if len(find_stt) == 1:
      modify('report',
             position=data.keys(),
             value=data.values(),
             index=id,
             primary_key="STT")
      # commit()
      return render_template('submit_confirmation.html')
    else:
      return render_template('error.html')

  elif func == "delete":
    id = data.get('STT')
    print(id)
    find_stt = show(['report'], ['STT','ID_TAI_KHOAN'], [('STT', f'$ = {id}')])
    if len(find_stt) == 1 and (find_stt[0]['id_tai_khoan']==session['id'] or session['admin']):
      delete('report', conditions=[(id, "STT = $")])
      # commit()
      return render_template('submit_confirmation.html')
    else:
      return render_template("error.html")

  else:
    return render_template('error.html')


@app.route('/api/getFormREPORT')
def get_form_report():
  stt = request.args.get('stt')
  data = show(['report'], ['NOI_DUNG','ID_TAI_KHOAN'], [('STT', f'$ = {stt}')])
  print(data)
  if data[0]['id_tai_khoan'] != session['id'] or not session['admin']:
    response = jsonify({"error": "Không có quyền truy nhập"})
    response.status_code = 404  # Set the status code to indicate not found
    return response
  print(data)
  if len(data) == 1:
    return jsonify(noiDung=data[0]['noi_dung'])
  else:
    response = jsonify({"error": "STT không tồn tại!"})
    response.status_code = 404  # Set the status code to indicate not found
    return response


# test
@app.route("/api/NK/enhanced_mode", methods=["POST", "GET"])
def execute_changeNK():
  data = json.loads(request.data)
  print(data)
  for x in data['delete']:
    delete("nhan_khau", [('cccd', f'$ = {x["cccd"]}')])
  for x in data['modify']:
    modify("nhan_khau", x.keys(), x.values(), "cccd", x['cccd'])
  return "Xu li thanh cong"


@app.route("/api/HK/enhanced_mode", methods=["POST", "GET"])
def execute_changeHK():
  data = json.loads(request.data)
  print(data)
  for x in data['delete']:
    delete("ho_gd", [('id_ho', f'$ = {x["id_ho"]}')])
  for x in data['modify']:
    modify("ho_gd", x.keys(), x.values(), "id_ho", x['id_ho'])
  return "Xu li thanh cong"


@app.route("/api/TC/enhanced_mode", methods=["POST", "GET"])
def execute_changeTC():
  data = json.loads(request.data)
  print(data)
  for x in data['delete']:
    delete("thu_chi", [('stt', f'$ = {x["stt"]}')])
  for x in data['modify']:
    modify("thu_chi", x.keys(), x.values(), "stt", x['stt'])
  return "Xu li thanh cong"


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
