%module AB


%{
    /* Includes the header in the wrapper code */
    #include "aqbanking/banking.h"
    #include "gwenhywfar/gwenhywfar.h"
    #include "gwenhywfar/gui_be.h"       

    /* XXX define some missing functions: */
    void GWEN_InheritData_freeAllData(GWEN_INHERITDATA *d) {
        assert(0);
    }

    GWENHYWFAR_API void GWEN_StringListEntry_SetData(GWEN_STRINGLISTENTRY *se, const char *s) {
        assert(0);
    }

    AB_ACCOUNT_SPEC_LIST * getAqbankingAccounts(AB_BANKING *ab) {

        AB_ACCOUNT_SPEC_LIST *accountSpecList=NULL;

        accountSpecList=AB_AccountSpec_List_new();
        int rv=AB_Banking_GetAccountSpecList(ab, &accountSpecList);
        if (rv<0) {
            assert(0);
        }
        return accountSpecList;
    }

    // Prototype
    GWEN_GUI *GWEN_Gui_CGui_new(void);
%}

AB_ACCOUNT_SPEC_LIST * getAqbankingAccounts(AB_BANKING *ab);

typedef unsigned int uint32_t;
/* typedef signed int int32_t; */

/* Prevent syntax error in gui_be.h because of __attribute__ format usage: */
#define GWEN_FORMAT(x, y, z) 

%include "gwenhywfar/gwenhywfarapi.h"
%include "gwenhywfar/db.h"
%include "gwenhywfar/path.h"
%include "gwenhywfar/cgui.h"
%include "gwenhywfar/list1.h" 
%include "gwenhywfar/list2.h" 
%include "gwenhywfar/stringlist.h" 
%include "gwenhywfar/gwentime.h" 
%include "gwenhywfar/inherit.h"
%include "gwenhywfar/gui.h"
%include "gwenhywfar/gui_be.h"
%include "gwenhywfar/error.h"
%include "gwenhywfar/buffer.h"
%include "gwenhywfar/gwendate.h"

%include "aqbanking/error.h"
%include "aqbanking/banking.h"

%include "aqbanking/banking_online.h"

%include "aqbanking/types/account_spec.h"
%include "aqbanking/types/transaction.h"
%include "aqbanking/types/transactionlimits.h"
%include "aqbanking/types/value.h"
%include "aqbanking/types/balance.h"
%include "aqbanking/types/imexporter_context.h"
%include "aqbanking/types/imexporter_accountinfo.h"

