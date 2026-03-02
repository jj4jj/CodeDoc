# Analysis Module

## Overview

The **Analysis Module** is the core engine of CodeWiki's dependency analysis system. It provides comprehensive repository analysis capabilities, including file structure parsing, multi-language AST (Abstract Syntax Tree) analysis, and call graph generation. This module serves as the foundation for understanding code relationships across diverse programming languages.

### Purpose

The Analysis Module enables:
- **Repository Structure Analysis**: Scanning and filtering repository file trees
- **Multi-Language Support**: Analyzing code in Python, JavaScript, TypeScript, Java, C#, C, C++, PHP, and Go
- **Call Graph Generation**: Building comprehensive function/method call relationship graphs
- **Dependency Mapping**: Extracting component dependencies for documentation generation

### Key Features

- **Language-Agnostic Analysis**: Unified interface for analyzing multiple programming languages
- **Configurable Filtering**: Include/exclude patterns for targeted analysis
- **Security-Conscious**: Safe file access with path validation
- **Automatic Cleanup**: Managed temporary directory handling for cloned repositories
- **Visualization Ready**: Cytoscape.js compatible output for interactive graph rendering

---

## Architecture

### Component Hierarchy

```mermaid
graph TB
    subgraph "Analysis Module"
        AS[AnalysisService<br/>Central Orchestrator]
        CGA[CallGraphAnalyzer<br/>Multi-Language Analysis]
        RA[RepoAnalyzer<br/>Structure Analysis]
    end
    
    subgraph "Analyzers Module"
        PA[PythonASTAnalyzer]
        JSA[TreeSitterJSAnalyzer]
        TSA[TreeSitterTSAnalyzer]
        JA[TreeSitterJavaAnalyzer]
        CSA[TreeSitterCSharpAnalyzer]
        CA[TreeSitterCAnalyzer]
        CppA[TreeSitterCppAnalyzer]
        PHA[TreeSitterPHPAnalyzer]
        GoA[TreeSitterGoAnalyzer]
    end
    
    subgraph "Models Module"
        Node[Node<br/>Component Model]
        CR[CallRelationship<br/>Call Edge Model]
        AR[AnalysisResult<br/>Result Container]
    end
    
    subgraph "External Dependencies"
        DP[DependencyParser<br/>AST Parser Module]
        Clone[Repository Cloning<br/>Utility]
    end
    
    AS --> CGA
    AS --> RA
    CGA --> PA
    CGA --> JSA
    CGA --> TSA
    CGA --> JA
    CGA --> CSA
    CGA --> CA
    CGA --> CppA
    CGA --> PHA
    CGA --> GoA
    CGA --> Node
    CGA --> CR
    AS --> AR
    DP --> AS
    AS --> Clone
    
    style AS fill:#4A90D9,stroke:#2E5C8A,stroke-width:2px,color:#fff
    style CGA fill:#4A90D9,stroke:#2E5C8A,stroke-width:2px,color:#fff
    style RA fill:#4A90D9,stroke:#2E5C8A,stroke-width:2px,color:#fff
    style Node fill:#5CB85C,stroke:#3D8B3D,stroke-width:2px,color:#fff
    style CR fill:#5CB85C,stroke:#3D8B3D,stroke-width:2px,color:#fff
    style AR fill:#5CB85C,stroke:#3D8B3D,stroke-width:2px,color:#fff
```

### Module Dependencies

```mermaid
graph LR
    subgraph "Current Module: analysis"
        AM[Analysis Module]
    end
    
    subgraph "Sibling Modules"
        AN[Analyzers Module<br/>Language-specific parsers]
        MD[Models Module<br/>Data structures]
        AP[AST Parser Module<br/>DependencyParser]
    end
    
    subgraph "Parent Module"
        DA[Dependency Analyzer<br/>Parent Module]
    end
    
    subgraph "Consumer Modules"
        DG[Documentation Generator]
        WA[Web Application]
        CLI[CLI Tool]
    end
    
    AM --> AN
    AM --> MD
    AM --> AP
    DA --> AM
    DG --> AM
    WA --> AM
    CLI --> AM
    
    style AM fill:#4A90D9,stroke:#2E5C8A,stroke-width:2px,color:#fff
    style DA fill:#D9534F,stroke:#A83230,stroke-width:2px,color:#fff
    style DG fill:#F0AD4E,stroke:#C98B3D,stroke-width:2px,color:#fff
    style WA fill:#F0AD4E,stroke:#C98B3D,stroke-width:2px,color:#fff
    style CLI fill:#F0AD4E,stroke:#C98B3D,stroke-width:2px,color:#fff
```

