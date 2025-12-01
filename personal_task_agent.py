import os

import google.generativeai as genai



# FORCE THE KEY TO BE SEEN

os.environ["GEMINI_API_KEY"] = "Insert API Key"

os.environ["GOOGLE_API_KEY"] = "Insert API Key"

"""
Personal AI Task & Reflection Agent
Google AI Agents Intensive Capstone Project
November 2024

This agent combines task management with AI diary capabilities,
demonstrating key concepts from the 5-day course:
1. Agent Architecture & Tool Usage
2. Memory Management (Short & Long-term)
3. Context Engineering
4. Observability & Evaluation
5. Production-ready features
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, asdict, field
from enum import Enum
import hashlib
import sqlite3
from collections import defaultdict
import re
# New Gemini client (GenAI) - required for Google Gemini API
# Make sure GEMINI_API_KEY is exported in your shell session
from google import genai
try:
    client = genai.Client(api_key="AIzaSyDlTYoWMLLtDHm5AKpv_gBDfEr7eKdy-WU")
except Exception as e:
    logger.warning("Could not initialize genai.Client(): %s", e)
    client = None
# Configure logging for observability (Day 4 concept)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent_logs.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Google Gemini API setup
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("Google Gemini not available. Install with: pip install google-generativeai")

# OpenAI API as fallback
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI not available. Install with: pip install openai")

# ==================== Data Models ====================

class Priority(Enum):
    """Task priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

class TaskStatus(Enum):
    """Task completion status"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class MoodLevel(Enum):
    """User mood levels for diary entries"""
    VERY_SAD = 1
    SAD = 2
    NEUTRAL = 3
    HAPPY = 4
    VERY_HAPPY = 5

@dataclass
class Task:
    """Task data model"""
    id: str
    title: str
    description: str
    category: str
    priority: Priority
    status: TaskStatus
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    subtasks: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    estimated_hours: float = 0
    actual_hours: float = 0
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary for storage"""
        data = asdict(self)
        data['priority'] = self.priority.value
        data['status'] = self.status.value
        data['due_date'] = self.due_date.isoformat() if self.due_date else None
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        data['completed_at'] = self.completed_at.isoformat() if self.completed_at else None
        return data

@dataclass
class DiaryEntry:
    """Diary/journal entry data model"""
    id: str
    date: datetime
    content: str
    mood: MoodLevel
    tasks_mentioned: List[str]
    insights: List[str]
    gratitude: List[str]
    challenges: List[str]
    tomorrow_goals: List[str]
    energy_level: int  # 1-10
    productivity_score: int  # 1-10
    
    def to_dict(self) -> Dict:
        """Convert diary entry to dictionary"""
        data = asdict(self)
        data['date'] = self.date.isoformat()
        data['mood'] = self.mood.value
        return data

# ==================== Memory Management (Day 3) ====================

