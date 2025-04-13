# -*- coding: utf-8 -*-
from nonebot import on_command
from nonebot import require
from typing import Optional, Dict, Any, Union
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.params import CommandArg
import httpx  
from jinja2 import  Environment, FileSystemLoader
import os
import base64
require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import html_to_pic
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="bfvservermap",
    description="查询服务器地图信息",
    usage="map<服务器名称>",
    homepage="https://github.com/LLbuxudong/nonebot-plugin-bfvservermap",
    type={"application"},
    supported_adapters={"~onebot.v11"}
    )

servermessage = on_command("map", aliases={"地图,map="}, priority=5, block=True)

# 异步请求 JSON 数据
async def fetch_json(url: str, timeout: int = 20) -> Optional[Dict[str, Any]]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=timeout)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"请求失败，状态码: {response.status_code}, 响应内容: {response.text}"}
    except httpx.RequestError as e:
        return {"error": f"请求发生错误: {e}"}

# 获取服务器列表信息
async def get_server(servername: str) -> Optional[Dict[str, Any]]:
    server_url = f"https://api.gametools.network/bfv/servers/?name={servername}&platform=pc&limit=5&region=all&lang=zh-CN"
    data = await fetch_json(server_url)
    return data

# 获取服务器详细信息
async def get_server_info(servername_detail: str) -> Optional[Dict[str, Any]]:
    server_url = f"https://api.gametools.network/bfv/detailedserver/?name={servername_detail}&platform=pc&lang=zh-CN"
    data = await fetch_json(server_url)
    return data

@servermessage.handle()
async def handle_server(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    server_name = arg.extract_plain_text().strip()
    
    if not server_name:
        await servermessage.finish("请输入要查询的服务器名称")
    else:
        serverlistdata = await get_server(server_name)
        
        if "error" in serverlistdata:
            await servermessage.finish(f"查询服务器信息失败: {serverlistdata['error']}")
        
        servers = serverlistdata.get("servers", [])
        
        if not servers:
            await servermessage.finish(f"未找到包含{server_name}的服务器信息，请检查服务器名称是否正确")

        prefix_data = []  # 存储服务器列表
        for server in servers:
            prefix = server.get("prefix")
            if prefix and server_name.lower() in prefix.lower():  # 匹配服务器名 将用户输入的服务器名称和服务器前缀都转换为小写，然后检查用户输入的名称是否包含在服务器前缀中。
                prefix_data.append(prefix)
        
        if len(prefix_data) == 1:  # 查询该服务器的详细信息
            servername = prefix_data[0]  # 只有一个服务器，赋值给servername
            serverdata_detail = await get_server_info(servername)
            if "error" in serverdata_detail:
                await servermessage.finish(f"查询服务器信息失败: {serverdata_detail['error']}")
            else:  # 获取到的详细数据为serverdata_detail
                rendering_message = await servermessage.send("亚托利成功找到信息了哦，正在渲染图片给主人😊")
                rendering_message_id = rendering_message["message_id"]
                
                # 提取字段信息
                player_amount = serverdata_detail.get('playerAmount', 'N/A')
                max_player_amount = serverdata_detail.get('maxPlayerAmount', 'N/A')
                in_queue = serverdata_detail.get('inQueue', 'N/A')
                prefix = serverdata_detail.get('prefix', 'N/A')
                description = serverdata_detail.get('description', '无描述')
                current_map = serverdata_detail.get('currentMap', 'N/A')
                current_map_image = serverdata_detail.get('currentMapImage', 'N/A')
                country = serverdata_detail.get('country', 'N/A')
                mode = serverdata_detail.get('mode', 'N/A')
                game_id = serverdata_detail.get('gameId', 'N/A')
                owner_name = serverdata_detail.get('owner', {}).get('name', 'N/A')
                teams = serverdata_detail.get('teams', {})
                rotation_info = serverdata_detail.get('rotation', [])
                description = serverdata_detail.get('description', '无描述')

                # 获取背景图片的绝对路径
                template_path = os.path.dirname(__file__)  # 获取当前文件所在目录
                background_image_path = os.path.join(template_path, 'background-image.jpg')
                
                # 将背景图片转换为Base64编码
                with open(background_image_path, 'rb') as image_file:
                    background_image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
                
                # 构建模板参数
                template_params = {
                    "player_amount": player_amount,
                    "max_player_amount": max_player_amount,
                    "in_queue": in_queue,
                    "prefix": prefix,
                    "description": description,
                    "current_map": current_map,
                    "current_map_image": current_map_image,
                    "country": country,
                    "mode": mode,
                    "game_id": game_id,
                    "owner_name": owner_name,
                    "teams": teams,
                    "rotation_info": rotation_info,
                    "description": description,
                    "background_image": f"data:image/jpeg;base64,{background_image_base64}"  # 传递Base64编码的背景图片
                }

                # 读取并渲染模板
                env = Environment(loader=FileSystemLoader(template_path))
                template = env.get_template('server_template.html')
                html_content = template.render(template_params)

                # 渲染HTML并生成图像
                image_path = await html_to_pic(
                    html=html_content,
                    viewport={"width": 500, "height": 250},
                    wait=2,
                    type="png",
                    device_scale_factor=2
                )

                # 撤回正在渲染图片的消息
                await bot.delete_msg(message_id=rendering_message_id)
                
                # 发送图片
                await bot.send(event, MessageSegment.image(image_path))

        elif len(prefix_data) > 1:
            servernamelist_all = "\n".join(prefix_data[:5])  # 显示最多5个服务器
            await servermessage.finish(f"查询到服务器列表(最多显示5个)：\n{servernamelist_all}\n当前查询到的服务器较多，请输入准确的服务器名称")