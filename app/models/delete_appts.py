import db_queries
import db_modify

'''
appts = db_queries.get_appointments({"booked": True})
for appt in appts:
    print(appt.get_tutor_netid())
    print(appt.get_time())
    db_modify.cancel_appointment(appt.get_time(), appt.get_tutor_netid())
    print("canceled\n")
'''

'''
appts = db_queries.get_appointments()
for appt in appts:
    if appt.get_tutor_netid() not in ['hgranger', 'llvgd', 'pweasley', 'habbott','cchang', 'ppatil']:
        continue
    print(appt.get_tutor_netid())
    print(appt.get_time())
    db_modify.delete_appointment(appt.get_time(), appt.get_tutor_netid())
    print("deleted\n")
'''

for user in ['hgranger', 'llvgd', 'pweasley', 'habbott','cchang', 'ppatil']:
    db_modify.delete_tutor(user)