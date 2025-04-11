from collections.abc import Sequence
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
import json
import logging
from .obsidian import Obsidian, ObsidianError # Import custom error

logger = logging.getLogger(__name__) # Use module-specific logger


# --- Tool Name Constants ---
TOOL_LIST_FILES_IN_VAULT = "obsidian_list_files_in_vault"
TOOL_LIST_FILES_IN_DIR = "obsidian_list_files_in_dir"
TOOL_GET_FILE_CONTENTS = "obsidian_get_file_contents"
TOOL_BATCH_GET_FILE_CONTENTS = "obsidian_batch_get_file_contents"
TOOL_SIMPLE_SEARCH = "obsidian_simple_search"
TOOL_COMPLEX_SEARCH = "obsidian_complex_search"
TOOL_APPEND_CONTENT = "obsidian_append_content"
TOOL_PATCH_CONTENT = "obsidian_patch_content"
TOOL_DELETE_FILE = "obsidian_delete_file"
TOOL_GET_PERIODIC_NOTE = "obsidian_get_periodic_note"
TOOL_GET_RECENT_PERIODIC_NOTES = "obsidian_get_recent_periodic_notes"
TOOL_GET_RECENT_CHANGES = "obsidian_get_recent_changes"

# --- Base Handler ---
class ToolHandler():
    """Base class for MCP tool handlers for Obsidian."""
    def __init__(self, tool_name: str, api_client: Obsidian):
        """
        Initializes the handler.
        Args:
            tool_name: The name of the tool this handler manages.
            api_client: An initialized Obsidian API client instance.
        """
        self.name = tool_name
        self.api = api_client
    def get_tool_description(self) -> Tool:
        raise NotImplementedError("Subclasses must implement get_tool_description")

    async def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        # Basic validation can be added here if common across tools
        if not isinstance(args, dict):
             raise ValueError("Tool arguments must be a dictionary.")
        try:
            # Subclasses will implement the specific logic
            return await self._execute_tool(args)
        except ObsidianError as e:
            logger.error(f"Obsidian API error in tool '{self.name}': {e}")
            # Re-raise as a generic RuntimeError for MCP, but log the specific error
            raise RuntimeError(f"Obsidian API Error: {str(e)}") from e
        except ValueError as e: # Catch validation errors
             logger.warning(f"Validation error in tool '{self.name}' with args {args}: {e}")
             raise RuntimeError(f"Invalid arguments for tool '{self.name}': {str(e)}") from e
        except Exception as e:
            logger.exception(f"Unexpected error in tool '{self.name}' with args {args}: {e}")
            raise RuntimeError(f"An unexpected error occurred while running tool '{self.name}'.") from e

    async def _execute_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
         """Subclasses must implement the core tool logic here."""
         raise NotImplementedError("Subclasses must implement _execute_tool")


# --- Specific Tool Handlers ---
class ListFilesInVaultToolHandler(ToolHandler):
    def __init__(self, api_client: Obsidian):
        super().__init__(TOOL_LIST_FILES_IN_VAULT, api_client)

    def get_tool_description(self):
        return Tool(
            name=self.name,
            description="Lists all files and directories directly within the root folder of the Obsidian vault. Does not list recursively.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        )

    async def _execute_tool(self, args: dict) -> Sequence[TextContent]:
        files = self.api.list_files_in_vault()
        return [TextContent(type="text", text=json.dumps(files, indent=2))]
class ListFilesInDirToolHandler(ToolHandler):
    def __init__(self, api_client: Obsidian):
        super().__init__(TOOL_LIST_FILES_IN_DIR, api_client)

    def get_tool_description(self):
        return Tool(
            name=self.name,
            description="Lists all files and directories directly within a specific folder in the Obsidian vault. Does not list recursively. Note: Empty directories might not be listed.",
            inputSchema={
                "type": "object",
                "properties": {
                    "dirpath": {
                        "type": "string",
                        "description": "Path of the directory to list, relative to the vault root (e.g., 'Notes/Projects' or '').",
                    },
                },
                "required": ["dirpath"]
            }
        )

    async def _execute_tool(self, args: dict) -> Sequence[TextContent]:
        dirpath = args.get("dirpath")
        if dirpath is None: # Check for None explicitly, empty string is valid for root
            raise ValueError("Missing required argument: dirpath")
        files = self.api.list_files_in_dir(dirpath)
        return [TextContent(type="text", text=json.dumps(files, indent=2))]

class GetFileContentsToolHandler(ToolHandler):
    def __init__(self, api_client: Obsidian):
        super().__init__(TOOL_GET_FILE_CONTENTS, api_client)

    def get_tool_description(self):
        return Tool(
            name=self.name,
            description="Retrieves the full text content of a single specified file from the Obsidian vault.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path to the file relative to the vault root (e.g., 'Daily Notes/2024-10-26.md').",
                        "format": "path" # Keep format hint if useful for client UI
                    },
                },
                "required": ["filepath"]
            }
        )

    async def _execute_tool(self, args: dict) -> Sequence[TextContent]:
        filepath = args.get("filepath")
        if not filepath:
            raise ValueError("Missing or empty required argument: filepath")
        content = self.api.get_file_contents(filepath)
        return [TextContent(type="text", text=content)]

