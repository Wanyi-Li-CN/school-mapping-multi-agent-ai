import folium
import requests
import json
import math
import ssl
import urllib3
from folium import plugins
import geopandas as gpd
from shapely.geometry import box

# 禁用SSL验证警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 高德地图API配置
AMAP_KEY = "##"
AMAP_URL = "##"

city = "揭阳"
gdf_file = city+'市'+'_市.geojson'

def get_schools_in_chaozhou():
    # 使用高德地图POI搜索API获取潮州市的中学
    params = {
        'key': AMAP_KEY,
        'keywords': '中学',
        'city': city,
        'offset': 50,  # 每页记录数
        'page': 1,     # 页码
        'extensions': 'all'
    }
    
    all_schools = []
    while True:
        # 禁用SSL验证
        response = requests.get(AMAP_URL, params=params, verify=False)
        data = response.json()
        
        if data['status'] == '1' and data['pois']:
            all_schools.extend(data['pois'])
            if len(data['pois']) < params['offset']:
                break
            params['page'] += 1
        else:
            break
    
    return all_schools

def create_mask_geojson(gdf):
    # 获取潮州市边界的外接矩形
    bounds = gdf.total_bounds
    # 创建一个大的矩形作为遮罩
    world = box(bounds[0] - 1, bounds[1] - 1, bounds[2] + 1, bounds[3] + 1)
    # 从大矩形中减去潮州市区域
    mask = world.difference(gdf.unary_union)
    # 转换为GeoJSON格式
    return json.loads(gpd.GeoSeries([mask]).to_json())

def create_map(schools):
    # 读取潮州市边界数据
    gdf = gpd.read_file(gdf_file)
    bounds = gdf.total_bounds
    
    # 计算地图中心点
    center_lat = (bounds[1] + bounds[3]) / 2
    center_lon = (bounds[0] + bounds[2]) / 2
    
    # 创建地图
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=11,
        tiles='https://webst01.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}',
        attr='高德卫星图',
        max_bounds=True,  # 限制地图边界
        min_zoom=10,      # 最小缩放级别
        max_zoom=18       # 最大缩放级别
    )
    
    # 添加遮罩层
    mask_geojson = create_mask_geojson(gdf)
    folium.GeoJson(
        mask_geojson,
        style_function=lambda x: {
            'fillColor': 'black',
            'color': 'black',
            'weight': 0,
            'fillOpacity': 1
        }
    ).add_to(m)
    
    # 添加潮州市边界
    folium.GeoJson(
        gdf,
        style_function=lambda x: {
            'fillColor': 'none',
            'color': 'red',
            'weight': 2,
            'fillOpacity': 0
        }
    ).add_to(m)
    
    # 设置地图边界
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

    # 添加学校标记
    for school in schools:
        location = school['location'].split(',')
        lat = float(location[1])
        lon = float(location[0])
        name = school['name']
        
        # 创建自定义图标
        icon = folium.DivIcon(
            html=f"""
            <div style="
                background-color: rgba(255, 0, 0, 0.7);
                border-radius: 50%;
                width: 8px;
                height: 8px;
                position: relative;
            ">
                <div style="
                    position: absolute;
                    top: -20px;
                    left: 10px;
                    color: white;
                    font-size: 12px;
                    font-weight: bold;
                    text-shadow: 1px 1px 2px black;
                    white-space: nowrap;
                ">{name}</div>
            </div>
            """
        )
        
        # 创建弹出信息
        popup_text = f"""
        <b>{name}</b><br>
        地址: {school.get('address', '未知')}<br>
        电话: {school.get('tel', '未知')}<br>
        类型: {school.get('type', '中学')}
        """
        
        # 添加标记
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_text, max_width=300),
            icon=icon
        ).add_to(m)

    # 保存地图
    m.save(city+'_schools_map.html')

def main():
    print("正在获取"+city+"市中学数据...")
    schools = get_schools_in_chaozhou()
    print(f"找到 {len(schools)} 所学校")
    
    print("正在创建地图...")
    create_map(schools)
    print("地图已保存为 "+city+"_schools_map.html")

if __name__ == "__main__":
    main() 