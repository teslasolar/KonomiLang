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
        - Full viewport height
        - Centered content
        - Responsive design
        Output only the HTML with Tailwind CSS classes.
        """
        result = self.program_library.component_builder(specs)
        if result.get('success'):
            return result['results'][-1]  # Get the final generated component
        return None

    def generate_feature_cards(self, features):
        specs = f"""
        Create a responsive feature cards section with:
        - Grid layout
        - Features: {features}
        - Icon placeholder for each feature
        - Card hover effects
        Output only the HTML with Tailwind CSS classes.
        """
        result = self.program_library.component_builder(specs)
        if result.get('success'):
            return result['results'][-1]
        return None

    def generate_testimonial_section(self, testimonials):
        specs = f"""
        Create a testimonial section with:
        - Testimonials: {testimonials}
        - Avatar placeholders
        - Quote styling
        - Grid or flex layout
        Output only the HTML with Tailwind CSS classes.
        """
        result = self.program_library.component_builder(specs)
        if result.get('success'):
            return result['results'][-1]
        return None

    def generate_contact_form(self):
        specs = """
        Create a contact form with:
        - Name field
        - Email field
        - Message textarea
        - Submit button
        - Form validation
        - Modern styling
        Output only the HTML with Tailwind CSS classes.
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
        - Copyright notice
        - Responsive layout
        Output only the HTML with Tailwind CSS classes.
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
