"""
Example implementations of HTML components
"""
from ..html.components import (
    Button, ButtonProps, Input, InputProps, 
    Card, CardProps, Alert, AlertProps,
    NavBar, NavBarProps, NavItem, NavItemProps
)
from ..html.layouts import Container, ContainerProps, Grid, GridProps, Flex, FlexProps
from ..html.forms import Form, FormProps, FormGroup, FormGroupProps, Select, SelectProps

def generate_components_example():
    """Generate examples of all available components."""
    
    # Button examples
    buttons = []
    for variant in ["primary", "secondary", "outline"]:
        button_props = ButtonProps(variant=variant, class_name="mr-4")
        buttons.append(Button(f"{variant.title()} Button", button_props).render())
    
    # Input examples
    inputs = []
    input_types = [
        ("text", "Text input"),
        ("email", "Email input"),
        ("password", "Password")
    ]
    for input_type, placeholder in input_types:
        input_props = InputProps(
            type=input_type,
            placeholder=placeholder,
            class_name="mb-4"
        )
        inputs.append(Input(input_props).render())
    
    # Alert examples
    alerts = []
    for alert_type in ["info", "success", "warning", "error"]:
        alert_props = AlertProps(
            type=alert_type,
            dismissible=True,
            class_name="mb-4"
        )
        alerts.append(
            Alert(f"This is an {alert_type} alert message", alert_props).render()
        )
    
    # Form example
    form_group_props = FormGroupProps(
        label="Username",
        help_text="Enter your username",
        required=True
    )
    
    select_props = SelectProps(
        options=[
            {"value": "1", "label": "Option 1"},
            {"value": "2", "label": "Option 2"},
            {"value": "3", "label": "Option 3"}
        ],
        placeholder="Select an option"
    )
    
    form_content = [
        FormGroup(Input(InputProps(type="text", required=True)).render(), form_group_props).render(),
        Select(select_props).render(),
        Button("Submit", ButtonProps(variant="primary", class_name="mt-4")).render()
    ]
    
    form = Form(form_content, FormProps(method="post", action="/submit")).render()
    
    # Card with form
    card = Card(
        form,
        CardProps(
            padding="large",
            shadow="medium",
            hover_effect=True,
            class_name="mb-8"
        )
    ).render()
    
    # Create sections using Grid and Flex
    grid = Grid(
        [
            Card(
                "\n".join(buttons),
                CardProps(padding="normal", class_name="mb-4")
            ).render(),
            Card(
                "\n".join(inputs),
                CardProps(padding="normal", class_name="mb-4")
            ).render(),
            Card(
                "\n".join(alerts),
                CardProps(padding="normal", class_name="mb-4")
            ).render()
        ],
        GridProps(columns=3, gap=4)
    ).render()
    
    flex = Flex(
        [grid, card],
        FlexProps(direction="column", align="center")
    ).render()
    
    # Create navigation example
    nav_items = [
        NavItem("Home", NavItemProps(href="/", active=True, icon="home")),
        NavItem("About", NavItemProps(href="/about", icon="info-circle")),
        NavItem("Contact", NavItemProps(href="/contact", icon="envelope"))
    ]
    navbar = NavBar(nav_items, NavBarProps(brand="Component Library", dark=True, fixed=True))

    # Wrap everything in a container
    main_content = Container(
        flex,
        ContainerProps(max_width="xl", padding=True, center=True)
    ).render()

    return f"{navbar.render()}\n<div class='pt-16'>{main_content}</div>"
