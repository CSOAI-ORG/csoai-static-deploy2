#!/usr/bin/env python3
"""
SOV Autonomous Agent — Browser control + Code execution + Web scraping
Uses Groq API for fast inference + Playwright for browser control
"""
import json, os, time, subprocess
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# GROQ API (Fast inference)
# ═══════════════════════════════════════════════════════════════
class GroqInference:
    """Fast inference using Groq API"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('GROQ_API_KEY')
        self.base_url = 'https://api.groq.com/openai/v1'
    
    def chat(self, messages, model='meta-llama/llama-4-scout-17b-16e-instruct'):
        """Chat completion via Groq"""
        import urllib.request
        payload = json.dumps({
            'model': model,
            'messages': messages,
            'temperature': 0,
            'max_tokens': 1024
        }).encode()
        req = urllib.request.Request(
            f'{self.base_url}/chat/completions',
            data=payload,
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except Exception as e:
            return {'error': str(e)}

# ═══════════════════════════════════════════════════════════════
# BROWSER CONTROL (Playwright)
# ═══════════════════════════════════════════════════════════════
class BrowserControl:
    """Control browser using Playwright"""
    
    def __init__(self):
        self.browser = None
        self.page = None
    
    def start(self):
        """Start browser"""
        try:
            from playwright.sync_api import sync_playwright
            self.pw = sync_playwright().start()
            self.browser = self.pw.chromium.launch(headless=False)
            self.page = self.browser.new_page()
            print("Browser started")
            return True
        except Exception as e:
            print(f"Browser error: {e}")
            return False
    
    def navigate(self, url):
        """Navigate to URL"""
        if self.page:
            self.page.goto(url)
            print(f"Navigated to {url}")
            return True
        return False
    
    def click(self, selector):
        """Click element"""
        if self.page:
            self.page.click(selector)
            return True
        return False
    
    def type_text(self, selector, text):
        """Type text into element"""
        if self.page:
            self.page.fill(selector, text)
            return True
        return False
    
    def screenshot(self, path='screenshot.png'):
        """Take screenshot"""
        if self.page:
            self.page.screenshot(path=path)
            return True
        return False
    
    def get_content(self):
        """Get page content"""
        if self.page:
            return self.page.content()
        return ''
    
    def stop(self):
        """Stop browser"""
        if self.browser:
            self.browser.close()
        if hasattr(self, 'pw'):
            self.pw.stop()

# ═══════════════════════════════════════════════════════════════
# CODE EXECUTION
# ═══════════════════════════════════════════════════════════════
class CodeExecutor:
    """Execute code in sandbox"""
    
    def execute(self, code, language='python'):
        """Execute code and return result"""
        if language == 'python':
            try:
                result = subprocess.run(
                    ['python3', '-c', code],
                    capture_output=True, text=True, timeout=10
                )
                return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
            except Exception as e:
                return {'error': str(e)}
        return {'error': f'Unsupported language: {language}'}

# ═══════════════════════════════════════════════════════════════
# SOV AUTONOMOUS AGENT
# ═══════════════════════════════════════════════════════════════
class SOVAgent:
    """Autonomous agent combining Groq + Browser + Code"""
    
    def __init__(self):
        self.groq = GroqInference()
        self.browser = BrowserControl()
        self.executor = CodeExecutor()
        self.history = []
    
    def think(self, task):
        """Use Groq to think about the task"""
        messages = [
            {'role': 'system', 'content': 'You are SOV, an autonomous AI agent. Think step by step about how to accomplish tasks.'},
            {'role': 'user', 'content': f'Task: {task}\n\nPlan:'}
        ]
        response = self.groq.chat(messages)
        return response.get('choices', [{}])[0].get('message', {}).get('content', '')
    
    def act(self, action):
        """Execute an action (browser click, code execution, etc.)"""
        if action['type'] == 'navigate':
            return self.browser.navigate(action['url'])
        elif action['type'] == 'click':
            return self.browser.click(action['selector'])
        elif action['type'] == 'type':
            return self.browser.type_text(action['selector'], action['text'])
        elif action['type'] == 'execute':
            return self.executor.execute(action['code'])
        elif action['type'] == 'screenshot':
            return self.browser.screenshot(action.get('path', 'screenshot.png'))
        return {'error': f'Unknown action type: {action["type"]}'}
    
    def run(self, task):
        """Run autonomous agent on task"""
        print(f"SOV Agent: {task}")
        
        # Think about the task
        plan = self.think(task)
        print(f"Plan: {plan[:200]}...")
        
        # Execute based on plan
        if 'browser' in plan.lower() or 'click' in plan.lower():
            self.browser.start()
            # Example: navigate to Kaggle
            self.browser.navigate('https://www.kaggle.com/competitions')
            time.sleep(2)
            self.browser.screenshot('kaggle.png')
            print("Screenshot saved to kaggle.png")
        
        return {'plan': plan, 'status': 'executed'}

if __name__ == '__main__':
    agent = SOVAgent()
    result = agent.run('Submit to Kaggle LLM Classification competition')
    print(json.dumps(result, indent=2))
