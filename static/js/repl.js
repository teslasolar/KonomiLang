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

    // Properly escape special characters for the server
    const escapedCode = code.replace(/\\/g, '\\\\')
                           .replace(/\n/g, '\\n')
                           .replace(/"/g, '\\"');

    fetch('/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `code=${encodeURIComponent(escapedCode)}`
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
    const lastWord = currentText.split(/[\s\n]/).pop(); // Only look at last word
    
    // Only trigger for commands at start of line or after newline
    if (currentText === lastWord) {
        for (const [cmd, template] of Object.entries(commands)) {
            if (cmd.startsWith(lastWord) && lastWord.length >= 2) { // Require at least 2 chars
                const cursorPos = input.selectionStart;
                // Replace escaped newlines with actual newlines
                const processedTemplate = template.replace(/\\n/g, '\n');
                input.value = currentText.slice(0, -lastWord.length) + processedTemplate;
                
                // Smart cursor positioning
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
    // Replace escaped newlines with actual newlines
    const processedTemplate = template.replace(/\\n/g, '\n');
    input.value = processedTemplate;
    input.focus();
    
    // Position cursor based on template type
    if (template.includes('""')) {
        const quotePos = input.value.indexOf('""') + 1;
        input.setSelectionRange(quotePos, quotePos);
    } else if (template.includes('()')) {
        const parenPos = input.value.indexOf('()') + 1;
        input.setSelectionRange(parenPos, parenPos);
    }
}
