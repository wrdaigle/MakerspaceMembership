import helperFunctions

#get a dictionary of all contacts
allContacts = helperFunctions.getContacts()

# determine what is owed
totalOwed = 0
for contact in allContacts:
    if contact['Balance'] > 0:
        print(contact['DisplayName'],contact['Balance'])
        totalOwed += contact['Balance']
print(totalOwed)