class MemorySystem:
    """
    Implements both short-term and long-term memory
    Following Day 3 concepts: Context Engineering & Memory Management
    """
    
    def __init__(self, db_path: str = "agent_memory.db"):
        self.db_path = db_path
        self.short_term_memory = []  # Recent interactions (last 10)
        self.working_memory = {}  # Current session context
        self._initialize_database()
        
    def _initialize_database(self):
        """Initialize SQLite database for long-term memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        ''')
        
        # Diary entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diary_entries (
                id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                date TIMESTAMP,
                mood INTEGER
            )
        ''')
        
        # User patterns table (for AI insights)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_patterns (
                id TEXT PRIMARY KEY,
                pattern_type TEXT,
                pattern_data TEXT,
                confidence REAL,
                discovered_at TIMESTAMP
            )
        ''')
        
        # Conversation history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT,
                agent_response TEXT,
                timestamp TIMESTAMP,
                context TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Memory system initialized")
        
    def add_to_short_term(self, item: Dict):
        """Add item to short-term memory (limited to 10 items)"""
        self.short_term_memory.append({
            'timestamp': datetime.now().isoformat(),
            'data': item
        })
        if len(self.short_term_memory) > 10:
            self.short_term_memory.pop(0)
            
    def store_task(self, task: Task):
        """Store task in long-term memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO tasks (id, data, created_at, updated_at)
            VALUES (?, ?, ?, ?)
        ''', (task.id, json.dumps(task.to_dict()), task.created_at, task.updated_at))
        conn.commit()
        conn.close()
        
    def retrieve_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """Retrieve tasks from long-term memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT data FROM tasks')
        tasks = []
        for row in cursor.fetchall():
            task_data = json.loads(row[0])
            # Reconstruct Task object
            task = self._reconstruct_task(task_data)
            if status is None or task.status == status:
                tasks.append(task)
        conn.close()
        return tasks
    
    def _reconstruct_task(self, data: Dict) -> Task:
        """Reconstruct Task object from stored data"""
        return Task(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            category=data['category'],
            priority=Priority(data['priority']),
            status=TaskStatus(data['status']),
            due_date=datetime.fromisoformat(data['due_date']) if data['due_date'] else None,
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            completed_at=datetime.fromisoformat(data['completed_at']) if data['completed_at'] else None,
            subtasks=data['subtasks'],
            dependencies=data['dependencies'],
            estimated_hours=data['estimated_hours'],
            actual_hours=data['actual_hours'],
            tags=data['tags']
        )
    
    def store_diary_entry(self, entry: DiaryEntry):
        """Store diary entry in long-term memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO diary_entries (id, data, date, mood)
            VALUES (?, ?, ?, ?)
        ''', (entry.id, json.dumps(entry.to_dict()), entry.date, entry.mood.value))
        conn.commit()
        conn.close()
        
    def get_patterns(self) -> List[Dict]:
        """Retrieve discovered patterns about user behavior"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT pattern_type, pattern_data, confidence FROM user_patterns')
        patterns = [
            {'type': row[0], 'data': json.loads(row[1]), 'confidence': row[2]}
            for row in cursor.fetchall()
        ]
        conn.close()
        return patterns

# ==================== Tool System (Day 2) ====================

class ToolRegistry:
    """
    Tool registry implementing MCP (Model Context Protocol) concepts
    Allows the agent to use various tools for different tasks
    """
    
    def __init__(self):
        self.tools = {}
        self._register_default_tools()
        
    def _register_default_tools(self):
        """Register default tools available to the agent"""
        self.register_tool("create_task", self.create_task_tool)
        self.register_tool("break_down_task", self.break_down_task_tool)
        self.register_tool("prioritize_tasks", self.prioritize_tasks_tool)
        self.register_tool("analyze_mood", self.analyze_mood_tool)
        self.register_tool("generate_insights", self.generate_insights_tool)
        self.register_tool("suggest_next_action", self.suggest_next_action_tool)
        
    def register_tool(self, name: str, function):
        """Register a new tool"""
        self.tools[name] = function
        logger.info(f"Tool registered: {name}")
        
    def use_tool(self, name: str, **kwargs) -> Any:
        """Use a registered tool"""
        if name not in self.tools:
            raise ValueError(f"Tool {name} not found")
        logger.info(f"Using tool: {name}")
        return self.tools[name](**kwargs)
    
    # Tool implementations
    def create_task_tool(self, title: str, description: str, **kwargs) -> Task:
        """Tool to create a new task"""
        task_id = hashlib.md5(f"{title}{datetime.now()}".encode()).hexdigest()[:8]
        task = Task(
            id=task_id,
            title=title,
            description=description,
            category=kwargs.get('category', 'general'),
            priority=Priority[kwargs.get('priority', 'MEDIUM').upper()],
            status=TaskStatus.TODO,
            due_date=kwargs.get('due_date'),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            tags=kwargs.get('tags', [])
        )
        return task
    
    def break_down_task_tool(self, task: Task, llm_client) -> List[str]:
        """Break down a task into subtasks using AI"""
        prompt = f"""
        Break down this task into 3-5 actionable subtasks:
        Title: {task.title}
        Description: {task.description}
        
        Return as a JSON list of strings.
        """
        
        if llm_client:
            response = llm_client.generate(prompt)
            try:
                subtasks = json.loads(response)
                return subtasks
            except:
                return ["Plan the task", "Execute main work", "Review and finalize"]
        return ["Plan the task", "Execute main work", "Review and finalize"]
    
    def prioritize_tasks_tool(self, tasks: List[Task]) -> List[Task]:
        """Prioritize tasks based on urgency and importance"""
        def score_task(task):
            score = task.priority.value * 10
            if task.due_date:
                days_until = (task.due_date - datetime.now()).days
                if days_until <= 1:
                    score += 50
                elif days_until <= 3:
                    score += 30
                elif days_until <= 7:
                    score += 10
            return score
        
        return sorted(tasks, key=score_task, reverse=True)
    
    def analyze_mood_tool(self, text: str) -> MoodLevel:
        """Analyze mood from diary text"""
        positive_words = ['happy', 'great', 'excellent', 'amazing', 'wonderful', 'excited']
        negative_words = ['sad', 'frustrated', 'angry', 'tired', 'stressed', 'worried']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count + 2:
            return MoodLevel.VERY_HAPPY
        elif positive_count > negative_count:
            return MoodLevel.HAPPY
        elif negative_count > positive_count + 2:
            return MoodLevel.VERY_SAD
        elif negative_count > positive_count:
            return MoodLevel.SAD
        return MoodLevel.NEUTRAL
    
    def generate_insights_tool(self, entries: List[DiaryEntry]) -> List[str]:
        """Generate insights from diary entries"""
        if not entries:
            return []
        
        insights = []
        
        # Mood patterns
        moods = [e.mood.value for e in entries]
        avg_mood = sum(moods) / len(moods)
        if avg_mood < 2.5:
            insights.append("You've been feeling down lately. Consider talking to someone or taking a break.")
        elif avg_mood > 3.5:
            insights.append("Your mood has been consistently positive! Keep up what you're doing.")
        
        # Productivity patterns
        productivity = [e.productivity_score for e in entries]
        avg_productivity = sum(productivity) / len(productivity)
        if avg_productivity < 5:
            insights.append("Productivity seems low. Try breaking tasks into smaller chunks.")
        elif avg_productivity > 7:
            insights.append("You're being very productive! Remember to maintain work-life balance.")
        
        return insights
    
    def suggest_next_action_tool(self, tasks: List[Task], current_time: datetime) -> str:
        """Suggest the next best action based on tasks and time"""
        pending_tasks = [t for t in tasks if t.status != TaskStatus.COMPLETED]
        if not pending_tasks:
            return "All tasks completed! Time to add new goals or relax."
        
        # Prioritize tasks
        prioritized = self.prioritize_tasks_tool(pending_tasks)
        next_task = prioritized[0]
        
        suggestion = f"Focus on: {next_task.title}"
        if next_task.due_date:
            days_until = (next_task.due_date - current_time).days
            if days_until <= 1:
                suggestion += " (Due soon!)"
        
        return suggestion

# =============== Updated LLM Interface (Gemini 2.5 Flash) ===============

from google import genai

class LLMInterface:
    """Unified interface for different LLM providers"""

    def __init__(self, provider: str = "gemini", api_key: Optional[str] = None):
        self.provider = provider
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the LLM client"""
        if self.provider == "gemini":
            try:
                # This automatically reads GEMINI_API_KEY from your environment
                self.client = genai.Client()
                logger.info("Gemini client initialized.")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                self.client = None
        else:
            logger.warning(f"Unsupported provider: {self.provider}")
            self.client = None

    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate text using Gemini"""
        if not self.client:
            logger.warning("LLM not available. Returning default fallback response.")
            return "⚠️ LLM unavailable — using fallback mode."

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
               config={"temperature": temperature}
            )
            return response.text

        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return "⚠️ Error generating response."


# ==================== Main Agent (Day 1 & Day 5) ====================

class PersonalTaskAgent:
    """
    Main agent implementing agentic architecture
    Combines all components for a production-ready system
    """
    
    def __init__(self, llm_provider: str = "gemini", api_key: Optional[str] = None):
        self.memory = MemorySystem()
        self.tools = ToolRegistry()
        self.llm = LLMInterface(llm_provider, api_key)
        self.metrics = MetricsCollector()
        self.session_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        logger.info(f"Agent initialized with session {self.session_id}")
        
    def process_natural_language(self, user_input: str) -> Dict:
        """Process natural language input and determine intent"""
        prompt = f"""
        Analyze this user input and determine the intent and entities:
        "{user_input}"
        
        Return a JSON with:
        - intent: one of [create_task, update_task, diary_entry, get_tasks, get_insights, ask_advice]
        - entities: extracted information like task title, description, dates, etc.
        
        Example:
        {{"intent": "create_task", "entities": {{"title": "...", "description": "..."}}}}
        """
        
        response = self.llm.generate(prompt)
        try:
            return json.loads(response)
        except:
            # Fallback parsing
            if any(word in user_input.lower() for word in ['create', 'add', 'new task']):
                return {"intent": "create_task", "entities": {"title": user_input}}
            elif any(word in user_input.lower() for word in ['diary', 'journal', 'feeling']):
                return {"intent": "diary_entry", "entities": {"content": user_input}}
            else:
                return {"intent": "ask_advice", "entities": {"question": user_input}}
    
    def create_task(self, title: str, description: str = "", **kwargs) -> Task:
        """Create a new task"""
        task = self.tools.use_tool(
            "create_task",
            title=title,
            description=description,
            **kwargs
        )
        
        # Generate subtasks if description is detailed
        if len(description) > 50:
            subtasks = self.tools.use_tool(
                "break_down_task",
                task=task,
                llm_client=self.llm
            )
            task.subtasks = subtasks
        
        # Store in memory
        self.memory.store_task(task)
        self.memory.add_to_short_term({"action": "task_created", "task": task.to_dict()})
        
        # Track metrics
        self.metrics.track_event("task_created", {"category": task.category})
        
        logger.info(f"Task created: {task.id}")
        return task
    
    def add_diary_entry(self, content: str) -> DiaryEntry:
        """Add a new diary entry"""
        # Analyze mood
        mood = self.tools.use_tool("analyze_mood", text=content)
        
        # Extract mentioned tasks
        tasks = self.memory.retrieve_tasks()
        mentioned_tasks = [
            t.id for t in tasks 
            if t.title.lower() in content.lower()
        ]
        
        # Generate AI insights
        prompt = f"""
        From this diary entry, extract:
        1. Key insights or realizations
        2. Things the person is grateful for
        3. Challenges mentioned
        4. Goals for tomorrow
        
        Entry: {content}
        
        Return as JSON with keys: insights, gratitude, challenges, tomorrow_goals (all as lists)
        """
        
        ai_analysis = self.llm.generate(prompt)
        try:
            analysis = json.loads(ai_analysis)
        except:
            analysis = {
                "insights": [],
                "gratitude": [],
                "challenges": [],
                "tomorrow_goals": []
            }
        
        entry = DiaryEntry(
            id=hashlib.md5(f"{content}{datetime.now()}".encode()).hexdigest()[:8],
            date=datetime.now(),
            content=content,
            mood=mood,
            tasks_mentioned=mentioned_tasks,
            insights=analysis.get('insights', []),
            gratitude=analysis.get('gratitude', []),
            challenges=analysis.get('challenges', []),
            tomorrow_goals=analysis.get('tomorrow_goals', []),
            energy_level=5,  # Could be extracted from content
            productivity_score=5  # Could be calculated from completed tasks
        )
        
        self.memory.store_diary_entry(entry)
        self.metrics.track_event("diary_entry_added", {"mood": mood.value})
        
        return entry
    
    def get_daily_briefing(self) -> str:
        """Generate a daily briefing with tasks and insights"""
        tasks = self.memory.retrieve_tasks(TaskStatus.TODO)
        prioritized = self.tools.use_tool("prioritize_tasks", tasks=tasks)
        
        briefing = "📅 **Daily Briefing**\n\n"
        
        # Today's priorities
        briefing += "**Top Priorities:**\n"
        for i, task in enumerate(prioritized[:3], 1):
            briefing += f"{i}. {task.title}"
            if task.due_date:
                days_until = (task.due_date - datetime.now()).days
                if days_until <= 1:
                    briefing += " ⚠️ Due Soon"
            briefing += "\n"
        
        # Recent patterns
        patterns = self.memory.get_patterns()
        if patterns:
            briefing += "\n**Recent Patterns:**\n"
            for pattern in patterns[:2]:
                briefing += f"- {pattern['data'].get('description', 'Pattern detected')}\n"
        
        # Suggestion
        suggestion = self.tools.use_tool(
            "suggest_next_action",
            tasks=tasks,
            current_time=datetime.now()
        )
        briefing += f"\n**Suggested Focus:** {suggestion}\n"
        
        return briefing
    
    def chat(self, user_input: str) -> str:
        """Main chat interface"""
        # Log conversation
        logger.info(f"User input: {user_input}")
        
        # Process input
        parsed = self.process_natural_language(user_input)
        intent = parsed['intent']
        entities = parsed.get('entities', {})
        
        response = ""
        
        if intent == 'create_task':
            task = self.create_task(
                title=entities.get('title', user_input),
                description=entities.get('description', ''),
                category=entities.get('category', 'general'),
                priority=entities.get('priority', 'MEDIUM')
            )
            response = f"✅ Task created: {task.title}\n"
            if task.subtasks:
                response += "Subtasks:\n" + "\n".join(f"- {s}" for s in task.subtasks)
                
        elif intent == 'diary_entry':
            entry = self.add_diary_entry(entities.get('content', user_input))
            response = f"📝 Diary entry saved!\n"
            response += f"Mood detected: {entry.mood.name}\n"
            if entry.insights:
                response += "Insights: " + ", ".join(entry.insights[:2])
                
        elif intent == 'get_tasks':
            tasks = self.memory.retrieve_tasks(TaskStatus.TODO)
            if tasks:
                response = "📋 Your tasks:\n"
                for task in tasks[:5]:
                    response += f"- {task.title} [{task.priority.name}]\n"
            else:
                response = "No pending tasks. Time to add some goals!"
                
        elif intent == 'get_insights':
            # Generate insights from recent data
            conn = sqlite3.connect(self.memory.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT data FROM diary_entries ORDER BY date DESC LIMIT 7')
            recent_entries = []
            for row in cursor.fetchall():
                # Simple reconstruction for insights
                entry_data = json.loads(row[0])
                recent_entries.append(type('Entry', (), {
                    'mood': type('Mood', (), {'value': entry_data['mood']}),
                    'productivity_score': entry_data.get('productivity_score', 5)
                }))
            conn.close()
            
            if recent_entries:
                insights = self.tools.use_tool("generate_insights", entries=recent_entries)
                response = "💡 Insights from your recent activity:\n"
                for insight in insights:
                    response += f"- {insight}\n"
            else:
                response = "Add more diary entries to generate insights!"
                
        else:  # ask_advice or general chat
            # Use LLM for general advice
            context = f"""
            You are a helpful personal assistant helping with task management and life reflection.
            Recent tasks: {len(self.memory.retrieve_tasks())} tasks
            User question: {user_input}
            
            Provide helpful, encouraging advice.
            """
            response = self.llm.generate(context)
        
        # Store conversation
        conn = sqlite3.connect(self.memory.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO conversations (user_input, agent_response, timestamp, context)
            VALUES (?, ?, ?, ?)
        ''', (user_input, response, datetime.now(), json.dumps(parsed)))
        conn.commit()
        conn.close()
        
        # Track metrics
        self.metrics.track_event("chat_interaction", {"intent": intent})
        
        return response

# ==================== Observability & Metrics (Day 4) ====================

class MetricsCollector:
    """
    Collects metrics for agent performance evaluation
    Implements observability concepts from Day 4
    """
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.start_time = datetime.now()
        
    def track_event(self, event_type: str, data: Dict):
        """Track an event with metadata"""
        self.metrics[event_type].append({
            'timestamp': datetime.now().isoformat(),
            'data': data
        })
        
    def get_statistics(self) -> Dict:
        """Get performance statistics"""
        stats = {
            'uptime_hours': (datetime.now() - self.start_time).total_seconds() / 3600,
            'total_events': sum(len(events) for events in self.metrics.values()),
            'event_types': {}
        }
        
        for event_type, events in self.metrics.items():
            stats['event_types'][event_type] = len(events)
        
        return stats
    
    def export_metrics(self, filepath: str):
        """Export metrics to JSON file"""
        with open(filepath, 'w') as f:
            json.dump({
                'metrics': dict(self.metrics),
                'statistics': self.get_statistics()
            }, f, indent=2)

# ==================== Multi-Agent System (Day 5) ====================

class MultiAgentOrchestrator:
    """
    Orchestrates multiple specialized agents
    Demonstrates multi-agent systems from Day 5
    """
    
    def __init__(self):
        self.agents = {}
        self._initialize_agents()
        
    def _initialize_agents(self):
        """Initialize specialized agents"""
        # Main task agent
        self.agents['task_manager'] = PersonalTaskAgent()
        
        # Specialized agents (simplified for demo)
        self.agents['scheduler'] = SchedulerAgent()
        self.agents['motivator'] = MotivationalAgent()
        self.agents['analyst'] = AnalyticsAgent()
        
    def coordinate_response(self, user_input: str) -> str:
        """Coordinate response across multiple agents"""
        responses = []
        
        # Get main response from task manager
        main_response = self.agents['task_manager'].chat(user_input)
        responses.append(main_response)
        
        # Check if scheduler agent should contribute
        if any(word in user_input.lower() for word in ['schedule', 'calendar', 'when']):
            schedule_response = self.agents['scheduler'].suggest_schedule(
                self.agents['task_manager'].memory.retrieve_tasks()
            )
            responses.append(f"\n📅 Scheduling suggestion: {schedule_response}")
        
        # Check if motivational support needed
        if any(word in user_input.lower() for word in ['tired', 'stressed', 'overwhelmed']):
            motivation = self.agents['motivator'].provide_encouragement()
            responses.append(f"\n💪 {motivation}")
        
        return "\n".join(responses)

class SchedulerAgent:
    """Agent specialized in scheduling and time management"""
    
    def suggest_schedule(self, tasks: List[Task]) -> str:
        """Suggest optimal schedule for tasks"""
        if not tasks:
            return "No tasks to schedule"
        
        urgent_tasks = [t for t in tasks if t.priority == Priority.URGENT]
        if urgent_tasks:
            return f"Focus on urgent task: {urgent_tasks[0].title} first"
        
        total_hours = sum(t.estimated_hours for t in tasks if t.estimated_hours > 0)
        return f"You have approximately {total_hours:.1f} hours of work. Consider time-blocking your calendar."

class MotivationalAgent:
    """Agent specialized in providing motivation and support"""
    
    def provide_encouragement(self) -> str:
        """Provide motivational message"""
        messages = [
            "You're doing great! One step at a time.",
            "Remember, progress over perfection!",
            "Every small task completed is a victory.",
            "Take a deep breath. You've got this!"
        ]
        import random
        return random.choice(messages)

class AnalyticsAgent:
    """Agent specialized in analyzing patterns and providing insights"""
    
    def analyze_productivity_trends(self, tasks: List[Task], entries: List[DiaryEntry]) -> Dict:
        """Analyze productivity trends"""
        analysis = {
            'task_completion_rate': 0,
            'average_task_duration': 0,
            'mood_productivity_correlation': 0,
            'best_productivity_time': 'morning'  # Could be calculated from data
        }
        
        if tasks:
            completed = [t for t in tasks if t.status == TaskStatus.COMPLETED]
            analysis['task_completion_rate'] = len(completed) / len(tasks)
            
            durations = [t.actual_hours for t in completed if t.actual_hours > 0]
            if durations:
                analysis['average_task_duration'] = sum(durations) / len(durations)
        
        return analysis

# ==================== Production Deployment Features ====================

class ProductionAgent(PersonalTaskAgent):
    """
    Production-ready agent with additional features
    Implements concepts from Day 5: Prototype to Production
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rate_limiter = RateLimiter(max_requests=100, window_seconds=3600)
        self.cache = ResponseCache()
        self.health_checker = HealthChecker(self)
        
    def chat_with_production_features(self, user_input: str) -> str:
        """Chat with production features like rate limiting and caching"""
        # Check rate limit
        if not self.rate_limiter.allow_request():
            return "Rate limit exceeded. Please try again later."
        
        # Check cache
        cached = self.cache.get(user_input)
        if cached:
            logger.info("Returning cached response")
            return cached
        
        # Get response
        response = self.chat(user_input)
        
        # Cache response
        self.cache.set(user_input, response)
        
        return response
    
    def get_health_status(self) -> Dict:
        """Get health status of the agent"""
        return self.health_checker.check_health()

