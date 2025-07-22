import pandas as pd

def analysis_data():
  category_df = pd.read_csv('./area_category.csv')
  map_df = pd.read_csv('./area_map.csv')
  struct_df = pd.read_csv('./area_struct.csv')

  category_df.columns = category_df.columns.str.strip()
  map_df.columns = map_df.columns.str.strip()
  struct_df.columns = struct_df.columns.str.strip()

  structCategory_df = struct_df.merge(category_df, on='category', how='left')
  categoryMap_df = structCategory_df.merge(map_df, on=['x', 'y'], how='left')

  cols = ['area', 'x', 'y', 'category', 'struct', 'ConstructionSite']
  wholeData_df = categoryMap_df.sort_values('area')[cols]

  return wholeData_df

wholeData_df = analysis_data()

def filtering_area1(df):
  area1_df = df[df['area'] == 1]

  return area1_df

area1_df = filtering_area1(wholeData_df)
print('===== area1의 데이터 =====')
print(area1_df)

def struct_stats(df):
  print(df['struct'].value_counts())

print('===== 구조물 종류별 요약 통계 =====')
struct_stats(wholeData_df)