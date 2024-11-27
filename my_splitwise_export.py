from splitwise import Splitwise
import pandas as pd
from fuzzywuzzy import process 
from fuzzywuzzy import utils
from config import CONSUMER_KEY, CONSUMER_SECRET, API_KEY, GROUP_ID, CSV_FILE_PATH

food_df = pd.read_csv(
    r"crea_food_composition_tables.csv"
)

CONFIDENCE_THRESHOLD = 80

categorie_ristorante = [
    "Carni trasformate e conservate",
    "Dolci",
    "Ricette Italiane",
    "Alimenti Etnici"
]


def initialize():
    sObj = Splitwise(
    consumer_key=CONSUMER_KEY, 
    consumer_secret=CONSUMER_SECRET, 
    api_key=API_KEY
    )
    return sObj
    

def get_group_expenses(sObj, group_id= GROUP_ID,save = False):
    limit = 999  # default limit is 20

    expenses = sObj.getExpenses(limit=limit, group_id=group_id, visible=False)

    df = []
    for expense in expenses:
        df_d = {
            "Id": expense.getId(),
            "Description": expense.getDescription(),
            "Date": expense.getDate(),
            "Category": adjust_category(
                expense.getCategory().getName(), expense.getDescription()
            ),
            "Details": expense.getDetails(),
            "Cost": expense.getCost(),
            "Currency": expense.getCurrencyCode(),
            "Created by": expense.getCreatedBy().getFirstName(),
        }
        df.append(df_d)

    df = pd.DataFrame(df)
    if save:
        df.to_csv(CSV_FILE_PATH, encoding="utf-8", index=False, sep=";")
    return df


def getCategory(alimento):
    global food_df
    if utils.full_process(alimento):
        res = process.extract(alimento, food_df["name"], limit=1)[0]
    else: 
        return None
    if res[1]<CONFIDENCE_THRESHOLD:
        return None
    else:
        return food_df[food_df["name"]==res[0]]["category"].values[0]


def adjust_category(category, description):
    if category not in ["Generali","Carburante","Cinema","Sport","TV/Telefono/Internet"]:
        return category
    if description == "Payment":
        return "Pareggio"
    description = description.lower()
    descrittori = {
        "Alimentari": ["everli", "spes", "ingredient","mercato","conad","in's","ins"],
        "Utenze": ["bollett", "internet", "vodafone","gas","luce","corrente"],
        "Ristorante": ["kebab","pizza","panino","kfc","antico vinaio","shawarma","deniz"],
        "Svago":["calcetto","mostra","bigliett","partita","bowling","cinema"]
    }
    for k, v in descrittori.items():
        for i in v:
            if i in description:
                return k
    for i in description.split(" "):
        computed_category = getCategory(i)
        if computed_category != None:
            if computed_category in categorie_ristorante:
                return "Ristorante"
            else:
                return "Alimentari"
        
    return "Generali"
