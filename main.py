from openai import OpenAI

OLLAMA_BASE_URL = 'http://localhost:11434/v1'
ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key="YoooSenpai")


firstQuestion="Pick a business area that might be worth exploring for an Agentic AI opportunity"
response = ollama.chat.completions.create(
    model="llama3.2",
    messages=[{"role": "user", "content": firstQuestion}]
)

firstAns=response.choices[0].message.content

secondQuestion = ollama.chat.completions.create(
    model="llama3.2",
    messages=[{"role":"user", "content":f"{firstAns}Present pain point of these industries - something challenging that might be ripe for an Agentic Solution"}]
)

secondAnswer=secondQuestion.choices[0].message.content

thirdQuestion = ollama.chat.completions.create(
    model="llama3.2",
    messages=[{"role":"user", "content": f"Propose the agentic AI solution for {secondAnswer}"}]
)

print(thirdQuestion.choices[0].message.content)