from RPA.Robocorp.Vault import Vault
from OracleExtendedDatabase import OracleExtendedDatabase

VAULT = Vault()
DB = OracleExtendedDatabase()


def minimal_task():
    secrets = VAULT.get_secret("Oracle")
    DB.connect_to_database(
        "oracledb",
        database=secrets["db_name"],
        username=secrets["db_user"],
        password=secrets["db_pass"],
        host=secrets["db_address"],
    )
    data = DB.query("SELECT * FROM TABLE1")
    for d in data:
        print(d)
    result = DB.oracle_call_procedure("PROCEDURE1", ["Mika"])
    print(f"stored procedure = {result}")
    print("Done.")


if __name__ == "__main__":
    minimal_task()
