# 🤖 Personal AI Task & Reflection Agent
### Google AI Agents Intensive — Capstone Project

## 📋 Executive Summary

The **Personal AI Task & Reflection Agent** is a sophisticated, production-ready AI assistant designed to help users manage their tasks and emotional well-being. Unlike standard chatbots, this agent is built on a robust **agentic architecture** that allows it to reason about user intent, maintain persistent context, execute specialized tools, and orchestrate sub-agents for complex problem-solving.

This project serves as a practical application of advanced AI concepts, demonstrating how to build a reliable, observable, and scalable AI system using Python and the Google Gemini API.

---

## 🏗️ System Architecture

The system is built on a modular, class-based architecture where a central agent orchestrates various specialized components. This design ensures separation of concerns, making the system easier to maintain and extend.

### 📂 File Function Overview (Starter Guide)

This table provides a quick overview of each file in the repository and its role, serving as a starter guide for navigating the project.

| File | Function |
| :--- | :--- |
| `personal_task_agent.py` | **Core Application Code.** The main entry point for the agent, containing the `PersonalTaskAgent`, `MemorySystem`, `ToolRegistry`, `LLMInterface`, and `ProductionAgent` classes. It orchestrates the entire interaction loop. |
| `agent_memory.db` | **Long-Term Memory.** An SQLite database generated at runtime to persist tasks, diary entries, user patterns, and conversation history across sessions. |
| `agent_logs.log` | **Activity & Error Logs.** A file generated at runtime that records detailed timestamped events, including tool executions, API calls, and errors for debugging. |
| `agent_metrics.json` | **Performance Metrics.** A JSON file generated on exit containing high-level session statistics like uptime, total events, and counts of different actions. |
| `simple_demo.py` | **Logic-Only Demo.** A script that demonstrates the agent's internal logic (like task creation) without requiring an API key, useful for basic verification. |
| `test_setup.py` | **Environment Checker.** A diagnostic script to verify the Python environment, installed libraries, and connectivity to the Google Gemini API. |
| `key_test.py` | **API Key Tester.** A minimal script designed specifically to test if a provided Google Gemini API key is valid and working. |
| `check_models.py` | **Model Lister.** A utility script that queries the Gemini API to list the models available for use with your specific API key. |
| `README.md` | **Documentation.** The file you are currently reading, providing a comprehensive overview, setup guide, and technical details of the project. |

### High-Level Architecture Diagram

The following diagram illustrates the primary components and their interactions. The User interacts with the `PersonalTaskAgent`, which acts as the central controller, coordinating with the LLM, Memory, and Tools.

> **[Insert High-Level Architecture Diagram Here]**
> *(Note: A diagram showing the User connected to the PersonalTaskAgent. The Agent is connected bi-directionally to the LLMInterface, ToolRegistry, and MemorySystem (which connects to SQLite). The ProductionAgent wraps the central Agent, and a MetricsCollector observes the whole system.)*

* **User:** The end-user interacting via a command-line interface.
* **PersonalTaskAgent (Main Controller):** The core logic that receives input, determines intent, and manages the overall conversation flow.
* **LLMInterface:** An abstraction layer for communication with the Google Gemini API.
* **ToolRegistry:** A central repository of executable functions (tools) that the agent can call.
* **MemorySystem:** Manages both short-term (in-memory) and long-term (SQLite database) context.
* **ProductionAgent (Wrapper):** Adds a layer of production features like rate limiting and caching around the main agent.
* **MetricsCollector & Logger:** Tracks system performance and logs events for observability.

---

## 🔄 Data Flow & Request Lifecycle

Understanding how a user's request is processed is key to grasping the agent's operation. The data flow follows a "reason-then-act" pattern.

### Request Processing Data Flow Diagram

This diagram shows the step-by-step journey of a user's input from ingestion to response generation.

> **[Insert Data Flow Diagram Here]**
> *(Note: A sequential diagram illustrating steps: 1. User Input -> 2. Intent Classification (Agent->LLM) -> 3. Tool Selection (Agent->Registry) -> 4. Tool Execution (Agent->Tool->Memory/Calc) -> 5. Response Generation (Agent->LLM) -> 6. Context Update (Agent->Memory) -> 7. Output to User.)*

1.  **Input:** The user provides a natural language query (e.g., "Create a task to finish my report by Friday").
2.  **Intent Classification:** The `PersonalTaskAgent` sends the input to the `LLMInterface`. The LLM analyzes the text and determines the user's intent (e.g., `create_task`).
3.  **Tool Selection:** Based on the determined intent, the agent consults the `ToolRegistry` to find the corresponding tool (e.g., `create_task_tool`).
4.  **Tool Execution:** The selected tool is executed. This may involve:
    * Extracting parameters from the user's input (using the LLM).
    * Interacting with the `MemorySystem` to store or retrieve data (e.g., adding a new row to the `tasks` table in SQLite).
    * Performing a calculation or analysis.
5.  **Response Generation:** The tool returns a result. The agent then formulates a final, natural language response to the user, often incorporating the tool's output.
6.  **Context Update:** The entire interaction (user input and agent response) is logged into the `MemorySystem` (both short-term list and long-term `conversations` table) to maintain context for future turns.
7.  **Output:** The final response is displayed to the user.

---

## 🧑‍💻 Technical Deep Dive: `personal_task_agent.py`

