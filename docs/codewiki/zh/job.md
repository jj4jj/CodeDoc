# 作业模型

作业模型定义了文档生成作业的数据结构。

## 概述

作业模型包括：
- 作业状态跟踪
- 生成选项
- 统计信息
- LLM 配置

## 类

### JobStatus

```python
class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
```

### GenerationOptions

```python
@dataclass
class GenerationOptions:
    create_branch: bool = False
    github_pages: bool = False
    index_page: bool = False
    no_cache: bool = False
    custom_output: Optional[str] = None
```

### JobStatistics

```python
@dataclass
class JobStatistics:
    total_files_analyzed: int = 0
    leaf_nodes: int = 0
    max_depth: int = 0
    total_tokens_used: int = 0
```

### DocumentationJob

```python
@dataclass
class DocumentationJob:
    job_id: str
    repository_path: str
    repository_name: str
    output_directory: str
    commit_hash: str
    status: JobStatus
    generation_options: GenerationOptions
    llm_config: LLMConfig
    statistics: JobStatistics
```

## 相关文档

- [后台工作者](background_worker.md)
- [路由](routes.md)