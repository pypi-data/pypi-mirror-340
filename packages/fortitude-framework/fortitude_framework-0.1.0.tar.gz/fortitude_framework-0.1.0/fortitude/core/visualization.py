from typing import List, Optional, Any, Dict, Union
from pydantic import BaseModel
from IPython.display import display, HTML
import uuid
import html
import json

_rendered_css = False  # global state

class PrettyRenderableModel(BaseModel):
    def _repr_html_(self):
        global _rendered_css
        if not _rendered_css:
            display(HTML("""
            <style>
                /* Modern Card Design */
                .pretty-card {
                    border-radius: 12px;
                    background: rgba(255, 255, 255, 0.98);
                    padding: 1.5em;
                    margin: 1.2em 0;
                    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'SF Pro', Roboto, sans-serif;
                    border: 1px solid rgba(150,150,150,0.15);
                    transition: all 0.3s ease;
                    position: relative;
                    overflow: hidden;
                }
                
                .pretty-card:hover {
                    box-shadow: 0 12px 28px rgba(0,0,0,0.15);
                    transform: translateY(-2px);
                }
                
                /* Card Header */
                .pretty-header {
                    font-size: 1.4em;
                    font-weight: 600;
                    color: #1a3c6e;
                    margin-bottom: 0.8em;
                    padding-bottom: 0.6em;
                    border-bottom: 2px solid rgba(0,51,102,0.1);
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                }
                
                .pretty-header-badge {
                    font-size: 0.65em;
                    background: #e8f0fe;
                    color: #1967d2;
                    padding: 0.3em 0.6em;
                    border-radius: 20px;
                    font-weight: 500;
                }
                
                /* Key-Value Pairs */
                .pretty-kv {
                    margin: 0.5em 0;
                    line-height: 1.5;
                    display: flex;
                    flex-wrap: wrap;
                }
                
                .pretty-key {
                    font-weight: 500;
                    color: #333;
                    margin-right: 0.5em;
                    min-width: 120px;
                }
                
                .pretty-value {
                    flex: 1;
                    color: #444;
                }
                
                /* Different Value Types */
                .pretty-string {
                    color: #0971A6;
                }
                
                .pretty-number {
                    color: #1967d2;
                    font-family: 'SF Mono', 'Menlo', 'Consolas', monospace;
                }
                
                .pretty-boolean-true {
                    color: #188038;
                    font-weight: 500;
                }
                
                .pretty-boolean-false {
                    color: #d93025;
                    font-weight: 500;
                }
                
                .pretty-null {
                    color: #888;
                    font-style: italic;
                }
                
                /* Nested Elements */
                .pretty-nested {
                    margin-left: 1.5em;
                    border-left: 3px solid #e8eaed;
                    padding-left: 1em;
                    margin-top: 0.5em;
                }
                
                /* Lists */
                ul.pretty-list {
                    padding-left: 1.2em;
                    margin: 0.3em 0;
                    list-style-type: none;
                }
                
                ul.pretty-list li {
                    position: relative;
                    margin: 0.3em 0;
                }
                
                ul.pretty-list li:before {
                    content: "•";
                    color: #5f6368;
                    position: absolute;
                    left: -1em;
                    top: 0.1em;
                }
                
                /* Collapsible sections */
                .pretty-collapsible {
                    cursor: pointer;
                }
                
                .pretty-collapsible:after {
                    content: "▼";
                    font-size: 0.8em;
                    margin-left: 0.5em;
                    color: #5f6368;
                }
                
                .pretty-collapsed:after {
                    content: "►";
                }
                
                .pretty-collapsed + .pretty-content {
                    display: none;
                }
                
                /* Copy button */
                .pretty-copy-btn {
                    position: absolute;
                    top: 1em;
                    right: 1em;
                    padding: 0.3em 0.6em;
                    background: rgba(0,0,0,0.05);
                    border: none;
                    border-radius: 4px;
                    font-size: 0.8em;
                    color: #5f6368;
                    cursor: pointer;
                    transition: all 0.2s;
                }
                
                .pretty-copy-btn:hover {
                    background: rgba(0,0,0,0.1);
                }
                
                /* Type indicators */
                .pretty-type-indicator {
                    font-size: 0.7em;
                    color: #777;
                    margin-left: 0.5em;
                    vertical-align: super;
                }
                
                /* Special field styling */
                .pretty-field-important {
                    background: #fef7e0;
                    border-radius: 4px;
                    padding: 0.2em 0.5em;
                }
                
                /* Confidence meter */
                .confidence-meter {
                    height: 6px;
                    width: 100px;
                    background: #f1f3f4;
                    border-radius: 3px;
                    display: inline-block;
                    margin-left: 8px;
                    vertical-align: middle;
                    overflow: hidden;
                }
                
                .confidence-fill {
                    height: 100%;
                    background: linear-gradient(90deg, #34a853 0%, #4285f4 100%);
                }
            </style>
            <script>
                // Add collapsible functionality
                function toggleCollapse(id) {
                    const header = document.getElementById(id);
                    header.classList.toggle('pretty-collapsed');
                }
                
                // Add copy functionality
                function copyToClipboard(id) {
                    const card = document.getElementById(id);
                    const textToCopy = JSON.stringify(JSON.parse(card.getAttribute('data-json')), null, 2);
                    
                    navigator.clipboard.writeText(textToCopy).then(() => {
                        const btn = card.querySelector('.pretty-copy-btn');
                        const originalText = btn.textContent;
                        btn.textContent = 'Copied!';
                        setTimeout(() => {
                            btn.textContent = originalText;
                        }, 2000);
                    });
                }
            </script>
            """))
            _rendered_css = True

        title = self.__class__.__name__
        html_id = f"pretty_{uuid.uuid4().hex}"
        json_data = json.dumps(self.model_dump())
        
        return f"""
        <div id='{html_id}' class='pretty-card' data-json='{html.escape(json_data)}'>
            <button class='pretty-copy-btn' onclick="copyToClipboard('{html_id}')">Copy JSON</button>
            {self._render_fields(title, html_id)}
        </div>
        """

    def _render_fields(self, title=None, parent_id=None):
        data = self.model_dump()
        html_parts = []
        
        if title:
            type_count = len(data.keys())
            html_parts.append(f"""
            <div class='pretty-header'>
                <span>🔹 {html.escape(title)}</span>
                <span class='pretty-header-badge'>{type_count} fields</span>
            </div>
            """)

        for k, v in data.items():
            # Highlight special fields
            key_class = ""
            if k in ["request_id", "provenance_id", "goal", "priority"]:
                key_class = "pretty-field-important"
                
            field_id = f"{parent_id}_{k}" if parent_id else f"field_{uuid.uuid4().hex}"
            
            html_parts.append(f"""
            <div class='pretty-kv'>
                <span class='pretty-key {key_class}'>{html.escape(str(k))}</span>
                <span class='pretty-value'>{self._render_value(v, field_id)}</span>
            </div>
            """)

        return "\n".join(html_parts)

    def _render_value(self, val, field_id=None):
        if val is None:
            return "<span class='pretty-null'>null</span>"
            
        if isinstance(val, bool):
            if val:
                return "<span class='pretty-boolean-true'>true</span>"
            else:
                return "<span class='pretty-boolean-false'>false</span>"
                
        if isinstance(val, (int, float)):
            # Special handling for confidence values
            if field_id and "confidence" in field_id and 0 <= val <= 1:
                percentage = int(val * 100)
                return f"""
                <span class='pretty-number'>{val}</span>
                <span class='confidence-meter'>
                    <span class='confidence-fill' style='width: {percentage}%'></span>
                </span>
                <span>({percentage}%)</span>
                """
            return f"<span class='pretty-number'>{val}</span>"
            
        if isinstance(val, str):
            if len(val) > 100:  # Collapsible for long strings
                short_val = html.escape(val[:100]) + "..."
                full_val = html.escape(val)
                collapse_id = f"collapse_{uuid.uuid4().hex}"
                return f"""
                <span class='pretty-collapsible pretty-collapsed pretty-string' id='{collapse_id}' 
                      onclick="toggleCollapse('{collapse_id}')">{short_val}</span>
                <div class='pretty-content pretty-string'>{full_val}</div>
                """
            return f"<span class='pretty-string'>{html.escape(val)}</span>"
            
        if isinstance(val, list):
            if not val:
                return "<i class='pretty-null'>[]</i>"
                
            collapse_id = f"collapse_{uuid.uuid4().hex}"
            item_count = len(val)
            
            # Make lists collapsible if they have many items
            if item_count > 3:
                return f"""
                <div>
                    <span class='pretty-collapsible' id='{collapse_id}' 
                          onclick="toggleCollapse('{collapse_id}')">
                        List ({item_count} items)
                    </span>
                    <div class='pretty-content'>
                        <ul class='pretty-list'>
                            {"".join(f"<li>{self._render_value(v)}</li>" for v in val)}
                        </ul>
                    </div>
                </div>
                """
            
            return "<ul class='pretty-list'>" + "".join(f"<li>{self._render_value(v)}</li>" for v in val) + "</ul>"
            
        elif isinstance(val, dict):
            collapse_id = f"collapse_{uuid.uuid4().hex}"
            key_count = len(val.keys())
            
            if key_count > 5:  # Collapsible for large dicts
                return f"""
                <div>
                    <span class='pretty-collapsible' id='{collapse_id}' 
                          onclick="toggleCollapse('{collapse_id}')">
                        Object ({key_count} properties)
                    </span>
                    <div class='pretty-content pretty-nested'>
                        {"".join(
                            f"<div><span class='pretty-key'>{html.escape(str(k))}</span>: {self._render_value(v)}</div>"
                            for k, v in val.items()
                        )}
                    </div>
                </div>
                """
            
            return "<div class='pretty-nested'>" + "".join(
                f"<div><span class='pretty-key'>{html.escape(str(k))}</span>: {self._render_value(v)}</div>"
                for k, v in val.items()
            ) + "</div>"
            
        elif isinstance(val, PrettyRenderableModel):
            collapse_id = f"collapse_{uuid.uuid4().hex}"
            return f"""
            <div>
                <span class='pretty-collapsible' id='{collapse_id}' 
                      onclick="toggleCollapse('{collapse_id}')">
                    {val.__class__.__name__}
                </span>
                <div class='pretty-content pretty-nested'>
                    {val._render_fields()}
                </div>
            </div>
            """
        else:
            return html.escape(str(val))


class ThoughtSegment(PrettyRenderableModel):
    content: str
    inference_type: str
    confidence: float

class ChainOfThought(PrettyRenderableModel):
    thoughts: List[ThoughtSegment]
    goal: str
    provenance_id: str

class Step(PrettyRenderableModel):
    instructions: str
    dependencies: List[int]
    tool_hint: str
    estimated_cost: float

class Plan(PrettyRenderableModel):
    chain_of_thought: ChainOfThought
    steps: List[Step]
    priority: int
    origin_agent: str

class DecomposedUserRequest(PrettyRenderableModel):
    initial_prompt: str
    plan: Plan
    tags: List[str]
    request_id: str