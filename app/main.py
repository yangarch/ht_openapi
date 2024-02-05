from fastapi import FastAPI, Request

app = FastAPI()


#main code
@app.get("/get")
async def get_data(q):
    ...
    return q


@app.post("/post")
async def post_data(request: Request):
    ...
    return {request}
