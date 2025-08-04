# ----------------------------------------------------------------------------------------------------
# 작성목적 : 내 집에서 반달곰 커피까지의 최단 경로 탐색 및 시각화
# 작성일 : 2025-07-21

# 변경사항 내역 (날짜 | 변경목적 | 변경내용 | 작성자 순으로 기입)
# 2025-07-21 | 최초 구현 | BFS 최단 경로 알고리즘 및 지도 시각화 구현 | zookeeper
# 2025-07-21 | 수정 | 8방향 이동을 4방향 이동으로 변경 (대각선 이동 제거) | zookeeper
# 2025-07-23 | 보너스 구현 | 모든 구조물을 방문하는 최적화된 경로 계산 추가 | zookeeper
# ----------------------------------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 한글 폰트 설정
plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def load_and_prepare_data():
    """데이터를 로드하고 경로 탐색을 위해 준비하는 함수"""
    
    print('=== 데이터 로딩 및 준비 ===')
    
    # CSV 파일들 로드
    area_category = pd.read_csv('area_category.csv', skipinitialspace=True)
    area_map = pd.read_csv('area_map.csv')
    area_struct = pd.read_csv('area_struct.csv')
    
    # 결측치 확인 및 처리
    print('=== 결측치 확인 및 처리 ===')
    
    files_data = [
        ('area_category', area_category),
        ('area_map', area_map), 
        ('area_struct', area_struct)
    ]
    
    for name, df in files_data:
        missing_count = df.isnull().sum().sum()
        print(f'{name}: {len(df)}개 행, 결측치 {missing_count}개')
        
        if missing_count > 0:
            print(f'  컬럼별 결측치:')
            for col, count in df.isnull().sum().items():
                if count > 0:
                    print(f'    {col}: {count}개')
            
            # 결측치 처리 (필요시)
            if name == 'area_map':
                # 좌표나 건설현장 정보에 결측치가 있으면 제거
                df.dropna(inplace=True)
                print(f'  → {name} 결측치 제거 후: {len(df)}개 행')
            elif name == 'area_struct':
                # 좌표에 결측치가 있으면 제거, category는 0으로 대체
                df.dropna(subset=['x', 'y'], inplace=True)
                df['category'].fillna(0, inplace=True)
                print(f'  → {name} 결측치 처리 후: {len(df)}개 행')
    
    # 구조물 ID를 이름으로 변환
    print('=== 구조물 ID → 이름 변환 ===')
    category_mapping = dict(zip(area_category['category'], area_category['struct']))
    area_struct['struct_name'] = area_struct['category'].map(category_mapping)
    
    # 매핑되지 않은 값들을 'Empty'로 처리 (결측치 처리)
    unmapped_count = area_struct['struct_name'].isnull().sum()
    print(f'매핑되지 않은 구조물: {unmapped_count}개 → "Empty"로 처리')
    area_struct['struct_name'] = area_struct['struct_name'].fillna('Empty')
    
    # 데이터 병합
    print('=== 데이터 병합 ===')
    print(f'병합 전 - area_map: {len(area_map)}개, area_struct: {len(area_struct)}개')
    
    merged_data = pd.merge(area_map, area_struct, on=['x', 'y'], how='inner')
    
    print(f'병합 후 - merged_data: {len(merged_data)}개')
    
    # 병합 후 결측치 최종 확인
    final_missing = merged_data.isnull().sum().sum()
    if final_missing > 0:
        print(f'⚠️ 병합 후 결측치 발견: {final_missing}개')
        for col, count in merged_data.isnull().sum().items():
            if count > 0:
                print(f'  {col}: {count}개')
        
        # 최종 결측치 제거
        merged_data.dropna(inplace=True)
        print(f'최종 결측치 제거 후: {len(merged_data)}개')
    else:
        print('✅ 병합 후 결측치 없음')
    
    print(f'✅ 전체 데이터 포인트: {len(merged_data)}')
    
    return merged_data

def find_start_and_destinations(data):
    """시작점(내 집)과 도착점들(반달곰 커피)을 찾는 함수"""
    
    print('=== 시작점과 도착점 찾기 ===')
    
    # 내 집 위치 찾기
    my_home = data[data['struct_name'] == 'MyHome']
    if len(my_home) == 0:
        raise ValueError('내 집을 찾을 수 없습니다!')
    
    start_point = (my_home.iloc[0]['x'], my_home.iloc[0]['y'])
    print(f'시작점 (내 집): {start_point}')
    
    # 반달곰 커피 위치들 찾기
    coffee_shops = data[data['struct_name'] == 'BandalgomCoffee']
    if len(coffee_shops) == 0:
        raise ValueError('반달곰 커피를 찾을 수 없습니다!')
    
    destinations = [(row['x'], row['y']) for _, row in coffee_shops.iterrows()]
    print(f'도착점들 (반달곰 커피): {destinations}')
    
    return start_point, destinations

