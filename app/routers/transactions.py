"""
Transaction router
"""

from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select

from app.models import Transaction, TransactionCreate, Customer
from app.db import SessionDep


#Create router
router = APIRouter()


@router.post(
    '/transactions',
    response_model=TransactionCreate,
    status_code=status.HTTP_201_CREATED,
    tags=['Transactions']
)
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    """
    Create a new transaction
    """
    # convert the transaction data to dict
    transaction_data_dict = transaction_data.model_dump()
    # verify if the customer exists
    customer = session.get(Customer, transaction_data_dict['customer_id'])

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    # validate the transaction
    transaction = Transaction.model_validate(transaction_data_dict)

    # Save transaction
    session.add(transaction)
    session.commit()
    session.refresh(transaction)

    return transaction


@router.get(
    '/transactions',
    response_model=list[Transaction],
    tags=['Transactions']
)
async def list_transactions(
        session: SessionDep,
        skip: int = Query(0, description="Number of transactions to skip"),
        limit: int = Query(10, description="Number of transactions to return")
    ):
    """
    Get all transactions
    """
    query = (
        select(Transaction)
        .offset(skip)
        .limit(limit)
    )

    transactions = session.exec(query).all()

    return transactions
