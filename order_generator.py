# order generator 需要每分钟往每个station里放一个drone的单子和一个robot的单子
# 单子里需要order ID
# destination address (可以用scheduling folder里面的adresses Excel，里面有1000随机出来的真实的SF地址)
# order weight（随机给，如果是drone给0.1-5.0， robot给0.1-10.0）
# order cost （如果是drone就用4.0+0.4*3*weight，如果是robot就用2.0+0.2*3*weight）
# trackingID
# carrier type
# 以及appointment time（cur time+30 min）

import pandas as pd
import random
from uuid import uuid1
import  datetime
import db_connection as db
import numpy as np

def order_generator(minutes):
    pd_read(minutes)

orders = pd.DataFrame()
contact = pd.DataFrame()
users = pd.DataFrame()
machine = pd.DataFrame()
station = pd.DataFrame()
tracking = pd.DataFrame()

def pd_read(rows):
    filename = "1000 real addresses_San Francisco - Sheet1.csv"
    n = sum(1 for line in open(filename)) - 1 #number of records in file (excludes header)
    s = rows #desired sample size
    skip = sorted(random.sample(range(1,n+1),n-s)) #the 0-indexed header will not be included in the skip list
    df = pd.read_csv(filename, skiprows=skip)

    # table orders
    orders['order_id'] = df.index.to_series().map(lambda x: str(uuid1().int))
    orders['user_id'] = df.index.to_series().map(lambda x: 'user' + str(x))
    orders['tracking_id'] = df.index.to_series().map(lambda x: str(uuid1().hex))
    station_id = []
    for i in range(0, rows):
        if i < rows / 3:
            station_id.append(1)
        elif i < rows / 3 * 2:
            station_id.append(2)
        else:
            station_id.append(3)
    orders['station_id'] = df.index.to_series().map(lambda x: station_id[x])
    orders['machine_id'] = df.index.to_series().map(lambda x: None)
    orders['active'] = df.index.to_series().map(lambda x: True)
    sender_id = []
    recipient_id = []
    for i in range(1, rows + 1):
        sender_id.append(2 * i - 1)
        recipient_id.append(2 * i)
    orders['sender_id'] = df.index.to_series().map(lambda x: sender_id[x])
    orders['recipient_id'] = df.index.to_series().map(lambda x: recipient_id[x])
    carrier = []
    package_weight = []
    total_cost = []
    for i in range(0, rows):
        if i % 2 == 0:
            carrier.append('drone')
            package_weight.append(round(random.uniform(0.1, 5.0), 1))
            total_cost.append(round(4.0 + 0.4 * 3 * package_weight[i], 1))
        else:
            carrier.append('robot')
            package_weight.append(round(random.uniform(0.1, 10.0), 1))
            total_cost.append(round(2.0 + 0.2 * 3 * package_weight[i], 1))
    orders['package_weight'] = df.index.to_series().map(lambda x: package_weight[x])
    orders['package_height'] = df.index.to_series().map(lambda x: 3.5)
    orders['package_fragile'] = df.index.to_series().map(lambda x: False)
    orders['package_length'] = df.index.to_series().map(lambda x: 3.1)
    orders['package_width'] = df.index.to_series().map(lambda x: 3.1)
    orders['carrier'] = df.index.to_series().map(lambda x: carrier[x])
    # orders['delivery_time'] = df.index.to_series().map(lambda x: 1.5)
    orders['total_cost'] = df.index.to_series().map(lambda x: total_cost[x])
    appointment_time = []
    now = datetime.datetime.now()
    minute = datetime.timedelta(days=0, seconds=60, microseconds=0)
    for i in range(0, rows):
        appointment_time.append(now.strftime("%Y-%m-%d %H:%M:%S"))
        now += minute
    orders['appointment_time'] = df.index.to_series().map(lambda x: appointment_time[x])

    # table contact
    contact['contact_id'] = pd.concat([orders['sender_id'], orders['recipient_id']]).sort_values(ascending = True).reset_index(drop=True)
    contact['first_name'] = contact.index.to_series().map(lambda x: 'firstname{}'.format(x))
    contact['last_name'] = contact.index.to_series().map(lambda x: 'lastname{}'.format(x))
    contact['phone_number'] = contact.index.to_series().map(lambda x: '1234567890')
    contact['email_address'] = contact.index.to_series().map(lambda x: 'user{}@gmail.com'.format(x))
    address = [None] * (rows * 2)
    for i in range(0, 2 * rows):
        if i % 2 != 0:
            address[i] = str(df['NUMBER'][(i - 1) / 2]) + ' ' + df['STREET'][(i - 1) / 2] + ', San Francisco, CA, USA' + ' ' + str(df['POSTCODE'][(i - 1) / 2])
    contact['address'] = contact.index.to_series().map(lambda x: address[x])

    # table users
    users['user_id'] = orders['user_id']
    password = []
    first_name = []
    last_name = []
    email_address = []
    phone_number = []
    address = []
    for i in range(0, len(users['user_id'])):
        password.append('{}'.format(i))
        first_name.append('firstxxx{}'.format(i))
        last_name.append('lastxxx{}'.format(i))
        first_name.append('firstxxx{}'.format(i))
        email_address.append('emailxxx{}@gmail.com'.format(i))
        phone_number.append('xxxxxxxxxx')
        address.append('addressxxx{}'.format(i))
    users['password'] = users.index.to_series().map(lambda x: password[x])
    users['first_name'] = users.index.to_series().map(lambda x: first_name[x])
    users['last_name'] = users.index.to_series().map(lambda x: last_name[x])
    users['email_address'] = users.index.to_series().map(lambda x: email_address[x])
    users['phone_number'] = users.index.to_series().map(lambda x: phone_number[x])
    users['address'] = users.index.to_series().map(lambda x: address[x])

    # machine
    machine_id = []
    station_id = []
    machine_type = []
    height_limit = []
    weight_limit = []
    unit_price_per_mile = []
    for i in range(0, 60):
        machine_id.append(i)
        if i < 20:
            station_id.append(1)
            if i < 10:
                machine_type.append('drone')
                height_limit.append(13.0)
                weight_limit.append(5.0)
                unit_price_per_mile.append(0.4)
            else:
                machine_type.append('robot')
                height_limit.append(25.0)
                weight_limit.append(20.0)
                unit_price_per_mile.append(0.2)
        elif i < 40:
            station_id.append(2)
            if i < 30:
                machine_type.append('drone')
                height_limit.append(13.0)
                weight_limit.append(5.0)
                unit_price_per_mile.append(0.4)
            else:
                machine_type.append('robot')
                height_limit.append(25.0)
                weight_limit.append(20.0)
                unit_price_per_mile.append(0.2)
        else:
            station_id.append(3)
            if i < 50:
                machine_type.append('drone')
                height_limit.append(13.0)
                weight_limit.append(5.0)
                unit_price_per_mile.append(0.4)
            else:
                machine_type.append('robot')
                height_limit.append(25.0)
                weight_limit.append(20.0)
                unit_price_per_mile.append(0.2)
    machine['machine_id'] = pd.Series(np.array(machine_id))
    machine['station_id'] = machine.index.to_series().map(lambda x: station_id[x])
    machine['machine_type'] = machine.index.to_series().map(lambda x: machine_type[x])
    machine['available'] = machine.index.to_series().map(lambda x: True)
    machine['height_limit'] = machine.index.to_series().map(lambda x: height_limit[x])
    machine['weight_limit'] = machine.index.to_series().map(lambda x: weight_limit[x])
    machine['unit_price_per_mile_per_kg'] = machine.index.to_series().map(lambda x: unit_price_per_mile[x])

    # table station
    station['station_id'] = pd.Series(np.array([1,2,3]))
    station['drone_num'] = pd.Series(np.array([10,10,10]))
    station['robot_num'] = pd.Series(np.array([10,10,10]))
    station['address'] = pd.Series(np.array(['Parkside, San Francisco, CA, USA','Mission District, San Francisco, CA, USA','Excelsior, San Francisco, CA, USA']))
    station['lon'] = pd.Series(np.array([-122.494880,-122.4147977,-122.4272295]))
    station['lat'] = pd.Series(np.array([37.749690,37.7598648,37.7244152]))

    # table tracking
    tracking['tracking_id'] = orders['tracking_id']
    tracking['status'] = tracking.index.to_series().map(lambda x: 'ordered')
    tracking['created_at'] = orders['appointment_time']
    tracking['estimated_delivered_at'] = tracking.index.to_series().map(lambda x: 'xxx')
    tracking['delay'] = tracking.index.to_series().map(lambda x: False)
    tracking['previous_destination'] = tracking.index.to_series().map(lambda x: 'xxx')
    tracking['previous_destination_start_time'] = tracking.index.to_series().map(lambda x: 'xxx')

