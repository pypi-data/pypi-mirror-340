# ragtune/core.py
import json
import numpy as np
from typing import Optional
from sentence_transformers import SentenceTransformer

class ragtune:
    def __init__(self, json_path: str, model_name: Optional[str] = None, show_intro: bool = False):
        self.json_path = json_path
        self.data = self._load_data()
        if show_intro:
            self._print_intro()

        try:
            self.model = SentenceTransformer("BAAI/bge-large-en-v1.5")
        except Exception as e:
            print("⚠️  BGE model not found or failed to load.")
            print("💡  Tip: Run this to install it manually:\n")
            print("    >>> from sentence_transformers import SentenceTransformer")
            print("    >>> SentenceTransformer('BAAI/bge-large-en-v1.5')\n")
            raise e

        self.embed_prompt = "Represent this sentence for retrieval: "
        self.key_embeddings = {key: self._embed(key) for key in self.data}
        self.retrieved_keys_history = set()
    def _print_intro(self):
        print("\n" + "="*60)
        print("🎵  RAGTUNE: Pseudo-Finetuning RAG Framework")
        print("🧠  JSON-based semantic memory retriever")
        print("💡  Created by Joshikaran K | github.com/Joshikarank")
        print("="*60 + "\n")

    def _load_data(self):
        with open(self.json_path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def _suggest_cleaning_if_needed(self):
        """
        Suggest using the cleaner if the JSON is deeply nested.
        """
        nested_keys = [k for k, v in self.data.items() if isinstance(v, (dict, list))]
        if len(nested_keys) > 0:
            print("\n💡 Tip: Your JSON contains nested structures. Consider flattening it using:")
            print("     👉  python -m ragtune.utils.json_cleaner your_file.json --output flat.json\n")


    def _embed(self, text: str) -> np.ndarray:
        return self.model.encode([self.embed_prompt + text], normalize_embeddings=True)[0]

    def _format_entry(self, value):
        if isinstance(value, list):
            if value and isinstance(value[0], dict):
                return "\n\n".join(json.dumps(item, indent=2) for item in value)
            return "\n".join(str(v) for v in value)
        return str(value)

    def retrieve(self, query: str) -> str:
        query_vec = self._embed(query)
        scores = {key: np.dot(query_vec, key_vec) for key, key_vec in self.key_embeddings.items()}
        best_key = max(scores, key=scores.get)
        score = scores[best_key]

        print(f"\n🔍 Best matching section: {best_key} (score: {score:.4f})")

        if best_key in self.retrieved_keys_history:
            return f"(Already discussed **{best_key}** earlier. Check above if needed.)"

        self.retrieved_keys_history.add(best_key)
        value = self.data[best_key]
        return self._format_entry(value)

# CLI Entry Point
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="🎵 RAGTune: JSON-based Semantic Retriever — Pseudo-Finetuning for LLMs"
    )
    parser.add_argument("json_file", nargs="?", help="Path to your structured JSON memory file")
    parser.add_argument("--show-intro", action="store_true", help="Show animated intro on start")
    parser.add_argument("--help-advanced", action="store_true", help="Show extra tips and usage patterns")
    args = parser.parse_args()

    if args.help_advanced:
        print("""
📘 Advanced RAGTune Usage — Pseudo-Finetuning Tips

🧠 What it does:
  RAGTune avoids costly model finetuning by injecting memory retrieved from a structured JSON file.
  It uses semantic similarity (BGE embeddings) to find the best match and returns formatted context.

💡 Use Cases:
  - Digital Twins (identity bots)
  - Personal Assistants
  - Chatbot Memory Injection
  - Resume Bots / Project Showcases
  - Rapid RAG Prototypes

📓 Tips:
  - Use readable keys and clean nested JSON (lists, dicts, etc.)
  - Summarize long chat history using HuggingFace's summarization pipeline to save tokens.
  - Memory can be updated anytime without retraining — just update the JSON.
  - Model used: BAAI/bge-large-en-v1.5 (auto-downloaded)

📦 Quick Test:
  python -m ragtune your_memory.json

  Then type your queries in the CLI.

Built by Joshikaran K. | github.com/Joshikarank
        """)
        exit()

    if not args.json_file:
        print("❌ JSON file required.\nRun with --help for more info.")
        exit()

    retriever = ragtune(args.json_file, show_intro=args.show_intro)

    print("\n🎵 RAGTune is Ready! Type your question (or 'exit' to quit):\n")
    while True:
        user_input = input("> ").strip()
        if user_input.lower() in ["exit", "quit"]:
            break
        if user_input:
            result = retriever.retrieve(user_input)
            print(f"\n📦 Result:\n{result}\n")
