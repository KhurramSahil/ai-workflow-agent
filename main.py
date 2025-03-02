from langgraph.graph import StateGraph, END
from myagents.orchestrator import Orchestrator
from myagents.hubspot_agnet import HubSpotAgent
from myagents.email_agent import EmailAgent
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

# Define conditional edges
def route_after_orchestrator(state):
    if state.get("action_type") != "fallback":
        return "hubspot_agent"
    return "email_agent"

workflow.add_conditional_edges(
    "orchestrator",
    route_after_orchestrator,
    {
        "hubspot_agent": "hubspot_agent",
        "email_agent": "email_agent"
    }
)

workflow.add_edge("hubspot_agent", "email_agent")
workflow.add_edge("email_agent", END)
workflow.set_entry_point("orchestrator")


def handle_user_query(query):
    """Main workflow executor"""
    app = workflow.compile()
    result = app.invoke({"query": query})
    
    if result.get("email_sent", False) and result.get("hubspot_result", {}).get("success", False):
        print("✅ Successfully completed all operations")
    else:
        print("❌ Workflow completed with errors")
    
    return result

if __name__ == "__main__":
    sample_query = "add contact in hubspot with user333@gmail.com and name for this is Rehman, send notification email also"
    sample_query = "Send urgent email about to sahil for meeting"
    # sample_query = "Hi"
    result = handle_user_query(sample_query)
    print("\nWorkflow Result:")
    print(json.dumps(result, indent=2))