import tweepy

from auth import *
import urllib.request, json, time


def auth():
    """
    se connecte à l'api twitter
    """
	
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api,auth

def check_new_stats():
    with open("data.json", "r+") as f:
        data = f.read()

    with urllib.request.urlopen("https://www.data.gouv.fr/fr/datasets/r/3c8e4999-df8f-4683-a2a8-6bae13813c39") as url:
        new_data = json.loads(url.read().decode())
        #print(str(new_data)+"\n\n")
        #print(data)
        if str(new_data) != data:
            print("new data")
            with open("data.json", "w") as data_w:
                data_w.seek(0)
                data_w.write(str(new_data))
                data=data_w
            n_dose1 = '{:,}'.format(int(new_data[len(new_data)-1]["n_dose1"])).replace(',', ' ')
            n_dose2 = '{:,}'.format(int(new_data[len(new_data)-1]["n_dose2"])).replace(',', ' ')
            n_cum_dose1 = '{:,}'.format(int(new_data[len(new_data)-1]["n_cum_dose1"])).replace(',', ' ')
            n_cum_dose2 = '{:,}'.format(int(new_data[len(new_data)-1]["n_cum_dose2"])).replace(',', ' ')
            couv_dose1 = new_data[len(new_data)-1]["couv_dose1"]

            date=str(new_data[len(new_data)-1]["jour"])
            text_to_push = f"Stats du {date} \U0001F489, hier :\n" \
                           f"\U0001F4CC {n_dose1} 1ères doses ont été injectées ({n_cum_dose1} au total)\n" \
                           f"\U0001F4CC {n_dose2} 2èmes doses ({n_cum_dose2} au total)\n" \
                           f"\U0001F465 {couv_dose1}% de la population a reçu au moins 1 dose\n" \
                           f" #vaccin #vaccination #astrazeneca #pfizer #moderna"
            api.update_status(status=text_to_push)
                

if __name__ == "__main__":
    api,auth = auth()
    while(True):
        print("checking")
        check_new_stats()
        time.sleep(60)
