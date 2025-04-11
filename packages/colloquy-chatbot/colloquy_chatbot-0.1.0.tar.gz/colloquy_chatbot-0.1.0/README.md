# Colloquy

A more intuitive and consistent interface on top of existing chatbot APIs.

## Installation

```bash
pip install colloquy_chatbot
```

## Quick Start

```python
from colloquy_chatbot import OpenAIBot, ClaudeBot, PromptFunction

# Create a basic OpenAI chatbot
openai_bot = OpenAIBot(instructions="You are a helpful assistant.")

# Or use Claude
claude_bot = ClaudeBot(instructions="You are a helpful assistant.")

# Send a message and get a response
response = openai_bot.prompt("Hello, can you help me?")
print(response)  # Bot's response

# Create a chatbot with function calling
def get_weather(location="New York"):
    return f"It's sunny in {location}"

weather_bot = OpenAIBot(
    instructions="You can check the weather.",
    functions=[
        PromptFunction(get_weather, 
                       description="Get the current weather for a location")
    ]
)

weather_response = weather_bot.prompt("What's the weather like in Tokyo?")
print(weather_response)
```

## Chatbot Types

### OpenAIBot

The main chatbot implementation that uses OpenAI's API:

```python
from colloquy_chatbot import OpenAIBot

bot = OpenAIBot(instructions="You are a helpful assistant.")  # Optional system message

response = bot.prompt("Hello!")
print(response)

# Access conversation history
print(bot.history)
```

### ClaudeBot

The chatbot implementation that uses Anthropic's Claude API:

```python
from colloquy_chatbot import ClaudeBot

bot = ClaudeBot(instructions="You are a helpful assistant.")  # Optional system message

response = bot.prompt("Hello!")
print(response)

# Access conversation history
print(bot.history)
```

### EchoBot

A simple bot for testing that echoes back the input:

```python
from colloquy_chatbot import EchoBot

bot = EchoBot()
response = bot.prompt("Hello!")
print(response)  # "Hello!"
```

### Custom Bots

Create your own bot by extending the ChatBot class:

```python
from colloquy_chatbot import ChatBot, BotMessage

class ReverseBot(ChatBot):
    async def send_prompt(self):
        last_message = self.history[-1]
        reversed = last_message.text[::-1]
        return BotMessage(reversed)

bot = ReverseBot()
print(await bot.prompt("Hello"))  # "olleH"
```

## Function Calling

Colloquy makes it easy to enable function calling with both OpenAI and Claude:

### With OpenAI

```python
from colloquy_chatbot import OpenAIBot, prompt_function

# Define a function
@prompt_function(description="Calculate the area of a rectangle",
                parameter_descriptions={
                    "length": "The length of the rectangle",
                    "width": "The width of the rectangle"
                })
def calculate_area(length=1, width=1):
    return length * width

# Create a bot with the function
bot = OpenAIBot(
    functions=[calculate_area]
)

# The AI can now use the function when appropriate
response = bot.prompt("What's the area of a 5x3 rectangle?")
print(response)
```

### With Claude

```python
from colloquy_chatbot import ClaudeBot, prompt_function

# Define a function
@prompt_function(description="Calculate the area of a rectangle",
                parameter_descriptions={
                    "length": "The length of the rectangle",
                    "width": "The width of the rectangle"
                })
def calculate_area(length=1, width=1):
    return length * width

# Create a bot with the function
bot = ClaudeBot(
    functions=[calculate_area]
)

# Claude can now use the function when appropriate
response = bot.prompt("What's the area of a 5x3 rectangle?")
print(response)
```

It can infer a lot from the function definition itself:
* It can determine the name from the name of the function
  - It understands both `lambda: "foo"` and `def test(): return "foo"`, but only the latter has a name attached
* Default parameters are used to infer the type when they are specified
  - Type hints are helpful at development time, but default parameters are used at runtime

These inferences are there to make your life easier, but you can always override everything but parameter names like this:

```python
@prompt_function(
    name="some-other-name",
    description="Calculate the area of a rectangle",
    parameter_descriptions={
        "length": "The length of the rectangle",
        "width": "The width of the rectangle"
    }
)
def calculate_area(length=1, width=1):
    return length * width
```

Positional arguments get translated into an object before being sent to OpenAI, so feel free to use them in your functions. The goal is to allow you to define functions in a way that is intuitive, while still translating into a form supported by the API.

### Environment Variables

- `OPENAI_API_KEY`: Required for using OpenAIBot
- `ANTHROPIC_API_KEY`: Required for using ClaudeBot

## License

MIT
