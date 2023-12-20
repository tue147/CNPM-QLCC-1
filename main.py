from flask import Flask, render_template, request, redirect, url_for, session

from backend import *

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
    find_account = show(['tai_khoan'], ['*'], [('ten_dang_nhap', f'$ = "{username}"'),
                                    ('mat_khau', f'$ = "{password}"')])
    if len(find_account) != 1:
      print("failed")
      return render_template(
          'login.html',
          error={'error_code': 'Tài khoản hoặc mật khẩu không tồn tại'})
    else:
      print("success", find_account)
      # print(acc)
      session['id'] = find_account[0][0]
      session['admin'] = find_account[0][3]
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


@app.route('/admin')
def admin():
  return render_template('admin.html', user={'user':'admin'})

@app.route('/user')
def user():
  return render_template('user.html', user={'user':'user'})


'''
Ho Khau
'''


@app.route('/api/HK')
def HK():
  return render_template('main_hokhau.html')


@app.route('/api/HK/add')
def HK_add():
  return render_template('form_hokhau.html', hokhau={'title':'Thêm Hộ Khẩu', 'func':'add', 'form_name':'Household Form'})


@app.route('/api/HK/add/apply', methods=['post'])
def HK_add_apply():
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

@app.route('/api/HK/update')
def HK_update():
  return render_template('form_hokhau.html', hokhau={'title':'Thay đổi Hộ Khẩu', 'func':'update', 'form_name':'Household Form'})

@app.route('/api/HK/update/apply', methods=['post'])
def HK_update_apply():
  data = request.form
  print(data)
  # update hk
  
  # commit()
  return render_template('submit_confirmation.html')

@app.route('/api/HK/delete')
def HK_delete():
  return render_template('form_delete.html', format={'title':'Xóa Hộ Khẩu', 'class':'HK', 'name':'ID Hộ', 'label':'ID Hộ'})

@app.route('/api/HK/delete/apply', methods=['post'])
def HK_delete_apply():
  data = request.form
  id = data.get('ID Hộ')
  print(id)
  delete('ho_gd', conditions=[(id, "ID_HO = %")])
  # commit()
  return render_template('submit_confirmation.html')


@app.route('/api/HK/find/apply', methods=['post'])
def HK_find_apply():
  data = request.form
  # to be updated


'''
Nhan khau 
'''
@app.route('/api/NK')
def NK():
  return render_template('main_nhankhau.html')


@app.route('/api/NK/add')
def NK_add():
  return render_template('form_nhankhau.html', nhankhau={'title':'Thêm Nhân Khẩu', 'func':'add', 'form_name':'Resident Form'})


@app.route('/api/NK/add/apply', methods=['post'])
def NK_add_apply():
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


@app.route('/api/NK/update/apply', methods=['post'])
def NK_update_apply():
  data = request.form
  print(data)
  data = {k: v for k, v in data.items() if k != 'CCCD'}
  modify('nhan_khau',
         position=data.keys(),
         value=data.values(),
         index=id,
         primary_key="CCCD")
  # commit()
  return render_template('update_nhankhau_submitted.html')

@app.route('/api/NK/delete')
def NK_delete():
  return render_template('form_delete.html', format={'title':'Xóa Nhân Khẩu', 'class':'NK', 'name':'CCCD', 'label':'CCCD'})

@app.route('/api/NK/delete/apply', methods=['post'])
def NK_delete_apply():
  data = request.form
  id = data.get('CCCD')
  print(id)
  delete('nhan_khau', conditions=[(id, "CCCD = %")])
  # commit()
  return render_template('submit_confirmation.html')


@app.route('/api/NK/find/apply', methods=['post'])
def NK_find_apply():
  data = request.form
  # to be updated


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
