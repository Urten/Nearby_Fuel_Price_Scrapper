from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from geocoder import get_name_by_coordinates
from cache_mongodb import MongoDB


def crawler_indian_oil(lat: float | int, lon: float | int, driver: any):
    """
    """

    # driver = driver

    data = []
    elem = []
    petrol_prices = []
    diesel_prices = []
    pump_addresses: str = []
    pump_names: str = []

    try:
        '''Caching the addresss with the latitude and longitude data'''
        m = MongoDB("latitdue_longitude_of_the_address")
        res = m.search_one({'latitude': lat,
                            'longitude': lon})
        if res is not None:
            addr_name = res["address"]
        else:
            addr_name = get_name_by_coordinates(lat=lat,
                                                lon=lon)
            m.post({'latitude': lat,
                    'longitude': lon, "address": addr_name})
    except Exception as e:
        print(e)

    driver.get("https://associates.indianoil.co.in/PumpLocator/")

    element = Select(driver.find_element(
        By.XPATH, '/html/body/div[3]/div[1]/table/tbody/tr/td[1]/div/div[1]/select'))

    element.select_by_value('MS')

    driver.find_element(
        By.XPATH, '/html/body/div[3]/div[1]/table/tbody/tr/td[1]/div/div[1]/input[1]').send_keys(addr_name)

    locate_pump_btn = driver.find_element(
        By.XPATH, '/html/body/div[3]/div[1]/table/tbody/tr/td[1]/div/div[2]/input[2]')

    locate_pump_btn.click()
    try:
        # table = driver.find_element(By.XPATH,
        #                             '/html/body/div[3]/div[2]/table/tbody')
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[3]/div[2]/table/tbody')))

    except NoSuchElementException:
        return print("Location error, Servers too busy. Please try after sometime. ")

    sub_child_elems = table.find_elements(
        By.XPATH, "*")

    for child in sub_child_elems:
        elem.append(child.tag_name)

    i = 2

    while len(elem) >= i:
        petrol_price = driver.find_element(
            By.XPATH, f'/html/body/div[3]/div[2]/table/tbody/tr[{i}]/td[7]')

        diesel_price = driver.find_element(
            By.XPATH, f'/html/body/div[3]/div[2]/table/tbody/tr[{i}]/td[8]')

        pump_address = driver.find_element(
            By.XPATH, f'/html/body/div[3]/div[2]/table/tbody/tr[{i}]/td[5]')
        pump_name = driver.find_element(
            By.XPATH, f'/html/body/div[3]/div[2]/table/tbody/tr[{i}]/td[4]')

        petrol_prices.append(petrol_price.text)
        diesel_prices.append(diesel_price.text)
        pump_addresses.append(str(pump_address.text))
        pump_names.append(str(pump_name.text))

        i += 1

    for u in range(len(pump_names)):
        data.append({
            "pump_name": pump_names[u],
            "pump_address": pump_addresses[u],
            "petrol_price": petrol_prices[u],
            "diesel_price": diesel_prices[u]
        })

    return data
