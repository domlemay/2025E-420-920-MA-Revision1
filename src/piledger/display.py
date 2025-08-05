from .func import get_all_accounts, calculate_balance, read_data_file, validate_account_name, handle_balance_inquiry, handle_statistics, handle_export, handle_date_search



def display_all_transactions(data): # Choix 2
    print("\n=== TOUTES LES TRANSACTIONS ===")
    for transaction in data:
        print(f"Transaction {transaction.no_txn} - {transaction.date}")
        print(f"  Compte: {transaction.account.name}")
        print(f"  Montant: {transaction.amount:.2f}$")
        if transaction.comment:
            print(f"  Commentaire: {transaction.comment}")
        print()

def display_transactions_by_account(data, account_name): # Choix 3
    print(f"\n=== TRANSACTIONS POUR LE COMPTE '{account_name}' ===")
    found_any = False
    for transaction in data:
        if transaction.account.name == account_name:
            found_any = True
            print(f"Transaction {transaction.no_txn} - {transaction.date}")
            print(f"  Montant: {transaction.amount:.2f}$")
            if transaction.comment:
                print(f"  Commentaire: {transaction.comment}")
            print()
    
    if not found_any:
        print(f"Aucune transaction trouvée pour le compte '{account_name}'")

def display_summary(data): # Choix 4
    print("\n=== RÉSUMÉ DES COMPTES ===")
    accounts = get_all_accounts(data)
    for account in accounts:
        balance = calculate_balance(data, account)
        print(f"{account}: {balance:.2f}$")
        
        
def display_menu(data, accounts):
    print("\n" + "="*50)
    print("SYSTÈME DE GESTION COMPTABLE PERSONNEL")
    print("="*50)
    print("1. Afficher le solde d'un compte")
    print("2. Afficher toutes les transactions")
    print("3. Afficher les transactions d'un compte")
    print("4. Afficher le résumé de tous les comptes")
    print("5. Afficher les statistiques")
    print("6. Exporter les écritures d'un compte")
    print("7. Rechercher par période")
    print("0. Quitter")
    print("="*50)

    try:
        choice = input("\nVotre choix: ").strip()
    except ValueError:
        print("❌ Entrée invalide! Veuillez entrer un nombre.")
        
            
    if choice == "1":
        handle_balance_inquiry(data, accounts)
    elif choice == "2":
        display_all_transactions(data)
    elif choice == "3":
        print("\n--- Transactions par compte ---")
        print("Comptes disponibles:")
        for account in accounts:
            print(f"  - {account}")
                
        account_input = input("\nEntrez le nom du compte: ").strip()
                
        if account_input:
            validated_account = validate_account_name(accounts, account_input)
            if validated_account:
                display_transactions_by_account(data, validated_account)
            else:
                print(f"Compte '{account_input}' introuvable!")
        else:
                    print("Nom de compte invalide!")
    elif choice == "4":
        display_summary(data)
    elif choice == "5":
        handle_statistics(data)
    elif choice == "6":
        handle_export(data, accounts)
    elif choice == "7":
        handle_date_search(data)
    elif choice == "0":
        print("\nMerci d'avoir utilisé le système de gestion comptable!")
        print("Au revoir!")
        return False
    else:
        print("❌ Choix invalide! Veuillez sélectionner une option valide.")
        
    if choice != "0":
        input("\nAppuyez sur Entrée pour continuer...")
    return True    