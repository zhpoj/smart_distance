from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI(title="智能点餐的API接口", description="基于OpenAI的智能点餐系统", version="1.0.0")

@app.get("/")
def root():
    return {"message": "欢迎来到智能点餐系统"}

@app.get("/healthy")
def healthy():
    return {"message": "系统正常"}

class MenuListResponse(BaseModel):
    sucess: bool
    menu_list: List[Dict]
    count: int
    message: str

@app.get("/menulist",responses=MenuListResponse)
async def get_menulist():
    #菜品区域的列表展示


