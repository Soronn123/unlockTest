import logging

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s",
    datefmt='%I:%M:%S',
    level=logging.INFO
)


from src.CoreClass import Core

def main():
    core = Core()
    try:
        core.load()
        core.run()
    except Exception as e:
        logging.error(f"Critical error: {e}")


if __name__ == "__main__":
    main()
