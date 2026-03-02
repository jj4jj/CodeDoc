# PHP & Go Analyzers Module

## Overview

The **php_go_analyzers** module provides language-specific code analysis capabilities for PHP and Go programming languages within the CodeWiki dependency analysis system. This module contains two specialized analyzers that leverage tree-sitter parsing to extract code structure, components, and dependency relationships from PHP and Go source files.

These analyzers are part of the broader [dependency_analyzer](dependency_analyzer.md) module's analyzer ecosystem, which supports multiple programming languages through a unified interface.

## Core Components

| Component | File | Purpose |
|-----------|------|---------|
| `TreeSitterPHPAnalyzer` | `codewiki/src/be/dependency_analyzer/analyzers/php.py` | Analyzes PHP files to extract classes, interfaces, traits, enums, functions, methods, and their relationships |
| `TreeSitterGoAnalyzer` | `codewiki/src/be/dependency_analyzer/analyzers/go.py` | Analyzes Go files to extract functions, methods, structs, interfaces, and call relationships |

## Architecture

```mermaid
graph TB
    subgraph "php_go_analyzers Module"
        PHP[TreeSitterPHPAnalyzer]
        GO[TreeSitterGoAnalyzer]
        NS[NamespaceResolver<br/>PHP Only]
    end
    
    subgraph "External Dependencies"
        TSPHP[tree-sitter-php]
        TSGO[tree-sitter-go]
        TREE[tree-sitter]
    end
    
    subgraph "Shared Models"
        NODE[Node]
        REL[CallRelationship]
    end
    
    PHP --> TSPHP
    PHP --> TREE
    PHP --> NS
    GO --> TSGO
    GO --> TREE
    PHP --> NODE
    PHP --> REL
    GO --> NODE
    GO --> REL
    
    style PHP fill:#e1f5fe
    style GO fill:#e1f5fe
    style NS fill:#fff3e0
```

## Component Details

### TreeSitterPHPAnalyzer

The PHP analyzer extracts comprehensive code structure from PHP files including:

**Extractable Components:**
- Classes (including abstract classes)
- Interfaces
- Traits
- Enums
- Functions
- Methods

**Dependency Relationships:**
- `use` statements (namespace imports)
- `extends` (class inheritance)
- `implements` (interface implementation)
- `new` expressions (object instantiation)
- Static method calls (`::`)
- Property promotion types (PHP 8+)

**Special Features:**
- **Namespace Resolution**: Handles PHP namespaces and use statement aliases through the `NamespaceResolver` class
- **Template Detection**: Automatically skips template files (Blade, Twig, PHTML) to avoid false positives
- **Docstring Extraction**: Captures PHPDoc comments preceding code elements
- **Parameter Extraction**: Extracts function/method parameters with type hints

```mermaid
flowchart TD
    A[PHP File Input] --> B{Is Template File?}
    B -->|Yes| C[Skip Analysis]
    B -->|No| D[Parse with tree-sitter-php]
    D --> E[Pass 1: Extract Namespace Info]
    E --> F[Pass 2: Extract Nodes]
    F --> G[Pass 3: Extract Relationships]
    G --> H[Return Nodes + Relationships]
    
    subgraph "Pass 1: Namespace"
        E1[Find namespace_definition]
        E2[Find namespace_use_declaration]
        E3[Build use_map]
    end
    
    subgraph "Pass 2: Nodes"
        F1[Extract class_declaration]
        F2[Extract interface_declaration]
        F3[Extract trait_declaration]
        F4[Extract enum_declaration]
        F5[Extract function_definition]
        F6[Extract method_declaration]
    end
    
    subgraph "Pass 3: Relationships"
        G1[use statements]
        G2[extends clauses]
        G3[implements clauses]
        G4[object_creation_expression]
        G5[scoped_call_expression]
        G6[property_promotion_parameter]
    end
    
    E --> E1
    E --> E2
    E --> E3
    F --> F1
    F --> F2
    F --> F3
    F --> F4
    F --> F5
    F --> F6
    G --> G1
    G --> G2
    G --> G3
    G --> G4
    G --> G5
    G --> G6
```

### TreeSitterGoAnalyzer

The Go analyzer extracts code structure from Go files including:

**Extractable Components:**
- Functions (top-level and package-level)
- Methods (with receiver type tracking)
- Structs
- Interfaces

