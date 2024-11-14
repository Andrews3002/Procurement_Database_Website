import click, sys, csv, json
from tabulate import tabulate
from models import*
from sqlalchemy.exc import IntegrityError
from app import app


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()

  with open('data.json') as file:
    data = json.load(file)
    for row in data:
      temp = row['Line Of Business']
      properLOB = ""

      if "LEVEL" in temp:
        index = temp.index("LEVEL")
        properLOB = temp[:index]
      else:
        properLOB = temp

      new_entry = Database(row['Supplier Name'], properLOB)

      suppliers = Company.query.filter_by(name=row['Supplier Name']).first()
      if not suppliers:
        new_entry2 = Company(
            name=row.get('Supplier Name', None)
            if row.get('Supplier Name') else None,
            status=row.get('Status', None) if row.get('Status') else None,
            score=row.get('Score', None) if row.get('Score') else None,
            supplierNumber=row.get('Supplier Number', None)
            if row.get('Supplier Number') else None,
            services=row.get('Services', None)
            if row.get('Services') else None,
            buildingName=row.get('BuildingNm', None)
            if row.get('BuildingNm') else None,
            street1Address=row.get('Street1Addr', None)
            if row.get('Street1Addr') else None,
            street2Address=row.get('Street2Addr', None)
            if row.get('Street2Addr') else None,
            street3Address=row.get('Street3Addr', None)
            if row.get('Street3Addr') else None,
            cityName=row.get('CityNm', None) if row.get('CityNm') else None,
            supplierType=row.get('SupplierTypeCd', None)
            if row.get('SupplierTypeCd') else None,
            employeesQuantity=row.get('EmployeesQty', None)
            if row.get('EmployeesQty') else None,
            natureOfBusinessOrService=row.get('NatureOfBusinessOrServicesTxt',
                                              None)
            if row.get('NatureOfBusinessOrServicesTxt') else None,
            firmLegalName=row.get('FirmLegalNm', None)
            if row.get('FirmLegalNm') else None,
            operatedUnderOtherBusiness=row.get(
                'Operated_Under_Other_Business_', None)
            if row.get('Operated_Under_Other_Business_') else None,
            otherBusinessName=row.get('OtherBusinessNm', None)
            if row.get('OtherBusinessNm') else None,
            subsidiaryAffiliateFirm=row.get('Subsidiary_Affiliate_Firm_', None)
            if row.get('Subsidiary_Affiliate_Firm_') else None,
            affiliatesName=row.get('AffiliatesNm', None)
            if row.get('AffiliatesNm') else None,
            legalQuery=row.get('Legal_Query_', None)
            if row.get('Legal_Query_') else None,
            legalQueryDetails=row.get('LegalQueryDetailsTxt', None)
            if row.get('LegalQueryDetailsTxt') else None,
            incorporationOrRegistrationYear=row.get('IncorporationYr', None)
            if row.get('IncorporationYr') else None,
            incorporationOrRegistrationCountry=row.get(
                'IncorporationCountryCd', None)
            if row.get('IncorporationCountryCd') else None,
            websiteAddress=row.get('CompanyWebsiteUrl', None)
            if row.get('CompanyWebsiteUrl') else None,
            municipality=row.get('GeographicLocationCd', None)
            if row.get('GeographicLocationCd') else None,
            country=row.get('CountryCd', None)
            if row.get('CountryCd') else None,
            postalCode=row.get('PostalCd', None)
            if row.get('PostalCd') else None,
            telephone=row.get('TelephoneNum', None)
            if row.get('TelephoneNum') else None,
            addressType=row.get('AddressTypeTp', None)
            if row.get('AddressTypeTp') else None,
            createdBy=row.get('CreBy', None) if row.get('CreBy') else None,
            createdTimestamp=row.get('CreDttm')
            if row.get('CreDttm') else None,
            fav = "0")
        db.session.add(new_entry2)
      db.session.add(new_entry)

  with open('lines-data.json') as file:
    data = json.load(file)
    for row in data:
      entry = LineOfBusiness(n=row['LOB name'], c=row['code'], l=row['Level'])
      db.session.add(entry)

  with open('LineLayers_Entries.json') as file:
    data = json.load(file)
    for row in data:

      line = row['L1'].strip()
      index = line.index(" - ")
      layer1 = (line[index:]).strip(" - ")
      layer1code = line[:index]

      line = row['L2'].strip()
      index = line.index(" - ")
      layer2 = (line[index:]).strip(" - ")
      layer2code = line[:index]

      line = row['L3'].strip()
      index = line.index(" - ")
      layer3 = (line[index:]).strip(" - ")
      layer3code = line[:index]

      line = row['L4']
      index = line.index(" - ")
      layer4 = (line[index:]).strip(" - ")
      layer4code = line[:index]

      reg = LineOfBusiness.query.filter(
          LineOfBusiness.code.ilike(f"%{layer4code}%")).first()

      registered = "Yes" if reg else "No"

      val = Layer1.query.filter(Layer1.code.ilike(f"%{layer1code}%")).first()

      if not val:
        new_entry = Layer1(name=layer1, code=layer1code)
        db.session.add(new_entry)

      val = Layer2.query.filter(Layer2.code.ilike(f"%{layer2code}%")).first()

      if not val:
        new_entry = Layer2(outerCode=layer1code, name=layer2, code=layer2code)
        db.session.add(new_entry)

      val = Layer3.query.filter(Layer3.code.ilike(f"%{layer3code}%")).first()

      if not val:
        new_entry = Layer3(outerCode=layer2code, name=layer3, code=layer3code)
        db.session.add(new_entry)

      val = Layer4.query.filter(Layer4.code.ilike(f"%{layer4code}%")).first()

      if not val:
        new_entry = Layer4(outerCode=layer3code,
                           name=layer4,
                           code=layer4code,
                           registered=registered)
        db.session.add(new_entry)

      entry = LineLayers(layer1, layer1code, layer2, layer2code, layer3,
                         layer3code, layer4, layer4code, registered)
      db.session.add(entry)
      print(layer1code)

  db.session.commit()
  print('database intialized')


@app.cli.command("get-user", help="Retrieves a User by username or id")
@click.argument('key', default='bob')
def get_user(key):
  bob = User.query.filter_by(username=key).first()
  if not bob:
    bob = User.query.get(int(key))
    if not bob:
      print(f'{key} not found!')
      return
  print(bob)


@app.cli.command("change-email")
@click.argument('username', default='bob')
@click.argument('email', default='bob@mail.com')
def change_email(username, email):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found!')
    return
  bob.email = email
  db.session.add(bob)
  db.session.commit()
  print(bob)


@app.cli.command('get-users')
def get_users():
  users = User.query.all()
  print(users)


@app.cli.command('create-user')
@click.argument('username', default='rick')
@click.argument('email', default='rick@mail.com')
@click.argument('password', default='rickpass')
def create_user(username, email, password):
  newuser = User(username, email, password)
  try:
    db.session.add(newuser)
    db.session.commit()
  except IntegrityError as e:
    db.session.rollback()
    print(e.orig)
    print("Username or email already taken!")
  else:
    print(newuser)


@app.cli.command('delete-user')
@click.argument('username', default='bob')
def delete_user(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found!')
    return
  db.session.delete(bob)
  db.session.commit()
  print(f'{username} deleted')


@app.cli.command('data')
def get_database():
  line = Company.query.filter_by(name="GEOEX MCG ").first()
  print(line)
