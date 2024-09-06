from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

# Elasticsearch 연결 설정
es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200, 'scheme': 'http'}])

# 사전 학습된 Sentence-BERT 모델 로드
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 인덱스 이름 설정
index_name = 'biographies_vecdb'

# 검색할 텍스트를 벡터로 변환 (384 차원)
query_text = "무역가"
query_vector = model.encode([query_text])[0]  # 384 차원의 벡터로 변환

# Elasticsearch 벡터 검색 쿼리 작성
query_body = {
    "query": {
        "script_score": {
            "query": {
                "match_all": {}
            },
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'content_vector') + 1.0",
                "params": {
                    "query_vector": query_vector.tolist()  # 벡터 데이터를 리스트로 변환
                }
            }
        }
    }
}

# Elasticsearch에서 검색 실행
res = es.search(index=index_name, body=query_body)

# 검색 결과 출력
for hit in res['hits']['hits']:
    print(f"ID: {hit['_id']}, 점수: {hit['_score']}")
    print(f"제목: {hit['_source']['title']}")
    print(f"내용: {hit['_source']['content'][:200]}...")  # 내용 일부만 출력
