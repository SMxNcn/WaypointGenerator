import json
import os

def parse_coord(s):
    """解析 'x,y,z' 字符串为元组 (x, y, z)"""
    try:
        parts = s.strip().split(',')
        if len(parts) != 3:
            raise ValueError
        return int(parts[0]), int(parts[1]), int(parts[2])
    except:
        raise ValueError("坐标格式错误，请使用 x,y,z 格式（整数）")

def parse_action_keys(s, mode='other'):
    """
    解析按键字符串为 Action 字典，包含互斥检查。
    W/S 互斥, A/D 互斥。
    """
    action = {}
    s = s.upper().strip()
    
    # 提取有效键
    has_w = 'W' in s
    has_s = 'S' in s
    has_a = 'A' in s
    has_d = 'D' in s
    has_l = 'L' in s
    
    # 互斥检查
    if has_w and has_s:
        print("⚠️  警告: W 和 S 互斥，已自动忽略两者。")
        has_w = False
        has_s = False
        
    if has_a and has_d:
        print("⚠️  警告: A 和 D 互斥，已自动忽略两者。")
        has_a = False
        has_d = False

    # 构建 Action
    if has_w: action['forward'] = True
    if has_s: action['back'] = True
    if has_a: action['left'] = True
    if has_d: action['right'] = True
    
    # Flower 模式默认全程左键，Other 模式由用户决定
    if has_l or mode == 'flower':
        action['leftClick'] = True
        
    return action

def action_to_json(action):
    """Gson 优化：只保留值为 true 的字段"""
    return {k: v for k, v in action.items() if v}

def save_to_output(filename, waypoints):
    """保存 JSON 到执行目录下的 output 文件夹"""
    output_dir = os.path.join(os.getcwd(), "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filepath = os.path.join(output_dir, filename)
    if not filepath.endswith('.json'):
        filepath += '.json'
        
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(waypoints, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 已生成 {len(waypoints)} 个路径点到: {filepath}")
    return filepath