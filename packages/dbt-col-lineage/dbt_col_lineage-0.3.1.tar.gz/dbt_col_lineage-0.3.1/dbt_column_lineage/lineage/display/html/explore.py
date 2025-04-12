import typing
from typing import Dict, Union, Set, List, Any, Optional, Mapping
from pydantic import BaseModel, Field
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
import uvicorn
import logging
from dbt_column_lineage.models.schema import Column, ColumnLineage

logger = logging.getLogger(__name__)


class ColumnInfo(BaseModel):
    name: str
    model: str
    type: Optional[str] = None
    description: Optional[str] = None


class GraphNode(BaseModel):
    id: str
    label: str
    type: str
    model: str
    data_type: Optional[str] = None
    is_main: bool = False
    resource_type: Optional[str] = None
    is_key: bool = False


class GraphEdge(BaseModel):
    source: str
    target: str
    type: str = "lineage"


class GraphData(BaseModel):
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[Dict[str, Any]] = Field(default_factory=list)
    main_node: Optional[str] = None
    column_info: Optional[ColumnInfo] = None


class LineageExplorer:
    """Interactive server for exploring column lineage."""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8000):
        self.app = FastAPI()
        self.host = host
        self.port = port
        self.data = GraphData()
        self.lineage_service = None
        
        self._setup_templates_and_routes()
    
    def _setup_templates_and_routes(self) -> None:
        """Setup templates, static files, and routes."""
        self.templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
        self.app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
        
        @self.app.get("/", response_class=HTMLResponse)
        async def home(request: Request) -> Any:
            return self.templates.TemplateResponse(
                "graph.html",
                {"request": request, "data": self.data.model_dump(), "explore_mode": True}
            )

        @self.app.get("/api/graph")
        async def get_graph_data() -> Dict[str, Any]:
            return self.data.model_dump()
            
        @self.app.get("/api/models")
        async def get_models() -> List[Dict[str, Any]]:
            if not self.lineage_service:
                return []
            
            models = []
            for model_name, model in self.lineage_service.registry.get_models().items():
                columns = [
                    {"name": col_name, "type": col.data_type}
                    for col_name, col in model.columns.items()
                ]
                
                models.append({
                    "name": model_name,
                    "columns": columns,
                    "resource_type": model.resource_type
                })
            return models
            
        @self.app.get("/api/lineage/{model}/{column}")
        async def get_lineage(model: str, column: str) -> Dict[str, Any]:
            if not self.lineage_service:
                return {"error": "Lineage service not initialized"}
                
            try:
                self.data = GraphData()
                model_obj = self.lineage_service.registry.get_model(model)
                column_obj = model_obj.columns.get(column)
                
                if not column_obj:
                    return {"error": f"Column {column} not found in model {model}"}
                
                self._set_column_info(column_obj)
                self.data.main_node = f"col_{model}_{column}"
                self._process_lineage_tree(model, column)
            
                return self.data.model_dump()
            except Exception as e:
                import traceback
                logger.error(f"Error getting lineage: {e}")
                logger.debug(traceback.format_exc())
                return {"error": str(e)}
        
    def _process_lineage_tree(self, start_model: str, start_column: str) -> None:
        """Process complete lineage tree from starting point."""
        processed = set()
        to_process = [(start_model, start_column)]
        
        while to_process:
            current_model, current_col = to_process.pop(0)
            if (current_model, current_col) in processed:
                continue
                
            processed.add((current_model, current_col))
            
            try:
                upstream_refs = self.lineage_service._get_upstream_lineage(current_model, current_col)
                downstream_refs = self.lineage_service._get_downstream_lineage(current_model, current_col)
                self._enrich_nodes_with_metadata([upstream_refs, downstream_refs])
                self._add_processed_data(upstream_refs, "upstream")
                self._add_processed_data(downstream_refs, "downstream")
                self._queue_additional_nodes(upstream_refs, downstream_refs, processed, to_process)
                
            except Exception as e:
                logger.error(f"Error processing lineage for {current_model}.{current_col}: {e}")
    
    def _enrich_nodes_with_metadata(self, refs_list: List) -> None:
        """Enrich nodes with metadata like data types and resource types."""
        for refs in refs_list:
            for model_name, columns in refs.items():
                if isinstance(columns, dict):
                    try:
                        model_obj = self.lineage_service.registry.get_model(model_name)
                        if not model_obj:
                            continue
                            
                        resource_type = getattr(model_obj, 'resource_type', None)
                        
                        for col_name in columns.keys():
                            col_obj = model_obj.columns.get(col_name)
                            if not col_obj:
                                continue
                                
                            node_id = f"col_{model_name}_{col_name}"
                            
                            found = False
                            for node in self.data.nodes:
                                if node['id'] == node_id:
                                    node['data_type'] = col_obj.data_type
                                    node['resource_type'] = resource_type
                                    found = True
                                    break
                            
                            if not found:
                                self._add_node(
                                    id=node_id,
                                    label=col_name,
                                    model=model_name,
                                    data_type=col_obj.data_type,
                                    resource_type=resource_type
                                )
                    except Exception as e:
                        logger.error(f"Error enriching node metadata for {model_name}: {e}")
    
    def _queue_additional_nodes(self, upstream_refs, downstream_refs, processed, to_process):
        """Queue additional nodes for processing."""
        for refs in [upstream_refs, downstream_refs]:
            for model_name, columns in refs.items():
                if isinstance(columns, dict):
                    for col_name in columns.keys():
                        if (model_name, col_name) not in processed and (model_name, col_name) not in to_process:
                            to_process.append((model_name, col_name))
    
    def _add_processed_data(self, refs, direction):
        """Process refs and add to graph."""
        processed = self._process_refs(refs, direction)
        
        for node in processed["nodes"]:
            if not any(n["id"] == node["id"] for n in self.data.nodes):
                self.data.nodes.append(node)
                
        for edge in processed["edges"]:
            if not any(e["source"] == edge["source"] and e["target"] == edge["target"] for e in self.data.edges):
                self.data.edges.append(edge)

    def set_lineage_service(self, lineage_service) -> None:
        """Set the lineage service for the explore server."""
        self.lineage_service = lineage_service
        
    def _set_column_info(self, column: Column) -> None:
        """Set the main column info for display."""
        self.data.column_info = ColumnInfo(
            name=column.name,
            model=column.model_name,
            type=column.data_type,
            description=column.description
        )
        
        resource_type = self._get_model_resource_type(column.model_name)
        
        self._add_node(
            id=f"col_{column.model_name}_{column.name}",
            label=column.name,
            model=column.model_name,
            data_type=column.data_type,
            is_main=True,
            resource_type=resource_type
        )
    
    def _get_model_resource_type(self, model_name: str) -> Optional[str]:
        """Get resource type for a model."""
        try:
            if self.lineage_service:
                model_obj = self.lineage_service.registry.get_model(model_name)
                if model_obj:
                    return getattr(model_obj, 'resource_type', None)
        except Exception:
            pass
        return None

    def start(self) -> None:
        """Start the server to display the graph."""
        uvicorn.run(self.app, host=self.host, port=self.port)

    def _add_node(self, id: str, label: str, model: str, data_type: Optional[str] = None, 
                 is_main: bool = False, resource_type: Optional[str] = None, is_key: bool = False) -> Dict[str, Any]:
        """Helper to create and add a node."""
        node = GraphNode(
            id=id,
            label=label,
            type="column",
            model=model,
            data_type=data_type,
            is_main=is_main,
            resource_type=resource_type,
            is_key=is_key
        ).model_dump()
        
        self.data.nodes.append(node)
        return node

    def _add_edge(self, source_id: str, target_id: str) -> Dict[str, str]:
        """Helper to create and add an edge."""
        edge = GraphEdge(
            source=source_id,
            target=target_id,
            type="lineage"
        ).model_dump()
        
        self.data.edges.append(edge)
        return edge
    
    def _process_refs(self, refs: Mapping[str, Union[Dict[str, ColumnLineage], Set[str]]], 
                     direction: str) -> Dict[str, List[Dict[str, Any]]]:
        """Process reference data into nodes and edges."""
        nodes: List[Dict[str, Any]] = []
        edges: List[Dict[str, Any]] = []
        node_ids = set()

        for model_name, columns in refs.items():
            if not isinstance(columns, dict):
                continue
            
            model_resource_type = self._get_model_resource_type(model_name)
            
            for col_name, lineage in columns.items():
                col_node_id = f"col_{model_name}_{col_name}"
                if col_node_id not in node_ids:
                    col_node = GraphNode(
                        id=col_node_id,
                        label=col_name,
                        type="column",
                        model=model_name,
                        data_type=getattr(lineage, 'data_type', None),
                        resource_type=model_resource_type
                    ).model_dump()
                    
                    nodes.append(col_node)
                    node_ids.add(col_node_id)

                if direction == "upstream" and hasattr(lineage, 'source_columns'):
                    self._process_source_columns(lineage.source_columns, col_node_id, refs, nodes, edges, node_ids)
                elif direction == "downstream" and hasattr(lineage, 'source_columns'):
                    self._add_downstream_edges(lineage.source_columns, col_node_id, edges)

        return {"nodes": nodes, "edges": edges}
    
    def _add_downstream_edges(self, source_columns, target_node_id, edges):
        """Add edges for downstream lineage."""
        for source in source_columns:
            if '.' in source:
                src_model, src_col = source.split('.')
                src_node_id = f"col_{src_model}_{src_col}"
                edge = GraphEdge(
                    source=src_node_id,
                    target=target_node_id
                ).model_dump()
                edges.append(edge)
    
    def _process_source_columns(self, source_columns: Union[List[str], Set[str]], target_node_id: str, 
                              refs: Mapping[str, Union[Dict[str, ColumnLineage], Set[str]]], 
                              nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]], 
                              node_ids: Set[str]) -> None:
        """Process source columns and create nodes/edges."""
        for source in source_columns:
            if '.' in source:
                src_model, src_col = source.split('.')
                src_node_id = f"col_{src_model}_{src_col}"
                
                if src_node_id not in node_ids:
                    self._add_source_node(src_model, src_col, refs, nodes, node_ids)
                
                edge = GraphEdge(
                    source=src_node_id,
                    target=target_node_id
                ).model_dump()
                edges.append(edge)
    
    def _add_source_node(self, src_model, src_col, refs, nodes, node_ids):
        """Add a source node to the graph."""
        src_node_id = f"col_{src_model}_{src_col}"
        src_data_type = None
        model_resource_type = self._get_model_resource_type(src_model)
        
        if src_model in refs and isinstance(refs[src_model], dict):
            src_model_data = refs[src_model]
            if isinstance(src_model_data, dict) and src_col in src_model_data:
                src_lineage = src_model_data[src_col]
                src_data_type = getattr(src_lineage, 'data_type', None)
        
        src_node = GraphNode(
            id=src_node_id,
            label=src_col,
            type="column",
            model=src_model,
            data_type=src_data_type,
            resource_type=model_resource_type
        ).model_dump()
        
        nodes.append(src_node)
        node_ids.add(src_node_id) 