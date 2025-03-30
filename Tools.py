from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b."""
    return a * b

@tool
def decode_base64(encoded_str: str) -> str:
    """Decode a base64 encoded string."""
    import base64
    return base64.b64decode(encoded_str).decode('utf-8')

def get_tools():
    return [multiply, decode_base64]