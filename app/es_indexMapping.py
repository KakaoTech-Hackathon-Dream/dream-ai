from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

# Elasticsearch 연결 설정
es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200, 'scheme': 'http'}])

# 사전 학습된 Sentence-BERT 모델 로드
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 인덱스 이름 설정
index_name = 'biographies_vecdb'

# 인덱스 매핑 설정 (384 차원으로 수정)
mapping = {
    "mappings": {
        "properties": {
            "content": {
                "type": "text"
            },
            "content_vector": {
                "type": "dense_vector",
                "dims": 384  # 모델의 벡터 차원을 384로 설정
            },
            "title": {
                "type": "text"
            }
        }
    }
}

# 인덱스 생성 (필요시)
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=mapping)

print("인덱스가 384 차원으로 생성되었습니다.")
