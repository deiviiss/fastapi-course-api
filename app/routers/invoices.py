"""
Invoice router
"""

from fastapi import APIRouter, status
from sqlmodel import select

from app.models import Invoice
from app.db import SessionDep


# Create router
router = APIRouter()


@router.post(
        '/invoices',
        response_model=Invoice,
        status_code=status.HTTP_201_CREATED,
        tags=['Invoices']
    )
async def create_invoice(invoice_data: Invoice):
    """
    Create a new invoice
    """
    return invoice_data


@router.get(
    '/invoices',
    response_model=list[Invoice],
    tags=['Invoices']
)
async def list_invoices(session: SessionDep):
    """
    Get all invoices
    """
    invoices = session.exec(select(Invoice)).all()

    return invoices
