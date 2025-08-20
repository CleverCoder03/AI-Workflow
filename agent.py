from dotenv import load_dotenv
from openai import OpenAI
# from IPython.display import Markdown, display

load_dotenv(override=True)

openai = OpenAI()

firstQuestion="Pick a business area that might be worth exploring for an Agentic AI opportunity"
response = openai.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": firstQuestion}]
)

firstAns=response.choices[0].message.content

secondQuestion = openai.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[{"role":"user", "content":f"{firstAns}Present pain point of these industries - something challenging that might be ripe for an Agentic Solution"}]
)

secondAnswer=secondQuestion.choices[0].message.content

thirdQuestion = openai.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role":"user", "content": f"Propose the agentic AI solution for {secondAnswer}"}]
)

conclusion = thirdQuestion.choices[0].message.content
print(conclusion)
# display(Markdown(conclusion))