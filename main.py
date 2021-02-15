from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {
        'data': 'hello world'
    }


@app.get('/about')
def about():
    return {
        'data': {
            'key': 'about api'
        }
    }
