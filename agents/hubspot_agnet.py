import json
import hubspot
from hubspot.crm.contacts import (
    SimplePublicObjectInputForCreate,
    PublicObjectSearchRequest,
    ApiException
)

def load_config():
    with open('config/config.json', 'r') as f:
        return json.load(f)

config = load_config()

# Initialize client
hubspot_client = hubspot.Client.create(access_token=config['hubspot']['access_token'])



class HubSpotAgent:
    def execute_operation(self, action_type, data):
        """Execute HubSpot operations with proper formatting"""
        try:
            if action_type == "contact_create":
                # Convert array format to dictionary if needed
                properties = data.get("properties", {})
                if isinstance(properties, list):
                    properties = {item["property"]: item["value"] for item in properties}
                
                return self.create_contact(properties)
        except ApiException as e:
            return self._handle_api_exception(e)
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_contact(self, properties):
        """Create contact with validated properties"""
        required_fields = ["email"]
        for field in required_fields:
            if field not in properties:
                raise ValueError(f"Missing required field: {field}")
        
        contact_input = SimplePublicObjectInputForCreate(properties=properties)
        response = hubspot_client.crm.contacts.basic_api.create(
            simple_public_object_input_for_create=contact_input
        )
        return {
            "success": True,
            "id": response.id,
            "properties": response.properties
        }


    def _handle_api_exception(self, e):
        """Handle HubSpot API exceptions"""
        error_details = {
            "status": e.status,
            "reason": e.reason,
            "body": json.loads(e.body) if e.body else {}
        }
        return {
            "success": False,
            "error": "HubSpot API Error",
            "details": error_details
        }