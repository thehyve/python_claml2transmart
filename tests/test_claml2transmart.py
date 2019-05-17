#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the claml2transmart module.
"""
from typing import Optional
from unittest.mock import Mock
from xml.dom import Node

import pytest
from claml2transmart.claml2transmart import run
from python_claml.claml_types import ClaML, Identifier, Class, Rubric, SuperClass
from transmart_loader.copy_writer import TransmartCopyWriter

from claml2transmart.ontology_writer import OntologyWriter


def count_lines(filename) -> int:
    count = 0
    with open(filename, 'r') as f:
        for line in f:
            count = count + 1
    return count


def mock_dom(value: str):
    node = Mock()
    node.nodeType = Node.TEXT_NODE
    node.data = value
    dom = Mock()
    dom.childNodes = [node]
    return dom


def mock_rubric(label: str) -> Rubric:
    rubric: Rubric = Mock()
    rubric.kind = 'preferred'
    rubric.Label = [Mock()]
    rubric.Label[0].toDOM.return_value = mock_dom(label)
    return rubric


def mock_superclass(code: str) -> SuperClass:
    cls: SuperClass = Mock()
    cls.code = code
    return cls


def mock_class(code: str, name: str, super_class: Optional[str] = None) -> Class:
    cls: Class = Mock()
    cls.code = code
    cls.Rubric = [mock_rubric(name)]
    if super_class is not None:
        cls.SuperClass = [mock_superclass(super_class)]
    else:
        cls.SuperClass = []
    return cls


@pytest.fixture
def simple_classification() -> ClaML:
    identifier: Identifier = Mock()
    identifier.authority = 'http://mock.system'
    identifier.uid = '1234567'
    classification: ClaML = Mock()
    classification.Identifier = [identifier]
    classification.Class = [
        mock_class('I', 'First category'),
        mock_class('123', 'Test class', 'I'),
        mock_class('ABC', 'Dummy class', 'I'),
        mock_class('II', 'Second category'),
        mock_class('XYZ', 'Test case', 'II')
    ]
    return classification


def test_write_ontology(tmp_path, simple_classification: ClaML):
    for identifier in simple_classification.Identifier:
        assert identifier.authority == 'http://mock.system'
        assert identifier.uid == '1234567'
    target_path = tmp_path.as_posix()
    copy_writer = TransmartCopyWriter(target_path)
    writer = OntologyWriter('http://mock.system')
    for cls in simple_classification.Class:
        writer.process_class(cls)
    assert len(writer.mapper.concepts) == 5
    assert len(writer.mapper.root_nodes) == 2
    assert len(writer.mapper.nodes) == 5
    writer.write(copy_writer)
    del writer, copy_writer
    assert count_lines(target_path + '/i2b2demodata/concept_dimension.tsv') == 6
    assert count_lines(target_path + '/i2b2metadata/i2b2_secure.tsv') == 6


def test_claml2transmart_with_code_prefix(tmp_path):
    target_path = tmp_path.as_posix()
    run('http://mock.system', 'resources/test.xml', target_path, True)
    assert count_lines(target_path + '/i2b2demodata/concept_dimension.tsv') == 10
    assert count_lines(target_path + '/i2b2metadata/i2b2_secure.tsv') == 10


def test_claml2transmart_without_code_prefix(tmp_path):
    target_path = tmp_path.as_posix()
    run('http://hl7.org/fhir', 'resources/fhir.xml', target_path, False)
    assert count_lines(target_path + '/i2b2demodata/concept_dimension.tsv') == 6
    assert count_lines(target_path + '/i2b2metadata/i2b2_secure.tsv') == 6
