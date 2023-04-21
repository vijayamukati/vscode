import os
import openai
import requests
import re
import gradio as gr
import time

openai.api_key ="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" 
prompt="The following is a conversation with an AI assistant"


def ask_gpt(prompt):
    response = openai.Completion.create(
        engine="davinci", # Replace with the engine of your choice
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )

    answer = response.choices[0].text
    answer = re.sub('[^0-9a-zA-Z\n\.\?\!]+', ' ', answer) # Remove special characters
    return answer.strip()

def gpt_output(message,state):
    prompt = f"Human: {message}\nChatbot:"
    response = ask_gpt(prompt)
    state["chat_history"] += f"\n\n{message}\n{response}"
    return response, state["chat_history"]

block = gr.Interface(
    fn=gpt_output,
    inputs=[gr.inputs.Textbox(placeholder="Type your message here...")],
    outputs=[gr.outputs.Textbox(label="Chatbot")],
    title="Chish AGI",
    description="A chatbot powered by OpenAI's GPT-3.5",
    allow_flagging=False,
    layout="vertical",
    theme="compact",
)

block.launch(debug=True)


