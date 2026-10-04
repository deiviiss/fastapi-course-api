"""
Customers router
"""

from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select

from app.models import Customer, CustomerCreate, CustomerUpdate, CustomerPlan, Plan, StatusEnum
from app.db import SessionDep

router = APIRouter()


@router.post(
    '/customers',
    response_model=Customer,
    status_code=status.HTTP_201_CREATED,
    tags=['Customers'],
)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    """
    Create a new customer
    """

    # customer_data.model_dump() devuelve un diccionario con todos los datos del usuario
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)

    return customer


@router.get(
    '/customers',
    response_model=list[Customer],
    tags=['Customers']
)
async def list_customers(session: SessionDep):
    """
    Get all customers
    """
    customers = session.exec(select(Customer)).all()

    return customers


@router.get(
    '/customers/{customer_id}',
    response_model=Customer,
    tags=['Customers']
)
async def get_customer(customer_id: int, session: SessionDep):
    """
    Get a customer by ID
    """
    customer = session.get(Customer, customer_id)

    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    return customer


@router.delete(
    '/customers/{customer_id}',
    tags=['Customers']
)
async def delete_customer(customer_id: int, session: SessionDep):
    """
    Delete a customer by ID
    """
    customer = session.get(Customer, customer_id)

    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    session.delete(customer)
    session.commit()

    return {"message": "Customer deleted successfully"}


@router.patch(
    '/customers/{customer_id}',
    response_model=Customer,
    tags=['Customers']
)
async def update_customer(customer_id: int, customer_data: CustomerUpdate, session: SessionDep):
    """
    Update a customer by ID
    """
    customer = session.get(Customer, customer_id)

    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    # exclude_unset=True evita que se actualicen los campos que no se enviaron en el body
    # exclude_none=True evita que se actualicen los campos que tienen valor None
    # exclude_defaults=True evita que se actualicen los campos que tienen valor por defecto
    # exclude_unset=True, exclude_none=True, exclude_defaults=True
    # toma los datos del body y los convierte a dict
    customer_data_dict = customer_data.model_dump(exclude_unset=True)

    # toma los datos del dict y los actualiza en el customer
    customer.sqlmodel_update(customer_data_dict)

    session.add(customer) # agrega el customer a la session
    session.commit() # confirma la transaccion
    session.refresh(customer) # refresca el customer

    return customer


@router.post(
    '/customers/{customer_id}/plan/{plan_id}',
    tags=['Customers'],
    status_code=status.HTTP_201_CREATED
)
async def suscribe_customer_to_plan(
    customer_id: int,
    plan_id: int,
    session: SessionDep,
    plan_status: StatusEnum = Query() # Permite crear query params
):
    """
    Subscribe a customer to a plan
    """
    customer = session.get(Customer, customer_id)
    plan = session.get(Plan, plan_id)

    if not customer or not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer or Plan not found"
        )

    customer_plan = CustomerPlan(
        customer_id=customer_id,
        plan_id=plan_id,
        status=plan_status
    )

    session.add(customer_plan)
    session.commit()
    session.refresh(customer_plan)

    return customer_plan


@router.get(
    '/customers/{customer_id}/plans',
    response_model=list[Plan],
    tags=['Customers']
)
async def get_plans_from_customer(
    customer_id: int,
    session: SessionDep,
    plan_status: StatusEnum = Query()
    ):
    """
    Get the plans of a customer
    """
    customer = session.get(Customer, customer_id)

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    query = (
        select(Plan)
        .join(CustomerPlan)
        .where(CustomerPlan.customer_id == customer_id)
        .where(CustomerPlan.status == plan_status)
    )

    customer_plans = session.exec(query).all()

    return customer_plans
