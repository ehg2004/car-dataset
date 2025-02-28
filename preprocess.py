import json
import pandas as pd
from datetime import datetime
import ast
import re

def parse_string(raw_string):
    fixed_str = raw_string.replace("{", "[").replace("}", "]")
    fixed_str = re.sub(r'(?<=\[|,)(\s*[A-Za-zÀ-ÿ0-9-]+(?:\s+[A-Za-zÀ-ÿ0-9-]+)*\s*)(?=,|\])', r'"\1"', fixed_str) 
    parsed_set = ast.literal_eval(fixed_str)
    parsed_list = sorted(parsed_set)
    return parsed_list


# Define input and output files
json_file = "CaseData.json"
csv_file = "processed_dataset1.csv"

with open('CaseData.json') as f:
#Como dataset contem um vetor de carros, podemos carrega-los dessa forma
    cars = json.load(f)
#retorna cars como uma lista#
#podemos enxergar cada carro como um dicionário de sets

preprocessed_cars=[]


#estaremos removendo as hashes já que são unicas e não atribuem sentido à análise que faremos
hashed_keys = {"listing_id", "vehicle_plate", "vehicle_category", "color", "gearbox", "dealer_id"}
#palavras-chave a serem removidas#

diferentials_set = set()
equipaments_set = set()

diferentials_list=[]
equipaments_list=[]
for i,car in enumerate(cars):
    # if i>3:
    #     break
    
    diferentials=parse_string(car["diferentials"])
    print(diferentials)
    equipaments=parse_string(car["equipaments"])
    print(equipaments)
    for diferential in diferentials:
        if diferential not in diferentials_list:
            diferentials_list.append(diferential)
    for equipament in equipaments:
        if equipament not in equipaments_list:
            equipaments_list.append(equipament)

diferentials_list = sorted(diferentials_list)
equipaments_list = sorted(equipaments_list)

print(diferentials_list)
print(equipaments_list)


data=[]
listed_keys={"diferentials","equipaments"}
time_keys={"created_at","updated_at"}
year_keys={"model_year","make_year"}

#estaremos removendo as hashes já que são unicas e não atribuem sentido à análise que faremos
# removed_keys = {"listing_id", "vehicle_plate", "vehicle_category", "color", "gearbox", "dealer_id"}
#palavras-chave a serem removidas#


#extrair as palavras-chaves do dicionario 
keys = list(cars[0].keys())


#encontra as hashes e outros campos com string para passarem pelo encoder 
#(para serem transformados em categorias discretas)
#((desconsidera-se listed_keys, year_keys,time_keys))
to_encoder=[]
for key in cars[0].keys():
    if isinstance(cars[0][key],(int,float,datetime)) is False and (key not in listed_keys) and (key not in time_keys) and (key not in year_keys):
        to_encoder.append(key)

print(to_encoder)

# import time
# time.sleep(30)


#lista os campos sem listas (excluindo timestamps) 
keys_non_listed = [key for key in keys if (key not in listed_keys) and (key not in time_keys)]

#transforma os itens diferenciais em chaves unicas (já categorizadas)
keys_diferential=[]
for diferential in diferentials_list:
    key="diferential_"+diferential.replace(' ', '_')
    keys_diferential.append(key)

#transforma os equipamentos em chaves unicas (já categorizadas)
keys_equipment=[]
for equipament in equipaments_list:
    key="equipament_"+equipament.replace(' ', '_')
    keys_equipment.append(key)

#junta as chaves para a nova formatação
counter_keys=["diferentials_counter", "equipaments_counter"]
#junta as chaves para a nova formatação
fomated_keys=keys_non_listed+keys_diferential+keys_equipment+counter_keys

import random
from sklearn.utils import shuffle
cars=shuffle(cars)
data=[]
for i,car in enumerate(cars):

    if i>10000-1:
        break
    #cria novo objeto de dicionario e inicaliza as chaves
    preprocessed_car=dict().fromkeys(fomated_keys)




    #copia campos por chave
    for key in keys_non_listed:
        #transforma string com ano em valor numérico
        if key in year_keys:
            preprocessed_car[key]=int(car[key])
        else:
            preprocessed_car[key]=car[key]
    
    #encontra equipamentos presentes no carro
    try:
        car_equipaments=parse_string(car["equipaments"])
    except:
        print(car["equipaments"])
        break   


    preprocessed_car["equipaments_counter"]=len(car_equipaments)
    if len(car_equipaments) >60:
        print(car_equipaments)
    for equipament in equipaments_list:
        key=f"equipament_{equipament.replace(' ', '_')}"
        #identifica a presença
        if equipament in car_equipaments:
            preprocessed_car[key]=1
        else:
            preprocessed_car[key]=0

    #encontra itens diferenciais presentes no carro
    try:
        car_diferentials=parse_string(car["diferentials"])
    except:
        print(car["diferentials"])
        break   

    preprocessed_car["diferentials_counter"]=len(car_diferentials)
    for diferential in diferentials_list:
        key=f"diferential_{diferential.replace(' ', '_')}"
        #identifica a presença
        if diferential in car_diferentials:
            preprocessed_car[key]=1
        else:
            preprocessed_car[key]=0
    #junta nota linha
    data.append(preprocessed_car)   

        



# print(keys)
# for i,car in enumerate(cars):
#     if i>3:
#         break

#     preprocessed_car=dict().fromkeys(keys)
#     for key in keys:
#         preprocessed_car[key]=car[key]
#     preprocessed_cars.append(preprocessed_car) 

# print(data)


# Convert to DataFrame
df = pd.DataFrame(data)

# df = df.drop('column_name', axis=1)

from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
encoder.fit(to_encoder)
encoder_list={}
for col in to_encoder:
    encoder_list[col]=LabelEncoder()
    df[col]=encoder_list[col].fit_transform(df[col])
    # print((encoder_list[col].))
print(df)
# Save to CSV
print("Saving processed dataset to CSV...")
df.to_csv(csv_file, index=False, encoding='utf-8')
print("Done!")


# print(objects[0:5]["listing_id"])
# for obj in object
# # Features to remove (hash-based features)

# # Read JSON dataset in chunks
# def read_json_lines(filename):
#     with open(filename, "r", encoding="utf-8") as f:
#         for line in f:
#             yield json.loads(line)