---

## Core Components

### 1. AnalysisService

**File**: `codewiki/src/be/dependency_analyzer/analysis/analysis_service.py`

**Purpose**: Central orchestrator for the complete repository analysis workflow.

**Responsibilities**:
- Repository cloning and validation
- Coordination between RepoAnalyzer and CallGraphAnalyzer
- Multi-language filtering and support
- Result consolidation and cleanup management
- Both local and remote (GitHub) repository analysis

**Key Methods**:

| Method | Description |
|--------|-------------|
| `analyze_local_repository()` | Analyze a local repository folder with language filtering |
| `analyze_repository_full()` | Complete analysis including call graph generation |
| `analyze_repository_structure_only()` | Lightweight structure analysis without call graphs |
| `_clone_repository()` | Clone GitHub repository to temporary directory |
| `_analyze_structure()` | Build file tree with include/exclude filtering |
| `_analyze_call_graph()` | Perform multi-language AST analysis |
| `_cleanup_repository()` | Clean up temporary cloned repository |

**Usage Example**:
```python
from codewiki.src.be.dependency_analyzer.analysis.analysis_service import AnalysisService

service = AnalysisService()
result = service.analyze_repository_full(
    github_url="https://github.com/owner/repo",
    include_patterns=["*.py", "*.js"],
    exclude_patterns=["*test*", "*__pycache__*"]
)
```

**See Also**: [Documentation Generator Module](documentation_generator.md) - Uses AnalysisService for code analysis

---

### 2. CallGraphAnalyzer

**File**: `codewiki/src/be/dependency_analyzer/analysis/call_graph_analyzer.py`

**Purpose**: Multi-language call graph analysis orchestrator that coordinates language-specific analyzers.

**Responsibilities**:
- Routing files to appropriate language-specific analyzers
- Aggregating function nodes and call relationships
- Resolving call relationships across files
- Deduplicating relationships
- Generating visualization data (Cytoscape.js format)
- Generating LLM-optimized format

**Supported Languages**:
- Python (AST-based)
- JavaScript (Tree-sitter)
- TypeScript (Tree-sitter)
- Java (Tree-sitter)
- C# (Tree-sitter)
- C (Tree-sitter)
- C++ (Tree-sitter)
- PHP (Tree-sitter)
- Go (Tree-sitter)

**Key Methods**:

| Method | Description |
|--------|-------------|
| `analyze_code_files()` | Complete analysis of multiple code files |
| `extract_code_files()` | Extract code files from file tree structure |
| `_analyze_*_file()` | Language-specific analysis methods (9 variants) |
| `_resolve_call_relationships()` | Match function calls to definitions |
| `_deduplicate_relationships()` | Remove duplicate caller-callee pairs |
| `_generate_visualization_data()` | Create Cytoscape.js compatible graph data |
| `generate_llm_format()` | Generate LLM-optimized analysis format |
| `_select_most_connected_nodes()` | Filter to most connected nodes for large repos |

**Data Flow**:

```mermaid
sequenceDiagram
    participant AS as AnalysisService
    participant CGA as CallGraphAnalyzer
    participant LA as Language Analyzer
    participant Node as Node Model
    participant Rel as CallRelationship
    
    AS->>CGA: extract_code_files(file_tree)
    CGA-->>AS: List[CodeFile]
    
    AS->>CGA: analyze_code_files(files, base_dir)
    
    loop For each code file
        CGA->>CGA: Route by language
        CGA->>LA: analyze_*_file(path, content)
        LA-->>CGA: functions, relationships
        CGA->>Node: Store function nodes
        CGA->>Rel: Store call relationships
    end
    
    CGA->>CGA: _resolve_call_relationships()
    CGA->>CGA: _deduplicate_relationships()
    CGA->>CGA: _generate_visualization_data()
    CGA-->>AS: Analysis result dict
```

**See Also**: [Analyzers Module](analyzers.md) - Contains language-specific analyzer implementations

---

### 3. RepoAnalyzer

**File**: `codewiki/src/be/dependency_analyzer/analysis/repo_analyzer.py`

**Purpose**: Repository structure analyzer that builds filtered file tree representations.

**Responsibilities**:
- Building hierarchical file tree structures
- Applying include/exclude pattern filtering
- Security validation (symlink detection, path escape prevention)
- File counting and size calculation
- Permission error handling

**Key Methods**:

| Method | Description |
|--------|-------------|
| `analyze_repository_structure()` | Main entry point for structure analysis |
| `_build_file_tree()` | Recursively build file tree with security checks |
| `_should_exclude_path()` | Check if path matches exclude patterns |
| `_should_include_file()` | Check if file matches include patterns |
| `_count_files()` | Count total files in tree |
| `_calculate_size()` | Calculate total size in KB |

