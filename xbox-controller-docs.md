# Xbox Controller Viewer API Documentation

## Overview
The Xbox Controller Viewer is a web-based system for visualizing and simulating Xbox controller inputs. It provides both real gamepad input handling and simulation capabilities through a comprehensive JavaScript API.

## Table of Contents
- [Installation](#installation)
- [Components](#components)
- [Controller State Interface](#controller-state-interface)
- [Events](#events)
- [API Methods](#api-methods)
- [CSS Classes](#css-classes)
- [Examples](#examples)

## Installation

### Basic Setup
```html
<script src="js/gamepad.js"></script>
<link rel="stylesheet" href="css/styles.css">
```

### Required Directory Structure
```
project/
├── index.html          # Main entry point
├── controller.html     # Controller viewer component
├── js/
│   ├── gamepad.js     # Core gamepad handling
│   └── simulator.js   # Simulation capabilities
└── css/
    └── styles.css     # Controller styling
```

## Components

### XboxController
The main controller visualization component.

```javascript
const controller = new XboxController({
    element: '#controller',
    simulationMode: false,
    debug: false
});
```

#### Configuration Options
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| element | string\|HTMLElement | required | Container element for the controller |
| simulationMode | boolean | false | Enable simulation mode |
| debug | boolean | false | Enable debug logging |
| updateRate | number | 16 | Update rate in milliseconds |

## Controller State Interface

### ButtonState
```typescript
interface ButtonState {
    pressed: boolean;
    value: number;    // Range: 0.0 - 1.0
    touched?: boolean;
}
```

### ControllerState
```typescript
interface ControllerState {
    buttons: {
        a: ButtonState;
        b: ButtonState;
        x: ButtonState;
        y: ButtonState;
        lb: ButtonState;
        rb: ButtonState;
        lt: ButtonState;
        rt: ButtonState;
        back: ButtonState;
        start: ButtonState;
        leftStick: ButtonState;
        rightStick: ButtonState;
        dpadUp: ButtonState;
        dpadDown: ButtonState;
        dpadLeft: ButtonState;
        dpadRight: ButtonState;
    };
    axes: {
        leftStickX: number;  // Range: -1.0 - 1.0
        leftStickY: number;  // Range: -1.0 - 1.0
        rightStickX: number; // Range: -1.0 - 1.0
        rightStickY: number; // Range: -1.0 - 1.0
    };
    connected: boolean;
}
```

## Events

### Controller Events
```javascript
controller.on('connect', (gamepadIndex) => {});
controller.on('disconnect', (gamepadIndex) => {});
controller.on('buttonpress', (button, value) => {});
controller.on('buttonrelease', (button) => {});
controller.on('axischange', (axis, value) => {});
```

### Event Details
| Event | Parameters | Description |
|-------|------------|-------------|
| connect | gamepadIndex: number | Fired when controller connects |
| disconnect | gamepadIndex: number | Fired when controller disconnects |
| buttonpress | button: string, value: number | Fired when button is pressed |
| buttonrelease | button: string | Fired when button is released |
| axischange | axis: string, value: number | Fired when stick axis changes |

## API Methods

### Controller Management
```javascript
controller.connect();              // Initialize controller detection
controller.disconnect();           // Clean up controller connection
controller.reset();               // Reset all inputs to default state
controller.update();              // Force state update
controller.enableSimulation();    // Enable simulation mode
controller.disableSimulation();   // Disable simulation mode
```

### State Management
```javascript
controller.getState();            // Get current controller state
controller.setState(state);       // Set controller state (simulation mode only)
controller.updateButton(name, state); // Update specific button
controller.updateAxis(name, value);   // Update specific axis
```

### Simulation Methods
```javascript
controller.simulate.pressButton(name);    // Simulate button press
controller.simulate.releaseButton(name);  // Simulate button release
controller.simulate.setTrigger(name, value); // Set trigger value
controller.simulate.setStick(name, x, y);    // Set stick position
```

## CSS Classes

### Button States
```css
.button               /* Base button style */
.button.pressed       /* Pressed state */
.button.active        /* Active state */
.button.disabled      /* Disabled state */
```

### Trigger States
```css
.trigger             /* Base trigger style */
.trigger-fill        /* Trigger fill element */
```

### Stick States
```css
.stick               /* Base stick style */
.stick-dot          /* Stick position indicator */
```

## Examples

### Initialize Controller Viewer
```javascript
const controller = new XboxController({
    element: document.getElementById('controller')
});

controller.on('connect', (index) => {
    console.log(`Controller ${index} connected`);
});
```

### Simulate Button Press
```javascript
controller.enableSimulation();
controller.simulate.pressButton('a');
setTimeout(() => controller.simulate.releaseButton('a'), 1000);
```

### Handle Button Events
```javascript
controller.on('buttonpress', (button, value) => {
    console.log(`${button} pressed with value ${value}`);
});

controller.on('axischange', (axis, value) => {
    console.log(`${axis} changed to ${value}`);
});
```

### Custom State Updates
```javascript
controller.setState({
    buttons: {
        a: { pressed: true, value: 1.0 },
        b: { pressed: false, value: 0.0 }
    },
    axes: {
        leftStickX: 0.5,
        leftStickY: -0.5
    }
});
```

### Error Handling
```javascript
try {
    controller.connect();
} catch (error) {
    if (error.name === 'SecurityError') {
        console.error('Gamepad API access denied');
    } else if (error.name === 'NotSupportedError') {
        console.error('Gamepad API not supported');
    }
}
```

## Browser Support
- Chrome 35+
- Firefox 29+
- Edge 12+
- Safari 10.1+

## Security Considerations
- Requires HTTPS or localhost for Gamepad API access
- Permissions Policy header required for iframe support
- Cross-origin restrictions apply to gamepad access

## Best Practices
1. Always check for API support before initialization
2. Implement error handling for security and permission issues
3. Clean up event listeners when disconnecting
4. Use requestAnimationFrame for smooth updates
5. Implement debouncing for axis changes

## Troubleshooting

### Common Issues
1. **SecurityError**: Ensure running on HTTPS or localhost
2. **Permission Denied**: Check permissions policy headers
3. **No Controller Detected**: Verify controller is connected and supported
4. **Performance Issues**: Check update rate and event handling

### Debug Mode
Enable debug mode for detailed logging:
```javascript
const controller = new XboxController({
    debug: true
});
```
