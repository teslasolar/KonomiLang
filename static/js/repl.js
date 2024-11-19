const commands = {
    'ask': 'ask ""',
    'let': 'let name = ""',
    'if': 'if () {\n    ask ""\n}',
    'try': 'try {\n    ask ""\n} catch {\n    ask ""\n}'
};

function executeCode() {
    const input = document.getElementById('input');
    const output = document.getElementById('output');
    const code = input.value.trim();

    if (!code) return;

    // Create FormData for proper encoding
    const formData = new FormData();
    formData.append('code', code);

    fetch('/execute', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            output.innerHTML += `\n> ${escapeHtml(code)}\n${escapeHtml(data.result)}`;
        } else {
            output.innerHTML += `\n> ${escapeHtml(code)}\nError: ${escapeHtml(data.error)}`;
        }
        input.value = '';
        output.scrollTop = output.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
        output.innerHTML += `\n> ${escapeHtml(code)}\nError: Failed to execute code`;
        input.value = '';
    });
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

document.getElementById('input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        executeCode();
    }
});

document.getElementById('input').addEventListener('input', function(e) {
    const input = e.target;
    const currentText = input.value.trim();
    const lastWord = currentText.split(/[\s\n]/).pop();
    
    if (currentText === lastWord) {
        for (const [cmd, template] of Object.entries(commands)) {
            if (cmd.startsWith(lastWord) && lastWord.length >= 2) {
                input.value = currentText.slice(0, -lastWord.length) + template;
                
                if (template.includes('""')) {
                    const quotePos = input.value.indexOf('""') + 1;
                    input.setSelectionRange(quotePos, quotePos);
                } else if (template.includes('()')) {
                    const parenPos = input.value.indexOf('()') + 1;
                    input.setSelectionRange(parenPos, parenPos);
                }
                break;
            }
        }
    }
});

function insertCommand(template) {
    const input = document.getElementById('input');
    input.value = template;
    input.focus();
    
    if (template.includes('""')) {
        const quotePos = input.value.indexOf('""') + 1;
        input.setSelectionRange(quotePos, quotePos);
    } else if (template.includes('()')) {
        const parenPos = input.value.indexOf('()') + 1;
        input.setSelectionRange(parenPos, parenPos);
    }
}
