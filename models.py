from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from fuzzywuzzy import process

db = SQLAlchemy()


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  type = db.Column(db.String(50))
  __mapper_args__ = {'polymorphic_identity': 'user', 'polymorphic_on': type}

  def search_cp(self, q, page):
    results = None

    if q == "":
      results = Company.query
    else:
      results = Company.query.filter(
          db.or_(Company.name.ilike(f"%{q}%"), Company.services.like(f"%{q}%"),
                 Company.status.ilike(f"%{q}%")))

    return results.paginate(page=page, per_page=20)

  def search_fav(self, q, page):
    results = None

    if q == "":
      results = Company.query.filter(Company.fav == "1")
    else:
      results = Company.query.filter(Company.fav == "1", db.or_(Company.name.ilike(f"%{q}%"),
      Company.services.like(f"%{q}%"),                  
      Company.status.ilike(f"%{q}%")))

    return results.paginate(page=page, per_page=20)
      

  def search_lob(self, q, page):
    results = None
    if q == "":
      results = LineOfBusiness.query
    else:
      results = LineOfBusiness.query.filter(
          db.or_(LineOfBusiness.name.ilike(f"%{q}%"),
                 LineOfBusiness.code.ilike(f"%{q}%"),
                 LineOfBusiness.level.ilike(f"%{q}%")))

    return results.paginate(page=page, per_page=20)

  def search_LL1(self, q, page):
    results = None
    if q == "":
      results = Layer1.query
    else:
      results = Layer1.query.filter(
          db.or_(Layer1.name.ilike(f"%{q}%"),
                 Layer1.code.ilike(f"%{q}%")))

    return results.paginate(page=page, per_page=20)

  def search_LL2(self, q, page, outerCode):
    results = None
    if q == "":
      results = Layer2.query.filter(Layer2.outerCode.ilike(f"%{outerCode}%"))
    else:
      results = Layer2.query.filter(
          db.or_(Layer2.name.ilike(f"%{q}%"),
                 Layer2.code.ilike(f"%{q}%"),
                 Layer2.outerCode.ilike(f"%{outerCode}%")))

    return results.paginate(page=page, per_page=20)

  def search_LL3(self, q, page, outerCode):
    results = None
    if q == "":
      results = Layer3.query.filter(Layer3.outerCode.ilike(f"%{outerCode}%"))
    else:
      results = Layer3.query.filter(
          db.or_(Layer3.name.ilike(f"%{q}%"),
                 Layer3.code.ilike(f"%{q}%"),
                 Layer3.outerCode.ilike(f"%{outerCode}%")))

    return results.paginate(page=page, per_page=20)

  def search_LL4(self, q, page, lineCode):
    results = None
    if q == "":
      results = Layer4.query.filter(Layer4.outerCode.ilike(f"%{lineCode}%"))
    else:
      results = Layer4.query.filter(
          db.or_(Layer4.name.ilike(f"%{q}%"),
                 Layer4.code.ilike(f"%{q}%"),
                 Layer4.outerCode.ilike(f"%{lineCode}%")))

    return results.paginate(page=page, per_page=20)

  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.set_password(password)

  def set_password(self, password):
    """Create hashed password."""
    self.password = generate_password_hash(password, method='scrypt')

  def check_password(self, password):
    """Check hashed password."""
    return check_password_hash(self.password, password)

  def __repr__(self):
    return f'<User {self.id} {self.username} - {self.email}>'

  def get_json(self):
    return {
        "id": self.id,
        "username": self.username,
        "email": self.email,
        "type": self.type
    }