def find_all_structures(data):
    """보너스: 방문해야 할 모든 구조물을 찾는 함수"""
    
    print('\n=== 보너스: 모든 구조물 찾기 ===')
    
    # 건설현장이 아닌 모든 구조물 찾기 (Empty 제외)
    all_structures = data[(data['struct_name'] != 'Empty') & (data['ConstructionSite'] == 0)]
    
    structure_points = []
    structure_types = []
    
    for _, struct in all_structures.iterrows():
        point = (struct['x'], struct['y'])
        struct_type = struct['struct_name']
        structure_points.append(point)
        structure_types.append(struct_type)
        print(f'  {struct_type}: {point}')
    
    print(f'총 {len(structure_points)}개 구조물을 방문해야 합니다.')
    
    return structure_points, structure_types

def create_grid_map(data):
    """경로 탐색을 위한 그리드 맵을 생성하는 함수 (순수 Python)"""
    
    print('=== 그리드 맵 생성 ===')
    
    min_x, max_x = data['x'].min(), data['x'].max()
    min_y, max_y = data['y'].min(), data['y'].max()
    
    # 그리드 크기
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    
    # 순수 Python으로 2D 리스트 생성 (0: 이동 가능, 1: 이동 불가)
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(0)  # 기본값: 이동 가능
        grid.append(row)
    
    # 건설 현장은 이동 불가
    construction_sites = data[data['ConstructionSite'] == 1]
    blocked_count = 0
    
    for _, site in construction_sites.iterrows():
        grid_x = site['x'] - min_x
        grid_y = site['y'] - min_y
        grid[grid_y][grid_x] = 1  # 이동 불가
        blocked_count += 1
    
    print(f'그리드 크기: {width} x {height}')
    print(f'이동 불가 구역 (건설 현장): {blocked_count}개')
    print(f'그리드 타입: {type(grid)} (순수 Python 리스트)')
    
    return grid, min_x, min_y, max_x, max_y

def calculate_manhattan_distance(point1, point2):
    """두 점 사이의 맨하탄 거리를 계산하는 함수"""
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def bfs_distance_between_points(grid, start, end, min_x, min_y):
    """두 점 사이의 BFS 최단 거리를 계산하는 함수"""
    
    height = len(grid)
    width = len(grid[0])
    
    # 좌표를 그리드 인덱스로 변환
    start_grid = (start[0] - min_x, start[1] - min_y)
    end_grid = (end[0] - min_x, end[1] - min_y)
    
    if start_grid == end_grid:
        return 0, [start]
    
    # BFS
    queue = [(start_grid[0], start_grid[1], 0, [start_grid])]
    visited = set()
    visited.add(start_grid)
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        x, y, distance, path = queue.pop(0)
        
        if (x, y) == end_grid:
            # 실제 좌표로 변환
            actual_path = [(px + min_x, py + min_y) for px, py in path]
            return distance, actual_path
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in visited and grid[ny][nx] == 0:
                    visited.add((nx, ny))
                    new_path = path + [(nx, ny)]
                    queue.append((nx, ny, distance + 1, new_path))
    
    return float('inf'), []  # 경로를 찾을 수 없음

