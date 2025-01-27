from typing import Annotated

from fastapi import APIRouter, Depends

from src.services.customer_service import CustomerService, get_customer_service
from src.schemas.base_response import GenericResponseModel
from src.schemas.create_customer_request import CreateCustomerRequest
from src.schemas.customer.customer_update import CustomerUpdate
from src.utils.constants import CREATED, OK

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post(
    path="",
    summary="Creates a customer.",
    description="This endpoint creates customer records.",
    operation_id="post-customers",
    response_model=GenericResponseModel,
    status_code=CREATED,
)
async def create_single_customer(
    request_body: CreateCustomerRequest,
    customer_service: Annotated[CustomerService, Depends(get_customer_service)]
) -> GenericResponseModel:
    """
    This endpoint handles POST requests to create a single customer.

    Args:
        request_body (CreateCustomerRequest): Request body with the new record details.
        customer_service (CustomerService): Service instance for creating customers.

    Returns:
        GenericResponseModel: The respoonse containing the created customer details.
    """
    return await customer_service.create(request_body)


@router.put(
    path="/{guid}",
    summary="Updates a single customer.",
    description="This endpoint handles PUT requests to update a single customer.",
    operation_id="update-single-customer",
    response_model=GenericResponseModel,
    status_code=OK,
)
async def update_customer(
    request_body: CustomerUpdate,
    guid: str,
    customer_service: Annotated[CustomerService, Depends(get_customer_service)]
):
    """
    This endpoint handles PUT requests to update an existing customer.

    Args:
        guid (str): The unique identifier for the customer.
        request_body (CustomerUpdate): Request body containing updated details.
        customer_service (CustomerService): Service instance for updating customers.

    Returns:
        GenericResponseModel: The respoonse containing the updated customer record.
    """
    return await customer_service.update(guid, request_body)


@router.get(
    path="",
    summary="Retrieves a list of customers.",
    description="This endpoint handles GET requests to retrieve a list of customers.",
    operation_id="get-customers-list",
    response_model=GenericResponseModel,
    status_code=OK,
)
async def get_customers(
    customer_service: Annotated[CustomerService, Depends(get_customer_service)]
) -> GenericResponseModel:
    """
    This endpoint handles GET requests to retrieve all existing customers.

    Args:
        customer_service (CustomerService): Service instance for retrieving customers.

    Returns:
        GenericResponseModel: The respoonse containing the retrieved customers.
    """
    return await customer_service.get_all()


@router.get(
    path="/{guid}",
    summary="Retrieves a single customer.",
    description="This endpoint handles GET requests to retrieve a single customer.",
    operation_id="get-single-customer",
    response_model=GenericResponseModel,
    status_code=OK,
)
async def get_single_customer(
    guid: str, 
    customer_service: Annotated[CustomerService, Depends(get_customer_service)]
) -> GenericResponseModel:
    """
    This endpoint handles GET requests to retrieve an existing customer.

    Args:
        guid (str): The unique identifier for the customer.
        customer_service (CustomerService): Service instance for retrieving customers.

    Returns:
        GenericResponseModel: The response containing the retrieved customer record.
    """
    return await customer_service.get_customer(guid)


@router.delete(
    path="/{guid}",
    summary="Deletes a single customer.",
    description="This endpoint deletes a single customer.",
    operation_id="delete-single-customer",
    response_model=GenericResponseModel,
    status_code=OK,
)
async def delete_single_customer(
    guid: str,
    customer_service: Annotated[CustomerService, Depends(get_customer_service)]
) -> GenericResponseModel:
    """
    This endpoint handles DELETE requests to delete an existing customer.

    Args:
        guid (str): The unique identifier for the customer.
        customer_service (CustomerService): Service instance for deleting customers.

    Returns:
        GenericResponseModel: The respoonse containing the outcome of the deletion.
    """
    return await customer_service.delete(guid)
