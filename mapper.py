import json
import os
from groq import Groq

class AdaptiveTaxonomyMapper:
    def __init__(self, taxonomy_path, api_key=None):
        with open(taxonomy_path, 'r') as f:
            self.taxonomy = json.load(f)
        
        self.valid_subgenres = []
        self.genre_map = {}
        
        # Flatten taxonomy for validation
        for main_category, genres_dict in self.taxonomy.items():
            for sub_genre, specifics_list in genres_dict.items():
                for specific in specifics_list:
                    self.valid_subgenres.append(specific)
                    self.genre_map[specific] = {
                        "main": main_category, "sub": sub_genre, "specific": specific
                    }
        
        # Initialize Groq Client
        api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Groq API Key not found. Set GROQ_API_KEY environment variable.")
        
        self.client = Groq(api_key=api_key)

    def validate_and_format(self, raw_category):
        """Validates category exists in taxonomy, prevents hallucination."""
        if raw_category == "[UNMAPPED]":
            return "[UNMAPPED]"
        if raw_category in self.valid_subgenres:
            info = self.genre_map[raw_category]
            return f"{info['main']} > {info['sub']} > {info['specific']}"
        return "[UNMAPPED]"

    def build_prompt(self, tags, blurb):
        """Constructing prompt with the 3 core rules."""
        taxonomy_str = json.dumps(self.taxonomy, indent=2)
        valid_cats = ", ".join(self.valid_subgenres)

        return f"""You are a content categorization expert. 
Map the story to our taxonomy using these rules:

1. CONTEXT WINS: Prioritize the story blurb over tags.
2. HONESTY: Return "[UNMAPPED]" ONLY for non-fiction instructional content (how-to guides, recipes, tutorials). Fiction stories that discuss science or technology should still be mapped to appropriate fiction genres.
3. HIERARCHY: Only use sub-genres from the valid list below.

TAXONOMY: 
{taxonomy_str}

VALID LIST: 
{valid_cats}

IMPORTANT DISTINCTIONS:
- "How to build a telescope" = [UNMAPPED] (instructional)
- "A story exploring the physics of FTL travel" = Hard Sci-Fi (fiction with technical elements)
- "Mix flour and sugar" = [UNMAPPED] (recipe)

INPUT:
Tags: {tags}
Blurb: "{blurb}"

Respond ONLY in valid JSON format:
{{"mapped_category": "SubGenreName or [UNMAPPED]", "reasoning": "Explanation"}}"""

    def call_llm(self, prompt):
        """Calls Groq API and returns parsed JSON response."""
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0,
                response_format={"type": "json_object"}
            )
            return json.loads(chat_completion.choices[0].message.content)
        except Exception as e:
            return {"mapped_category": "[UNMAPPED]", "reasoning": f"Groq Error: {str(e)}"}

    def process_test_cases(self, test_path):
        """Iterates through test cases and generates reasoning log."""
        with open(test_path, 'r') as f:
            cases = json.load(f)
        
        final_log = {}
        for i, case in enumerate(cases, 1):
            case_id = case.get('id', i)
            print(f"Processing case {case_id}/{len(cases)} via Groq...")
            res = self.call_llm(self.build_prompt(case.get('tags', []), case.get('blurb', "")))

            final_log[f"case_{case_id}"] = {
                "input_tags": case.get('tags', []),
                "blurb": case.get('blurb', ""),
                "mapped_category": self.validate_and_format(res.get("mapped_category")),
                "reasoning": res.get("reasoning", "No reasoning provided.")
            }
        return final_log


if __name__ == "__main__":
    mapper = AdaptiveTaxonomyMapper("taxonomy.json")
    log = mapper.process_test_cases("test_cases.json")
    
    with open("reasoning_log.json", "w") as f:
        json.dump(log, f, indent=4)
    
    # Print summary
    unmapped = sum(1 for v in log.values() if v['mapped_category'] == '[UNMAPPED]')
    print(f"\n✓ Groq processing complete. reasoning_log.json created.")
    print(f"✓ Processed {len(log)} cases")
    print(f"✓ Mapped: {len(log) - unmapped}, Unmapped: {unmapped}")