from sentence_transformers import SentenceTransformer

# 사전 학습된 Sentence-BERT 모델 로드
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 인덱스 이름 설정 (원래 쓰던대로)
index_name = 'biographies_vecdb'

def search_by_job(es, job: str):
    """
    주어진 직업(job)을 벡터로 변환하여 Elasticsearch에서 유사한 문서를 검색하고,
    가장 높은 _score 값을 가진 문서의 content 값을 반환하는 함수.

    :param job: 검색할 직업 문자열
    :return: _score가 가장 높은 문서의 content 값
    """

    # job 값을 벡터로 변환 (384 차원)
    query_vector = model.encode([job])[0]  # 384 차원의 벡터로 변환

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

    # 검색 결과에서 가장 높은 _score를 가진 문서의 content 값 추출
    if res['hits']['hits']:
        top_hit = res['hits']['hits'][0]  # 가장 높은 _score 문서 (첫 번째 문서)
        return top_hit['_source']['content']
    else:
        return None  # 검색 결과가 없을 경우 None 반환