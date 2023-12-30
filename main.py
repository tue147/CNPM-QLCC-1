from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from backend import *
import random

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


@app.route('/admin')
def admin():
  data_hk = show(
      ['tai_khoan'],
      ['*'],
  )
  #print(data_hk)
  return render_template('admin.html',
                         user={
                             'user': 'admin',
                             'USER': 'ADMIN',
                             'data': data_hk
                         })


@app.route('/user')
def user():
  return render_template('user.html', user={'user': 'user', 'USER': 'USER'})


'''
Ho Khau
'''


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
  return render_template('form_hokhau.html',
                         hokhau={
                             'title': 'Thêm Hộ Khẩu',
                             'func': 'add',
                             'form_name': 'Household Form'
                         })


@app.route('/api/HK/update')
def HK_update():
  return render_template('form_hokhau.html',
                         hokhau={
                             'title': 'Thay đổi Hộ Khẩu',
                             'func': 'update',
                             'form_name': 'Household Form'
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
    print((values))
    # values.append('test')
    try:
      create('ho_gd', [tuple(values)])
    except:
      return render_template('error.html')
    # commit()
    return render_template('submit_confirmation.html')

  elif func == "update":
    data = request.form
    print(data)
    id = data.get('ID_HO')
    data = {k: v for k, v in data.items() if k != 'ID_HO'}
    if data['LOAI_PHONG'] == 'standard':
      data['LOAI_PHONG'] = 0
    else:
      data['LOAI_PHONG'] = 1
    find_hogd = show(['ho_gd'], ['*'], [('ID_HO', f'$ = {id}')])
    if len(find_hogd) == 1:
      modify('ho_gd',
             position=data.keys(),
             value=data.values(),
             index=id,
             primary_key="ID_HO")
      # commit()
      return render_template('submit_confirmation.html')
    else:
      return render_template('error.html')

  elif func == "delete":
    id = data.get('ID Hộ')
    print(id)
    find_account = show(['ho_gd'], ['*'], [('id_ho', f'$ = {id}')])
    if len(find_account) == 1:
      delete('ho_gd', conditions=[(id, "ID_HO = %")])
      # commit()
      return render_template('submit_confirmation.html')
    else:
      return render_template("error.html")

  else:
    return render_template("error.html")


'''
Nhan khau 
'''


@app.route('/api/NK')
def NK():
  try:
    if 'id' in session:
      if session['admin']:
        data_nk = show(['nhan_khau'], ['*'])
        return render_template('main_nhankhau.html',
                               user={
                                   'user': 'admin',
                                   'USER': 'NK',
                                   'data': data_nk,
                               })  # update for admin
      else:
        list_hogd = show(['ho_gd'], ['id_ho'],
                         conditions=[('id_tai_khoan', f'$ = {session["id"]}')])
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
  return render_template('form_nhankhau.html',
                         nhankhau={
                             'title': 'Thêm Nhân Khẩu',
                             'func': 'add',
                             'form_name': 'Resident Form'
                         })


@app.route('/api/NK/update')
def NK_update():
  return render_template('form_nhankhau.html',
                         nhankhau={
                             'title': 'Thay đổi Nhân Khẩu',
                             'func': 'update',
                             'form_name': 'Resident Form'
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
    #   values.append('test')
    try:
      create('nhan_khau', [tuple(values)])
    except:
      return render_template('error.html')
    # commit()
    return render_template('submit_confirmation.html', form=values)

  elif func == "update":
    data = request.form
    print(data)
    id = data.get('CCCD')
    data = {k: v for k, v in data.items() if k != 'CCCD'}
    find_cccd = show(['nhan_khau'], ['*'], [('cccd', f'$ = {id}')])
    if len(find_cccd) == 1:
      modify('nhan_khau',
             position=data.keys(),
             value=data.values(),
             index=id,
             primary_key="CCCD")
      # commit()
      return render_template('submit_confirmation.html')
    else:
      return render_template('error.html')

  elif func == "delete":
    id = data.get('CCCD')
    print(id)
    find_account = show(['nhan_khau'], ['*'], [('cccd', f'$ = {id}')])
    if len(find_account) == 1:
      delete('nhan_khau', conditions=[(id, "CCCD = $")])
      # commit()
      return render_template('submit_confirmation.html')
    else:
      return render_template("error.html")
  else:
    return render_template("error.html")


'''
Thu chi
'''


@app.route('/api/TC')
def TC():
  try:
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
        data_tc = show(['thu_chi'], ['*'],
                       conditions=[('id_tai_khoan', f'$ = {session["id"]}')])
        return render_template('main_thuchi.html',
                               user={
                                   'user': 'user',
                                   'USER': 'TC',
                                   'data': data_tc
                               })  # update for user
  except:
    pass
  return redirect('/login')  # if something wrong: redirect to login


@app.route('/api/TC/add')
def TC_add():
  return render_template('form_thuchi.html',
                         thuchi={
                             'title': 'Thêm Khoản Thu',
                             'func': 'add',
                             'form_name': 'Payment Form'
                         })


@app.route('/api/TC/update')
def TC_update():
  return render_template('form_thuchi.html',
                         thuchi={
                             'title': 'Thay đổi Khoản Thu',
                             'func': 'update',
                             'form_name': 'Payment Form'
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
    values.remove(values[2])   # remove name of fee
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
    data = {k: v for k, v in data.items() if (k != 'STT' and k!='TEN_DICH_VU')}
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
  print(id_dich_vu)
  data = show(['dich_vu'], ['don_gia', 'ten_dich_vu'], [('ID_DICH_VU', f'$ = {id_dich_vu}')])
  print(data)
  if len(data) == 1:
    return jsonify(price=data[0]['don_gia'], name = data[0]['ten_dich_vu'])
  else:
    response = jsonify({"error": "Dịch vụ không tồn tại!"})
    response.status_code = 404  # Set the status code to indicate not found
    return response


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
