const commands = {
    'ask': 'ask ""',
    'let': 'let name = ""',
    'if': `if () {
    ask ""
}`,
    'try': `try {
    ask ""
} catch {
    ask ""
}`
};

function executeCode() {
    const input = document.getElementById('input');
    const output = document.getElementById('output');
    const code = input.value;

    if (!code) return;

    fetch('/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `code=${encodeURIComponent(code)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            output.innerHTML += `\n> ${code}\n${data.result}`;
        } else {
            output.innerHTML += `\n> ${code}\nError: ${data.error}`;
        }
        input.value = '';
        output.scrollTop = output.scrollHeight;
    })
    .catch(error => {
        output.innerHTML += `\n> ${code}\nError: ${error}`;
        input.value = '';
    });
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
