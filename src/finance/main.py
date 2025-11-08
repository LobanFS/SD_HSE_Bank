from src.finance.di.container import Container
from src.UI.app import run

if __name__ == "__main__":
    container = Container()
    run(container)