from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.es_vecDB_search import search_by_job
from services.llm_service import interactive_story_generation
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
import openai

load_dotenv()

# FastAPI 인스턴스 생성
app = FastAPI()

# Elasticsearch 연결 설정
es = Elasticsearch(hosts=["http://elasticsearch:9200"])

openai_api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key = openai_api_key)

# Pydantic을 사용해 요청 모델 정의
class StoryRequest(BaseModel):
    job: str
    text: str
    storyIndex: int
    id: int

# Pydantic을 사용해 응답 모델 정의
class StoryResponse(BaseModel):
    story: str
    flag: bool
    storyIndex: int
    id: int
    
# Pydantic을 사용해 요청 모델 정의 (이미지 생성)
class ImageRequest(BaseModel):
    job: str

# 프롬프트 생성 함수
def generate_prompt(age, gender, job):
    return f"{age}세의 한국인 {gender}가 {job}로 일하고 있습니다. {gender}는 {job} 관련 작업 환경에서 전문적인 일을 수행하고 있으며, 주위에는 {job}과 관련된 작업 도구와 환경이 마련되어 있습니다."


# 스토리 생성 엔드포인트 정의
@app.post("/ai/story", response_model=StoryResponse)
async def generate_story_endpoint(request: StoryRequest):
    try:
         # 직업값을 기반으로 Elasticsearch에서 가장 유사한 다큐먼트의 내용을 가져오기
        doc_content = search_by_job(es, request.job)  # 직업 값을 이용한 벡터 검색 함수 호출
        print(doc_content)

        # 스토리 생성 로직 호출 (interactive_story_generation 함수 사용)
        gen_story, flag, index= interactive_story_generation(request.job, request.text, doc_content, request.storyIndex)
        
        # 결과 반환 
        result = {
            "story": gen_story,
            "flag": flag,  # 성공 시 True
            "storyIndex": index,
            "id": request.id
        }

        return StoryResponse(**result)

    except Exception as e:
        # 에러 발생 시 HTTP 500 예외 처리
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/generate-image/")
async def generate_image(request: ImageRequest):
    try:
        age = 66
        gender = "여성"
        prompt = generate_prompt(age, gender, request.job)

        # OpenAI DALL-E API를 호출하여 이미지 생성
        response = client.images.generate(
            model='dall-e-3',
            prompt=prompt,
            size='1024x1024',
            quality='standard',
            n=1
        )
        
        image_url = response.data[0].url
        return {"image_url": image_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# uvicorn ai_server:app --reload