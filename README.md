# 🧠 Adaptive Taxonomy Mapper

## 🔍 Overview

The **Adaptive Taxonomy Mapper** is an intelligent content classification system designed to map messy user tags + story descriptions into precise internal categories using a controlled LLM-based reasoning pipeline.

Instead of blindly trusting AI outputs, the system treats the LLM as a **Simulator LLM** — a constrained reasoning component inside a rule-driven architecture. Final decisions are enforced programmatically, not by the model.

---

## 🎯 Problem Statement

User-generated content is often incorrectly or vaguely tagged (e.g., "Love", "Scary").  
However, recommendation engines require accurate, fine-grained taxonomy mapping such as:

- **Enemies-to-Lovers**
- **Gothic Horror**
- **Legal Thriller**
- **Hard Sci-Fi**

The system must:

1. Prioritize story meaning over user tags
2. Return `[UNMAPPED]` for non-fiction
3. Strictly follow the given taxonomy hierarchy
4. Explain why a decision was made

---

## ✅ Core Rules Implemented

### 1️⃣ Context Wins
If tags say "Action" but the description is legal drama → map to **Legal Thriller**.

### 2️⃣ Honesty Rule
If the story does not fit the taxonomy (e.g., recipes, tutorials):  
→ `[UNMAPPED]`

### 3️⃣ Hierarchy Rule
Only categories explicitly listed in `taxonomy.json` are allowed.  
No hallucinated labels are accepted.

---

## ✨ Key Features

✔ Uses LLM for reasoning, but system remains in control  
✔ Strict JSON-based output enforcement  
✔ Anti-hallucination validation layer  
✔ Taxonomy hierarchy verification  
✔ Generates detailed reasoning logs  
✔ Works offline for taxonomy validation logic  
✔ Successfully processes all 10 challenge test cases  

---

## 🧩 System Architecture

```
Input (Tags + Blurb)
       ↓
Prompt Builder
       ↓
Simulator LLM (Groq – Llama 3.3 70B)
       ↓
Validation Layer
  ✓ Hierarchy Check
  ✓ Approved Category List
  ✓ Honest UNMAPPED Handling
       ↓
Final Output + Reasoning Log
```

---

## ⚙️ How It Works

### 1️⃣ Load and Flatten Taxonomy
- Extracts all valid sub-genres
- Builds lookup map → `Main > Genre > SubGenre`
- Enables validation + formatting

### 2️⃣ Build Controlled Prompt
Prompt enforces:
- Rules
- Taxonomy
- Valid category list
- JSON-only output
- Clarity in ambiguous cases

### 3️⃣ Call Groq LLM (Simulator Mode)
- `temperature = 0` → deterministic
- Strict JSON response enforced

### 4️⃣ Validate Output
- If response not in taxonomy → `[UNMAPPED]`
- If valid → formatted as: `Fiction > Genre > SubGenre`

### 5️⃣ Generate Reasoning Log
Produces:
- `mapped_category`
- `reasoning`
- `input_tags`
- `story-blurb`

---

## 📁 Output Example

```json
"case_9": {
  "input_tags": ["Ghost"],
  "blurb": "A masked killer stalks a group of teenagers at a summer camp.",
  "mapped_category": "Fiction > Horror > Slasher",
  "reasoning": "Classic masked killer stalking teens matches Slasher sub-genre."
}
```

---

## 🚀 Tech Stack

- **Python 3.12+**
- **Groq API** (Llama-3.3-70B Versatile)
- **JSON Handling**
- **Structured Validation**

---

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/adaptive-taxonomy-mapper.git
cd adaptive-taxonomy-mapper
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install groq
```

4. Set your Groq API key:
```bash
export GROQ_API_KEY="your_api_key_here"  # On Windows: $env:GROQ_API_KEY="your_key"
```

5. Run the mapper:
```bash
python mapper.py
```

---

## 📂 Project Structure

```
project/
├── taxonomy.json          # Category definitions
├── test_cases.json        # 10 test cases
├── mapper.py             # Main inference engine
├── reasoning_log.json    # Output with reasoning
├── .gitignore            # Git exclusions
└── README.md             # This file
```

---

## 🧪 Results — Golden Test Cases

All 10 required tricky cases:

✅ Correct mapping produced  
✅ Ambiguous case handled with clear reasoning  
✅ Non-fiction correctly flagged `[UNMAPPED]`  

---

## 🏆 Evaluation Criteria Compliance

| Criterion | How It Is Satisfied |
|-----------|---------------------|
| **System Thinking** | Designed controlled AI pipeline, not blind AI use |
| **Technical Execution** | Clean architecture, modular, scalable |
| **AI Engineering** | Strong prompt strategy, JSON schema control, no hallucination |
| **Problem Decomposition** | Taxonomy handling, prompt builder, LLM caller, validator, logger |

---

## ⚠️ Limitations

- Depends on API availability
- Currently supports one taxonomy structure (easily extendable)

---

## 🚧 Future Enhancements

- [ ] Add batching + caching
- [ ] Support multi-taxonomy systems
- [ ] Confidence scoring
- [ ] Hybrid rule-based + ML fallback

---

## 📝 License

MIT License - feel free to use and modify.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## 📧 Contact

For questions or feedback, reach out via [GitHub Issues](https://github.com/yourusername/adaptive-taxonomy-mapper/issues).
