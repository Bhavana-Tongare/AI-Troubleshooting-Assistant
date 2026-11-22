from dotenv import load_dotenv
from retrieve import search 
from groq import Groq
import os
import json


load_dotenv()

# Groq client
groq_client = Groq(
    api_key = os.getenv("GROQ_API_KEY")
)



def ask_groq(question, kb_entry):

    prompt = f""" 
                You are a troubleshooting assistant.

                STRICT RULES:
                1. Use ONLY the retrieved knowledge base information.
                2. Do not add information from your general knowledge.
                3. Do not invent possible causes, solutions, commands, or prevention tips.
                4. Do not create a separate Possible Causes or Prevention section.
                5. Explain the diagnostic_checks and known_resolution
                without changing their meaning.
                6. If information is missing, clearly state that it
                is not available in the knowledge base.
    
              KNOWLEDGE BASE ID:
                {kb_entry["id"]}

                USER PROBLEM:
                {question}

                RETRIEVED KNOWLEDGE BASE:
                {json.dumps(kb_entry, indent=2)}


              Write the response in exactly this format:

                Knowledge Base Reference
                Mention the Knowledge Base ID.

               1. Identified Problem
                Explain the issue using the knowledge base.

                2. Step-by-Step Troubleshooting Checks
                Present every diagnostic check as a numbered step.
                Do not add new checks.

                3. Recommended Solutions
                Explain the known resolution from the knowledge base.
                Use numbered steps where possible.
                Do not invent solutions.
                
                4. Escalation Team
                Mention the escalation team exactly as provided.

                If any information is missing, write:
                "Not specified in the knowledge base."

                Use simple, professional language.
    
        """
    response = groq_client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.3,
    max_tokens=500
)

    return response.choices[0].message.content



