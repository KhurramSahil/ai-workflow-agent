# main workflow

from langgraph.graph import StateGraph, END
from agents.orchestrator import Orchestrator
from agents.hubspot_agnet import HubSpotAgent
from agents.email_agent import EmailAgent
import json


workflow = StateGraph(dict)

def orchestrator_node(state):
    query = state["query"]
    orchestrator = Orchestrator()
    analysis = orchestrator.process_query(query)
    return {**state, **analysis}

def hubspot_node(state):
    hubspot_agent = HubSpotAgent()
    try:
        result = hubspot_agent.execute_operation(
            state["action_type"],
            state["hubspot_data"]
        )
    except ValueError as e:
        result = {
            "success": False,
            "error": f"Validation Error: {str(e)}",
            "details": state["hubspot_data"]
        }
    return {**state, "hubspot_result": result}

def email_node(state):
    email_agent = EmailAgent()
    success = email_agent.send_notification(
        state["email_subject"],
        state["email_body"]
    )
    return {**state, "email_sent": success}

# Build workflow
workflow.add_node("orchestrator", orchestrator_node)
workflow.add_node("hubspot_agent", hubspot_node)
workflow.add_node("email_agent", email_node)

# Define conditional routing
def route_after_orchestrator(state):
    """Determine next node based on action type"""
    action_type = state.get("action_type")
    if action_type == "contact_create":
        return "hubspot_agent"
    return "email_agent"  # Handles send_email and fallback

workflow.add_conditional_edges(
    "orchestrator",
    route_after_orchestrator,
    {
        "hubspot_agent": "hubspot_agent",
        "email_agent": "email_agent"
    }
)

# Define normal edges
workflow.add_edge("hubspot_agent", "email_agent")
workflow.add_edge("email_agent", END)
workflow.set_entry_point("orchestrator")


def handle_user_query(query):
    """Main workflow executor"""
    app = workflow.compile()
    result = app.invoke({"query": query})
    
    # Determine success based on action type
    action_type = result.get("action_type")
    email_success = result.get("email_sent", False)
    hubspot_success = result.get("hubspot_result", {}).get("success", False)
    
    if action_type == "contact_create":
        success = email_success and hubspot_success
    else:  # send_email or fallback
        success = email_success
    
    if success:
        print("✅ Successfully completed all operations")
    else:
        print("❌ Workflow completed with errors")
    
    return result

if __name__ == "__main__":
    # sample_query = "add contact in hubspot with user33443@gmail.com and name for this is Ali Rehman, send notification email also"
    sample_query = "Send urgent email for meeting"
    result = handle_user_query(sample_query)
    print("\nWorkflow Result:")
    print(json.dumps(result, indent=2))