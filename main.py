import email
from string import Template
from splitwise import Splitwise
from config import (
    db_name,
    password,
    port,
    sender,
    smtp_server,
    ssl_enable,
    subject,
    username,
    consumer_key,
    consumer_secret,
    api_key
    )
from database import if_table_exist, if_user_exist, if_user_exist, setup, insert_data
from debtors import get_debtors, get_debtors_by_amount, update_debt
from emails import EmailSender, Credentials


def create_mail_content(debtor):
    template = Template('''Hej $name !!!
    Gdzie jest ka$$ka, ja się pytam?
    Oddawaj w podskokach.
    
    Pozdrawiam
    JW
    ''')

    text = template.substitute({
        'name': debtor.username
    })
    
    message = email.message_from_string(text)

    message.set_charset('utf-8')
    message['From'] = sender
    message['To'] = debtor.email
    message['Subject'] = subject
    
    return message.as_string()

if __name__ == '__main__':
    splitwise_obj = Splitwise(consumer_key, consumer_secret, api_key=api_key)
    credentials = Credentials(username, password)
    
    if not if_table_exist(db_name, 'debtors'):
        setup(db_name)
   
    debtors_from_api = get_debtors(splitwise_obj)
    debtors = get_debtors_by_amount(db_name, 0)

    repaids_ids = set([debt.id for debt in debtors]) - set([debt.id for debt in debtors_from_api])

    for debtor in debtors_from_api:
        if not if_user_exist(db_name, 'debtors', debtor.id):
            insert_data(db_name, 'debtors', debtor)
        else:
            update_debt(db_name, 'debtors', (debtor.debt_amount, debtor.id))
    
    for repaid_id in repaids_ids:
        update_debt(db_name, 'debtors', (0.0, repaid_id))

    debtors = get_debtors_by_amount(db_name, 0)

    with EmailSender(port, smtp_server, credentials, ssl_enable) as email_server:
        for debtor in debtors:
            print(debtor.username)
            mail_text = create_mail_content(debtor)
            email_server.sendmail(sender, debtor.email, mail_text)
