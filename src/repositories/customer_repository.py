from typing import Annotated, List, Optional, Type

from fastapi import Depends
from sqlmodel import select

from src.db.database import DatabaseClient, get_database_client
from src.logger import logger
from src.models.banking_models import Account, Customer
from src.repositories.base import AbstractAllRepository
from src.schemas.account.account_input import AccountInput
from src.schemas.account.account_output import AccountOutput
from src.schemas.customer.customer_input import CustomerInput
from src.schemas.customer.customer_output import CustomerOutput
from src.schemas.customer.customer_update import CustomerUpdate


class CustomerRepository(AbstractAllRepository):
    """
    Repository class for handling customers.
    """

    async def get_all(self) -> List[Optional[CustomerOutput]]:
        """
        Retrieves all customers.

        Returns:
            List[Optional[CustomerOutput]]: List of all customers.
        """
        async with self._db.get_session() as session:
            customers = await session.exec(select(Customer))
            customers_list = customers.fetchall()

            return self.__map_customer_to_schema(customers_list)

    async def get_by_guid(self, guid: str) -> List[CustomerOutput]:
        """
        Retrieves customer by guid.

        Args:
            guid (str): Unique identifer for the customer record.

        Returns:
            List[CustomerOutput]: List containing Customer record with specified guid.
        """
        async with self._db.get_session() as session:
            filtered_customer = await session.get(Customer, guid)

            return self.__map_customer_to_schema([filtered_customer])

    async def create(self, data: CustomerInput, account_data: AccountInput) -> Customer:
        """
        Creates a customer.

        Args:
            data (CustomerInput): The customer data.
            account_data (AccountInput): The account data.

        Returns:
            Customer: The created customer.
        """
        async with self._db.get_session() as session:
            new_customer = Customer(**data.model_dump())
            new_account = Account(**account_data.model_dump())
            new_customer.accounts = [new_account]

            session.add(new_customer)
            await session.commit()
            await session.refresh(new_customer)

            return self.__map_customer_to_schema([new_customer])

    async def update(self, guid: str, data: CustomerUpdate) -> List[CustomerOutput]:
        """
        Updates a customer.

        Args:
            guid (str): The ID of the customer to be updated.
            data (CustomerUpdate): The updated customer data.

        Returns:
            List[CustomerOutput]: List of updated customer data.
        """
        async with self._db.get_session() as session:
            customer_db = await session.get(Customer, guid)
            updated_data_dict = data.model_dump(exclude_unset=True)
            customer_db.sqlmodel_update(updated_data_dict)
            session.add(customer_db)
            await session.commit()
            await session.refresh(customer_db)

            return self.__map_customer_to_schema([customer_db])

    async def delete(self, guid: str) -> bool:
        """
        Delete a customer.

        Args:
            guid (str): The ID for the customer.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        async with self._db.get_session() as session:
            try:
                customer = await session.get(Customer, guid)
                await session.delete(customer)
                await session.commit()
                return True
            except Exception as e:
                logger.exception(
                    f"Unexpected error in deletion of customer {guid}: {str(e)}"
                )
                return False

    async def customer_exists_by_guid(self, guid: str) -> bool:
        """
        Check if a customer exists by ID.

        Args:
            guid (str): The customer ID.

        Returns:
            bool: True if the customer exists, False otherwise.
        """
        async with self._db.get_session() as session:
            customer_result = await session.exec(
                select(Customer).where(Customer.guid == guid)
            )
            customer = customer_result.fetchall()

            return bool(customer)

    @staticmethod
    def __map_customer_to_schema(
        customers: List[Type[Customer]],
    ) -> List[CustomerOutput]:
        """
        Map customers to CustomerOutput schema:

        Args:
            customers (List[Type[Customer]]): List of Customer instances.

        Returns:
            List[CustomerOutput]: List of CustomerOutput instances.
        """
        return [
            CustomerOutput(
                guid=customer.guid,
                first_name=customer.first_name,
                middle_names=customer.middle_names,
                last_name=customer.last_name,
                date_of_birth=customer.date_of_birth,
                phone_number=customer.phone_number,
                email_address=customer.email_address,
                address=customer.address,
                accounts=[
                    AccountOutput(
                        guid=account.guid,
                        account_name=account.account_name,
                        status=account.status,
                    )
                    for account in customer.accounts
                ],
            )
            for customer in customers
        ]


async def get_customer_repository(
    db_client: Annotated[DatabaseClient, Depends(get_database_client)]
) -> CustomerRepository:
    """Dependency provider for CustomerRepository."""
    return CustomerRepository(db=db_client)
