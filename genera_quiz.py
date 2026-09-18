import os
import json
import time
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

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

max_tentativi = 5
attesa_secondi = 10
successo = False

for tentativo in range(1, max_tentativi + 1):
    try:
        print(f"Tentativo {tentativo} di {max_tentativi} in corso...")
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
        successo = True
        break

    except Exception as e:
        print(f"Tentativo {tentativo} fallito: {e}")
        if tentativo < max_tentativi:
            print(f"Attendo {attesa_secondi} secondi prima di riprovare...")
            time.sleep(attesa_secondi)
            attesa_secondi *= 1.5  # Aumenta progressivamente l'attesa (backoff)
        else:
            print("Tutti i tentativi sono falliti.")
            exit(1)
