构建包含 C 依赖的 Python 容器镜像
==============================================================================


1. 纯 Python 本地开发
------------------------------------------------------------------------------
我们先不要急着上容器, 首先你要保证你的代码在本地能跑通, 测试没问题. 在本例中我们的 App 有两个函数:

- ``show_deps`` 打印了 polars (数据处理包, 由 rust 实现, 有 C 依赖) 的版本, 用于确认 polars 可以成功运行
- ``say_hello`` 根据人名打印字符串.

通常用容器部署的 Python app 都需要一个 CLI 接口来运行底层的 Python 函数. 这里我们的 ``my_project/cli.py`` 模块利用了谷歌出品的命令行工具 `python-fire <https://github.com/google/python-fire>`_ 将我们的函数包装成了命令行工具. 然后再用 ``main.py`` 作为入口脚本对我们的源码进行包装.


.. codeblock:: bash

    # 创建虚拟环境
    virtualenv -p python3.9 .venv

    # 激活虚拟环境
    source .venv/bin/activate

    # 使用 poetry 进行确定性的包管理
    pip install poetry

    # 解析依赖的版本
    poetry lock

    # 安装核心依赖
    poetry install

    # 安装测试所需依赖
    poetry install --with test

    # 进行测试
    pytest -s --tb=native --cov=my_project --cov-report term-missing --cov-report html:htmlcov tests

    # 用 CLI 进行本地测试
    python main.py
    python main.py show-deps
    python main.py say-hello --name alice

    # 测试通过后, 将核心依赖和测试依赖输出为 requirements.txt 文件, 以供 pip 安装
    poetry export -f requirements.txt --output requirements.txt
    poetry export -f requirements.txt --only test --output requirements-test.txt

至此, 你可以确定你的代码已经被充分测试过了, 可以构建容器镜像了.


2. 探索基础镜像
------------------------------------------------------------------------------
刚开始拿到一个基础镜像, 先不要急着开始写 Dockerfile. 因为你对这个镜像里面到底有什么, 目录结构是怎样的还不是很清楚. 我推荐用守护态运行模式, 然后用伪终端进入到容器里面, 在里面手动输入命令实验一次. 实验成功后再将打过的命令再转换成 Dockerfile 的格式.

本例中我们用的是 slim 镜像. 因为我们有一些需要 C 依赖才能跑的包 (polars), 所以不能用 Alpine.

.. codeblock:: bash

    # 在本地以守护态运行, 并开启一个伪终端, 给容器命名为 dev, 并且在结束后自动销毁
    # 详情请参考镜像的官方文档 https://gallery.ecr.aws/docker/library/python
    docker run --rm -dt --name dev public.ecr.aws/docker/library/python:3.9-slim

    # 进入容器的 bash, 按 ctrl + D 可退出
    docker exec -it dev bash

    # 关闭容器
    docker container stop dev


3. 使用 multi-stage 技术进行容器构建
------------------------------------------------------------------------------
请详细阅读 `Dockerfile <./Dockerfile>`_ 中的注释, 理解构建是如何实现的, 如何测试你的容器, 以及如何优化镜像的大小. 最终我们的镜像有 188 MB. 其中基础镜像占了 128 MB, Python 依赖 (主要是 Polars
) 占据了 58 MB.

.. codeblock:: bash

    # 构建你的镜像
    docker build -t my_project:latest .

    # 在本地运行一下你的镜像
    docker run --rm my_project:latest
    docker run --rm my_project:latest show-deps --help
    docker run --rm my_project:latest show-deps
    docker run --rm my_project:latest say-hello --help
    docker run --rm my_project:latest say-hello --name alice

你可能还需要下面的命令清理没用的镜像和容器:

.. codeblock:: bash

    # 列出所有镜像
    docker image ls
    # 删除指定镜像 (通常是那些没有 Tag 的)
    docker image rm ${id}

    # 列出所有容器 (包括已经停止的)
    docker container ls -a
    # 停止指定容器 (通常是那些以守护态运行着的)
    docker container stop ${id}
    # 删除指定容器
    docker container rm ${id}

    # 删除所有镜像, 容器, 缓存等
    docker system prune -a
