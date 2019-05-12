from xml.dom import Node

from python_claml.claml_types import Class

from .ontology_mapper import OntologyMapper
from transmart_loader.copy_writer import TransmartCopyWriter


def normalise_code(code: str) -> str:
    return code.replace('!', '').replace('*', '')


def to_string(nodes):
    """
    Serialise a forest of DOM nodes to text,
    using the data fields of text nodes.
    :param nodes: the forest of DOM nodes
    :return: a concatenation of string representations.
    """
    result = []
    for node in nodes:
        if node.nodeType == Node.TEXT_NODE:
            result.append(node.data)
        else:
            result.append(to_string(node.childNodes))
    return ''.join(result)


class OntologyWriter:

    def process_class(self, cls: Class) -> None:
        class_label = None
        for rubric in cls.Rubric:
            if rubric.kind == 'preferred':
                for label in rubric.Label:
                    class_label = to_string(label.toDOM().childNodes)
        class_label = cls.code + '. ' + class_label
        if len(cls.SuperClass) > 0:
            for superClass in cls.SuperClass:
                self.mapper.map_code(superClass.code, cls.code, class_label)
        else:
            self.mapper.map_code(None, cls.code, class_label)

    def write(self, writer: TransmartCopyWriter):
        for concept in self.mapper.concepts:
            writer.visit_concept(concept)
        for node in self.mapper.root_nodes:
            writer.visit_node(node)

    def __init__(self, system: str):
        self.mapper = OntologyMapper(system)
