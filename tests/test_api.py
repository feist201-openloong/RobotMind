"""
系统集成测试用例
用于测试助学助手系统的各个API接口
"""

import requests
import json
import time
from datetime import datetime, timedelta
import pytest

# 配置
BASE_URL = "http://localhost:5000/api"
TIMEOUT = 10  # 请求超时时间（秒）


class TestHealthCheck:
    """健康检查测试"""
    
    def test_health_endpoint(self):
        """测试健康检查接口"""
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_health_response_time(self):
        """测试健康检查响应时间"""
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 2  # 响应时间应小于2秒
    
    def test_health_content_type(self):
        """测试健康检查返回内容类型"""
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        assert response.status_code == 200
        assert "application/json" in response.headers.get("Content-Type", "")


class TestKnowledgeAPI:
    """知识库API测试"""
    
    def test_create_knowledge(self):
        """测试创建知识条目"""
        data = {
            "title": "Python装饰器详解",
            "content": "装饰器是Python的一个强大功能，可以修改函数或类的行为...",
            "category": "Python",
            "tags": ["Python", "装饰器", "高级特性"]
        }
        response = requests.post(f"{BASE_URL}/knowledge", json=data, timeout=TIMEOUT)
        assert response.status_code == 201
        result = response.json()
        assert "id" in result
        assert result["title"] == data["title"]
    
    def test_get_knowledge_list(self):
        """测试获取知识条目列表"""
        response = requests.get(f"{BASE_URL}/knowledge", timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_knowledge_by_id(self):
        """测试根据ID获取知识条目"""
        # 先创建一个知识条目
        create_data = {
            "title": "测试知识条目",
            "content": "这是测试内容",
            "category": "测试"
        }
        create_response = requests.post(f"{BASE_URL}/knowledge", json=create_data, timeout=TIMEOUT)
        assert create_response.status_code == 201
        knowledge_id = create_response.json()["id"]
        
        # 获取创建的知识条目
        response = requests.get(f"{BASE_URL}/knowledge/{knowledge_id}", timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == knowledge_id
        assert data["title"] == create_data["title"]
    
    def test_update_knowledge(self):
        """测试更新知识条目"""
        # 先创建一个知识条目
        create_data = {
            "title": "待更新的知识条目",
            "content": "原始内容",
            "category": "测试"
        }
        create_response = requests.post(f"{BASE_URL}/knowledge", json=create_data, timeout=TIMEOUT)
        assert create_response.status_code == 201
        knowledge_id = create_response.json()["id"]
        
        # 更新知识条目
        update_data = {
            "title": "已更新的知识条目",
            "content": "更新后的内容"
        }
        response = requests.put(f"{BASE_URL}/knowledge/{knowledge_id}", json=update_data, timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
    
    def test_delete_knowledge(self):
        """测试删除知识条目"""
        # 先创建一个知识条目
        create_data = {
            "title": "待删除的知识条目",
            "content": "将被删除的内容",
            "category": "测试"
        }
        create_response = requests.post(f"{BASE_URL}/knowledge", json=create_data, timeout=TIMEOUT)
        assert create_response.status_code == 201
        knowledge_id = create_response.json()["id"]
        
        # 删除知识条目
        response = requests.delete(f"{BASE_URL}/knowledge/{knowledge_id}", timeout=TIMEOUT)
        assert response.status_code == 204
        
        # 验证删除
        get_response = requests.get(f"{BASE_URL}/knowledge/{knowledge_id}", timeout=TIMEOUT)
        assert get_response.status_code == 404
    
    def test_search_knowledge(self):
        """测试搜索知识条目"""
        # 先创建测试数据
        test_data = {
            "title": "Python搜索测试",
            "content": "这是用于搜索测试的内容",
            "category": "Python"
        }
        requests.post(f"{BASE_URL}/knowledge", json=test_data, timeout=TIMEOUT)
        
        # 搜索知识条目
        response = requests.get(f"{BASE_URL}/knowledge/search?q=Python", timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_knowledge_validation(self):
        """测试知识条目验证"""
        # 测试缺少必填字段
        invalid_data = {
            "content": "缺少标题的内容"
        }
        response = requests.post(f"{BASE_URL}/knowledge", json=invalid_data, timeout=TIMEOUT)
        assert response.status_code == 400
        
        # 测试空标题
        invalid_data2 = {
            "title": "",
            "content": "标题为空"
        }
        response = requests.post(f"{BASE_URL}/knowledge", json=invalid_data2, timeout=TIMEOUT)
        assert response.status_code == 400


class TestCodeAPI:
    """代码管理API测试"""
    
    def test_create_code_snippet(self):
        """测试创建代码片段"""
        data = {
            "title": "快速排序算法",
            "code": """def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)""",
            "language": "python",
            "category": "算法",
            "description": "快速排序的Python实现"
        }
        response = requests.post(f"{BASE_URL}/code", json=data, timeout=TIMEOUT)
        assert response.status_code == 201
        result = response.json()
        assert "id" in result
        assert result["title"] == data["title"]
    
    def test_get_code_list(self):
        """测试获取代码片段列表"""
        response = requests.get(f"{BASE_URL}/code", timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_code_by_id(self):
        """测试根据ID获取代码片段"""
        # 先创建一个代码片段
        create_data = {
            "title": "测试代码片段",
            "code": "print('Hello, World!')",
            "language": "python",
            "category": "测试"
        }
        create_response = requests.post(f"{BASE_URL}/code", json=create_data, timeout=TIMEOUT)
        assert create_response.status_code == 201
        code_id = create_response.json()["id"]
        
        # 获取创建的代码片段
        response = requests.get(f"{BASE_URL}/code/{code_id}", timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == code_id
    
    def test_update_code_snippet(self):
        """测试更新代码片段"""
        # 先创建一个代码片段
        create_data = {
            "title": "待更新的代码片段",
            "code": "原始代码",
            "language": "python",
            "category": "测试"
        }
        create_response = requests.post(f"{BASE_URL}/code", json=create_data, timeout=TIMEOUT)
        assert create_response.status_code == 201
        code_id = create_response.json()["id"]
        
        # 更新代码片段
        update_data = {
            "title": "已更新的代码片段",
            "code": "更新后的代码",
            "description": "更新后的描述"
        }
        response = requests.put(f"{BASE_URL}/code/{code_id}", json=update_data, timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
    
    def test_delete_code_snippet(self):
        """测试删除代码片段"""
        # 先创建一个代码片段
        create_data = {
            "title": "待删除的代码片段",
            "code": "将被删除的代码",
            "language": "python",
            "category": "测试"
        }
        create_response = requests.post(f"{BASE_URL}/code", json=create_data, timeout=TIMEOUT)
        assert create_response.status_code == 201
        code_id = create_response.json()["id"]
        
        # 删除代码片段
        response = requests.delete(f"{BASE_URL}/code/{code_id}", timeout=TIMEOUT)
        assert response.status_code == 204
        
        # 验证删除
        get_response = requests.get(f"{BASE_URL}/code/{code_id}", timeout=TIMEOUT)
        assert get_response.status_code == 404
    
    def test_search_code(self):
        """测试搜索代码片段"""
        # 先创建测试数据
        test_data = {
            "title": "Python搜索测试代码",
            "code": "# 这是用于搜索测试的代码",
            "language": "python",
            "category": "Python"
        }
        requests.post(f"{BASE_URL}/code", json=test_data, timeout=TIMEOUT)
        
        # 搜索代码片段
        response = requests.get(f"{BASE_URL}/code/search?q=Python", timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_code_language_filter(self):
        """测试按语言过滤代码片段"""
        response = requests.get(f"{BASE_URL}/code?language=python", timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # 验证所有返回的代码片段都是Python语言
        for code in data:
            assert code.get("language") == "python"


class TestTodoAPI:
    """待办任务API测试"""
    
    def test_create_todo(self):
        """测试创建待办任务"""
        data = {
            "title": "完成系统集成文档",
            "description": "编写详细的系统集成指南",
            "priority": "high",
            "due_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "category": "工作"
        }
        response = requests.post(f"{BASE_URL}/todos", json=data, timeout=TIMEOUT)
        assert response.status_code == 201
        result = response.json()
        assert "id" in result
        assert result["title"] == data["title"]
        assert result["completed"] == False
    
    def test_get_todo_list(self):
        """测试获取待办任务列表"""
        response = requests.get(f"{BASE_URL}/todos", timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_todo_by_id(self):
        """测试根据ID获取待办任务"""
        # 先创建一个待办任务
        create_data = {
            "title": "测试待办任务",
            "description": "测试描述",
            "priority": "medium"
        }
        create_response = requests.post(f"{BASE_URL}/todos", json=create_data, timeout=TIMEOUT)
        assert create_response.status_code == 201
        todo_id = create_response.json()["id"]
        
        # 获取创建的待办任务
        response = requests.get(f"{BASE_URL}/todos/{todo_id}", timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
    
    def test_update_todo(self):
        """测试更新待办任务"""
        # 先创建一个待办任务
        create_data = {
            "title": "待更新的待办任务",
            "description": "原始描述",
            "priority": "low"
        }
        create_response = requests.post(f"{BASE_URL}/todos", json=create_data, timeout=TIMEOUT)
        assert create_response.status_code == 201
        todo_id = create_response.json()["id"]
        
        # 更新待办任务
        update_data = {
            "title": "已更新的待办任务",
            "description": "更新后的描述",
            "priority": "high"
        }
        response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=update_data, timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
    
    def test_complete_todo(self):
        """测试完成待办任务"""
        # 先创建一个待办任务
        create_data = {
            "title": "待完成的待办任务",
            "description": "将被标记为完成",
            "priority": "medium"
        }
        create_response = requests.post(f"{BASE_URL}/todos", json=create_data, timeout=TIMEOUT)
        assert create_response.status_code == 201
        todo_id = create_response.json()["id"]
        
        # 完成待办任务
        response = requests.patch(f"{BASE_URL}/todos/{todo_id}", json={"completed": True}, timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] == True
    
    def test_delete_todo(self):
        """测试删除待办任务"""
        # 先创建一个待办任务
        create_data = {
            "title": "待删除的待办任务",
            "description": "将被删除",
            "priority": "low"
        }
        create_response = requests.post(f"{BASE_URL}/todos", json=create_data, timeout=TIMEOUT)
        assert create_response.status_code == 201
        todo_id = create_response.json()["id"]
        
        # 删除待办任务
        response = requests.delete(f"{BASE_URL}/todos/{todo_id}", timeout=TIMEOUT)
        assert response.status_code == 204
        
        # 验证删除
        get_response = requests.get(f"{BASE_URL}/todos/{todo_id}", timeout=TIMEOUT)
        assert get_response.status_code == 404
    
    def test_todo_priority_filter(self):
        """测试按优先级过滤待办任务"""
        response = requests.get(f"{BASE_URL}/todos?priority=high", timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # 验证所有返回的任务都是高优先级
        for todo in data:
            assert todo.get("priority") == "high"
    
    def test_todo_status_filter(self):
        """测试按状态过滤待办任务"""
        # 测试获取未完成的任务
        response = requests.get(f"{BASE_URL}/todos?completed=false", timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        for todo in data:
            assert todo.get("completed") == False
        
        # 测试获取已完成的任务
        response = requests.get(f"{BASE_URL}/todos?completed=true", timeout=TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        for todo in data:
            assert todo.get("completed") == True


class TestIntegration:
    """集成测试"""
    
    def test_api_endpoints_availability(self):
        """测试所有API端点可用性"""
        endpoints = [
            "/health",
            "/knowledge",
            "/code",
            "/todos"
        ]
        
        for endpoint in endpoints:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=TIMEOUT)
            assert response.status_code == 200, f"端点 {endpoint} 不可用"
    
    def test_concurrent_requests(self):
        """测试并发请求"""
        import concurrent.futures
        
        def make_request():
            response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
            return response.status_code
        
        # 并发发送10个请求
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # 所有请求都应该成功
        assert all(status == 200 for status in results)
    
    def test_large_data_handling(self):
        """测试大数据处理"""
        # 创建一个大型知识条目
        large_content = "这是一段很长的内容。" * 1000  # 约10KB的内容
        data = {
            "title": "大数据测试条目",
            "content": large_content,
            "category": "测试"
        }
        
        response = requests.post(f"{BASE_URL}/knowledge", json=data, timeout=TIMEOUT)
        assert response.status_code == 201
        
        # 验证数据正确保存
        knowledge_id = response.json()["id"]
        get_response = requests.get(f"{BASE_URL}/knowledge/{knowledge_id}", timeout=TIMEOUT)
        assert get_response.status_code == 200
        assert len(get_response.json()["content"]) == len(large_content)


class TestErrorHandling:
    """错误处理测试"""
    
    def test_invalid_json(self):
        """测试无效JSON请求"""
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            f"{BASE_URL}/knowledge",
            data="invalid json",
            headers=headers,
            timeout=TIMEOUT
        )
        assert response.status_code == 400
    
    def test_nonexistent_resource(self):
        """测试访问不存在的资源"""
        response = requests.get(f"{BASE_URL}/knowledge/99999", timeout=TIMEOUT)
        assert response.status_code == 404
    
    def test_method_not_allowed(self):
        """测试不支持的HTTP方法"""
        response = requests.patch(f"{BASE_URL}/health", timeout=TIMEOUT)
        assert response.status_code == 405


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v", "--tb=short"])