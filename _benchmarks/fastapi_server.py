from fastapi import FastAPI
from fastapi.responses import Response
from common_data import CONTENTS
app = FastAPI()


@app.get("/")
async def root():
    return Response(content=CONTENTS, media_type="application/json")