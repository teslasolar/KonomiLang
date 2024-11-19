// Command templates with proper string escaping
const commands = {
    'ask': {
        template: 'ask ""',
        placeholderText: 'Your question here',
        cursorOffset: -1
    },
    'let': {
        template: 'let name = ""',
        placeholderText: 'value',
        cursorOffset: -1
    },
    'if': {
        template: 'if (condition) {\n    ask ""\n}',
        placeholderText: 'Your question here',
        cursorOffset: -2
    },
    'try': {
        template: 'try {\n    ask ""\n} catch {\n    ask ""\n}',
        placeholderText: 'Your question here',
        cursorOffset: -2
    }
};

// Error type classification
const errorTypes = {
    SYNTAX_ERROR: 'Syntax Error',
    RUNTIME_ERROR: 'Runtime Error',
    NETWORK_ERROR: 'Network Error',
    UNKNOWN_ERROR: 'Unknown Error'
};

function classifyError(error) {
    if (error.includes('SyntaxError')) return errorTypes.SYNTAX_ERROR;
    if (error.includes('RuntimeError')) return errorTypes.RUNTIME_ERROR;
    if (error.includes('Network')) return errorTypes.NETWORK_ERROR;
    return errorTypes.UNKNOWN_ERROR;
}

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
            throw new Error(`Network response was not ok: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            appendToOutput(output, code, data.result);
        } else {
            const errorType = classifyError(data.error || '');
            appendError(output, code, data.error || 'Unknown error', errorType);
        }
        input.value = '';
    })
    .catch(error => {
        console.error('Error:', error);
        const errorType = classifyError(error.message);
        appendError(output, code, 'Failed to execute code', errorType);
        input.value = '';
    });
}

function appendToOutput(output, code, result) {
    const formattedOutput = `<div class="repl-entry">
        <div class="repl-input">> ${escapeHtml(code)}</div>
        <div class="repl-result">${escapeHtml(result)}</div>
    </div>`;
    output.innerHTML += formattedOutput;
    output.scrollTop = output.scrollHeight;
}

function appendError(output, code, error, errorType) {
    const formattedError = `<div class="repl-entry">
        <div class="repl-input">> ${escapeHtml(code)}</div>
        <div class="repl-error">${errorType}: ${escapeHtml(error)}</div>
    </div>`;
    output.innerHTML += formattedError;
    output.scrollTop = output.scrollHeight;
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

function insertCommand(template) {
    const input = document.getElementById('input');
    const command = commands[template];
    
    if (command) {
        input.value = command.template;
        input.focus();
        
        // Calculate cursor position from the right side of the template
        const insertPoint = command.template.lastIndexOf('"');
        if (insertPoint !== -1) {
            input.setSelectionRange(insertPoint, insertPoint);
        }
        
        // Insert placeholder text if provided
        if (command.placeholderText) {
            const before = input.value.slice(0, insertPoint);
            const after = input.value.slice(insertPoint);
            input.value = before + command.placeholderText + after;
            input.setSelectionRange(insertPoint, insertPoint + command.placeholderText.length);
        }
    }
}

// Input handling with improved command completion
let inputTimeout = null;
document.getElementById('input').addEventListener('input', function(e) {
    const input = e.target;
    const currentText = input.value;
    
    clearTimeout(inputTimeout);
    inputTimeout = setTimeout(() => {
        const lastWord = currentText.trim().split(/[\s\n]/).pop();
        
        if (lastWord && lastWord.length >= 2) {
            const matchingCommands = Object.entries(commands)
                .filter(([cmd]) => cmd.startsWith(lastWord));
            
            if (matchingCommands.length === 1) {
                const [cmd, details] = matchingCommands[0];
                if (currentText === lastWord) {
                    input.value = details.template;
                    if (details.placeholderText) {
                        const insertPoint = details.template.lastIndexOf('"');
                        if (insertPoint !== -1) {
                            const before = input.value.slice(0, insertPoint);
                            const after = input.value.slice(insertPoint);
                            input.value = before + details.placeholderText + after;
                            input.setSelectionRange(insertPoint, insertPoint + details.placeholderText.length);
                        }
                    }
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

// Initialize output scroll position
document.addEventListener('DOMContentLoaded', function() {
    const output = document.getElementById('output');
    if (output) {
        output.scrollTop = output.scrollHeight;
    }
});
