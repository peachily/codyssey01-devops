# ----------------------------------------------------------------------------------------------------
# 작성목적 : 지역 지도 시각화 및 PNG 파일 저장
# 작성일 : 2025-07-21

# 변경사항 내역 (날짜 | 변경목적 | 변경내용 | 작성자 순으로 기입)
# 2025-07-21 | 최초 구현 | 지역 지도 시각화 기능 구현 | zookeeper
# ----------------------------------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def create_map_visualization():
    """지역 데이터를 시각화하여 지도를 생성하는 함수"""
    
    # 1. 데이터 로드 및 병합
    print('=== 데이터 로딩 및 병합 ===')
    
    area_category = pd.read_csv('area_category.csv', skipinitialspace=True)
    area_map = pd.read_csv('area_map.csv')
    area_struct = pd.read_csv('area_struct.csv')
    
    # 구조물 ID를 이름으로 변환
    category_mapping = dict(zip(area_category['category'], area_category['struct']))
    area_struct['struct_name'] = area_struct['category'].map(category_mapping)
    area_struct['struct_name'] = area_struct['struct_name'].fillna('Empty')
    
    # 데이터 병합
    merged_data = pd.merge(area_map, area_struct, on=['x', 'y'], how='inner')
    
    print(f'전체 데이터 포인트: {len(merged_data)}')
    
    # 2. 맵 크기 설정
    min_x, max_x = merged_data['x'].min(), merged_data['x'].max()
    min_y, max_y = merged_data['y'].min(), merged_data['y'].max()
    
    print(f'맵 범위: x({min_x}~{max_x}), y({min_y}~{max_y})')
    
    # 3. 시각화 설정
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    ax.set_xlim(min_x - 0.5, max_x + 0.5)
    ax.set_ylim(min_y - 0.5, max_y + 0.5)
    
    # y축 뒤집기 (좌측 상단이 (1,1)이 되도록)
    ax.invert_yaxis()
    
    # 4. 그리드 라인 그리기
    print('=== 그리드 라인 생성 ===')
    
    # 세로 그리드 라인 (x축)
    for x in range(min_x, max_x + 1):
        ax.axvline(x=x - 0.5, color='lightgray', linewidth=0.5, alpha=0.7)
    ax.axvline(x=max_x + 0.5, color='lightgray', linewidth=0.5, alpha=0.7)
    
    # 가로 그리드 라인 (y축)
    for y in range(min_y, max_y + 1):
        ax.axhline(y=y - 0.5, color='lightgray', linewidth=0.5, alpha=0.7)
    ax.axhline(y=max_y + 0.5, color='lightgray', linewidth=0.5, alpha=0.7)
    
    # 5. 건설 현장 먼저 그리기 (다른 구조물보다 뒤에 배치)
    print('=== 건설 현장 표시 ===')
    
    construction_sites = merged_data[merged_data['ConstructionSite'] == 1]
    print(f'건설 현장 개수: {len(construction_sites)}')
    
    for _, site in construction_sites.iterrows():
        # 회색 사각형 (살짝 겹치도록 크게)
        rect = patches.Rectangle(
            (site['x'] - 0.6, site['y'] - 0.6), 1.2, 1.2,
            linewidth=1, edgecolor='gray', facecolor='lightgray', 
            alpha=0.7, zorder=1
        )
        ax.add_patch(rect)
    
    # 6. 구조물 표시 (건설 현장 위에 그리기)
    print('=== 구조물 표시 ===')
    
    # 각 구조물별로 처리
    structures = merged_data[merged_data['struct_name'] != 'Empty']
    
    apartment_count = 0
    building_count = 0
    coffee_count = 0
    myhome_count = 0
    
    for _, struct in structures.iterrows():
        x, y = struct['x'], struct['y']
        struct_type = struct['struct_name']
        
        if struct_type == 'Apartment':
            # 갈색 원형
            circle = patches.Circle(
                (x, y), 0.25, linewidth=2, 
                edgecolor='saddlebrown', facecolor='sandybrown', 
                zorder=3
            )
            ax.add_patch(circle)
            apartment_count += 1
            
        elif struct_type == 'Building':
            # 갈색 원형
            circle = patches.Circle(
                (x, y), 0.25, linewidth=2, 
                edgecolor='saddlebrown', facecolor='sandybrown', 
                zorder=3
            )
            ax.add_patch(circle)
            building_count += 1
            
        elif struct_type == 'BandalgomCoffee':
            # 녹색 사각형
            rect = patches.Rectangle(
                (x - 0.2, y - 0.2), 0.4, 0.4,
                linewidth=2, edgecolor='darkgreen', facecolor='lightgreen', 
                zorder=4
            )
            ax.add_patch(rect)
            coffee_count += 1
            
        elif struct_type == 'MyHome':
            # 녹색 삼각형
            triangle = patches.Polygon(
                [(x, y - 0.25), (x - 0.22, y + 0.15), (x + 0.22, y + 0.15)],
                linewidth=2, edgecolor='darkgreen', facecolor='lightgreen', 
                zorder=4
            )
            ax.add_patch(triangle)
            myhome_count += 1
    
    print(f'아파트: {apartment_count}개')
    print(f'빌딩: {building_count}개') 
    print(f'반달곰 커피: {coffee_count}개')
    print(f'내 집: {myhome_count}개')
    
    # 7. 좌표 레이블 추가
    print('=== 좌표 레이블 추가 ===')
    
    # x축 레이블
    ax.set_xticks(range(min_x, max_x + 1))
    ax.set_xticklabels(range(min_x, max_x + 1))
    
    # y축 레이블  
    ax.set_yticks(range(min_y, max_y + 1))
    ax.set_yticklabels(range(min_y, max_y + 1))
    
    # 8. 제목 및 범례
    ax.set_title('Area Map', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('X Coordinate', fontsize=12)
    ax.set_ylabel('Y Coordinate', fontsize=12)
    
    # 범례 생성
    legend_elements = [
        patches.Patch(color='lightgray', label='Construction Site (Gray Square)'),
        patches.Patch(color='sandybrown', label='Apartment/Building (Brown Circle)'),
        patches.Patch(color='lightgreen', label='Bandalcom Coffee (Green Square)'),
        patches.Patch(color='lightgreen', label='My Home (Green Triangle)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
    
    # 9. Area 구분선 표시 (선택사항)
    print('=== Area 구분 정보 추가 ===')
    
    # Area별로 다른 배경색 적용 (매우 연하게)
    area_colors = {0: 'red', 1: 'blue', 2: 'yellow', 3: 'purple'}
    
    for area_id in sorted(merged_data['area'].unique()):
        area_data = merged_data[merged_data['area'] == area_id]
        for _, point in area_data.iterrows():
            if point['struct_name'] == 'Empty' and point['ConstructionSite'] == 0:
                # 빈 공간에만 매우 연한 색상 적용
                circle = patches.Circle(
                    (point['x'], point['y']), 0.1, 
                    facecolor=area_colors.get(area_id, 'white'), 
                    alpha=0.2, zorder=0
                )
                ax.add_patch(circle)
    
    # Area 정보를 텍스트로 추가
    area_info = merged_data.groupby('area').size()
    info_text = 'Area Info:\n'
    for area_id, count in area_info.items():
        info_text += f'Area {area_id}: {count} coords\n'
    
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # 10. 이미지 저장
    plt.tight_layout()
    plt.savefig('map.png', dpi=300, bbox_inches='tight')
    print('\n=== Map Saved Successfully ===')
    print('Map saved as \'map.png\' file.')
    
    # 플롯 보여주기
    plt.show()
    
    return merged_data

if __name__ == '__main__':
    data = create_map_visualization() 
