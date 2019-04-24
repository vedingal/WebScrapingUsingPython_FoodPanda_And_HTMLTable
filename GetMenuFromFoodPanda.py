import requests
from bs4 import BeautifulSoup
import pandas as pd

# get html contents of website
r = requests.get('https://www.foodpanda.ph/chain/cg0ep/jollibee')
soup = BeautifulSoup(r.text, 'html.parser')

# get category details
results_categories = soup.find_all('ul', attrs={'class':'dish-list'})
print('Qty of Categories:' + str(len(results_categories)))

category_counter = 0
item_counter = 0
SKU_counter = 0
JFC_Menu_Records = []

# go through all categories
for category_counter in range(len(results_categories)):
    item_list = results_categories[category_counter].find_all('li', attrs={'class':''})

    # go through all items per category
    for item_counter in range(len(item_list)):
        item_code = item_list[item_counter].find('div')['data-product-id']
        item_name = item_list[item_counter].find('span').text
        item_price = item_list[item_counter].find('span', attrs={'class': 'price p-price'}).text\
            .replace(" ", "").replace('\n₱', '').replace('\nfrom₱', '').replace('\n', '')
        item_category = item_list[item_counter].find('div')['data-menu-category']
        try:
            item_img_url = item_list[item_counter].find('picture').find('div')['data-src'].replace("?width=302", "")
        except AttributeError:
            item_img_url = 'NULL'

        # add each line item to a record
        JFC_Menu_Records.append((item_code,item_category,item_name,item_price,item_img_url))
        SKU_counter = SKU_counter + 1
        '''
        print('\n' + str(item_counter))
        print(item_code)
        print(item_category)
        print(item_name)
        print(item_price)
        print(item_img_url)
        print(SKU_counter)(
        '''

# add records to a data frame then export to csv
df = pd.DataFrame(JFC_Menu_Records
        , columns=['Item_Code', 'Item_Category', 'Item_Name', 'Item_Price', 'Item_Img_URL'])
df.to_csv('JFC_Menu.csv', index=False, encoding='utf-8')






