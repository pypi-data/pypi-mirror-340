### 简介

- 使用 json5 配置 基于视图的 工作流

#### 命令

```sh
  uv sync # 安装依赖
  rm -rf src/**/__pycache__ # 清空编译产物
  uv run -m src.index -h # 查看帮助
  uv run -m src.index --workflowJsonAddress tdd.json5 --imagesDirPath $PWD/src/common/images/tdd --isDebug # vscode 示例
  uv run -m src.test.index # 测试
```

#### Tip

- pyautogui.moveTo(0, 0) wins 上会报错 pyautogui.FailSafeException: PyAutoGUI fail-safe triggered from mouse moving to a corner of the screen. To disable this fail-safe, set pyautogui.FAILSAFE to False. DISABLING FAIL-SAFE IS NOT RECOMMENDED

#### MCP

- @modelcontextprotocol/inspector 并不是很好用 先用 vscode cline 调试