order_generator(240)

with pd.ExcelWriter('dispatch_db.xlsx') as writer:
    users.to_excel(writer, sheet_name='users')
    tracking.to_excel(writer, sheet_name='tracking')
    station.to_excel(writer, sheet_name='station')
    machine.to_excel(writer, sheet_name='machine')
    contact.to_excel(writer, sheet_name='contact')
    orders.to_excel(writer, sheet_name='orders')

# db.csv_insert_tables(contact, 'Insert into contact (contact_id, first_name, last_name, phone_number, email_address, address)')
# db.csv_insert_tables(machine, 'Insert into machine (machine_id, station_id, machine_type, available, height_limit, weight_limit, unit_price_per_mile_per_kg)')
# db.csv_insert_tables(station, 'Insert into station (station_id, drone_num, robot_num, address, lon, lat)')
# db.csv_insert_tables(tracking, 'Insert into tracking (tracking_id, status, created_at, estimated_delivered_at, delay, previous_destination, previous_destination_start_time)')
# db.csv_insert_tables(users, 'Insert into users (user_id, password, first_name, last_name, email_address, phone_number, address)')
# db.csv_insert_tables(orders, 'Insert into orders (order_id, user_id, tracking_id, station_id, machine_id, active, sender_id, recipient_id, package_weight, package_height, package_fragile, package_length, package_width, carrier, delivery_time, total_cost, appointment_time)')

print('done!')

# now = datetime.datetime.now()
# print(now.strftime("%Y-%m-%d %H:%M:%S"))
# minute = datetime.timedelta(days=0, seconds=60, microseconds=0)
# print((now + minute).strftime("%Y-%m-%d %H:%M:%S"))