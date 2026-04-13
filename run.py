import uvicorn


def main():
    """启动AiMenu API服务"""

    print("🍽️ AiMenu 智能点餐系统 v2.0")
    print("=" * 50)

    print("✅ 环境配置检查通过")
    print("🚀 正在启动API服务...")
    print("📍 服务地址: http://localhost:8000")
    print("📖 API文档: http://localhost:8000/docs")
    print("=" * 50)

    # 启动服务
    try:
        uvicorn.run(
            "api.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,  # 开发模式，文件变化时自动重启
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")


if __name__ == "__main__":
    main()