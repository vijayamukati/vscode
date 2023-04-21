import openai
import time
import gradio as gr
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# Set up OpenAI API
openai.api_key = "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"
engine_name = "davinci"

def gpt_output(message):
    response = openai.Completion.create(
        engine="davinci",
        prompt=message,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip() # type: ignore

def search_product():
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

    search_box = driver.find_element(By.XPATH,'/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div[1]/input')
    search_box.send_keys('laptop')
    search_button=driver.find_element(By.XPATH,"/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[3]/div/span/input")
    search_button.click()
    url=driver.find_element(By.CLASS_NAME,"a-section a-spacing-none puis-padding-right-small s-title-instructions-style")
    url.click() 
    
    add_to_cart_button = driver.find_element(By.ID,"add-to-cart-button")
    add_to_cart_button.click()

search_product()


# Function to interact with ChatGPT
def chat_gpt(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip() # type: ignore

# Function to create Gradio interface
def chatbot_interface():
    inputs = gr.inputs.Textbox(lines=2, label="Enter your query")
    outputs = gr.outputs.Textbox(label="ChatGPT")

    def chatbot(query):
        search_product()  # type: ignore
        time.sleep(5)
        prompt = "I need help buying a laptop"
        response = chat_gpt(prompt)
        return response
    title = "Chatbot to help buy a laptop"
    description = "Enter your query and let the chatbot assist you in buying a laptop on Amazon"
    return gr.Interface(chatbot, inputs, outputs, title=title, description=description)

# Launch Gradio interface
chatbot_interface().launch()
