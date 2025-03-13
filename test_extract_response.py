import json

# Sample response from the API
sample_response = """{"request_id":"d70ef67f-98c3-42fa-a7a0-01c24bc2c1b6","response":"<think>\\nOkay, let's tackle this query. The user received an email from Benedek with the subject \\"teszt\\" (which means \\"test\\" in Hungarian) and the body is a simple message asking if the assistant can reply. The task is to draft a response based on the provided documents, using only the information available there.\\n\\nFirst, I need to check if there's any relevant information in the documents that can help answer this. The user mentioned that if the info isn't available, the response should state that they can't help and an agent will follow up. Since the original email is a test and doesn't ask for specific information, there's likely no data in the documents to address it. \\n\\nThe assistant's response needs to be in Hungarian, as the sender's email is from a Hungarian domain and the message is in Hungarian. The greeting should be appropriate, maybe \\"Kedves Benedek,\\". The body should mention that they can't help based on the current information and that an agent will contact them soon. Also, include the standard signature with Gergő Krucsai and SMP Solution. Make sure to use <br> tags for line breaks as specified.\\n</think>\\n\\nKedves Benedek,<br><br>Köszönjük üzenetét! Jelenlegi információink alapján sajnos nem tudunk konkrét válasszal szolgálni. Kollégánk hamarosan felveszi Önnel a kapcsolatot.<br><br>Üdvözlettel,<br>Gergő Krucsai<br>SMP Solution","status":"success","timestamp":"2025-03-13T11:29:04.252444"}"""

# Parse the JSON
response_data = json.loads(sample_response)

# Extract the response text
response_text = response_data["response"]

# Clean the response by removing the thinking section
def clean_response(response):
    if "<think>" in response and "</think>" in response:
        think_end = response.find("</think>") + len("</think>")
        return response[think_end:].lstrip()
    return response

# Apply the cleaning function
cleaned_response = clean_response(response_text)

# Print the results
print("=== Original Response ===")
print(response_text)
print("\n=== Cleaned Response ===")
print(cleaned_response)

# Create the Power Automate expression
power_automate_expr = """if(contains(body('HTTP')['response'], '<think>') && contains(body('HTTP')['response'], '</think>'),
   substring(body('HTTP')['response'], 
             indexOf(body('HTTP')['response'], '</think>') + 8,
             length(body('HTTP')['response'])),
   body('HTTP')['response'])"""

print("\n=== Power Automate Expression ===")
print(power_automate_expr)
