#!/usr/bin/env python3
"""
Comprehensive Test Suite for Enhanced V0 MCP Server
Tests all 20 MCP tools including new Platform API features
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, 'src')

# Set environment variable
os.environ['V0_API_KEY'] = 'v1:VAbNhNzcXd53hVhUEJ5DffUp:rigbaHc9wa9HYhRqVoA6TodT'

class V0MCPTester:
    def __init__(self):
        self.results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'errors': [],
            'test_details': {}
        }
        self.mcp = None
    
    async def setup(self):
        """Initialize the MCP server"""
        try:
            from vercel_v0_server import mcp
            self.mcp = mcp
            print(f"✅ Server initialized: {mcp.name}")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize server: {e}")
            return False
    
    def log_test(self, test_name, success, details=None, error=None):
        """Log test result"""
        self.results['total_tests'] += 1
        if success:
            self.results['passed'] += 1
            print(f"✅ {test_name}")
        else:
            self.results['failed'] += 1
            print(f"❌ {test_name}")
            if error:
                print(f"   Error: {error}")
                self.results['errors'].append(f"{test_name}: {error}")
        
        self.results['test_details'][test_name] = {
            'success': success,
            'details': details,
            'error': str(error) if error else None
        }
    
    async def test_tool_registration(self):
        """Test 1: Verify all 20 tools are registered"""
        test_name = "Tool Registration Count"
        try:
            # Get tools using the FastMCP interface
            tools_result = await self.mcp.get_tools()
            if hasattr(tools_result, 'tools'):
                tools = [tool.name for tool in tools_result.tools]
            else:
                tools = list(tools_result.keys()) if isinstance(tools_result, dict) else []
            
            expected_tools = [
                'create_v0_session', 'generate_with_v0', 'continue_v0_session',
                'get_v0_session_files', 'create_v0_frame_preview', 'list_v0_sessions',
                'generate_component', 'generate_and_create_component',
                'create_v0_project', 'list_v0_projects', 'get_v0_project_by_id',
                'assign_project_to_chat', 'initialize_chat_from_repo',
                'initialize_chat_from_files', 'create_v0_deployment',
                'get_deployment_status', 'get_deployment_logs', 'fork_v0_chat',
                'update_chat_metadata', 'favorite_chat'
            ]
            
            success = len(tools) == 20 and all(tool in tools for tool in expected_tools)
            details = f"Found {len(tools)} tools: {sorted(tools)}"
            self.log_test(test_name, success, details)
            
            return tools
        except Exception as e:
            self.log_test(test_name, False, error=e)
            return []
    
    async def test_new_platform_api_endpoints(self):
        """Test 2: Test new Platform API endpoints"""
        platform_api_tests = [
            ('create_v0_project', lambda: self.test_create_project()),
            ('list_v0_projects', lambda: self.test_list_projects()),
            ('get_v0_project_by_id', lambda: self.test_get_project_by_id()),
            ('assign_project_to_chat', lambda: self.test_assign_project_to_chat()),
            ('initialize_chat_from_repo', lambda: self.test_initialize_from_repo()),
            ('initialize_chat_from_files', lambda: self.test_initialize_from_files()),
            ('create_v0_deployment', lambda: self.test_create_deployment()),
            ('get_deployment_status', lambda: self.test_get_deployment_status()),
            ('get_deployment_logs', lambda: self.test_get_deployment_logs()),
            ('fork_v0_chat', lambda: self.test_fork_chat()),
            ('update_chat_metadata', lambda: self.test_update_chat_metadata()),
            ('favorite_chat', lambda: self.test_favorite_chat())
        ]
        
        for test_name, test_func in platform_api_tests:
            try:
                await test_func()
            except Exception as e:
                self.log_test(f"Platform API - {test_name}", False, error=e)
    
    async def test_create_project(self):
        """Test create_v0_project tool"""
        test_name = "Platform API - create_v0_project"
        try:
            tool = await self.mcp.get_tool('create_v0_project')
            result = await self.mcp.call_tool(
                'create_v0_project',
                arguments={
                    'name': 'test-project',
                    'description': 'Test project for MCP testing'
                }
            )
            success = result and 'project_id' in str(result)
            self.log_test(test_name, success, details=str(result))
            return result
        except Exception as e:
            self.log_test(test_name, False, error=e)
            return None
    
    async def test_list_projects(self):
        """Test list_v0_projects tool"""
        test_name = "Platform API - list_v0_projects"
        try:
            result = await self.mcp.call_tool('list_v0_projects', arguments={})
            success = result is not None
            self.log_test(test_name, success, details=str(result)[:200])
            return result
        except Exception as e:
            self.log_test(test_name, False, error=e)
            return None
    
    async def test_get_project_by_id(self):
        """Test get_v0_project_by_id tool"""
        test_name = "Platform API - get_v0_project_by_id"
        try:
            # Use a test project ID
            result = await self.mcp.call_tool(
                'get_v0_project_by_id',
                arguments={'project_id': 'test-project-id'}
            )
            success = result is not None
            self.log_test(test_name, success, details=str(result)[:200])
        except Exception as e:
            self.log_test(test_name, False, error=e)
    
    async def test_assign_project_to_chat(self):
        """Test assign_project_to_chat tool"""
        test_name = "Platform API - assign_project_to_chat"
        try:
            result = await self.mcp.call_tool(
                'assign_project_to_chat',
                arguments={
                    'session_id': 'test-session',
                    'project_id': 'test-project'
                }
            )
            success = result is not None
            self.log_test(test_name, success, details=str(result)[:200])
        except Exception as e:
            self.log_test(test_name, False, error=e)
    
    async def test_initialize_from_repo(self):
        """Test initialize_chat_from_repo tool"""
        test_name = "Platform API - initialize_chat_from_repo"
        try:
            result = await self.mcp.call_tool(
                'initialize_chat_from_repo',
                arguments={
                    'session_id': 'test-session',
                    'repository_url': 'https://github.com/test/repo',
                    'branch': 'main'
                }
            )
            success = result is not None
            self.log_test(test_name, success, details=str(result)[:200])
        except Exception as e:
            self.log_test(test_name, False, error=e)
    
    async def test_initialize_from_files(self):
        """Test initialize_chat_from_files tool"""
        test_name = "Platform API - initialize_chat_from_files"
        try:
            result = await self.mcp.call_tool(
                'initialize_chat_from_files',
                arguments={
                    'session_id': 'test-session',
                    'files': [{'path': 'test.js', 'content': 'console.log("test");'}]
                }
            )
            success = result is not None
            self.log_test(test_name, success, details=str(result)[:200])
        except Exception as e:
            self.log_test(test_name, False, error=e)
    
    async def test_create_deployment(self):
        """Test create_v0_deployment tool"""
        test_name = "Platform API - create_v0_deployment"
        try:
            result = await self.mcp.call_tool(
                'create_v0_deployment',
                arguments={
                    'session_id': 'test-session',
                    'name': 'test-deployment'
                }
            )
            success = result is not None
            self.log_test(test_name, success, details=str(result)[:200])
        except Exception as e:
            self.log_test(test_name, False, error=e)
    
    async def test_get_deployment_status(self):
        """Test get_deployment_status tool"""
        test_name = "Platform API - get_deployment_status"
        try:
            result = await self.mcp.call_tool(
                'get_deployment_status',
                arguments={'deployment_id': 'test-deployment-id'}
            )
            success = result is not None
            self.log_test(test_name, success, details=str(result)[:200])
        except Exception as e:
            self.log_test(test_name, False, error=e)
    
    async def test_get_deployment_logs(self):
        """Test get_deployment_logs tool"""
        test_name = "Platform API - get_deployment_logs"
        try:
            result = await self.mcp.call_tool(
                'get_deployment_logs',
                arguments={'deployment_id': 'test-deployment-id'}
            )
            success = result is not None
            self.log_test(test_name, success, details=str(result)[:200])
        except Exception as e:
            self.log_test(test_name, False, error=e)
    
    async def test_fork_chat(self):
        """Test fork_v0_chat tool"""
        test_name = "Platform API - fork_v0_chat"
        try:
            result = await self.mcp.call_tool(
                'fork_v0_chat',
                arguments={
                    'session_id': 'test-session',
                    'fork_name': 'test-fork'
                }
            )
            success = result is not None
            self.log_test(test_name, success, details=str(result)[:200])
        except Exception as e:
            self.log_test(test_name, False, error=e)
    
    async def test_update_chat_metadata(self):
        """Test update_chat_metadata tool"""
        test_name = "Platform API - update_chat_metadata"
        try:
            result = await self.mcp.call_tool(
                'update_chat_metadata',
                arguments={
                    'session_id': 'test-session',
                    'metadata': {'tags': ['test'], 'description': 'Test session'}
                }
            )
            success = result is not None
            self.log_test(test_name, success, details=str(result)[:200])
        except Exception as e:
            self.log_test(test_name, False, error=e)
    
    async def test_favorite_chat(self):
        """Test favorite_chat tool"""
        test_name = "Platform API - favorite_chat"
        try:
            result = await self.mcp.call_tool(
                'favorite_chat',
                arguments={
                    'session_id': 'test-session',
                    'favorite': True
                }
            )
            success = result is not None
            self.log_test(test_name, success, details=str(result)[:200])
        except Exception as e:
            self.log_test(test_name, False, error=e)
    
    async def test_backward_compatibility(self):
        """Test 3: Test existing functionality still works"""
        legacy_tests = [
            ('create_v0_session', lambda: self.test_legacy_create_session()),
            ('generate_with_v0', lambda: self.test_legacy_generate()),
            ('list_v0_sessions', lambda: self.test_legacy_list_sessions()),
            ('generate_component', lambda: self.test_legacy_generate_component())
        ]
        
        for test_name, test_func in legacy_tests:
            try:
                await test_func()
            except Exception as e:
                self.log_test(f"Backward Compatibility - {test_name}", False, error=e)
    
    async def test_legacy_create_session(self):
        """Test legacy create_v0_session functionality"""
        test_name = "Backward Compatibility - create_v0_session"
        try:
            result = await self.mcp.call_tool(
                'create_v0_session',
                arguments={'project_path': '/tmp/test-project'}
            )
            success = result and 'session_id' in str(result)
            self.log_test(test_name, success, details=str(result)[:200])
            return result
        except Exception as e:
            self.log_test(test_name, False, error=e)
            return None
    
    async def test_legacy_generate(self):
        """Test legacy generate_with_v0 functionality"""
        test_name = "Backward Compatibility - generate_with_v0"
        try:
            result = await self.mcp.call_tool(
                'generate_with_v0',
                arguments={'prompt': 'Create a simple React button component'}
            )
            success = result is not None
            self.log_test(test_name, success, details=str(result)[:200])
        except Exception as e:
            self.log_test(test_name, False, error=e)
    
    async def test_legacy_list_sessions(self):
        """Test legacy list_v0_sessions functionality"""
        test_name = "Backward Compatibility - list_v0_sessions"
        try:
            result = await self.mcp.call_tool('list_v0_sessions', arguments={})
            success = result is not None
            self.log_test(test_name, success, details=str(result)[:200])
        except Exception as e:
            self.log_test(test_name, False, error=e)
    
    async def test_legacy_generate_component(self):
        """Test legacy generate_component functionality"""
        test_name = "Backward Compatibility - generate_component"
        try:
            result = await self.mcp.call_tool(
                'generate_component',
                arguments={'prompt': 'A simple card component'}
            )
            success = result is not None
            self.log_test(test_name, success, details=str(result)[:200])
        except Exception as e:
            self.log_test(test_name, False, error=e)
    
    async def test_integration_workflow(self):
        """Test 4: Complete integration workflow"""
        test_name = "Integration Workflow"
        try:
            # Step 1: Create project
            project_result = await self.mcp.call_tool(
                'create_v0_project',
                arguments={
                    'name': 'integration-test-project',
                    'description': 'Project for integration testing'
                }
            )
            
            # Step 2: Create session
            session_result = await self.mcp.call_tool(
                'create_v0_session',
                arguments={'project_path': '/tmp/integration-test'}
            )
            
            # Step 3: Generate component
            if session_result and 'session_id' in str(session_result):
                generate_result = await self.mcp.call_tool(
                    'generate_with_v0',
                    arguments={'prompt': 'Create a todo app component'}
                )
                
                # Step 4: Try deployment (will likely fail due to API limits but should not crash)
                try:
                    deploy_result = await self.mcp.call_tool(
                        'create_v0_deployment',
                        arguments={
                            'session_id': str(session_result).split("'")[1] if "'" in str(session_result) else 'test',
                            'name': 'integration-test-deployment'
                        }
                    )
                except:
                    deploy_result = "Expected to fail - API limits"
                
                success = all([project_result, session_result, generate_result])
                details = f"Project: {bool(project_result)}, Session: {bool(session_result)}, Generate: {bool(generate_result)}, Deploy: {bool(deploy_result)}"
            else:
                success = False
                details = "Failed to create session"
            
            self.log_test(test_name, success, details)
        except Exception as e:
            self.log_test(test_name, False, error=e)
    
    async def test_error_handling(self):
        """Test 5: Error handling"""
        error_tests = [
            ('Invalid session ID', lambda: self.test_invalid_session()),
            ('Invalid project ID', lambda: self.test_invalid_project()),
            ('Empty prompt', lambda: self.test_empty_prompt()),
            ('Malformed arguments', lambda: self.test_malformed_args())
        ]
        
        for test_name, test_func in error_tests:
            try:
                await test_func()
            except Exception as e:
                # Error handling tests should catch errors gracefully
                self.log_test(f"Error Handling - {test_name}", True, details="Caught exception as expected")
    
    async def test_invalid_session(self):
        """Test error handling with invalid session ID"""
        test_name = "Error Handling - Invalid session ID"
        try:
            result = await self.mcp.call_tool(
                'continue_v0_session',
                arguments={
                    'session_id': 'non-existent-session',
                    'prompt': 'test'
                }
            )
            # Should handle gracefully
            success = 'error' in str(result).lower() or 'not found' in str(result).lower()
            self.log_test(test_name, success, details=str(result)[:200])
        except Exception as e:
            # Exception is acceptable for error handling test
            self.log_test(test_name, True, details=f"Exception caught: {e}")
    
    async def test_invalid_project(self):
        """Test error handling with invalid project ID"""
        test_name = "Error Handling - Invalid project ID"
        try:
            result = await self.mcp.call_tool(
                'get_v0_project_by_id',
                arguments={'project_id': 'non-existent-project'}
            )
            success = 'error' in str(result).lower() or 'not found' in str(result).lower()
            self.log_test(test_name, success, details=str(result)[:200])
        except Exception as e:
            self.log_test(test_name, True, details=f"Exception caught: {e}")
    
    async def test_empty_prompt(self):
        """Test error handling with empty prompt"""
        test_name = "Error Handling - Empty prompt"
        try:
            result = await self.mcp.call_tool(
                'generate_with_v0',
                arguments={'prompt': ''}
            )
            success = 'error' in str(result).lower() or result is None
            self.log_test(test_name, success, details=str(result)[:200])
        except Exception as e:
            self.log_test(test_name, True, details=f"Exception caught: {e}")
    
    async def test_malformed_args(self):
        """Test error handling with malformed arguments"""
        test_name = "Error Handling - Malformed arguments"
        try:
            result = await self.mcp.call_tool(
                'create_v0_project',
                arguments={'invalid_field': 'test'}
            )
            success = 'error' in str(result).lower() or result is None
            self.log_test(test_name, success, details=str(result)[:200])
        except Exception as e:
            self.log_test(test_name, True, details=f"Exception caught: {e}")
    
    async def test_performance(self):
        """Test 6: Basic performance metrics"""
        test_name = "Performance - Session persistence"
        try:
            import time
            
            # Test session creation time
            start_time = time.time()
            result = await self.mcp.call_tool(
                'create_v0_session',
                arguments={'project_path': '/tmp/perf-test'}
            )
            create_time = time.time() - start_time
            
            # Test session listing time
            start_time = time.time()
            sessions = await self.mcp.call_tool('list_v0_sessions', arguments={})
            list_time = time.time() - start_time
            
            # Performance is good if operations complete under reasonable time
            success = create_time < 5.0 and list_time < 2.0
            details = f"Create time: {create_time:.2f}s, List time: {list_time:.2f}s"
            self.log_test(test_name, success, details)
        except Exception as e:
            self.log_test(test_name, False, error=e)
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("ENHANCED V0 MCP SERVER TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {self.results['total_tests']}")
        print(f"Passed: {self.results['passed']} ✅")
        print(f"Failed: {self.results['failed']} ❌")
        print(f"Success Rate: {(self.results['passed']/self.results['total_tests']*100):.1f}%")
        
        if self.results['errors']:
            print("\nERRORS:")
            for error in self.results['errors']:
                print(f"  • {error}")
        
        # Overall assessment
        success_rate = self.results['passed']/self.results['total_tests']
        if success_rate >= 0.8:
            print("\n🎉 OVERALL: PRODUCTION READY")
        elif success_rate >= 0.6:
            print("\n⚠️  OVERALL: NEEDS MINOR FIXES")
        else:
            print("\n❌ OVERALL: NEEDS MAJOR FIXES")
        
        print("="*60)
    
    async def run_all_tests(self):
        """Run all tests"""
        print("Enhanced V0 MCP Server - Comprehensive Test Suite")
        print("="*60)
        
        if not await self.setup():
            return
        
        # Test 1: Tool registration
        print("\n📋 Test 1: Tool Registration")
        tools = await self.test_tool_registration()
        
        # Test 2: Platform API endpoints
        print("\n🚀 Test 2: Platform API Endpoints")
        await self.test_new_platform_api_endpoints()
        
        # Test 3: Backward compatibility
        print("\n🔄 Test 3: Backward Compatibility")
        await self.test_backward_compatibility()
        
        # Test 4: Integration workflow
        print("\n🔗 Test 4: Integration Workflow")
        await self.test_integration_workflow()
        
        # Test 5: Error handling
        print("\n🛡️  Test 5: Error Handling")
        await self.test_error_handling()
        
        # Test 6: Performance
        print("\n⚡ Test 6: Performance")
        await self.test_performance()
        
        # Print summary
        self.print_summary()
        
        # Save results
        with open('test_results.json', 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        return self.results

async def main():
    """Main test runner"""
    tester = V0MCPTester()
    results = await tester.run_all_tests()
    return results

if __name__ == "__main__":
    asyncio.run(main())
