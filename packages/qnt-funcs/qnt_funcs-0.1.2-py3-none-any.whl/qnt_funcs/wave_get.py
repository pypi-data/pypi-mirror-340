"""
WaveGet - Advanced interface for WaveState syntax error correction

This module provides a simplified and enhanced interface to the WaveState
functionality, allowing for automatic syntax error correction in Python code.
"""

import sys
import os
import re
import inspect
import traceback
from wavestate import WaveState

class WaveGet:
    """Advanced interface for WaveState with additional utilities."""
    
    _enabled = False
    _debug = False
    _auto_fix = True
    
    @classmethod
    def enable(cls, debug=False, auto_fix=True):
        """Enable WaveState with advanced options."""
        if not cls._enabled:
            WaveState.enable(debug=debug)
            cls._enabled = True
            cls._debug = debug
            cls._auto_fix = auto_fix
            print("WaveGet enabled - syntax errors will be automatically fixed")
    
    @classmethod
    def disable(cls):
        """Disable WaveState and all advanced features."""
        if cls._enabled:
            WaveState.disable()
            cls._enabled = False
            cls._debug = False
            print("WaveGet disabled - normal Python syntax rules apply")
    
    @classmethod
    def execute(cls, code, globals_dict=None, locals_dict=None):
        """Execute code with automatic syntax error correction."""
        if globals_dict is None:
            # Get the caller's globals
            frame = inspect.currentframe().f_back
            globals_dict = frame.f_globals
            locals_dict = frame.f_locals
        
        if not cls._enabled:
            cls.enable(debug=cls._debug)
        
        # First, manually fix common syntax errors
        fixed_code = cls._fix_syntax_errors(code)
        
        if cls._debug and fixed_code != code:
            print("\nManually fixed syntax:")
            print(f"Original:\n{code}")
            print(f"Fixed:\n{fixed_code}")
        
        # Then try to execute the fixed code
        try:
            exec(fixed_code, globals_dict, locals_dict)
            print("✓ Code executed successfully")
            return None
        except Exception as e:
            if cls._debug:
                print(f"Error executing code: {e}")
                traceback.print_exc()
            raise
    
    @classmethod
    def _fix_syntax_errors(cls, code):
        """Fix common syntax errors in the code."""
        if not isinstance(code, str):
            return code
        
        # Split the code into lines for line-by-line processing
        lines = code.split('\n')
        fixed_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Skip empty lines and comments
            if not line.strip() or line.strip().startswith('#'):
                fixed_lines.append(line)
                i += 1
                continue
            
            # Fix missing colon in control structures
            if re.match(r'^\s*(if|for|while|def|class|with|try|except|finally)\s+.*[^:]\s*$', line):
                line = line.rstrip() + ':'
            
            # Fix standalone try/except statements without colon
            if line.strip() == 'try' or re.match(r'^\s*except(\s+[\w.]+)?\s*$', line):
                line = line.rstrip() + ':'
            
            # Fix missing comma in tuple
            if '(' in line and ')' in line:
                # Look for patterns like (1, 2 3)
                line = re.sub(r'(\(\s*[\w\'\"]+\s*,\s*[\w\'\"]+)\s+([\w\'\"]+\s*\))', r'\1, \2', line)
            
            # Fix missing commas in dictionaries
            if '{' in line and '}' in line and ':' in line:
                # Look for patterns like {"key": value "key2": value2}
                dict_pattern = r'(\{\s*.*?[\'\"]?\s*:\s*[\w\'\"]+)\s+([\'\"][\w]+[\'\"]?\s*:)'
                line = re.sub(dict_pattern, r'\1, \2', line)
                
                # Also look for patterns like {"key": value, "key2": value2 "key3": value3}
                dict_pattern2 = r'([\'\"][\w]+[\'\"]?\s*:\s*[\w\'\"]+,\s*[\'\"][\w]+[\'\"]?\s*:\s*[\w\'\"]+)\s+([\'\"][\w]+[\'\"]?\s*:)'
                line = re.sub(dict_pattern2, r'\1, \2', line)
                
                # Handle numeric values in dictionaries
                dict_pattern3 = r'([\'\"][\w]+[\'\"]?\s*:\s*\d+)\s+([\'\"][\w]+[\'\"]?\s*:)'
                line = re.sub(dict_pattern3, r'\1, \2', line)
            
            # Fix missing commas in lists
            if '[' in line and ']' in line:
                # Look for patterns like [1 2 3]
                list_pattern = r'\[\s*([\w\'\"]+)(\s+[\w\'\"]+)+\s*\]'
                if re.search(list_pattern, line):
                    # Replace spaces between elements with commas
                    list_content = re.search(r'\[\s*(.*?)\s*\]', line).group(1)
                    elements = re.split(r'\s+', list_content)
                    fixed_list = '[' + ', '.join(elements) + ']'
                    line = re.sub(r'\[\s*.*?\s*\]', fixed_list, line)
            
            # Fix list comprehension with missing bracket - CORRECTED
            if '[' in line and 'for' in line and 'in' in line and 'range(' in line:
                # Handle list comprehension with range specifically
                match = re.search(r'(.*?\[.*?for.*?in\s+range\s*\()([^)]*?)(\].*)', line)
                if match:
                    # This is a list comprehension with range missing a closing parenthesis
                    prefix, range_args, suffix = match.groups()
                    line = f"{prefix}{range_args}){suffix}"
                else:
                    # Check if we're missing the closing bracket
                    if line.count('[') > line.count(']'):
                        # Extract the variable name if this is an assignment
                        var_match = re.match(r'^\s*(\w+)\s*=\s*\[', line)
                        if var_match:
                            var_name = var_match.group(1)
                            # Extract the expression and range arguments
                            comp_match = re.search(r'\[\s*(.+?)\s+for\s+(.+?)\s+in\s+range\s*\(\s*(.+?)\s*$', line)
                            if comp_match:
                                expr, loop_var, range_args = comp_match.groups()
                                line = f"{var_name} = [{expr} for {loop_var} in range({range_args})]"
            
            # Fix missing closing parenthesis (do this after list comprehension fix)
            elif line.count('(') > line.count(')'):
                line = line.rstrip() + ')' * (line.count('(') - line.count(')'))
            
            # Fix general list comprehension missing closing bracket
            elif '[' in line and line.count('[') > line.count(']'):
                line = line.rstrip() + ']' * (line.count('[') - line.count(']'))
            
            # Fix indentation errors in function definitions
            if line.strip().startswith('def ') and line.rstrip().endswith(':'):
                # Check if the next line is indented
                if i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].startswith(' ') and not lines[i + 1].startswith('\t'):
                    # Add indentation to the next line
                    lines[i + 1] = '    ' + lines[i + 1]
            
            fixed_lines.append(line)
            i += 1
        
        return '\n'.join(fixed_lines)
    
    @classmethod
    def eval(cls, expr, globals_dict=None, locals_dict=None):
        """Evaluate an expression with automatic syntax error correction."""
        if globals_dict is None:
            # Get the caller's globals
            frame = inspect.currentframe().f_back
            globals_dict = frame.f_globals
            locals_dict = frame.f_locals
        
        if not cls._enabled:
            cls.enable(debug=cls._debug)
        
        # Fix common syntax errors
        fixed_expr = cls._fix_syntax_errors(expr)
        
        if cls._debug and fixed_expr != expr:
            print("Fixed expression:")
            print(f"Original: {expr}")
            print(f"Fixed: {fixed_expr}")
        
        # Evaluate the fixed expression
        try:
            result = eval(fixed_expr, globals_dict, locals_dict)
            return result
        except Exception as e:
            if cls._debug:
                print(f"Error evaluating expression: {e}")
                traceback.print_exc()
            raise
    
    @classmethod
    def fix_file(cls, file_path):
        """Fix syntax errors in a file and save the corrected version."""
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            return False
        
        try:
            # Read the file
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Fix the syntax
            fixed_content = cls._fix_syntax_errors(content)
            
            # If changes were made, write back to the file
            if fixed_content != content:
                with open(file_path, 'w') as f:
                    f.write(fixed_content)
                
                print(f"✓ Fixed syntax errors in {file_path}")
                return True
            else:
                print(f"No syntax errors found in {file_path}")
                return True
        except Exception as e:
            print(f"Error fixing file {file_path}: {e}")
            return False

