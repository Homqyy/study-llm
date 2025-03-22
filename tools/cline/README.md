# Cline学习记录

官网手册：<https://docs.cline.bot/>

关键命令：

1. `initialize memory bank`
2. `update memory bank`

启动流程：

1. 创建`cline_docs/projectBrief.md`。示例：

    ```markdown
    # Project Brief

    ## Overview
    Building a [type of application] that will [main purpose].

    ## Core Features
    - Feature 1
    - Feature 2
    - Feature 3

    ## Target Users
    [Describe who will use your application]

    ## Technical Preferences (optional)
    - Any specific technologies you want to use
    - Any specific requirements or constraints
    ```

2. 告诉Cline：`initialize memory bank`
3. 审查初始化结果，并做适当的优化
4. 创建`.clinerules`文件，并写入工程配置。示例：

    ```markdown
    # Project Configuration

    ## Tech Stack
    - Next.js 14+ with App Router
    - Tailwind CSS for styling
    - Supabase for backend
    - Vercel for deployment
    - GitHub for version control

    ## Project Structure
    /src
    /app         # Next.js App Router pages
    /components  # React components
    /lib         # Utility functions
    /types       # TypeScript types
    /supabase
    /migrations  # SQL migration files
    /seed        # Seed data files
    /public        # Static assets

    ## Database Migrations
    SQL files in /supabase/migrations should:
    - Use sequential numbering: 001, 002, etc.
    - Include descriptive names
    - Be reviewed by Cline before execution
    Example: 001_create_users_table.sql

    ## Development Workflow
    - Cline helps write and review code changes
    - Vercel automatically deploys from main branch
    - Database migrations reviewed by Cline before execution

    ## Security
    DO NOT read or modify:
    - .env files
    - **/config/secrets.*
    - Any file containing API keys or credentials
    ```
