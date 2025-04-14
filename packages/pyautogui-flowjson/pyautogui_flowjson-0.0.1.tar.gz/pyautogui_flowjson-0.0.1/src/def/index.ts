import { ToolCallback } from '@modelcontextprotocol/sdk/server/mcp.js'
import z, { ZodRawShape } from 'zod'

/** Ts 辅助函数 */
function def<Args extends ZodRawShape>(obj: {
  name: string
  description: string
  argsSchema: Args
  requestHandler: ToolCallback<Args>
}) {
  return obj
}

// 业务
const Records: Record<
  string,
  {
    id: string
    content: string
  }
> = {
  key: {
    id: '999',
    content: '999的内容',
  },
}

export const SaveRecordDef = def({
  name: 'save-record',
  description: 'save 本地记录',
  argsSchema: {
    key: z.string().describe('本地记录 的 key'),
    content: z.string().describe('本地记录 的 content'),
  },
  async requestHandler({ key, content }) {
    Records[key] = {
      id: `${Object.keys(Records).length + 1}`,
      content,
    }

    return {
      content: [
        {
          type: 'text',
          text: `Save successfully id: ${Records[key].id} content: ${Records[key].content}`,
        },
      ],
    }
  },
})
// TODO 可选参数
export const GetRecordDef = def({
  name: 'get-record',
  description: 'get 本地记录',
  argsSchema: {
    key: z.string().optional().describe('本地记录 的 key'),
    id: z.string().optional().describe('本地记录 的 id'),
  },
  async requestHandler({ key, id }) {
    if (!key && !id) throw new Error('key 和 id 至少要有一个')

    const obj = key
      ? Records[key]
      : Object.values(Records).find((item) => item.id === id)
    if (!obj)
      return {
        content: [
          {
            type: 'text',
            text: '未能检索预测数据',
          },
        ],
      }
    return {
      content: [
        {
          type: 'text',
          text: `get successfully id: ${obj.id} content: ${obj.content}`,
        },
      ],
    }
  },
})
