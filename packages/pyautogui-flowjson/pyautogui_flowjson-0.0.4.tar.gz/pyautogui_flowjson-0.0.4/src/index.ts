import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import { z } from 'zod'
import { zodToJsonSchema } from 'zod-to-json-schema'
import pkg from '../package.json'
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js'
import { GetRecordDef, SaveRecordDef } from './def'

// McpServer
const mcpServer = new McpServer({
  name: pkg.name,
  version: pkg.version,
  capabilities: {
    resources: {},
    tools: {},
  },
})

mcpServer.tool(
  SaveRecordDef.name,
  SaveRecordDef.description,
  SaveRecordDef.argsSchema,
  SaveRecordDef.requestHandler
)

mcpServer.tool(
  GetRecordDef.name,
  GetRecordDef.description,
  GetRecordDef.argsSchema,
  GetRecordDef.requestHandler
)

// Server
const server = new Server(
  {
    name: pkg.name,
    version: pkg.version,
  },
  {
    capabilities: {
      tools: {},
    },
  }
)

// Define available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: SaveRecordDef.name,
        description: SaveRecordDef.description,
        inputSchema: zodToJsonSchema(z.object(SaveRecordDef.argsSchema)),
      },
      {
        name: GetRecordDef.name,
        description: GetRecordDef.description,
        inputSchema: zodToJsonSchema(z.object(GetRecordDef.argsSchema)),
      },
    ],
  }
})

// Handle tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    const { name, arguments: args } = request.params
    switch (name) {
      case SaveRecordDef.name: {
        // @ts-expect-error
        const res = SaveRecordDef.requestHandler(args)
        return res
      }
      case GetRecordDef.name: {
        // @ts-expect-error
        const res = GetRecordDef.requestHandler(args)
        return res
      }
      default:
        throw new Error(`Unknown tool: ${name}`)
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error)
    return {
      content: [{ type: 'text', text: `Error: ${errorMessage}` }],
      isError: true,
    }
  }
})

async function main() {
  const transport = new StdioServerTransport()
  // mcpServer
  // await mcpServer.connect(transport)
  await server.connect(transport)
  console.error('Pyautogui MCP Server running on stdio')
}

main().catch((error) => {
  console.error('Fatal error in main():', error)
  process.exit(1)
})
