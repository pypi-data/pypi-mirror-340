"""
🎵 RAGTune: A Pseudo-Finetuning RAG Framework

Built by Joshikaran K. (aka Joshi Felix)
🔗 github.com/Joshikarank
"""

from .core import ragtune

# Optional intro on import
def _intro():
    print("\n🎵  RAGTUNE: A Pseudo-Finetuning RAG Framework  🎵")
    print("🧠  JSON Semantic Retriever for LLM Agents")
    print("💡  Built with soul by Joshikaran K. (@Joshikarank)\n")

_intro()  # uncomment to show intro on import
import os

def _show_intro_once():
    flag_path = os.path.expanduser("~/.ragtune_intro_seen")
    if not os.path.exists(flag_path):
        print(r"""
🎵  RAGTune - A Pseudo-Finetuning RAG Framework
-----------------------------------------------
📦 Semantic retrieval from JSON without finetuning.
💡 Built by: Joshikaran K  |  github.com/Joshikarank

🚀 Tip: Run `python -m ragtune your.json` to get started!
""")
        with open(flag_path, "w") as f:
            f.write("shown")

_show_intro_once()
