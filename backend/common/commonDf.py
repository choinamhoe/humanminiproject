import json
from datetime import datetime

def dftoDict(df,name):
    # 2. 💡 DataFrame을 딕셔너리의 '리스트' 형태로 변환합니다.
    # orient='records' 옵션이 각 행을 하나의 딕셔너리로 만들어 리스트에 담아줍니다.
    golf_list  = df.to_dict(orient='records')
    # 3. 원하는 대표 이름('golfInfo')을 키로 하는 최종 딕셔너리를 만듭니다.
    final_dict = {name : golf_list}
    #print(final_dict)
    # 결과 확인 (pprint나 json.dumps를 사용하면 보기 편합니다)
    # row = json.dumps(final_dict, indent=2, ensure_ascii=False)
    #print(row)
    return final_dict

def dftoJson(df,name):
    # 2. 💡 DataFrame을 딕셔너리의 '리스트' 형태로 변환합니다.
    # orient='records' 옵션이 각 행을 하나의 딕셔너리로 만들어 리스트에 담아줍니다.
    golf_list  = df.to_dict(orient='records')
    # 3. 원하는 대표 이름('golfInfo')을 키로 하는 최종 딕셔너리를 만듭니다.
    final_dict = {name : golf_list}
    #print(final_dict)
    # 결과 확인 (pprint나 json.dumps를 사용하면 보기 편합니다)
    row = json.dumps(final_dict, indent=2, ensure_ascii=False)
    #print(row)
    return row

from datetime import datetime

def postprocess_weather(data,dateColumn):
    #print(f"postprocess_weather start data:{data}, datecolumn:{dateColumn}")
    processed = []
    for item in data:
        #print(f"postprocess_weather start item:{item}")
        new_item = item.copy()

        # 1. time 처리 (+09:00 여부에 따라 분기)
        if dateColumn in new_item and isinstance(new_item[dateColumn], str):
            #print(f"postprocess_weather time 처리 (+09:00 여부에 따라 분기) start")
            time_str = new_item[dateColumn]
            if "+09:00" in time_str:  # case 1: +09:00 포함
                #print(f"postprocess_weather time 처리 (+09:00 포함) start")
                try:
                    dt = datetime.fromisoformat(time_str.replace("+09:00", ""))
                    new_item[dateColumn] = dt.strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    new_item[dateColumn] = time_str.replace("+09:00", "")
                #print(f"postprocess_weather time 처리 (+09:00 포함) end")
            else:  # case 2: +09:00 없음
                #print(f"postprocess_weather time 처리 (+09:00 없음) start")
                try:
                    dt = datetime.fromisoformat(time_str)
                    new_item[dateColumn] = dt.strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    new_item[dateColumn] = time_str  # 파싱 실패 시 원본 유지
                #print(f"postprocess_weather time 처리 (+09:00 없음) end")
            new_item[dateColumn] = str(new_item[dateColumn])

        # 2. 숫자형 값 → 항상 소수 둘째자리까지 (문자열 변환)
        for key, value in new_item.items():
            #print(f"postprocess_weather 2. 숫자형 값 → 항상 소수 둘째자리까지 (문자열 변환) start")
            if isinstance(value, float):
                new_item[key] = "{:.2f}".format(value)

        processed.append(new_item)
    return processed

