const commands = {
    'ask': 'ask ""',
    'let': 'let name = ""',
    'if': 'if () {\n    ask ""\n}',
    'try': 'try {\n    ask ""\n} catch {\n    ask ""\n}'
};

function executeCode() {
    const input = document.getElementById('input');
    const output = document.getElementById('output');
    const code = input.value;

    if (!code) return;

    // Properly encode the code for transmission
    const encodedCode = encodeURIComponent(code).replace(/%20/g, '+');

    fetch('/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `code=${encodedCode}`
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
        output.innerHTML += `\n> ${escapeHtml(code)}\nError: ${escapeHtml(error)}`;
        input.value = '';
    });
}

// Add HTML escaping function
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

document.getElementById('input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
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

// Update the insertCommand function
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
