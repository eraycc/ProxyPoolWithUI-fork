FROM python:3.7.0

WORKDIR /proxy

# 复制依赖文件
COPY requirements.txt .

# 设置pip源并安装依赖
RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
    && pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

# 复制所有源代码到工作目录
COPY . .

CMD ["python", "main.py"]
