import json
import os
from openai import OpenAI
# from google import genai
# from google.genai import types
from dotenv import load_dotenv

load_dotenv(override=True)

# BASE URL
GOOGLE_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
OLLAMA_BASE_URL="http://localhost:11434/v1"

# API KEYS
google_api_key= os.getenv('GEMINI_API_KEY')
ollama_api_key= os.getenv('OLLAMA_API_KEY')

#MODELS
questionModel="gpt-4o-mini"

firstAnswerModel="gpt-4.1-nano"
secondANswerModel="llama3.2"
thirdAnswerModel="gemini-2.0-flash"
fourthAnswerModel="gpt-4.1-mini"

judgeModel="gpt-4o-mini"

request = "Please come up with a challenging, nuanced question that I can ask a number of LLMs to evaluate their intelligence. "
request += "Answer only with the question, no explanation."
messages = [{"role": "user", "content": request}]

openai = OpenAI()
response = openai.chat.completions.create(
    model=questionModel,
    messages=messages
)

question = response.choices[0].message.content
print(question)

competitors=[]
answers=[]
messages=[{"role":"user", "content": question}]

response=openai.chat.completions.create(
    model=firstAnswerModel,
    messages=messages
)

answer=response.choices[0].message.content
print(answer)
competitors.append(firstAnswerModel)
answers.append(answer)

ollama= OpenAI(base_url=OLLAMA_BASE_URL, api_key=ollama_api_key)
response = ollama.chat.completions.create(
    model=secondANswerModel,
    messages=messages
)

answer=response.choices[0].message.content
print(answer)
competitors.append(secondANswerModel)
answers.append(answer)


gemini= OpenAI(base_url=GOOGLE_BASE_URL, api_key=google_api_key)
response=gemini.chat.completions.create(
    model=thirdAnswerModel,
    messages=messages
)
# gemini=genai.Client()
# response=gemini.models.generate_content(
#     model=thirdAnswerModel,
#     contents=messages,
#     config=types.GenerateContentConfig(
#         thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
#     )
# )

answer=response.choices[0].message.content
print(answer)
# answer=response.text
competitors.append(thirdAnswerModel)
answers.append(answer)


response=openai.chat.completions.create(
    model=fourthAnswerModel,
    messages=messages
)

answer=response.choices[0].message.content
print(answer)
competitors.append(fourthAnswerModel)
answers.append(answer)

print(competitors)
print(answers)


for competitor,answer in zip(competitors,answers):
    print(f"Competitors: {competitor}\n\n{answer}")

together=""
for index,answer in enumerate(answers):
    together+=f"# Response from competitor {index+1}\n"
    together+= answer + "\n\n"

judge = f"""You are judging a competition between {len(competitors)} competitors.
Each model has been given this question:

{question}

Your job is to evaluate each response for clarity and strength of argument, and rank them in order of best to worst.
Respond with JSON, and only JSON, with the following format:
{{"results": ["best competitor number", "second best competitor number", "third best competitor number", ...]}}
Answer only the number for example
{{"results": ["1", "4", "3", ...]}}

Here are the responses from each competitor:

{together}

Now respond with the JSON with the ranked order of the competitors, nothing else. Do not include markdown formatting or code blocks."""


judge_answer = [{"role":"user", "content": judge}]

response = openai.chat.completions.create(
    model=judgeModel,
    messages=judge_answer
)

results=response.choices[0].message.content
print(results)

result_dict=json.loads(results)
ranks = result_dict["results"]
for index, result in enumerate(ranks):
    competitor = competitors[int(result)-1]
    print(f"Rank {index+1}: {competitor}")
