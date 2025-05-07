from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add a and b."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b."""
    return a * b

@tool
def encode_base64(data: str) -> str:
    """Encode a string to base64."""
    import base64
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')

@tool
def decode_base64(encoded_str: str) -> str:
    """Decode a base64 encoded string."""
    import base64
    return base64.b64decode(encoded_str).decode('utf-8')

def get_tools():
    return [add, multiply, encode_base64, decode_base64]