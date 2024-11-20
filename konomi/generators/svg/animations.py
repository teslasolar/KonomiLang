"""
SVG Animation functionality
"""
from typing import Dict, Optional, Union
from .validation import SVGValidator

class AnimationManager:
    """Manages SVG animations and interactive behaviors."""
    
    def __init__(self):
        self.validator = SVGValidator()
        self.has_interactive = False
        
    def create_transform_animation(
        self, target_id: str, trigger: str,
        transform_type: str, from_val: str, to_val: str,
        duration: float, timing: str = 'ease',
        repeat_count: Optional[Union[int, str]] = "1"
    ) -> str:
        """Create a transform animation element."""
        self.validator.validate_transform_animation(
            target_id, trigger, transform_type, timing
        )
        
        self.has_interactive = True
        animation_id = f"{target_id}-{trigger}-animation"
        
        return (
            f'<animateTransform id="{animation_id}" '
            f'xlink:href="#{target_id}" '
            f'attributeName="transform" '
            f'type="{transform_type}" '
            f'from="{from_val}" '
            f'to="{to_val}" '
            f'dur="{duration}s" '
            f'begin="{target_id}.{trigger}" '
            f'calcMode="spline" '
            f'keySplines="{self.validator.get_timing_spline(timing)}" '
            f'additive="replace" '
            f'fill="freeze" '
            f'restart="whenNotActive" '
            f'repeatCount="{repeat_count}"/>'
        )
        
    def create_morph_animation(
        self, target_id: str, path1: str, path2: str,
        duration: float, trigger: Optional[str] = None,
        timing: str = 'ease'
    ) -> str:
        """Create a path morphing animation element."""
        if trigger:
            self.validator.validate_trigger(trigger)
        self.validator.validate_timing(timing)
        
        begin = f"#{target_id}.{trigger}" if trigger else "0s"
        
        return (
            f'<animate '
            f'xlink:href="#{target_id}" '
            f'attributeName="d" '
            f'from="{path1}" to="{path2}" '
            f'dur="{duration}s" '
            f'begin="{begin}" '
            f'calcMode="spline" '
            f'keySplines="{self.validator.get_timing_spline(timing)}" '
            f'fill="freeze"/>'
        )
    
    def get_initialization_script(self) -> str:
        """Get the animation initialization script."""
        if not self.has_interactive:
            return ""
            
        return """
    <script type="text/javascript"><![CDATA[
        function initInteractiveAnimations() {
            const svg = document.querySelector('svg');
            if (!svg) return;
            
            function getAnimationsForElement(elementId) {
                const nsResolver = prefix => {
                    const ns = {
                        'xlink': 'http://www.w3.org/1999/xlink',
                        'svg': 'http://www.w3.org/2000/svg'
                    };
                    return ns[prefix] || null;
                };
                
                return [
                    ...svg.querySelectorAll(`animate[*|href="#${elementId}"]`),
                    ...svg.querySelectorAll(`animateTransform[*|href="#${elementId}"]`)
                ].filter(el => el.getAttributeNS('http://www.w3.org/1999/xlink', 'href') === `#${elementId}`);
            }
            
            function setupEventHandler(element, trigger, animation) {
                element.style.cursor = 'pointer';
                const eventName = trigger === 'mouseover' ? 'mouseenter' : 
                                 trigger === 'mouseout' ? 'mouseleave' : trigger;
                
                element.addEventListener(eventName, () => {
                    // Cancel any running animation
                    try {
                        animation.endElement();
                    } catch (e) {
                        // Ignore errors from endElement
                    }
                    
                    // Force a reflow to ensure the animation restarts properly
                    element.style.animationName = 'none';
                    void element.offsetWidth;
                    element.style.animationName = '';
                    
                    // Start the new animation
                    requestAnimationFrame(() => {
                        animation.beginElement();
                    });
                });
            }
            
            function initElement(element) {
                if (!element.id) return;
                
                const animations = getAnimationsForElement(element.id);
                animations.forEach(animation => {
                    const begin = animation.getAttribute('begin');
                    if (!begin || !begin.includes(element.id)) return;
                    
                    const [_, trigger] = begin.split('.');
                    if (!trigger) return;
                    
                    setupEventHandler(element, trigger, animation);
                });
            }
            
            // Initialize all elements with IDs
            Array.from(svg.getElementsByTagName('*')).forEach(initElement);
        }
        
        // Initialize animations when the document is loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initInteractiveAnimations);
        } else {
            setTimeout(initInteractiveAnimations, 0);
        }
    ]]></script>"""
