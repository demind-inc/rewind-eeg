from openai import OpenAI
import config

"""
categorize screenshot summary into deep and shallow work
"""
client = OpenAI(
    api_key=config.api_key
)

"""
test openai categorization

params: categories
output: categorized event titles
"""
def categorize(summary, categories=["deep", "shallow", "not"]):
    category = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "user", "content": f"Categorize this event: {summary} as {categories[0]} or {categories[1]} or {categories[2]} work."}
        ]
    )
    response = category.choices[0].message
    print(response)
    resp = simplify_response(str(response).lower(), categories)
    return resp

"""
simplify chatgpt text output

params: completion output, category titles
output: simplified output of chatgpt output (social, personal, work)
"""
def simplify_response(response, nl_categories):
    for category in nl_categories:
        if response.__contains__(category):
            return category
    return None

if __name__ == "__main__":
    sum = "software development"
    print(categorize(sum))