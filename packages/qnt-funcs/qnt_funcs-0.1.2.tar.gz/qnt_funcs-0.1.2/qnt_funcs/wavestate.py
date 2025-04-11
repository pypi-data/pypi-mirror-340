"""
WaveState - Automatic syntax error correction for Python

This module provides functionality to automatically fix common syntax errors
in Python code at runtime.
"""

import sys
import traceback
import re

class WaveState:
    """
    WaveState provides automatic syntax error correction for Python code.
    """
    
    _enabled = False
    _debug = False
    _original_excepthook = None
    
    @classmethod
    def enable(cls, debug=False):
        """
        Enable WaveState syntax error correction.
        
        Args:
            debug: If True, print debug information about syntax fixes
        """
        if not cls._enabled:
            cls._original_excepthook = sys.excepthook
            sys.excepthook = cls._syntax_error_handler
            cls._enabled = True
            cls._debug = debug
            print("Wave state enabled - syntax errors will be automatically fixed")
    
    @classmethod
    def disable(cls):
        """
        Disable WaveState syntax error correction.
        """
        if cls._enabled:
            sys.excepthook = cls._original_excepthook
            cls._enabled = False
            cls._debug = False
            print("Wave state disabled - normal Python syntax rules apply")
    
    @classmethod
    def _syntax_error_handler(cls, exc_type, exc_value, exc_traceback):
        """
        Custom exception handler that attempts to fix syntax errors.
        """
        if exc_type is SyntaxError:
            # Try to fix the syntax error
            if cls._fix_syntax_error(exc_value):
                return
        
        # If we couldn't fix it or it's not a syntax error, use the original handler
        cls._original_excepthook(exc_type, exc_value, exc_traceback)
    
    @classmethod
    def _fix_syntax_error(cls, syntax_error):
        """
        Attempt to fix a syntax error.
        
        Args:
            syntax_error: The SyntaxError exception
            
        Returns:
            bool: True if the error was fixed, False otherwise
        """
        try:
            # Get information about the syntax error
            filename = syntax_error.filename
            lineno = syntax_error.lineno
            offset = syntax_error.offset
            text = syntax_error.text
            msg = str(syntax_error)
            
            if cls._debug:
                print(f"Wave state: Syntax error in {filename}, line {lineno}")
                print(f"Wave state: Error message: {msg}")
                print(f"Wave state: Error text: {text}")
            
            # Don't try to fix errors in the standard library
            if filename.startswith('<'):
                if cls._debug:
                    print("Wave state: Cannot fix errors in dynamic code")
                return False
            
            # Read the file
            with open(filename, 'r') as f:
                lines = f.readlines()
            
            # Fix the syntax error
            fixed = False
            
            # Common syntax errors and their fixes
            if "invalid syntax" in msg:
                fixed = cls._fix_invalid_syntax(lines, lineno, text, offset)
            elif "unexpected EOF" in msg or "unexpected end of file" in msg:
                fixed = cls._fix_unexpected_eof(lines, lineno, text)
            elif "expected ':'" in msg:
                fixed = cls._fix_missing_colon(lines, lineno, text)
            elif "expected an indented block" in msg:
                fixed = cls._fix_indentation(lines, lineno)
            elif "unindent does not match" in msg:
                fixed = cls._fix_unindent(lines, lineno)
            
            if fixed:
                # Write the fixed file
                with open(filename, 'w') as f:
                    f.writelines(lines)
                
                if cls._debug:
                    print("Wave state: Fixed syntax error, rerunning code")
                
                # Re-execute the file
                with open(filename, 'r') as f:
                    code = f.read()
                
                # Execute in the original context
                frame = sys._getframe(2)
                globals_dict = frame.f_globals
                locals_dict = frame.f_locals
                
                try:
                    exec(code, globals_dict, locals_dict)
                    return True
                except SyntaxError as e:
                    if cls._debug:
                        print(f"Wave state: Syntax error after fixing: {e}")
                    return False
            
            return False
        except Exception as e:
            if cls._debug:
                print(f"Wave state: Error while fixing syntax: {e}")
                traceback.print_exc()
            return False
    
    @classmethod
    def _fix_invalid_syntax(cls, lines, lineno, text, offset):
        """Fix invalid syntax errors."""
        line = lines[lineno - 1]
        
        # Missing closing bracket
        if '[' in line and ']' not in line:
            lines[lineno - 1] = line.rstrip() + ']\n'
            return True
        
        # Missing closing parenthesis
        if line.count('(') > line.count(')'):
            lines[lineno - 1] = line.rstrip() + ')' * (line.count('(') - line.count(')')) + '\n'
            return True
        
        # Missing comma in tuple
        if '(' in line and ')' in line:
            # Look for patterns like (1, 2 3)
            match = re.search(r'\(\s*[\w\'\"]+\s*,\s*[\w\'\"]+\s+[\w\'\"]+', line)
            if match:
                fixed_line = re.sub(r'(\(\s*[\w\'\"]+\s*,\s*[\w\'\"]+)\s+([\w\'\"]+)', r'\1, \2', line)
                lines[lineno - 1] = fixed_line
                return True
        
        return False
    
    @classmethod
    def _fix_unexpected_eof(cls, lines, lineno, text):
        """Fix unexpected EOF errors."""
        # Add missing closing brackets/parentheses
        line = lines[lineno - 1]
        
        # Count opening and closing brackets/parentheses in the whole file
        open_brackets = 0
        open_parens = 0
        open_braces = 0
        
        for l in lines:
            open_brackets += l.count('[') - l.count(']')
            open_parens += l.count('(') - l.count(')')
            open_braces += l.count('{') - l.count('}')
        
        # Add missing closing characters
        if open_brackets > 0 or open_parens > 0 or open_braces > 0:
            lines.append('\n')  # Add a new line
            lines.append(']' * open_brackets + ')' * open_parens + '}' * open_braces + '\n')
            return True
        
        return False
    
    @classmethod
    def _fix_missing_colon(cls, lines, lineno, text):
        """Fix missing colon errors."""
        line = lines[lineno - 1]
        
        # Add missing colon to control structures
        if re.match(r'^\s*(if|for|while|def|class|with|try|except|finally)\s+.*[^:]\s*$', line):
            lines[lineno - 1] = line.rstrip() + ':\n'
            return True
        
        return False
    
    @classmethod
    def _fix_indentation(cls, lines, lineno):
        """Fix indentation errors."""
        # Add indentation to the line after a colon
        if lineno <= len(lines) and lines[lineno - 1].rstrip().endswith(':'):
            if lineno < len(lines):
                lines[lineno] = '    ' + lines[lineno]
                return True
            else:
                # Add a pass statement if this is the last line
                lines.append('    pass\n')
                return True
        
        return False
    
    @classmethod
    def _fix_unindent(cls, lines, lineno):
        """Fix unindent errors."""
        # Adjust indentation to match the previous block
        if lineno > 1:
            prev_indent = len(lines[lineno - 2]) - len(lines[lineno - 2].lstrip())
            curr_line = lines[lineno - 1]
            curr_indent = len(curr_line) - len(curr_line.lstrip())
            
            # Find the correct indentation level
            i = lineno - 2
            while i >= 0:
                if not lines[i].strip() or lines[i].strip().startswith('#'):
                    i -= 1
                    continue
                
                prev_indent = len(lines[i]) - len(lines[i].lstrip())
                break
            
            # Adjust the current line's indentation
            lines[lineno - 1] = ' ' * prev_indent + curr_line.lstrip()
            return True
        
        return False