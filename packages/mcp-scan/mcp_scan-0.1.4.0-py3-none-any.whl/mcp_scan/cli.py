import sys
import argparse
from .MCPScanner import MCPScanner

WELL_KNOWN_MCP_PATHS = [
    "~/.codeium/windsurf/mcp_config.json",  # windsurf
    "~/.cursor/mcp.json",  # cursor
    "~/Library/Application Support/Claude/claude_desktop_config.json",  # Claude Desktop
]


def main():
    parser = argparse.ArgumentParser(description="MCP Scanner CLI")
    parser.add_argument(
        "--checks-per-server",
        type=int,
        default=1,
        help="Number of checks to perform on each server, values greater than 1 help catch non-deterministic behavior",
    )
    parser.add_argument(
        "--storage-file",
        type=str,
        default="~/.mcp-scan",
        help="Path to previous scan results",
    )
    parser.add_argument(
        "--base-url",
        type=str,
        default="https://mcp.invariantlabs.ai/",
        help="Base URL for the checking server",
    )
    parser.add_argument(
        "--server-timeout",
        type=float,
        default=10,
        help="Number of seconds to wait while trying a mcp server",
    )
    parser.add_argument(
        "files", type=str, nargs="*", default=WELL_KNOWN_MCP_PATHS, help="Files to scan"
    )
    args = parser.parse_args()
    scanner = MCPScanner(**vars(args))
    scanner.start()

    sys.exit(0)


if __name__ == "__main__":
    main()