class SearchToolHandler(ToolHandler):
    def __init__(self, api_client: Obsidian):
        super().__init__(TOOL_SIMPLE_SEARCH, api_client)

    def get_tool_description(self):
        return Tool(
            name=self.name,
            description="Performs a simple text search across all files in the Obsidian vault. Returns a list of matching files with context snippets.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The text string to search for."
                    },
                    "context_length": {
                        "type": "integer",
                        "description": "Number of characters of context to include around each match.",
                        "default": 100,
                        "minimum": 10
                    }
                },
                "required": ["query"]
            }
        )

    async def _execute_tool(self, args: dict) -> Sequence[TextContent]:
        query = args.get("query")
        if not query:
            raise ValueError("Missing or empty required argument: query")
        context_length = args.get("context_length", 100)
        if not isinstance(context_length, int) or context_length < 10:
             raise ValueError("Invalid argument: context_length must be an integer >= 10.")
        results = self.api.search(query, context_length)

        # Formatting logic remains the same as before
        formatted_results = []
        for result in results:
            formatted_matches = []
            for match in result.get('matches', []):
                context = match.get('context', '')
                match_pos = match.get('match', {})
                start = match_pos.get('start', 0)
                end = match_pos.get('end', 0)
                formatted_matches.append({
                    'context': context,
                    'match_position': {'start': start, 'end': end}
                })
            formatted_results.append({
                'filename': result.get('filename', ''),
                'score': result.get('score', 0),
                'matches': formatted_matches
            })

        return [TextContent(type="text", text=json.dumps(formatted_results, indent=2))]

class AppendContentToolHandler(ToolHandler):
   def __init__(self, api_client: Obsidian):
       super().__init__(TOOL_APPEND_CONTENT, api_client)

   def get_tool_description(self):
       return Tool(
           name=self.name,
           description="Appends the provided text content to the end of a specified file. If the file does not exist, it will be created.",
           inputSchema={
               "type": "object",
               "properties": {
                   "filepath": {
                       "type": "string",
                       "description": "Path to the file relative to the vault root (e.g., 'Journal/Entries.md').",
                   },
                   "content": {
                       "type": "string",
                       "description": "The text content to append."
                   }
               },
               "required": ["filepath", "content"]
           }
       )

   async def _execute_tool(self, args: dict) -> Sequence[TextContent]:
       filepath = args.get("filepath")
       content = args.get("content") # Allow empty content? Yes.
       if not filepath:
           raise ValueError("Missing or empty required argument: filepath")
       if content is None:
            raise ValueError("Missing required argument: content")

       self.api.append_content(filepath, content)
       return [TextContent(type="text", text=f"Successfully appended content to {filepath}")]

