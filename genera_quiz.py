import os
import json
import random
import time
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Prompt ultra-rigido per evitare domande difficili, ripetitive e risposte sempre al primo posto
prompt = """
Sei un autore di quiz divertenti, dinamici e accessibili. Genera esattamente 6 domande di cultura generale affascinante, curiosa e moderna (spaziando tra cinema, tecnologia, storia curiosa, geografia, pop culture e natura).
REGOLE FONDAMENTALI:
1. Le domande DEVONO essere di media difficoltà: interessanti e stimolanti, ma che una persona comune possa indovinare senza essere un professore universitario. Evita date oscure o nozioni troppo tecniche.
2. Varia radicalmente gli argomenti rispetto ai quiz tradizionali.
3. Per ogni domanda, fornisci 4 opzioni di risposta. La risposta corretta NON DEVE ESSERE SEMPRE LA PRIMA: posizionala in modo casuale tra la prima, la seconda, la terza o la quarta opzione.
4. RISPONDI ESCLUSIVAMENTE IN FORMATO JSON VALIDO, senza blocchi di codice markdown (niente ```json ... ```), rispettando esattamente questa struttura:
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
                temperature=1.2, # Temperatura altissima per costringere la creatività a cambiare ogni giorno
            )
        )
        
        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
        raw_text = raw_text.strip()

        data = json.loads(raw_text)
        
        # MISCHIARE LE OPZIONI (Controllo di sicurezza extra in Python)
        # Assicura che l'ordine delle opzioni e la posizione della risposta corretta siano casuali al 100%
        for q in data.get("domande", []):
            corretta = q["risposta_corretta"]
            opzioni = q["opzioni"]
            random.shuffle(opzioni)
            q["opzioni"] = opzioni
            q["risposta_corretta"] = corretta # Mantiene la stringa corretta intatta
        
        with open("quiz.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print("Quiz generato, rimescolato e salvato con successo in quiz.json!")
        successo = True
        break

    except Exception as e:
        print(f"Tentativo {tentativo} fallito: {e}")
        if tentativo < max_tentativi:
            print(f"Attendo {attesa_secondi} secondi prima di riprovare...")
            time.sleep(attesa_secondi)
            attesa_secondi *= 1.5
        else:
            print("Tutti i tentativi sono falliti.")
            exit(1)
