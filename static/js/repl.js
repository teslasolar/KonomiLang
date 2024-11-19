const commands = {
    'ask': 'ask ""',
    'let': 'let variable = ""',
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
    
    for (const [cmd, template] of Object.entries(commands)) {
        if (cmd.startsWith(currentText) && currentText.length > 0) {
            input.value = template;
            input.setSelectionRange(
                template.indexOf('""') > -1 ? template.indexOf('""') + 1 : template.indexOf('()') + 1,
                template.indexOf('""') > -1 ? template.indexOf('""') + 1 : template.indexOf('()') + 1
            );
            break;
        }
    }
});

function insertCommand(template) {
    const input = document.getElementById('input');
    input.value = template;
    input.focus();
    
    // Position cursor based on template type
    if (template.includes('""')) {
        const cursorPos = template.indexOf('""') + 1;
        input.setSelectionRange(cursorPos, cursorPos);
    } else if (template.includes('()')) {
        const cursorPos = template.indexOf('()') + 1;
        input.setSelectionRange(cursorPos, cursorPos);
    } else if (template.includes('{\n')) {
        const cursorPos = template.indexOf('{\n') + 2;
        input.setSelectionRange(cursorPos, cursorPos);
    }
}