**Dependency Relationships:**
- Function calls (direct and selector expressions)
- Method calls on struct receivers

**Special Features:**
- **Receiver Type Resolution**: Correctly identifies the struct type for methods, including pointer receivers (`*StructName`)
- **Call Relationship Tracking**: Maintains a `seen_relationships` set to avoid duplicate relationships
- **Component ID Generation**: Creates hierarchical IDs based on module path and struct containment

```mermaid
flowchart TD
    A[Go File Input] --> B{Parser Initialized?}
    B -->|No| C[Log Error & Skip]
    B -->|Yes| D[Parse with tree-sitter-go]
    D --> E[Traverse for Components]
    E --> F[Extract Nodes]
    F --> G[Sort by Line Number]
    G --> H[Extract Call Relationships]
    H --> I[Return Nodes + Relationships]
    
    subgraph "Component Extraction"
        E1[function_declaration]
        E2[method_declaration]
        E3[type_declaration<br/>struct/interface]
    end
    
    subgraph "Relationship Extraction"
        H1[Track current function/method]
        H2[Find call_expression nodes]
        H3[Extract callee name]
        H4[Resolve to component_id]
        H5[Check for duplicates]
    end
    
    E --> E1
    E --> E2
    E --> E3
    H --> H1
    H --> H2
    H --> H3
    H --> H4
    H --> H5
```

## Data Flow

```mermaid
sequenceDiagram
    participant Client as AnalysisService
    participant PHP as TreeSitterPHPAnalyzer
    participant GO as TreeSitterGoAnalyzer
    participant Models as Node/CallRelationship
    
    Client->>PHP: analyze_php_file(path, content, repo_path)
    activate PHP
    PHP->>PHP: Initialize NamespaceResolver
    PHP->>PHP: Check template file patterns
    PHP->>PHP: Parse with tree-sitter-php
    PHP->>PHP: Extract namespace & use statements
    PHP->>PHP: Extract nodes (classes, functions, etc.)
    PHP->>PHP: Extract relationships
    PHP-->>Client: Tuple[List[Node], List[CallRelationship]]
    deactivate PHP
    
    Client->>GO: analyze_go_file(path, content, repo_path)
    activate GO
    GO->>GO: Initialize tree-sitter-go parser
    GO->>GO: Traverse AST for components
    GO->>GO: Extract functions, methods, structs, interfaces
    GO->>GO: Extract call relationships
    GO-->>Client: Tuple[List[Node], List[CallRelationship]]
    deactivate GO
    
    Client->>Models: Process returned nodes
    Client->>Models: Process returned relationships
```

## Integration with Dependency Analyzer

