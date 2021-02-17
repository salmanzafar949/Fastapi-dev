from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index(limit):
    return {
        'data': f'{limit} from the blog List'
    }


@app.get('/blog/unpublished')
def unpublished_blogs():
    return {
        'data': 'unpublished blogs'
    }


@app.get('/blog/{id}')
def show(id:int):
    return {
        'data': id
    }