import http


DEV_DB_PATH = "sqlite:///app.db"
EXAMPLE_GUID_1 = "bf2a60a6-6322-40b3-88df-79a6631f4996"
EXAMPLE_GUID_2 = "254e6eb6-78a5-4481-ac7a-b551de0e1b48"

# HTTP Status Codes
OK = http.HTTPStatus.OK
CREATED = http.HTTPStatus.CREATED
NOT_FOUND = http.HTTPStatus.NOT_FOUND
INTERNAL_SERVER_ERROR = http.HTTPStatus.INTERNAL_SERVER_ERROR


# Error messages


# Generic Response Model
SUCCESS_TRUE = "true"
SUCCESS_FALSE = "false"

# Success messages - Customer
SUCCESS_CUSTOMER_CREATED = "Customer record created"
SUCCESS_CUSTOMER_DATA_FOUND = "Available customer data returned"
SUCCESS_CUSTOMER_DELETED = "Customer record deleted"
SUCCESS_CUSTOMER_UPDATED = "Customer record updated"

# Success messages - Account
SUCCESS_ACCOUNT_DATA_FOUND = "Available account data returned"
SUCCESS_ACCOUNT_DELETED = "Account record deleted"
SUCCESS_ACCOUNT_UPDATED = "Account record updated"
