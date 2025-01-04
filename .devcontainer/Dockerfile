FROM nvidia/cuda:12.6.3-runtime-ubuntu22.04

RUN cp /etc/apt/sources.list /etc/apt/sources.list.bk
RUN cat > /etc/apt/sources.list <<EOF
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse
# deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
# deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
# deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse

# 以下安全更新软件源包含了官方源与镜像站配置，如有需要可自行修改注释切换
deb http://security.ubuntu.com/ubuntu/ jammy-security main restricted universe multiverse
# deb-src http://security.ubuntu.com/ubuntu/ jammy-security main restricted universe multiverse

# 预发布软件源，不建议启用
# deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-proposed main restricted universe multiverse
# # deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-proposed main restricted universe multiverse
EOF

RUN apt-get update \
    && apt-get install -y git vim curl wget \
        python3 python3-pip \
        python3-venv

# if country is CN, replace the mirror
RUN if [ "$COUNTRY" = "CN" ]; then \
        git clone https://github.com/Homqyy/china-mirror \
        && bash china-mirror/pypi.sh; \
    fi

# cleanup
RUN if [ "$COUNTRY" = "CN" ]; then \
        rm -rf china-mirror; \
    fi

RUN pip install --upgrade pip \
RUN pip install datasets transformers sentencepiece modelscope[framework] \
    torch torchvision torchaudio