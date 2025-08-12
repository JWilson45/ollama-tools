import ollama
import pathlib

def read_file(path: str) -> str:
    # Restrict reading files to current working directory
    base_path = pathlib.Path.cwd()
    file_path = base_path / path
    try:
        file_path = file_path.resolve()
        if not str(file_path).startswith(str(base_path)):
            return "Error: Access to the specified file is not allowed."
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

tools = {
    "read_file": read_file,
}

def main():
    user_input = "Read notes.txt in this folder."
    # First call to ollama.chat with tools as functions
    resp = ollama.chat(
        messages=[{"role": "user", "content": user_input}],
        tools=[read_file],
        model="qwen3:4b",
    )
    # Extract tool calls from resp.message.tool_calls
    tool_calls = resp.message.tool_calls or []
    tool_results = {}
    for call in tool_calls:
        tool_name = call.function.name
        tool_args = call.function.arguments or {}
        if tool_name in tools:
            result = tools[tool_name](**tool_args)
            tool_results[tool_name] = result
        else:
            tool_results[tool_name] = f"Tool {tool_name} not found."

    # Build follow-up messages with user and assistant messages as dicts
    followup_messages = [
        {"role": "user", "content": user_input},
        {
            "role": "assistant",
            "content": resp.message.content,
            "tool_calls": resp.message.tool_calls
        }
    ]
    for tool_name, result in tool_results.items():
        followup_messages.append({"role": "tool", "name": tool_name, "content": result})

    final_response = ollama.chat(messages=followup_messages, model="qwen3:4b")
    print(final_response.message.content)

if __name__ == "__main__":
    main()
