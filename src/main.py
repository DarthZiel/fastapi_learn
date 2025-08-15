from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def great(name: str='World'):
    return {f'hello, {name.title()}'}