class RateLimiter:
    """Simple rate limiter for production use"""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = []
        
    def allow_request(self) -> bool:
        """Check if request is allowed"""
        now = datetime.now()
        window_start = now - timedelta(seconds=self.window_seconds)
        
        # Remove old requests
        self.requests = [r for r in self.requests if r > window_start]
        
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False

class ResponseCache:
    """Simple response cache"""
    
    def __init__(self, ttl_seconds: int = 300):
        self.cache = {}
        self.ttl_seconds = ttl_seconds
        
    def get(self, key: str) -> Optional[str]:
        """Get cached response"""
        if key in self.cache:
            timestamp, value = self.cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.ttl_seconds):
                return value
        return None
    
    def set(self, key: str, value: str):
        """Cache a response"""
        self.cache[key] = (datetime.now(), value)

class HealthChecker:
    """Health checker for production monitoring"""
    
    def __init__(self, agent: PersonalTaskAgent):
        self.agent = agent
        
    def check_health(self) -> Dict:
        """Check agent health"""
        health = {
            'status': 'healthy',
            'checks': {}
        }
        
        # Check database connection
        try:
            conn = sqlite3.connect(self.agent.memory.db_path)
            conn.execute('SELECT 1')
            conn.close()
            health['checks']['database'] = 'ok'
        except:
            health['checks']['database'] = 'error'
            health['status'] = 'unhealthy'
        
        # Check LLM availability
        if self.agent.llm.client:
            health['checks']['llm'] = 'ok'
        else:
            health['checks']['llm'] = 'unavailable'
        
        # Check metrics
        stats = self.agent.metrics.get_statistics()
        health['checks']['metrics'] = {
            'uptime_hours': stats['uptime_hours'],
            'total_events': stats['total_events']
        }
        
        return health

