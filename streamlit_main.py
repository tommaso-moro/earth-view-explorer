import os
import pymongo
from dotenv import load_dotenv
load_dotenv('.env')
import streamlit as st
from streamlit_logic import Model


## OVERWRITE DEFAULT STREAMLIT STYLING FOR BUTTONS ##

m = st.markdown(""" 
            <style>
            div.stButton > button:first-child {
                background: none;
                border: none; 
                text-decoration: underline;
                margin-top: -1rem;
            }
            </style>""", unsafe_allow_html=True)


## CONNECT TO MONGO ##
def get_mongo_collection():
    mongo_server_url = os.getenv('MONGO_URI')
    db_name = os.getenv('DB_NAME') 
    col_name = os.getenv('COLLECTION_NAME')
    #mongo_server_url = st.secrets["MONGO_URI"]
    client = pymongo.MongoClient(mongo_server_url) 
    #db_name = st.secrets["DB_NAME"]
    #col_name = st.secrets["COLLECTION_NAME"]
    mongo_col = client.get_database(db_name)[col_name]
    return mongo_col

## LAYOUT ##
header = st.container()
dropdown_select = st.container()
photos = st.container()

def handle_img_download(img_url, img_name):
    print(img_name)
    model.save_img_to_file(img_url, img_name)

def delete_images_folder():
    model.delete_images_folder()

col = get_mongo_collection()
model = Model(col)
photos_urls_and_captions = []
country_photos_data = []

def handle_country_photos_data(selected_country):
    country_photos_data = model.get_country_photos_data(selected_country)
    for item in country_photos_data:
        photos_urls_and_captions.append({
            "photoUrl": item["photoUrl"],
            "caption": item["name"]
        })



## HEADER ##
with header:
    st.title("Earth View Explorer :earth_africa:")
    st.write("Welcome! This is a tool that allows you to systematically explore Earth View\'s beautiful landscape images.")
    st.write("Simply select a country \
        from the dropdown menu and enjoy the photos that appear below. You can download the photos too!")
    st.write("PS. they make for stunning wallpapers :)")
    st.caption("Never heard of Earth View? Earth View is a Google Chrome extension which displays a beautiful landscape \
        from Google Earth every time you open a new tab. Find out more at: https://chrome.google.com/webstore/detail/earth-view-from-google-ea/bhloflhklmhfpedakmangadcdofhnnoh?hl=en.")
    st.caption("This tool was made by Tommaso Moro (tommsmoro@gmail.com)")
    st.write("\n")
    st.write("\n")
    st.write("\n")


## DROPDOWN SELECT ##
with dropdown_select:
    selected_country = st.selectbox(
            'Pick a country',
            model.get_countries())
    handle_country_photos_data(selected_country)

    st.write("\n")
    st.write("\n")
    st.write("\n")


## PHOTOS ##
with photos:
    for photo_url_and_caption in photos_urls_and_captions:
        #photo-specific variables 
        photo_url = photo_url_and_caption["photoUrl"]
        photo_name = photo_url_and_caption["caption"]

        #photo
        st.image(photo_url, caption=photo_name)  

        col1, col2, col3, col4, col5 = st.columns([0.73,0.73,1,0.73,0.73]) #workaround to ensure the button is horizontally centered

        #custom CSS for download button (overwrites streamlit's default style)
        if col3.button("Download this image", on_click=handle_img_download, args=[photo_url, photo_name], key=photo_url):
            col1, col2, col3, col4, col5 = st.columns([1.3,1.3,0.9,1.3,1.3]) #workaround to ensure the button is horizontally centered
            col3.download_button(
                label="Download",
                data=open(f"images/{photo_name}.jpg", "rb"), #the data to be downloaded is the file that has just been created
                on_click=delete_images_folder, #delete img once the pic has been downloaded
                file_name=f"{photo_name}.jpg", #the .jpg after the file name ensures that the downloaded file's icon looks like a jpg file
                mime='image/jpg',
                key=photo_url
            )
        

        st.write("\n")
        st.write("\n")
        st.write("\n")

        

