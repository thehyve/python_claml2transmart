import sys

import click
from python_claml import claml
from python_claml.claml_types import ClaML

from .ontology_writer import OntologyWriter

from transmart_loader.console import Console
from transmart_loader.copy_writer import TransmartCopyWriter
from transmart_loader.loader_exception import LoaderException


def run(system: str, input_file: str, output_dir: str):
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
                ontology_writer.process_class(cls)
        ontology_writer.write(copy_writer)
        Console.info('Done.')
    except LoaderException as e:
        Console.error(e)
        sys.exit(1)


@click.command()
@click.argument('system')
@click.argument('input_file')
@click.argument('output_dir')
def claml2transmart(system: str, input_file: str, output_dir: str):
    run(system, input_file, output_dir)


def main():
    claml2transmart()


if __name__ == '__main__':
    main()
