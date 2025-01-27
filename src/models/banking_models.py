from datetime import date,               datetime
from sqlalchemy import Column
from sqlalchemy.orm import RelationshipProperty
from sqlmodel import Enum, Field, Relationship, SQLModel, TIMESTAMP
import uuid

from src.enums.account_status import AccountStatus
from src.enums.currency_code import CurrencyCode
from src.enums.transaction_status import TransactionStatus
from src.enums.transaction_type import TransactionType
from src.utils.retrieve_enum_values import get_enum_values
from src.utils.time_functions import get_current_time


class CustomerAccountLink(SQLModel, table=True):
    """Linking table for customers and accounts."""

    created_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=get_current_time)
    )
    customer_guid: str | None = Field(
        default=None, 
        foreign_key="customer.guid", 
        primary_key=True
    )
    account_guid: str | None = Field(
        default=None,
        foreign_key="account.guid",
        primary_key=True
    )
    last_updated_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            default=get_current_time, onupdate=get_current_time
    )) 
    is_deleted: bool = Field(default=False)


class Customer(SQLModel, table=True):
    """Customer Entity - parties with at least one banking product."""

    guid: str = Field(
            nullable=False, primary_key=True, default_factory=uuid.uuid4
    )
    created_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=get_current_time)
    )
    first_name: str = Field(max_length=255)
    middle_names: str | None = Field(default=None, max_length=200)
    last_name: str = Field(max_length=255)
    date_of_birth: date = Field()
    phone_number: str = Field(max_length=15)
    email_address: str | None = Field(default=None, max_length=255)
    address: str = Field(max_length=255)
    last_updated_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            default=get_current_time, onupdate=get_current_time
    )) 
    is_deleted: bool = Field(default=False)

    accounts: list["Account"] = Relationship(
        back_populates="customers",
        link_model=CustomerAccountLink, 
        sa_relationship_kwargs={'lazy': 'selectin'}
    )


class Account(SQLModel, table=True):
    """Account entity - bank accounts."""

    guid: str = Field(
            nullable=False, primary_key=True, default_factory=uuid.uuid4
    )
    created_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=get_current_time)
    )
    account_name: str = Field(max_length=100)
    status: AccountStatus = Field(
        sa_column=Column(Enum(AccountStatus, values_callable=get_enum_values
    )))
    last_updated_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            default=get_current_time, onupdate=get_current_time
    )) 
    is_deleted: bool = Field(default=False)

    customers: list["Customer"] = Relationship(
        back_populates="accounts", 
        link_model=CustomerAccountLink, 
        sa_relationship_kwargs={'lazy': 'selectin'}
    )

    creditor_accounts: list["Transaction"] = Relationship(
        sa_relationship=RelationshipProperty(
            "Transaction",
            back_populates="creditor",
            foreign_keys="[Transaction.creditor_account]"
        )
    )

    debtor_accounts: list["Transaction"] = Relationship(
        sa_relationship=RelationshipProperty(
            "Transaction",
            back_populates="debtor",
            foreign_keys="[Transaction.debtor_account]"
        )
    )



class Transaction(SQLModel, table=True):
    """Transaction Entity - captures financial activity between accounts."""

    guid: str = Field(
            nullable=False, primary_key=True, default_factory=uuid.uuid4
    )
    created_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=get_current_time)
    )
    transaction_type: TransactionType = Field(
        sa_column=Column(Enum(TransactionType, values_callable=get_enum_values
    )))
    creditor_account: str = Field(
        default=None, 
        foreign_key="account.guid"
    )
    debtor_account: str = Field(
        default=None, 
        foreign_key="account.guid"
    )
    amount: int
    currency: CurrencyCode = Field(
        sa_column=Column(Enum(CurrencyCode, values_callable=get_enum_values
    )))
    transaction_date: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=get_current_time)
    )
    transaction_status: TransactionStatus = Field(
        sa_column=Column(Enum(TransactionStatus, values_callable=get_enum_values
    )))
    last_updated_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            default=get_current_time, onupdate=get_current_time
    )) 
    is_deleted: bool = Field(default=False)

    creditor: Account = Relationship(
        sa_relationship=RelationshipProperty(
            "Account",
            back_populates="creditor_accounts",
            foreign_keys='[Transaction.creditor_account]'
        )
    )

    debtor: Account = Relationship(
        sa_relationship=RelationshipProperty(
            "Account",
            back_populates="debtor_accounts",
            foreign_keys='[Transaction.debtor_account]'
        )
    )
