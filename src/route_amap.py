import folium
from folium import plugins
import webbrowser
import requests
import json
import urllib3

# 禁用SSL验证警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 高德地图API配置
AMAP_KEY = "AMAP_KEY"
AMAP_POI_URL = "AMAP_KEY"
AMAP_ROUTE_URL = "AMAP_KEY"

def get_location_by_poi(keywords, city="潮州市"):
    """使用高德地图POI搜索API获取位置信息"""
    params = {
        'key': AMAP_KEY,
        'keywords': keywords,
        'city': city,
        'extensions': 'all'
    }
    
    try:
        response = requests.get(AMAP_POI_URL, params=params, verify=False)
        data = response.json()
        
        if data['status'] == '1' and data['pois']:
            poi = data['pois'][0]  # 获取第一个匹配结果
            location = poi['location'].split(',')
            return {
                'name': poi['name'],
                'address': poi['address'],
                'location': [float(location[1]), float(location[0])]  # 转换为[纬度, 经度]
            }
        return None
    except Exception as e:
        print(f"获取位置信息时出错: {str(e)}")
        return None

def create_route_between_schools():
    # 创建地图，中心点设置在潮州市
    m = folium.Map(location=[23.6617, 116.6307], zoom_start=14, tiles='OpenStreetMap')

    # 添加高德卫星图层
    folium.TileLayer(
        tiles='https://webst01.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}',
        attr='高德卫星图',
        name='Satellite',
        overlay=True
    ).add_to(m)

    # 添加图层控制
    folium.LayerControl().add_to(m)

    # 定义起点和终点
    locations = {
        "起点": "韩山师范学院南一区文科楼",
        "终点": "韩山师范学院韩东校区"
    }

    try:
        # 使用高德地图POI搜索获取位置信息
        coordinates = {}
        for name, keywords in locations.items():
            location_info = get_location_by_poi(keywords)
            if location_info:
                coordinates[name] = location_info
                # 添加标记
                folium.Marker(
                    location_info['location'],
                    popup=f"{location_info['name']}<br>{location_info['address']}",
                    icon=folium.Icon(color='red' if name == "起点" else 'green', icon='info-sign')
                ).add_to(m)
            else:
                print(f"无法找到 {name} 的位置")

        if len(coordinates) == 2:
            # 构建高德地图API请求参数
            params = {
                'key': AMAP_KEY,
                'origin': f"{coordinates['起点']['location'][1]},{coordinates['起点']['location'][0]}",  # 经度,纬度
                'destination': f"{coordinates['终点']['location'][1]},{coordinates['终点']['location'][0]}",  # 经度,纬度
                'extensions': 'all',
                'strategy': 0  # 0-速度优先，不考虑路况
            }

            # 发送请求到高德地图API
            response = requests.get(AMAP_ROUTE_URL, params=params, verify=False)
            data = response.json()

            if data['status'] == '1' and data['route']:
                route_info = data['route']
                path = route_info['paths'][0]  # 获取第一条推荐路线
                
                # 解析路线坐标
                route_coords = []
                for step in path['steps']:
                    polyline = step['polyline'].split(';')
                    for point in polyline:
                        lng, lat = point.split(',')
                        route_coords.append([float(lat), float(lng)])

                # 添加路线到地图（使用更醒目的样式）
                folium.PolyLine(
                    route_coords,
                    weight=8,  # 增加线条粗细
                    color='#FF4500',  # 路线颜色（橙红色）
                    opacity=0.9,  # 增加不透明度
                    dash_array='15',  # 增加虚线间隔
                    line_cap='round',  # 线条端点样式
                    line_join='round'  # 线条连接处样式
                ).add_to(m)

                # 获取路线距离和时间
                distance_km = float(path['distance']) / 1000  # 转换为公里
                duration_min = int(path['duration']) / 60  # 转换为分钟

                # 在路线中间添加距离和时间标记
                mid_point = route_coords[len(route_coords) // 2]
                folium.Popup(
                    f"路线距离: {distance_km:.1f} 公里<br>预计时间: {duration_min:.0f} 分钟",
                    max_width=200
                ).add_to(folium.CircleMarker(
                    location=mid_point,
                    radius=10,  # 增加标记点大小
                    color='#FF4500',
                    fill=True,
                    fill_color='#FF4500',
                    fill_opacity=0.8
                ).add_to(m))

                # 添加路线动画效果
                plugins.AntPath(
                    route_coords,
                    weight=6,
                    color='#FF4500',
                    opacity=0.8,
                    delay=400
                ).add_to(m)

                # 保存地图
                m.save('潮州市学校路线图.html')
                print("地图已保存为'潮州市学校路线图.html'")

                # 自动打开地图
                webbrowser.open('潮州市学校路线图.html')
            else:
                print("无法获取路线信息")
        else:
            print("无法获取所有地点的坐标")

    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    create_route_between_schools()
    
