import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

function_descriptions = [
    {
        "name": "extract_info_from_email",
        "description": "categorise & extract key info from an email, such as use case, company name, contact details, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "company_name": {
                    "type": "string",
                    "description": "name of the company that sent the email"
                },
                "use_case": {
                    "type": "string",
                    "description": "the purpose & use case of this this company's enquiry"
                },
                "product": {
                    "type": "string",
                    "description": "the product that the company is interested in"
                },
                "amount": {
                    "type": "string",
                    "description": "the amount of the product that the company is interested in, just calculate the total amount of the product, e.g. 100, 1203, etc."
                },
                "priority": {
                    "type": "string",
                    "description": "try to give a priority score to this email, based on how likely this email will lead to a good business opportunity, from 0 to 10"
                },
                "category": {
                    "type": "string",
                    "description": "categorise this email into one of the following categories: sales, support, partnership, spam, other"
                },
                "next_action": {
                    "type": "string",
                    "description": "what is the next action to take for this email? e.g. reply, forward, archive, delete, etc."
                }
            },
            "required": ["company_name", "use_case", "priority", "category", "next_action"]
        }
    }
]

class Email(BaseModel):
    from_email: str
    content: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def analyse_email(email: Email):
    content = email.content
    query = f'Please extract the key info from this email:{content}'
    messages = [{"role": "user", "content": query}]
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-0613",
        messages = messages,
        functions = function_descriptions,
        function_call = "auto"
    )

    arguments = response.choices[0]["message"]["function_call"]["arguments"]
    company_name = eval(arguments).get("company_name")
    use_case = eval(arguments).get("use_case")
    priority = eval(arguments).get("priority")
    product = eval(arguments).get("product")
    amount = eval(arguments).get("amount")
    category = eval(arguments).get("category")
    next_action = eval(arguments).get("next_action")

    return {
        "company_name": company_name,
        "use_case": use_case,
        "priority": priority,
        "product": product,
        "amount": amount,
        "category": category,
        "next_action": next_action
    }
