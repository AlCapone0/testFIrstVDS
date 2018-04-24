import requests

url = 'https://job.firstvds.ru/spares.json'
spar = requests.get(url).json() #качаем spares.json

url = 'https://job.firstvds.ru/alternatives.json'
alternatives = requests.get(url).json() #качаем alternatives.json

alter = alternatives.pop('alternatives') #удоляем 'alternatives'



def alterkey(key, s_alter_key):                 #выбираем все ключи из alter если нет ключа то None
    for keys in s_alter_key.keys():
        if key in s_alter_key[keys]:
            return keys

def in_alter(key, s_alter):         #проверка ключей spar в alternatives если есть то true
    for keys in s_alter.keys():
        if key in s_alter[keys]:
            return True
    return False

def newspares():                  #функция создаёт новый словарь со строкой SSD2XX
    newdict = {}
    for key_spar in spar.keys():
        if in_alter(key_spar, alter):
            key_alter = alterkey(key_spar, alter)
            if key_alter in newdict.keys():
                newdict[key_alter]['count'] += spar[key_spar]['count']
                newdict[key_alter]['arrive'] += spar[key_spar]['arrive']
                newdict[key_alter]['mustbe'] = max(newdict[key_alter]['mustbe'], spar[key_spar]['mustbe'])
            else:
                newdict[key_alter] = {}
                newdict[key_alter]['count'] = spar[key_spar]['count']
                newdict[key_alter]['arrive'] = spar[key_spar]['arrive']
                newdict[key_alter]['mustbe'] = spar[key_spar]['mustbe']
        else:
            newdict[key_spar] = {}
            newdict[key_spar]['count'] = spar[key_spar]['count']
            newdict[key_spar]['arrive'] = spar[key_spar]['arrive']
            newdict[key_spar]['mustbe'] = spar[key_spar]['mustbe']

    return newdict


newspar = newspares()

def sumspares():           #функция создаёт новый словарь sum=cout+arrive

    sumdict = {}
    for sum in newspares():
        sumdict[sum] = {}
        sumdict[sum]['count'] = newspar[sum]['count']
        sumdict[sum]['arrive'] = newspar[sum]['arrive']
        sumdict[sum]['mustbe'] = newspar[sum]['mustbe']
        sumdict[sum]['sum'] = sumdict[sum]['count'] + sumdict[sum]['arrive']

    return sumdict

sumsparesbuy = sumspares()

def needtobuy():             #функция создаёт новый словарь запчастей которые надо докупить

    needtobuy = {}
    for tobuy in sumspares():
        needtobuy[tobuy] = {}
        needtobuy[tobuy]['mustbbay'] = sumsparesbuy[tobuy]['mustbe'] - sumsparesbuy[tobuy]['sum']
        if needtobuy[tobuy]['mustbbay'] <= 1:
            del needtobuy[tobuy]

    return needtobuy