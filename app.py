import os
import datetime
from flask import Flask, request, render_template, flash, jsonify, redirect, url_for
from functools import wraps
from models import*

from flask_jwt_extended import (JWTManager, create_access_token, 
get_jwt_identity, jwt_required, current_user, set_access_cookies,
unset_jwt_cookies, current_user,)


def create_app():
  app = Flask(__name__, static_url_path='/static')
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://procurement_database_user:cVt8TtmqhLyHz45HrdEt87dM4Ym5Dxlg@dpg-csqqf3qj1k6c73c165e0-a.oregon-postgres.render.com/procurement_database"
  app.config['PREFERRED_URL_SCHEME'] = 'https'
  app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
  app.config['JWT_REFRESH_COOKIE_NAME'] = 'refresh_token'
  app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=15)
  app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
  app.config["JWT_COOKIE_SECURE"] = True
  app.config["JWT_SECRET_KEY"] = "super-secret"
  app.config["JWT_COOKIE_CSRF_PROTECT"] = False
  
  db.init_app(app)
  app.app_context().push()
  return app


app = create_app()
jwt = JWTManager(app)


@jwt.user_identity_loader
def user_identity_lookup(user):
  return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
  identity = jwt_data["sub"]
  return User.query.get(identity)

@jwt.expired_token_loader
@jwt.invalid_token_loader
def custom_unauthorized_response(error):
    return render_template('401.html', error=error), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return render_template('401.html'), 401  

def login_required(required_class):
  def wrapper(f):
      @wraps(f)
      @jwt_required() 
      def decorated_function(*args, **kwargs):
        user = required_class.query.get(get_jwt_identity())
        if user.__class__ != required_class: 
            return jsonify(message='Invalid user role'), 403
        return f(*args, **kwargs)
      return decorated_function
  return wrapper

def login_user(username, password):
  user = User.query.filter_by(username=username).first()
  if user and user.check_password(password):
    token = create_access_token(identity=user)
    return token
  return None

# AUTHENTICATION GET ROUTES-------------------------------------------------------------------------------
@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET'])
def login_page():
  return render_template('login.html')

@app.route('/signup', methods=['GET'])
def signup_page():
  return render_template('signup.html')


@app.route('/logout', methods=['GET'])
@jwt_required()
def logout_action():
  flash('Logged Out')
  response = redirect(url_for('login_page'))
  unset_jwt_cookies(response)
  return response




# AUTHENTICATION ACTION ROUTES----------------------------------------------------------------------------
@app.route('/signup', methods=['POST'])
def signup_action():
  data = request.form  # get data from form submission
  newuser = User(username=data['username'], email=data['email'], password=data['password'])  # create user object
  response = None
  try:
    db.session.add(newuser)
    db.session.commit()  # save user
    token = login_user(data['username'], data['password'])
    response = redirect(url_for('home_page'))
    set_access_cookies(response, token)
    flash('Account Created!')  # send message
  except Exception:  # attempted to insert a duplicate user
    db.session.rollback()
    flash("username or email already exists")  # error message
    response = redirect(url_for('signup_page'))
  return response

@app.route('/login', methods=['POST'])
def login_action():
  data = request.form
  token = login_user(data['username'], data['password'])
  print(token)
  if token:
    response = redirect(url_for('home_page'))  
    set_access_cookies(response, token)
    flash(f'welcome {data["username"]}')
  else:
    flash('Invalid username or password')  
    response = redirect(url_for('login_page'))
  return response





# CENTRAL HUB OF WEBSITE----------------------------------------------------------------------------------
@app.route('/home', methods=['GET'])
@login_required(User)
def home_page():
  return render_template('home.html')



# REGISTERED COMPANIES EXPLORATION ROUTES-----------------------------------------------------------------
@app.route('/Companies')
@login_required(User)
def companies_page():
  page = request.args.get('page', 1, type=int)
  q = request.args.get('q', default='', type=str) 
  Companies = current_user.search_cp(q, page)
  return render_template('Companies.html', Companies=Companies, q=q, page=page)

@app.route('/Company/<string:compName>', methods=['GET'])
@jwt_required()
def company_page(compName):
  company = Company.query.filter(Company.name.like(f"%{compName}%")).first()
  return render_template('company.html', company=company)

