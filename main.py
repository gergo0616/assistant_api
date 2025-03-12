"""
Main entry point for the Azure Email Assistant application.
"""
import argparse
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Azure Email Assistant")
    parser.add_argument(
        "action",
        choices=["run", "test"],
        help="Action to perform: 'run' to start the server, 'test' to run tests"
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock assistant instead of Azure OpenAI"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port to run the server on (default: 5000)"
    )
    
    args = parser.parse_args()
    
    if args.action == "run":
        # Import here to avoid circular imports
        from azure_email_assistant.api.server import create_azure_server, create_mock_server
        
        if args.mock:
            logger.info("Starting API server with mock assistant")
            server = create_mock_server()
        else:
            logger.info("Starting API server with Azure OpenAI assistant")
            server = create_azure_server()
        
        logger.info(f"Server running at http://{server.host}:{server.port}")
        logger.info("Available endpoints:")
        logger.info("  - /webhook/email (POST): Process incoming emails")
        logger.info("  - /health (GET): Health check endpoint")
        logger.info("  - /test (GET): Test endpoint")
        
        server.run()
    
    elif args.action == "test":
        # Import the test runner
        from run_tests_new import main as run_tests
        
        # Run tests
        return run_tests()


if __name__ == "__main__":
    sys.exit(main())
