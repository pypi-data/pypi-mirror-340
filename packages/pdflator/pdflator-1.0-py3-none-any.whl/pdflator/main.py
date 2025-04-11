import os
import argparse
import sys

from pdflator.languages import *
from pdflator.translation import *
from pdflator.translate_pdf import translate_pdf
from importlib import import_module

def translate_cli(args):
    """
    Function to handle PDF translation from the command line.
    """
    input_path = args.input
    output_path = args.output
    input_lang = args.input_lang
    dest_lang = args.output_lang
    translator_code = args.translator

    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)

    try:
        print(f"Translating {input_path} from {input_lang} to {dest_lang} using {translator_code}...")
        translate_pdf(
            input_path=input_path,
            output_path=output_path,
            input_lang=input_lang,
            dest_lang=dest_lang,
            translator_code=translator_code
        )
        print(f"Translation complete! Output saved to {output_path}")
    except Exception as e:
        print(f"Error during translation: {str(e)}")
        sys.exit(1)

def web_cli(args):
    """
    Function to start the web application with custom host/port.
    """
    try:
        # Import app module dynamically to avoid circular imports
        web_module = import_module('pdflator.web')
        web_module.run_web_app(host=args.host, port=args.port, debug=args.debug)
    except Exception as e:
        print(f"Error starting web application: {str(e)}")
        sys.exit(1)

def main():
    """    
    Main function to handle PDFlator's CLI interface.
    """
    parser = argparse.ArgumentParser(
        description="PDFlator - Translate PDF files while preserving layout",
        prog="pdflator"
    )
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Translation command (default when no subcommand is provided)
    translate_parser = subparsers.add_parser("translate", help="Translate a PDF file")
    translate_parser.add_argument('-i', '--input', required=True, help='Input PDF file path')
    translate_parser.add_argument('-o', '--output', required=True, help='Output PDF file path')
    translate_parser.add_argument('-il', '--input-lang', default='auto', help='Input language code (default: auto)')
    translate_parser.add_argument('-ol', '--output-lang', default='en', help='Output language code (default: en)')
    try:
        translate_parser.add_argument('-t', '--translator', default='gtrans', choices=[t['code'] for t in TranslatorFactory.list_translators()],
                               help='Translator to use (default: gtrans)')
    except Exception as e:
        print(f"Error listing translators: {e}")
        sys.exit(1)
    translate_parser.set_defaults(func=translate_cli)
    
    # Web interface command
    web_parser = subparsers.add_parser("web", help="Start the web interface")
    web_parser.add_argument('--host', default='127.0.0.1', help='Host to listen on (default: 127.0.0.1)')
    web_parser.add_argument('--port', type=int, default=5000, help='Port to listen on (default: 5000)')
    web_parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    web_parser.set_defaults(func=web_cli)
    
    # Also add translation arguments to the main parser for backward compatibility
    # and to make it the default behavior when no subcommand is specified
    parser.add_argument('-i', '--input', help='Input PDF file path')
    parser.add_argument('-o', '--output', help='Output PDF file path')
    parser.add_argument('-il', '--input-lang', default='auto', choices=[lang['code'] for lang in LanguageFactory.list_languages()], help='Input language code (default: auto)')
    parser.add_argument('-ol', '--output-lang', default='en', choices=[lang['code'] for lang in LanguageFactory.list_languages()], help='Output language code (default: en)')
    try:
        parser.add_argument('-t', '--translator', default='gtrans', choices=[t['code'] for t in TranslatorFactory.list_translators()],
                       help='Translator to use (default: gtrans)')
    except Exception as e:
        print(f"Error listing translators: {e}")
        sys.exit(1)
    
    # Add version flag
    parser.add_argument('--version', action='store_true', help='Show version information')
    
    args = parser.parse_args()
    
    # Handle version flag
    if args.version:
        import pkg_resources
        try:
            version = pkg_resources.get_distribution("pdflator").version # type: ignore
            print(f"PDFlator version {version}")
        except pkg_resources.DistributionNotFound: # type: ignore
            print("PDFlator version unknown (development mode)")
        return
    
    # If a subcommand was specified, call its handler function
    if hasattr(args, 'func'):
        args.func(args)
        return
    
    # If no subcommand but input/output are specified, do translation
    if args.input and args.output:
        translate_cli(args)
        return
    
    # If no valid command was determined, show help
    parser.print_help()

if __name__ == '__main__':
    main()