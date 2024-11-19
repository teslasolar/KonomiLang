// Command templates with proper escaping
const commands = {
    'ask': {
        template: 'ask "Your question here"',
        cursorOffset: -1
    },
    'let': {
        template: 'let name = "value"',
        cursorOffset: -7
    },
    'if': {
        template: 'if (condition) {\n    ask "Your question here"\n}',
        cursorOffset: -24
    },
    'try': {
        template: 'try {\n    ask "Your question here"\n} catch {\n    ask "Error handler"\n}',
        cursorOffset: -24
    }
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
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            output.innerHTML += `\n> ${escapeHtml(code)}\n${escapeHtml(data.result)}`;
        } else {
            output.innerHTML += `\n> ${escapeHtml(code)}\nError: ${escapeHtml(data.error || 'Unknown error')}`;
        }
        input.value = '';
        output.scrollTop = output.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
        output.innerHTML += `\n> ${escapeHtml(code)}\nError: Failed to execute code`;
        input.value = '';
        output.scrollTop = output.scrollHeight;
    });
}

function escapeHtml(unsafe) {
    if (unsafe == null) return '';
    return unsafe
        .toString()
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Improved input handling with debounce
let inputTimeout = null;
document.getElementById('input').addEventListener('input', function(e) {
    const input = e.target;
    const currentText = input.value;
    
    clearTimeout(inputTimeout);
    inputTimeout = setTimeout(() => {
        const lastWord = currentText.trim().split(/[\s\n]/).pop();
        
        if (currentText === lastWord && lastWord.length >= 2) {
            for (const [cmd, details] of Object.entries(commands)) {
                if (cmd.startsWith(lastWord)) {
                    const cursorPos = details.cursorOffset ? 
                        details.template.length + details.cursorOffset : 
                        details.template.length;
                    
                    input.value = details.template;
                    input.setSelectionRange(cursorPos, cursorPos);
                    input.focus();
                    break;
                }
            }
        }
    }, 100);
});

document.getElementById('input').addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        executeCode();
    }
});

function insertCommand(template) {
    const input = document.getElementById('input');
    const command = commands[template];
    
    if (command) {
        input.value = command.template;
        input.focus();
        
        const cursorPos = command.cursorOffset ? 
            command.template.length + command.cursorOffset : 
            command.template.length;
        
        input.setSelectionRange(cursorPos, cursorPos);
    }
}

// Initialize output scroll position
document.addEventListener('DOMContentLoaded', function() {
    const output = document.getElementById('output');
    if (output) {
        output.scrollTop = output.scrollHeight;
    }
});
