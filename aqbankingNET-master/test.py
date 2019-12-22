
import AB

print "loaded AB module: ", AB

api = AB.AB_Banking_new("gnucash", None, 0)

print "api is:", api

print "AQ init..."
assert(AB.AB_Banking_Init(api) == 0)

gui = AB.GWEN_Gui_CGui_new()
print "gwen gui is: ", gui

AB.GWEN_Gui_SetGui(gui)

al = AB.getAqbankingAccounts(api)
print "Accounts:", al, type(al)
print "Number of accounts:", AB.AB_AccountSpec_List_GetCount(al)
first = AB.AB_AccountSpec_List_First(al)
while first:
    print "Account:", first, AB.AB_AccountSpec_GetIban(first)
    first = AB.AB_AccountSpec_List_Next(first)

print "done ..."