**Pattern Matching**:
- Uses `fnmatch` for Unix shell-style wildcard matching
- Supports directory and file name patterns
- Default ignore patterns for common non-code directories

**Security Features**:
- Symlink rejection
- Path escape detection (prevents accessing files outside repo)
- Permission error handling

**See Also**: [Models Module](models.md) - Defines data structures used by RepoAnalyzer

---

## Data Models

### Node

**File**: `codewiki/src/be/dependency_analyzer/models/core.py`

Represents a code component (function, method, class, etc.) in the dependency graph.

```python
class Node(BaseModel):
    id: str                      # Unique identifier
    name: str                    # Component name
    component_type: str          # Type: function, method, class, etc.
    file_path: str              # Absolute file path
    relative_path: str          # Path relative to repo root
    depends_on: Set[str]        # Set of component IDs this depends on
    source_code: Optional[str]  # Source code snippet
    start_line: int             # Starting line number
    end_line: int               # Ending line number
    has_docstring: bool         # Whether docstring exists
    docstring: str              # Docstring content
    parameters: Optional[List[str]]  # Parameter names
    node_type: Optional[str]    # function, method, class, etc.
    base_classes: Optional[List[str]]  # For classes
    class_name: Optional[str]   # Parent class name (for methods)
    display_name: Optional[str] # Human-readable name
    component_id: Optional[str] # Fully qualified identifier
```

### CallRelationship

**File**: `codewiki/src/be/dependency_analyzer/models/core.py`

Represents a function/method call relationship between two components.

```python
class CallRelationship(BaseModel):
    caller: str          # ID of calling function
    callee: str          # ID of called function
    call_line: Optional[int]  # Line number where call occurs
    is_resolved: bool    # Whether callee was found in analyzed code
```

### AnalysisResult

**File**: `codewiki/src/be/dependency_analyzer/models/analysis.py`

Container for complete analysis results.

```python
class AnalysisResult(BaseModel):
    repository: Repository           # Repository metadata
    functions: List[Node]           # All discovered functions/methods
    relationships: List[CallRelationship]  # All call relationships
    file_tree: Dict[str, Any]       # Hierarchical file structure
    summary: Dict[str, Any]         # Analysis statistics
    visualization: Dict[str, Any]   # Cytoscape.js graph data
    readme_content: Optional[str]   # README file content
```

---

## Data Flow

### Complete Analysis Workflow

```mermaid
flowchart TD
    Start([Start Analysis]) --> Clone[Clone Repository]
    Clone --> Structure[Analyze Structure<br/>RepoAnalyzer]
    Structure --> Extract[Extract Code Files<br/>CallGraphAnalyzer]
    Extract --> Filter{Language Filter?}
    Filter -->|Yes| LangFilter[Filter by Languages]
    Filter -->|No| Analyze
    LangFilter --> Analyze[Analyze Files<br/>CallGraphAnalyzer]
    
    subgraph "Multi-Language Analysis"
        Analyze --> Route{Route by Language}
        Route -->|Python| PyAnalyze[Python AST Analyzer]
        Route -->|JavaScript| JSAnalyze[TreeSitter JS Analyzer]
        Route -->|TypeScript| TSAnalyze[TreeSitter TS Analyzer]
        Route -->|Java| JavaAnalyze[TreeSitter Java Analyzer]
        Route -->|C#| CSharpAnalyze[TreeSitter C# Analyzer]
        Route -->|C| CAnalyze[TreeSitter C Analyzer]
        Route -->|C++| CppAnalyze[TreeSitter C++ Analyzer]
        Route -->|PHP| PHPAnalyze[TreeSitter PHP Analyzer]
        Route -->|Go| GoAnalyze[TreeSitter Go Analyzer]
        
        PyAnalyze --> Aggregate[Aggregate Results]
        JSAnalyze --> Aggregate
        TSAnalyze --> Aggregate
        JavaAnalyze --> Aggregate
        CSharpAnalyze --> Aggregate
        CAnalyze --> Aggregate
        CppAnalyze --> Aggregate
        PHPAnalyze --> Aggregate
        GoAnalyze --> Aggregate
    end
    
    Aggregate --> Resolve[Resolve Call Relationships]
    Resolve --> Dedup[Deduplicate Relationships]
    Dedup --> Viz[Generate Visualization Data]
    Viz --> Readme[Read README File]
    Readme --> Cleanup[Cleanup Temp Directory]
    Cleanup --> Result([Return AnalysisResult])
    
    style Start fill:#5CB85C,stroke:#3D8B3D,color:#fff
    style Result fill:#5CB85C,stroke:#3D8B3D,color:#fff
    style Clone fill:#4A90D9,stroke:#2E5C8A,color:#fff
    style Structure fill:#4A90D9,stroke:#2E5C8A,color:#fff
    style Extract fill:#4A90D9,stroke:#2E5C8A,color:#fff
    style Analyze fill:#4A90D9,stroke:#2E5C8A,color:#fff
    style Aggregate fill:#F0AD4E,stroke:#C98B3D,color:#fff
    style Resolve fill:#F0AD4E,stroke:#C98B3D,color:#fff
    style Dedup fill:#F0AD4E,stroke:#C98B3D,color:#fff
    style Viz fill:#F0AD4E,stroke:#C98B3D,color:#fff
    style Cleanup fill:#D9534F,stroke:#A83230,color:#fff
```

