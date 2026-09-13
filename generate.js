const fs = require('fs');

async function generaCuriosita() {
  const apiKey = process.env.GEMINI_API_KEY;
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`;

  const prompt = "Fornisci una curiosità scientifica, storica o geografica poco nota ma affascinante, seguita da una spiegazione dettagliata. Rispondi esclusivamente in formato JSON valido con questa struttura esatta: {\"titolo\": \"...\", \"spiegazione\": \"...\"}";

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: { responseMimeType: "application/json" }
      })
    });

    const data = await response.json();
    const testoGenerato = data.candidates[0].content.parts[0].text;
    const curiositaJson = JSON.parse(testoGenerato);

    // Salva il file curiosita.json
    fs.writeFileSync('curiosita.json', JSON.stringify(curiositaJson, null, 2));
    console.log('Curiosità generata con successo!');
  } catch (error) {
    console.error('Errore nella generazione:', error);
    process.exit(1);
  }
}

generaCuriosita();