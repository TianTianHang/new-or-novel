from flask import jsonify

from factory import create_app

app = create_app()


@app.route('/')
def index():
    return 'yes'


@app.after_request
def format_response(response):
    # 检查响应是否是JSON格式
    if not response.is_json:
        return response
    # 获取原始的响应数据
    data = response.get_json()

    # 检查响应是否包含符合格式的字段
    if data and all(key in data for key in ["code", "message", "data"]):
        return response

    # 如果不符合格式，进行格式化

    # 默认响应信息
    code = response.status_code
    message = response.status
    if data:
        # 提取数据和消息（如果存在）
        code = data.get("code", code)

        if "message" in data:
            message = data["message"]
        elif "msg" in data:
            message = data["msg"]
        data = data.get("data", None)

    # 格式化为JSON响应
    response_data = {
        "code": code,
        "message": message,
        "data": data
    }

    # 更新响应内容
    response.data = jsonify(response_data).data
    return response


if __name__ == '__main__':
    app.run()
