// Secure Messenger Mini App
var tg = window.Telegram.WebApp;
if (tg) {
    tg.ready();
    tg.expand();
}

var currentMode = 'encrypt';

function setEncrypt() {
    currentMode = 'encrypt';
    document.getElementById('btnEncrypt').className = 'mode-btn active';
    document.getElementById('btnDecrypt').className = 'mode-btn';
    document.getElementById('actionBtn').textContent = 'Encrypt';
    document.getElementById('inputText').placeholder = 'Enter your message...';
    hideResult();
}

function setDecrypt() {
    currentMode = 'decrypt';
    document.getElementById('btnEncrypt').className = 'mode-btn';
    document.getElementById('btnDecrypt').className = 'mode-btn active';
    document.getElementById('actionBtn').textContent = 'Decrypt';
    document.getElementById('inputText').placeholder = 'Enter encrypted text...';
    hideResult();
}

function hideResult() {
    document.getElementById('resultBox').style.display = 'none';
    document.getElementById('copyBtn').style.display = 'none';
    document.getElementById('errorBox').style.display = 'none';
}

function showResult(text) {
    document.getElementById('resultBox').textContent = text;
    document.getElementById('resultBox').style.display = 'block';
    document.getElementById('copyBtn').style.display = 'block';
    document.getElementById('errorBox').style.display = 'none';
}

function showError(text) {
    document.getElementById('errorBox').textContent = text;
    document.getElementById('errorBox').style.display = 'block';
    document.getElementById('resultBox').style.display = 'none';
    document.getElementById('copyBtn').style.display = 'none';
}

function doProcess() {
    var input = document.getElementById('inputText').value.trim();
    if (!input) return;

    var btn = document.getElementById('actionBtn');
    btn.disabled = true;
    btn.textContent = currentMode === 'encrypt' ? 'Encrypting...' : 'Decrypting...';
    hideResult();

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/' + currentMode, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            btn.disabled = false;
            btn.textContent = currentMode === 'encrypt' ? 'Encrypt' : 'Decrypt';

            if (xhr.status === 200) {
                try {
                    var data = JSON.parse(xhr.responseText);
                    showResult(data.result);
                } catch (e) {
                    showError('Invalid response');
                }
            } else {
                try {
                    var err = JSON.parse(xhr.responseText);
                    showError(err.detail || 'Error occurred');
                } catch (e) {
                    showError('Request failed: ' + xhr.status);
                }
            }
        }
    };

    xhr.onerror = function() {
        btn.disabled = false;
        btn.textContent = currentMode === 'encrypt' ? 'Encrypt' : 'Decrypt';
        showError('Network error');
    };

    xhr.send(JSON.stringify({text: input}));
}

function copyResult() {
    var text = document.getElementById('resultBox').textContent;
    var textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    try {
        document.execCommand('copy');
        if (tg) {
            tg.showAlert('Copied to clipboard!');
        }
    } catch (e) {
        console.log('Copy failed');
    }
    document.body.removeChild(textarea);
}
