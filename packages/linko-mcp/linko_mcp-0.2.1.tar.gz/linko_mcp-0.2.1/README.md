# Linko MCP

A Model Context Protocol (MCP) extension that allows LLMs (Large Language Models) to access Linko (https://www.linko.study) study notes and resources. It's designed to be used with `uvx` for a seamless, installation-free experience.

## Features

- Search and retrieve notes from Linko
- Find learning resources by title, author, or subject
- Get information about your knowledge distribution across subjects
- AI-specific tools for AI assistants to create and manage their own notes
- Built-in rate limiting to prevent API overload
- Secure credential handling with environment variables

## Available MCP Tools

Linko MCP provides two distinct sets of tools:

### Tools for Humans

These tools provide access to the user's own learning materials:

- `get_notes`: Retrieve and search through user's notes with filtering options
  - Search notes using keywords (with semantic embedding for relevance)
  - Filter notes by subject/topic
  - Filter notes by resource (book, article, video, etc.)
  - Filter notes by time period

- `get_resources`: Find books, articles, and other learning resources
  - Search resources by title or author using keywords
  - Filter resources by subject/topic
  - Filter resources by type (books, videos, articles, podcasts)
  - Filter resources by completion status

- `get_subjects`: Browse knowledge areas and subjects
  - View distribution of user's notes and resources across subjects
  - Get details about a specific subject including notes count and resources count
  - Discover which subjects user has the most content in

### Tools for AI Assistants

These tools allow the AI to manage its own notes for cognitive continuity (requires a separate Linko account):

- `get_notes_for_AI`: Retrieve the AI's own notes
  - Semantically search AI's notes
  - Filter by subject or time period
  - Browse recent notes

- `create_note_for_AI`: Create a new note in the AI's account
  - Store information for future reference
  - Build knowledge continuity between sessions

- `update_note_for_AI`: Modify an existing note
  - Update previously stored information
  - Refine understanding as new information is acquired

- `delete_note_for_AI`: Remove a previously created note
  - Clean up outdated or incorrect information

## Prerequisites

- A Linko account for yourself - Sign up at [www.linko.study](https://www.linko.study) if you don't have one
- A separate Linko account for your AI assistant (recommended for AI-specific features)
- [uv](https://github.com/astral-sh/uv) Python package manager (for uvx command)

## Installation

The package is designed to be used with `uvx` and doesn't need to be installed directly. Simply configure your LLM to use the MCP server with uvx as shown in the setup section below.

If you still want to install the package for development or other purposes:

### From PyPI

```bash
pip install linko-mcp
```

## Setup with Claude Desktop, Cursor or Other MCP-Compatible Host

```json
{
  "mcpServers": {
    "linko": {
      "command": "uvx",
      "args": ["--from", "linko-mcp", "mcp-server-linko"],
      "env": {
        "LINKO_USERNAME": "your_personal_linko_email@example.com",
        "LINKO_PASSWORD": "your_personal_linko_password"
      }
    },
    "linko_for_AI": {
      "command": "uvx",
      "args": ["--from", "linko-mcp", "mcp-server-linko-for-ai"],
      "env": {
        "LINKO_AI_USERNAME": "your_ai_linko_email@example.com",
        "LINKO_AI_PASSWORD": "your_ai_linko_password"
      }
    }
  }
}
```

You can also define the environment variables in your local environment without setting it in the json.


3. Restart your LLM application

## Usage Examples

### For Human Tools

You can ask your LLM to:

- "Find my notes about machine learning"
- "Show me my resources for psychology"
- "What subjects do I have notes on?"
- "Get my most recent notes"
- "Find books about quantum computing"
- "Show my completed resources"

### For AI Tools

These require the AI to have its own Linko account:

- AI can create notes about your project or conversation: "I'll make a note about this design pattern for future reference"
- AI can retrieve its previous knowledge: "Let me check my notes about your project"
- AI can update its understanding: "I'll update my notes about your preferences"

## Human vs. AI Accounts: Important Distinction

Linko MCP uses two separate services:

1. **Human Account (`mcp-server-linko`)**: 
   - Provides AI assistants READ-ONLY access to YOUR notes and resources
   - Uses YOUR Linko credentials
   - AI cannot modify your notes or resources

2. **AI Account (`mcp-server-linko-for-ai`)**:
   - Provides AI assistants READ/WRITE access to THEIR OWN notes
   - Uses a SEPARATE Linko account created specifically for the AI
   - Allows AI to maintain cognitive continuity between sessions
   - Keeps AI's notes separate from your personal study materials

**We strongly recommend using separate accounts** to maintain a clear separation between your notes and the AI's notes.

## AI-specific Features

The `mcp-server-linko-for-ai` server enables AI assistants to:

- Create their own notes in a dedicated Linko account
- Update or delete their notes
- Retrieve their own notes for continuity between sessions and cognitive growth

### Note-taking Best Practices for AI

AI assistants should focus on capturing:

1. High-level concepts and architectural patterns
2. User preferences for coding style and project organization
3. Project requirements and business logic
4. Conceptual challenges and reasoning behind solutions
5. Evolving understanding of the project

## Security Notes

### Environment Variables for Credentials

For improved security, we recommend using environment variables for your Linko credentials:

1. Set environment variables in your system or session as shown in the setup section
2. Use the configuration with environment variables (no need to specify them again in the JSON)
3. Ensure your environment variables are set before starting your LLM application

## Technical Details

### Rate Limiting

The Linko MCP includes built-in rate limiting to prevent excessive API calls to the Linko service. By default, the rate limiter is configured to allow:

- 2 requests per second
- Maximum burst of 10 requests

The rate limiter implements a token bucket algorithm that works with both synchronous and asynchronous code.

### Authentication

The MCP handles authentication in the following order:

1. Look for stored tokens in `~/.linko/auth.json` (or `~/.linko/auth_ai.json` for AI)
2. Attempt to refresh expired tokens
3. Fall back to environment variables for credentials
4. Fall back to command line arguments

## Troubleshooting

If you encounter issues:

1. Enable verbose logging with the `--verbose` flag:
```bash
linko-mcp --verbose
```

2. Check the log files in the `logs` directory of the package

## License

MIT

## Contact

For questions or support, please contact linko.assistant@gmail.com or open an issue on GitHub. 