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
    
    # 5. Area 1 반달곰 커피 분석
    print("\n=== Area 1 반달곰 커피 분석 ===")
    
    # 반달곰 커피 위치 찾기
    coffee_locations = area1_data[area1_data['struct_name'] == 'BandalgomCoffee']
    print(f"\n반달곰 커피 매장 수: {len(coffee_locations)}")
    print("반달곰 커피 위치:")
    for idx, row in coffee_locations.iterrows():
        construction_status = "건설 가능" if row['ConstructionSite'] == 1 else "건설 불가"
        print(f"  좌표 ({row['x']}, {row['y']}) - {construction_status}")
    
    # Area 1 구조물 분포
    print("\nArea 1 구조물 분포:")
    struct_count = area1_data['struct_name'].value_counts()
    for struct_name, count in struct_count.items():
        print(f"  {struct_name}: {count}개")
    
    # Area 1 건설 가능 지역 분석
    construction_possible = area1_data[area1_data['ConstructionSite'] == 1]
    construction_impossible = area1_data[area1_data['ConstructionSite'] == 0]
    
    print(f"\nArea 1 건설 현황:")
    print(f"  건설 가능 지역: {len(construction_possible)}개")
    print(f"  건설 불가 지역: {len(construction_impossible)}개")
    
    # 6. Area 1 맵 시각화 (텍스트 기반)
    print("\n=== Area 1 맵 시각화 ===")
    print("범례: [C] = 반달곰커피, [A] = 아파트, [B] = 빌딩, [M] = 내집, [ ] = 빈공간")
    print("배경: ■ = 건설불가, □ = 건설가능")
    
    # Area 1의 x, y 범위 찾기
    min_x, max_x = area1_data['x'].min(), area1_data['x'].max()
    min_y, max_y = area1_data['y'].min(), area1_data['y'].max()
    
    print(f"\nArea 1 범위: x({min_x}~{max_x}), y({min_y}~{max_y})")
    print()
    
    # 맵 그리기
    for y in range(min_y, max_y + 1):
        row_str = ""
        for x in range(min_x, max_x + 1):
            cell_data = area1_data[(area1_data['x'] == x) & (area1_data['y'] == y)]
            
            if len(cell_data) > 0:
                cell = cell_data.iloc[0]
                
                # 구조물 기호 결정
                if cell['struct_name'] == 'BandalgomCoffee':
                    symbol = '[C]'
                elif cell['struct_name'] == 'Apartment':
                    symbol = '[A]'
                elif cell['struct_name'] == 'Building':
                    symbol = '[B]'
                elif cell['struct_name'] == 'MyHome':
                    symbol = '[M]'
                else:
                    symbol = '[ ]'
                
                # 건설 가능 여부에 따른 배경
                if cell['ConstructionSite'] == 1:
                    background = '□'
                else:
                    background = '■'
                
                row_str += f"{background}{symbol} "
            else:
                row_str += "     "
        
        print(f"y={y:2d}: {row_str}")
    
    # 7. 반달곰 커피 주변 분석
    print("\n=== 반달곰 커피 주변 분석 ===")
    
    for idx, coffee in coffee_locations.iterrows():
        coffee_x, coffee_y = coffee['x'], coffee['y']
        print(f"\n반달곰 커피 ({coffee_x}, {coffee_y}) 주변 상황:")
        
        # 주변 8방향 + 자기 자신 체크
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,0), (0,1), (1,-1), (1,0), (1,1)]
        
        for dx, dy in directions:
            check_x, check_y = coffee_x + dx, coffee_y + dy
            nearby = area1_data[(area1_data['x'] == check_x) & (area1_data['y'] == check_y)]
            
            if len(nearby) > 0:
                nearby_cell = nearby.iloc[0]
                if dx == 0 and dy == 0:
                    position = "현재위치"
                else:
                    position = f"({dx:+2d},{dy:+2d})"
                
                construction = "건설가능" if nearby_cell['ConstructionSite'] == 1 else "건설불가"
                print(f"  {position}: {nearby_cell['struct_name']} - {construction}")
    
    # 8. 결과를 CSV로 저장
    output_filename = 'area1_coffee_data.csv'
    area1_data.to_csv(output_filename, index=False)
    print(f"\nArea 1 데이터가 '{output_filename}' 파일로 저장되었습니다.")
    
    return area1_data

if __name__ == '__main__':
    area1_data = filter_area1_coffee_data() 
