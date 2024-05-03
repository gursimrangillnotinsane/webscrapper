
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import schemas
from . import jobs

app=FastAPI()
origions=["*"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origions,#domains which 
    allow_credentials=True,
    allow_methods=["*"],# allow specific mehods(get,update)
    allow_headers=["*"],#allwo which headers
)



@app.get("/") #decorator
async def root():
    return {"message": f"Hello "}

@app.post("/get")
def get_posts(title:schemas.userInput):
    indeed,jonbank=jobs.caller(title.skill,title.location,title.pagenumber)

    return {"indeed":indeed,"jobank":jonbank}

