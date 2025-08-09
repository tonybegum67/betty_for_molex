"""
Clipboard helper utilities for Betty AI Assistant.
Provides copy-to-clipboard functionality for responses.
"""

import streamlit as st
import streamlit.components.v1 as components
import json


def create_copy_button(text: str, button_id: str) -> bool:
    """
    Creates a copy-to-clipboard button using Streamlit components.
    
    Args:
        text: The text to copy to clipboard
        button_id: Unique identifier for the button
        
    Returns:
        True if the button was clicked, False otherwise
    """
    # Escape special characters for JavaScript
    escaped_text = json.dumps(text)
    
    # JavaScript code for copying to clipboard
    copy_script = f"""
    <script>
    function copyToClipboard_{button_id}() {{
        const text = {escaped_text};
        
        // Modern clipboard API (preferred)
        if (navigator.clipboard && window.isSecureContext) {{
            navigator.clipboard.writeText(text).then(function() {{
                // Show success message
                const button = document.getElementById('copy_btn_{button_id}');
                const originalText = button.innerText;
                button.innerText = '✅ Copied!';
                button.style.backgroundColor = '#4CAF50';
                
                // Reset button after 2 seconds
                setTimeout(function() {{
                    button.innerText = originalText;
                    button.style.backgroundColor = '';
                }}, 2000);
            }}).catch(function(err) {{
                console.error('Failed to copy: ', err);
                fallbackCopyToClipboard(text);
            }});
        }} else {{
            // Fallback for older browsers or non-secure contexts
            fallbackCopyToClipboard(text);
        }}
    }}
    
    function fallbackCopyToClipboard(text) {{
        // Create a temporary textarea element
        const textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed";
        textArea.style.left = "-999999px";
        textArea.style.top = "-999999px";
        document.body.appendChild(textArea);
        
        // Select and copy the text
        textArea.focus();
        textArea.select();
        
        try {{
            const successful = document.execCommand('copy');
            if (successful) {{
                const button = document.getElementById('copy_btn_{button_id}');
                const originalText = button.innerText;
                button.innerText = '✅ Copied!';
                button.style.backgroundColor = '#4CAF50';
                
                setTimeout(function() {{
                    button.innerText = originalText;
                    button.style.backgroundColor = '';
                }}, 2000);
            }}
        }} catch (err) {{
            console.error('Fallback copy failed: ', err);
        }}
        
        // Clean up
        document.body.removeChild(textArea);
    }}
    </script>
    
    <button 
        id="copy_btn_{button_id}"
        onclick="copyToClipboard_{button_id}()"
        style="
            background-color: #f0f2f6;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 4px 8px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
        "
        onmouseover="this.style.backgroundColor='#e0e2e6'"
        onmouseout="this.style.backgroundColor='#f0f2f6'"
    >
        📋 Copy
    </button>
    """
    
    # Render the HTML/JavaScript component
    components.html(copy_script, height=35)
    
    return False  # Since this is a JavaScript-only interaction