def find_optimized_all_structures_path(grid, start_point, structure_points, min_x, min_y):
    """보너스: 모든 구조물을 방문하는 최적화된 경로를 찾는 함수 (Greedy 알고리즘)"""
    
    print('\n=== 보너스: 모든 구조물 방문 최적화 경로 계산 ===')
    
    if not structure_points:
        return [], 0
    
    # 현재 위치에서 시작
    current_point = start_point
    unvisited = list(structure_points)  # 복사
    total_path = [start_point]
    total_distance = 0
    
    print(f'시작점: {start_point}')
    print(f'방문할 구조물: {len(unvisited)}개')
    
    # Greedy 알고리즘: 현재 위치에서 가장 가까운 구조물을 선택
    step = 1
    while unvisited:
        print(f'\n--- Step {step}: 현재 위치 {current_point} ---')
        
        # 현재 위치에서 각 미방문 구조물까지의 거리 계산
        min_distance = float('inf')
        next_point = None
        best_path = []
        
        for target in unvisited:
            distance, path = bfs_distance_between_points(grid, current_point, target, min_x, min_y)
            print(f'  {target}까지 거리: {distance}')
            
            if distance < min_distance:
                min_distance = distance
                next_point = target
                best_path = path
        
        if next_point is None:
            print('❌ 더 이상 방문할 수 있는 구조물이 없습니다!')
            break
        
        # 다음 구조물로 이동
        print(f'  → 선택: {next_point} (거리: {min_distance})')
        
        # 경로에 추가 (시작점 제외하고 추가)
        total_path.extend(best_path[1:])  # 첫 번째 요소는 현재 위치이므로 제외
        total_distance += min_distance
        
        # 상태 업데이트
        current_point = next_point
        unvisited.remove(next_point)
        step += 1
    
    print(f'\n✅ 모든 구조물 방문 완료!')
    print(f'총 경로 길이: {len(total_path)}개 지점')
    print(f'총 이동 거리: {total_distance}')
    
    return total_path, total_distance

def bfs_shortest_path(grid, start, destinations, min_x, min_y):
    """BFS 알고리즘으로 최단 경로를 찾는 함수 (4방향 이동만 허용, 순수 Python)"""
    
    print('=== BFS 최단 경로 탐색 ===')
    
    height = len(grid)
    width = len(grid[0])
    
    # 좌표를 그리드 인덱스로 변환
    start_grid = (start[0] - min_x, start[1] - min_y)
    dest_grids = [(dest[0] - min_x, dest[1] - min_y) for dest in destinations]
    
    print(f'시작 그리드 좌표: {start_grid}')
    print(f'목표 그리드 좌표들: {dest_grids}')
    
    # BFS를 위한 큐와 방문 체크 (순수 Python 리스트로 큐 구현)
    queue = [(start_grid[0], start_grid[1], 0, [start_grid])]  # (x, y, distance, path)
    visited = set()
    visited.add(start_grid)
    
    # 4방향 이동 (상하좌우만)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 상, 하, 좌, 우
    
    shortest_path = None
    shortest_distance = float('inf')
    target_dest = None
    
    while queue:
        x, y, distance, path = queue.pop(0)  # 순수 Python 리스트로 큐의 popleft() 구현
        
        # 목표 지점 중 하나에 도달했는지 확인
        if (x, y) in dest_grids:
            if distance < shortest_distance:
                shortest_distance = distance
                shortest_path = path.copy()
                target_dest = (x + min_x, y + min_y)
                print(f'목표 지점 도달: {target_dest}, 거리: {distance}')
            continue
        
        # 4방향으로 이동
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # 그리드 경계 체크
            if 0 <= nx < width and 0 <= ny < height:
                # 방문하지 않았고 이동 가능한 지점인지 확인
                if (nx, ny) not in visited and grid[ny][nx] == 0:
                    visited.add((nx, ny))
                    new_path = path + [(nx, ny)]
                    queue.append((nx, ny, distance + 1, new_path))  # 순수 Python 리스트 append
    
    if shortest_path is None:
        raise ValueError('경로를 찾을 수 없습니다!')
    
    # 그리드 좌표를 실제 좌표로 변환
    actual_path = [(x + min_x, y + min_y) for x, y in shortest_path]
    
    print(f'최단 경로 발견!')
    print(f'목표 지점: {target_dest}')
    print(f'경로 길이: {len(actual_path)}개 지점')
    print(f'총 거리: {shortest_distance}')
    
    return actual_path, target_dest, shortest_distance

def save_path_to_csv(path, filename='home_to_cafe.csv'):
    """경로를 CSV 파일로 저장하는 함수"""
    
    print(f'=== 경로를 {filename}로 저장 ===')
    
    path_df = pd.DataFrame(path, columns=['x', 'y'])
    path_df['step'] = range(1, len(path) + 1)
    path_df = path_df[['step', 'x', 'y']]  # 순서 변경
    
    path_df.to_csv(filename, index=False)
    
    print(f'경로 데이터:')
    print(path_df.head(10))
    if len(path_df) > 10:
        print(f'... (총 {len(path_df)}개 행)')
    print(f'총 {len(path)}개 지점이 {filename}에 저장되었습니다.')

