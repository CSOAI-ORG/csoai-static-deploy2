#!/usr/bin/env python3
"""SOV-Space RAG Pipeline — Pure Python Implementation

Retrieval Augmented Generation for SOV-space honey knowledge.
No external dependencies — pure Python with hashlib-based embeddings.

Implements:
  1. Vector Database (in-memory with cosine similarity)
  2. RAG Pipeline (retrieve → augment → generate)
  3. HyDE (Hypothetical Document Embeddings)
  4. Chain-of-Thought (CoT) prompting
  5. Self-Consistency (majority voting)
  6. Reflexion (self-critique learning)
  7. Tree-of-Thought (ToT) reasoning
"""

import json
import hashlib
import math
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple

ROOT = Path(__file__).resolve().parent.parent


# ─── Pure Python Vector Store ────────────────────────────────────────────────

class VectorStore:
    """In-memory vector store with cosine similarity. No dependencies."""

    def __init__(self):
        self.vectors = []  # List of (id, embedding, metadata)
        self.dimension = 64  # Fixed dimension for hash-based embeddings

    def _embed(self, text: str) -> List[float]:
        """Generate a deterministic embedding from text using hashing."""
        # Create multiple hash-based features
        features = []
        for i in range(self.dimension):
            seed = f"{text}_{i}"
            h = hashlib.sha256(seed.encode()).hexdigest()
            # Convert first 8 hex chars to float
            val = int(h[:8], 16) / 0xFFFFFFFF
            features.append(val * 2 - 1)  # Normalize to [-1, 1]
        return features

    def add(self, doc_id: str, text: str, metadata: Dict = None):
        """Add a document to the store."""
        embedding = self._embed(text)
        self.vectors.append((doc_id, embedding, metadata or {}))

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float, Dict]]:
        """Search for similar documents using cosine similarity."""
        query_emb = self._embed(query)
        results = []
        for doc_id, doc_emb, metadata in self.vectors:
            sim = self._cosine_similarity(query_emb, doc_emb)
            results.append((doc_id, sim, metadata))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Compute cosine similarity between two vectors."""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)


# ─── RAG Pipeline ────────────────────────────────────────────────────────────

class RAGPipeline:
    """Retrieval Augmented Generation for SOV-space."""

    def __init__(self):
        self.store = VectorStore()
        self.knowledge = []
        self._load_knowledge()

    def _load_knowledge(self):
        """Load all honey knowledge into the vector store."""
        # Load bloodline
        bloodline_path = ROOT / "forest" / "bloodline.json"
        if bloodline_path.exists():
            data = json.load(open(bloodline_path))
            for entry in data.get("knowledge", []):
                content = entry.get("content", "")
                family = entry.get("family", "general")
                topic = entry.get("topic", "")
                doc_id = f"bloodline-{hashlib.sha256(content.encode()).hexdigest()[:8]}"
                self.store.add(doc_id, content, {"family": family, "topic": topic, "source": "bloodline"})
                self.knowledge.append(entry)

        # Load honey
        honey_path = ROOT / "forest" / "honey_chatml.jsonl"
        if honey_path.exists():
            for i, line in enumerate(open(honey_path)):
                try:
                    entry = json.loads(line.strip())
                    for msg in entry.get("conversations", []):
                        if msg.get("from") == "assistant":
                            content = msg["value"]
                            doc_id = f"honey-{i}"
                            self.store.add(doc_id, content, {"source": "honey", "index": i})
                except:
                    pass

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve relevant knowledge for a query."""
        results = self.store.search(query, top_k)
        retrieved = []
        for doc_id, score, metadata in results:
            # Find the original content
            for entry in self.knowledge:
                content = entry.get("content", "")
                if hashlib.sha256(content.encode()).hexdigest()[:8] in doc_id:
                    retrieved.append({
                        "content": content[:500],
                        "family": entry.get("family", "general"),
                        "topic": entry.get("topic", ""),
                        "score": round(score, 3),
                        "source": metadata.get("source", "unknown"),
                    })
                    break
        return retrieved

    def generate_prompt(self, query: str, retrieved: List[Dict]) -> str:
        """Generate an augmented prompt with retrieved context."""
        context = "\n".join([
            f"[{r['family']}] {r['topic']}: {r['content'][:200]}"
            for r in retrieved[:3]
        ])
        return f"""Context from SOV-space knowledge:
{context}

Question: {query}

Answer based on the context above:"""


