build python container image best practice
==============================================================================
本项目是我在生产项目中总结的构建 Python 应用容器镜像的最佳实践. 其中包含了:

- 用 poetry 保障依赖是确定的, 不随时间变化的, immutable 的.
- 对容器中的 app 进行单元测试, 防止能在本地运行, 但因容器中缺少某些系统依赖导致无法运行的情况.
- 使用多阶段构建, 在最终的镜像中只包含所必须得依赖和源码.
- 处理需要编译的依赖例如 pandas, polars 的情况.

我给出了两个示例项目, 一个是用来部署纯 Python 应用的, 一个是用来部署包含需要编译的依赖的 Python 应用的 (通常是数据处理, 加密解密等).

- `alpine <./alpine/README.rst>`_
- `slim <./slim/README.rst>`_
