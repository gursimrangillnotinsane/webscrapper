
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

@app.post("/jobank/get")
def get_posts(title:schemas.userInput):
    jonbank=jobs.searchJobsJobBank(title.skill,title.location,title.pagenumber)

    return jonbank

@app.post("/indeed/get")
def get_INposts(title:schemas.userInput):
    indeed=jobs.searchJobIndeed(title.skill,title.location,title.pagenumber)

    return indeed

@app.post("/linkdin/get")
def get_LIposts(title:schemas.userInput):
    linkdin=jobs.searchJobsLinkdin(title.skill,title.location,title.pagenumber)

    return linkdin