def visualize_map_with_path(data, path, target_dest, filename='map_final.png', all_structures_path=None):
    """지도에 경로를 시각화하는 함수"""
    
    print('=== 지도에 경로 시각화 ===')
    
    # 맵 크기 설정
    min_x, max_x = data['x'].min(), data['x'].max()
    min_y, max_y = data['y'].min(), data['y'].max()
    
    # 시각화 설정
    fig, ax = plt.subplots(1, 1, figsize=(16, 14))
    ax.set_xlim(min_x - 0.5, max_x + 0.5)
    ax.set_ylim(min_y - 0.5, max_y + 0.5)
    ax.invert_yaxis()  # y축 뒤집기
    
    # 그리드 라인
    for x in range(min_x, max_x + 1):
        ax.axvline(x=x - 0.5, color='lightgray', linewidth=0.5, alpha=0.7)
    ax.axvline(x=max_x + 0.5, color='lightgray', linewidth=0.5, alpha=0.7)
    
    for y in range(min_y, max_y + 1):
        ax.axhline(y=y - 0.5, color='lightgray', linewidth=0.5, alpha=0.7)
    ax.axhline(y=max_y + 0.5, color='lightgray', linewidth=0.5, alpha=0.7)
    
    # 건설 현장 표시
    construction_sites = data[data['ConstructionSite'] == 1]
    for _, site in construction_sites.iterrows():
        rect = patches.Rectangle(
            (site['x'] - 0.6, site['y'] - 0.6), 1.2, 1.2,
            linewidth=1, edgecolor='gray', facecolor='lightgray', 
            alpha=0.7, zorder=1
        )
        ax.add_patch(rect)
    
    # 구조물 표시
    structures = data[data['struct_name'] != 'Empty']
    
    for _, struct in structures.iterrows():
        x, y = struct['x'], struct['y']
        struct_type = struct['struct_name']
        
        if struct_type == 'Apartment':
            circle = patches.Circle(
                (x, y), 0.25, linewidth=2, 
                edgecolor='saddlebrown', facecolor='sandybrown', 
                zorder=3
            )
            ax.add_patch(circle)
            ax.text(x, y, 'A', ha='center', va='center', fontsize=8, fontweight='bold')
            
        elif struct_type == 'Building':
            circle = patches.Circle(
                (x, y), 0.25, linewidth=2, 
                edgecolor='saddlebrown', facecolor='sandybrown', 
                zorder=3
            )
            ax.add_patch(circle)
            ax.text(x, y, 'B', ha='center', va='center', fontsize=8, fontweight='bold')
            
        elif struct_type == 'BandalgomCoffee':
            # 목표 지점 강조
            if (x, y) == target_dest:
                rect = patches.Rectangle(
                    (x - 0.3, y - 0.3), 0.6, 0.6,
                    linewidth=3, edgecolor='red', facecolor='lightgreen', 
                    zorder=5
                )
            else:
                rect = patches.Rectangle(
                    (x - 0.2, y - 0.2), 0.4, 0.4,
                    linewidth=2, edgecolor='darkgreen', facecolor='lightgreen', 
                    zorder=4
                )
            ax.add_patch(rect)
            ax.text(x, y, 'C', ha='center', va='center', fontsize=8, fontweight='bold', color='darkgreen')
            
        elif struct_type == 'MyHome':
            # 시작점 강조
            triangle = patches.Polygon(
                [(x, y - 0.3), (x - 0.26, y + 0.2), (x + 0.26, y + 0.2)],
                linewidth=3, edgecolor='blue', facecolor='lightgreen', 
                zorder=5
            )
            ax.add_patch(triangle)
            ax.text(x, y, 'H', ha='center', va='center', fontsize=8, fontweight='bold', color='blue')
    
    # 기본 경로 그리기 (빨간 선)
    if len(path) > 1:
        path_x = [point[0] for point in path]
        path_y = [point[1] for point in path]
        
        ax.plot(path_x, path_y, 'r-', linewidth=3, alpha=0.8, zorder=6, label='Shortest Path to Coffee')
        
        # 경로 지점들 표시 (작은 원)
        for i, (x, y) in enumerate(path):
            if i == 0:  # 시작점
                ax.plot(x, y, 'bo', markersize=8, zorder=7)
            elif i == len(path) - 1:  # 도착점
                ax.plot(x, y, 'ro', markersize=8, zorder=7)
            else:  # 중간 지점
                ax.plot(x, y, 'r.', markersize=4, zorder=7)
    
    # 보너스: 모든 구조물 방문 경로 그리기 (파란 선)
    if all_structures_path and len(all_structures_path) > 1:
        all_path_x = [point[0] for point in all_structures_path]
        all_path_y = [point[1] for point in all_structures_path]
        
        ax.plot(all_path_x, all_path_y, 'b-', linewidth=2, alpha=0.6, zorder=5, 
                linestyle='--', label='All Structures Path (Bonus)')
        
        # 방문 순서 표시
        for i, (x, y) in enumerate(all_structures_path[::5]):  # 5개마다 표시
            ax.text(x + 0.1, y + 0.1, str(i*5+1), fontsize=6, color='blue', fontweight='bold')
    
    # 좌표 레이블
    ax.set_xticks(range(min_x, max_x + 1))
    ax.set_yticks(range(min_y, max_y + 1))
    
    # 제목 및 범례
    title = 'Shortest Path from My Home to Bandalcom Coffee'
    if all_structures_path:
        title += ' + All Structures Path (Bonus)'
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('X Coordinate', fontsize=12)
    ax.set_ylabel('Y Coordinate', fontsize=12)
    
    # 범례
    legend_elements = [
        patches.Patch(color='lightgray', label='Construction Site (Blocked)'),
        patches.Patch(color='sandybrown', label='Apartment (A) / Building (B)'),
        patches.Patch(color='lightgreen', label='Bandalcom Coffee (C)'),
        patches.Patch(color='lightgreen', label='My Home (H)'),
        patches.Patch(color='red', label='Shortest Path to Coffee')
    ]
    
    if all_structures_path:
        legend_elements.append(patches.Patch(color='blue', label='All Structures Path (Bonus)'))
    
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.2, 1))
    
    # 경로 정보 텍스트
    path_info = f"""Path Info:
Basic Path Steps: {len(path)}
Basic Distance: {len(path)-1}
Destination: {target_dest}"""
    
    if all_structures_path:
        path_info += f"""

Bonus - All Structures:
Total Steps: {len(all_structures_path)}
Total Distance: {len(all_structures_path)-1}"""
    
    ax.text(0.02, 0.02, path_info, transform=ax.transAxes, 
            verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # 이미지 저장
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f'경로가 시각화된 지도가 \'{filename}\' 파일로 저장되었습니다.')
    
    plt.show()

