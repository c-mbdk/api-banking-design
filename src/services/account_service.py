from typing import Annotated

from fastapi import Depends, HTTPException

from src.repositories.account_repository import (
    AccountRepository, get_account_repository
)
from src.schemas.base_response import GenericResponseModel
from src.schemas.account.account_update import AccountUpdate
from src.utils.constants import (
    INTERNAL_SERVER_ERROR,
    NOT_FOUND, 
    OK, 
    SUCCESS_ACCOUNT_DATA_FOUND, 
    SUCCESS_ACCOUNT_DELETED,
    SUCCESS_ACCOUNT_UPDATED,
    SUCCESS_FALSE, 
    SUCCESS_TRUE
    )


class AccountService:
    """
    Service class for handling accounts.

    This class provides methods to manage accounts.
    It interacts with the database via repositories to perform CRUD operations.
    """

    def __init__(self, account_repository: AccountRepository):
        """
        Initialises the service with an AccountRepository instance.

        Args:
            account_repository (AccountRepository): AccountRepository instance.
        """
        self.account_repository = account_repository


    async def get_all(self) -> GenericResponseModel:
        """
        Retrieve all accounts.

        Returns:
            GenericResponseModel: The wrapper for the response from the database.
            The retrieved data is in the wrapper's data attribute.
        """
        return GenericResponseModel(
            status_code=OK,
            success=SUCCESS_TRUE,
            message=SUCCESS_ACCOUNT_DATA_FOUND,
            data=[account.model_dump_json() for 
                  account in await self.account_repository.get_all()
                ]
        )
    
    async def get_account(self, guid: str) -> GenericResponseModel:
        """
        Retrieve an account by ID.

        Args:
            guid (str): The ID of the account.

        Returns:
            GenericResponseModel: The wrapper for the response from the database.
            The retrieved data is in the wrapper's data attribute.
        """
        if not await self.account_repository.account_exists_by_guid(guid):
            raise HTTPException(
                status_code=NOT_FOUND,
                detail=f"Account not found: {guid}"
            )
        
        return GenericResponseModel(
            status_code=OK,
            success=SUCCESS_TRUE,
            message=SUCCESS_ACCOUNT_DATA_FOUND,
            data=[
                account.model_dump_json() for 
                account in await self.account_repository.get_by_guid(guid)
            ]
        )
    
    async def update(self, guid: str, data: AccountUpdate) -> GenericResponseModel:
        """
        Update an account.

        Args:
            guid (str): The ID of the account.
            data (AccountUpdate): The data to update the account.

        Returns:
            GenericResponseModel: The wrapper for the response from the database.
            The retrieved data is in the wrapper's data attribute.
        """
        if not await self.account_repository.account_exists_by_guid(guid):
            raise HTTPException(
                status_code=NOT_FOUND,
                detail=f"Account not found: {guid}"
            )
        
        return GenericResponseModel(
            status_code=OK,
            success=SUCCESS_TRUE,
            message=SUCCESS_ACCOUNT_UPDATED,
            data=[
                account.model_dump_json() for 
                account in await self.account_repository.update(guid, data)
            ]
        )
    
    async def delete(self, guid: str) -> GenericResponseModel:
        """
        Delete an account.

        Args:
            guid (str): ID of the customer.

        Returns:
            GenericResponseModel: The wrapper for the response from the database.
            The retrieved data is in the wrapper's data attribute.
        """
        if not await self.account_repository.account_exists_by_guid(guid):
            raise HTTPException(
                status_code=NOT_FOUND,
                detail=f"Account not found: {guid}"
            )

        account_deleted = await self.account_repository.delete(guid)

        if not account_deleted:
            return GenericResponseModel(
                status_code=INTERNAL_SERVER_ERROR,
                success=SUCCESS_FALSE,
                message=f"Account record not deleted: {guid}",
                data=[]
            )
        
        return GenericResponseModel(
            status_code=OK,
            success=SUCCESS_TRUE,
            message=SUCCESS_ACCOUNT_DELETED,
            data=[]
        )


async def get_account_service(
        account_repository: Annotated[AccountRepository,
        Depends(get_account_repository)]
    ):
    """Dependency provider for AccountService."""
    return AccountService(account_repository=account_repository)
