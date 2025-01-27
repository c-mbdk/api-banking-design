from typing import Annotated

from fastapi import APIRouter, Depends

from src.schemas.base_response import GenericResponseModel
from src.schemas.account.account_update import AccountUpdate
from src.services.account_service import AccountService, get_account_service
from src.utils.constants import OK

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get(
    path="",
    summary="Retrieves a list of accounts.",
    description="This endpoint handles GET requests to retrieve a list of accounts.",
    operation_id="get-accounts-list",
    response_model=GenericResponseModel,
    status_code=OK,
)
async def get_accounts(
    account_service: Annotated[AccountService, Depends(get_account_service)]
) -> GenericResponseModel:
    """
    This endpoint handles GET requests to retrieve all existing accounts.

    Args:
        account_service (AccountService): Service instance for retrieving accounts.

    Returns:
        GenericResponseModel: The respoonse containing the retrieved accounts.
    """
    return await account_service.get_all()


@router.get(
    path="/{guid}",
    summary="Retrieves a single account.",
    description="This endpoint handles GET requests to retrieve a single account.",
    operation_id="get-single-account",
    response_model=GenericResponseModel,
    status_code=OK,
)
async def get_single_account(
    guid: str,
    account_service: Annotated[AccountService, Depends(get_account_service)],
) -> GenericResponseModel:
    """
    This endpoint handles GET requests to retrieve an existing account.

    Args:
        guid (str): The unique identifier for the account.
        account_service (AccountService): Service instance for retrieving accounts.

    Returns:
        GenericResponseModel: The response containing the retrieved account record.
    """
    return await account_service.get_account(guid)


@router.put(
    path="/{guid}",
    summary="Updates a single account.",
    description="This endpoint handles PUT requests to update a single account.",
    operation_id="update-single-account",
    response_model=GenericResponseModel,
    status_code=OK
)
async def update_customer(
    request_body: AccountUpdate,
    guid: str,
    account_service: Annotated[AccountService, Depends(get_account_service)]
):
    """
    This endpoint handles PUT requests to update an existing account.

    Args:
        guid (str): The unique identifier for the account.
        request_body (CustomerUpdate): Request body containing updated details.
        customer_service (CustomerService): Service instance for updating accounts.

    Returns:
        GenericResponseModel: The respoonse containing the updated account record.
    """
    return await account_service.update(guid, request_body)


@router.delete(
    path="/{guid}",
    summary="Deletes a single account.",
    description="This endpoint deletes a single account.",
    operation_id="delete-single-account",
    response_model=GenericResponseModel,
    status_code=OK
)
async def delete_single_account(
    guid: str,
    account_service: Annotated[AccountService, Depends(get_account_service)]
) -> GenericResponseModel:
    """
    This endpoint handles DELETE requests to delete an existing account.

    Args:
        guid (str): The unique identifier for the account.
        account_service (CustomerService): Service instance for deleting customers.

    Returns:
        GenericResponseModel: The respoonse containing the outcome of the deletion.
    """
    return await account_service.delete(guid)
