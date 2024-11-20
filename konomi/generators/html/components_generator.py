"""
HTML Components Generator using ChatGPT chains
"""
import os
from konomi.chained_programs import ProgramLibrary
from konomi.interpreter import Interpreter

class HTMLComponentsGenerator:
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.interpreter = Interpreter()
        self.program_library = ProgramLibrary(self.interpreter)

    def generate_hero_section(self, title, subtitle, cta_text):
        specs = f"""
        Create a modern hero section with:
        - Title: {title}
        - Subtitle: {subtitle}
        - CTA Button: {cta_text}
        Style requirements:
        - Full viewport height (min-h-screen)
        - Centered content using flex and items-center
        - Dark mode compatible using slate colors
        - Responsive text sizing (text-4xl md:text-6xl for title)
        - Gradient background (bg-gradient-to-br from-slate-900 to-indigo-900)
        - Smooth transitions on hover effects
        - Maximum width container with proper padding
        - Responsive spacing and padding (px-4 md:px-8 lg:px-16)
        Output only the HTML with Tailwind CSS classes.
        Include proper aria-labels and semantic HTML.
        """
        result = self.program_library.component_builder(specs)
        if result.get('success'):
            return result['results'][-1]  # Get the final generated component
        return None

    def generate_feature_cards(self, features):
        specs = f"""
        Create a responsive feature cards section with:
        - Features: {features}
        Style requirements:
        - Responsive grid layout (grid-cols-1 md:grid-cols-2 lg:grid-cols-3)
        - Consistent gap spacing (gap-6 md:gap-8)
        - Card styling with proper padding (p-6 md:p-8)
        - Smooth hover transitions (transform hover:scale-105 transition-all)
        - Elevated cards with shadows (shadow-md hover:shadow-xl)
        - Icon placeholders with proper sizing and colors
        - Subtle background colors (bg-slate-50 dark:bg-slate-800)
        - Proper typography hierarchy for titles and descriptions
        - Consistent spacing between elements (space-y-4)
        - Border radius for cards (rounded-xl)
        Output only the HTML with Tailwind CSS classes.
        Include proper aria-labels and semantic HTML.
        """
        result = self.program_library.component_builder(specs)
        if result.get('success'):
            return result['results'][-1]
        return None

    def generate_testimonial_section(self, testimonials):
        specs = f"""
        Create a testimonial section with:
        - Testimonials: {testimonials}
        Style requirements:
        - Responsive grid layout (grid-cols-1 md:grid-cols-2)
        - Elegant quote styling with proper spacing
        - Avatar placeholders with consistent sizing (w-16 h-16 rounded-full)
        - Subtle background (bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-900)
        - Card styling with proper padding and margins
        - Smooth hover effects on cards (hover:shadow-lg transition-shadow)
        - Typography with proper hierarchy and line height
        - Consistent spacing between elements (space-y-6 md:space-y-8)
        - Quote marks styling using pseudo-elements
        - Proper alignment of avatar and text
        Output only the HTML with Tailwind CSS classes.
        Include proper aria-labels and semantic HTML.
        """
        result = self.program_library.component_builder(specs)
        if result.get('success'):
            return result['results'][-1]
        return None

    def generate_contact_form(self):
        specs = """
        Create a contact form with:
        Style requirements:
        - Container with max-width and centered (max-w-lg mx-auto)
        - Consistent form field spacing (space-y-6)
        - Input styling with proper padding and borders
        - Focus states with ring effects (focus:ring-2 focus:ring-indigo-500)
        - Smooth transitions on focus and hover
        - Error state styling for validation
        - Submit button with gradient and hover effects
        - Proper label alignment and spacing
        - Responsive padding and margins
        - Accessible form elements with proper labels
        Form fields:
        - Name field with proper validation
        - Email field with email validation
        - Message textarea with adjustable height
        - Submit button with loading state
        Output only the HTML with Tailwind CSS classes.
        Include proper aria-labels and semantic HTML.
        """
        result = self.program_library.component_builder(specs)
        if result.get('success'):
            return result['results'][-1]
        return None

    def generate_footer(self, links, social_media):
        specs = f"""
        Create a footer section with:
        - Navigation links: {links}
        - Social media links: {social_media}
        Style requirements:
        - Dark background with proper contrast (bg-slate-900)
        - Responsive grid layout for link sections
        - Consistent spacing and padding (py-12 px-4 md:px-8)
        - Hover effects on links (hover:text-indigo-400 transition-colors)
        - Social media icons with proper sizing and colors
        - Proper typography hierarchy for different sections
        - Responsive layout for mobile and desktop
        - Border top for separation (border-t border-slate-800)
        - Maximum width container with proper centering
        - Proper spacing between sections (space-y-8)
        Additional elements:
        - Copyright notice with current year
        - Responsive navigation columns
        - Social media icons with hover effects
        Output only the HTML with Tailwind CSS classes.
        Include proper aria-labels and semantic HTML.
        """
        result = self.program_library.component_builder(specs)
        if result.get('success'):
            return result['results'][-1]
        return None

    def generate_complete_page(self):
        hero = self.generate_hero_section(
            "Welcome to Konomi",
            "A powerful AI programming language",
            "Get Started"
        )
        
        features = [
            {"title": "Easy to Learn", "description": "Simple and intuitive syntax"},
            {"title": "AI-Powered", "description": "Built-in AI capabilities"},
            {"title": "Extensible", "description": "Rich plugin ecosystem"}
        ]
        feature_section = self.generate_feature_cards(features)
        
        testimonials = [
            {"name": "John Doe", "text": "Konomi has revolutionized our development process."},
            {"name": "Jane Smith", "text": "The AI integration is seamless and powerful."}
        ]
        testimonial_section = self.generate_testimonial_section(testimonials)
        
        contact_form = self.generate_contact_form()
        
        footer = self.generate_footer(
            ["Home", "Documentation", "Examples", "Contact"],
            ["GitHub", "Twitter", "Discord"]
        )
        
        return {
            "hero": hero,
            "features": feature_section,
            "testimonials": testimonial_section,
            "contact": contact_form,
            "footer": footer
        }
