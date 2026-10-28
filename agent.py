import os
import json
from groq import Groq
from dotenv import load_dotenv
from tools.datetime_tool import get_current_datetime
from tools.web_search import web_search
from tools.file_reader import read_file

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Get the current date and time.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information about any topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read and return the content of a text or PDF file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "The file path to read"}
                },
                "required": ["path"],
            },
        },
    },
]


def execute_tool(tool_name: str, tool_args: dict) -> str:
    """Execute the tool called by the agent."""
    if tool_name == "get_current_datetime":
        return get_current_datetime()
    elif tool_name == "web_search":
        return web_search(tool_args["query"])
    elif tool_name == "read_file":
        return read_file(tool_args["path"])
    else:
        return f"Unknown tool: {tool_name}"


def run_agent(user_message: str) -> tuple[str, list]:
    """
    Run the agent loop:
    1. Send message to LLM with available tools
    2. If LLM calls a tool, execute it and send result back
    3. Repeat until LLM gives a final answer
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant with access to tools. "
                "Use them when needed to answer the user's question accurately."
            ),
        },
        {"role": "user", "content": user_message},
    ]

    steps = []

    while True:
        response = client.chat.completions.create(
            model=os.getenv("LLM_MODEL", "openai/gpt-oss-20b"),
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content, steps

        messages.append(
            {
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in message.tool_calls
                ],
            }
        )

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            tool_result = execute_tool(tool_name, tool_args)

            steps.append(
                {"tool": tool_name, "args": tool_args, "result": tool_result[:200]}
            )

            messages.append(
                {"role": "tool", "tool_call_id": tool_call.id, "content": tool_result}
            )


if __name__ == "__main__":
    questions = [
        "What time is it right now?",
        "Search for the latest news about robotics and AI",
    ]
    for q in questions:
        print(f"\nQ: {q}")
        answer, steps = run_agent(q)
        print(f"Tools used: {[s['tool'] for s in steps]}")
        print(f"A: {answer}")