@app.route('/company-lines/<string:compName>', methods=['GET'])
@jwt_required()
def company_lines_page(compName):
  lines = Database.query.filter(Database.supplierName.ilike(f"%{compName}%")).all()
  return render_template('company-lines.html', lines=lines, compName=compName)





# REGISTERED LINES OF BUSINESS EXPLORATION ROUTES---------------------------------------------------------
@app.route('/Linesofbusiness')
@login_required(User)
def linesofbusiness_page():
  page = request.args.get('page', 1, type=int)
  q = request.args.get('q', default='', type=str) 
  LinesOfBusiness = current_user.search_lob(q, page)
  return render_template('Linesofbusiness.html', LinesOfBusiness=LinesOfBusiness, q=q, page=page)

@app.route('/line-companies/<string:lineName>', methods=['GET'])
@jwt_required()
def line_companies_page(lineName):
  suppliers = Database.query.filter(Database.lineOfBusiness.ilike(f"%{lineName}%")).all()
  companies = []
  for sup in suppliers:
    companies.append(Company.query.filter(Company.name.ilike(f"%{sup.supplierName}%")).first())
  return render_template('line-companies.html', companies=companies, lineName=lineName)

@app.route('/line-companies/<string:placeHolder1>/<string:placeHolder2>/<string:lineName>', methods=['GET'])
@jwt_required()
def line_companies_page2(lineName, placeHolder1, placeHolder2):
  placeHolder1 = None
  placeHolder2 = None
  if lineName == " 4d seismic data interpretation":
    lineName = "2d / 3d/ 4d seismic data interpretation"
    suppliers = Database.query.filter_by(lineOfBusiness=lineName).all()
    companies = []
    for sup in suppliers:
      companies.append(Company.query.filter(Company.name.ilike(f"%{sup.supplierName}%")).first())
  elif lineName == " 4d land seismic acquisition services":
    lineName = "2d/ 3d/ 4d land seismic acquisition services"
    suppliers = Database.query.filter_by(lineOfBusiness=lineName).all()
    companies = []
    for sup in suppliers:
      companies.append(Company.query.filter(Company.name.ilike(f"%{sup.supplierName}%")).first())
  elif lineName == " 4d marine seismic acquisition services":
    lineName = "2d/ 3d/ 4d marine seismic acquisition services"
    suppliers = Database.query.filter_by(lineOfBusiness=lineName).all()
    companies = []
    for sup in suppliers:
      companies.append(Company.query.filter(Company.name.ilike(f"%{sup.supplierName}%")).first())
  else:
    lineName = "2d / 3d/ 4d seismic data interpretation"
    suppliers = Database.query.filter_by(lineOfBusiness=lineName).all()
    companies = []
    for sup in suppliers:
      companies.append(Company.query.filter(Company.name.ilike(f"%{sup.supplierName}%")).first())

  return render_template('line-companies.html', companies=companies, lineName=lineName)





#ALL LINES OF BUSINESS EXPLORATION ROUTES-----------------------------------------------------------------
@app.route('/layer1')
@login_required(User)
def layer1_page():
  page = request.args.get('page', 1, type=int)
  q = request.args.get('q', default='', type=str) 
  lines = current_user.search_LL1(q, page)
  return render_template('layer1.html', lines=lines, q=q, page=page)

@app.route('/layer1-companies/<string:lineCode>/<string:lineName>', methods=['GET'])
@jwt_required()
def layer1_companies_page(lineCode, lineName):
  data1 = LineLayers.query.filter(LineLayers.l1code.ilike(f"%{lineCode}%")).all()
  if not data1:
      return render_template('layer1-companies.html', suppliers=[], lineCode=lineCode, lineName=lineName)

  l4_values = [data.l4 for data in data1]

  data2 = Database.query.filter(Database.lineOfBusiness.in_(l4_values)).all()
  if not data2:
      return render_template('layer1-companies.html', suppliers=[], lineCode=lineCode, lineName=lineName)
    
  supplier_names = {data.supplierName for data in data2}
  suppliers = Company.query.filter(Company.name.in_(supplier_names)).all()
  return render_template('layer1-companies.html', suppliers=suppliers, lineCode=lineCode, lineName=lineName)