def create_inline_copy_button(text: str, button_id: str, button_text: str = "📋") -> None:
    """
    Creates a small inline copy button suitable for placement next to feedback buttons.
    
    Args:
        text: The text to copy to clipboard
        button_id: Unique identifier for the button
        button_text: Text or emoji to display on the button
    """
    escaped_text = json.dumps(text)
    
    copy_script = f"""
    <style>
    .copy-btn-{button_id} {{
        background-color: transparent;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 2px 6px;
        cursor: pointer;
        font-size: 16px;
        transition: all 0.2s ease;
        display: inline-block;
    }}
    .copy-btn-{button_id}:hover {{
        background-color: #f0f2f6;
        transform: scale(1.05);
    }}
    .copy-btn-{button_id}.copied {{
        background-color: #d4edda !important;
        border-color: #28a745 !important;
    }}
    </style>
    
    <button 
        class="copy-btn-{button_id}"
        onclick="(function() {{
            const text = {escaped_text};
            const button = event.target;
            
            if (navigator.clipboard && window.isSecureContext) {{
                navigator.clipboard.writeText(text).then(function() {{
                    button.classList.add('copied');
                    button.innerHTML = '✅';
                    setTimeout(function() {{
                        button.classList.remove('copied');
                        button.innerHTML = '{button_text}';
                    }}, 2000);
                }}).catch(function(err) {{
                    // Fallback method
                    const textArea = document.createElement('textarea');
                    textArea.value = text;
                    textArea.style.position = 'fixed';
                    textArea.style.opacity = '0';
                    document.body.appendChild(textArea);
                    textArea.select();
                    try {{
                        document.execCommand('copy');
                        button.classList.add('copied');
                        button.innerHTML = '✅';
                        setTimeout(function() {{
                            button.classList.remove('copied');
                            button.innerHTML = '{button_text}';
                        }}, 2000);
                    }} catch (err) {{
                        console.error('Copy failed:', err);
                    }}
                    document.body.removeChild(textArea);
                }});
            }} else {{
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = text;
                textArea.style.position = 'fixed';
                textArea.style.opacity = '0';
                document.body.appendChild(textArea);
                textArea.select();
                try {{
                    document.execCommand('copy');
                    button.classList.add('copied');
                    button.innerHTML = '✅';
                    setTimeout(function() {{
                        button.classList.remove('copied');
                        button.innerHTML = '{button_text}';
                    }}, 2000);
                }} catch (err) {{
                    console.error('Copy failed:', err);
                }}
                document.body.removeChild(textArea);
            }}
        }})()"
        title="Copy response to clipboard"
    >
        {button_text}
    </button>
    """
    
    components.html(copy_script, height=30)


def create_copy_code_button(code: str, language: str, button_id: str) -> None:
    """
    Creates a copy button specifically for code blocks.
    
    Args:
        code: The code to copy
        language: Programming language for syntax highlighting
        button_id: Unique identifier for the button
    """
    escaped_code = json.dumps(code)
    
    code_block_html = f"""
    <style>
    .code-container-{button_id} {{
        position: relative;
        background-color: #f6f8fa;
        border-radius: 6px;
        padding: 16px;
        margin: 10px 0;
    }}
    .copy-code-btn-{button_id} {{
        position: absolute;
        top: 8px;
        right: 8px;
        background-color: #ffffff;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        padding: 4px 8px;
        cursor: pointer;
        font-size: 12px;
        transition: all 0.2s ease;
    }}
    .copy-code-btn-{button_id}:hover {{
        background-color: #f3f4f6;
    }}
    .copy-code-btn-{button_id}.copied {{
        background-color: #d4edda !important;
        border-color: #28a745 !important;
        color: #28a745;
    }}
    .code-content-{button_id} {{
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        font-size: 14px;
        line-height: 1.5;
        overflow-x: auto;
        white-space: pre;
    }}
    </style>
    
    <div class="code-container-{button_id}">
        <button 
            class="copy-code-btn-{button_id}"
            onclick="(function() {{
                const code = {escaped_code};
                const button = event.target;
                
                if (navigator.clipboard && window.isSecureContext) {{
                    navigator.clipboard.writeText(code).then(function() {{
                        button.classList.add('copied');
                        button.innerHTML = '✅ Copied';
                        setTimeout(function() {{
                            button.classList.remove('copied');
                            button.innerHTML = '📋 Copy';
                        }}, 2000);
                    }});
                }} else {{
                    const textArea = document.createElement('textarea');
                    textArea.value = code;
                    textArea.style.position = 'fixed';
                    textArea.style.opacity = '0';
                    document.body.appendChild(textArea);
                    textArea.select();
                    try {{
                        document.execCommand('copy');
                        button.classList.add('copied');
                        button.innerHTML = '✅ Copied';
                        setTimeout(function() {{
                            button.classList.remove('copied');
                            button.innerHTML = '📋 Copy';
                        }}, 2000);
                    }} catch (err) {{
                        console.error('Copy failed:', err);
                    }}
                    document.body.removeChild(textArea);
                }}
            }})()"
        >
            📋 Copy
        </button>
        <pre class="code-content-{button_id}"><code>{code}</code></pre>
    </div>
    """
    
    components.html(code_block_html, height=150)