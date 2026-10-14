import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Birthday Surprise",
    page_icon="🎂",
    layout="centered"
)

html_code = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
    margin: 0;
    padding: 15px;
    text-align: center;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #ffe1ec, #d9e8ff);
    color: #54234d;
}
h1 { color: #e63878; }
.cake {
    position: relative;
    margin: 100px auto 30px;
    width: 220px;
    height: 115px;
    background: #ff91b5;
    border-radius: 12px 12px 20px 20px;
    border-bottom: 12px solid #e65d8b;
    box-shadow: 0 10px 15px #0002;
}
.icing {
    position: absolute;
    top: 0;
    width: 100%;
    height: 25px;
    background: #fff0f5;
    border-radius: 12px 12px 5px 5px;
}
.candle {
    position: absolute;
    bottom: 110px;
    width: 13px;
    height: 55px;
    background: repeating-linear-gradient(
        45deg, white, white 5px, #ff6d94 5px, #ff6d94 10px
    );
    border-radius: 4px;
}
.candle:nth-child(2) { left: 40px; }
.candle:nth-child(3) { left: 103px; }
.candle:nth-child(4) { left: 167px; }
.flame {
    position: absolute;
    width: 17px;
    height: 25px;
    background: radial-gradient(ellipse at bottom, #fff36b 5%, #ff9d22 65%, #ff633d);
    border-radius: 50% 50% 45% 45%;
    top: -29px;
    left: -2px;
    animation: flicker 0.4s infinite alternate;
}
@keyframes flicker {
    from { transform: rotate(-5deg) scale(0.9); }
    to { transform: rotate(5deg) scale(1.1); }
}
button {
    border: none;
    padding: 13px 20px;
    margin: 8px;
    border-radius: 25px;
    background: #e63878;
    color: white;
    font-size: 16px;
    cursor: pointer;
}
#status { min-height: 30px; font-weight: bold; }
#surprise {
    display: none;
    padding: 15px;
    background: #ffffffbb;
    border-radius: 15px;
    margin-top: 15px;
}
</style>
</head>
<body>

<h1>🎉 Happy Birthday! 🎉</h1>
<p>A special surprise is waiting for you!</p>

<div class="cake">
    <div class="icing"></div>
    <div class="candle"><div class="flame"></div></div>
    <div class="candle"><div class="flame"></div></div>
    <div class="candle"><div class="flame"></div></div>
</div>

<h3>Make a wish and blow out the candles!</h3>

<button id="start">🎤 Start Microphone</button>
<button id="manual">🕯️ Blow Candles (Test)</button>

<p id="status">Microphone start karke cake par phoonk maaro!</p>

<div id="surprise">
    <h2>🎂 Hello 🎂</h2>
    <h2>💖 Happy Birthday, dear 💖</h2> 
    <p>May your life be filled with happiness, love and success.</p>
    <p>You deserve all the beautiful things in this world !</p>
    <h1>🎉🥳🎁</h1>
</div>

<script>
let audioContext;
let stream;
let listening = false;
let blown = false;
let loudSince = 0;

const statusText = document.getElementById("status");

async function startMic() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({
            audio: true
        });

        audioContext = new (
            window.AudioContext || window.webkitAudioContext
        )();

        const source = audioContext.createMediaStreamSource(stream);
        const analyser = audioContext.createAnalyser();
        analyser.fftSize = 2048;
        source.connect(analyser);

        const data = new Uint8Array(analyser.fftSize);
        listening = true;

        statusText.textContent =
            "Mic on hai! Ab candles ki taraf phoonk maaro.";

        function detectBlow() {
            if (!listening || blown) return;

            analyser.getByteTimeDomainData(data);

            let sum = 0;
            for (let i = 0; i < data.length; i++) {
                const sample = (data[i] - 128) / 128;
                sum += sample * sample;
            }

            const volume = Math.sqrt(sum / data.length);

            // Loud sound ko lagbhag 200 ms tak detect karo.
            if (volume > 0.10) {
                if (loudSince === 0) {
                    loudSince = Date.now();
                }

                if (Date.now() - loudSince > 200) {
                    extinguishCandles();
                    return;
                }
            } else {
                loudSince = 0;
            }

            requestAnimationFrame(detectBlow);
        }

        detectBlow();

    } catch (error) {
        statusText.textContent =
            "Mic access nahi mila. Browser settings mein microphone allow karo.";
    }
}

function extinguishCandles() {
    if (blown) return;
    blown = true;
    listening = false;

    document.querySelectorAll(".flame").forEach(flame => {
        flame.style.display = "none";
    });

    document.getElementById("surprise").style.display = "block";
    statusText.textContent = "Yay! Candles bujh gayi! 🎉";

    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
}

document.getElementById("start").addEventListener("click", startMic);

document.getElementById("manual").addEventListener(
    "click", extinguishCandles
);
</script>
</body>
</html>
"""

components.html(html_code, height=700, scrolling=True)