@app.route('/layer2/<string:outerCode>/<string:outerName>')
@login_required(User)
def layer2_page(outerCode, outerName):
  page = request.args.get('page', 1, type=int)
  q = request.args.get('q', default='', type=str) 
  lines = current_user.search_LL2(q, page, outerCode)
  return render_template('layer2.html', lines=lines, q=q, page=page, outerCode=outerCode, outerName=outerName)

@app.route('/layer2-companies/<string:lineCode>/<string:lineName>', methods=['GET'])
@jwt_required()
def layer2_companies_page(lineCode, lineName):
  data1 = LineLayers.query.filter(LineLayers.l2code.ilike(f"%{lineCode}%")).all()
  if not data1:
      return render_template('layer2-companies.html', suppliers=[], lineCode=lineCode, lineName=lineName)

  l4_values = [data.l4 for data in data1]

  data2 = Database.query.filter(Database.lineOfBusiness.in_(l4_values)).all()
  if not data2:
      return render_template('layer2-companies.html', suppliers=[], lineCode=lineCode, lineName=lineName)

  supplier_names = {data.supplierName for data in data2}
  suppliers = Company.query.filter(Company.name.in_(supplier_names)).all()
  return render_template('layer2-companies.html', suppliers=suppliers, lineCode=lineCode, lineName=lineName)

@app.route('/layer3/<string:outerCode>/<string:outerName>')
@login_required(User)
def layer3_page(outerCode, outerName):
  page = request.args.get('page', 1, type=int)
  q = request.args.get('q', default='', type=str) 
  lines = current_user.search_LL3(q, page, outerCode)
  return render_template('layer3.html', lines=lines, q=q, page=page, outerCode=outerCode, outerName=outerName)

@app.route('/layer3-companies/<string:lineCode>/<string:lineName>', methods=['GET'])
@jwt_required()
def layer3_companies_page(lineCode, lineName):
  data1 = LineLayers.query.filter(LineLayers.l3code.ilike(f"%{lineCode}%")).all()
  if not data1:
      return render_template('layer3-companies.html', suppliers=[], lineCode=lineCode, lineName=lineName)

  l4_values = [data.l4 for data in data1]

  data2 = Database.query.filter(Database.lineOfBusiness.in_(l4_values)).all()
  if not data2:
      return render_template('layer3-companies.html', suppliers=[], lineCode=lineCode, lineName=lineName)

  supplier_names = {data.supplierName for data in data2}
  suppliers = Company.query.filter(Company.name.in_(supplier_names)).all()
  return render_template('layer3-companies.html', suppliers=suppliers, lineCode=lineCode, lineName=lineName)

@app.route('/layer4/<string:outerCode>/<string:outerName>')
@login_required(User)
def layer4_page(outerCode, outerName):
  page = request.args.get('page', 1, type=int)
  q = request.args.get('q', default='', type=str) 
  lines = current_user.search_LL4(q, page, outerCode)
  return render_template('layer4.html', lines=lines, q=q, page=page, outerCode=outerCode, outerName=outerName)





# --------------------------------------------COMPANY FAVORITES-------------------------------------------
@app.route('/favorites-update/<string:compName>', methods=['POST'])
@login_required(User)
def add_favorite(compName):
  comp = Company.query.filter(Company.name.ilike(f"%{compName}%")).first()
  if not comp:
    flash(f'{compName} not found!')
    return redirect(request.referrer)
  value = request.form.get('mycheckbox')
  if not value:
    value = request.form.get('mybutton')
  comp.fav = value
  db.session.add(comp)
  db.session.commit()
  if comp.fav == "1":
    flash(f'{compName} added to frequent suplliers')
  else:
    flash(f'{compName} removed from frequent suppliers')
  return redirect(request.referrer)

@app.route('/remove-favorite/<string:compName>', methods=['POST'])
@login_required(User)
def remove_favorite(compName):
  comp = Company.query.filter(Company.name.ilike(f"%{compName}%")).first()
  if not comp:
    flash(f'{compName} not found!')
    return redirect(request.referrer)
  comp.fav = "0"
  db.session.add(comp)
  db.session.commit()
  flash(f'{compName} removed from frequent suppliers')
  return redirect(request.referrer)

@app.route('/favorites-page')
@login_required(User)
def favorites_page():
  page = request.args.get('page', 1, type=int)
  q = request.args.get('q', default='', type=str)
  Companies = current_user.search_fav(q, page)
  return render_template('Favorites.html', Companies=Companies, q=q, page=page)
  
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)




