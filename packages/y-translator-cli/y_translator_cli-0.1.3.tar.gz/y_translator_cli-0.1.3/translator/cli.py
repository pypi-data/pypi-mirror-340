"""Command-line interface for Y-Translator CLI"""

import argparse
import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from . import __version__
from .config import Config
from .agent import TranslatorAgent

def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Y-Translator CLI - AI-powered English-Chinese translator"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"Y-Translator CLI version {__version__}"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug mode"
    )
    parser.add_argument(
        "--model",
        help="AI model to use (default: gpt-4)",
        default=None
    )
    parser.add_argument(
        "--api-key",
        help="OpenAI API key",
        default=None
    )
    parser.add_argument(
        "--api-base",
        help="Custom API base URL",
        default=None
    )
    parser.add_argument(
        "-n", "--no-stream",
        action="store_true",
        help="Disable streaming mode"
    )
    return parser

def run_interactive_session(agent: TranslatorAgent, stream: bool = True):
    """Run an interactive session with the agent"""
    history = InMemoryHistory()
    session = PromptSession(history=history)
    
    print("\n" + "="*60)
    print(f"🚀 \033[1;36mY-Translator CLI v{__version__}\033[0m - \033[1mAI-powered Translator\033[0m")
    print("="*60)
    print("\033[1;32m✓\033[0m English to Chinese translation")
    print("\033[1;32m✓\033[0m Chinese to English translation")
    print("\033[1;32m✓\033[0m Type 'exit' or press Ctrl+C to quit")
    print("")
    print("\033[1;33mType your text to translate and press Enter:\033[0m")
    
    while True:
        try:
            query = session.prompt('>>> ')

            if query.lower() in ("exit", "quit", "退出"):
                print("\n\033[1;32mGoodbye! Have a great day!\033[0m")
                break

            agent.process_query(query, stream=stream)

        except KeyboardInterrupt:
            print("\n\033[1;32mExiting...\033[0m")
            break
        except Exception as e:
            print(f"\033[1;31mError: {e}\033[0m")

def main():
    """Main entry point for Y-Translator CLI"""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        config = Config.from_args(args)
        agent = TranslatorAgent(config)
        run_interactive_session(agent, stream=not args.no_stream)
    except KeyboardInterrupt:
        print("\n\033[1;32mExiting...\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\033[1;31mError: {e}\033[0m", file=sys.stderr)
        if args.verbose:
            raise
        sys.exit(1)

if __name__ == "__main__":
    main() 