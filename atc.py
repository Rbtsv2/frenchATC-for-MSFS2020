import os

try:
    from config import *
    import argparse
    import queue
    import sounddevice as sd
    import vosk
    import json
    from colorama import Fore, Back, Style
    import time
    import sys
    import pygame
except Exception as e:
    print("❌ Impossible d'importer les modules nécessaires. Exécutez le programme 'libraries_installer.bat'. " + str(e))
    os.system("pause")
    exit()

try:
    from gtts import gTTS
    import Files.atc_paroles as atc_paroles
    import Files.atc_fs as atc_fs
    import Files.atc_meteo as atc_meteo
    import Files.data_maker as data_maker
    import Files.atc_display as aff

except:
    print("❌ Installation incomplète ou corrompue. Impossible d'exécuter le programme.")


q = queue.Queue()

# affichage des chargements modules et parametre
#atc_paroles.info()
atc_fs.info()
data_maker.info()
#atc_meteo.info()
#aff.config(q)
aff.start()

pygame.mixer.init()

print(Fore.YELLOW + "En attente du démarrage d'un vol pour commencer..." + Style.RESET_ALL)

callsignD = atc_fs.getImmatOfAircraft()

callsign = atc_fs.getCallSign(callsignD)





authFrequencies = []
precedAuthFrequencies = []

clearance = "sol"
lastClearance = clearance
ifNeedCollation = False

frequency = "000.000"
lastfrequency = frequency

rep = [clearance,ifNeedCollation,frequency]



def printHead():

    aff.clear()
    if WITHOUT_FS:
        aff.display("# WITHOUT FS#")
    aff.display('#' * 80)
    if frequency in authFrequencies:
        aff.display("#" + 'Service ATC en fonction !'+ Fore.GREEN +' Bon vol !' + Style.RESET_ALL + ((27-len(frequency))*" ") + Back.CYAN + Fore.BLACK + " " + callsignD + " " + Style.RESET_ALL + " " + Back.BLUE + " " + frequency + " mHz " + Style.RESET_ALL + " #")
    else:
        aff.display("#" + 'Service ATC en fonction !'+ Fore.GREEN +' Bon vol !' + Style.RESET_ALL + ((27-len(frequency))*" ") + Back.CYAN + Fore.BLACK + " " + callsignD + " " + Style.RESET_ALL + " " + Back.RED + " " + frequency + " mHz " + Style.RESET_ALL + " #")
    aff.display('#' * 80)
    aff.display("#" + "Airport : " + airportData["OACI"] + " "*5 + "Freq : " + str(authFrequencies) + " "*(52-len(str(authFrequencies))) + "#")
    aff.display('#' * 80)

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    #if status:
        #print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    #print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

