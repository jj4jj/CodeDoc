# Agent 工具

Agent 工具是 AI Agent 可用于生成文档的工具集。

## 概述

AI Agent 使用这些工具来：
1. 读取代码组件
2. 查看和编辑文档文件
3. 生成子模块文档

## 工具

### read_code_components

从代码库读取代码：

```python
async def read_code_components(
    ctx: RunContext[CodeWikiDeps],
    component_ids: List[str],
) -> str:
    """Read specified code components."""
    components = ctx.deps.components
    result = []

    for comp_id in component_ids:
        if comp_id in components:
            node = components[comp_id]
            result.append(format_component(node))

    return "\n\n".join(result)
```

### str_replace_editor

编辑文档文件：

```python
async def str_replace_editor(
    ctx: RunContext[CodeWikiDeps],
    working_dir: Literal["repo", "docs"],
    command: Literal["view", "create", "str_replace", "insert", "undo_edit"],
    path: str,
    ...
) -> str:
    """View, create, or edit documentation files."""
```

可用命令：
- **view**：显示文件内容
- **create**：创建新文件
- **str_replace**：替换文件中的文本
- **insert**：在指定行插入文本
- **undo_edit**：撤销上次编辑

### generate_sub_module_documentation

为子模块生成文档：

```python
async def generate_sub_module_documentation(
    ctx: RunContext[CodeWikiDeps],
    module_names: List[str],
    ...
) -> str:
    """Generate documentation for sub-modules."""
```

## CodeWikiDeps

Agent 上下文的依赖注入：

```python
@dataclass
class CodeWikiDeps:
    absolute_docs_path: str      # Output directory
    absolute_repo_path: str     # Source repository
    registry: dict
    components: dict[str, Node] # Parsed components
    path_to_current_module: list[str]
    current_module_name: str
    module_tree: dict
    max_depth: int
    current_depth: int
    config: Config
    custom_instructions: str
```

## 使用示例

Agent 使用工具的方式如下：

```
Agent: I need to document the database module
Tool: read_code_components(["src.database.Connection"])
Tool Result: class Connection:
    def connect(self): ...

Agent: Now I'll create the documentation
Tool: str_replace_editor(command="create", path="docs/database.md", file_text="...")
```

## 相关文档

- [Agent 编排器](agent_orchestrator.md)
- [文档生成器](documentation_generator.md)