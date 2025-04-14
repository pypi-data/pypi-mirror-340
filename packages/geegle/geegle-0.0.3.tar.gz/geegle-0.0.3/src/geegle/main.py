import asyncio
from geegle.cli import CLI

async def main():
    """Main entry point for the application."""
    cli = CLI()
    try:
        await cli.start()
    except Exception as e:
        print(f"Fatal error: {e}")
        exit(1)

def run():
    asyncio.run(main())

if __name__ == "__main__":
    run()