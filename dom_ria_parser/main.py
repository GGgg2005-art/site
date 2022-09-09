from bs4 import BeautifulSoup
import requests
import csv



counter = 1

url = "https://dom.ria.com/uk/prodazha-kvartir/kiev/?page="

#Here you can type how much pages you want to parse
while counter <= 9:

    headers = {
        "Accept": "*/*",
        "User-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"
    }

    req = requests.get(url, headers=headers)
    src = req.text

    #Saving pages
    # with open(f"html/{counter}index.html", "w", encoding="utf-8-sig") as file:
    #     file.write(src)
    #
    #
    # with open(f"html/{counter}index.html", "r", encoding="utf-8-sig") as file:
    #     src = file.read()

    headers = {
        "Accept": "*/*",
        "User-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"
    }

    soup = BeautifulSoup(src, "lxml")

    all_flats = soup.find_all("div", class_="wrap_desc p-rel")



    for flat in all_flats:
        flat_cost = flat.find("b", class_="size18").get_text(strip=True)

    #In some flats we havent tag a and hrefs
        if flat.h2.next_element.name == "a":
            flat_href = "https://dom.ria.com/uk/" + flat.find("a", class_="realty-link size22 bold mb-10 break b").get("href")
            flat_name = flat.find("a", class_="realty-link size22 bold mb-10 break b").get_text(strip=True)
        else:
            flat_href = "https://dom.ria.com/uk/" + flat.find("a", class_="realty-link").get("href")
            flat_name = flat.find("span", class_="size22 bold break").get_text(strip=True)

        flat_headers = ["Name", "Href", "Cost"]
        flat_info = [flat_name, flat_href, flat_cost]

        # with open("data/data.csv", "w", newline="") as file:
        #     writer = csv.writer(file)
        #     writer.writerow(flat_headers)


        with open("data/data.csv", "a", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(flat_info)

    url = "https://dom.ria.com/uk/prodazha-kvartir/kiev/?page=" + f"{counter}"
    counter += 1