try:
    if args.model is None:
        args.model = "model"
    if not os.path.exists(args.model):
        print("Erreur lors du démarrage : disier 'model' manquant ! Ajoutez le dossier model.")
        print ("Please download a model for your language from https://alphacephei.com/vosk/models")
        print ("and unpack as 'model' in the current folder.")
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            printHead()
           
            rec = vosk.KaldiRecognizer(model, args.samplerate)
            while True:
                
            
                testSiTransfertRespNecessaire = atc_paroles.transfertResponsabilitesNecessaire(callsign,frequency,authFrequencies)

           
                # print(testSiTransfertRespNecessaire)
                # exit()
                
                if testSiTransfertRespNecessaire:
                    ifNeedCollation = "fréquence"

                try:
                    # recupere un aeroport en fonction de la latitude longitude
                    # On recuperer latitude et longitude de l'avion à travers Flight Simulator
                    # On soumet longitude et latitude au limites des zones géré par les aeroports pour identifié l'aeroport concerné 
                    if atc_fs.updatePositionAndFrequencies()[1] != "None":
                      
                        airportData = data_maker.maker(atc_fs.updatePositionAndFrequencies()[1])
                       
                    else:   
                        airportData = {"OACI":"NONE"}

                    authFrequencies = atc_fs.updatePositionAndFrequencies()[0]

                except TypeError:
                    pass
               
            
                #aff.defTitleOfWindow("ATC" + " ("+callsignD+")")
                
                frequency = str(atc_fs.getFrequencyInAircraft(frequency))

      
                if frequency != lastfrequency:
                    aff.display(Back.BLUE +"Fréquence modifiée :" + frequency +Style.RESET_ALL)
                    lastfrequency = frequency
                    printHead()
                if precedAuthFrequencies != authFrequencies:
                    printHead()
                    precedAuthFrequencies = authFrequencies

                data = q.get()
           
                if rec.AcceptWaveform(data):
                    pilot = json.loads(rec.FinalResult())
                    if "fox" in pilot['text']:

                        debut_sound = pygame.mixer.Sound("Sounds/debut.wav")
                        debut_sound.play()



                    if not(str(pilot['text']) == "")  and "fox" in str(pilot['text']):

                        if "météo" in pilot['text']:
                           

                            # marche pas très bien de demande mété par recup vocal du code OACI... plouip :~\
                            #phrase_pilote = pilot['text']
                            #mots = phrase_pilote.split()
                            # appels_tour_controle = [mot for mot in mots if len(mot) <= 4]
                            # oaci_pilot = appels_tour_controle[-1] if appels_tour_controle else None
                            # print(oaci_pilot)
                         
                            if airportData["OACI"] != "None":
                               
                                weather_data = atc_meteo.get_meteo(airportData["OACI"])

                                cloud_base = ""
                                if weather_data['clouds_base'] is not None and weather_data['clouds_base'] != "":
                                    cloud_base = "à une altitude de " + str(weather_data['clouds_base']) + " pieds"


                                meteo_text = f"{callsign}, la météo actuelle à {weather_data['name']} annonce des conditions météorologiques {weather_data['clouds_text']} {cloud_base}, " \
                                            f"la visibilité est de {weather_data['visib']} kilomètres, le vent de {weather_data['wdir']} degrés avec une vitesse de {weather_data['wspd']} nœuds, " \
                                            f"la température est de {weather_data['temp']} degrés Celsius, et le point de rosée est de {weather_data['dewp']} degrés Celsius." \
                                            f"La pression atmosphérique QNH est situé à {weather_data['altim']} hPa"
                                
                                meteo_tts = gTTS(meteo_text, lang="fr", slow=False)
                                meteo_tts.save("conv.mp3")
                                airport_sound = pygame.mixer.Sound("conv.mp3")
                                airport_sound.play()


                        elif ifNeedCollation == False:
                            if airportData["OACI"] != "None":
                                rep = atc_paroles.reconaissanceATC(str(pilot['text']),callsign,clearance,frequency,airportData)
                            ifNeedCollation = rep[1]
                        elif "répéter" in pilot['text'] or "répétez" in pilot['text'] or "répété" in pilot['text']:
                            time.sleep(0.3)
                            #os.popen("conv.mp3")
                            debut_sound = pygame.mixer.Sound("conv.mp3")
                            debut_sound.play()
                        else:
                            print("En attente de collation '" + ifNeedCollation + "' ... ")
                            if ifNeedCollation in pilot['text'] or "copié" in pilot['text'] or "copier" in pilot['text']:
                                ifNeedCollation = False
                                aff.display(Back.GREEN +"Collationné"+Style.RESET_ALL)
                                #os.popen("Sounds/collation.wav")
                                debut_sound = pygame.mixer.Sound("Sounds/collation.wav")
                                debut_sound.play()
                            else:
                                aff.display(Fore.RED +"Merci de collationner ! "+Style.RESET_ALL + " ("+ifNeedCollation+")")
                                aff.display(pilot['text'])
                        if rep[0] != "":
                            clearance = rep[0]
                            if clearance != lastClearance:
                                aff.display(Back.MAGENTA + "Nouvelle Clearance : " + clearance + Style.RESET_ALL)
                                lastClearance = clearance
                    #printHead()
                
                if dump_fn is not None:
                    dump_fn.write(data)

except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
