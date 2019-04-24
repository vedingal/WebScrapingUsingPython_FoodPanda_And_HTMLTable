import requests
from bs4 import BeautifulSoup
import pandas as pd

# Creates a list of web pages per geo location
GeoLocation_Link = [
    'https://www.bpicards.com/RealThrills/Details/8833' # Metro North
    , 'https://www.bpicards.com/RealThrills/Details/8834' # Metro South
    , 'https://www.bpicards.com/RealThrills/Details/8835' # North Luzon
    , 'https://www.bpicards.com/RealThrills/Details/8836' # South Luzon
    , 'https://www.bpicards.com/RealThrills/Details/8837' # Visayas
    , 'https://www.bpicards.com/RealThrills/Details/8838' # Mindanao
]

# Sets up variables for later use
GeoLocation_Name_Counter = 1 # Fixed at '1' specifically because of the website code pattern
Store_Records = []

# Creates a loop that will go through the GeoLocation_Link[] list
for i in range(len(GeoLocation_Link)):

    # Gets all web link content
    request = requests.get(GeoLocation_Link[i])
    soup = BeautifulSoup(request.text, 'html.parser')

    # Based on the code pattern, the geo location name is located at the 2nd HTML section that has the 'h1' tag.
    # Hence, initially setting the GeoLocation_Name_Counter variable to '1'. This also tells us that the data we ineed
    # is in the 'span' child tag of the 2nd 'h1' tag. We can get the actual geo location name value by extracting the
    # text from the 'span' tag.     # It is also a fact that there's only one geo location name per page.
    Geolocation_Name = soup.find_all('h1')[GeoLocation_Name_Counter].find('span').text

    # Class names 'x167' and 'x168' are from the website code
    # Once again, based on the website code pattern, it can be observed that only the first page on the list
    # (https://www.bpicards.com/RealThrills/Details/8833) has the 'x167' class name for its stores. Other pages use
    # 'x168' as class names.
    if i == 0:
        Store_Names = soup.find_all('td', attrs={'class':'xl67'})
    else:
        Store_Names = soup.find_all('td', attrs={'class': 'xl68'})

    # This part loops through all the store names found fom the code above and appends each store name as an entry to
    # the Store_Records[] list.
    for j in range(len(Store_Names)):
        Store_Name = Store_Names[j].find('span').text.replace("   ", " ")
        Store_Records.append((Geolocation_Name, Store_Name))

# Before we can extract our GeoLocation_Name and Store_Name records, we must put them first into a Data Frame.
df = pd.DataFrame(Store_Records, columns=['Geolocation','Store_Name'])

# This exports the data set to a .CSV file into your work folder
df.to_csv('JFC_Store.csv', index=False, encoding='utf-8')

