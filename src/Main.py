import os
from UDF import query1, query2, query3, query4

def menu():
    """Displays a menu with query options and executes the selected query.

    The function presents a menu of query options and prompts the user to select
    a query. Depending on the user's choice, the corresponding query function
    is called to perform the query.
    """
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
    # Entry point of the program
    menu()

# Check if the module is being run as a standalone program
if __name__ == "__main__":
    main()
