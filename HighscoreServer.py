#!/usr/bin/python3

import os  # Ympäristömuuttujat yms.
import cgi  # CGI moduuli serveritoteutusta varten
import cgitb  # Virheenkäsittelijä, joka osaa tulostaa nettisivulle virheviestit
import json  # Pythonin JSON endoder/decoder
import csv  # Moduuli csv-formaatin käsittelyyn
import config # config.py tiedosto, jotta kaikki toiminnot toimivat oikein


scoreList = [] # Luodaan uusi lista, jonne kopioidaan nykyiset tulokset
nameList = [] # Luodaan uusi lista, jonne kopioidaan nykyisten ennätysten haltijat
positionList = [1,2,3,4,5,6,7,8,9,10] # Tiedoston ensimmäinen pystyrivi

def Get():
# Luetaan pisteet tiedostosta, muodostetaan niistä scoreData- lista
# Palautetaan highscore lista JSON-muodossa pyynnön tekijälle
    inputFile = open("/home/study05/e6jkuusi/public_html/Example/scores.csv", "r")
    reader = csv.reader(inputFile)
    scoreData = list(reader)
    print(json.dumps(scoreData, indent= 2))
    


def Add(player, score, user, password):
# Tarkistetaan käyttäjä ja salasana.
    validPassword = config.verify_password(user, password)
    if validPassword == True:
# Jos autentikointi onnistuu, avaa tiedoston ja tallentaa tulokset listaan
        with open("/home/study05/e6jkuusi/public_html/Example/scores.csv", "r") as csv_file:
            csv_reader = csv.reader(csv_file, skipinitialspace = True, delimiter=',')
            for lines in csv_reader:
                scoreList.append(lines[2])
                nameList.append(lines[1])
# Jos tulos oikeuttaa listalle, niin lisätään se oikealle paikalleen. 
            if score >= int(lines[2]):
                scoreList.append(int(score))
                scoreList.remove(lines[2])
            scoreList.sort(reverse = True, key = int)
# Jos ei oikeutta listalle, palautetaan virhekoodi 2 sekä viesti json-muodossa.            
            if score < int(lines[2]):
                message = 'Pisteesi eivät riitä listalle!'
                response = [
                {'error': 2},
                {'message': message}
                ]
                print(json.dumps(response))
                exit()

        index = scoreList.index(score)
        nameList.pop(index)
        nameList.insert(index, player)
# Ylikirjoittaa highscore listan oikeilla tiedoilla  

        with open("/home/study05/e6jkuusi/public_html/Example/scores.csv", "w", newline= '') as file:
            writer = csv.writer(file, delimiter = ',')
            writer.writerows(zip(positionList, nameList, scoreList))
# Palautetaan virhekoodi 0 sekä viesti onnistuneesta operaatiosta
        message = 'Lisattiin kayttaja ' + player + \
         ' highscore-listalle pisteilla ' + \
            str(score) + ':  ' + 'Salasana oli oikein: ' + str(validPassword)
        response = [
        {'error': 0},
        {'message': message}
        ]
# Jos ei oikeutta tiedostoon, palautetaan virhekoodi 1 sekä viesti json-muodossa.
    elif validPassword == False:
        message = 'Käyttäjää ei lisätty, tarkista käyttäjänimi ja salasana!'
        response = [
        {'error': 1},
        {'message': message}
        ]

    print(json.dumps(response))


print('Content-type: application/json\n')

# Selvitetään, millä HTTP-metodilla pyyntö tehtiin
cgiMethod = os.environ['REQUEST_METHOD'].lower()
if cgiMethod == 'get':
# Luetaan high scoret tiedostosta ja lähetetään ne json-muodossa pyynnön tekijälle
    Get()
elif cgiMethod == 'post':
# Käyttäjä haluaa lisätä uuden highscoren tiedostoon.
# Luetaan pyynnön parametrit ja tarkistetaan nämä Add-funktiossa
    data = cgi.FieldStorage()
    name = data.getvalue('name', '')
    try:
        score = int(data.getvalue('score', '-1'))
    except ValueError:
        score = -1
    user = data.getvalue('user', '')
    password = data.getvalue('password', '')
    Add(name, score, user, password)

# Virhekoodit;
# 0 == Ok
# 1 == Autentikointi epäonnistui
# 2 == Pisteet eivät riitä listalle