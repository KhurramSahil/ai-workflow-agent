import json
from groq import Groq



def load_config():
    with open('config/config.json', 'r') as f:
        return json.load(f)

config = load_config()

# Initialize clients
groq_client = Groq(api_key=config['groq']['api_key'])


class Orchestrator:
#     def process_query(self, query):
#         """Analyze query and determine required actions"""
#         # In Orchestrator class
#         prompt = f"""Analyze the following user query and generate HubSpot parameters accordingly:
#         {query}
#         if user intent is about tpo create contact:
#         Return the output in JSON format with the following keys:
#         - 'action_type': (e.g., contact_create)
#         - 'email_subject': (A subject line for an email)
#         - 'email_body': (The content of the email in passonate way like welcome etc and this mail is auto genrated do not reply this email)
#         - 'Best Regards': (XYZ Company)
#         - 'hubspot_data': {{
#             "properties": {{
#                 "firstname": (First name extracted or generated),
#                 "lastname": (Last name extracted or generated),
#                 "email": (Email extracted or generated)
#             }}
#         }}"""


        
#         try:
#             completion = groq_client.chat.completions.create(
#                 model="llama-3.3-70b-versatile",
#                 messages=[{"role": "user", "content": prompt}],
#                 temperature=0.6,
#                 max_tokens=1024,
#                 top_p=0.95,
#                 response_format={"type": "json_object"}
#             )
            
#             response = json.loads(completion.choices[0].message.content)
#             return response
            
#         except Exception as e:
#             print(f"Orchestrator error: {e}")
#             return {
#                 "action_type": "fallback",
#                 "email_subject": "Action Confirmation",
#                 "email_body": f"We've received your request: {query}",
#                 "hubspot_data": {}
#             }

    def process_query(self, query):
        """
        Analyze the query and determine the required actions based on user intent.

        Cases:
        1. If the intent is to create a contact, add a contact, or create a lead:
        - Return a JSON with:
            - "action_type": (e.g., "contact_create")
            - "email_subject": A subject line for an email.
            - "email_body": A passionate welcome message (auto-generated; do not reply).
            - "Best Regards": "XYZ Company"
            - "hubspot_data": {
                    "properties": {
                        "firstname": (First name extracted or generated),
                        "lastname": (Last name extracted or generated),
                        "email": (Email extracted or generated)
                    }
            }
        2. If the intent is to send an email:
        - Return a JSON with:
            - "email_subject": (Email subject)
            - "email_body": (Email content)
        """

        prompt = f"""Analyze the following user query and generate parameters accordingly:
    Query: {query}

    Instructions:
    1. If the user's intent is to create a contact, add a contact, or create a lead, return a JSON object with:
    - "action_type": "contact_create"
    - "email_subject": A subject line for an email.
    - "email_body": A passionate welcome message (note that this email is auto-generated and no replies are monitored).
    - "Best Regards": "XYZ Company"
    - "hubspot_data": {{
            "properties": {{
                "firstname": (extracted or generated first name),
                "lastname": (extracted or generated last name),
                "email": (extracted or generated email)
            }}
    }}
    2. If the user's intent is solely to send an email, return a JSON object with:
    - "action_type": "send_email"
    - "email_subject": A subject line for an email.
    - "email_body": A passionate welcome message (note that this email is auto-generated and no replies are monitored).
    - "Best Regards": "XYZ Company"
    """

        try:
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=1024,
                top_p=0.95,
                response_format={"type": "json_object"}
            )
            response = json.loads(completion.choices[0].message.content)
            return response

        except Exception as e:
            print(f"Orchestrator error: {e}")
            # Fallback response if an error occurs
            return {
                "action_type": "fallback",
                "email_subject": "Action Confirmation",
                "email_body": f"We've received your request: {query}",
                "hubspot_data": {}
            }
