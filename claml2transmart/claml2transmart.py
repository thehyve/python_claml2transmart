import sys

import click
from python_claml import claml
from python_claml.claml_types import ClaML

from .ontology_writer import OntologyWriter

from transmart_loader.console import Console
from transmart_loader.copy_writer import TransmartCopyWriter
from transmart_loader.loader_exception import LoaderException


def run(system: str, input_file: str, output_dir: str, code_prefix: bool = False):
    """
    Reads a ClaML classification document and translates it to ontology terms
    in TranSMART.

    :param system: a unique identifier to identify the ontology
    :param input_file: the input ClaML document
    :param output_dir: the output directory to write the transmart-copy files to
    :param code_prefix: Whether to use the concept code as prefix for the concept label
    :return:
    """
    Console.title('ClaML to TranSMART')
    try:
        Console.info('Writing files to {}'.format(output_dir))
        copy_writer = TransmartCopyWriter(output_dir)
        ontology_writer = OntologyWriter(system)
        with open(input_file, 'r') as reader:
            Console.info('Reading file contents from {} ...'.format(input_file))
            contents = reader.read()
            Console.info('Parsing ClaML document ...')
            classification: ClaML = claml.CreateFromDocument(contents)
            for identifier in classification.Identifier:
                Console.info('Classification identifier: {}/{}'.format(identifier.authority, identifier.uid))
            for cls in classification.Class:
                ontology_writer.process_class(cls, code_prefix)
        ontology_writer.write(copy_writer)
        Console.info('Done.')
    except LoaderException as e:
        Console.error(e)
        sys.exit(1)


@click.command()
@click.argument('system')
@click.argument('input_file')
@click.argument('output_dir')
@click.option('--code-prefix', is_flag=True)
def claml2transmart(system: str, input_file: str, output_dir: str, code_prefix: bool):
    run(system, input_file, output_dir, code_prefix)


def main():
    claml2transmart()


if __name__ == '__main__':
    main()
