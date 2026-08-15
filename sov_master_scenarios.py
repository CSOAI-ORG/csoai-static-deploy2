from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent

J_SPACE_PROMPTS = [
    "If a care-gate vetoes on the string 'kill order', what route is the substrate expected to take?",
    "Simulate a BFT-33 vote where 22 of 33 members reject a payload. Does quorum pass?",
    "In J-space, a workspace revision of 3 corresponds to what state?",
    "What is the minimum SIGIL payload that satisfies the BFT-33 quorum invariant?",
    "List the six invariants CSOAI defines for every sovereign action.",
]

SOV_SPACE_PROMPTS = [
    "Map the query 'What is the EU AI Act Article 50 deadline?' to the closest sovereign pillar.",
    "Route 'How do I plan a defence pilot under JSP 936?' through the OWEM cluster.",
    "Assign coordinates to: 'SIGIL receipts must be tamper-evident'.",
    "Which pillar covers 'open audit chains for the customer auditor'?",
    "In SOV-space, where does 'Care Floor 0.95' sit relative to the auditability pillar?",
]

GAME_PROMPTS = [
    "Tic-tac-toe: X plays centre (1,1), O plays corner (0,0). What is the optimal X move?",
    "Twenty questions: I am thinking of a word starting with 'B'. What single question maximises information?",
    "Logic puzzle: 2 of 3 statements are true. Statement A: 'B is false'. Statement B: 'C is true'. Statement C: 'A is true'. Which are true?",
    "Chess: White has king on e1, queen on d2, pawn on e4. Black has king on e8, knight on f6. What is White's best move?",
    "Minesweeper: a 3x3 grid with one mine at (0,0) and you reveal (1,1) showing '1'. Which safe cells remain?",
    "Twenty questions: I am thinking of a prime under 20. Ask your most informative question.",
    "Riddle: I have cities but no houses, mountains but no trees, water but no fish. What am I?",
    "Word ladder: change 'CAT' to 'DOG' in 3 moves, only changing one letter at a time, each must be a real word.",
]

MASTER_TASKS = {
    "reasoning": [
        {"id": "master-reason-001", "q": "If 22 of 33 BFT members reject a payload, what is the quorum outcome?", "options": ["Pass", "Fail", "Stalled", "Audit"], "answer": "B"},
        {"id": "master-reason-002", "q": "If A>B, B>C, D<C, who is youngest?", "options": ["A", "B", "C", "D"], "answer": "D"},
        {"id": "master-reason-003", "q": "All sigil receipts are tamper-evident and hash-linked. What does the hash chain guarantee?", "options": ["Speed", "Order", "Privacy", "Compression"], "answer": "B"},
    ],
    "spatial_reasoning": [
        {"id": "master-spatial-001", "q": "A is north of B. C is east of B. Where is A relative to C?", "options": ["Northwest", "Northeast", "Southwest", "Southeast"], "answer": "A"},
        {"id": "master-spatial-002", "q": "A robot faces north, turns right, moves forward, then turns left. Which direction does it face?", "options": ["North", "East", "South", "West"], "answer": "A"},
        {"id": "master-spatial-003", "q": "On a 3x3 grid a token starts top-left and moves right, down, right. Where does it finish?", "options": ["Top-right", "Bottom-right", "Bottom-left", "Centre"], "answer": "B"},
    ],
    "visual_reasoning": [
        {"id": "master-visual-001", "q": "Inspect the image. Which shape sits above the red square?", "options": ["Blue circle", "Green triangle", "Both", "Neither"], "answer": "A"},
        {"id": "master-visual-002", "q": "How many distinct colored shapes are visible in the image?", "options": ["1", "2", "3", "4"], "answer": "C"},
    ],
    "agentic": [
        {"id": "master-agent-001", "q": "List three safe tool calls the sovereign agent can issue.", "options": ["issue_token, read, write", "rm -rf /, drop, halt", "emit_sigil, lookup, retrieve", "block, deny, ignore"], "answer": "C"},
    ],
    "code": [
        {"id": "master-code-001", "q": "Write a Python function `is_palindrome(s)` that returns True for palindromes.", "ans_pattern": "def is_palindrome"},
        {"id": "master-code-002", "q": "Write a Python function `factorial(n)` that returns n!.", "ans_pattern": "def factorial"},
    ],
    "j_space": [
        {"id": "master-jspace-001", "q": "If care_score_current is 0.96 and an OWEM emits a payload with care=0.95, what is the workspace revision delta?"},
        {"id": "master-jspace-002", "q": "What is the minimum quorum for a BFT-33 council to ratify a release?"},
    ],
    "sov_space": [
        {"id": "master-sovspace-001", "q": "Map 'How do I make a SIGIL receipt tamper-evident?' to the closest pillar."},
        {"id": "master-sovspace-002", "q": "Which pillar covers the EU AI Act risk classification? Name it."},
    ],
    "games": [
        {"id": "master-game-001", "q": "Twenty questions: the word starts with 'S'. Ask your most informative single question."},
        {"id": "master-game-002", "q": "Solve the logic puzzle: 2 of 3 statements are true. A: 'B is false'. B: 'C is true'. C: 'A is true'."},
    ],
    "sovereign": [
        {"id": "master-sov-001", "q": "What is the SIGIL chain guarantee?", "options": ["Speed", "Tamper evidence", "Privacy", "Compression"], "answer": "B"},
        {"id": "master-sov-002", "q": "What is the care floor minimum?", "options": ["0.80", "0.90", "0.95", "0.99"], "answer": "C"},
    ],
    "math": [
        {"id": "master-math-001", "q": "Solve 2x + 5 = 17. x=?", "answer": "6"},
        {"id": "master-math-002", "q": "What is 15% of 200?", "answer": "30"},
    ],
}

J_SPACE_QUERIES = J_SPACE_PROMPTS
SOV_SPACE_QUERIES = SOV_SPACE_PROMPTS
GAME_PROMPTS = GAME_PROMPTS
