import click, sys, csv, json
from tabulate import tabulate
from models import*
from sqlalchemy.exc import IntegrityError
from app import app


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()
  
  print("initialize started")

  with open('data.json') as file:
    data = json.load(file)
    total_entries = len(data)
    i = 0
    batch1 = []
    batch2 = []
    
    for row in data:
      i = i+1
      
      temp = row['Line Of Business']
      properLOB = ""

      if "LEVEL" in temp:
        index = temp.index("LEVEL")
        properLOB = temp[:index]
      else:
        properLOB = temp

      new_entry = Database(row['Supplier Name'], properLOB)
      batch1.append(new_entry)

      duplicate = False
      
      if batch2:
        for supplier in batch2:
          if supplier.name == row['Supplier Name']:
            duplicate = True
            break 
      
      if duplicate == False:
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
        batch2.append(new_entry2)
          
      progress = (i/total_entries) * 100
      print(f"phase 1 progress: {progress:.0f}%")
    
    if batch1:
      db.session.bulk_save_objects(batch1)
    
    if batch2:
      db.session.bulk_save_objects(batch2)
      

  print("phase 1 completed")
  
  with open('lines-data.json') as file:
    data = json.load(file)
    total_entries = len(data)
    i = 0
    batch = []
    
    for row in data:
      i = i+1
      entry = LineOfBusiness(n=row['LOB name'], c=row['code'], l=row['Level'])
      batch.append(entry)
      
      progress = (i/total_entries) * 100
      print(f"phase 2 progress: {progress:.0f}%")
      
    if batch:
      db.session.bulk_save_objects(batch)
    
    print("phase 2 completed")

  with open('LineLayers_Entries.json') as file:
    data = json.load(file)
    total_entries = len(data)
    i = 0
    batch1 = []
    batch2 = []
    batch3 = []
    batch4 = []
    batch5 = []
    lineOfBusinessList = LineOfBusiness.query.all()
    
    for row in data:
      
      i = i+1      

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
      
      reg = False
      
      for val in lineOfBusinessList:
        if val.code == layer4code:
          reg = True
          break

      registered = "Yes" if reg else "No"
        
      duplicate = False
      
      if batch1:
        for layer in batch1:
          if layer.code == layer1code:
            duplicate = True
            break
          
      if not duplicate:
        new_entry = Layer1(name=layer1, code=layer1code)
        batch1.append(new_entry)

      duplicate = False
      
      if batch2:
        for layer in batch2:
          if layer.code == layer2code:
            duplicate = True
            break

      if not duplicate:
        new_entry = Layer2(outerCode=layer1code, name=layer2, code=layer2code)
        batch2.append(new_entry)
      
      duplicate = False
      
      if batch3:
        for layer in batch3:
          if layer.code == layer3code:
            duplicate = True
            break
      
      if not duplicate:
        new_entry = Layer3(outerCode=layer2code, name=layer3, code=layer3code)
        batch3.append(new_entry)
      
      duplicate = False
      
      if batch4:
        for layer in batch4:
          if layer.code == layer4code:
            duplicate = True
            break
      
      if not duplicate:
        new_entry = Layer4(outerCode=layer3code,
                          name=layer4,
                          code=layer4code,
                          registered=registered)
        batch4.append(new_entry)

      entry = LineLayers(layer1, layer1code, layer2, layer2code, layer3,
                        layer3code, layer4, layer4code, registered)
      batch5.append(entry)
      
      progress = (i / total_entries) * 100
      print(f"phase 3 Progress: {progress:.0f}%")
      
    if batch1:
      db.session.bulk_save_objects(batch1)
    
    if batch2:
      db.session.bulk_save_objects(batch2)
      
    if batch3:
      db.session.bulk_save_objects(batch3)
      
    if batch4:
      db.session.bulk_save_objects(batch4)
      
    if batch5:
      db.session.bulk_save_objects(batch5)

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
