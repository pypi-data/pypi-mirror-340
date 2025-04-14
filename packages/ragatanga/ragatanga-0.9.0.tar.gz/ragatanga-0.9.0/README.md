# Ragatanga Ontology Management System

A comprehensive system for managing ontologies with multi-tenant support, RESTful API, FastMCP integration, and intelligent navigation capabilities.

[![Package Version](https://img.shields.io/badge/version-0.9.0-blue.svg)](https://github.com/jquant/ragatanga-mcp/releases)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Multi-tenant Architecture**: Isolate ontologies across different tenants
- **Ontology Management**: Upload, query, delete, and modify ontologies
- **RESTful API**: Complete API with OpenAPI documentation
- **SPARQL Query Support**: Execute complex queries against ontologies
- **Pheromone-based Navigation**: Intelligent ontology exploration with reinforced learning paths
- **MCP Agent Integration**: Conversational agents powered by Model Context Protocol
- **Redis Integration**: Upstash Redis for persistence and caching
- **File Format Support**: Turtle (.ttl) as default format with support for various RDF formats
- **GraphDB Integration**: Connect to existing semantic databases

## Installation

### As a Package (Recommended)

Ragatanga is available as a package on GitHub Packages. See [INSTALL.md](INSTALL.md) for detailed instructions on how to configure pip and install the package.

```bash
# Quick installation (after configuring pip for GitHub Packages)
pip install ragatanga
```

### From Source

1. Clone the repository:
   ```
   git clone https://github.com/jquant/ragatanga-mcp.git
   cd ragatanga-mcp
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file:
   ```
   cp .env.example .env
   ```

4. Edit the `.env` file with your configuration

## Usage

### As a Python Package

```python
from ragatanga.shared.ontology_service import OntologyManager

# Initialize the ontology manager
ontology_manager = OntologyManager(tenant_id="my_tenant")

# Query an ontology
results = ontology_manager.execute_sparql(
    ontology_id="my_ontology", 
    query="SELECT ?s ?p ?o WHERE { ?s ?p ?o . } LIMIT 10"
)

# Process results
for result in results:
    print(result)
```

### Running the Agent

```python
from ragatanga.agent import run_agent

# Configure the agent
config = {
    "tenant_id": "my_tenant",
    "model": "gpt-4o"
}

# Run the agent
run_agent(config)
```

Or directly from the command line:

```bash
python agent.py --model gpt-4o
```

## System Architecture

Ragatanga consists of several integrated components:

- **Ontology Service**: Core service for managing and querying ontologies
- **Storage Services**: Persistence layer for ontologies and metadata
- **Ant Colony Services**: Pheromone-based intelligent navigation
- **Auth Services**: Authentication and tenant management
- **MCP Integration**: Fast Model Context Protocol integration for AI agents

## Running the API

Using Python directly:
```
python app.py
```

Using uvicorn directly:
```
uvicorn shared.ontology_service.api:app --reload
```

Using uv (fast Python package installer):
```
# Install uv
pip install uv

# Create and activate environment
uv venv
source .venv/bin/activate  # On Unix/Mac
# OR
.venv\Scripts\activate  # On Windows

# Install dependencies
uv pip install -r requirements.txt

# Run the application
uv run python app.py
```

## API Endpoints

### Tenant Management

- `GET /tenants/` - List all available tenants
- `POST /tenants/` - Create a new tenant
- `GET /tenants/{tenant_id}/ontologies` - List all ontologies for a tenant

### Ontology Management

- `POST /tenants/{tenant_id}/ontologies/` - Upload a new ontology file (supports various formats, stored as .ttl)
- `DELETE /tenants/{tenant_id}/ontologies/{ontology_id}` - Delete an ontology
- `GET /tenants/{tenant_id}/ontologies/{ontology_id}/stats` - Get ontology statistics
- `POST /tenants/{tenant_id}/ontologies/{ontology_id}/query` - Execute SPARQL queries

## MCP Capabilities

The integrated Model Context Protocol (MCP) server provides the following capabilities:

### Ontology Management Tools

- `query_ontology` - Get information about a specific URI
- `search_ontology` - Search for entities in the ontology
- `execute_sparql` - Run SPARQL queries against the ontology
- `get_class_props` - Get properties of a specific class
- `get_class_instances` - Get instances of a specific class
- `get_subgraph` - Get a visual representation of the ontology

### Intelligent Navigation

- `explore_with_pheromones` - Navigate the ontology using ant colony optimization
- `reinforce_knowledge_path` - Strengthen successful navigation paths
- `analyze_knowledge_trails` - Examine emergent knowledge pathways
- `visualize_knowledge_network` - Generate a Mermaid diagram of the knowledge graph

### Natural Language Tools

- `find_concept_uri` - Map natural language terms to formal ontology URIs
- `explore_concept` - Explore a concept described in natural language
- `reinforce_concept_path` - Reinforce paths between natural language concepts

### Ontology Modification

- `create_class` - Add a new class to the ontology
- `create_property` - Add a new property to the ontology
- `create_individual` - Add a new individual instance
- `update_entity_property` - Modify properties of an entity
- `remove_entity` - Remove an entity from the ontology

## Using the API

### Swagger UI

API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `DEBUG` - Enable debug mode (default: False)
- `UPSTASH_REDIS_REST_URL` - Upstash Redis URL
- `UPSTASH_REDIS_REST_TOKEN` - Upstash Redis token
- `RAGATANGA_ONTOLOGY_PATH` - Path to ontology files (default: ontologies/default)
- `ONTOLOGY_FORMAT` - Ontology serialization format (default: turtle)
- `ENABLE_LLM_COMPLETIONS` - Enable LLM-powered entity completion (default: false)
- `OPENAI_API_KEY` - OpenAI API key (if LLM completions enabled)
- `OPENAI_MODEL` - OpenAI model to use (default: gpt-4o)

## Context Propagation in WebSocket Tools

The server uses a context propagation mechanism to ensure that tools invoked through WebSocket connections have access to the shared application state. When a tool is called via a WebSocket, the following happens:

1. The `server_lifespan` context manager initializes services (graph service, session service) and adds them to the service registry.
2. This shared state is yielded from the lifespan and automatically added to the Starlette app's scope.
3. When handling WebSocket tool calls in `handle_tools_call()`:
   - The shared state is retrieved from `websocket.scope.get('state')` 
   - The session context for the current connection is stored in a global variable (`_SESSION_CONTEXT_{connection_id}`)
   - The service registry is stored in a global variable (`_SERVICE_REGISTRY`)
   - Tools can access these globals through enhanced getter functions in `server_tools.py`

This approach ensures that tools invoked through WebSocket connections have access to:
- The current SessionContext (tenant/ontology ID, etc.)
- The service registry (graph service, session service, etc.)
- Any other shared state needed by tools

If you implement new tools, you can use the existing `get_session_context()` and `get_registry()` helper functions which will automatically find the correct context information.

## License

MIT
