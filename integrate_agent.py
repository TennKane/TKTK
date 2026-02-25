import os
import shutil
import subprocess
import time
import re

# Configuration
SOURCE_DIR = r"D:\Desktop\后端\SuperBizAgent-release-2026-01-02"
DEST_ROOT = r"F:\借鉴\Video"
MODULE_NAME = "tktk-agent"
DEST_DIR = os.path.join(DEST_ROOT, MODULE_NAME)

# Dates
DATES = [
    "2026-02-25 10:30:00 +0800",
    "2026-02-26 14:20:00 +0800",
    "2026-02-28 09:15:00 +0800",
    "2026-03-01 16:45:00 +0800",
    "2026-03-03 11:10:00 +0800",
    "2026-03-04 15:30:00 +0800"
]

def run_git_cmd(args, cwd=DEST_ROOT, env=None):
    if env is None:
        env = os.environ.copy()
    subprocess.run(["git"] + args, cwd=cwd, env=env, check=True)

def git_commit(message, date_str):
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    run_git_cmd(["add", "."], env=env)
    try:
        run_git_cmd(["commit", "-m", message], env=env)
    except subprocess.CalledProcessError:
        print(f"Nothing to commit for {message}")

def replace_in_file(file_path, old, new):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = content.replace(old, new)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def regex_replace_in_file(file_path, pattern, replacement):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE|re.DOTALL)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

# --- Stage 1: Initialize ---
def stage_1():
    print("Stage 1: Copying files...")
    if os.path.exists(DEST_DIR):
        shutil.rmtree(DEST_DIR)
    
    # Copy ignoring .git and target
    shutil.copytree(SOURCE_DIR, DEST_DIR, ignore=shutil.ignore_patterns('.git', 'target', '.idea'))
    
    # Clean up any potential git repo inside
    if os.path.exists(os.path.join(DEST_DIR, ".git")):
        shutil.rmtree(os.path.join(DEST_DIR, ".git"))

    git_commit("Feat: Initialize tktk-agent module from SuperBizAgent release", DATES[0])

# --- Stage 2: Prune AIOps ---
def stage_2():
    print("Stage 2: Pruning AIOps...")
    
    # Delete files
    files_to_delete = [
        "src/main/java/org/example/service/AiOpsService.java",
        "src/main/java/org/example/agent/tool/QueryMetricsTools.java",
        "src/main/java/org/example/agent/tool/QueryLogsTools.java",
        "src/main/java/org/example/controller/MilvusCheckController.java", 
    ]
    dirs_to_delete = [
        "aiops-docs"
    ]
    
    for f in files_to_delete:
        p = os.path.join(DEST_DIR, f)
        if os.path.exists(p):
            os.remove(p)
            
    for d in dirs_to_delete:
        p = os.path.join(DEST_DIR, d)
        if os.path.exists(p):
            shutil.rmtree(p)

    # Modify ChatService.java
    chat_service = os.path.join(DEST_DIR, "src/main/java/org/example/service/ChatService.java")
    
    # Remove fields (robust regex)
    regex_replace_in_file(chat_service, r'@Autowired\s+private QueryMetricsTools queryMetricsTools;', '')
    # Match Autowired with optional required=false and comments
    regex_replace_in_file(chat_service, r'@Autowired\(required = false\).*?private QueryLogsTools queryLogsTools;', '')
    
    regex_replace_in_file(chat_service, r'import org\.example\.agent\.tool\.QueryLogsTools;', '')
    regex_replace_in_file(chat_service, r'import org\.example\.agent\.tool\.QueryMetricsTools;', '')
    
    # Update buildMethodToolsArray
    regex_replace_in_file(chat_service, 
                          r'public Object\[\] buildMethodToolsArray\(\) \{.*?\}', 
                          'public Object[] buildMethodToolsArray() {\n        return new Object[]{dateTimeTools, internalDocsTools};\n    }')
    
    # Update buildSystemPrompt
    regex_replace_in_file(chat_service, r'systemPromptBuilder\.append\("当用户需要查询 Prometheus.*?"\);', '')
    regex_replace_in_file(chat_service, r'systemPromptBuilder\.append\("当用户需要查询腾讯云日志.*?"\);', '')
    regex_replace_in_file(chat_service, r'以及查询 Prometheus 告警信息。', '。')

    # Modify ChatController.java
    chat_controller = os.path.join(DEST_DIR, "src/main/java/org/example/controller/ChatController.java")
    regex_replace_in_file(chat_controller, r'@Autowired\s+private AiOpsService aiOpsService;', '')
    regex_replace_in_file(chat_controller, r'import org\.example\.service\.AiOpsService;', '')

    # Clean application.yml
    app_yml = os.path.join(DEST_DIR, "src/main/resources/application.yml")
    # Remove Prometheus, CLS, MCP
    regex_replace_in_file(app_yml, r'# Prometheus 配置.*?mock-enabled: false.*?\n', '')
    regex_replace_in_file(app_yml, r'# CLS 云日志服务配置.*?mock-enabled: false.*?\n', '')
    # Remove mcp section under spring.ai
    regex_replace_in_file(app_yml, r'# Spring AI MCP 客户端配置.*?sse-endpoint: /sse/92XXXXXXXXb4  # 完整的SSE端点路径', '')
    
    git_commit("Refactor: Prune AIOps features, keep only RAG and Chat capabilities", DATES[1])

