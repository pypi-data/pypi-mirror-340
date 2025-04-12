import os
from typing import Optional

from pydantic import Field

from fellow.clients.OpenAIClient import OpenAIClient
from fellow.commands.command import CommandContext, CommandInput


class SummarizeFileInput(CommandInput):
    filepath: str = Field(..., description="Path to the file to summarize.")
    max_chars: Optional[int] = Field(
        None, description="Optional limit on number of characters to read."
    )


def summarize_file(args: SummarizeFileInput, context: CommandContext) -> str:
    """
    Summarizes the contents of a file using OpenAIClient.
    # todo: optional use different model
    """
    if not os.path.isfile(args.filepath):
        return f"[ERROR] File not found: {args.filepath}"

    try:
        with open(args.filepath, "r", encoding="utf-8") as f:
            content = f.read(args.max_chars)

        if not content.strip():
            return "[INFO] File is empty or only contains whitespace."

        client = OpenAIClient(
            system_content="Summarize the following file content.",
            model=context["ai_client"].model,
        )
        # Adjusted to handle the tuple returned by chat()
        summary, _, _ = client.chat(
            f"Please summarize the following file content:\n\n{content}"
        )
        summary = summary.strip() if summary else "[INFO] No summary generated."
        return f"[OK] Summary:\n{summary}"

    except Exception as e:
        return f"[ERROR] Could not read or summarize file: {e}"
