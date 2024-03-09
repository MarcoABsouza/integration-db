from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
import pprint

Base = declarative_base()


class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String(11), unique=True)
    address = Column(String, unique=True)
    accounts = relationship("Account", backref="client")

    def __repr__(self):
        return f"Client (id = {self.id}, name = {self.name}, cpf = {self.cpf}, address = {self.address})"


class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True)
    type_account = Column(String)
    agency = Column(String)
    number_account = Column(Integer, unique=True)
    id_client = Column(Integer, ForeignKey("client.id"))
    balance = Column(Float(precision=2))

    def __repr__(self):
        return f"Account (id = {self.id}, type account = {self.type_account}, agency = {self.agency}, number account = {self.number_account}, balance = {self.balance})"


# Define a conection with DB
engine = create_engine("sqlite://")

# Create class as tables in DB
Base.metadata.create_all(engine)

# Search in engine informations
inspector = inspect(engine)

# Found two tables in engine
# pprint.pprint(inspector.get_table_names())

# Create a session maker object
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def search_and_print_data():
    """Searches and prints client and account information from the database."""
    with SessionLocal() as session:
        # Search for all clients
        clients = session.query(Client).all()

        # Print information for each client and their accounts
        for client in clients:
            print(f"Client: {client}")
            for account in client.accounts:
                print(f"\n- Account: {account}")


if __name__ == "__main__":
    with SessionLocal() as session:
        client = Client(name="Marco Aurelio", cpf="12345678945", address="Goiania/GO")
        current_account = Account(
            type_account="current",
            agency="0001",
            number_account="12545678",
            balance="1000.00",
            client=client,
        )
        savings_account = Account(
            type_account="savings",
            agency="0002",
            number_account="98765432",
            balance="100.00",
            client=client,
        )
        session.add_all([client])
        session.add_all([current_account, savings_account])
        session.commit()
    search_and_print_data()