class PatchContentToolHandler(ToolHandler):
   def __init__(self, api_client: Obsidian):
       super().__init__(TOOL_PATCH_CONTENT, api_client)

   def get_tool_description(self):
       valid_ops = ["append", "prepend", "replace"]
       valid_types = ["heading", "block", "frontmatter"]
       return Tool(
           name=self.name,
           description=f"Modifies content within an existing file relative to a target element (heading, block ID, or frontmatter key). Operations: {', '.join(valid_ops)}. Target types: {', '.join(valid_types)}.",
           inputSchema={
               "type": "object",
               "properties": {
                   "filepath": {"type": "string", "description": "Path to the file relative to the vault root."},
                   "operation": {"type": "string", "description": "The modification operation.", "enum": valid_ops},
                   "target_type": {"type": "string", "description": "The type of element to target.", "enum": valid_types},
                   "target": {"type": "string", "description": "Identifier for the target (e.g., heading text like '## Section Title', block ID like '^abcde', frontmatter key like 'status')."},
                   "content": {"type": "string", "description": "The text content to insert or replace with."}
               },
               "required": ["filepath", "operation", "target_type", "target", "content"]
           }
       )

   async def _execute_tool(self, args: dict) -> Sequence[TextContent]:
       required = ["filepath", "operation", "target_type", "target", "content"]
       if not all(args.get(key) for key in ["filepath", "operation", "target_type", "target"]): # Content can be empty
            raise ValueError(f"Missing or empty required arguments from: {', '.join(required)}")
       if args.get("content") is None:
            raise ValueError("Missing required argument: content")

       # Further validation could check enum values if needed, but schema should handle it
       self.api.patch_content(
           args["filepath"],
           args["operation"],
           args["target_type"],
           args["target"],
           args["content"]
       )
       return [TextContent(type="text", text=f"Successfully patched content in {args['filepath']}")]

class DeleteFileToolHandler(ToolHandler):
   def __init__(self, api_client: Obsidian):
       super().__init__(TOOL_DELETE_FILE, api_client)

   def get_tool_description(self):
       return Tool(
           name=self.name,
           description="Permanently deletes a specified file or an empty directory from the Obsidian vault. Requires explicit confirmation.",
           inputSchema={
               "type": "object",
               "properties": {
                   "filepath": {"type": "string", "description": "Path to the file or empty directory to delete, relative to the vault root."},
                   "confirm": {"type": "boolean", "description": "Must be explicitly set to 'true' to confirm deletion.", "default": False}
               },
               "required": ["filepath", "confirm"]
           }
       )

   async def _execute_tool(self, args: dict) -> Sequence[TextContent]:
       filepath = args.get("filepath")
       confirm = args.get("confirm")
       if not filepath:
           raise ValueError("Missing or empty required argument: filepath")
       if confirm is not True: # Must be exactly True
           raise ValueError("Deletion requires 'confirm' argument to be explicitly set to true.")

       self.api.delete_file(filepath)
       return [TextContent(type="text", text=f"Successfully deleted {filepath}")]

class ComplexSearchToolHandler(ToolHandler):
   def __init__(self, api_client: Obsidian):
       super().__init__(TOOL_COMPLEX_SEARCH, api_client)

   def get_tool_description(self):
       return Tool(
           name=self.name,
           description="Performs a complex search using a JsonLogic query object. Allows filtering files based on metadata (tags, path, dates, etc.). See Obsidian REST API documentation for JsonLogic details and available variables (like 'path', 'tags', 'stat.mtime').",
           inputSchema={
               "type": "object",
               "properties": {
                   "query": {
                       "type": "object",
                       "description": "A JsonLogic query object. Example: {\"and\": [{\"==\": [{\"var\": \"frontmatter.status\"}, \"active\"]}, {\"glob\": [\"Projects/*.md\", {\"var\": \"path\"}]}]}"
                   }
               },
               "required": ["query"]
           }
       )

   async def _execute_tool(self, args: dict) -> Sequence[TextContent]:
       query = args.get("query")
       if not query or not isinstance(query, dict):
           raise ValueError("Missing or invalid required argument: query (must be a non-empty JSON object)")

       results = self.api.search_json(query)
       return [TextContent(type="text", text=json.dumps(results, indent=2))]

class BatchGetFileContentsToolHandler(ToolHandler):
    def __init__(self, api_client: Obsidian):
        super().__init__(TOOL_BATCH_GET_FILE_CONTENTS, api_client)

    def get_tool_description(self):
        return Tool(
            name=self.name,
            description="Retrieves the contents of multiple specified files from the Obsidian vault. Returns a single string with each file's content preceded by a header line '# filepath' and separated by '---'. Errors encountered for individual files are included in the output.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepaths": {
                        "type": "array",
                        "items": {"type": "string", "description": "Path to a file relative to the vault root."},
                        "description": "A list of file paths to read.",
                        "minItems": 1
                    },
                },
                "required": ["filepaths"]
            }
        )

    async def _execute_tool(self, args: dict) -> Sequence[TextContent]:
        filepaths = args.get("filepaths")
        if not filepaths or not isinstance(filepaths, list):
            raise ValueError("Missing or invalid required argument: filepaths (must be a non-empty list of strings)")
        if not all(isinstance(fp, str) and fp for fp in filepaths):
             raise ValueError("Invalid argument: filepaths must contain only non-empty strings.")

        content = self.api.get_batch_file_contents(filepaths)
        return [TextContent(type="text", text=content)]

