import gradio as gr
import openai
import re
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up OpenAI API key
openai.api_key = "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"

def search_house(location, family_size):
    # Use Selenium to navigate to real estate website and search for houses in given location
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get('https://www.realtor.com/')
    search_box = driver.find_element(By.NAME, "location")
    search_box.send_keys(location)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)
    family_size_box = driver.find_element(By.ID, "sqftSelect")
    family_size_box.click()
    family_size_option = driver.find_element(By.XPATH, f"//option[text()='{family_size}']")
    family_size_option.click()
    time.sleep(3)
    results = driver.find_elements(By.CLASS_NAME, "jsx-4070371813")
    result_texts = [result.text for result in results]
    return result_texts

def ask_gpt(prompt):
    # Use OpenAI's GPT-3.5 to generate a response based on the user's search criteria
    response = openai.Completion.create(
        engine="davinci-2",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )

    answer = response.choices[0].text # type: ignore
    return answer.strip()

def gpt_output(location, family_size, state):
    # Search for houses using Selenium
    results = search_house(location, family_size)
    if len(results) == 0:
        response = "Sorry, no results found."
    else:
        # Generate a personalized response using OpenAI's GPT-3.5
        prompt = f"I'm looking for a house for a family of {family_size} in {location}. Can you help me?\nResults:\n" + "\n".join(results)
        response = ask_gpt(prompt)
    state["chat_history"] += f"\n\nI'm looking for a house for a family of {family_size} in {location}.\n{response}"
    return response, state["chat_history"]

# Create the Gradio interface
def new_func():
    return False

block = gr.Interface(
fn=gpt_output,
inputs=[
gr.inputs.Textbox(label="Location"),
gr.inputs.Number(label="Family Size")
],
outputs=[gr.outputs.Textbox(label="Chatbot")],
title="Find a House for Your Family",
description="Get personalized recommendations for houses in your desired location and for your family size using OpenAI's GPT-3.5.",
layout="vertical",
theme="compact",                       
)

# Launch the interface
block.launch() # type: ignore
