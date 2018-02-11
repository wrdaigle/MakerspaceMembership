import configparser
import WaApi
import urllib.parse
import json

#fetch the credential from the config file
config = configparser.ConfigParser()
config.read('config.ini')
waUserName = config.get('WildApricot','username')
waPassword = config.get('WildApricot','password')
waClientID = config.get('WildApricot','clientID')
waClientSecret = config.get('WildApricot','clientSecret')

waTestUserId = config.get('WildApricot','testUser')  #optional user for testing purposes


# fetch the account info
api = WaApi.WaApiClient(waClientID, waClientSecret)
api.authenticate_with_contact_credentials(waUserName, waPassword)
accounts = api.execute_request("/v2/accounts")
account = accounts[0]

invoicesUrl = next(res for res in account.Resources if res.Name == 'Invoices').Url

##def getInvoices():
##    params = {'$top':3,'contactId': waTestUserId}
##    request_url = invoicesUrl + '?' + urllib.parse.urlencode(params)
##    print(request_url)
##    return api.execute_request(request_url)
##for inv in getInvoices():
##    print(inv.DocumentNumber)
##
##def createInvoice():
##    invoiceDetails = {
##        "OrderDetails": [
##            {
##                "Value": 1.29,
##                "Quantity": 1,
##                "Notes": "test auto invoice"
##            }
##        ],
##        "Contact": {
##            "Id": waTestUserId
##        },
##        "CreatedDate": "2017-01-16T13:24:38",
##        "CreatedBy": {
##            "Id": waTestUserId
##        }
##    }
##    return api.execute_request(invoicesUrl, api_request_object=invoiceDetails, method='POST')
##createInvoice()



contactsUrl = next(res for res in account.Resources if res.Name == 'Contacts').Url



def get_50_active_members():
    params = {'$filter': 'member eq true',
              '$top': '50',
              '$async': 'false'}
    request_url = contactsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Contacts


def print_contact_info(contact):
    print(contact.DisplayName + ', ' + contact.Email)
    for field in contact.FieldValues:
        if field.FieldName == 'Last login date':
            print('\t\t' + field.FieldName + ':' + repr(field.Value))
##    print('Main info:')
##    print('\tID:' + str(contact.Id))
##    print('\tFirst name:' + contact.FirstName)
##    print('\tLast name:' + contact.LastName)
##    print('\tEmail:' + contact.Email)
##    print('\tAll contact fields:')
##    for field in contact.FieldValues:
##        if field.Value is not None:
##            print('\t\t' + field.FieldName + ':' + repr(field.Value))


def create_contact(email, name):
    data = {
        'Email': email,
        'FirstName': name}
    return api.execute_request(contactsUrl, api_request_object=data, method='POST')


def archive_contact(contact_id):
    data = {
        'Id': contact_id,
        'FieldValues': [
            {
                'FieldName': 'Archived',
                'Value': 'true'}]
    }
    return api.execute_request(contactsUrl + str(contact_id), api_request_object=data, method='PUT')

def create_invoice(data):
    return api.execute_request(contactsUrl + str(contact_id), api_request_object=data, method='post')



#print contact list by login date
contacts = get_50_active_members()
contactDictList = []
for contact in contacts:
    newRec = {'name':contact.DisplayName,'email':contact.Email}
    for field in contact.FieldValues:
        if field.FieldName == 'Last login date':
            if field.Value == None:
                newRec['Last login date']=""
            else:
                newRec['Last login date']=field.Value
    contactDictList.append(newRec)
contactDictList = sorted(contactDictList, key=lambda k: k['Last login date'])
emails = []
for rec in contactDictList:
    emails.append(rec['email'])
    print(rec)

print()
#print contact list by last profile update
contactDictList = []
for contact in contacts:
    newRec = {'name':contact.DisplayName,'email':contact.Email}
    for field in contact.FieldValues:
        if field.FieldName == 'Profile last updated':
            if field.Value == None:
                newRec['Profile last updated']=""
            else:
                newRec['Profile last updated']=field.Value
    contactDictList.append(newRec)
contactDictList = sorted(contactDictList, key=lambda k: k['Profile last updated'])
emails = []
for rec in contactDictList:
    emails.append(rec['email'])
    print(rec)

##
### get top 10 active members and print their details
##contacts = get_50_active_members()
##for contact in contacts:
##    print_contact_info(contact)

# create new contact
#new_copntact = create_contact('some_email2@invaliddomain.org', 'John Dae')
#print_contact_info(new_copntact)

# finally archive it
#archived_contact = archive_contact(new_copntact.Id)
#print_contact_info(archived_contact)
