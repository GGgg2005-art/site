from bs4 import BeautifulSoup
import csv
import requests
import json

url = 'https://calorizator.ru/product'
headers = {
    "Accept": "*/*",
    "User-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"
}

req = requests.get(url, headers=headers)
src = req.text
#
#
#
# with open("index.html", "w", encoding='utf-8-sig') as file:
#     file.write(src)
#
#
# with open("index.html") as file:
#     src = file.read()



#Получаем ссылки на продукты
# soup = BeautifulSoup(src, "lxml")
#
# all_categories_dic = {
#
# }
# all_products = soup.find_all('ul', class_="product", limit=5)
#
#
# for item in all_products:
#     all_products_href = item.find_all('li')
#     for prod in all_products_href:
#         prod_text = prod.text
#         prod_href = "https://calorizator.ru/" + prod.next_element.get('href')
#         all_categories_dic[prod_text] = prod_href
#
# with open("all_categories_dic.json", "w", encoding='utf-8-sig') as file:
#     json.dump(all_categories_dic, file, indent=4, ensure_ascii=False)


with open("all_categories_dic.json") as file:
    all_categories = json.load(file)




for category_name, category_href in all_categories.items():
    req1 = requests.get(category_href, headers=headers)
    src1 = req1.text

    # with open(f"data/{category_name}.html", "w") as file:
    #     file.write(src)
    #
    # with open(f"data/{category_name}.html") as file:
    #     src = file.read()

    soup = BeautifulSoup(src1, "lxml")
    #Собираем заголовки
    table_head_names = [];

    table_head = soup.find('table', class_='views-table sticky-enabled cols-6').find('thead').find('tr').find_all('th')
    for item in table_head:
        table_head_name = item.next_element.next_element
        table_head_names.append(table_head_name.text)
    table_head_names.remove('\n')


    products = table_head_names[0]
    proteins = table_head_names[1]
    fats = table_head_names[2]
    carb = table_head_names[3]
    calories = table_head_names[4]


    with open(f"data/{category_name}.csv", "w", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
                products,
                proteins,
                fats,
                carb,
                calories
            )
        )

    #Собираем данные о продуктах
    products_data = soup.find('table', class_='views-table sticky-enabled cols-6').find('tbody').find_all('tr')

    for prod_find in products_data:

        products_tds = prod_find.find_all('td')
        products_tds = products_tds[1:]

        title = products_tds[0].find('a').text
        proteins = products_tds[1].text
        fats = products_tds[2].text
        carb = products_tds[3].text
        calories = products_tds[4].text

        with open(f"data/{category_name}.csv", "a", encoding="utf-8-sig") as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                (
                    title,
                    proteins,
                    fats,
                    carb,
                    calories
                )
            )