def main():
    """메인 함수"""
    try:
        # 1. 데이터 로드
        data = load_and_prepare_data()
        
        # 2. 시작점과 도착점 찾기
        start_point, destinations = find_start_and_destinations(data)
        
        # 3. 보너스: 모든 구조물 찾기
        all_structure_points, structure_types = find_all_structures(data)
        
        # 4. 그리드 맵 생성
        grid, min_x, min_y, max_x, max_y = create_grid_map(data)
        
        # 5. 기본: BFS로 최단 경로 탐색 (집 → 가장 가까운 커피숍)
        shortest_path, target_dest, distance = bfs_shortest_path(grid, start_point, destinations, min_x, min_y)
        
        # 6. 보너스: 모든 구조물을 방문하는 최적화된 경로
        all_structures_path, all_structures_distance = find_optimized_all_structures_path(
            grid, start_point, all_structure_points, min_x, min_y)
        
        # 7. 기본 경로를 CSV로 저장
        save_path_to_csv(shortest_path, 'home_to_cafe.csv')
        
        # 8. 보너스 경로를 CSV로 저장
        if all_structures_path:
            save_path_to_csv(all_structures_path, 'home_to_all_structures.csv')
        
        # 9. 지도에 두 경로 모두 시각화
        visualize_map_with_path(data, shortest_path, target_dest, 'map_final.png', all_structures_path)
        
        print('\n' + '=' * 60)
        print('✅ 최단 경로 탐색 완료 (기본 + 보너스)')
        print('=' * 60)
        print('🏠 기본 경로 (집 → 가장 가까운 커피숍):')
        print(f'  시작점: {start_point}')
        print(f'  도착점: {target_dest}')
        print(f'  경로 길이: {len(shortest_path)}개 지점')
        print(f'  총 이동 거리: {distance}')
        print('  결과 파일: home_to_cafe.csv')
        
        if all_structures_path:
            print(f'\n🏢 보너스 경로 (모든 구조물 방문):')
            print(f'  시작점: {start_point}')
            print(f'  방문 구조물: {len(all_structure_points)}개')
            print(f'  경로 길이: {len(all_structures_path)}개 지점')
            print(f'  총 이동 거리: {all_structures_distance}')
            print('  결과 파일: home_to_all_structures.csv')
        
        print(f'\n📁 시각화 파일: map_final.png')
        
    except Exception as e:
        print(f'❌ 오류 발생: {e}')

if __name__ == '__main__':
    main() 