# Create simplified interface functions for backward compatibility
def wave(command, debug=False):
    """Simplified interface to WaveGet functionality."""
    if command.lower() == 'enable':
        WaveGet.enable(debug=debug)
    elif command.lower() == 'disable':
        WaveGet.disable()
    else:
        print(f"Unknown command: {command}")

def execute(code, globals_dict=None, locals_dict=None):
    """Execute code with automatic syntax error correction."""
    return WaveGet.execute(code, globals_dict, locals_dict)

def eval_expr(expr, globals_dict=None, locals_dict=None):
    """Evaluate an expression with automatic syntax error correction."""
    return WaveGet.eval(expr, globals_dict, locals_dict)

def fix_file(file_path):
    """Fix syntax errors in a file and save the corrected version."""
    return WaveGet.fix_file(file_path)

def test_wave():
    """Run a comprehensive test suite for WaveGet functionality."""
    print("\n=== Testing WaveGet ===")
    
    # Define test cases with syntax errors
    test_code = [
        "result = [x*2 for x in range(10]",  # Missing closing bracket
        "result = len('hello'",              # Missing closing parenthesis
        "x = 5\nif x > 3\n    print(x)"      # Missing colon
    ]
    
    # First try with WaveGet disabled
    print("\nWithout WaveGet:")
    WaveGet.disable()
    
    for i, code in enumerate(test_code):
        print(f"\nTest {i+1}: {code.replace(chr(10), ' ')}")
        try:
            # Use built-in exec to show the error
            exec(code)
            print("✓ Code executed successfully (unexpected)")
        except Exception as e:
            print(f"✗ Error (expected): {e}")
    
    # Now enable WaveGet and try again
    print("\nWith WaveGet enabled:")
    WaveGet.enable(debug=True)
    
    for i, code in enumerate(test_code):
        print(f"\nTest {i+1}: {code.replace(chr(10), ' ')}")
        try:
            # For list comprehension, create a complete example
            if "for x in range" in code:
                # Create a complete script that prints the result
                full_code = f"""
print(f'Result: {{result}}')
"""
                execute(full_code)
            else:
                execute(code)
            print("✓ Code executed successfully")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    # Test expression evaluation
    print("\nTesting expression evaluation:")
    expressions = [
        "[x*2 for x in range(5]",  # Missing closing bracket
        "len('hello'",             # Missing closing parenthesis
        "5 + 3 * (2 + 1"           # Missing closing parenthesis
    ]
    
    for expr in expressions:
        print(f"\nEvaluating: {expr}")
        try:
            result = eval_expr(expr)
            print(f"✓ Result: {result}")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    # Disable WaveGet when done
    WaveGet.disable()
    print("\n=== Testing complete ===")

# Allow running this file directly
if __name__ == "__main__":
    print("WaveGet - Advanced WaveState Interface")
    print("=====================================")
    print("1. Enable WaveGet")
    print("2. Disable WaveGet")
    print("3. Run test suite")
    print("4. Fix a Python file")
    print("5. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            debug = input("Enable debug mode? (y/n): ").lower() == 'y'
            wave('enable', debug=debug)
        elif choice == '2':
            wave('disable')
        elif choice == '3':
            test_wave()
        elif choice == '4':
            file_path = input("Enter the path to the Python file: ")
            fix_file(file_path)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")