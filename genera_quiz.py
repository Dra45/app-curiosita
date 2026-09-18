import os
import json
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Aggiungiamo un elemento casuale basato sul timestamp o una richiesta esplicita di massima variabilità
prompt = """
Genera esattamente 6 domande di cultura generale di vario livello (storia, scienza, geografia, arte, tecnologia) a risposta multipla (4 opzioni ciascuna). 
IMPORTANTE: Scegli argomenti sempre nuovi, unici e completamente diversi dai quiz standard, variando drasticamente i temi.
RISPONDI ESCLUSIVAMENTE IN FORMATO JSON VALIDO, senza blocchi di codice markdown (niente ```json ... ```), rispettando esattamente questa struttura:
{
  "domande": [
    {
      "domanda": "Testo della domanda?",
      "opzioni": ["Opzione A", "Opzione B", "Opzione C", "Opzione D"],
      "risposta_corretta": "L'opzione esatta identica a una di quelle elencate"
    }
  ]
}
"""

try:
    # Impostiamo la temperatura alta (1.0) per garantire massima creatività e varietà giornaliera
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=1.0,
        )
    )
    
    raw_text = response.text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
    raw_text = raw_text.strip()

    data = json.loads(raw_text)
    
    with open("quiz.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print("Quiz generato e salvato con successo in quiz.json!")

except Exception as e:
    print(f"Errore durante la generazione del quiz: {e}")
    exit(1)
