from collections import namedtuple
from datetime import datetime
from typing import List
from splitwise import Splitwise
from database import Database


Debtor = namedtuple('Debtor', 'id username email debt_amount date')

def get_debtors(split_obj:Splitwise) -> List[Debtor]:

    debtors = []
    date = datetime.today().strftime('%Y-%m-%d')

    for friend in split_obj.getFriends():
        if friend.getBalances():
            debt_amount = float(friend.getBalances()[0].getAmount())
            if debt_amount > 0:
                debtors.append(Debtor(friend.getId(), friend.getFirstName(), friend.getEmail(), debt_amount, date))

    return debtors
        
def update_debt(db_name, table_name, data):
    with Database(db_name) as database:
        database.cursor.execute(f'UPDATE {table_name} SET debt_amount = ? WHERE id = ?;', data)

def get_debtors_by_amount(db_name, amount):
    debtors = []
    with Database(db_name) as database:
        database.cursor.execute('''SELECT
            id,
            username,
            email,
            debt_amount,
            debt_incurred_from
        FROM debtors
        WHERE debt_amount > ?''', (amount,))

        for id, username, email, debt_amount, debt_incurred_from in database.cursor.fetchall():
            debtors.append(Debtor(id, username, email, debt_amount, debt_incurred_from))

    return debtors