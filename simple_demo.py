#!/usr/bin/env python3
"""
Simple Demo - Works Without API Key
This demonstrates the agent structure even if API is not working
"""

import json
from datetime import datetime
import hashlib

print("🤖 Personal AI Task & Reflection Agent - Simple Demo")
print("=" * 50)
print("This demo works WITHOUT an API key\n")

# Simple task structure
class SimpleTask:
    def __init__(self, title, priority="MEDIUM"):
        self.id = hashlib.md5(title.encode()).hexdigest()[:8]
        self.title = title
        self.priority = priority
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.status = "TODO"
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'priority': self.priority,
            'status': self.status,
            'created_at': self.created_at
        }

# Simple agent without LLM
class SimpleAgent:
    def __init__(self):
        self.tasks = []
        self.diary_entries = []
        print("✅ Agent initialized (No API mode)\n")
    
    def create_task(self, title, priority="MEDIUM"):
        task = SimpleTask(title, priority)
        self.tasks.append(task)
        return task
    
    def add_diary(self, content):
        # Simple mood detection without AI
        mood = "NEUTRAL"
        if any(word in content.lower() for word in ['happy', 'great', 'excellent']):
            mood = "HAPPY"
        elif any(word in content.lower() for word in ['sad', 'tired', 'stressed']):
            mood = "SAD"
        
        entry = {
            'content': content[:50] + '...' if len(content) > 50 else content,
            'mood': mood,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.diary_entries.append(entry)
        return entry
    
    def list_tasks(self):
        if not self.tasks:
            return "No tasks yet!"
        
        result = "📋 Your Tasks:\n"
        for task in self.tasks:
            result += f"  • {task.title} [{task.priority}] - {task.status}\n"
        return result
    
    def get_stats(self):
        return {
            'total_tasks': len(self.tasks),
            'diary_entries': len(self.diary_entries),
            'agent_type': 'SimpleAgent (No API)'
        }

# Demo the agent
agent = SimpleAgent()

# Demo 1: Create tasks
print("📝 Demo 1: Creating Tasks")
print("-" * 30)
tasks_to_create = [
    ("Complete AI Agents capstone project", "HIGH"),
    ("Review course materials", "MEDIUM"),
    ("Test multi-agent features", "HIGH")
]

for title, priority in tasks_to_create:
    task = agent.create_task(title, priority)
    print(f"✅ Created: {task.title} [Priority: {task.priority}]")

print("\n" + agent.list_tasks())

# Demo 2: Diary entries
print("\n📔 Demo 2: Diary Entries")
print("-" * 30)
diary_entries = [
    "Feeling great! Made good progress on the capstone project today.",
    "A bit tired but still pushing through. The multi-agent system is fascinating.",
    "Stressed about the deadline but learning so much!"
]

for entry_text in diary_entries:
    entry = agent.add_diary(entry_text)
    print(f"📝 Entry added - Mood: {entry['mood']}")
    print(f"   \"{entry['content']}\"")

# Demo 3: Statistics
print("\n📊 Demo 3: Agent Statistics")
print("-" * 30)
stats = agent.get_stats()
print(json.dumps(stats, indent=2))

# Demo 4: What the full version offers
print("\n🚀 Full Version Features (with API):")
print("-" * 30)
print("✨ AI-powered task breakdown into subtasks")
print("✨ Natural language understanding")
print("✨ Advanced mood analysis from diary text")
print("✨ Pattern recognition and insights")
print("✨ Multi-agent orchestration")
print("✨ Production features (caching, rate limiting)")
print("✨ SQLite database for persistence")

print("\n📌 To enable full features:")
print("1. Get API key from: https://makersuite.google.com/app/apikey")
print("2. Run: export GEMINI_API_KEY='your-key'")
print("3. Run: python3 test_setup.py (to verify)")
print("4. Run: python3 demo.py (full demo)")

print("\n✅ This proves your Python environment is working correctly!")
print("   The issue is just with the API configuration.\n")
