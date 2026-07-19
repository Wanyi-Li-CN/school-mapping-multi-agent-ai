import folium
import osmnx as ox
from geopy.geocoders import Nominatim
import networkx as nx
from folium import plugins
import webbrowser
import osmnx as ox
from osmnx import utils_graph


def create_route_between_schools():
    # 创建地图，中心点设置在潮州市
    m = folium.Map(location=[23.6617, 116.6307], zoom_start=14, tiles='OpenStreetMap')

    # 添加卫星图层
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite',
        overlay=True
    ).add_to(m)

    # 添加图层控制
    folium.LayerControl().add_to(m)

    # 定义起点和终点
    locations = {
        "金山中学": "潮州市金山中学",
        "阳光实验学校": "潮州市湘桥区阳光实验学校"
    }

    # 使用Nominatim进行地理编码
    geolocator = Nominatim(user_agent="my_agent")

    try:
        # 获取所有地点的坐标
        coordinates = {}
        for name, address in locations.items():
            location = geolocator.geocode(address)
            if location:
                coordinates[name] = (location.latitude, location.longitude)
                # 添加标记
                folium.Marker(
                    [location.latitude, location.longitude],
                    popup=name,
                    icon=folium.Icon(color='red' if name == "金山中学" else 'green', icon='info-sign')
                ).add_to(m)
            else:
                print(f"无法找到 {name} 的位置")

        if len(coordinates) == 2:
            # 获取路线网络
            G = ox.graph_from_place("潮州市", network_type="drive")

            # 找到最近的节点
            start_node = ox.nearest_nodes(G, coordinates["金山中学"][1], coordinates["金山中学"][0])
            end_node = ox.nearest_nodes(G, coordinates["阳光实验学校"][1], coordinates["阳光实验学校"][0])

            # 计算最短路径
            route = nx.shortest_path(G, start_node, end_node, weight='length')

            # 获取路线坐标
            route_coords = []
            for node in route:
                route_coords.append([G.nodes[node]['y'], G.nodes[node]['x']])

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

            # 计算路线总长度
            route_length = sum(ox.utils_graph.get_route_edge_attributes(G, route, 'length'))
            distance_km = route_length / 1000  # 转换为公里

            # 在路线中间添加距离标记
            mid_point = route_coords[len(route_coords) // 2]
            folium.Popup(
                f"路线距离: {distance_km:.1f} 公里",
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
            print("无法获取所有地点的坐标")

    except Exception as e:
        print(f"发生错误: {str(e)}")


if __name__ == "__main__":
    create_route_between_schools()
    