# ─── HyDE (Hypothetical Document Embeddings) ─────────────────────────────────

class HyDE:
    """Hypothetical Document Embeddings for better retrieval."""

    def __init__(self, rag: RAGPipeline):
        self.rag = rag

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve using HyDE: generate hypothetical answer, then retrieve."""
        # Step 1: Generate hypothetical answer
        hypothetical = self._generate_hypothetical(query)

        # Step 2: Retrieve using the hypothetical answer
        results = self.rag.store.search(hypothetical, top_k)

        retrieved = []
        for doc_id, score, metadata in results:
            for entry in self.rag.knowledge:
                content = entry.get("content", "")
                if hashlib.sha256(content.encode()).hexdigest()[:8] in doc_id:
                    retrieved.append({
                        "content": content[:500],
                        "family": entry.get("family", "general"),
                        "topic": entry.get("topic", ""),
                        "score": round(score, 3),
                    })
                    break
        return retrieved

    def _generate_hypothetical(self, query: str) -> str:
        """Generate a hypothetical answer document."""
        # Simple heuristic: expand the query with related terms
        terms = query.lower().split()
        expanded = []
        for term in terms:
            expanded.append(term)
            # Add related terms based on common patterns
            if "eu" in term or "ai" in term:
                expanded.extend(["regulation", "compliance", "article"])
            if "sovereign" in term:
                expanded.extend(["bft", "sigil", "care floor"])
            if "model" in term:
                expanded.extend(["training", "inference", "benchmark"])
        return " ".join(expanded)


# ─── Chain-of-Thought (CoT) ──────────────────────────────────────────────────

class ChainOfThought:
    """Chain-of-Thought prompting for step-by-step reasoning."""

    @staticmethod
    def generate_prompt(question: str, context: str = "") -> str:
        """Generate a CoT prompt."""
        return f"""Think step by step.

{f'Context: {context}' if context else ''}

Question: {question}

Let me think through this step by step:
1. First, I need to understand what's being asked.
2. Then, I'll consider the relevant knowledge.
3. Finally, I'll arrive at the answer.

