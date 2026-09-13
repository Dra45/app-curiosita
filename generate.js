const fs = require('fs');

async function generaCuriosita() {
  const apiKey = process.env.GEMINI_API_KEY;

  if (!apiKey) {
    console.error("Errore: GEMINI_API_KEY non trovata nei Secret di GitHub!");
    process.exit(1);
  }

  // Endpoint aggiornato per Gemini
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

    if (data.error) {
      console.error('Errore restituito da Google Gemini:', JSON.stringify(data.error, null, 2));
      process.exit(1);
    }

    if (!data.candidates || !data.candidates[0] || !data.candidates[0].content) {
      console.error('Struttura risposta inattesa:', JSON.stringify(data, null, 2));
      process.exit(1);
    }

    const testoGenerato = data.candidates[0].content.parts[0].text;
    const curiositaJson = JSON.parse(testoGenerato);

    fs.writeFileSync('curiosita.json', JSON.stringify(curiositaJson, null, 2));
    console.log('Curiosità generata e salvata con successo!');
  } catch (error) {
    console.error('Errore durante la generazione:', error.message);
    process.exit(1);
  }
}

generaCuriosita();
