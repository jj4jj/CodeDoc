import logging
import os
import traceback
from typing import List, Tuple, Optional
from pathlib import Path
from importlib.metadata import PackageNotFoundError, version

from tree_sitter import Parser, Language
import tree_sitter_go

from codewiki.src.be.dependency_analyzer.models.core import Node, CallRelationship

logger = logging.getLogger(__name__)


def _pkg_version(name: str) -> str:
    try:
        return version(name)
    except PackageNotFoundError:
        return "not-installed"


class TreeSitterGoAnalyzer:
    def __init__(self, file_path: str, content: str, repo_path: str = None):
        self.file_path = Path(file_path)
        self.content = content
        self.repo_path = repo_path or ""
        self.nodes: List[Node] = []
        self.call_relationships: List[CallRelationship] = []
        
        self.top_level_nodes = {}
        self.seen_relationships = set()

        try:
            language_capsule = tree_sitter_go.language()
            self.go_language = Language(language_capsule)
            self.parser = Parser(self.go_language)
        except ValueError as e:
            if "Incompatible Language version" in str(e):
                logger.error(f"Tree-sitter Go language version incompatible: {e}")
                logger.error(
                    "Detected versions: tree-sitter=%s, tree-sitter-go=%s",
                    _pkg_version("tree-sitter"),
                    _pkg_version("tree-sitter-go"),
                )
                logger.error(
                    "Use compatible versions (for tree-sitter 0.23.x, pin tree-sitter-go to 0.23.4)."
                )
                logger.error("Run: pip install --force-reinstall 'tree-sitter==0.23.2' 'tree-sitter-go==0.23.4'")
            else:
                logger.error(f"Failed to initialize Go parser: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            self.parser = None
            self.go_language = None
        except Exception as e:
            logger.error(f"Failed to initialize Go parser: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            self.parser = None
            self.go_language = None

    def _get_relative_path(self) -> str:
        if self.repo_path:
            try:
                return os.path.relpath(str(self.file_path), self.repo_path)
            except ValueError:
                pass
        return str(self.file_path)

    def _get_module_path(self) -> str:
        rel_path = self._get_relative_path()
        if rel_path.endswith('.go'):
            rel_path = rel_path[:-3]
        return rel_path.replace('/', '.').replace('\\', '.')

    def _get_component_id(self, name: str, struct_name: str = None) -> str:
        module_path = self._get_module_path()
        if struct_name:
            return f"{module_path}.{struct_name}.{name}"
        return f"{module_path}.{name}"

    def analyze(self) -> None:
        if self.parser is None:
            logger.warning(f"Skipping {self.file_path} - parser initialization failed")
            return

        try:
            tree = self.parser.parse(bytes(self.content, "utf8"))
            root_node = tree.root_node

            self._traverse_for_components(root_node)
            self.nodes.sort(key=lambda n: n.start_line)

            self._extract_call_relationships(root_node)

            logger.debug(
                f"Go analysis complete: {len(self.nodes)} nodes, {len(self.call_relationships)} relationships"
            )

        except Exception as e:
            logger.error(f"Error analyzing Go file {self.file_path}: {e}", exc_info=True)

    def _get_node_text(self, node) -> str:
        start_byte = node.start_byte
        end_byte = node.end_byte
        return self.content.encode("utf8")[start_byte:end_byte].decode("utf8")

    def _find_child_by_type(self, node, node_type: str):
        for child in node.children:
            if child.type == node_type:
                return child
        return None

    def _traverse_for_components(self, node):
        if node.type == "function_declaration":
            func = self._extract_function_declaration(node)
            if func:
                self.nodes.append(func)
                self.top_level_nodes[func.name] = func
        elif node.type == "method_declaration":
             func = self._extract_method_declaration(node)
             if func:
                self.nodes.append(func)
                self.top_level_nodes[func.name] = func
        elif node.type == "type_declaration":
            # Type declaration might contain struct or interface
            self._extract_type_declarations(node)

        for child in node.children:
            self._traverse_for_components(child)

    def _extract_type_declarations(self, node):
        for child in node.children:
            if child.type == "type_spec":
                name_node = self._find_child_by_type(child, "type_identifier")
                if not name_node:
                    continue
                type_name = self._get_node_text(name_node)
                
                struct_type = self._find_child_by_type(child, "struct_type")
                interface_type = self._find_child_by_type(child, "interface_type")
                
                node_type = None
                display_name = None
                
                if struct_type:
                    node_type = "struct"
                    display_name = f"struct {type_name}"
                elif interface_type:
                    node_type = "interface"
                    display_name = f"interface {type_name}"
                
                if node_type:
                    line_start = child.start_point[0] + 1
                    line_end = child.end_point[0] + 1
                    code_snippet = self._get_node_text(child)
                    component_id = self._get_component_id(type_name)
                    relative_path = self._get_relative_path()

                    type_node = Node(
                        id=component_id,
                        name=type_name,
                        component_type=node_type,
                        file_path=str(self.file_path),
                        relative_path=relative_path,
                        source_code=code_snippet,
                        start_line=line_start,
                        end_line=line_end,
                        has_docstring=False,
                        docstring="",
                        parameters=None,
                        node_type=node_type,
                        base_classes=None,
                        class_name=None,
                        display_name=display_name,
                        component_id=component_id
                    )
                    self.nodes.append(type_node)
                    self.top_level_nodes[type_name] = type_node

    def _extract_function_declaration(self, node) -> Optional[Node]:
        name_node = self._find_child_by_type(node, "identifier")
        if not name_node:
            return None

        func_name = self._get_node_text(name_node)
        line_start = node.start_point[0] + 1
        line_end = node.end_point[0] + 1
        code_snippet = self._get_node_text(node)
        
        parameters = self._extract_parameters(self._find_child_by_type(node, "parameter_list"))

        component_id = self._get_component_id(func_name)
        relative_path = self._get_relative_path()

        return Node(
            id=component_id,
            name=func_name,
            component_type="function",
            file_path=str(self.file_path),
            relative_path=relative_path,
            source_code=code_snippet,
            start_line=line_start,
            end_line=line_end,
            has_docstring=False,
            docstring="",
            parameters=parameters,
            node_type="function",
            base_classes=None,
            class_name=None,
            display_name=f"func {func_name}",
            component_id=component_id
        )

    def _extract_method_declaration(self, node) -> Optional[Node]:
        name_node = self._find_child_by_type(node, "field_identifier")
        if not name_node:
            return None

        func_name = self._get_node_text(name_node)
        
        # extract receiver struct name
        receiver_node = self._find_child_by_type(node, "parameter_list")
        struct_name = None
        if receiver_node:
            for param in receiver_node.children:
                if param.type == "parameter_declaration":
                    type_id = self._find_child_by_type(param, "type_identifier")
                    if type_id:
                        struct_name = self._get_node_text(type_id)
                    # Handle pointer receivers usually wrapped in pointer_type
                    ptr_node = self._find_child_by_type(param, "pointer_type")
                    if ptr_node:
                        type_id = self._find_child_by_type(ptr_node, "type_identifier")
                        if type_id:
                            struct_name = self._get_node_text(type_id)
                            
        line_start = node.start_point[0] + 1
        line_end = node.end_point[0] + 1
        code_snippet = self._get_node_text(node)
        
        params_node = None
        for child in node.children:
            if child.type == "parameter_list" and child != receiver_node:
                params_node = child
                break
                
        parameters = self._extract_parameters(params_node) if params_node else []

        component_id = self._get_component_id(func_name, struct_name)
        relative_path = self._get_relative_path()

        return Node(
            id=component_id,
            name=func_name,
            component_type="method",
            file_path=str(self.file_path),
            relative_path=relative_path,
            source_code=code_snippet,
            start_line=line_start,
            end_line=line_end,
            has_docstring=False,
            docstring="",
            parameters=parameters,
            node_type="method",
            base_classes=None,
            class_name=struct_name,
            display_name=f"func ({struct_name}) {func_name}",
            component_id=component_id
        )

    def _extract_parameters(self, params_node) -> List[str]:
        parameters = []
        if params_node:
            for child in params_node.children:
                if child.type == "parameter_declaration":
                    ident = self._find_child_by_type(child, "identifier")
                    if ident:
                        parameters.append(self._get_node_text(ident))
        return parameters

    def _extract_call_relationships(self, node):
        current_top_level = None
        self._traverse_for_calls(node, current_top_level, None)

    def _traverse_for_calls(self, node, current_top_level, current_struct=None):
        if node.type == "function_declaration":
            name_node = self._find_child_by_type(node, "identifier")
            if name_node:
                current_top_level = self._get_node_text(name_node)
                current_struct = None
        elif node.type == "method_declaration":
            name_node = self._find_child_by_type(node, "field_identifier")
            if name_node:
                current_top_level = self._get_node_text(name_node)
                
            receiver = self._find_child_by_type(node, "parameter_list")
            if receiver:
                for param in receiver.children:
                    if param.type == "parameter_declaration":
                        type_id = self._find_child_by_type(param, "type_identifier")
                        if type_id:
                            current_struct = self._get_node_text(type_id)
                        ptr_node = self._find_child_by_type(param, "pointer_type")
                        if ptr_node:
                            type_id = self._find_child_by_type(ptr_node, "type_identifier")
                            if type_id:
                                current_struct = self._get_node_text(type_id)

        if node.type == "call_expression" and current_top_level:
            callee_name = self._extract_callee_name(node)
            if callee_name:
                caller_id = self._get_component_id(current_top_level, current_struct)
                callee_id = f"{self._get_module_path()}.{callee_name}"
                is_resolved = False

                for func_id, func_node in self.top_level_nodes.items():
                    if func_node.name == callee_name:
                        is_resolved = True
                        callee_id = func_node.component_id
                        break
                        
                rel_key = (caller_id, callee_id, node.start_point[0] + 1)
                if rel_key not in self.seen_relationships:
                    relationship = CallRelationship(
                        caller=caller_id,
                        callee=callee_id,
                        call_line=node.start_point[0] + 1,
                        is_resolved=is_resolved
                    )
                    self.seen_relationships.add(rel_key)
                    self.call_relationships.append(relationship)

        for child in node.children:
            self._traverse_for_calls(child, current_top_level, current_struct)

    def _extract_callee_name(self, call_node) -> Optional[str]:
        if not call_node.children:
            return None
        callee_node = call_node.children[0]

        if callee_node.type == "identifier":
            return self._get_node_text(callee_node)
        elif callee_node.type == "selector_expression":
            field_ident = self._find_child_by_type(callee_node, "field_identifier")
            if field_ident:
                return self._get_node_text(field_ident)
        return None


def analyze_go_file(
    file_path: str, content: str, repo_path: str = None
) -> Tuple[List[Node], List[CallRelationship]]:
    """Analyze a Go file using tree-sitter."""
    try:
        logger.debug(f"Tree-sitter Go analysis for {file_path}")
        analyzer = TreeSitterGoAnalyzer(file_path, content, repo_path)
        analyzer.analyze()
        return analyzer.nodes, analyzer.call_relationships
    except Exception as e:
        logger.error(f"Error in tree-sitter Go analysis for {file_path}: {e}", exc_info=True)
        return [], []
