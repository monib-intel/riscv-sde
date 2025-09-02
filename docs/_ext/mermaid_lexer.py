"""
Custom lexer for Mermaid diagrams.
"""
from pygments.lexer import RegexLexer
from pygments.token import *

class MermaidLexer(RegexLexer):
    """
    Basic lexer for Mermaid diagram syntax.
    """
    name = 'Mermaid'
    aliases = ['mermaid']
    filenames = ['*.mmd']

    tokens = {
        'root': [
            (r'(graph|flowchart|sequenceDiagram|classDiagram|stateDiagram|erDiagram|gantt|pie|journey)\b', Keyword),
            (r'(subgraph|end|style|class|click|link|linkStyle)\b', Keyword),
            (r'(-->|-->|==>|-.->|--.-|-\.-|\.-\.|===>)', Operator),
            (r'[\[\]\(\)\{\}<>]', Punctuation),
            (r'"[^"]*"', String),
            (r'[A-Za-z][A-Za-z0-9_]*', Name),
            (r'[\s]+', Text),
            (r'[^A-Za-z0-9_\s\[\]\(\)\{\}<>]+', Text),
        ]
    }

def setup(app):
    app.add_lexer('mermaid', MermaidLexer)
    
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
