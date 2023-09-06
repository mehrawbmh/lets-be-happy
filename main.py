from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Let's be happy."}


@app.get("/hello/{name}")
async def say_hello(name: str, message: str = ''):
    message = 'you said ' + message if message else ''

    resp = {
        'message': f"Hello {name}. It's working bro ^_^. {message}"
    }
    response = JSONResponse(resp, 200)

    return response
