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

function insertCommand(template) {
    const input = document.getElementById('input');
    input.value = template;
    input.focus();
    
    // If the template contains quotes, place cursor between them
    if (template.includes('""')) {
        const cursorPos = input.value.indexOf('""') + 1;
        input.setSelectionRange(cursorPos, cursorPos);
    }
}
