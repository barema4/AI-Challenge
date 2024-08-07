import csv
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Base, engine, SessionLocal
from app.models import Company, Event, Person

async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        async with session.begin():
            # Process company_info.csv
            with open('data/company_info.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                companies = [Company(**{k: v for k, v in row.items() if k in Company.__table__.columns.keys()}) for row in reader]
                session.add_all(companies)

            # Process event_info.csv
            with open('data/event_info.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                events = [Event(**{k: v for k, v in row.items() if k in Event.__table__.columns.keys()}) for row in reader]
                session.add_all(events)

            # Process people_info.csv
            with open('data/people_info.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                people = [Person(**{k: v for k, v in row.items() if k in Person.__table__.columns.keys()}) for row in reader]
                session.add_all(people)

if __name__ == "__main__":
    import asyncio
    asyncio.run(setup_database())

