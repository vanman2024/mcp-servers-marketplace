#\!/usr/bin/env python3
"""
Enhanced V0 MCP Server - Deployment Validation Script
Comprehensive testing for production deployment readiness
"""

import asyncio
import aiohttp
import json
import time
import sys
import logging
from typing import Dict, List, Any
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DeploymentValidator:
    """Comprehensive deployment validation"""
    
    def __init__(self, server_url: str = "http://localhost:8015"):
        self.server_url = server_url
        self.results = {
            "overall_status": "UNKNOWN",
            "timestamp": time.time(),
            "tests_passed": 0,
            "tests_failed": 0,
            "test_results": {},
            "performance_metrics": {},
            "deployment_ready": False
        }
        
    async def validate_server_startup(self) -> bool:
        """Test 1: Server startup and basic connectivity"""
        logger.info("🔍 Testing server startup and connectivity...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.server_url}/health", timeout=10) as response:
                    if response.status == 200:
                        health_data = await response.json()
                        self.results["test_results"]["server_startup"] = {
                            "status": "PASSED",
                            "message": "Server responding on port 8015",
                            "health_data": health_data
                        }
                        logger.info("✅ Server startup: PASSED")
                        return True
        except Exception as e:
            self.results["test_results"]["server_startup"] = {
                "status": "FAILED", 
                "message": f"Server not responding: {e}"
            }
            logger.error(f"❌ Server startup: FAILED - {e}")
            return False
    
    async def validate_mcp_tools(self) -> bool:
        """Test 2: All 20 MCP tools are available"""
        logger.info("🔍 Testing MCP tools availability...")
        
        expected_tools = [
            "create_v0_session", "generate_with_v0", "continue_v0_session",
            "get_v0_session_files", "create_v0_frame_preview", "list_v0_sessions",
            "generate_component", "generate_and_create_component", "create_v0_project",
            "list_v0_projects", "get_v0_project_by_id", "assign_project_to_chat",
            "initialize_chat_from_repo", "initialize_chat_from_files", "create_v0_deployment",
            "get_deployment_status", "get_deployment_logs", "fork_v0_chat",
            "update_chat_metadata", "favorite_chat"
        ]
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.server_url}/tools") as response:
                    if response.status == 200:
                        tools_data = await response.json()
                        available_tools = [tool["name"] for tool in tools_data.get("tools", [])]
                        
                        missing_tools = set(expected_tools) - set(available_tools)
                        extra_tools = set(available_tools) - set(expected_tools)
                        
                        if len(available_tools) == 20 and not missing_tools:
                            self.results["test_results"]["mcp_tools"] = {
                                "status": "PASSED",
                                "message": f"All {len(available_tools)} MCP tools available",
                                "available_tools": available_tools
                            }
                            logger.info(f"✅ MCP tools: PASSED - {len(available_tools)} tools available")
                            return True
                        else:
                            self.results["test_results"]["mcp_tools"] = {
                                "status": "FAILED",
                                "message": f"Expected 20 tools, found {len(available_tools)}",
                                "missing_tools": list(missing_tools),
                                "extra_tools": list(extra_tools)
                            }
                            logger.error(f"❌ MCP tools: FAILED - Missing: {missing_tools}")
                            return False
        except Exception as e:
            self.results["test_results"]["mcp_tools"] = {
                "status": "FAILED",
                "message": f"Failed to retrieve tools: {e}"
            }
            logger.error(f"❌ MCP tools: FAILED - {e}")
            return False
    
    async def validate_api_connectivity(self) -> bool:
        """Test 3: V0 API connectivity"""
        logger.info("🔍 Testing V0 API connectivity...")
        
        try:
            # Test session creation (lightweight test)
            test_payload = {
                "context": {"test": True, "validation": "deployment"}
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.server_url}/create_session",
                    json=test_payload,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        session_data = await response.json()
                        self.results["test_results"]["api_connectivity"] = {
                            "status": "PASSED",
                            "message": "V0 API connectivity confirmed",
                            "session_id": session_data.get("session_id")
                        }
                        logger.info("✅ API connectivity: PASSED")
                        return True
        except Exception as e:
            self.results["test_results"]["api_connectivity"] = {
                "status": "FAILED",
                "message": f"V0 API connectivity failed: {e}"
            }
            logger.error(f"❌ API connectivity: FAILED - {e}")
            return False
    
    async def validate_persistence_layer(self) -> bool:
        """Test 4: Data persistence functionality"""
        logger.info("🔍 Testing persistence layer...")
        
        try:
            # Check if persistence directories exist and are writable
            persist_dir = Path.home() / ".mcp-persistent"
            
            if not persist_dir.exists():
                persist_dir.mkdir(parents=True, exist_ok=True)
            
            # Test file creation
            test_file = persist_dir / "deployment-test.json"
            test_data = {"test": True, "timestamp": time.time()}
            
            with open(test_file, 'w') as f:
                json.dump(test_data, f)
            
            # Test file reading
            with open(test_file, 'r') as f:
                read_data = json.load(f)
            
            # Cleanup
            test_file.unlink()
            
            self.results["test_results"]["persistence_layer"] = {
                "status": "PASSED",
                "message": "Persistence layer functional",
                "persist_dir": str(persist_dir)
            }
            logger.info("✅ Persistence layer: PASSED")
            return True
            
        except Exception as e:
            self.results["test_results"]["persistence_layer"] = {
                "status": "FAILED",
                "message": f"Persistence layer failed: {e}"
            }
            logger.error(f"❌ Persistence layer: FAILED - {e}")
            return False
    
    async def validate_performance(self) -> bool:
        """Test 5: Performance benchmarks"""
        logger.info("🔍 Testing performance benchmarks...")
        
        try:
            # Test response time
            start_time = time.time()
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.server_url}/health") as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200 and response_time < 2.0:
                        self.results["test_results"]["performance"] = {
                            "status": "PASSED",
                            "message": f"Response time acceptable: {response_time:.3f}s",
                            "response_time": response_time
                        }
                        self.results["performance_metrics"]["response_time"] = response_time
                        logger.info(f"✅ Performance: PASSED - {response_time:.3f}s response time")
                        return True
                    else:
                        self.results["test_results"]["performance"] = {
                            "status": "FAILED",
                            "message": f"Response time too slow: {response_time:.3f}s"
                        }
                        logger.error(f"❌ Performance: FAILED - {response_time:.3f}s response time")
                        return False
        except Exception as e:
            self.results["test_results"]["performance"] = {
                "status": "FAILED",
                "message": f"Performance test failed: {e}"
            }
            logger.error(f"❌ Performance: FAILED - {e}")
            return False
    
    async def validate_concurrent_requests(self) -> bool:
        """Test 6: Concurrent request handling"""
        logger.info("🔍 Testing concurrent request handling...")
        
        try:
            async def make_request(session, i):
                async with session.get(f"{self.server_url}/health?req={i}") as response:
                    return response.status == 200
            
            # Test 10 concurrent requests
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                tasks = [make_request(session, i) for i in range(10)]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                duration = time.time() - start_time
                
                successful_requests = sum(1 for r in results if r is True)
                
                if successful_requests >= 8:  # Allow 2 failures
                    self.results["test_results"]["concurrent_requests"] = {
                        "status": "PASSED",
                        "message": f"{successful_requests}/10 concurrent requests successful",
                        "duration": duration,
                        "success_rate": successful_requests / 10
                    }
                    logger.info(f"✅ Concurrent requests: PASSED - {successful_requests}/10 successful")
                    return True
                else:
                    self.results["test_results"]["concurrent_requests"] = {
                        "status": "FAILED",
                        "message": f"Only {successful_requests}/10 requests successful"
                    }
                    logger.error(f"❌ Concurrent requests: FAILED - {successful_requests}/10 successful")
                    return False
        except Exception as e:
            self.results["test_results"]["concurrent_requests"] = {
                "status": "FAILED",
                "message": f"Concurrent request test failed: {e}"
            }
            logger.error(f"❌ Concurrent requests: FAILED - {e}")
            return False
    
    async def run_validation(self) -> Dict[str, Any]:
        """Run complete deployment validation"""
        logger.info("🚀 Starting Enhanced V0 MCP Server deployment validation...")
        
        validation_tests = [
            ("Server Startup", self.validate_server_startup),
            ("MCP Tools", self.validate_mcp_tools),
            ("API Connectivity", self.validate_api_connectivity),
            ("Persistence Layer", self.validate_persistence_layer),
            ("Performance", self.validate_performance),
            ("Concurrent Requests", self.validate_concurrent_requests)
        ]
        
        for test_name, test_func in validation_tests:
            try:
                success = await test_func()
                if success:
                    self.results["tests_passed"] += 1
                else:
                    self.results["tests_failed"] += 1
            except Exception as e:
                logger.error(f"❌ {test_name}: EXCEPTION - {e}")
                self.results["tests_failed"] += 1
                self.results["test_results"][test_name.lower().replace(" ", "_")] = {
                    "status": "EXCEPTION",
                    "message": str(e)
                }
        
        # Determine overall status
        total_tests = len(validation_tests)
        if self.results["tests_passed"] == total_tests:
            self.results["overall_status"] = "PASSED"
            self.results["deployment_ready"] = True
            logger.info("🎉 ALL VALIDATION TESTS PASSED - DEPLOYMENT READY\!")
        elif self.results["tests_passed"] >= total_tests * 0.8:  # 80% pass rate
            self.results["overall_status"] = "MOSTLY_PASSED"
            self.results["deployment_ready"] = True
            logger.warning("⚠️ MOST VALIDATION TESTS PASSED - DEPLOYMENT READY WITH WARNINGS")
        else:
            self.results["overall_status"] = "FAILED"
            self.results["deployment_ready"] = False
            logger.error("❌ VALIDATION FAILED - DEPLOYMENT NOT READY")
        
        return self.results

async def main():
    """Main deployment validation"""
    validator = DeploymentValidator()
    results = await validator.run_validation()
    
    # Save results
    results_file = Path("deployment-validation-results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    logger.info(f"📋 Validation results saved to {results_file}")
    
    # Print summary
    print("\n" + "="*60)
    print("ENHANCED V0 MCP SERVER - DEPLOYMENT VALIDATION SUMMARY")
    print("="*60)
    print(f"Overall Status: {results['overall_status']}")
    print(f"Tests Passed: {results['tests_passed']}")
    print(f"Tests Failed: {results['tests_failed']}")
    print(f"Deployment Ready: {'✅ YES' if results['deployment_ready'] else '❌ NO'}")
    print("="*60)
    
    # Exit with appropriate code
    sys.exit(0 if results["deployment_ready"] else 1)

if __name__ == "__main__":
    asyncio.run(main())

EOF < /dev/null
