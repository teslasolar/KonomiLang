// Command templates with proper template literals
const commands = {
    'ask': {
        template: 'ask ""',
        placeholderText: 'Your question here'
    },
    'let': {
        template: 'let name = ""',
        placeholderText: 'value'
    },
    'if': {
        template: 'if (condition) {\n    ask ""\n}',
        placeholderText: 'Your question here'
    },
    'try': {
        template: 'try {\n    ask ""\n} catch {\n    ask ""\n}',
        placeholderText: 'Your question here'
    },
    'ls': {
        template: 'ls ""',
        placeholderText: 'path (optional)'
    },
    'mkdir': {
        template: 'mkdir ""',
        placeholderText: 'directory_name'
    },
    'rmdir': {
        template: 'rmdir ""',
        placeholderText: 'directory_name'
    }
};

// Error type classification
const errorTypes = {
    SYNTAX_ERROR: 'Syntax Error',
    RUNTIME_ERROR: 'Runtime Error',
    NETWORK_ERROR: 'Network Error',
    UNKNOWN_ERROR: 'Unknown Error',
    FILE_SYSTEM_ERROR: 'File System Error'
};

function classifyError(error) {
    if (!error) return errorTypes.UNKNOWN_ERROR;
    const errorStr = String(error);
    if (errorStr.includes('SyntaxError')) return errorTypes.SYNTAX_ERROR;
    if (errorStr.includes('RuntimeError')) return errorTypes.RUNTIME_ERROR;
    if (errorStr.includes('Network')) return errorTypes.NETWORK_ERROR;
    if (errorStr.includes('File System Error')) return errorTypes.FILE_SYSTEM_ERROR;
    return errorTypes.UNKNOWN_ERROR;
}

function validatePath(path) {
    // Remove leading/trailing quotes if present
    path = path.replace(/^["']|["']$/g, '');
    
    // Check for directory traversal attempts
    if (path.includes('..')) {
        throw new Error('Directory traversal is not allowed');
    }
    
    // Check for absolute paths
    if (path.startsWith('/')) {
        throw new Error('Absolute paths are not allowed');
    }
    
    // Check for special characters
    const invalidChars = /[<>:"|?*\x00-\x1F]/;
    if (invalidChars.test(path)) {
        throw new Error('Path contains invalid characters');
    }
    
    return path;
}

function executeCode() {
    const input = document.getElementById('input');
    const output = document.getElementById('output');
    const code = input.value.trim();

    if (!code) return;

    // Validate file system commands
    try {
        if (code.startsWith('ls') || code.startsWith('mkdir') || code.startsWith('rmdir')) {
            const path = code.split(/\s+/)[1];
            if (path) {
                validatePath(path);
            }
        }
    } catch (error) {
        appendError(output, code, error.message, errorTypes.FILE_SYSTEM_ERROR);
        input.value = '';
        return;
    }

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
            const errorType = classifyError(data.error);
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
    const safeCode = escapeHtml(code);
    const safeResult = escapeHtml(result);
    const entry = document.createElement('div');
    entry.className = 'repl-entry';
    entry.innerHTML = `
        <div class="repl-input">&gt; ${safeCode}</div>
        <div class="repl-result">${safeResult}</div>
    `;
    output.appendChild(entry);
    output.scrollTop = output.scrollHeight;
}

function appendError(output, code, error, errorType) {
    const safeCode = escapeHtml(code);
    const safeError = escapeHtml(error);
    const safeErrorType = escapeHtml(errorType);
    const entry = document.createElement('div');
    entry.className = 'repl-entry';
    entry.innerHTML = `
        <div class="repl-input">&gt; ${safeCode}</div>
        <div class="repl-error">${safeErrorType}: ${safeError}</div>
    `;
    output.appendChild(entry);
    output.scrollTop = output.scrollHeight;
}

function escapeHtml(unsafe) {
    if (unsafe == null) return '';
    return String(unsafe)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function insertCommand(cmdName) {
    const input = document.getElementById('input');
    const command = commands[cmdName];
    
    if (!command) return;

    input.value = command.template;
    input.focus();

    // Find position between quotes for cursor placement
    const quoteMatch = command.template.match(/""/);
    if (quoteMatch) {
        const cursorPos = quoteMatch.index + 1;
        input.setSelectionRange(cursorPos, cursorPos);

        if (command.placeholderText) {
            const before = command.template.slice(0, cursorPos);
            const after = command.template.slice(cursorPos);
            const newValue = before + command.placeholderText + after;
            input.value = newValue;
            input.setSelectionRange(cursorPos, cursorPos + command.placeholderText.length);
        }
    }
}

// Command completion with debouncing
let inputTimeout = null;
const input = document.getElementById('input');

input.addEventListener('input', function(e) {
    clearTimeout(inputTimeout);
    inputTimeout = setTimeout(() => {
        const currentText = e.target.value;
        const lastWord = currentText.trim().split(/[\s\n]/).pop();
        
        if (lastWord && lastWord.length >= 2) {
            const matchingCommands = Object.entries(commands)
                .filter(([cmd]) => cmd.startsWith(lastWord));
            
            if (matchingCommands.length === 1 && lastWord === currentText) {
                const [cmdName, command] = matchingCommands[0];
                e.target.value = command.template;
                
                const quoteMatch = command.template.match(/""/);
                if (quoteMatch && command.placeholderText) {
                    const cursorPos = quoteMatch.index + 1;
                    const before = command.template.slice(0, cursorPos);
                    const after = command.template.slice(cursorPos);
                    e.target.value = before + command.placeholderText + after;
                    e.target.setSelectionRange(cursorPos, cursorPos + command.placeholderText.length);
                }
            }
        }
    }, 100);
});

input.addEventListener('keydown', function(e) {
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
