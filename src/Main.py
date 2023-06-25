import os
from UDF import query1, query2, query3, query4


def menu():
    query_options = [
        "10 most profitable products",
        "10 most effective employees",
        "3 least efficient employees",
        "Employee that made the most money",
        "Exit",
    ]

    while True:
        print("Select a query to run:")
        for i, option in enumerate(query_options):
            print(f"{i+1}. {option}")

        choice = input("Enter your choice: ")

        if choice == "1":
            query1()
        elif choice == "2":
            query2()
        elif choice == "3":
            query3()
        elif choice == "4":
            query4()
        elif choice == "5":
            print("Exiting program...")
            break
        else:
            os.system("cls" if os.name == "nt" else "clear")
            print("Invalid choice. Please try again.")


def main():
    menu()


if __name__ == "__main__":
    main()
