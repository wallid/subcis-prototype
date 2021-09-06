# prototype
# objective
# simulate subcis using a select surah and reciter
import time
import requests
import vlc


def prompts():
    number_of_surahs = 110
    reciters = get_reciters()

    reciters_list = ""
    for reciter in reciters:
        reciters_list += f"{reciter['id']}) {reciter['reciter_name']} [{reciter['style']}]\n"

    surah_id = input("Enter surah number: ")
    reciter_id = input("Select reciter from the following\n" + reciters_list +
                       "\nEnter reciter number: ")

    # validation

    response = {
        "surah_id": int(surah_id),
        "reciter": int(reciter_id)
    }

    return response

def get_reciters():
    url = f"https://api.quran.com/api/v4/resources/recitations?language=en"
    response = requests.get(url).json()
    reciters = response["recitations"]
    return reciters

def get_ayah_recitations(reciter_id, surah_id, surah_verses_count):

    url = f"https://api.quran.com/api/v4/recitations/{reciter_id}/by_chapter/{surah_id}?per_page={surah_verses_count}"
    response = requests.get(url)
    ayahs = response.json()["audio_files"]
    return ayahs


def get_surah(surah_id):
    url = f"https://api.quran.com/api/v4/chapters/{surah_id}?language=en"
    response = requests.get(url)
    return response.json()["chapter"]


def play_audio_file(url):
    url = f"https://verses.quran.com/{url}"
    # response = requests.get(url)
    p = vlc.MediaPlayer(url)
    p.play()
    duration = p.get_length() / 1000
    time.sleep(duration)


def recite_ayah(ayah):
    audio_file = play_audio_file(ayah["url"])
    



def start(reciter_id, surah_id):

    surah = get_surah(surah_id)
    ayahs = get_ayah_recitations(reciter_id, surah_id, surah["verses_count"])

    surah_information = f"\nSurah: {surah['name_simple']}" + \
    f"\nRevelation Place: {surah['revelation_place']}" + \
    f"\nVerses: {surah['verses_count']}\n"

    print(surah_information)

    simulator = True
    control = "-1"
    previous_ayah = {}

    for ayah in ayahs:
        if(simulator):
            print("... reciters turn ... ")
            recite_ayah(ayah)
        else:
            while(control != ""):
                try:
                    if(int(control) == 1):
                        recite_ayah(previous_ayah)
                    if(int(control) == 2):
                        recite_ayah(ayah)
                except ValueError:
                    print("")
                control = input("\nControls\n1) Repeat 2) Reveal\nPress [Enter] to continue: ")


        previous_ayah = ayah
        simulator = not simulator
        control = "-1"


def main():
    print("Assalamu alaykum\nThis is a prototype subcis tool.\n")
    response = prompts()

    start(response["reciter"], response["surah_id"])


if __name__ == "__main__":
    main()
