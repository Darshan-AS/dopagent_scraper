DOPAGENT_HOST = 'https://dopagent.indiapost.gov.in/'
DOPAGENT_BASE_URL = DOPAGENT_HOST + "corp/"
ACCOUNTS_PER_PAGE = 10
SUCCESS_RESPONSE_STATUS = 200


class Headers:
    EXPIRED_KEY = b'Expires'
    NOT_EXPIRED_VALUE = b'0'


class LoginPage:
    AGENT_ID_INPUT = 'AuthenticationFG.USER_PRINCIPAL'
    PASSWORD_INPUT = 'AuthenticationFG.ACCESS_CODE'
    LOG_IN_BUTTON = 'Action.VALIDATE_RM_PLUS_CREDENTIALS_CATCHA_DISABLED'
    CLEAR_VALUES_BUTTON = 'Action.CLEAR_VALUES'


class MenuPage:
    DASHBOARD_BUTTON = 'HREF_Dashboard'
    CHANGE_PASSWORD_BUTTON = 'HREF_Change Password'
    ACCOUNTS_BUTTON = 'HREF_Accounts'

    AGENT_ENQIRE_AND_UPDATE_SCREEN_LINK = 'HREF_Agent Enquire & Update Screen'
    REPORTS_LINK = 'HREF_Reports'


class AccountsListPage:
    MESSAGE_DISPLAY_TABLE_ID = 'MessageDisplay_TABLE'

    PAY_MODE_KEY = 'CustomAgentRDAccountFG.PAY_MODE_SELECTED_FOR_TRN'
    PAY_MODE_VALUE_CASH = 'C'
    PAY_MODE_VALUE_DOP_CHEQUE = 'DC'
    PAY_MODE_VALUE_NON_DOP_CHEQUE = 'NDC'

    ACCOUNT_NUMBER_SEARCH_BOX = 'CustomAgentRDAccountFG.ACCOUNT_NUMBER_FOR_SEARCH'
    FETCH_ACCOUNT_BUTTON = 'Action.FETCH_INPUT_ACCOUNT'
    CLEAR_VALUES_BUTTON = 'Action.CLEAR_ACCOUNTS'

    ACCOUNTS_LIST_TABLE_ID = 'SummaryList'
    CHECKBOX_PREFIX = "CustomAgentRDAccountFG.SELECT_INDEX_ARRAY"
    GOTO_PREV_PAGE_BUTTON = 'Action.AgentRDActSummaryAllListing.GOTO_PREV__'
    GOTO_NEXT_PAGE_BUTTON = 'Action.AgentRDActSummaryAllListing.GOTO_NEXT__'
    GOTO_PAGE_BUTTON = 'Action.AgentRDActSummaryAllListing.GOTO_PAGE__'
    GOTO_PAGE_NUMBER_INPUT = (
        'CustomAgentRDAccountFG.AgentRDActSummaryAllListing_REQUESTED_PAGE_NUMBER'
    )

    SAVE_ACCOUNTS_BUTTON = 'Action.SAVE_ACCOUNTS'
    VIEW_SAVED_INSTALLMENTS_BUTTON = 'Action.VIEW_SAVED_INSTALLMENTS'


class AccountDetailPage:
    ACCOUNT_NUMBER_ID = 'HREF_CustomAgentRDAccountFG.ACCOUNT_NUMBER'
    NAME_ID = 'HREF_CustomAgentRDAccountFG.ACCOUNT_NICKNAME'
    OPENING_DATE_ID = 'HREF_CustomAgentRDAccountFG.RD_ACCOUNT_OPEN_DATE'
    DENOMINATION_ID = 'HREF_CustomAgentRDAccountFG.RD_DESPOSIT_AMOUNT'
    TOTAL_DESPOSIT_AMOUNT_ID = 'HREF_CustomAgentRDAccountFG.RD_TOTAL_DESPOSIT_AMOUNT'
    MONTH_PAID_UPTO_ID = 'HREF_CustomAgentRDAccountFG.MONTH_PAID_UPTO_BASIC'
    NEXT_INSTALLMENT_DATE_ID = 'HREF_CustomAgentRDAccountFG.NEXT_RD_INSTALLMENT_DATE'
    LAST_DEPOSIT_DATE_ID = 'HREF_CustomAgentRDAccountFG.DATE_OF_LAST_DEPOSIT'
    REBATE_ID = 'HREF_CustomAgentRDAccountFG.REBATE'
    DEFAULT_FEE_ID = 'HREF_CustomAgentRDAccountFG.DEFAULT_FEE'
    DEFAULT_INSTALLMENT_ID = 'HREF_CustomAgentRDAccountFG.DEFAULT_INSTALLMENT'
    PENDING_INSTALLMENT_ID = 'HREF_CustomAgentRDAccountFG.PENDING_INSTALLMENT'

    BACK_BUTTON = 'Action.BACK_TO_ACCOUNT_LIST'


class InstallmentsPage:
    RADIO_BUTTON = 'CustomAgentRDAccountFG.SELECTED_INDEX'
    ACCOUNT_NUMBER_ID_PREFIX = 'HREF_CustomAgentRDAccountFG.ACCOUNT_NUMBER_ARRAY'

    GOTO_PREV_PAGE_BUTTON = 'Action.SelectedAgentRDActSummaryListing.GOTO_PREV__'
    GOTO_NEXT_PAGE_BUTTON = 'Action.SelectedAgentRDActSummaryListing.GOTO_NEXT__'
    GOTO_PAGE_BUTTON = 'Action.SelectedAgentRDActSummaryListing.GOTO_PAGE__'
    GOTO_PAGE_NUMBER_INPUT = (
        'CustomAgentRDAccountFG.SelectedAgentRDActSummaryListing_REQUESTED_PAGE_NUMBER'
    )

    PAY_ALL_SAVED_INSTALLMENTS_BUTTON = 'Action.PAY_ALL_SAVED_INSTALLMENTS'
    DELETE_SAVED_RECORD_BUTTON = 'Action.DELETE_SAVED_RECORD'
    BACK_TO_ACCOUNT_LIST_BUTTON = 'Action.BACK_TO_ACCOUNT_LIST'

    NO_OF_INSTALLMENTS_INPUT = 'CustomAgentRDAccountFG.RD_INSTALLMENT_NO'
    ASLASS_NUMBER_INPUT = 'CustomAgentRDAccountFG.ASLAAS_NO'
    GET_REBATE_AND_DEFAULT_FEE_BUTTON = 'Action.CALCULATE_REBATE'
    SAVE_NO_OF_INSTALLMENTS_BUTTON = 'Action.ADD_TO_LIST'