class PeriodicNotesToolHandler(ToolHandler):
    def __init__(self, api_client: Obsidian):
        super().__init__(TOOL_GET_PERIODIC_NOTE, api_client)

    def get_tool_description(self):
        return Tool(
            name=self.name,
            description=f"Retrieves the content of the current periodic note (e.g., today's daily note, this week's weekly note). Requires the Periodic Notes plugin to be configured. Valid periods: {', '.join(valid_periods)}.",
            inputSchema={
                "type": "object",
                "properties": {
                    "period": {"type": "string", "description": "The type of periodic note.", "enum": valid_periods}
                },
                "required": ["period"]
            }
        )

    async def _execute_tool(self, args: dict) -> Sequence[TextContent]:
        period = args.get("period")
        valid_periods = ["daily", "weekly", "monthly", "quarterly", "yearly"]
        if period not in valid_periods:
            raise ValueError(f"Invalid period: '{period}'. Must be one of: {', '.join(valid_periods)}")

        content = self.api.get_periodic_note(period)
        return [TextContent(type="text", text=content)]

class RecentPeriodicNotesToolHandler(ToolHandler):
    def __init__(self, api_client: Obsidian):
        super().__init__(TOOL_GET_RECENT_PERIODIC_NOTES, api_client)

    def get_tool_description(self):
        return Tool(
            name=self.name,
            description=f"Retrieves metadata (and optionally content) for the most recent periodic notes of a specified type. Requires the Periodic Notes plugin. Valid periods: {', '.join(valid_periods)}.",
            inputSchema={
                "type": "object",
                "properties": {
                    "period": {"type": "string", "description": "The type of periodic note.", "enum": valid_periods},
                    "limit": {"type": "integer", "description": "Maximum number of notes to return.", "default": 5, "minimum": 1, "maximum": 50},
                    "include_content": {"type": "boolean", "description": "Whether to include the full content of each note.", "default": False}
                },
                "required": ["period"]
            }
        )

    async def _execute_tool(self, args: dict) -> Sequence[TextContent]:
        period = args.get("period")
        valid_periods = ["daily", "weekly", "monthly", "quarterly", "yearly"]
        if period not in valid_periods:
            raise ValueError(f"Invalid period: '{period}'. Must be one of: {', '.join(valid_periods)}")

        limit = args.get("limit", 5)
        if not isinstance(limit, int) or not (1 <= limit <= 50):
            raise ValueError(f"Invalid limit: {limit}. Must be an integer between 1 and 50.")

        include_content = args.get("include_content", False)
        if not isinstance(include_content, bool):
            # Schema should catch this, but belt-and-suspenders
            raise ValueError(f"Invalid include_content: {include_content}. Must be a boolean.")

        results = self.api.get_recent_periodic_notes(period, limit, include_content)
        return [TextContent(type="text", text=json.dumps(results, indent=2))]

class RecentChangesToolHandler(ToolHandler):
    def __init__(self, api_client: Obsidian):
        super().__init__(TOOL_GET_RECENT_CHANGES, api_client)

    def get_tool_description(self):
        return Tool(
            name=self.name,
            description="Retrieves a list of files that have been most recently modified within a specified number of days. Uses a Dataview Query (DQL). Requires the Dataview plugin.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Maximum number of files to return.", "default": 10, "minimum": 1, "maximum": 100},
                    "days": {"type": "integer", "description": "How many days back to look for modifications.", "default": 90, "minimum": 1}
                },
                "required": [] # Use defaults if not provided
            }
        )

    async def _execute_tool(self, args: dict) -> Sequence[TextContent]:
        limit = args.get("limit", 10)
        days = args.get("days", 90)

        if not isinstance(limit, int) or not (1 <= limit <= 100):
            raise ValueError(f"Invalid limit: {limit}. Must be an integer between 1 and 100.")
        if not isinstance(days, int) or days < 1:
            raise ValueError(f"Invalid days: {days}. Must be a positive integer.")

        results = self.api.get_recent_changes(limit, days)
        return [TextContent(type="text", text=json.dumps(results, indent=2))]
