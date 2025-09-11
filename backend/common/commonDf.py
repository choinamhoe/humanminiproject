import json
def dftoJson(df,name):
    # 2. 💡 DataFrame을 딕셔너리의 '리스트' 형태로 변환합니다.
    # orient='records' 옵션이 각 행을 하나의 딕셔너리로 만들어 리스트에 담아줍니다.
    golf_list  = df.to_dict(orient='records')
    # 3. 원하는 대표 이름('golfInfo')을 키로 하는 최종 딕셔너리를 만듭니다.
    final_dict = {name : golf_list}
    # 결과 확인 (pprint나 json.dumps를 사용하면 보기 편합니다)
    row = json.dumps(final_dict, indent=2, ensure_ascii=False)
    #print(row)
    return row