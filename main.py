from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {
        'data': 'blog List'
    }


@app.get('/blog/{id}')
def show(id):
    return {
        'data': id
    }