# --- Stage 3: Nacos Config ---
def stage_3():
    print("Stage 3: Nacos Config...")
    
    pom_path = os.path.join(DEST_DIR, "pom.xml")
    
    nacos_dep = """
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
        </dependency>
    """
    
    regex_replace_in_file(pom_path, r'</dependencies>', f'{nacos_dep}\n    </dependencies>')
    
    sca_bom = """
            <dependency>
                <groupId>com.alibaba.cloud</groupId>
                <artifactId>spring-cloud-alibaba-dependencies</artifactId>
                <version>2023.0.1.0</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>2023.0.0</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
    """
    regex_replace_in_file(pom_path, r'<artifactId>spring-ai-alibaba-bom</artifactId>.*?<scope>import</scope>\s*</dependency>', 
                          f'<artifactId>spring-ai-alibaba-bom</artifactId>\n                <version>${{spring-ai-alibaba.version}}</version>\n                <type>pom</type>\n                <scope>import</scope>\n            </dependency>\n{sca_bom}')

    # Update application.yml
    app_yml = os.path.join(DEST_DIR, "src/main/resources/application.yml")
    
    # Prepend spring application name and cloud config to existing spring block
    # We replace "spring:" with the new config, ensuring indentation matches (usually 2 spaces for children)
    new_conf = """
  application:
    name: tktk-agent
  cloud:
    nacos:
      discovery:
        server-addr: localhost:8848
"""
    replace_in_file(app_yml, "spring:", "spring:" + new_conf)
    
    git_commit("Feat: Configure Nacos discovery for tktk-agent service", DATES[2])

# --- Stage 4: Package Rename ---
def stage_4():
    print("Stage 4: Package Rename...")
    
    src_root = os.path.join(DEST_DIR, "src/main/java")
    old_pkg_dir = os.path.join(src_root, "org", "example")
    new_pkg_dir = os.path.join(src_root, "com", "tktk", "agent")
    
    # Move files
    if os.path.exists(old_pkg_dir):
        if not os.path.exists(new_pkg_dir):
            os.makedirs(new_pkg_dir)
        
        # Move all contents
        for item in os.listdir(old_pkg_dir):
            shutil.move(os.path.join(old_pkg_dir, item), new_pkg_dir)
        
        # Remove empty org/example
        shutil.rmtree(os.path.join(src_root, "org"))

    # Update package declarations and imports in ALL java files
    for root, dirs, files in os.walk(DEST_DIR):
        for file in files:
            if file.endswith(".java"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace package declaration
                content = re.sub(r'package org\.example', 'package com.tktk.agent', content)
                
                # Replace imports
                content = content.replace('import org.example.', 'import com.tktk.agent.')
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
    
    # Update pom.xml groupId
    pom_path = os.path.join(DEST_DIR, "pom.xml")
    replace_in_file(pom_path, "<groupId>org.example</groupId>", "<groupId>com.tktk</groupId>")
    replace_in_file(pom_path, "<artifactId>super-biz-agent</artifactId>", "<artifactId>tktk-agent</artifactId>")

    git_commit("Refactor: Rename packages to com.tktk.agent to match project convention", DATES[3])

# --- Stage 5: Gateway Config ---
def stage_5():
    print("Stage 5: Gateway Config...")
    
    gateway_yml = os.path.join(DEST_ROOT, "tktk-gateway/src/main/resources/application.yml")
    
    old_route = """        - id: tktk-service-search
          uri: lb://tktk-service-search
          predicates:
            - Path=/tktk/search/**"""
            
    new_route = """        - id: tktk-service-search
          uri: lb://tktk-service-search
          predicates:
            - Path=/tktk/search/**
        - id: tktk-agent
          uri: lb://tktk-agent
          predicates:
            - Path=/api/ai/**"""
            
    replace_in_file(gateway_yml, old_route, new_route)

    git_commit("Config: Add gateway routes for AI agent service", DATES[4])

# --- Stage 6: Final Polish ---
def stage_6():
    print("Stage 6: Final Polish...")
    
    readme = os.path.join(DEST_DIR, "README.md")
    if os.path.exists(readme):
        with open(readme, 'w', encoding='utf-8') as f:
            f.write("# TKTK Agent Service\n\nAI Agent module for TKTK, providing RAG and Chat capabilities.\n\nIntegrated via Spring Boot 3.2 and Spring AI.")
    
    # Update root readme
    root_readme = os.path.join(DEST_ROOT, "README.md")
    if os.path.exists(root_readme):
         with open(root_readme, 'a', encoding='utf-8') as f:
             f.write("\n\n## AI Module\n\n- **tktk-agent**: AI service based on Spring AI, providing intelligent Q&A.")

    git_commit("Docs: Update documentation for AI Agent integration", DATES[5])

def main():
    stage_1()
    stage_2()
    stage_3()
    stage_4()
    stage_5()
    stage_6()

if __name__ == "__main__":
    main()