### Component Interaction Flow

```mermaid
sequenceDiagram
    participant Client as Client Module
    participant AS as AnalysisService
    participant RA as RepoAnalyzer
    participant CGA as CallGraphAnalyzer
    participant LA as Language Analyzers
    participant Models as Data Models
    
    Client->>AS: analyze_repository_full(url)
    activate AS
    
    AS->>AS: _clone_repository(url)
    AS->>AS: _parse_repository_info(url)
    
    AS->>RA: analyze_repository_structure(dir)
    activate RA
    RA-->>AS: file_tree, summary
    deactivate RA
    
    AS->>CGA: extract_code_files(file_tree)
    activate CGA
    CGA-->>AS: code_files[]
    
    AS->>CGA: analyze_code_files(files, dir)
    
    loop For each file
        CGA->>LA: analyze_*_file(path, content)
        activate LA
        LA-->>CGA: functions[], relationships[]
        deactivate LA
        CGA->>Models: Store Node
        CGA->>Models: Store CallRelationship
    end
    
    CGA->>CGA: _resolve_call_relationships()
    CGA->>CGA: _deduplicate_relationships()
    CGA->>CGA: _generate_visualization_data()
    CGA-->>AS: analysis_result dict
    deactivate CGA
    
    AS->>AS: _read_readme_file(dir)
    AS->>Models: Build AnalysisResult
    AS->>AS: _cleanup_repository(dir)
    
    AS-->>Client: AnalysisResult
    deactivate AS
```

---

## Integration with Other Modules

### Dependency Analyzer Module

The Analysis Module is a child of the **Dependency Analyzer** parent module, which provides:
- Utility functions for security and pattern matching
- Repository cloning utilities
- Base configuration and constants

**See**: [Dependency Analyzer Module](dependency_analyzer.md)

### Analyzers Module

The Analysis Module depends on the **Analyzers Module** for language-specific parsing:
- Each language has a dedicated analyzer implementation
- Analyzers return `Node` and `CallRelationship` objects
- Analysis Module routes files to appropriate analyzers

**See**: [Analyzers Module](analyzers.md)

### Models Module

The Analysis Module uses data models from the **Models Module**:
- `Node`: Represents code components
- `CallRelationship`: Represents function calls
- `AnalysisResult`: Container for analysis output
- `Repository`: Repository metadata

**See**: [Models Module](models.md)

### AST Parser Module

The **DependencyParser** in the AST Parser Module uses AnalysisService:
- Wraps AnalysisService for component extraction
- Converts analysis results to component dictionaries
- Saves dependency graphs to JSON

**See**: [AST Parser Module](ast_parser.md)

### Documentation Generator Module

The **Documentation Generator** consumes analysis results:
- Uses AnalysisService for repository analysis
- Processes Node and CallRelationship data
- Generates documentation from dependency graphs

**See**: [Documentation Generator Module](documentation_generator.md)

### Web Application Module

The **Web Application** integrates analysis capabilities:
- BackgroundWorker processes analysis jobs
- CacheManager stores analysis results
- WebRoutes expose analysis endpoints
- GitHubRepoProcessor handles repository input

**See**: [Web Application Module](web_application.md)

### CLI Module

The **CLI Tool** provides command-line access:
- CLIDocumentationGenerator wraps analysis functionality
- GitManager handles repository operations
- ProgressTracker shows analysis progress

**See**: [CLI Module](cli.md)

---

## Configuration

### Include/Exclude Patterns

The Analysis Module supports configurable file filtering:

**Default Include Patterns** (from `dependency_analyzer.utils.patterns`):
- Code file extensions for supported languages

