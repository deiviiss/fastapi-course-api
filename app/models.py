"""
Models for the FastAPI application
"""
from enum import Enum

from pydantic import BaseModel, EmailStr, field_validator
from sqlmodel import SQLModel, Field, Relationship, Session, select
from app.db import engine

# Create database model
# Heredamos la clase principal desde SQLModel sin table true para no crear una tabla en la bd
# para no crear tablas en la base de datos
class CustomerBase(SQLModel):
    """
    Model to represent a customer
    """
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    age: int = Field(default=None)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        """
        Validate email
        """
        if not value:
            return value

        with Session(engine) as session:
            query = (
                select(Customer)
                .where(Customer.email == value)
            )

            if session.exec(query).first():
                raise ValueError("Email already exists")

        return value


class CustomerCreate(CustomerBase):
    """
    Model to represent a customer
    """
    pass


class CustomerUpdate(CustomerBase):
    """
    Model to represent a customer
    """
    pass


class StatusEnum(str, Enum):
    """
    Enum to represent the status of a customer plan
    """
    ACTIVE = "active"
    INACTIVE = "inactive"


class CustomerPlan(SQLModel, table=True):
    """
    Model to represent a customer plan
    """
    id: int | None = Field(default=None, primary_key=True)
    plan_id: int = Field(foreign_key="plan.id")
    customer_id: int = Field(foreign_key="customer.id")
    status: StatusEnum = Field(default=StatusEnum.ACTIVE)


# Heredamos la clase CustomerBase que ya es un sqlmodel con
# table true para crear una tabla en la base de datos
class Customer(CustomerBase, table=True):
    """
    Model to represent a customer
    """
    # Field conecta un campo de pydantic con sqlmodel
    id: int | None = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    plans: list["Plan"] = Relationship(back_populates="customers", link_model=CustomerPlan)


class Plan(SQLModel, table=True):
    """
    Model to represent a plan
    """
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    price: int = Field(default=None)
    description: str | None = Field(default=None)
    customers: list["Customer"] = Relationship(back_populates="plans", link_model=CustomerPlan)


class TransactionBase(SQLModel):
    """
    Model to represent a transaction
    """
    amount: int
    description: str


class Transaction(TransactionBase, table=True):
    """
    Model to represent a transaction
    """
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="transactions")


class TransactionCreate(TransactionBase):
    """
    Model to represent a transaction
    """
    customer_id: int = Field(foreign_key="customer.id")


class Invoice(BaseModel):
    """
    Model to represent an invoice
    """
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    # Method to calculate the total amount of the invoice
    @property
    def amount_total(self) -> int:
        """
        Calculate the total amount of the invoice
        """
        return sum(transaction.amount for transaction in self.transactions)
