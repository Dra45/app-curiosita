const fs = require('fs');

async function inviaNotificaPush(titolo) {
  const appId = process.env.ONESIGNAL_APP_ID;
  const apiKey = process.env.ONESIGNAL_REST_KEY;

  if (!appId || !apiKey) {
    console.log("Secret OneSignal non trovati: notifica push saltata.");
    return;
  }

  try {
    const res = await fetch('https://onesignal.com/api/v1/notifications', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Basic ${apiKey}`
      },
      body: JSON.stringify({
        app_id: appId,
        included_segments: ["Subscribed Users"],
        headings: { it: "💡 Nuova Curiosità del Giorno!" },
        contents: { it: titolo }
      })
    });
    const data = await res.json();
    console.log("Stato invio notifica OneSignal:", JSON.stringify(data));
  } catch (err) {
    console.error("Errore nell'invio della notifica push:", err.message);
  }
}

async function generaCuriosita() {
  const apiKey = process.env.GEMINI_API_KEY;

  if (!apiKey) {
    console.error("GEMINI_API_KEY non trovata nei Secret di GitHub!");
    process.exit(1);
  }

  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key=${apiKey}`;
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
      console.error('Errore da Gemini:', JSON.stringify(data.error, null, 2));
      process.exit(1);
    }

    const testoGenerato = data.candidates[0].content.parts[0].text;
    const curiositaJson = JSON.parse(testoGenerato);

    fs.writeFileSync('curiosita.json', JSON.stringify(curiositaJson, null, 2));
    console.log('Curiosità generata e salvata con successo!');

    // Invio della notifica push agli utenti iscritti
    await inviaNotificaPush(curiositaJson.titolo);

  } catch (error) {
    console.error('Errore durante il processo:', error.message);
    process.exit(1);
  }
}

generaCuriosita();
