import requests
import json
from bs4 import BeautifulSoup
import time
import random
import pymongo


class Fetcher():
    def __init__(self, mongo_collection, sleep_time_lower_bound=0, sleep_time_upper_bound=3, batch_size=100):
        self.STARTING_FILE_NAME = "arles-france-2443"
        self.mongo_collection = mongo_collection
        self.SLEEP_TIME_LOWER_BOUND = sleep_time_lower_bound
        self.SLEEP_TIME_UPPER_BOUND = sleep_time_upper_bound
        self.batch_size = batch_size #in order to avoid running out of memory, data is inserted to mongo in batches (see "fetch" method)
        self.next_file_name = self.STARTING_FILE_NAME #points to the next url to fetch. It begins with self.STARTING_FILE_NAME
        self.num_docs_inserted = 0

    #return type: int
    def compute_sleep_time(self, lower_bound, upper_bound):
        return random.randint(lower_bound, upper_bound)

    #return type: dict
    def request_json_data(self):
        #sleep in-between requests
        random_sleep_time = self.compute_sleep_time(self.SLEEP_TIME_LOWER_BOUND, self.SLEEP_TIME_UPPER_BOUND)
        time.sleep(random_sleep_time)

        url = "https://earthview.withgoogle.com/_api/" + self.next_file_name + ".json"
        json_text = requests.get(url).text
        data = json.loads(json_text)
        return self.get_data_dict(data)

    #only a subset of the long photo-specific json is needed. This method computes the relevant subset
    def get_data_dict(self, json_data):
        country = json_data["country"] if "country" in json_data else "n/a"
        region = json_data["region"] if "region" in json_data else "n/a"
        name = json_data["name"] if "name" in json_data else "n/a"
        slug = json_data["slug"] if "slug" in json_data else "n/a"
        photo_url = json_data["photoUrl"] if "photoUrl" in json_data else "n/a"
        share_url = json_data["shareUrl"] if "shareUrl" in json_data else "n/a"
        photo_id = json_data["id"] if "id" in json_data else "n/a"
        next_slug = json_data["nextSlug"] if "nextSlug" in json_data else "n/a"
 
        return {
            "country": country ,
            "region": region,
            "name": name,
            "slug": slug,
            "photoUrl": photo_url,
            "shareUrl": share_url,
            "photoId": photo_id,
            "nextSlug": next_slug
        }

    def set_next_file_url(self, json_data):
        self.next_file_name = json_data['nextSlug']

    def fetch(self):
        print("\nFetching the data.", flush=True)
        photos_data = []

        #first photo's data
        photo_json_data = self.request_json_data()
        self.set_next_file_url(photo_json_data)
        photos_data.append(photo_json_data)
        
        while (self.next_file_name != self.STARTING_FILE_NAME):
            photo_json_data = self.request_json_data()
            self.set_next_file_url(photo_json_data)
            photos_data.append(photo_json_data)

            #every time batch_size is reached, the data is inserted to mongo and photos_data is emptied. 
            #this is to avoid running out of memory
            if (len(photos_data) == self.batch_size):
                self.mongo_collection.insert_many(photos_data)
                self.num_docs_inserted += self.batch_size
                print("\n")
                print("Batch of " + str(self.batch_size) + " docs inserted", flush=True)
                print("Total num docs inserted: " + str(self.num_docs_inserted), flush=True)
                photos_data = []
        
        if (len(photos_data) > 0):
            self.mongo_collection.insert_many(photos_data)
            self.num_docs_inserted += len(photos_data)
            print("\n")
            print("Batch of " + str(len(photos_data)) + " docs inserted", flush=True)
            print("Total num docs inserted: " + str(self.num_docs_inserted), flush=True)



    