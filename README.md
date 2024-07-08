# 用于搜索建筑和景观项目的AI Agent的简单演示

本项目来源于模版[search_and_chat](https://github.com/langchain-ai/streamlit-agent/blob/main/streamlit_agent/search_and_chat.py)，配置[Exa](https://dashboard.exa.ai/)工具以进行建筑景观相关网站的搜索，专用于检索建筑和景观项目、基于 [Streamlit](https://streamlit.io/) 的聊天应用。

![](https://oss.renhai.online/halo/2024/07/548acc4af083defb2699ac94bac2be68.png)



> 来源网站包含："mooool.com", "gooood.cn", "baike.baidu.com",  "mooool.com", "archiposition.com", "archdaily.cn", "arch-exist.com", "tlaidesign.com", "hhlloo.com"



### 环境配置参考

1. **克隆仓库:**

   ```shell
   git clone https://github.com/renhai-lab/streamli-agent.git
   cd streamli-agent
   ```

2. **配置环境变量:**

   ```shell
   cp .env.example .env
   ```

   在 `.env` 文件中填写相应的 API 密钥等信息。

3. **使用 Conda 创建虚拟环境:**

   ```shell
   # install
   conda env create -f environment.yaml
   # reinstall
   # conda env create --file environment.yaml --force
   # update
   # conda env update --file environment.yaml
   ```

4. **运行项目:**

   ```shell
   streamlit run streamlit_agent/search_and_chat.py
   ```

   这将在浏览器中打开应用。



**注意:**

- 请确保已安装 `conda`。你也可以用其他环境管理方式。
- 推荐使用 `environment.yaml` 和 `conda` 进行环境管理.