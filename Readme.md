{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;\f1\fnil\fcharset0 Menlo-Bold;\f2\fnil\fcharset0 Menlo-Italic;
}
{\colortbl;\red255\green255\blue255;\red0\green0\blue255;\red255\green255\blue254;\red0\green0\blue0;
\red0\green0\blue117;\red15\green112\blue1;\red144\green1\blue18;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c100000;\cssrgb\c100000\c100000\c99608;\cssrgb\c0\c0\c0;
\cssrgb\c0\c6667\c53333;\cssrgb\c0\c50196\c0;\cssrgb\c63922\c8235\c8235;}
\paperw11900\paperh16840\margl1440\margr1440\vieww21260\viewh11380\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs28 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 # \uc0\u55358 \u56598  Personal AI Task & Reflection Agent\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 ### Google AI Agents Intensive \'97 Capstone Project\cf0 \cb1 \strokec4 \
\
\cf2 \cb3 \strokec2 ## \uc0\u55357 \u56523  Executive Summary\cf0 \cb1 \strokec4 \
\
\cb3 The 
\f1\b **Personal AI Task & Reflection Agent**
\f0\b0  is a sophisticated, production-ready AI assistant designed to help users manage their tasks and emotional well-being. Unlike standard chatbots, this agent is built on a robust 
\f1\b **agentic architecture**
\f0\b0  that allows it to reason about user intent, maintain persistent context, execute specialized tools, and orchestrate sub-agents for complex problem-solving.\cb1 \
\
\cb3 This project serves as a practical application of advanced AI concepts, demonstrating how to build a reliable, observable, and scalable AI system using Python and the Google Gemini API.\cb1 \
\
\cf2 \cb3 \strokec2 ---\cf0 \cb1 \strokec4 \
\
\cf2 \cb3 \strokec2 ## \uc0\u55356 \u57303 \u65039  System Architecture\cf0 \cb1 \strokec4 \
\
\cb3 The system is built on a modular, class-based architecture where a central agent orchestrates various specialized components. This design ensures separation of concerns, making the system easier to maintain and extend.\cb1 \
\
\cf2 \cb3 \strokec2 ### \uc0\u55357 \u56514  File Function Overview (Starter Guide)\cf0 \cb1 \strokec4 \
\
\cb3 This table provides a quick overview of each file in the repository and its role, serving as a starter guide for navigating the project.\cb1 \
\
\cf2 \cb3 \strokec2 | File | Function |\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 | :--- | :--- |\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 |\cf0 \strokec4  \cf5 \strokec5 `personal_task_agent.py`\cf0 \strokec4  \cf2 \strokec2 |\cf0 \strokec4  
\f1\b **Core Application Code.**
\f0\b0  The main entry point for the agent, containing the \cf5 \strokec5 `PersonalTaskAgent`\cf0 \strokec4 , \cf5 \strokec5 `MemorySystem`\cf0 \strokec4 , \cf5 \strokec5 `ToolRegistry`\cf0 \strokec4 , \cf5 \strokec5 `LLMInterface`\cf0 \strokec4 , and \cf5 \strokec5 `ProductionAgent`\cf0 \strokec4  classes. It orchestrates the entire interaction loop. \cf2 \strokec2 |\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 |\cf0 \strokec4  \cf5 \strokec5 `agent_memory.db`\cf0 \strokec4  \cf2 \strokec2 |\cf0 \strokec4  
\f1\b **Long-Term Memory.**
\f0\b0  An SQLite database generated at runtime to persist tasks, diary entries, user patterns, and conversation history across sessions. \cf2 \strokec2 |\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 |\cf0 \strokec4  \cf5 \strokec5 `agent_logs.log`\cf0 \strokec4  \cf2 \strokec2 |\cf0 \strokec4  
\f1\b **Activity & Error Logs.**
\f0\b0  A file generated at runtime that records detailed timestamped events, including tool executions, API calls, and errors for debugging. \cf2 \strokec2 |\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 |\cf0 \strokec4  \cf5 \strokec5 `agent_metrics.json`\cf0 \strokec4  \cf2 \strokec2 |\cf0 \strokec4  
\f1\b **Performance Metrics.**
\f0\b0  A JSON file generated on exit containing high\cf2 \strokec2 -\cf0 \strokec4 level session statistics like uptime, total events, and counts of different actions. \cf2 \strokec2 |\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 |\cf0 \strokec4  \cf5 \strokec5 `simple_demo.py`\cf0 \strokec4  \cf2 \strokec2 |\cf0 \strokec4  
\f1\b **Logic-Only Demo.**
\f0\b0  A script that demonstrates the agent's internal logic (like task creation) without requiring an API key, useful for basic verification. \cf2 \strokec2 |\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 |\cf0 \strokec4  \cf5 \strokec5 `test_setup.py`\cf0 \strokec4  \cf2 \strokec2 |\cf0 \strokec4  
\f1\b **Environment Checker.**
\f0\b0  A diagnostic script to verify the Python environment, installed libraries, and connectivity to the Google Gemini API. \cf2 \strokec2 |\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 |\cf0 \strokec4  \cf5 \strokec5 `key_test.py`\cf0 \strokec4  \cf2 \strokec2 |\cf0 \strokec4  
\f1\b **API Key Tester.**
\f0\b0  A minimal script designed specifically to test if a provided Google Gemini API key is valid and working. \cf2 \strokec2 |\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 |\cf0 \strokec4  \cf5 \strokec5 `check_models.py`\cf0 \strokec4  \cf2 \strokec2 |\cf0 \strokec4  
\f1\b **Model Lister.**
\f0\b0  A utility script that queries the Gemini API to list the models available for use with your specific API key. \cf2 \strokec2 |\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 |\cf0 \strokec4  \cf5 \strokec5 `README.md`\cf0 \strokec4  \cf2 \strokec2 |\cf0 \strokec4  
\f1\b **Documentation.**
\f0\b0  The file you are currently reading, providing a comprehensive overview, setup guide, and technical details of the project. \cf2 \strokec2 |\cf0 \cb1 \strokec4 \
\
\cf2 \cb3 \strokec2 ### High-Level Architecture Diagram\cf0 \cb1 \strokec4 \
\
\cb3 The following diagram illustrates the primary components and their interactions. The User interacts with the \cf5 \strokec5 `PersonalTaskAgent`\cf0 \strokec4 , which acts as the central controller, coordinating with the LLM, Memory, and Tools.\cb1 \
\
\cf6 \cb3 \strokec6 >\cf0 \strokec4  
\f1\b **[Insert High-Level Architecture Diagram Here]**
\f0\b0 \cb1 \
\cf6 \cb3 \strokec6 >\cf0 \strokec4  
\f2\i *(Note: A diagram showing the User connected to the PersonalTaskAgent. The Agent is connected bi-directionally to the LLMInterface, ToolRegistry, and MemorySystem (which connects to SQLite). The ProductionAgent wraps the central Agent, and a MetricsCollector observes the whole system.)*
\f0\i0 \cb1 \
\
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **User:**
\f0\b0  The end-user interacting via a command-line interface.\cb1 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **PersonalTaskAgent (Main Controller):**
\f0\b0  The core logic that receives input, determines intent, and manages the overall conversation flow.\cb1 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **LLMInterface:**
\f0\b0  An abstraction layer for communication with the Google Gemini API.\cb1 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **ToolRegistry:**
\f0\b0  A central repository of executable functions (tools) that the agent can call.\cb1 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **MemorySystem:**
\f0\b0  Manages both short-term (in-memory) and long-term (SQLite database) context.\cb1 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **ProductionAgent (Wrapper):**
\f0\b0  Adds a layer of production features like rate limiting and caching around the main agent.\cb1 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **MetricsCollector & Logger:**
\f0\b0  Tracks system performance and logs events for observability.\cb1 \
\
\cf2 \cb3 \strokec2 ---\cf0 \cb1 \strokec4 \
\
\cf2 \cb3 \strokec2 ## \uc0\u55357 \u56580  Data Flow & Request Lifecycle\cf0 \cb1 \strokec4 \
\
\cb3 Understanding how a user's request is processed is key to grasping the agent's operation. The data flow follows a "reason-then-act" pattern.\cb1 \
\
\cf2 \cb3 \strokec2 ### Request Processing Data Flow Diagram\cf0 \cb1 \strokec4 \
\
\cb3 This diagram shows the step-by-step journey of a user's input from ingestion to response generation.\cb1 \
\
\cf6 \cb3 \strokec6 >\cf0 \strokec4  
\f1\b **[Insert Data Flow Diagram Here]**
\f0\b0 \cb1 \
\cf6 \cb3 \strokec6 >\cf0 \strokec4  
\f2\i *(Note: A sequential diagram illustrating steps: 1. User Input -> 2. Intent Classification (Agent->LLM) -> 3. Tool Selection (Agent->Registry) -> 4. Tool Execution (Agent->Tool->Memory/Calc) -> 5. Response Generation (Agent->LLM) -> 6. Context Update (Agent->Memory) -> 7. Output to User.)*
\f0\i0 \cb1 \
\
\cf2 \cb3 \strokec2 1. \cf0 \strokec4  
\f1\b **Input:**
\f0\b0  The user provides a natural language query (e.g., "Create a task to finish my report by Friday").\cb1 \
\cf2 \cb3 \strokec2 2. \cf0 \strokec4  
\f1\b **Intent Classification:**
\f0\b0  The \cf5 \strokec5 `PersonalTaskAgent`\cf0 \strokec4  sends the input to the \cf5 \strokec5 `LLMInterface`\cf0 \strokec4 . The LLM analyzes the text and determines the user's intent (e.g., \cf5 \strokec5 `create_task`\cf0 \strokec4 ).\cb1 \
\cf2 \cb3 \strokec2 3. \cf0 \strokec4  
\f1\b **Tool Selection:**
\f0\b0  Based on the determined intent, the agent consults the \cf5 \strokec5 `ToolRegistry`\cf0 \strokec4  to find the corresponding tool (e.g., \cf5 \strokec5 `create_task_tool`\cf0 \strokec4 ).\cb1 \
\cf2 \cb3 \strokec2 4. \cf0 \strokec4  
\f1\b **Tool Execution:**
\f0\b0  The selected tool is executed. This may involve:\cb1 \
\cf2 \cb3 \strokec2     * \cf0 \strokec4 Extracting parameters from the user's input (using the LLM).\cb1 \
\cf2 \cb3 \strokec2     * \cf0 \strokec4 Interacting with the \cf5 \strokec5 `MemorySystem`\cf0 \strokec4  to store or retrieve data (e.g., adding a new row to the \cf5 \strokec5 `tasks`\cf0 \strokec4  table in SQLite).\cb1 \
\cf2 \cb3 \strokec2     * \cf0 \strokec4 Performing a calculation or analysis.\cb1 \
\cf2 \cb3 \strokec2 5. \cf0 \strokec4  
\f1\b **Response Generation:**
\f0\b0  The tool returns a result. The agent then formulates a final, natural language response to the user, often incorporating the tool's output.\cb1 \
\cf2 \cb3 \strokec2 6. \cf0 \strokec4  
\f1\b **Context Update:**
\f0\b0  The entire interaction (user input and agent response) is logged into the \cf5 \strokec5 `MemorySystem`\cf0 \strokec4  (both short-term list and long-term \cf5 \strokec5 `conversations`\cf0 \strokec4  table) to maintain context for future turns.\cb1 \
\cf2 \cb3 \strokec2 7. \cf0 \strokec4  
\f1\b **Output:**
\f0\b0  The final response is displayed to the user.\cb1 \
\
\cf2 \cb3 \strokec2 ---\cf0 \cb1 \strokec4 \
\
\cf2 \cb3 \strokec2 ## \uc0\u55358 \u56785 \u8205 \u55357 \u56507  Technical Deep Dive: `personal_task_agent.py`\cf0 \cb1 \strokec4 \
\
\cb3 This file is the core of the application. It contains the primary class definitions that bring the agent to life. Below is a detailed breakdown of its key components.\cb1 \
\
\cf2 \cb3 \strokec2 ### 1. `PersonalTaskAgent` Class (The Orchestrator)\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **Role:**
\f0\b0  The central "brain" of the system. It integrates all other components and manages the main interaction loop.\cb1 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **Key Method: `process_natural_language(self, user_input)`:**
\f0\b0  This is the critical intent classifier. It constructs a prompt for the LLM, asking it to categorize the user's input into a predefined set of intents (e.g., \cf5 \strokec5 `create_task`\cf0 \strokec4 , \cf5 \strokec5 `ask_advice`\cf0 \strokec4 ). This is the first step in the "reasoning" process.\cb1 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **Key Method: `chat(self, user_input)`:**
\f0\b0  The primary public method. It coordinates the entire data flow described above: getting intent, finding the tool, executing it, and generating the final response.\cb1 \
\
\cf2 \cb3 \strokec2 ### 2. `MemorySystem` Class (The Context Keeper)\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **Role:**
\f0\b0  Manages the agent's state across interactions.\cb1 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **Short-Term Memory:**
\f0\b0  Implemented as a Python list (\cf5 \strokec5 `self.short_term_memory`\cf0 \strokec4 ) storing the last few interactions. This provides immediate context for follow-up questions.\cb1 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **Long-Term Memory:**
\f0\b0  Implemented using an 
\f1\b **SQLite database**
\f0\b0  (\cf5 \strokec5 `agent_memory.db`\cf0 \strokec4 ). This is crucial for persistence across sessions. The class defines and manages four relational tables:\cb1 \
\cf2 \cb3 \strokec2     * \cf5 \strokec5 `tasks`\cf0 \strokec4 : Stores task details (title, priority, status, deadline).\cb1 \
\cf2 \cb3 \strokec2     * \cf5 \strokec5 `diary_entries`\cf0 \strokec4 : Stores user reflections along with an AI-generated mood score.\cb1 \
\cf2 \cb3 \strokec2     * \cf5 \strokec5 `user_patterns`\cf0 \strokec4 : A place to store learned user preferences over time.\cb1 \
\cf2 \cb3 \strokec2     * \cf5 \strokec5 `conversations`\cf0 \strokec4 : A complete log of all user-agent turns.\cb1 \
\
\cf2 \cb3 \strokec2 ### 3. `ToolRegistry` Class (The Capability Hub)\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **Role:**
\f0\b0  Implements the 
\f1\b **Model Context Protocol (MCP)**
\f0\b0  pattern. It decouples the agent's reasoning ("what to do") from its execution ("how to do it").\cb1 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **Mechanism:**
\f0\b0  Uses a decorator (\cf5 \strokec5 `@register_tool`\cf0 \strokec4 ) to register Python functions as tools. The agent's core logic doesn't need to know 
\f2\i *how*
\f0\i0  a tool works, only its name. This makes adding new capabilities straightforward.\cb1 \
\
\cf2 \cb3 \strokec2 ### 4. `LLMInterface` Class (The AI Interface)\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **Role:**
\f0\b0  An abstraction layer for the Google Gemini API.\cb1 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **Functionality:**
\f0\b0  It handles the initialization of the \cf5 \strokec5 `genai.GenerativeModel`\cf0 \strokec4 , manages API keys securely from environment variables, and provides a clean \cf5 \strokec5 `generate_response`\cf0 \strokec4  method that encapsulates the API call, error handling, and retry logic.\cb1 \
\
\cf2 \cb3 \strokec2 ### 5. `MultiAgentOrchestrator` Class (The Delegator)\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **Role:**
\f0\b0  Demonstrates advanced multi-agent patterns.\cb1 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **Functionality:**
\f0\b0  For complex or specialized queries, the main agent can delegate to sub-agents. This class manages specialized agents like a \cf5 \strokec5 `SchedulerAgent`\cf0 \strokec4  (for time management) and a \cf5 \strokec5 `MotivationalAgent`\cf0 \strokec4 . A routing mechanism determines which sub-agent is best suited for a task.\cb1 \
\
\cf2 \cb3 \strokec2 ### 6. `ProductionAgent` Class (The Robustness Layer)\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **Role:**
\f0\b0  A wrapper class that inherits from \cf5 \strokec5 `PersonalTaskAgent`\cf0 \strokec4  to add production-grade features.\cb1 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **Features:**
\f0\b0 \cb1 \
\cf2 \cb3 \strokec2     * 
\f1\b \cf0 \strokec4 **Rate Limiting:**
\f0\b0  Implements checks to prevent abuse of the Gemini API.\cb1 \
\cf2 \cb3 \strokec2     * 
\f1\b \cf0 \strokec4 **Caching:**
\f0\b0  Uses \cf5 \strokec5 `functools.lru_cache`\cf0 \strokec4  to store responses to identical queries, reducing API costs and latency.\cb1 \
\cf2 \cb3 \strokec2     * 
\f1\b \cf0 \strokec4 **Health Checks:**
\f0\b0  Includes a method to verify the status of external dependencies like the database and API.\cb1 \
\
\cf2 \cb3 \strokec2 ---\cf0 \cb1 \strokec4 \
\
\cf2 \cb3 \strokec2 ## \uc0\u55357 \u56514  Project File Structure\cf0 \cb1 \strokec4 \
\
\cf7 \cb3 \strokec7 ```text\cf0 \cb1 \strokec4 \
\cb3 ai-agents-capstone/\cb1 \
\cb3 \uc0\u9500 \u9472 \u9472  agent_logs.log          # Runtime activity and error logs (Generated on run)\cb1 \
\cb3 \uc0\u9500 \u9472 \u9472  agent_memory.db         # SQLite database for long-term memory (Generated on run)\cb1 \
\cb3 \uc0\u9500 \u9472 \u9472  agent_metrics.json      # JSON file for performance metrics (Generated on exit)\cb1 \
\cb3 \uc0\u9500 \u9472 \u9472  check_models.py         # Utility to list available Gemini models for your key\cb1 \
\cb3 \uc0\u9500 \u9472 \u9472  key_test.py             # Minimal utility to test API key validity\cb1 \
\cb3 \uc0\u9500 \u9472 \u9472  personal_task_agent.py  # CORE APPLICATION CODE - Main Agent Entry Point\cb1 \
\cb3 \uc0\u9500 \u9472 \u9472  README.md               # This documentation file\cb1 \
\cb3 \uc0\u9500 \u9472 \u9472  simple_demo.py          # Logic-only demo (runs without API key dependence)\cb1 \
\cb3 \uc0\u9492 \u9472 \u9472  test_setup.py           # Environment, library, and connection checker script\cb1 \
\cf7 \cb3 \strokec7 ```\cf0 \cb1 \strokec4 \
\
\cf2 \cb3 \strokec2 ---\cf0 \cb1 \strokec4 \
\
\cf2 \cb3 \strokec2 ## \uc0\u55357 \u57056 \u65039  Setup and Usage Guide\cf0 \cb1 \strokec4 \
\
\cf2 \cb3 \strokec2 ### 1. Prerequisites\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 * \cf0 \strokec4 Python 3.8+\cb1 \
\cf2 \cb3 \strokec2 * \cf0 \strokec4 Google Generative AI SDK (\cf5 \strokec5 `pip install google-generativeai`\cf0 \strokec4 )\cb1 \
\cf2 \cb3 \strokec2 * \cf0 \strokec4 Google Gemini API key\cb1 \
\
\cf2 \cb3 \strokec2 ### 2. API Key Configuration\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 * \cf0 \strokec4 API Key is required for the project to work and connect with Google gemini. \cb1 \
\cf2 \cb3 \strokec2 * \cf0 \strokec4 Once the API key is generated, you can test it using key_test.py.\cb1 \
\cf7 \cb3 \strokec7     ```text\cf0 \cb1 \strokec4 \
\cf7 \cb3 \strokec7     client = genai.Client(api_key="Insert API key")\cf0 \cb1 \strokec4 \
\cf7 \cb3 \strokec7     ```\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 * \cf0 \strokec4 Once the test succeeds, you can place the values in the personal_task_agent.py \cb1 \
\cf7 \cb3 \strokec7     ```text\cf0 \cb1 \strokec4 \
\cf7 \cb3 \strokec7     os.environ["GEMINI_API_KEY"] = "Insert API Key"\cf0 \cb1 \strokec4 \
\cf7 \cb3 \strokec7     os.environ["GOOGLE_API_KEY"] = "Insert API Key"\cf0 \cb1 \strokec4 \
\cf7 \cb3 \strokec7     ```\cf0 \cb1 \strokec4 \
\
\
\
\cf2 \cb3 \strokec2 ### Running the Agent\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 1. \cf0 \strokec4  
\f1\b **Navigate to the project directory:**
\f0\b0 \cb1 \
\cf7 \cb3 \strokec7     ```bash\cf0 \cb1 \strokec4 \
\cf7 \cb3 \strokec7     cd ai-agents-capstone\cf0 \cb1 \strokec4 \
\cf7 \cb3 \strokec7     ```\cf0 \cb1 \strokec4 \
\cf2 \cb3 \strokec2 2. \cf0 \strokec4  
\f1\b **Run the main script:**
\f0\b0 \cb1 \
\cf7 \cb3 \strokec7     ```bash\cf0 \cb1 \strokec4 \
\cf7 \cb3 \strokec7     python personal_task_agent.py\cf0 \cb1 \strokec4 \
\cf7 \cb3 \strokec7     ```\cf0 \cb1 \strokec4 \
\cb3 The agent will perform an initial self-test and demo routine, after which it will enter an interactive chat mode where you can issue natural language commands.\cb1 \
\
\cf2 \cb3 \strokec2 ---\cf0 \cb1 \strokec4 \
\
\cf2 \cb3 \strokec2 ## \uc0\u55357 \u56522  Observability: Data and Metrics\cf0 \cb1 \strokec4 \
\
\cb3 The system is designed to be observable, providing insights into its operation and user interactions.\cb1 \
\
\cf2 \cb3 \strokec2 ### Persistent Data (`agent_memory.db`)\cf0 \cb1 \strokec4 \
\cb3 You can inspect the SQLite database using any standard SQLite viewer. Key tables include:\cb1 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **`tasks`:**
\f0\b0  View all created tasks, their status, priorities, and deadlines.\cb1 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **`diary_entries`:**
\f0\b0  Read user reflections and analyze the AI-assigned mood scores (scale 1-5) to track emotional trends.\cb1 \
\
\cf2 \cb3 \strokec2 ### Performance Metrics (`agent_metrics.json`)\cf0 \cb1 \strokec4 \
\cb3 After each session, a metrics summary is written to this JSON file. It includes data points such as:\cb1 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **`uptime_hours`**
\f0\b0 : Total duration of the session.\cb1 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **`total_events`**
\f0\b0 : The aggregate count of recorded actions.\cb1 \
\cf2 \cb3 \strokec2 * 
\f1\b \cf0 \strokec4 **`event_types`**
\f0\b0 : A breakdown of specific actions (e.g., \cf5 \strokec5 `\{"chat_interaction": 5, "task_created": 2\}`\cf0 \strokec4 ).\cb1 \
\
\cf2 \cb3 \strokec2 ### Activity Logs (`agent_logs.log`)\cf0 \cb1 \strokec4 \
\cb3 This file contains a detail\cb1 ed log of all actions being performed.}