This file is the core of the application. It contains the primary class definitions that bring the agent to life. Below is a detailed breakdown of its key components.

### 1. `PersonalTaskAgent` Class (The Orchestrator)
* **Role:** The central "brain" of the system. It integrates all other components and manages the main interaction loop.
* **Key Method: `process_natural_language(self, user_input)`:** This is the critical intent classifier. It constructs a prompt for the LLM, asking it to categorize the user's input into a predefined set of intents (e.g., `create_task`, `ask_advice`). This is the first step in the "reasoning" process.
* **Key Method: `chat(self, user_input)`:** The primary public method. It coordinates the entire data flow described above: getting intent, finding the tool, executing it, and generating the final response.

### 2. `MemorySystem` Class (The Context Keeper)
* **Role:** Manages the agent's state across interactions.
* **Short-Term Memory:** Implemented as a Python list (`self.short_term_memory`) storing the last few interactions. This provides immediate context for follow-up questions.
* **Long-Term Memory:** Implemented using an **SQLite database** (`agent_memory.db`). This is crucial for persistence across sessions. The class defines and manages four relational tables:
    * `tasks`: Stores task details (title, priority, status, deadline).
    * `diary_entries`: Stores user reflections along with an AI-generated mood score.
    * `user_patterns`: A place to store learned user preferences over time.
    * `conversations`: A complete log of all user-agent turns.

### 3. `ToolRegistry` Class (The Capability Hub)
* **Role:** Implements the **Model Context Protocol (MCP)** pattern. It decouples the agent's reasoning ("what to do") from its execution ("how to do it").
* **Mechanism:** Uses a decorator (`@register_tool`) to register Python functions as tools. The agent's core logic doesn't need to know *how* a tool works, only its name. This makes adding new capabilities straightforward.

### 4. `LLMInterface` Class (The AI Interface)
* **Role:** An abstraction layer for the Google Gemini API.
* **Functionality:** It handles the initialization of the `genai.GenerativeModel`, manages API keys securely from environment variables, and provides a clean `generate_response` method that encapsulates the API call, error handling, and retry logic.

### 5. `MultiAgentOrchestrator` Class (The Delegator)
* **Role:** Demonstrates advanced multi-agent patterns.
* **Functionality:** For complex or specialized queries, the main agent can delegate to sub-agents. This class manages specialized agents like a `SchedulerAgent` (for time management) and a `MotivationalAgent`. A routing mechanism determines which sub-agent is best suited for a task.

### 6. `ProductionAgent` Class (The Robustness Layer)
* **Role:** A wrapper class that inherits from `PersonalTaskAgent` to add production-grade features.
* **Features:**
    * **Rate Limiting:** Implements checks to prevent abuse of the Gemini API.
    * **Caching:** Uses `functools.lru_cache` to store responses to identical queries, reducing API costs and latency.
    * **Health Checks:** Includes a method to verify the status of external dependencies like the database and API.

---

## 📂 Project File Structure

```text
ai-agents-capstone/
├── agent_logs.log          # Runtime activity and error logs (Generated on run)
├── agent_memory.db         # SQLite database for long-term memory (Generated on run)
├── agent_metrics.json      # JSON file for performance metrics (Generated on exit)
├── check_models.py         # Utility to list available Gemini models for your key
├── key_test.py             # Minimal utility to test API key validity
├── personal_task_agent.py  # CORE APPLICATION CODE - Main Agent Entry Point
├── README.md               # This documentation file
├── simple_demo.py          # Logic-only demo (runs without API key dependence)
└── test_setup.py           # Environment, library, and connection checker script
```

---

## 🛠️ Setup and Usage Guide

### 1. Prerequisites
* Python 3.8+
* Google Generative AI SDK (`pip install google-generativeai`)
* Google Gemini API key

### 2. API Key Configuration
* API Key is required for the project to work and connect with Google gemini. 
* Once the API key is generated, you can test it using key_test.py.
    ```text
    client = genai.Client(api_key="Insert API key")
    ```
* Once the test succeeds, you can place the values in the personal_task_agent.py 
    ```text
    os.environ["GEMINI_API_KEY"] = "Insert API Key"
    os.environ["GOOGLE_API_KEY"] = "Insert API Key"
    ```



### Running the Agent
1.  **Navigate to the project directory:**
    ```bash
    cd ai-agents-capstone
    ```
2.  **Run the main script:**
    ```bash
    python personal_task_agent.py
    ```
The agent will perform an initial self-test and demo routine, after which it will enter an interactive chat mode where you can issue natural language commands.

---

## 📊 Observability: Data and Metrics

The system is designed to be observable, providing insights into its operation and user interactions.

### Persistent Data (`agent_memory.db`)
You can inspect the SQLite database using any standard SQLite viewer. Key tables include:
* **`tasks`:** View all created tasks, their status, priorities, and deadlines.
* **`diary_entries`:** Read user reflections and analyze the AI-assigned mood scores (scale 1-5) to track emotional trends.

### Performance Metrics (`agent_metrics.json`)
After each session, a metrics summary is written to this JSON file. It includes data points such as:
* **`uptime_hours`**: Total duration of the session.
* **`total_events`**: The aggregate count of recorded actions.
* **`event_types`**: A breakdown of specific actions (e.g., `{"chat_interaction": 5, "task_created": 2}`).

### Activity Logs (`agent_logs.log`)
This file contains a detailed log of all actions being performed.
