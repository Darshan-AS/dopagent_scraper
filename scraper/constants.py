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
    GOTO_PAGE_NUMBER_INPUT = 'CustomAgentRDAccountFG.AgentRDActSummaryAllListing_REQUESTED_PAGE_NUMBER'

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
    GOTO_PAGE_NUMBER_INPUT = 'CustomAgentRDAccountFG.SelectedAgentRDActSummaryListing_REQUESTED_PAGE_NUMBER'

    PAY_ALL_SAVED_INSTALLMENTS_BUTTON = 'Action.PAY_ALL_SAVED_INSTALLMENTS'
    DELETE_SAVED_RECORD_BUTTON = 'Action.DELETE_SAVED_RECORD'
    BACK_TO_ACCOUNT_LIST_BUTTON = 'Action.BACK_TO_ACCOUNT_LIST'

    NO_OF_INSTALLMENTS_INPUT = 'CustomAgentRDAccountFG.RD_INSTALLMENT_NO'
    ASLASS_NUMBER_INPUT = 'CustomAgentRDAccountFG.ASLAAS_NO'
    GET_REBATE_AND_DEFAULT_FEE_BUTTON = 'Action.CALCULATE_REBATE'
    SAVE_NO_OF_INSTALLMENTS_BUTTON = 'Action.ADD_TO_LIST'


class ReportsPage:
    FROM_DATE_INPUT = 'CustomAgentRDAccountFG.REPORT_DATE_FROM'
    TO_DATE_INPUT = 'CustomAgentRDAccountFG.REPORT_DATE_TO'
    REFERENCE_NUMBER_INPUT = 'CustomAgentRDAccountFG.EBANKING_REF_NUMBER'
    STATUS_SELECT = 'CustomAgentRDAccountFG.INSTALLMENT_STATUS'
    CHEQUE_NUMBER_INPUT = 'CustomAgentRDAccountFG.RD_CHEQUE_NO'

    STATUS_SELECT_VALUE_SELECT = ''
    STATUS_SELECT_VALUE_FAILED = 'FAL'
    STATUS_SELECT_VALUE_PENDING = 'PEN'
    STATUS_SELECT_VALUE_SUCCESS = 'SUC'

    SEARCH_BUTTON = 'Action.SEARCH_INSTALLMENT_DETAILS'
    CLEAR_BUTTON = 'Action.Clear'

    REPORTS_LIST_TABLE_ID = 'SearchResults'
    TRANSACTION_REFERENCE_NUMBER_ID_PREFIX = 'HREF_CustomAgentRDAccountFG.EBANKING_REF_NUMBER_ARRAY'
    TRANSACTION_ACCOUNT_NUMBER_ID_PREFIX = 'HREF_CustomAgentRDAccountFG.SAVED_ACCOUNT_NUMBER_ARRAY'
    TRANSACTION_TOTAL_DEPOSIT_AMOUNT_ID_PREFIX = 'HREF_CustomAgentRDAccountFG.SAVED_RD_INSTALLMENT_AMOUNT_ARRAY'
    TRANSACTION_NUMBER_OF_INSTALLMENTS_ID_PREFIX = 'HREF_CustomAgentRDAccountFG.NO_OF_INSTALLMENT_ARRAY'
    TRANSACTION_REBATE_ID_PREFIX = 'HREF_CustomAgentRDAccountFG.RD_REBATE_ARRAY'
    TRANSACTION_DEFAULT_FEE_ID_PREFIX = 'HREF_CustomAgentRDAccountFG.RD_DEFAUT_FEE_ARRAY'
    TRANSACTION_STATUS_ID_PREFIX = 'CustomAgentRDAccountFG.INSTALLMENT_STATUS_ARRAY'
    TRANSACTION_LAST_CREATED_DATE_AND_TIME_ID_PREFIX = 'HREF_CustomAgentRDAccountFG.LAST_CREATE_DATE_ARRAY'

    GOTO_PREV_PAGE_BUTTON = 'Action.RecurringInstallmentReportScreenListing.GOTO_PREV__'
    GOTO_NEXT_PAGE_BUTTON = 'Action.RecurringInstallmentReportScreenListing.GOTO_NEXT__'
    GOTO_PAGE_BUTTON = 'Action.RecurringInstallmentReportScreenListing.GOTO_PAGE__'
    GOTO_PAGE_NUMBER_INPUT = 'CustomAgentRDAccountFG.RecurringInstallmentReportScreenListing_REQUESTED_PAGE_NUMBER'

    DOWNLOAD_FORMAT_SELECT = 'CustomAgentRDAccountFG.OUTFORMAT'
    DOWNLOAD_FORMAT_SELECT_VALUE_SELECT = ''
    DOWNLOAD_FORMAT_SELECT_VALUE_PDF = '5'
    DOWNLOAD_FORMAT_SELECT_VALUE_XLS = '4'

    DOWNLOAD_REPORT_BUTTON = 'Action.GENERATE_REPORT'