The PHP and Go analyzers integrate with the broader [dependency_analyzer](dependency_analyzer.md) system through the [AnalysisService](dependency_analyzer.md#analysisservice):

```mermaid
graph LR
    subgraph "dependency_analyzer"
        AS[AnalysisService]
        RA[RepoAnalyzer]
        CGA[CallGraphAnalyzer]
    end
    
    subgraph "php_go_analyzers"
        PHP[TreeSitterPHPAnalyzer]
        GO[TreeSitterGoAnalyzer]
    end
    
    subgraph "models"
        NODE[Node]
        REL[CallRelationship]
        AR[AnalysisResult]
    end
    
    AS --> RA
    RA --> PHP
    RA --> GO
    PHP --> NODE
    PHP --> REL
    GO --> NODE
    GO --> REL
    NODE --> AR
    REL --> AR
    CGA --> AR
    
    style AS fill:#e3f2fd
    style RA fill:#e3f2fd
    style CGA fill:#e3f2fd
```

## Component ID Generation

Both analyzers generate unique component IDs following a consistent pattern:

### PHP Component IDs
```
{namespace}.{class_name}.{method_name}
{module_path}.{function_name}
{namespace}.{class_name}
```

**Example:**
- File: `src/App/User.php`
- Namespace: `App`
- Class: `User`
- Method: `getName`
- **Component ID:** `App.User.getName`

### Go Component IDs
```
{module_path}.{struct_name}.{method_name}
{module_path}.{function_name}
{module_path}.{type_name}
```

**Example:**
- File: `pkg/user/user.go`
- Struct: `User`
- Method: `GetName`
- **Component ID:** `pkg.user.User.GetName`

## Configuration & Behavior

### PHP Analyzer Settings

| Setting | Value | Description |
|---------|-------|-------------|
| `MAX_RECURSION_DEPTH` | 100 | Maximum AST traversal depth to prevent stack overflow |
| `TEMPLATE_PATTERNS` | `.blade.php`, `.phtml`, `.twig.php` | File extensions to skip |
| `TEMPLATE_DIRECTORIES` | `views`, `templates`, `resources/views` | Directory patterns to skip |
| `PHP_PRIMITIVES` | 30+ types | Built-in types excluded from dependency tracking |

### Go Analyzer Settings

| Setting | Value | Description |
|---------|-------|-------------|
| `tree-sitter-go` version | ≥0.23.0 | Required minimum version |
| Duplicate prevention | `seen_relationships` set | Prevents duplicate call relationships |

## Usage Examples

### PHP Analysis

```python
from codewiki.src.be.dependency_analyzer.analyzers.php import analyze_php_file

nodes, relationships = analyze_php_file(
    file_path="/path/to/User.php",
    content="<?php namespace App; class User { ... }",
    repo_path="/path/to/repo"
)

# nodes: List[Node] containing class, method definitions
# relationships: List[CallRelationship] containing extends, implements, use, etc.
```

### Go Analysis

```python
from codewiki.src.be.dependency_analyzer.analyzers.go import analyze_go_file

nodes, relationships = analyze_go_file(
    file_path="/path/to/user.go",
    content="package user; type User struct { ... }",
    repo_path="/path/to/repo"
)

# nodes: List[Node] containing function, method, struct, interface definitions
# relationships: List[CallRelationship] containing function/method calls
```

## Error Handling

### PHP Analyzer
- **RecursionError**: Logged as warning when max depth exceeded
- **ParseError**: Logged with file path and error message
- **Template Files**: Silently skipped with debug log

### Go Analyzer
- **Language Version Mismatch**: Detailed error with installation instructions
- **Parser Initialization Failure**: Logged with traceback, analysis skipped
- **General Errors**: Logged with full exception info

## Related Modules

| Module | Relationship | Documentation |
|--------|--------------|---------------|
| [dependency_analyzer](dependency_analyzer.md) | Parent module containing analyzer framework | See dependency_analyzer.md |
| [analyzers](dependency_analyzer.md#analyzers) | Sibling analyzers for other languages | See dependency_analyzer.md |
| [models](dependency_analyzer.md#models) | Shared Node and CallRelationship types | See dependency_analyzer.md |
| [analysis](dependency_analyzer.md#analysis) | AnalysisService that orchestrates analyzers | See dependency_analyzer.md |
| [documentation_generator](documentation_generator.md) | Consumes analysis results for documentation | See documentation_generator.md |

## Language Support Comparison

| Feature | PHP Analyzer | Go Analyzer |
|---------|--------------|-------------|
| Classes/Structs | ✅ | ✅ (struct) |
| Interfaces | ✅ | ✅ |
| Traits | ✅ | ❌ |
| Enums | ✅ | ❌ (Go 1.18+ not fully supported) |
| Functions | ✅ | ✅ |
| Methods | ✅ | ✅ |
| Namespace Resolution | ✅ (full) | ❌ (package-based) |
| Inheritance Tracking | ✅ (extends) | ❌ (no inheritance) |
| Interface Implementation | ✅ (implements) | ✅ (implicit) |
| Call Relationships | ✅ (static, new) | ✅ (function calls) |
| Template Detection | ✅ | ❌ |
| Docstring Extraction | ✅ (PHPDoc) | ❌ |

## Performance Considerations

1. **Recursion Limits**: Both analyzers implement `MAX_RECURSION_DEPTH` checks to prevent stack overflow on deeply nested code
2. **Duplicate Prevention**: Go analyzer uses a `seen_relationships` set to avoid processing duplicate call relationships
3. **Template Skipping**: PHP analyzer skips template files early to avoid unnecessary parsing
4. **Parser Initialization**: Go analyzer validates parser initialization before analysis to fail fast on version mismatches

## Future Enhancements

- [ ] Go 1.18+ generics support
- [ ] PHP attribute/annotation extraction
- [ ] Go module dependency resolution
- [ ] PHP composer.json dependency integration
- [ ] Enhanced docstring parsing for both languages
- [ ] Cross-file relationship resolution
