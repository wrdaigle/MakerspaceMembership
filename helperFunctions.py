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

# fetch the account info
api = WaApi.WaApiClient(waClientID, waClientSecret)
api.authenticate_with_contact_credentials(waUserName, waPassword)
accounts_v2_0 = api.execute_request("/v2/accounts")
account_v2_0 = accounts_v2_0[0]
accounts_v2_1 = api.execute_request("/v2.1/accounts")       # use version 2.1 some advanced features that weren't available in 2.0
account_v2_1 = accounts_v2_1[0]

#get a list of all contacts
def getContacts():
    allContacts = []
    contactsUrl = next(res for res in account_v2_0.Resources if res.Name == 'Contacts').Url

    def get_50_active_members():
        params = {'$filter': 'member eq true',
                  '$top': '50',
                  '$async': 'false'}
        request_url = contactsUrl + '?' + urllib.parse.urlencode(params)
        for contact in api.execute_request(request_url).Contacts:
            newcontact = {
                'ContactId':contact.Id,
                'DisplayName':contact.DisplayName,
                'FirstName':contact.FirstName,
                'LastName':contact.LastName,
                'MembershipLevel':contact.MembershipLevel.Name,
                'Status':contact.Status,
                'Url':contact.Url,
                'Email':contact.Email
            }
            for fieldValue in contact.FieldValues:
                if fieldValue.SystemCode =='Balance':
                    newcontact['Balance'] = fieldValue.Value
                if fieldValue.SystemCode =='RenewalDue':
                    newcontact['RenewalDue'] = fieldValue.Value
                if fieldValue.SystemCode =='Status':
                    newcontact['Status'] = fieldValue.Value.Value
            allContacts.append(newcontact)

    get_50_active_members()
    return allContacts


##
##
##    def print_contact_info(contact):
##        print(contact.DisplayName + ', ' + contact.Email)
##        for field in contact.FieldValues:
##            if field.FieldName == 'Last login date':
##                print('\t\t' + field.FieldName + ':' + repr(field.Value))



##
##
##
###fetch the credential from the config file
##config = configparser.ConfigParser()
##config.read('config.ini')
##waUserName = config.get('WildApricot','username')
##waPassword = config.get('WildApricot','password')
##waClientID = config.get('WildApricot','clientID')
##waClientSecret = config.get('WildApricot','clientSecret')
##
##waTestUserId = config.get('WildApricot','testUser')  #optional user for testing purposes
##
##
### fetch the account info
##api = WaApi.WaApiClient(waClientID, waClientSecret)
##api.authenticate_with_contact_credentials(waUserName, waPassword)
##accounts = api.execute_request("/v2.1/accounts")
##account = accounts[0]
##
##invoicesUrl = next(res for res in account.Resources if res.Name == 'Invoices').Url
##
##allInvoices = []
##
##def getInvoice(id):
##    request_url = invoicesUrl + str(id)
##    print(request_url)
##    return api.execute_request(request_url)
##
##def getUnpaidInvoiceIds():
##    params = {'$top':10,'UnpaidOnly':True,'idsOnly':True}
##    request_url = invoicesUrl + '?' + urllib.parse.urlencode(params)
##    print(request_url)
##    ids = api.execute_request(request_url).InvoiceIdentifiers
##    for id in ids:
##        allInvoices.append(getInvoice(id))
##getUnpaidInvoiceIds()
##
##def addVolunteerHoursDiscount(invoiceID,discount):
##    invoiceData = getInvoice(invoiceID)
##    newInvoiceData = invoiceData.OrderDetails
##    newInvoiceData.append({"Notes": "Volunteer discount - 2 hours", "Value": -1*discount, "Taxes": None})
##    data = {
##        'Id': invoiceID,
##        'OrderDetails': newInvoiceData,
##        "Contact": {
##            "Id": waTestUserId
##        }
##    }
##    return api.execute_request(invoicesUrl + str(invoiceID), api_request_object=data, method='PUT')
##
##
##
####out = getUnpaidInvoiceIds()
####
####
####
####for invoiceId in out.InvoiceIdentifiers:
####    print invoiceId
##
##
####out2 = getInvoice('33631935')
####
####contactsUrl = next(res for res in account.Resources if res.Name == 'Contacts').Url
####def getContact(id):
####    request_url = contactsUrl + id
####    print(request_url)
####    return api.execute_request(request_url)
####out3 = getContact('35641583')
##
####for inv in getInvoices():
####    print(inv.DocumentNumber)
##
####def getInvoice(invoiceId):
####    params = {'$DocumentNumber': invoiceId}
####    request_url = invoicesUrl + '?' + urllib.parse.urlencode(params)
######    request_url = invoicesUrl + invoiceId
######    request_url = invoicesUrl + '?UnpaidOnly'
####    print(request_url)
####    return api.execute_request(request_url)
####
####out2 = getInvoice('00027')
##
##
##
##
##
##
####def createInvoice():
####    invoiceDetails = {
####        "OrderDetails": [
####            {
####                "Value": 1.29,
####                "Quantity": 1,
####                "Notes": "test auto invoice"
####            }
####        ],
####        "Contact": {
####            "Id": waTestUserId
####        },
####        "CreatedDate": "2017-01-16T13:24:38",
####        "CreatedBy": {
####            "Id": waTestUserId
####        }
####    }
####    return api.execute_request(invoicesUrl, api_request_object=invoiceDetails, method='POST')
####createInvoice()


