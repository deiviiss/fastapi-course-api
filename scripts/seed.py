"""Database seed script for populating development and testing fixtures."""

import random
import sys
from pathlib import Path

# Resolve and inject the project root directory into the Python path.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlmodel import Session, SQLModel

from app.db import engine
from app.models import Customer, CustomerPlan, Plan, StatusEnum, Transaction

CUSTOMERS_DATA: list[dict[str, str]] = [
    {
        "name": "Carlos Mendoza",
        "email": "carlos.mendoza@empresa.com",
        "description": "Cliente corporativo - Sector retail y distribución"
    },
    {
        "name": "Ana Sofia Gómez",
        "email": "ana.gomez@consultoria.org",
        "description": "Servicios profesionales y auditoría financiera"
    },
    {
        "name": "Luis Alberto Hernández",
        "email": "luis.hernandez@cloudtech.io",
        "description": "Ingeniero de infraestructura y servicios cloud"
    },
    {
        "name": "María José Morales",
        "email": "maria.morales@logistica.com",
        "description": "Directora de operaciones y suministros"
    },
    {
        "name": "Pedro Ramírez",
        "email": "pedro.ramirez@gmail.com",
        "description": "Cliente particular - Cuenta premium individual"
    },
    {
        "name": "Sofía Valentina Castro",
        "email": "sofia.castro@creativestudio.com",
        "description": "Agencia digital y diseño de productos"
    },
    {
        "name": "Jorge Eduardo Vargas",
        "email": "jorge.vargas@inversiones.com",
        "description": "Gestión de portafolios y tesorería empresarial"
    },
    {
        "name": "Lucía Fernández",
        "email": "lucia.fernandez@techcorp.dev",
        "description": "Líder técnico y arquitectura de soluciones"
    },
    {
        "name": "Miguel Ángel Torres",
        "email": "miguel.torres@constructora.com",
        "description": "Desarrollos inmobiliarios y contratación civil"
    },
    {
        "name": "Elena Patricia Navarro",
        "email": "elena.navarro@saludintegral.org",
        "description": "Coordinación médica y suministros hospitalarios"
    }
]

TRANSACTION_DESCRIPTIONS: list[str] = [
    "Pago de nómina y honorarios profesionales",
    "Adquisición de licencias de software Cloud",
    "Consumo mensual de infraestructura AWS",
    "Transferencia interbancaria a proveedores",
    "Renovación de suscripción corporativa anual",
    "Reembolso de gastos operativos y viáticos",
    "Liquidación de servicios públicos oficina central",
    "Mantenimiento preventivo de servidores",
    "Honorarios por auditoría contable externa",
    "Comisión por pasarela de pagos internacionales",
    "Prima de póliza de seguro de responsabilidad civil",
    "Anticipo por adquisición de equipamiento informático"
]

PLAN_CONFIGS: list[tuple[str, int, str]] = [
    ("Basic", 100, "Acceso estándar a plataforma y soporte por correo electrónico"),
    ("Standard", 200, "Funcionalidades avanzadas, reportes mensuales y soporte prioritario"),
    ("Premium", 300, "Acceso total, analíticas en tiempo real y asesor dedicado"),
    ("VIP", 500, "Infraestructura dedicada, SLA 99.9% y auditoría personalizada")
]


def seed() -> None:
    """Populate the database with initial demo data.

    Creates sample customers, subscription plans, customer-plan associations,
    and financial transactions. Ensures schema tables exist before insertion.
    """
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        print("Starting database seed...")

        customers: list[Customer] = []
        for data in CUSTOMERS_DATA:
            customer = Customer(
                name=data["name"],
                email=data["email"],
                age=random.randint(22, 60),
                description=data["description"]
            )
            customers.append(customer)

        session.add_all(customers)
        session.commit()

        for customer in customers:
            session.refresh(customer)

        print(f"{len(customers)} customers created.")

        plans: list[Plan] = []
        for name, price, description in PLAN_CONFIGS:
            plan = Plan(
                name=name,
                price=price,
                description=description
            )
            plans.append(plan)

        session.add_all(plans)
        session.commit()

        for plan in plans:
            session.refresh(plan)

        print(f"{len(plans)} plans created.")

        customer_plans: list[CustomerPlan] = []
        for customer in customers:
            num_plans = random.choice([1, 2])
            selected_plans = random.sample(plans, num_plans)

            if num_plans == 1:
                cp = CustomerPlan(
                    customer_id=customer.id,
                    plan_id=selected_plans[0].id,
                    status=StatusEnum.ACTIVE
                )
                customer_plans.append(cp)
            else:
                cp_active = CustomerPlan(
                    customer_id=customer.id,
                    plan_id=selected_plans[0].id,
                    status=StatusEnum.ACTIVE
                )
                cp_inactive = CustomerPlan(
                    customer_id=customer.id,
                    plan_id=selected_plans[1].id,
                    status=StatusEnum.INACTIVE
                )
                customer_plans.extend([cp_active, cp_inactive])

        session.add_all(customer_plans)
        session.commit()

        print(f"{len(customer_plans)} customer plan associations created.")

        transactions: list[Transaction] = []
        for customer in customers:
            num_transactions = random.randint(5, 15)
            for _ in range(num_transactions):
                transaction = Transaction(
                    amount=random.randint(50, 5000),
                    description=random.choice(TRANSACTION_DESCRIPTIONS),
                    customer_id=customer.id
                )
                transactions.append(transaction)

        session.add_all(transactions)
        session.commit()

        print(f"{len(transactions)} transactions created.")
        print("Seed completed successfully.")


if __name__ == "__main__":
    seed()
