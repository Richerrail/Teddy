// Telegram Mini App
const tg = window.Telegram.WebApp;
tg.expand();
tg.ready();

let mode = 'encrypt';

function switchMode(newMode) {
    mode = newMode;
    document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
    if (event) event.target.classList.add('active');
    document.getElementById('actionBtn').textContent = mode === 'encrypt' ? 'Encrypt' : 'Decrypt';
    document.getElementById('input').placeholder = mode === 'encrypt' ? 'Enter your message...' : 'Enter encrypted text...';
    document.getElementById('result').classList.remove('show');
    document.getElementById('copyBtn').style.display = 'none';
    document.getElementById('error').classList.remove('show');
}

async function processText() {
    const input = document.getElementById('input').value.trim();
    if (!input) return;

    const btn = document.getElementById('actionBtn');
    btn.disabled = true;
    btn.textContent = mode === 'encrypt' ? 'Encrypting...' : 'Decrypting...';
    document.getElementById('result').classList.remove('show');
    document.getElementById('copyBtn').style.display = 'none';
    document.getElementById('error').classList.remove('show');

    try {
        const response = await fetch(`/api/${mode}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: input })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Request failed');
        }

        document.getElementById('result').textContent = data.result;
        document.getElementById('result').classList.add('show');
        document.getElementById('copyBtn').style.display = 'block';
    } catch (err) {
        document.getElementById('error').textContent = err.message;
        document.getElementById('error').classList.add('show');
    } finally {
        btn.disabled = false;
        btn.textContent = mode === 'encrypt' ? 'Encrypt' : 'Decrypt';
    }
}

function copyResult() {
    const text = document.getElementById('result').textContent;
    navigator.clipboard.writeText(text).then(() => {
        tg.showAlert('Copied to clipboard!');
    });
}
