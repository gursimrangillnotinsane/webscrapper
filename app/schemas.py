from pydantic import BaseModel

class userInput(BaseModel):
    skill:str
    location:str
    pagenumber:int