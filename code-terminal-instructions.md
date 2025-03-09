### 📜 **Terminal Skref**
_Þessi skrá inniheldur allar skipanir til að keyra verkefnin í terminal._  

---

# **🛠 1️⃣ Setja upp Leon AI Assistant**
```bash
git clone https://github.com/leon-ai/leon.git
cd leon
npm install
npm run dev
```

### **➡️ Breyta Leon til að nota Coqui TTS**
1. Opna skrána `leon/packages/tts/src/index.js`
2. Skipta út TTS kóðanum fyrir þetta:
```javascript
const axios = require("axios");

module.exports = async (text) => {
  try {
    const response = await axios.get(`http://localhost:8000/speak/?text=${encodeURIComponent(text)}`);
    return response.data.file; // Skilar íslenskri rödd
  } catch (error) {
    console.error("Villa í TTS kallinu:", error);
    return null;
  }
};
```
3. Vista og endurræsa Leon:
```bash
leon start
leon say "Halló! Ég tala íslensku!"
```

---

# **🛠 2️⃣ Þjálfa og setja upp íslenska TTS rödd**
```bash
git clone https://github.com/coqui-ai/TTS.git
cd TTS
pip install -r requirements.txt
```

➡️ **Sækja Talrómur gögn og undirbúa**
```bash
wget [LINK TIL TALRÓMUR]
unzip talromur.zip -d dataset
```

➡️ **Hreinsa hljóð með FFmpeg**
```bash
ffmpeg -i dataset/original.wav -ar 22050 -ac 1 dataset/clean.wav
```

➡️ **Undirbúa gögn fyrir training**
```bash
python TTS/bin/preprocess.py --config_path config.json
```

➡️ **Keyra TTS þjálfun**
```bash
python TTS/bin/train.py --config_path config.json
```

➡️ **Prófa íslenska rödd**
```bash
python TTS/bin/synthesize.py --text "Hæ, hvernig hefurðu það?" --config_path config.json
```

---

# **🛠 3️⃣ Búa til AI-generated intro**
➡️ **Sækja AI-generated rödd**
```bash
wget -O voice.mp3 [LINKUR FRÁ ElevenLabs/Uberduck]
```

➡️ **Búa til bakgrunnstónlist með AIVA.ai**
```bash
wget -O music.mp3 [LINKUR FRÁ AIVA]
```

➡️ **Blöndun (mixing) með ffmpeg**
```bash
ffmpeg -i voice.mp3 -i music.mp3 -filter_complex "[0:a]volume=1.5[a0];[1:a]volume=0.3[a1];[a0][a1]amix=inputs=2:duration=first:dropout_transition=3" final_intro.mp3
```

➡️ **Prófa lokaútkomu**
```bash
ffplay final_intro.mp3
```

---

# **🛠 4️⃣ Setja upp WebUI fyrir TTS prófanir**
```bash
git clone https://github.com/OpenWebUI/OpenWebUI.git
cd OpenWebUI
docker-compose up -d
```

➡️ **Breyta OpenWebUI til að tala íslensku**
1. Opna `webui/src/config.js`
2. Bæta við API endpoint fyrir íslensku röddina:
```javascript
const TTS_API = "http://localhost:8000/speak/?text=";
```

➡️ **Endurræsa WebUI**
```bash
docker-compose restart
```

➡️ **Prófa með því að slá inn texta og hlusta á úttak!**  

---

### **🔗 Tengingar við fyrri verkefni**

Til að nýta niðurstöður úr fyrri prófunum sem við gerðum í `helloiceland`:

1. **Nýta niðurstöður úr íslenskum TTS samanburði:**
```bash
cp /home/azureuser/helloiceland/ICELANDIC_VOICE_SERVICES_SUMMARY.md ./docs/
```

2. **Nýta test scripts sem við bjuggum til:**
```bash
cp /home/azureuser/helloiceland/test_*.py ./scripts/
```

3. **Tengja við n8n workflow sem við bjuggum til:**
```bash
cp /home/azureuser/helloiceland/n8n-icelandic-voice-workflow.json ./workflows/
```