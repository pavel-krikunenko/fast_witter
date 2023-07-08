import uvicorn
from service.app import create_app


app = create_app()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run("main:app", port=8010)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
