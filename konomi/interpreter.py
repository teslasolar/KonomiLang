"""
Konomi Language Interpreter

This module implements the core interpreter for the Konomi programming language.
"""
import os
from typing import Any, Dict, List, Optional
from .lexer import Lexer, TokenType
from .parser import (
    Parser, VariableDeclaration, AskCommand, BinaryOp,
    Number, String, Identifier, IfStatement, TryCatch,
    ListDirectoryCommand, CreateDirectoryCommand, RemoveDirectoryCommand
)
from .errors import RuntimeError
from .utils.error_handling import validate_type, validate_operation, safe_execute
from .utils.api_client import APIClient
from .utils.file_operations import safe_list_directory, safe_create_directory, safe_remove_directory

class Interpreter:
    """
    The Konomi language interpreter that executes parsed AST nodes.
    """
    
    def __init__(self):
        """Initialize the interpreter with empty variable storage and API client."""
        self.variables: Dict[str, Any] = {}
        self.api_client = APIClient()

    def visit_variabledeclaration(self, node: VariableDeclaration) -> str:
        """
        Process a variable declaration node.
        
        Args:
            node: Variable declaration AST node
            
        Returns:
            Success message
        """
        value = self.visit(node.value)
        self.variables[node.name] = value
        return f"Variable {node.name} set to: {value}"

    def visit_askcommand(self, node: AskCommand) -> str:
        """
        Process an ask command node.
        
        Args:
            node: Ask command AST node
            
        Returns:
            AI response text
        """
        prompt = self.visit(node.prompt) if not isinstance(node.prompt, str) else node.prompt
        return self.api_client.ask_ai(prompt)

    def visit_listdirectorycommand(self, node: ListDirectoryCommand) -> str:
        """
        Process a list directory command node.
        
        Args:
            node: List directory command AST node
            
        Returns:
            Directory listing
        """
        path = None if node.path is None else self.visit(node.path)
        return safe_list_directory(path)

    def visit_createdirectorycommand(self, node: CreateDirectoryCommand) -> str:
        """
        Process a create directory command node.
        
        Args:
            node: Create directory command AST node
            
        Returns:
            Success message
        """
        path = self.visit(node.path)
        return safe_create_directory(path)

    def visit_removedirectorycommand(self, node: RemoveDirectoryCommand) -> str:
        """
        Process a remove directory command node.
        
        Args:
            node: Remove directory command AST node
            
        Returns:
            Success message
        """
        path = self.visit(node.path)
        return safe_remove_directory(path)

    def visit_binaryop(self, node: BinaryOp) -> Any:
        """
        Process a binary operation node.
        
        Args:
            node: Binary operation AST node
            
        Returns:
            Operation result
        """
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        validate_operation(left, right, node.op)
        
        if node.op == TokenType.PLUS:
            return str(left) + str(right) if isinstance(left, str) or isinstance(right, str) else left + right
        elif node.op == TokenType.MINUS:
            return left - right
        elif node.op == TokenType.MULTIPLY:
            return left * right
        elif node.op == TokenType.DIVIDE:
            if right == 0:
                raise RuntimeError("Division by zero")
            return left / right
        elif node.op == TokenType.EQUALS_EQUALS:
            return left == right
        elif node.op == TokenType.GREATER:
            return left > right
        elif node.op == TokenType.LESS:
            return left < right
        else:
            raise RuntimeError(f"Unknown operator: {node.op}")

    def visit_number(self, node: Number) -> float:
        """Visit a number node."""
        return node.value

    def visit_string(self, node: String) -> str:
        """Visit a string node."""
        return node.value

    def visit_identifier(self, node: Identifier) -> Any:
        """Visit an identifier node."""
        if node.name not in self.variables:
            raise RuntimeError(f"Variable '{node.name}' is not defined")
        return self.variables[node.name]

    def visit_ifstatement(self, node: IfStatement) -> str:
        """
        Process an if statement node.
        
        Args:
            node: If statement AST node
            
        Returns:
            Execution result
        """
        condition = self.visit(node.condition)
        
        statements = node.if_body if condition else node.else_body
        if statements:
            results = []
            for statement in statements:
                result = self.visit(statement)
                if result is not None:
                    results.append(result)
            return '\n'.join(str(r) for r in results)
        return ""

    def visit_trycatch(self, node: TryCatch) -> str:
        """
        Process a try-catch statement node.
        
        Args:
            node: Try-catch AST node
            
        Returns:
            Execution result
        """
        try:
            results = []
            for statement in node.try_body:
                result = self.visit(statement)
                if result is not None:
                    results.append(result)
            return '\n'.join(str(r) for r in results)
        except Exception:
            results = []
            for statement in node.catch_body:
                result = self.visit(statement)
                if result is not None:
                    results.append(result)
            return '\n'.join(str(r) for r in results)

    def visit(self, node: Any) -> Any:
        """
        Visit and process an AST node.
        
        Args:
            node: AST node
            
        Returns:
            Node execution result
        """
        method_name = f'visit_{type(node).__name__.lower()}'
        visitor = getattr(self, method_name, None)
        if visitor is None:
            raise RuntimeError(f"No visitor found for {type(node).__name__}")
        return visitor(node)

    def execute(self, code: str) -> str:
        """
        Execute Konomi code.
        
        Args:
            code: Source code to execute
            
        Returns:
            Execution result
            
        Raises:
            RuntimeError: If execution fails
        """
        try:
            lexer = Lexer(code)
            parser = Parser(lexer)
            statements = parser.parse()
            
            results = []
            for statement in statements:
                result = self.visit(statement)
                if result is not None:
                    results.append(str(result))
            
            return '\n'.join(results)
        except Exception as e:
            raise RuntimeError(str(e))
