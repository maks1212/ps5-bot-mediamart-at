from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from twilio.rest import Client

# Thanks to  twissmueller for the basic
# Production specific settings like delays ...
isProduction = True
useTwillio = True

productToBuy = "https://www.mediamarkt.at/de/product/_sony-playstation®5-digital-1797340.html"
mmUsername = "Medimarkt Username"
mmPassword = "Media Markt Passwort"

# only necessary if you are using twillio, important don't forget + in front of the phone numbers
twillioAccountSid = "Twillio Sid"
twillioAuthToken = "Twillio Auth Token"
twillioAcoountPhonenumber = "+ Twillio Phone Number"
twillioMessageBody = "Playstation 5 ist im Warenkorb!"
receiverPhoneNumber = "+ Your Phone Number"

webdriverChromePath = "/Users/MYUSERNAME/Desktop/chromedriver"

def click_button(button_text):
    try:
        element = driver.find_element(By.XPATH, f'//button[text()="{button_text}"]')
        driver.execute_script("arguments[0].click();", element)
        time.sleep(3)
        return True
    except NoSuchElementException:
        return False


def login_mms(username, password):
    driver.find_element_by_id("mms-login-form__email").send_keys(username)
    driver.find_element_by_id("mms-login-form__password").send_keys(password)
    driver.find_element_by_id("mms-login-form__login-button").click()

def send_sms():
    account_sid = twillioAccountSid
    auth_token = twillioAuthToken
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=twillioMessageBody,
        from_=twillioAcoountPhonenumber,
        to=receiverPhoneNumber
    )
    print(message.sid)


options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(webdriverChromePath, options=options)
driver.maximize_window()
driver.get(productToBuy)

while True:
    click_button("Alles zulassen")
    if isProduction:
        time.sleep(30)
    if click_button("In den Warenkorb"):
        break
    driver.refresh()
click_button("Nein, danke")
click_button("Zum Warenkorb")
click_button("Zur Kasse gehen")
login_mms(mmUsername, mmPassword)
time.sleep(3)
if useTwillio:
    send_sms()
