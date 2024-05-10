import os
from colorama import Fore, Back, Style
from config import *


try:
    from SimConnect import *
    import json
    from colorama import Fore, Back, Style
except Exception as e:
    print("atc.fs : Impossible d'importer les modules nécessaires. Exécutez le programme 'libraries_installer.bat'. " + str(e))
    os.system("pause")
    exit()


with open("assets/airports-locations.json", "r", encoding="utf-8") as json_file:
    try :
        zoneData = json.load(json_file)
    except:
        print("Erreur lors du paramétrage de la position des aéroports.")
        print("Erreur courante : erreur de syntaxe dans le fichier json concernant la position des aéroports. (/assets/airports-locations.json)")
        os.system("pause")
        exit()

def init():

    AttenteLancement = False
    os.system('clear')
    print(Fore.RED + "⚠️  Si ce message persiste, la connexion avec MSFS2020 n’a pas été établie.\n")
    print(Fore.YELLOW + "⏳ En attente de la connection avec Flight Simulator...\n" + Style.RESET_ALL)
    while AttenteLancement == False:
        try:
            sm = SimConnect()
        except ConnectionError:
            AttenteLancement = False
        else:
            AttenteLancement = True
            print(Fore.GREEN + "Flight Simulator lancé ! Démarrage..." + Style.RESET_ALL)
    os.system('clear')
    aq = AircraftRequests(sm, _time=2000)
    return aq



def info()->bool:
    print(Fore.GREEN + "✅ CHARGEMENT DU MODULE FLIGHT SIMULATOR 2024" + Style.RESET_ALL)
    
    return True

def getImmatOfAircraft():

    callsignD = "F-RBTS" 
    # On recupere l'immatriculation de l'avion et on verifie la forme
    if not(len(callsignD) == 6 and "-" in callsignD and (callsignD[0] == "F" or callsignD == "f")):
        if not("ASXGS" in callsignD):
            print(Fore.RED + "Immatriculation invalide : " + callsignD  + " n'est pas de la forme 'F-XXXX' ! " + Style.RESET_ALL)
        while not(len(callsignD) == 6 and "-" in callsignD and (callsignD[0] == "F" or callsignD == "f")):
    
            aq = init()
            callsignD = str(aq.get("ATC_ID")) if aq.get("ATC_ID") is not None else "F-RBTS"
            callsignD = callsignD[2:]
            for i in callsignD:
                if i != "'":
                    callsignD += i
            break
        
    print(Fore.GREEN + "✅ Immatriculation détectée... Démarrage... (" + callsignD + ")" + Style.RESET_ALL)
    return callsignD

def getCallSign(callsignD):

    callsign = ""
    carractsLettres = [0,4,5]
    caract = 0

    if len(callsignD) == 6 and "-" in callsignD and (callsignD[0] == "F" or callsignD == "f"):
        for i in callsignD:
            if i in ALPHABET_MIN and caract in carractsLettres:
                callsign += ALPHABET_AERO[ALPHABET_MIN.index(i)]
                callsign += " "
            elif i in ALPHABET_MAJ and caract in carractsLettres:
                callsign += ALPHABET_AERO[ALPHABET_MAJ.index(i)]
                callsign += " "
            caract += 1

    print(Fore.GREEN + "✅ Indicatif d'appel :" + callsign + Style.RESET_ALL)
    return callsign

def getFrequencyInAircraft(frec):

    if WITHOUT_FS:
        frequency = "118.100"
        
    else: 
        aq = init()
        frequency = str(round(aq.get("COM_ACTIVE_FREQUENCY:1"), 4))

    if frequency != None:
        while len(frequency)<7:
            frequency += "0"
        return frequency
    else:
        print("Frequence introuvable, paramétrage de la dernière fréquence")
        return frec

## POSITION
def updateFrequences(pathFile,capted,i):
    if not os.path.exists(pathFile):
        print(Fore.BLUE + "Fichier aéroport :" + pathFile + Fore.RED + " inexistant..." + Style.RESET_ALL)
        print(Fore.YELLOW +"Le code OACI de l'aéroport saisi est inconnu. Vérifier l'ortographe.")
        print("Si l'ortographe est correct, l'aéroport n'a pas été paramétré pour ce programme, vous pouvez le créer et lui donner le nom OACI correct." + Style.RESET_ALL)
        os.system("pause")
        exit()
    else:
        try :
            with open(pathFile, "r", encoding="utf-8") as json_file:
                freqInJson = json.load(json_file)["frequency"]
                if str(zoneData[i]["type"]) == "auto": # autoinformation
                    capted.append(freqInJson["twr"])
                elif str(zoneData[i]["type"]) == "all":
                    capted.append(freqInJson["grd"])
                    capted.append(freqInJson["twr"])
                    capted.append(freqInJson["app"])
                elif str(zoneData[i]["type"]) == "app":
                    capted.append(freqInJson["app"])
                elif str(zoneData[i]["type"]) == "twr":
                    capted.append(freqInJson["twr"])
                elif str(zoneData[i]["type"]) == "grd":
                    capted.append(freqInJson["grd"])
                return capted
        except:
            print("Erreur lors du paramétrage des fréquences.")
            print("Erreur courante : erreur de syntaxe dans un des fichiers json concernant un des aéroports. (/assets/airports/????.json)")
            os.system("pause")
            exit()

def inZone():
    aq = init()
    latitude = str(aq.get("PLANE_LATITUDE"))
    longitude = str(aq.get("PLANE_LONGITUDE"))
    for i in latitude :
        decimal = False
        latitudeD = ""
        latitudeN = ""
        if i != ".":
            if decimal == False:
                latitudeN += i
            else:
                latitudeD += i

def updatePositionAndFrequencies():

    
    validateAirport = "None"
  
    if WITHOUT_FS:
        LATITUDE = "49.032047"
        LONGITUDE = "2.500504"
      
    else: 
        aq = init()
        LATITUDE = str(aq.get("PLANE_LATITUDE"))
        LONGITUDE = str(aq.get("PLANE_LONGITUDE"))

    if (LATITUDE != "None" or LONGITUDE != "None"):
        captedFrequences = []
        captedFrequencesUpdated = []
  
        for i in range(len(zoneData)):
            if(str(zoneData[i]["latitude1"]) == "ALL" and str(zoneData[i]["type"]) == "UNICOM"):     
                captedFrequencesUpdated.append("122.800")
            elif(LATITUDE <= str(zoneData[i]["latitude1"]) and LATITUDE >= str(zoneData[i]["latitude2"]) and LONGITUDE >= str(zoneData[i]["longitude1"]) and LONGITUDE <= str(zoneData[i]["longitude2"])):
                read_json = "assets/airports/" + str(zoneData[i]["OACI"]) + ".json"
                validateAirport = str(zoneData[i]["OACI"])
                captedFrequencesUpdated = updateFrequences(read_json,captedFrequences,i)
        if str(type(validateAirport)) != "<class 'NoneType'>":
            return captedFrequencesUpdated,validateAirport
        else:
            return captedFrequencesUpdated,"None"
