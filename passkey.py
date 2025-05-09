import subprocess

def run_generator():
    subprocess.run(['python3', 'password_generator.py'])

def run_modifier():
    subprocess.run(['python3', 'password_modifier.py'])

def run_evaluator():
    subprocess.run(['python3', 'password_evaluater_score5.py'])

def main():
    while True:
        print("\n=== Password Tool Menu ===")
        print("1. Generate a Password")
        print("2. Modify a Memorable Password")
        print("3. Evaluate a Password")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ").strip()

        if choice == '1':
            run_generator()
        elif choice == '2':
            run_modifier()
        elif choice == '3':
            run_evaluator()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
