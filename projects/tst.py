#Api key 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

import os
import openai
import gradio as gr
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
openai.api_key ="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" 

# Replace with the path to your chromedriver.exe file
driver = webdriver.Chrome("chromedriver.exe")
# Navigate to the Amazon website
driver.get('https://www.amazon.in')
           

signin=driver.find_element(By.XPATH,"/html/body/div[1]/header/div/div[1]/div[3]/div/a[2]")
signin.click()
email=driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/form/div/div/div/div[1]/input[1]')
email.send_keys("vijaya.gurjar@gmail.com")
continuebutton=driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/form/div/div/div/div[2]/span/span/input')
continuebutton.click()

pwd=driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div/form/div/div[1]/input')
pwd.send_keys("magpie@1234")
signin_button=driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div/form/div/div[2]/span/span/input')
signin_button.click()


# Find the search box and enter a search query
search_box = driver.find_element(By.XPATH,'/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div[1]/input')
search_box.send_keys('laptop')
search_button=driver.find_element(By.XPATH,"/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[3]/div/span/input")
search_button.click()
url=driver.find_element(By.CLASS_NAME,"a-section a-spacing-none puis-padding-right-small s-title-instructions-style")
url.click()
driver.implicitly_wait(10)
# Find the add-to-cart button and click on it
add_to_cart_button = driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div[5]/div[3]/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div[2]/div/div[2]/div/form/div/div/div[33]/div[1]/span/span/span/input")
add_to_cart_button.click()
driver.implicitly_wait(10)
# Find the "Proceed to checkout" button and click on it
proceed_to_checkout_button = driver.find_element(By.XPATH,"/html/body/div[4]/div[3]/div[3]/div/div[1]/div[3]/div[1]/div[2]/div[3]/span/span/input")
proceed_to_checkout_button.click()

useadd=driver.find_element(By.XPATH,"/html/body/div[5]/div[1]/div/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div[2]/span/span/span/span/input")
useadd.click()
#here you can now add you details and proceed..................for security purpose markdown this
# Fill out the checkout form with your information
# name_box = driver.find_element_by_id('enterAddressFullName')
# name_box.send_keys('Deepak mukati')
# address_box = driver.find_element_by_id('enterAddressAddressLine1')
# address_box.send_keys('123 Main St')
# city_box = driver.find_element_by_id('enterAddressCity')
# city_box.send_keys('Anytown')
# state_box = driver.find_element_by_id('enterAddressStateOrRegion')
# state_box.send_keys('CA')
# zip_box = driver.find_element_by_id('enterAddressPostalCode')
# zip_box.send_keys('12345')
# phone_box = driver.find_element_by_id('enterAddressPhoneNumber')
# phone_box.send_keys('555-555-5555')
# continue_button = driver.find_element_by_name('shipToThisAddress')
# continue_button.click()

# # Wait for the payment page to load
# time.sleep(5)

# # Enter your payment information and complete the purchase
# # (Note: this is just an example and should not be used with real payment information)
# card_box = driver.find_element_by_id('addCreditCardNumber')
# card_box.send_keys('1234 5678 9012 3456')
# expire_box = driver.find_element_by_id('ccMonth')
# expire_box.send_keys('01')
# expire_box = driver.find_element_by_id('ccYear')
# expire_box.send_keys('23')
# cvv_box = driver.find_element_by_id('addCreditCardVerificationNumber')
# cvv_box.send_keys('123')
# place_order_button = driver.find_element_by_id('placeYourOrder')
# place_order_button.click()

# # Wait for the order confirmation page to load
# time.sleep(5)

prompt=" The following ia a conversation with an AI assistant"

def gpt_output(message):
    response = openai.Completion.create(
        engine="davinci",
        prompt=message,
        max_tokens=1024,
        n=1,
        stop=None,
    
    )
    return response.choices[0].text.strip() # type: ignore

block=gr.Blocks()

with block:
    gr.Markdown("""<h1><center>Chish AGI</center></h1>""")
    chatbot=gr.Chatbot()
    message=gr.Textbox(placeholder=prompt)
    state=gr.State() # type: ignore
    submit=gr.Button("SEND")
    submit.click(gpt_output,inputs=[message,state],outputs=[chatbot,state]) # type: ignore
block.launch(debug=True)



