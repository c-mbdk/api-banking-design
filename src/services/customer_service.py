from typing import Annotated

from fastapi import Depends, HTTPException

from src.repositories.customer_repository import ( 
    CustomerRepository, get_customer_repository
    )
from src.schemas.base_response import GenericResponseModel
from src.schemas.create_customer_request import CreateCustomerRequest
from src.schemas.account.account_input import AccountInput
from src.schemas.customer.customer_input import CustomerInput
from src.schemas.customer.customer_output import CustomerOutput
from src.schemas.customer.customer_update import CustomerUpdate
from src.utils.constants import (
    CREATED, 
    INTERNAL_SERVER_ERROR,
    NOT_FOUND,
    OK, 
    SUCCESS_CUSTOMER_CREATED, 
    SUCCESS_CUSTOMER_DATA_FOUND,
    SUCCESS_CUSTOMER_DELETED,
    SUCCESS_CUSTOMER_UPDATED,
    SUCCESS_FALSE,
    SUCCESS_TRUE
)


class CustomerService:
    """
    Service class for handling customers.

    This class provides methods to create and manage customers.
    It interacts with the database via repositories to perform CRUD operations.
    """

    def __init__(self, customer_repository: CustomerRepository):
        """
        Initialises the service with a CustomerRepository instance.

        Args:
            customer_repository (CustomerRepository): CustomerRepository instance.
        """
        self.customer_repository = customer_repository

    async def create(
            self, 
            data: dict
        ) -> GenericResponseModel:
        """
        Create a new customer.

        Args:
            data (CustomerInput): The customer data.

        Returns:
            GenericResponseModel: The wrapper for the response from the database.
        """
        customer_data, account_data = self.__map_data_to_schema(data)
        customer = await self.customer_repository.create(customer_data, account_data)

        return GenericResponseModel(
            status_code=CREATED, 
            success=SUCCESS_TRUE, 
            message=SUCCESS_CUSTOMER_CREATED,
            data=[CustomerOutput(**customer.model_dump()).model_dump_json()]
        )
    
    async def get_all(self) -> GenericResponseModel:
        """
        Retrieve all customers.

        Returns:
            GenericResponseModel: The wrapper for the response from the database.
            The retrieved data is in the wrapper's data attribute.
        """
        return GenericResponseModel(
            status_code=OK,
            success=SUCCESS_TRUE,
            message=SUCCESS_CUSTOMER_DATA_FOUND,
            data=[
                customer.model_dump_json() for 
                customer in await self.customer_repository.get_all()
                ]
        )

    async def get_customer(self, guid: str) -> GenericResponseModel:
        """
        Retrieve a customer by ID.

        Args:
            guid (str): The ID of the customer.

        Returns:
            GenericResponseModel: The wrapper for the response from the database.
            The retrieved data is in the wrapper's data attribute.
        """
        if not await self.customer_repository.customer_exists_by_guid(guid):
            raise HTTPException(
                status_code=NOT_FOUND, 
                detail=f"Customer not found: {guid}"
            )

        return GenericResponseModel(
            status_code=OK,
            success=SUCCESS_TRUE,
            message=SUCCESS_CUSTOMER_DATA_FOUND,
            data=[
                customer.model_dump_json() for 
                customer in await self.customer_repository.get_by_guid(guid)
            ]
        )
    
    async def update(self, guid: str, data: CustomerUpdate) -> GenericResponseModel:
        """
        Update a customer.

        Args:
            guid (str): The ID of the customer.
            data (CustomerUpdate): The data to update the customer.

        Returns:
            GenericResponseModel: The wrapper for the response from the database.
            The retrieved data is in the wrapper's data attribute.
        """
        if not await self.customer_repository.customer_exists_by_guid(guid):
            raise HTTPException(
                status_code=NOT_FOUND, 
                detail=f"Customer not found: {guid}"
            )
        
        return GenericResponseModel(
            status_code=OK,
            success=SUCCESS_TRUE,
            message=SUCCESS_CUSTOMER_UPDATED,
            data=[
                customer.model_dump_json() for 
                customer in await self.customer_repository.update(guid, data)
            ]
        )
    
    async def delete(self, guid: str) -> GenericResponseModel:
        """
        Delete a customer.

        Args:
            guid (str): ID of the customer.

        Returns:
            GenericResponseModel: The wrapper for the response from the database.
            The retrieved data is in the wrapper's data attribute.
        """
        if not await self.customer_repository.customer_exists_by_guid(guid):
            raise HTTPException(
                status_code=NOT_FOUND, 
                detail=f"Customer not found: {guid}"
            )
        customer_deleted = await self.customer_repository.delete(guid)
        
        if not customer_deleted:
            return GenericResponseModel(
            status_code=INTERNAL_SERVER_ERROR,
            success=SUCCESS_FALSE,
            message=f"Customer record not deleted: {guid}",
            data=[]
        )

        return GenericResponseModel(
            status_code=OK,
            success=SUCCESS_TRUE,
            message=SUCCESS_CUSTOMER_DELETED,
            data=[]
        )
    
    @staticmethod
    def __map_data_to_schema(
        data: CreateCustomerRequest
    ) -> CustomerInput | AccountInput:
        """
        Maps the request data to the DTOs ahead of record creation.

        Args:
            data (CreateCustomerRequest): The data from the request.
            
        Returns:
            customer_input (CustomerInput): The data to create a customer.
            account_input (AccountInput): The data to create an account.
        """
        customer_input = CustomerInput(
            guid=data.customer_guid,
            first_name=data.first_name,
            middle_names=data.middle_names,
            last_name=data.last_name,
            date_of_birth=data.date_of_birth,
            phone_number=data.phone_number,
            email_address=data.email_address,
            address=data.address,
        )
 
        account_input = AccountInput(
            guid=data.account_guid,
            account_name=data.account_name,
            status=data.account_status
        )

        return customer_input, account_input


async def get_customer_service(
        customer_repository: Annotated[CustomerRepository, 
        Depends(get_customer_repository)]
    ) -> CustomerService:
    """Dependency provider for CustomerService."""
    return CustomerService(customer_repository=customer_repository)
