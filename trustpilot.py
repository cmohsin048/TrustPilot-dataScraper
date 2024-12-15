from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import time

# Initialize ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--disable-software-rasterizer')
options.add_argument('--disable-extensions')
options.add_argument('--disable-setuid-sandbox')
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(20)

try:
    # Navigate to the Trustpilot Salons & Clinics page
    driver.get('https://www.trustpilot.com/categories/salons_clinics')
    driver.maximize_window()

    # Find all div elements with the specified class
    div_elements = driver.find_elements(By.CSS_SELECTOR, ".paper_paper__1PY90.paper_outline__lwsUX.card_card__lQWDv.card_noPadding__D8PcU.styles_wrapper__2JOo2")

    # List to store hrefs
    hrefs = []

    # Loop through each div element to find the 'a' tag with the specified class and extract the href attribute
    for div in div_elements:
        try:
            a_tag = div.find_element(By.CSS_SELECTOR, ".link_internal__7XN06.link_wrapper__5ZJEx.styles_linkWrapper__UWs5j")
            href = a_tag.get_attribute('href')
            hrefs.append(href)
        except NoSuchElementException:
            # Skip if the 'a' tag is not found
            continue

    # Loop through each href to check for the <address> element inside the specified div
    for url in hrefs:
        driver.get(url)

        try:
            # Find the div with the specified class
            side_column_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, ".paper_paper__1PY90.paper_outline__lwsUX.card_card__lQWDv.card_noPadding__D8PcU.styles_sideColumnCard__eyHWa"
                ))
            )

            # Look for the <address> element inside the div
            try:
                address_element = side_column_div.find_element(By.TAG_NAME, "address")

                # Check for the <ul> element with the specified class
                try:
                    contact_info_ul = address_element.find_element(By.CSS_SELECTOR, ".styles_contactInfoElements__YqQAJ")

                    # Check for <li> elements with the specified class inside the <ul>
                    li_elements = contact_info_ul.find_elements(By.CSS_SELECTOR, ".styles_contactInfoElement__SxlS3")
                    if li_elements:
                        first_two_li_data = []

                        # Look for 'a' elements in the first two li elements
                        for i in range(min(2, len(li_elements))):
                            try:
                                a_element = li_elements[i].find_element(By.CSS_SELECTOR, ".link_internal__7XN06.typography_body-m__xgxZ_.typography_appearance-action__9NNRY.link_link__IZzHN.link_underlined__OXYVM")
                                first_two_li_data.append(a_element.get_attribute('href'))
                            except NoSuchElementException:
                                first_two_li_data.append(None)  # Append None if 'a' not found

                        # Check for ul element in the last li
                        try:
                            last_li_ul = li_elements[-1].find_element(By.CSS_SELECTOR, ".typography_body-m__xgxZ_.typography_appearance-default__AAY17.styles_contactInfoAddressList__RxiJI")

                            # Extract data from all li elements inside the last ul
                            last_li_data = []
                            inner_li_elements = last_li_ul.find_elements(By.TAG_NAME, "li")
                            for inner_li in inner_li_elements:
                                text = inner_li.text.replace('tel:', '').strip()  # Remove 'tel:' from numbers
                                last_li_data.append(text)

                            print("True")  # Last li ul found
                            print("First two li data:", first_two_li_data)
                            print("Data from last li ul:", last_li_data)
                        except NoSuchElementException:
                            print("False")  # Last li ul not found

                    else:
                        print("False")  # No li elements found

                except NoSuchElementException:
                    print("False")  # Address found but ul not found

            except NoSuchElementException:
                print("False")  # Address element not found

        except TimeoutException:
            print("Specified div not found on this page.")

finally:
    # Close the driver
    driver.quit()