**Default Exclude Patterns**:
- `.git/`, `__pycache__/`, `node_modules/`
- `*.pyc`, `*.pyo`, `*.so`, `*.dll`
- Test directories, build artifacts, etc.

**Custom Patterns**:
```python
service = AnalysisService()
result = service.analyze_repository_full(
    github_url="https://github.com/owner/repo",
    include_patterns=["src/**/*.py", "lib/**/*.js"],
    exclude_patterns=["*test*", "*mock*", "*fixture*"]
)
```

### Language Filtering

Limit analysis to specific languages:
```python
result = service.analyze_local_repository(
    repo_path="/path/to/repo",
    languages=["python", "javascript"],
    max_files=50
)
```

---

## Error Handling

### Security Validation

- **Path Traversal Prevention**: All file paths are validated against repository root
- **Symlink Rejection**: Symlinks are excluded to prevent escape attacks
- **Safe File Access**: Uses `safe_open_text()` for all file reads

### Exception Handling

- **File Analysis Errors**: Logged and skipped, analysis continues
- **Repository Clone Failures**: Raised as RuntimeError with cleanup
- **Permission Errors**: Handled gracefully during tree traversal
- **Cleanup on Failure**: Temporary directories cleaned on exceptions

### Logging

Comprehensive logging at DEBUG level:
- File analysis progress
- Function/relationship counts
- Resolution and deduplication statistics
- Error details with tracebacks

---

## Performance Considerations

### Large Repository Handling

- **File Limiting**: `max_files` parameter limits analysis scope
- **Node Selection**: `_select_most_connected_nodes()` filters to important nodes
- **Deduplication**: Removes duplicate relationships to reduce noise

### Memory Management

- **Streaming Analysis**: Files processed one at a time
- **Automatic Cleanup**: Temporary directories removed after analysis
- **Destructor Cleanup**: `__del__` ensures cleanup on service destruction

### Visualization Optimization

- **Resolved Relationships Only**: Only resolved calls included in graph
- **Summary Statistics**: Quick overview without full graph traversal
- **Cytoscape.js Format**: Optimized for client-side rendering

---

## Testing Guidelines

### Unit Testing

Test individual components:
- `RepoAnalyzer`: Pattern matching, file tree building
- `CallGraphAnalyzer`: Relationship resolution, deduplication
- `AnalysisService`: Workflow orchestration, cleanup

### Integration Testing

Test complete workflows:
- Local repository analysis
- GitHub repository cloning and analysis
- Multi-language repository analysis
- Error handling and cleanup

### Test Fixtures

Use sample repositories with:
- Single-language projects
- Multi-language projects
- Edge cases (symlinks, permissions, large files)

---

## Future Enhancements

### Planned Features

1. **Additional Language Support**: Rust, Ruby, Swift
2. **Cross-Language Call Detection**: Inter-language call resolution
3. **Incremental Analysis**: Cache-based re-analysis of changed files
4. **Dependency Version Tracking**: Package dependency analysis
5. **Code Quality Metrics**: Complexity, coverage integration

### Architecture Improvements

1. **Plugin System**: Dynamic language analyzer loading
2. **Parallel Analysis**: Multi-threaded file processing
3. **Streaming Results**: Progressive result delivery for large repos
4. **Graph Database Storage**: Persistent dependency graph storage

---

## API Reference

### AnalysisService

```python
class AnalysisService:
    def __init__(self)
    def analyze_local_repository(repo_path, max_files=100, languages=None) -> Dict
    def analyze_repository_full(github_url, include_patterns=None, exclude_patterns=None) -> AnalysisResult
    def analyze_repository_structure_only(github_url, include_patterns=None, exclude_patterns=None) -> Dict
    def cleanup_all()
```

### CallGraphAnalyzer

```python
class CallGraphAnalyzer:
    def __init__(self)
    def analyze_code_files(code_files, base_dir) -> Dict
    def extract_code_files(file_tree) -> List[Dict]
    def generate_llm_format() -> Dict
```

### RepoAnalyzer

```python
class RepoAnalyzer:
    def __init__(include_patterns=None, exclude_patterns=None)
    def analyze_repository_structure(repo_dir) -> Dict
```

---

## Related Documentation

- [Dependency Analyzer Module](dependency_analyzer.md) - Parent module overview
- [Analyzers Module](analyzers.md) - Language-specific analyzers
- [Models Module](models.md) - Data model definitions
- [AST Parser Module](ast_parser.md) - DependencyParser implementation
- [Documentation Generator Module](documentation_generator.md) - Analysis consumer
- [Web Application Module](web_application.md) - Web integration
- [CLI Module](cli.md) - Command-line interface
