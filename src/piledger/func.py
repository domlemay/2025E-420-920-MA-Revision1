from piledger.account import Account
from piledger.transaction import Transaction




def read_data_file():  # Lire et analyser le fichier data.csv
    data = []
    with open('data.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        if i == 0:
            continue  # Skip header
        line = line.strip()
        if line:
            parts = []
            current_part = ""
            in_quotes = False
            j = 0
            while j < len(line):
                char = line[j]
                if char == '"':
                    in_quotes = not in_quotes
                elif char == ',' and not in_quotes:
                    parts.append(current_part)
                    current_part = ""
                    j += 1
                    continue
                current_part += char
                j += 1
            parts.append(current_part)
            if len(parts) >= 5:
                txn = Transaction(
                    no_txn=int(parts[0]),
                    date=parts[1],
                    account=Account(parts[2]),
                    amount=float(parts[3]),
                    comment=parts[4]
                )
                data.append(txn)
    return data

def calculate_balance(data, account_name):  # Calculer le solde d'un compte
    balance = 0.0
    for transaction in data:
        if transaction.account.name == account_name:
            balance += transaction.amount
    return balance

def get_all_accounts(data):  # Extraire tous les noms de comptes uniques
    accounts = []
    for transaction in data:
        account = transaction.account
        if not any(acc.name == account.name for acc in accounts):
            accounts.append(account)
    return [acc.name for acc in accounts]



def get_transactions_by_date_range(data, start_date, end_date): # Filtrer les transactions par plage de dates
    filtered_transactions = []
    for transaction in data:
        if start_date <= transaction.date <= end_date:
            filtered_transactions.append(transaction)
    return filtered_transactions

def find_largest_expense(data): # Plus grosse dépense (hors compte courant et revenu)
    largest_expense = None
    max_amount = 0
    for transaction in data:
        if (transaction.amount > max_amount and 
            transaction.account.name != 'Compte courant' and 
            transaction.account.name != 'Revenu'):
            max_amount = transaction.amount
            largest_expense = transaction
    return largest_expense

def find_total_income(data): # Revenus totaux
    total = 0
    for transaction in data:
        if transaction.account.name == 'Revenu':
            total += abs(transaction.amount)
    return total

def find_total_expenses(data): # Dépenses totales (hors compte courant et revenu)
    total = 0
    for transaction in data:
        if (transaction.account.name != 'Compte courant' and 
            transaction.account.name != 'Revenu' and 
            transaction.amount > 0):
            total += transaction.amount
    return total

def export_account_postings(data, account_name, filename): # Exporter les écritures d'un compte vers un fichier CSV
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("No txn,Date,Compte,Montant,Commentaire\n")
        for transaction in data:
            if transaction.account.name == account_name:
                line = f"{transaction.no_txn},{transaction.date},{transaction.account.name},{transaction.amount},{transaction.comment}\n"
                file.write(line)
    print(f"Écritures exportées vers {filename}")

def validate_account_name(accounts, account_name): # Validation du nom de compte (insensible à la casse)
    for account in accounts:
        if account.lower() == account_name.lower():
            return account
    return None

def handle_balance_inquiry(data, accounts):  # Choix 1
    print("\n--- Consultation de solde ---")
    print("Comptes disponibles:")
    for account in accounts:
        print(f"  - {account}")
    
    account_input = input("\nEntrez le nom du compte: ").strip()
    
    if not account_input:
        print("Nom de compte invalide!")
        return
    
    validated_account = validate_account_name(accounts, account_input)
    
    if validated_account:
        balance = calculate_balance(data, validated_account)
        print(f"\nSolde du compte '{validated_account}': {balance:.2f}$")
        
    else:
        print(f"Compte '{account_input}' introuvable!")
        print("Vérifiez l'orthographe ou choisissez un compte dans la liste.")

def handle_statistics(data): # Choix 5
    print("\n=== STATISTIQUES FINANCIÈRES ===")
    
    total_income = find_total_income(data)
    total_expenses = find_total_expenses(data)
    net_worth = total_income - total_expenses
    
    print(f"Revenus totaux: {total_income:.2f}$")
    print(f"Dépenses totales: {total_expenses:.2f}$")
    print(f"Situation nette: {net_worth:.2f}$")
    
    if net_worth > 0:
        print("📈 Situation financière positive")
    elif net_worth < 0:
        print("📉 Situation financière négative")
    else:
        print("⚖️  Situation financière équilibrée")
    
    largest_expense = find_largest_expense(data)
    if largest_expense:
        print(f"\nPlus grosse dépense: {largest_expense.amount:.2f}$ ({largest_expense.account.name})")
        if largest_expense.comment:
            print(f"Commentaire: {largest_expense.comment}")
    
    current_account_balance = calculate_balance(data, 'Compte courant')
    print(f"\nSolde du compte courant: {current_account_balance:.2f}$")

def handle_date_search(data): # Choix 7
    print("\n--- Recherche par période ---")
    start_date = input("Date de début (YYYY-MM-DD): ").strip()
    end_date = input("Date de fin (YYYY-MM-DD): ").strip()
    
    if not start_date or not end_date:
        print("Dates invalides!")
        return
    
    filtered_data = get_transactions_by_date_range(data, start_date, end_date)
    
    if len(filtered_data) == 0:
        print(f"Aucune transaction trouvée entre {start_date} et {end_date}")
    else:
        print(f"\n{len(filtered_data)} écritures(s) trouvée(s) entre {start_date} et {end_date}:")
        for transaction in filtered_data:
            print(f"  {transaction.date} - {transaction.account.name}: {transaction.amount:.2f}$")

def handle_export(data, accounts): # Choix 6
    print("\n--- Exportation ---")
    print("Comptes disponibles:")
    for account in accounts:
        print(f"  - {account}")
    
    account_input = input("\nEntrez le nom du compte à exporter: ").strip()
    
    if not account_input:
        print("Nom de compte invalide!")
        return
    
    validated_account = validate_account_name(accounts, account_input)
    
    if validated_account:
        filename = input("Nom du fichier de sortie (ex: export.csv): ").strip()
        if not filename:
            filename = f"export_{validated_account.replace(' ', '_').lower()}.csv"
        
        export_account_postings(data, validated_account, filename)
    else:
        print(f"Compte '{account_input}' introuvable!")
        