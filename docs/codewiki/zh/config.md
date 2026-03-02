# 配置（后端）

后端 `Config` 类管理文档生成的运行时设置。

## 概述

`Config` 类被后端用于：
- 仓库路径
- LLM 配置
- Token 限制
- Agent 指令

## 类定义

```python
@dataclass
class Config:
    repo_path: str
    output_dir: str
    dependency_graph_dir: str
    docs_dir: str
    max_depth: int

    # LLM configuration
    llm_base_url: str
    llm_api_key: str
    main_model: str
    cluster_model: str
    fallback_model: str = ""
    fallback_models: List[str] = field(default_factory=list)
    agent_cmd: str = ""

    # Token settings
    max_tokens: int = 32768
    max_token_per_module: int = 36369
    max_token_per_leaf_module: int = 16000
    concurrency: int = 4

    # Agent instructions
    agent_instructions: Optional[Dict[str, Any]] = None
```

## 工厂方法

### from_args()

从 CLI 参数创建配置：

```python
@classmethod
def from_args(cls, args: argparse.Namespace) -> 'Config':
    repo_name = os.path.basename(os.path.normpath(args.repo_path))
    return cls(
        repo_path=args.repo_path,
        output_dir=OUTPUT_BASE_DIR,
        dependency_graph_dir=os.path.join(OUTPUT_BASE_DIR, DEPENDENCY_GRAPHS_DIR),
        docs_dir=os.path.join(OUTPUT_BASE_DIR, DOCS_DIR, f"{sanitized_repo_name}-docs"),
        max_depth=MAX_DEPTH,
        llm_base_url=LLM_BASE_URL,
        llm_api_key=LLM_API_KEY,
        main_model=MAIN_MODEL,
        cluster_model=CLUSTER_MODEL,
    )
```

### from_cli()

为 CLI 上下文创建配置：

```python
@classmethod
def from_cli(
    cls,
    repo_path: str,
    output_dir: str,
    llm_base_url: str,
    llm_api_key: str,
    main_model: str,
    cluster_model: str,
    fallback_model: str = "",
    fallback_models: Optional[List[str]] = None,
    agent_cmd: str = "",
    max_tokens: int = DEFAULT_MAX_TOKENS,
    max_token_per_module: int = DEFAULT_MAX_TOKEN_PER_MODULE,
    max_token_per_leaf_module: int = DEFAULT_MAX_TOKEN_PER_LEAF_MODULE,
    max_depth: int = MAX_DEPTH,
    agent_instructions: Optional[Dict[str, Any]] = None,
    concurrency: int = 4
) -> 'Config':
    ...
```

## 属性

```python
@property
def include_patterns(self) -> Optional[List[str]]:
    """Get file include patterns from agent instructions."""
    if self.agent_instructions:
        return self.agent_instructions.get('include_patterns')

@property
def exclude_patterns(self) -> Optional[List[str]]:
    """Get file exclude patterns from agent instructions."""

@property
def focus_modules(self) -> Optional[List[str]]:
    """Get focus modules from agent instructions."""

@property
def doc_type(self) -> Optional[str]:
    """Get documentation type from agent instructions."""
```

## 提示词补充

```python
def get_prompt_addition(self) -> str:
    """Generate prompt additions based on agent instructions."""
    additions = []

    if self.doc_type:
        doc_type_instructions = {
            'api': "Focus on API documentation: endpoints, parameters...",
            'architecture': "Focus on architecture documentation...",
            'user-guide': "Focus on user guide documentation...",
            'developer': "Focus on developer documentation...",
        }
        additions.append(doc_type_instructions.get(self.doc_type.lower(), ""))

    if self.focus_modules:
        additions.append(f"Focus on: {', '.join(self.focus_modules)}")

    return "\n".join(additions)
```

## 常量

```python
OUTPUT_BASE_DIR = 'output'
DEPENDENCY_GRAPHS_DIR = 'dependency_graphs'
DOCS_DIR = 'docs'
FIRST_MODULE_TREE_FILENAME = 'first_module_tree.json'
MODULE_TREE_FILENAME = 'module_tree.json'
OVERVIEW_FILENAME = 'overview.md'
MAX_DEPTH = 2
DEFAULT_MAX_TOKENS = 32_768
DEFAULT_MAX_TOKEN_PER_MODULE = 36_369
DEFAULT_MAX_TOKEN_PER_LEAF_MODULE = 16_000
```

## 相关文档

- [配置管理器](config_manager.md)
- [文档生成器](documentation_generator.md)