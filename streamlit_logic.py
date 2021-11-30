import urllib.request
import os
import shutil

class Model():
    def __init__(self, mongo_collection):
        self.mongo_collection = mongo_collection

    def get_countries(self):
        return self.mongo_collection.distinct("country")

    def get_country_photos_data(self, country):
        return self.mongo_collection.find({"country": country})

    def save_img_to_file(self, img_url, file_name):
        if not os.path.exists("images"):
            os.mkdir("images")
        urllib.request.urlretrieve(img_url, f"images/{file_name}.jpg")
         

    def delete_images_folder(self):
        if os.path.exists("images"):
            shutil.rmtree("images") 
