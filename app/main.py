from fastapi import FastAPI


app = FastAPI()


@app.get("/test")
def test():
    return {"message": "Hello World!"}


@app.get("/test2")
def test():
    return {"message": "Goodbye world!"}

@app.get("/test3")
def test():
    return {"message": "world!"}