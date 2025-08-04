# ----------------------------------------------------------------------------------------------------
# 작성목적 : 데이터 수집 및 분석 - Area 1 지역 반달곰 커피 데이터 분석
# 작성일 : 2025-07-22

# 변경사항 내역 (날짜 | 변경목적 | 변경내용 | 작성자 순으로 기입)
# 2025-07-22 | 요구사항 수정 | 요구사항에 맞는 데이터 분석 및 통계 리포트 구현 | zookeeper
# ----------------------------------------------------------------------------------------------------

import pandas as pd

def filter_area1_coffee_data():
    """Area 1 지역의 반달곰 커피 관련 데이터를 필터링하고 분석하는 함수"""
    
    # 1. CSV 파일들 불러오기
    print('=== CSV 파일 로딩 ===')
    
    area_category = pd.read_csv('area_category.csv', skipinitialspace=True)
    area_map = pd.read_csv('area_map.csv')
    area_struct = pd.read_csv('area_struct.csv')
    
    # 2. 구조물 ID를 이름으로 변환
    category_mapping = dict(zip(area_category['category'], area_category['struct']))
    area_struct['struct_name'] = area_struct['category'].map(category_mapping)
    area_struct['struct_name'] = area_struct['struct_name'].fillna('Empty')
    
    # 3. 데이터 병합
    merged_data = pd.merge(area_map, area_struct, on=['x', 'y'], how='inner')
    
    # 4. Area 1 데이터만 필터링
    print('=== Area 1 데이터 필터링 ===')
    
    area1_data = merged_data[merged_data['area'] == 1].copy()
    area1_data = area1_data.sort_values(['x', 'y']).reset_index(drop=True)
    
    print(f'Area 1 전체 좌표 개수: {len(area1_data)}')
    print('\nArea 1 전체 데이터:')
    print(area1_data)
    
    # 5. Area 1 구조물 분포
    print("\nArea 1 구조물 분포:")
    struct_count = area1_data['struct_name'].value_counts()
    for struct_name, count in struct_count.items():
        print(f"  {struct_name}: {count}개")
    
    return area1_data

if __name__ == '__main__':
    area1_data = filter_area1_coffee_data()
