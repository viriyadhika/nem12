from .sql_generator import execute_sql, get_sql_from_nim12, generate_nmi_details

if __name__ == "__main__":
    # with open("app/files/res.txt") as file:
    #     f = file.read()
    #     execute_sql.run(f.split("\n"))
    # get_sql_from_nim12()
    generate_nmi_details(5000, "app/files/out.csv")