class Database(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  supplierName = db.Column(db.String(1000), nullable=False)
  lineOfBusiness = db.Column(db.String(1000), nullable=False)

  def __init__(self, supplierName, lineOfBusiness):
    self.supplierName = supplierName
    self.lineOfBusiness = lineOfBusiness

  def get_json(self):
    return {
        "id": self.id,
        "supplierName": self.supplierName,
        "lineOfBusiness": self.lineOfBusiness
    }


class Company(db.Model):
  name = db.Column(db.String(1000), nullable=False, primary_key=True)
  status = db.Column(db.String(1000))
  score = db.Column(db.String(1000))
  supplierNumber = db.Column(db.String(1000))
  services = db.Column(db.String(10000))
  buildingName = db.Column(db.String(1000))
  street1Address = db.Column(db.String(1000))
  street2Address = db.Column(db.String(1000))
  street3Address = db.Column(db.String(1000))
  cityName = db.Column(db.String(1000))
  supplierType = db.Column(db.String(1000))
  employeesQuantity = db.Column(db.String(1000))
  natureOfBusinessOrService = db.Column(db.String(1000))
  firmLegalName = db.Column(db.String(1000))
  operatedUnderOtherBusiness = db.Column(db.String(1000))
  otherBusinessName = db.Column(db.String(1000))
  subsidiaryAffiliateFirm = db.Column(db.String(1000))
  affiliatesName = db.Column(db.String(1000))
  legalQuery = db.Column(db.String(1000))
  legalQueryDetails = db.Column(db.String(1000))
  incorporationOrRegistrationYear = db.Column(db.String(1000))
  incorporationOrRegistrationCountry = db.Column(db.String(1000))
  websiteAddress = db.Column(db.String(1000))
  municipality = db.Column(db.String(1000))
  country = db.Column(db.String(1000))
  postalCode = db.Column(db.String(1000))
  telephone = db.Column(db.String(1000))
  addressType = db.Column(db.String(1000))
  createdBy = db.Column(db.String(1000))
  createdTimestamp = db.Column(db.String(1000))
  fav = db.Column(db.String(1000))

  def __init__(self, name, status, score, supplierNumber, services,
               buildingName, street1Address, street2Address, street3Address,
               cityName, supplierType, employeesQuantity,
               natureOfBusinessOrService, firmLegalName,
               operatedUnderOtherBusiness, otherBusinessName,
               subsidiaryAffiliateFirm, affiliatesName, legalQuery,
               legalQueryDetails, incorporationOrRegistrationYear,
               incorporationOrRegistrationCountry, websiteAddress,
               municipality, country, postalCode, telephone, addressType,
               createdBy, createdTimestamp, fav):
    self.name = name
    self.status = status
    self.score = score
    self.supplierNumber = supplierNumber
    self.services = services
    self.buildingName = buildingName
    self.street1Address = street1Address
    self.street2Address = street2Address
    self.street3Address = street3Address
    self.cityName = cityName
    self.supplierType = supplierType
    self.employeesQuantity = employeesQuantity
    self.natureOfBusinessOrService = natureOfBusinessOrService
    self.firmLegalName = firmLegalName
    self.operatedUnderOtherBusiness = operatedUnderOtherBusiness
    self.otherBusinessName = otherBusinessName
    self.subsidiaryAffiliateFirm = subsidiaryAffiliateFirm
    self.affiliatesName = affiliatesName
    self.legalQuery = legalQuery
    self.legalQueryDetails = legalQueryDetails
    self.incorporationOrRegistrationYear = incorporationOrRegistrationYear
    self.incorporationOrRegistrationCountry = incorporationOrRegistrationCountry
    self.websiteAddress = websiteAddress
    self.municipality = municipality
    self.country = country
    self.postalCode = postalCode
    self.telephone = telephone
    self.addressType = addressType
    self.createdBy = createdBy
    self.createdTimestamp = createdTimestamp
    self.fav = fav

  def get_json(self):
    return {
        "name": self.name,
        "status": self.status,
        "score": self.score,
        "supplierNumber": self.supplierNumber,
        "services": self.services,
        "buildingName": self.buildingName,
        "street1Address": self.street1Address,
        "street2Address": self.street2Address,
        "street3Address": self.street3Address,
        "cityName": self.cityName,
        "supplierType": self.supplierType,
        "employeesQuantity": self.employeesQuantity,
        "natureOfBusinessOrService": self.natureOfBusinessOrService,
        "firmLegalName": self.firmLegalName,
        "operatedUnderOtherBusiness": self.operatedUnderOtherBusiness,
        "otherBusinessName": self.otherBusinessName,
        "subsidiaryAffiliateFirm": self.subsidiaryAffiliateFirm,
        "affiliatesName": self.affiliatesName,
        "legalQuery": self.legalQuery,
        "legalQueryDetails": self.legalQueryDetails,
        "incorporationOrRegistrationYear":
        self.incorporationOrRegistrationYear,
        "incorporationOrRegistrationCountry":
        self.incorporationOrRegistrationCountry,
        "websiteAddress": self.websiteAddress,
        "municipality": self.municipality,
        "country": self.country,
        "postalCode": self.postalCode,
        "telephone": self.telephone,
        "addressType": self.addressType,
        "createdBy": self.createdBy,
        "createdTimestamp": self.createdTimestamp,
        "fav": self.fav
    }


class LineOfBusiness(db.Model):
  name = db.Column(db.String(1000))
  code = db.Column(db.String(1000), primary_key=True)
  level = db.Column(db.String(1000))

  def __init__(self, n, c, l):
    self.name = n
    self.code = c
    self.level = l

  def get_json(self):
    return {"name": self.name, "code": self.code, "level": self.level}

class LineLayers(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  l1 = db.Column(db.String(1000))
  l2 = db.Column(db.String(1000))
  l3 = db.Column(db.String(1000))
  l4 = db.Column(db.String(1000))
  l1code = db.Column(db.String(1000))
  l2code = db.Column(db.String(1000))
  l3code = db.Column(db.String(1000))
  l4code = db.Column(db.String(1000))
  registered = db.Column(db.String(1000))

  def __init__(self, l1, l1code, l2, l2code, l3, l3code, l4, l4code, registered):
    self.l1 = l1
    self.l2 = l2
    self.l3 = l3
    self.l4 = l4
    self.l1code = l1code
    self.l2code = l2code
    self.l3code = l3code
    self.l4code = l4code
    self.registered = registered

  def get_json(self):
    return {"l1": self.l1, "l2": self.l2, "l3": self.l3, "l4": self.l4, "l1code": self.l1code, "l2code": self.l2code, "l3code": self.l3code, "l4code": self.l4code}

class Layer1(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(1000))
  code = db.Column(db.String(1000))

  def __init__(self, name, code):
    self.name = name
    self.code = code

  def get_json(self):  
    return {"name": self.name, "code": self.code}

class Layer2(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  outerCode = db.Column(db.String(1000))
  name = db.Column(db.String(1000))
  code = db.Column(db.String(1000))

  def __init__(self, outerCode, name, code):
    self.name = name
    self.code = code
    self.outerCode = outerCode

  def get_json(self):  
    return {"name": self.name, "code": self.code}

class Layer3(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  outerCode = db.Column(db.String(1000))
  name = db.Column(db.String(1000))
  code = db.Column(db.String(1000))

  def __init__(self, outerCode, name, code):
    self.name = name
    self.code = code
    self.outerCode = outerCode

  def get_json(self):  
    return {"name": self.name, "code": self.code}

class Layer4(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  outerCode = db.Column(db.String(1000))
  name = db.Column(db.String(1000))
  code = db.Column(db.String(1000))
  registered = db.Column(db.String(1000))

  def __init__(self, outerCode, name, code, registered):
    self.name = name
    self.code = code
    self.registered = registered
    self.outerCode = outerCode

  def get_json(self):  
    return {"name": self.name, "code": self.code}
