import img2pdf # type: ignore
import requests
from typing import NoReturn
from bs4 import BeautifulSoup
import re
import sys
import time
import threading
from pathlib import Path

nhpdf_dir = Path.home()/"Documents"/"nhpdf"
nhpdf_dir.mkdir(parents=True, exist_ok=True) 

def loading_animation():
    global la, pages, page
    spinner = ['|', '/', '-', '\\']
    while not la:
        for frame in spinner:
            sys.stdout.write(f'\rDownloading the pages ({page}/{pages})...{frame}')
            sys.stdout.flush()
            time.sleep(0.1)
            if la:  
                break
        
def compile_images(raw: list, name: str) -> NoReturn:
    global pages, page
    raw_images = []
    for item in raw:
        page += 1
        img_code, f_type = re.search(r'/(\d+)', item['data-src']).group(), re.search(r'\.([a-zA-Z0-9]+)$', item['data-src']).group()
        url = f'https://i3.nhentai.net/galleries{img_code}/{page}{f_type}'
        response = requests.get(url)
        raw_images.append(response.content)
        if page == pages:
            break
    nhpdf = nhpdf_dir/f"{name}.pdf"
    with open(nhpdf, "wb") as file:
        file.write(img2pdf.convert(raw_images))

def start_nhpdf():
    global la, page, pages
    if len(sys.argv) < 2:
        print("Usage: nhpdf <doujin-code>\nExamples:\n1. nhpdf 566212\n2. nhpdf 566212 563102")
        return
    codes = sys.argv[1:] 
    items = len(codes)
    item = 0
    for code in codes:
        la = False
        page = 0
        item += 1
        try: 
            code = int(code)
        except Exception:
            print("\nThe code needs to be numbers (Ex: 177013) :) \n\ngoing to the next code...")
            continue
        url = f'https://nhentai.net/g/{code}/'
        response = requests.get(url)
        try: 
            soup = BeautifulSoup(response.text, "html.parser")
            pages = len(soup.find_all(class_='gallerythumb'))
            name = soup.find(class_='pretty').text
            author = soup.find(class_='before').text
            raw_data = soup.find_all(class_='lazyload')
            if not author:
                author = '[NAME-MISSING]: They forgot to put the author name in the website.'
        except Exception:
            print("\n[ERROR]: The code cannot be found in the website.\n\ngoing to the next code...")
            continue
        print(f"\nH-Doujin Details:\nname: {name}\nauthor: {author}\npages: {pages}\n")
        function_thread = threading.Thread(target=loading_animation)
        function_thread.start()
        compile_images(raw_data, name)
        la = True
        function_thread.join()
        if item != items:
            print(f"\n\n{name}.pdf was successfully downloaded\n\ngoing to the next code...")

    print(f"\n\nOperation was success, the pdf's was saved into the nhpdf folder in your documents folder.\n")
        
