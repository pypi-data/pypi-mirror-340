# MCP Server: RepairWorld

This is an [MCP (Model Context Protocol)](https://pypi.org/project/mcp/) server that exposes tools for interacting with a repair request API. It allows AI models to create, retrieve, and list repair requests using structured tools.

## 🚀 Features

- ✅ MCP-compliant server built with [`fastmcp`](https://pypi.org/project/mcp/)
- 🔧 Tools to:
  - Create a repair request
  - View a repair request by ID
  - View all repair requests
- 🌐 Customizable API base URL and authentication key via CLI
- 🧩 Easy to integrate with [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/), Claude or other MCP-compatible agents

## 📦 Installation

You can install this package from PyPI:

```bash
pip install mcp-server-repairworld