# ==================== Main Execution ====================

def main():
    """Main execution function demonstrating all agent capabilities"""
    print("🤖 Personal AI Task & Reflection Agent")
    print("=" * 50)
    print("Google AI Agents Intensive Capstone Project")
    print("Demonstrating: Agent Architecture, Tools, Memory, Observability, Production Features")
    print("=" * 50)
    print()
    
    # Initialize production agent
    print("Initializing agent...")
    agent = ProductionAgent(
        llm_provider="gemini",  # or "openai"
        api_key=None  # Will use environment variable
    )
    print("Agent ready! ✅\n")
    
    # Demo interactions
    demos = [
        "Create a task to complete the AI Agents capstone project",
        "I'm feeling overwhelmed with all the work. Had a long day but managed to finish the memory system implementation.",
        "What are my top priorities?",
        "Break down the capstone project into smaller tasks",
        "Show me insights about my recent productivity"
    ]
    
    print("Running demo interactions:\n")
    for i, demo_input in enumerate(demos, 1):
        print(f"Demo {i}: {demo_input}")
        response = agent.chat_with_production_features(demo_input)
        print(f"Agent: {response}\n")
        print("-" * 30 + "\n")
    
    # Show metrics
    print("📊 Agent Metrics:")
    stats = agent.metrics.get_statistics()
    print(json.dumps(stats, indent=2))
    print()
    
    # Show health status
    print("🏥 Health Status:")
    health = agent.get_health_status()
    print(json.dumps(health, indent=2))
    print()
    
    # Export metrics
    agent.metrics.export_metrics("agent_metrics.json")
    print("✅ Metrics exported to agent_metrics.json")
    
    # Interactive mode
    print("\n" + "=" * 50)
    print("Interactive Mode - Type 'quit' to exit")
    print("=" * 50)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']:
            break
        
        response = agent.chat_with_production_features(user_input)
        print(f"Agent: {response}")
    
    print("\n👋 Thank you for using the Personal AI Task & Reflection Agent!")

if __name__ == "__main__":
    main()
