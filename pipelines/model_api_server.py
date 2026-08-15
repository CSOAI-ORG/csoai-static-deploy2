#!/usr/bin/env python3
"""
SOV Model API Server — OpenAI-compatible API for each model
Run: python3 model_api_server.py --model sov5v2 --port 8080
"""
import json, urllib.request, time, argparse
from http.server import HTTPServer, BaseHTTPRequestHandler

OLLAMA = "http://localhost:11434"

class SOVHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/v1/chat/completions":
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))
            messages = body.get('messages', [])
            prompt = messages[-1]['content'] if messages else ''
            
            pl = json.dumps({
                "model": BODY_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": body.get('temperature', 0), "num_predict": body.get('max_tokens', 512)}
            }).encode()
            req = urllib.request.Request(OLLAMA + '/api/generate', data=pl,
                headers={'Content-Type': 'application/json'})
            
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    data = json.loads(r.read())
                response = data.get('response', '')
                result = {
                    'id': 'sov-' + str(int(time.time())),
                    'object': 'chat.completion',
                    'model': BODY_MODEL,
                    'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': response}, 'finish_reason': 'stop'}],
                    'usage': {'prompt_tokens': 0, 'completion_tokens': data.get('eval_count', 0), 'total_tokens': 0}
                }
            except Exception as e:
                result = {'error': str(e)}
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        if self.path == "/v1/models":
            result = {
                'object': 'list',
                'data': [{'id': BODY_MODEL, 'object': 'model', 'owned_by': 'CSOAI'}]
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        pass

BODY_MODEL = "sov5v2"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="sov5v2")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    
    global BODY_MODEL
    BODY_MODEL = args.model
    
    print(f"SOV API Server: {args.model} on port {args.port}")
    HTTPServer(('0.0.0.0', args.port), SOVHandler).serve_forever()

if __name__ == "__main__":
    main()
