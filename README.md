# Waypoint Generator

为 [NecronClient-Fabric](https://github.com/SMxNcn/NecronClient-Fabric) 交互式生成农场路径点文件的工具


## 下载与运行

### 普通用户（下载 exe）

1. 前往 [Releases](https://github.com/SMxNcn/WaypointGenerator/releases) 下载最新版 `.exe`
2. 双击运行，按提示输入信息

### 运行源代码
```bash
git clone https://github.com/SMxNcn/WaypointGenerator.git
cd WaypointGenerator
python main.py
```

## 输出与使用

生成的 .json 文件位于运行目录下的 output/ 文件夹。

### 放入游戏目录：

无版本隔离：.minecraft/config/necron/waypoints/

有版本隔离（如 MultiMC、官方启动器开启版本隔离）：.minecraft/versions/<版本名>/config/necron/waypoints/

### 游戏内加载：

详见 [FARMING.md](https://github.com/SMxNcn/NecronClient-Fabric/blob/master/FARMING.md)