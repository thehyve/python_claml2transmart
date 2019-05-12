from typing import Dict, Set, Optional

from transmart_loader.transmart import TreeNode, ConceptNode, Concept, ValueType


class OntologyMapper:
    """
    Map ontology nodes to TranSMART
    """
    def __init__(self, system: str):
        self.system = system
        self.root_nodes: Set[TreeNode] = set()
        self.nodes: Dict[str, TreeNode] = {}
        self.concepts: Set[Concept] = set()

    def map_code(self, parent_code: Optional[str], code: str, label: str) -> None:
        concept = Concept(code, label, self.system + '/' + code, ValueType.Categorical)
        self.concepts.add(concept)
        node = ConceptNode(concept)
        if parent_code is not None and parent_code in self.nodes:
            parent_node = self.nodes[parent_code]
            parent_node.add_child(node)
        else:
            self.root_nodes.add(node)
        self.nodes[code] = node
