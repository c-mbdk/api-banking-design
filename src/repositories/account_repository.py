from typing import Annotated, List, Optional, Type

from fastapi import Depends
from sqlmodel import select

from src.db.database import DatabaseClient, get_database_client
from src.logger import logger
from src.models.banking_models import Account
from src.repositories.base import AbstractRepository
from src.schemas.account.account_output import AccountOutput
from src.schemas.account.account_update import AccountUpdate
from src.schemas.customer.customer_output import CustomerOutput


class AccountRepository(AbstractRepository):
    """
    Repository class for handling accounts.
    """

    async def get_all(self) -> List[Optional[AccountOutput]]:
        """
        Retrieves all accounts.

        Returns:
            List[Optional[AccountOutput]]: List of all accounts.
        """
        async with self._db.get_session() as session:
            accounts = await session.exec(select(Account))
            accounts_list = accounts.fetchall()

            return self.__map_account_to_schema(accounts_list)

    async def get_by_guid(self, guid: str) -> List[AccountOutput]:
        """
        Retrieves account by guid.

        Args:
            guid (UUID4): Unique identifier for the account record.

        Returns:
            List[AccountOutput]: List containing Account record with specified guid.
        """
        async with self._db.get_session() as session:
            filtered_account = await session.get(Account, guid)

            return self.__map_account_to_schema([filtered_account])

    async def update(self, guid: str, data: AccountUpdate) -> List[AccountOutput]:
        """
        Updates an account.

        Args:
            guid (UUID4): The ID of the account to be updated.
            data (AccountUpdate): The updated account data.

        Returns:
            List[AccountOutput]: List of updated account data.
        """
        async with self._db.get_session() as session:
            account_db = await session.get(Account, guid)
            updated_data_dict = data.model_dump(exclude_unset=True)
            account_db.sqlmodel_update(updated_data_dict)
            session.add(account_db)
            await session.commit()
            await session.refresh(account_db)

            return self.__map_account_to_schema([account_db])

    async def delete(self, guid: str) -> bool:
        """
        Delete an account.

        Args:
            guid (UUID4): The ID for the account.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        async with self._db.get_session() as session:
            try:
                account = await session.get(Account, guid)
                await session.delete(account)
                await session.commit()
                return True
            except Exception as e:
                logger.exception(
                    f"Unexpected error in deletion of account {guid}: {str(e)}"
                )
                return False

    async def account_exists_by_guid(self, guid: str) -> bool:
        """
        Check if an account exists by ID.

        Args:
            guid (UUID4): The account ID.

        Returns:
            bool: True if the account exists, False otherwise.
        """
        async with self._db.get_session() as session:
            account_result = await session.exec(
                select(Account).where(Account.guid == guid)
            )

            account = account_result.fetchall()

            return bool(account)

    @staticmethod
    def __map_account_to_schema(accounts: List[Type[Account]]) -> List[AccountOutput]:
        """
        Map accounts to AccountOutput schema.

        Args:
            accounts (List[Type[Account]]): List of Account instances.

        Returns:
            List[AccountOutput]: List of AccountOutput instances.
        """
        return [
            AccountOutput(
                guid=account.guid,
                account_name=account.account_name,
                status=account.status,
                customers=[
                    CustomerOutput(
                        guid=customer.guid,
                        first_name=customer.first_name,
                        middle_names=customer.middle_names,
                        last_name=customer.last_name,
                        date_of_birth=customer.date_of_birth,
                        phone_number=customer.phone_number,
                        email_address=customer.email_address,
                        address=customer.address,
                    )
                    for customer in account.customers
                ],
            )
            for account in accounts
        ]


async def get_account_repository(
    db_client: Annotated[DatabaseClient, Depends(get_database_client)]
) -> AccountRepository:
    """Dependency provider for AccountRepository."""
    return AccountRepository(db=db_client)
