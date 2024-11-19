# Konomi Basic Syntax Guide

## Variable Declaration
```konomi
let name = "Alice"
let age = 25
let price = 99.99
```

## Data Types
- Strings: Text enclosed in double quotes
- Numbers: Integer or decimal numbers
- Variables: References to stored values

## AI Interaction
```konomi
ask "What is the weather like today?"
let question = "Explain quantum physics"
ask question
```

## Control Flow
### If Statements
```konomi
if (age >= 18) {
    ask "What career advice would you give?"
} else {
    ask "What subjects should I study?"
}
```

### Try-Catch Blocks
```konomi
try {
    ask "Explain quantum entanglement"
} catch {
    ask "Can you explain that in simpler terms?"
}
```

## Operators
### Arithmetic Operators
```konomi
let sum = 10 + 5
let difference = 20 - 8
let product = 6 * 7
let quotient = 100 / 4
```

### Comparison Operators
```konomi
if (value == 10) {
    ask "Equal to 10"
}
if (value > 5) {
    ask "Greater than 5"
}
if (value < 20) {
    ask "Less than 20"
}
```

## String Operations
```konomi
let first_name = "John"
let last_name = "Doe"
let full_name = first_name + " " + last_name
```

## Best Practices
1. Use descriptive variable names
2. Break complex operations into simpler steps
3. Handle potential errors with try-catch blocks
4. Keep AI prompts clear and specific
