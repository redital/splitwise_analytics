import my_splitwise_export
import mysql_connector
import power_bi_connector

import time
import requests

def main(force = False):

    print("Stabilisco una connessione con SpliWise")
    sObj = my_splitwise_export.initialize()

    print("Raccolgo i dati da SplitWise")
    df = my_splitwise_export.get_group_expenses(sObj, save=False)

    print("Stabilisco una connessione con il DataBase")
    mysql = mysql_connector.initialize()

    if force:
        print("Richiesto aggiornamento forzato")
        mysql_connector.replace_db(mysql,df)
    else:
        print("Confronto i dati raccolti con quelli sul DataBase")
        diff = mysql_connector.ricerca_entity_non_caricate(mysql,df)

        print("Trovate {} nuove transazioni".format(len(diff)))

        if len(diff)==0:
            print("Database già aggiornato")
            return
        
        print("Aggiorno il Database")
        mysql_connector.update_db(mysql,diff)


    print("Controllo sul DataBase")
    diff = mysql_connector.ricerca_entity_non_caricate(mysql,df)

    if len(diff) != 0:
        print("Errore - Trovate {} n righe mancanti")

    print("Stabilisco una connessione con Power BI")
    token = power_bi_connector.authenticate()


    print("Cerco l'id del DataSet")
    dataset = power_bi_connector.get_dataset(token)

    print("Controllo se l'indirizzo IP pubblico è cambiato")
          
    ip = requests.get('https://api.ipify.org').content.decode('utf8')
    
    print("Cerco il datasource")
    datasource = power_bi_connector.get_datasource_connection_details(token,dataset)

    
    if datasource["server"]==ip:
        print("Aggiornamento IP non necessario")
    else:        
        print("Faccio l'update del datasource")
        exit_code = power_bi_connector.update_datasource(token, dataset, datasource, ip)
        
        if exit_code == 200:
            print("Aggiornamento avvenuto con successo")


    print("Invio una richiesta di refresh del DataSet")
    exit_code = power_bi_connector.refresh(token,dataset)
    if exit_code == 202:
        print("Richiesta di aggiornamento inoltrata")


    status = "Requested"
    attempt = 0
    start_time = time.time()
    print("In attesa di aggiornamento")
    while status!="Completed":
        attempt+=1
        status = power_bi_connector.check_refresh_status(token,dataset,top_n = 1)[0]
        print("." + "."*(attempt%3) + " "*(2-attempt%3),end="\r")
        time.sleep(0.1)
    end_time = time.time()
    time_taken = end_time-start_time
    print("Aggiornamento completato in {:.2f} secondi".format(time_taken))
    return
