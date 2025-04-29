# Connect with a client
# uv run simple_client.py
from python_a2a import A2AClient
from python_a2a.models.message import Message, MessageRole
from python_a2a.models.content import TextContent

client = A2AClient("http://localhost:8001")

# Create a message with text content
message = Message(
    content=TextContent(text="must visit places in utah in may"),
    role=MessageRole.USER
)

# Send a message
response = client.send_message(message)
print (response.content)

