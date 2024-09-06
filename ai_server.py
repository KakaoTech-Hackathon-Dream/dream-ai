from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.es_vecDB_search import search_by_job
from services.llm_service import interactive_story_generation
from elasticsearch import Elasticsearch

# FastAPI 인스턴스 생성
app = FastAPI()

# Elasticsearch 연결 설정
es = Elasticsearch(hosts=["http://localhost:9200"])

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

# uvicorn ai_server:app --reload