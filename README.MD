# AI-Powered Autonomous Workflow Agent

This project implements an AI-powered autonomous agent system designed to automate workflows involving CRM operations (using HubSpot) and email notifications. The solution is built using a multi-agent approach with a global orchestrator, a HubSpot agent, and an Email agent. The architecture leverages LangGraph for agent orchestration.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Configuration](#configuration)
- [Usage](#usage)
- [Error Handling](#error-handling)
- [Project Structure](#project-structure)
- [License](#license)

## Overview

This autonomous agent system receives a user query, delegates tasks to the appropriate agents, interacts with HubSpot to check or create leads, and sends email notifications to confirm actions. The agents use function calling to interact with external APIs (HubSpot, Email, and OpenAI/Groq for query processing).

## Architecture

- **Global Orchestrator Agent:**  
  Analyzes user queries and delegates tasks to the appropriate agent based on intent.  
  _Technologies:_ LangGraph, Groq API

- **HubSpot Agent:**  
  Interacts with the HubSpot CRM to check for and create contacts (leads).  
  _Technologies:_ HubSpot Python SDK

- **Email Agent:**  
  Sends email notifications confirming operations.  
  _Technologies:_ SMTP (with Python's `smtplib`)

- **Workflow Orchestration:**  
  The system uses LangGraph to manage the flow. Based on the orchestrator’s analysis, the workflow either calls the HubSpot agent (for contact creation) or directly proceeds with the email notification.

## Features

- **Multi-Agent Design:**  
  Uses separate modules for orchestration, HubSpot CRM operations, and email notifications.
  
- **Function Calling:**  
  Agents call functions in a structured manner to perform specific operations.
  
- **Configuration Management:**  
  All API keys and credentials are stored in a JSON configuration file.
  
- **Error Handling:**  
  The system gracefully handles errors (e.g., missing data, API failures) with try/except blocks and fallback responses.

## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/ai-workflow-agent.git
   cd ai-workflow-agent

2. **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
4. **Configure API Keys and Credentials:**
Create a config/config.json file with the following structure:
    ```json
    {
  "email": {
    "sender_email": "your_sender@example.com",
    "receiver_email": "your_receiver@example.com",
    "smtp_server": "smtp.example.com",
    "smtp_port": 587,
    "username": "your_smtp_username",
    "password": "your_smtp_password"
  },
  "hubspot": {
    "access_token": "your_hubspot_access_token"
  },
  "groq": {
    "api_key": "your_groq_api_key"
  }
}





