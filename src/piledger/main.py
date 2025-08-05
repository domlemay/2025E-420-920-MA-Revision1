from .func import get_all_accounts, calculate_balance, read_data_file, validate_account_name,handle_balance_inquiry, handle_statistics, handle_export, handle_date_search
from .display import display_all_transactions, display_transactions_by_account, display_summary, display_menu
import os




def main():
    print("Chargement des données...")
    
    if not os.path.exists('data.csv'):
        print("ERREUR: Le fichier data.csv est introuvable!")
        print("Assurez-vous que le fichier se trouve à la racine du répertoire.")
        return
    
    data = read_data_file()
    
    if len(data) == 0:
        print("ERREUR: Aucune donnée n'a pu être chargée!")
        return
    
    print(f"✅ {len(data)} transactions chargées avec succès!")
    
    accounts = get_all_accounts(data)
    
    running = True
    while running:
        running = display_menu(data, accounts)
        
        

if __name__ == "__main__":
    main()