Step-by-step reasoning:"""

    @staticmethod
    def parse_reasoning(response: str) -> Dict:
        """Parse a CoT response into steps and final answer."""
        steps = []
        lines = response.strip().split("\n")
        current_step = ""
        for line in lines:
            if re.match(r"^\d+\.", line.strip()):
                if current_step:
                    steps.append(current_step.strip())
                current_step = line
            else:
                current_step += " " + line
        if current_step:
            steps.append(current_step.strip())

        # Last line is usually the answer
        answer = lines[-1].strip() if lines else ""

        return {"steps": steps, "answer": answer, "num_steps": len(steps)}


# ─── Self-Consistency ────────────────────────────────────────────────────────

class SelfConsistency:
    """Self-Consistency: generate N paths, pick most common answer."""

    @staticmethod
    def vote(responses: List[str]) -> Dict:
        """Vote on multiple responses to find the most consistent answer."""
        # Normalize answers
        normalized = []
        for resp in responses:
            # Extract the key answer (last sentence or first number)
            answer = resp.strip().split("\n")[-1].strip()
            normalized.append(answer)

        # Count occurrences
        counts = {}
        for ans in normalized:
            # Simple normalization
            key = ans.lower().strip()
            counts[key] = counts.get(key, 0) + 1

        # Find majority
        if counts:
            majority = max(counts, key=counts.get)
            confidence = counts[majority] / len(responses)
        else:
            majority = ""
            confidence = 0.0

        return {
            "majority_answer": majority,
            "confidence": round(confidence, 3),
            "total_responses": len(responses),
            "unique_answers": len(counts),
            "distribution": counts,
        }


# ─── Reflexion ───────────────────────────────────────────────────────────────

class Reflexion:
    """Reflexion: learn from failures via verbal self-critique."""

    def __init__(self):
        self.memory = []  # List of (task, attempt, critique, improvement)

    def reflect(self, task: str, attempt: str, expected: str, actual: str) -> Dict:
        """Generate a reflection on a failed attempt."""
        # Determine if it was a success or failure
        success = self._check_success(expected, actual)

        if success:
            critique = "The approach worked well."
            improvement = "Continue with the same strategy."
        else:
            critique = self._generate_critique(expected, actual)
            improvement = self._generate_improvement(expected, actual)

        reflection = {
            "task": task,
            "attempt": attempt[:200],
            "expected": expected,
            "actual": actual[:200],
            "success": success,
            "critique": critique,
            "improvement": improvement,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        self.memory.append(reflection)
        return reflection

    def _check_success(self, expected: str, actual: str) -> bool:
        """Check if the attempt was successful."""
        exp = expected.lower().strip()
        act = actual.lower().strip()
        if exp in act:
            return True
        # Check for number match
        exp_nums = set(re.findall(r"\d+\.?\d*", exp))
        act_nums = set(re.findall(r"\d+\.?\d*", act))
        if exp_nums and act_nums and (exp_nums & act_nums):
            return True
        return False

    def _generate_critique(self, expected: str, actual: str) -> str:
        """Generate a critique of the failed attempt."""
        return f"Expected '{expected}' but got '{actual}'. The reasoning was incomplete or incorrect."

    def _generate_improvement(self, expected: str, actual: str) -> str:
        """Generate an improvement suggestion."""
        return f"Focus on the key concept: '{expected}'. Use more specific knowledge."

    def get_learnings(self) -> List[Dict]:
        """Get all learned reflections."""
        return [r for r in self.memory if not r["success"]]


# ─── Tree-of-Thought (ToT) ──────────────────────────────────────────────────

class TreeOfThought:
    """Tree-of-Thought: explore multiple reasoning branches."""

    @staticmethod
    def generate_branches(question: str, num_branches: int = 3) -> List[Dict]:
        """Generate multiple reasoning branches for a question."""
        branches = []
        for i in range(num_branches):
            branch = {
                "id": i,
                "approach": f"Approach {i+1}",
                "reasoning": f"Branch {i+1}: Consider {question} from perspective {i+1}.",
                "confidence": 0.5 + (i * 0.1),  # Simulated confidence
                "sub_branches": [],
            }
            branches.append(branch)
        return branches

    @staticmethod
    def evaluate_branches(branches: List[Dict]) -> Dict:
        """Evaluate and select the best branch."""
        if not branches:
            return {"best_branch": None, "score": 0}

        best = max(branches, key=lambda b: b.get("confidence", 0))
        return {
            "best_branch": best["id"],
            "best_approach": best["approach"],
            "score": best["confidence"],
            "all_scores": {b["id"]: b["confidence"] for b in branches},
        }


# ─── Main Integration ────────────────────────────────────────────────────────

class SOVRAG:
    """Unified RAG system for SOV-space."""

    def __init__(self):
        self.rag = RAGPipeline()
        self.hyde = HyDE(self.rag)
        self.cot = ChainOfThought()
        self.self_consistency = SelfConsistency()
        self.reflexion = Reflexion()
        self.tot = TreeOfThought()

    def query(self, question: str, method: str = "rag") -> Dict:
        """Query the SOV-space knowledge base."""
        if method == "rag":
            retrieved = self.rag.retrieve(question)
            prompt = self.rag.generate_prompt(question, retrieved)
        elif method == "hyde":
            retrieved = self.hyde.retrieve(question)
            prompt = self.rag.generate_prompt(question, retrieved)
        elif method == "cot":
            retrieved = self.rag.retrieve(question)
            context = "\n".join([r["content"][:100] for r in retrieved[:2]])
            prompt = self.cot.generate_prompt(question, context)
        elif method == "tot":
            branches = self.tot.generate_branches(question)
            evaluation = self.tot.evaluate_branches(branches)
            return {"method": "tot", "branches": branches, "evaluation": evaluation}
        else:
            retrieved = self.rag.retrieve(question)
            prompt = self.rag.generate_prompt(question, retrieved)

        return {
            "method": method,
            "question": question,
            "retrieved": retrieved,
            "prompt": prompt,
            "num_retrieved": len(retrieved),
        }

    def get_state(self) -> Dict:
        """Get the RAG system state."""
        return {
            "vector_store_size": len(self.rag.store.vectors),
            "knowledge_entries": len(self.rag.knowledge),
            "reflexion_memory": len(self.reflexion.memory),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  SOV-SPACE RAG PIPELINE — Pure Python                  ║")
    print("║  Vector Store · HyDE · CoT · Self-Consistency · ToT    ║")
    print("╚══════════════════════════════════════════════════════════╝")

    sov_rag = SOVRAG()

    # Show state
    state = sov_rag.get_state()
    print(f"\n─── RAG STATE ───")
    print(f"  Vector store: {state['vector_store_size']} documents")
    print(f"  Knowledge entries: {state['knowledge_entries']}")
    print(f"  Reflexion memory: {state['reflexion_memory']}")

    # Test RAG
    print(f"\n─── RAG QUERY ───")
    result = sov_rag.query("What is the BFT council quorum?", method="rag")
    print(f"  Question: {result['question']}")
    print(f"  Retrieved: {result['num_retrieved']} documents")
    for r in result["retrieved"][:3]:
        print(f"    {r['family']:15s} {r['topic']:20s} score={r['score']}")

    # Test HyDE
    print(f"\n─── HyDE QUERY ───")
    result = sov_rag.query("What is the BFT council quorum?", method="hyde")
    print(f"  Retrieved: {result['num_retrieved']} documents")

    # Test CoT
    print(f"\n─── CoT PROMPT ───")
    result = sov_rag.query("How does the care floor work?", method="cot")
    print(f"  Prompt length: {len(result['prompt'])} chars")

    # Test ToT
    print(f"\n─── TREE OF THOUGHT ───")
    result = sov_rag.query("What is the best strategy for EU AI Act compliance?", method="tot")
    print(f"  Branches: {len(result['branches'])}")
    print(f"  Best: {result['evaluation']['best_approach']} (score: {result['evaluation']['score']})")

    # Test Self-Consistency
    print(f"\n─── SELF-CONSISTENCY ───")
    responses = ["23", "23 out of 33", "The quorum is 23", "23 members", "23"]
    vote = sov_rag.self_consistency.vote(responses)
    print(f"  Majority: {vote['majority_answer']}")
    print(f"  Confidence: {vote['confidence']}")

    # Test Reflexion
    print(f"\n─── REFLEXION ───")
    reflection = sov_rag.reflexion.reflect(
        task="What is the BFT quorum?",
        attempt="The quorum is 33",
        expected="23",
        actual="33",
    )
    print(f"  Success: {reflection['success']}")
    print(f"  Critique: {reflection['critique']}")
    print(f"  Improvement: {reflection['improvement']}")

    # Save
    output = {
        "state": state,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    out_path = ROOT / "sov_space" / "rag_state.json"
    out_path.write_text(json.dumps(output, indent=2))
    print(f"\n  Saved: {out_path}")


if __name__ == "__main__":
    main()
