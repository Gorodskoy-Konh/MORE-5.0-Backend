import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base import Base
from models.office import OfficeDB
from models.product import ProductDB
from models.terminal_product import TerminalProductDB
from models.working_hours import WeekDays, WorkingHoursDB
from models.terminal import TerminalDB
from datetime import time
import sqlalchemy
import psycopg2


engine = create_engine("postgresql+psycopg2://postgres:1111@localhost/sqlalchemy_tuts")
engine.connect()
# Create a database connection and session
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Fill products table
products_individuals = ['Кредит', 'Ипотека', 'Вклады и счета', 'Другие услуги']
products_legals = ['Открыть счет', 'Регистрация бизнеса', 'Оформить кредит для бизнеса']

for product_name in products_individuals:
    product = ProductDB(name=product_name)
    session.add(product)

for product_name in products_legals:
    product = ProductDB(name=product_name)
    session.add(product)

# Commit the changes to the database
session.commit()

# Fill offices table
json_string = open('offices.json').read()

offices = json.loads(json_string)
for office in offices:
    officeDB = OfficeDB(
        address = office['address'],
        has_ramp = True if 'y' in office['hasRamp'].lower() else False,
        kep = office['kep'],
        latitude = float(office['latitude']),
        longitude = float(office['longitude']),
        name = office['salePointName'],
        office_type = True if 'да' in office['officeType'].lower() else False,
        rko = True if 'есть' in office['rko'].lower() else False,
        sale_point_format = office['salePointFormat'],
        suo_availability = True if 'y' in office['suoAvailability'].lower() else False,
    )
    session.add(officeDB)
    session.flush()
    inserted_id = officeDB.id

    # Parsing of working hours
    for day in office['openHoursIndividuals']:
        if day['hours'].lower() == 'выходной':
            continue
        weekDays = WeekDays.monday
        if day['days'].lower() == 'вт':
            weekDays = WeekDays.tuesday
        elif day['days'].lower() == 'ср':
            weekDays = WeekDays.wednesday
        elif day['days'].lower() == 'чт':
            weekDays = WeekDays.thursday
        elif day['days'].lower() == 'пт':
            weekDays = WeekDays.friday
        elif day['days'].lower() == 'сб':
            weekDays = WeekDays.saturday
        else:
            weekDays = WeekDays.sunday
        begin = time(hour=int(day['hours'].split('-')[0].split(':')[0]), minute=int(day['hours'].split('-')[0].split(':')[1]))
        end = time(hour=int(day['hours'].split('-')[1].split(':')[0]), minute=int(day['hours'].split('-')[1].split(':')[1]))
        WorkingHoursDB(
            begin=begin,
            end=end,
            office_id=inserted_id,
            individual=True,
            week_day=weekDays
        )
    for day in office['openHours']:
        if day['hours'].lower() == 'выходной':
            continue
        weekDays = WeekDays.monday
        if day['days'].lower() == 'вт':
            weekDays = WeekDays.tuesday
        elif day['days'].lower() == 'ср':
            weekDays = WeekDays.wednesday
        elif day['days'].lower() == 'чт':
            weekDays = WeekDays.thursday
        elif day['days'].lower() == 'пт':
            weekDays = WeekDays.friday
        elif day['days'].lower() == 'сб':
            weekDays = WeekDays.saturday
        else:
            weekDays = WeekDays.sunday
        begin = time(hour=int(day['hours'].split('-')[0].split(':')[0]), minute=int(day['hours'].split('-')[0].split(':')[1]))
        end = time(hour=int(day['hours'].split('-')[1].split(':')[0]), minute=int(day['hours'].split('-')[1].split(':')[1]))
        WorkingHoursDB(
            begin=begin,
            end=end,
            office_id=inserted_id,
            individual=False,
            week_day=weekDays
        )

    terminal_ids = []
    # Creation of terminal with specific product types and their insetion to office
    for i in range(len(products_individuals) -1):# + len(products_legals) - 1):
        terminal = TerminalDB(office_id = inserted_id)
        session.add(terminal)
        session.flush()
        terminal_ids.append(terminal.id)
        terminal_product_1 = TerminalProductDB(
            terminal_id = terminal.id,
            product_name = products_individuals[i],
            individual = True,
            legals = False
        )
        terminal_product_2 = TerminalProductDB(
            terminal_id = terminal.id,
            product_name = products_individuals[i + 1],
            individual = True,
            legals = False
        )
        session.add(terminal_product_1)
        session.add(terminal_product_2)
    for i in range(len(products_legals) -1):
        terminal = TerminalDB(office_id = inserted_id)
        session.add(terminal)
        session.flush()
        terminal_ids.append(terminal.id)
        terminal_product_1 = TerminalProductDB(
            terminal_id = terminal.id,
            product_name = products_legals[i],
            individual = False,
            legals = True
        )
        terminal_product_2 = TerminalProductDB(
            terminal_id = terminal.id,
            product_name = products_legals[i + 1],
            individual = False,
            legals = True
        )
        session.add(terminal_product_1)
        session.add(terminal_product_2)
    
    

# Commit the changes to the database
session.commit()

