"""
Load Testing & Stress Testing for N.L.D.S.
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Comprehensive load and stress testing to validate system behavior under
extreme conditions and identify breaking points.
"""

import pytest
import asyncio
import time
import statistics
import psutil
import gc
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import queue
import random

from nlds.integration import NLDSIntegrationOrchestrator
from nlds.api import create_test_client


class StressTestMetrics:
    """Metrics collection for stress testing."""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.request_data = []
        self.system_metrics = []
        self.error_log = []
        self.peak_metrics = {
            "max_response_time": 0,
            "max_cpu_usage": 0,
            "max_memory_usage": 0,
            "max_concurrent_requests": 0
        }
    
    def start_monitoring(self):
        """Start stress test monitoring."""
        self.start_time = time.time()
        self.request_data.clear()
        self.system_metrics.clear()
        self.error_log.clear()
        
        # Start system monitoring thread
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_system, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop stress test monitoring."""
        self.end_time = time.time()
        self.monitoring_active = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=1)
    
    def record_request(self, success: bool, response_time_ms: float, error: str = None):
        """Record request result."""
        self.request_data.append({
            "timestamp": time.time(),
            "success": success,
            "response_time_ms": response_time_ms,
            "error": error
        })
        
        # Update peak metrics
        if response_time_ms > self.peak_metrics["max_response_time"]:
            self.peak_metrics["max_response_time"] = response_time_ms
    
    def record_error(self, error_type: str, error_message: str):
        """Record error."""
        self.error_log.append({
            "timestamp": time.time(),
            "error_type": error_type,
            "error_message": error_message
        })
    
    def _monitor_system(self):
        """Monitor system resources."""
        while self.monitoring_active:
            try:
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                
                metric = {
                    "timestamp": time.time(),
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "memory_used_mb": memory.used / (1024 * 1024),
                    "memory_available_mb": memory.available / (1024 * 1024)
                }
                
                self.system_metrics.append(metric)
                
                # Update peak metrics
                if cpu_percent > self.peak_metrics["max_cpu_usage"]:
                    self.peak_metrics["max_cpu_usage"] = cpu_percent
                if memory.percent > self.peak_metrics["max_memory_usage"]:
                    self.peak_metrics["max_memory_usage"] = memory.percent
                
            except Exception as e:
                self.record_error("monitoring", str(e))
            
            time.sleep(1)
    
    def get_stress_summary(self) -> Dict[str, Any]:
        """Get stress test summary."""
        if not self.request_data:
            return {"error": "No request data collected"}
        
        successful_requests = [r for r in self.request_data if r["success"]]
        failed_requests = [r for r in self.request_data if not r["success"]]
        
        total_duration = self.end_time - self.start_time if self.end_time and self.start_time else 0
        
        return {
            "test_duration_seconds": total_duration,
            "total_requests": len(self.request_data),
            "successful_requests": len(successful_requests),
            "failed_requests": len(failed_requests),
            "success_rate": len(successful_requests) / len(self.request_data) if self.request_data else 0,
            "requests_per_second": len(self.request_data) / total_duration if total_duration > 0 else 0,
            "response_times": {
                "min_ms": min(r["response_time_ms"] for r in successful_requests) if successful_requests else 0,
                "max_ms": max(r["response_time_ms"] for r in successful_requests) if successful_requests else 0,
                "mean_ms": statistics.mean(r["response_time_ms"] for r in successful_requests) if successful_requests else 0,
                "p95_ms": self._percentile([r["response_time_ms"] for r in successful_requests], 95) if successful_requests else 0,
                "p99_ms": self._percentile([r["response_time_ms"] for r in successful_requests], 99) if successful_requests else 0
            },
            "peak_metrics": self.peak_metrics,
            "system_metrics": {
                "max_cpu_percent": max(m["cpu_percent"] for m in self.system_metrics) if self.system_metrics else 0,
                "mean_cpu_percent": statistics.mean(m["cpu_percent"] for m in self.system_metrics) if self.system_metrics else 0,
                "max_memory_mb": max(m["memory_used_mb"] for m in self.system_metrics) if self.system_metrics else 0,
                "mean_memory_mb": statistics.mean(m["memory_used_mb"] for m in self.system_metrics) if self.system_metrics else 0
            },
            "error_summary": {
                "total_errors": len(self.error_log),
                "error_types": list(set(e["error_type"] for e in self.error_log))
            }
        }
    
    def _percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile."""
        if not data:
            return 0
        sorted_data = sorted(data)
        index = int((percentile / 100) * len(sorted_data))
        return sorted_data[min(index, len(sorted_data) - 1)]


class TestLoadTesting:
    """Load testing scenarios."""
    
    @pytest.mark.performance
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_sustained_high_load(self, integration_orchestrator):
        """Test system under sustained high load."""
        metrics = StressTestMetrics()
        metrics.start_monitoring()
        
        try:
            # High sustained load: 50 RPS for 10 minutes
            target_rps = 50
            duration_seconds = 600  # 10 minutes
            total_requests = target_rps * duration_seconds
            
            # Generate load
            semaphore = asyncio.Semaphore(100)  # Limit concurrent requests
            
            async def make_request(request_id: int):
                async with semaphore:
                    start_time = time.time()
                    try:
                        result = await integration_orchestrator.process_complete_pipeline(
                            input_text=f"High load test request {request_id}",
                            user_context={"user_id": f"load_user_{request_id % 100}"}
                        )
                        response_time = (time.time() - start_time) * 1000
                        metrics.record_request(True, response_time)
                        return result
                    except Exception as e:
                        response_time = (time.time() - start_time) * 1000
                        metrics.record_request(False, response_time, str(e))
                        raise
            
            # Execute requests with controlled rate
            tasks = []
            start_time = time.time()
            
            for i in range(total_requests):
                # Control request rate
                expected_time = start_time + (i / target_rps)
                current_time = time.time()
                if current_time < expected_time:
                    await asyncio.sleep(expected_time - current_time)
                
                task = asyncio.create_task(make_request(i))
                tasks.append(task)
                
                # Process completed tasks periodically
                if len(tasks) >= 100:
                    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                    tasks = list(pending)
            
            # Wait for remaining tasks
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
            
        finally:
            metrics.stop_monitoring()
        
        # Analyze results
        summary = metrics.get_stress_summary()
        
        # Verify load test results
        assert summary["success_rate"] >= 0.90, f"Success rate {summary['success_rate']:.2%} below 90% under high load"
        assert summary["response_times"]["p95_ms"] < 5000, f"P95 response time {summary['response_times']['p95_ms']}ms too high"
        assert summary["system_metrics"]["max_cpu_percent"] < 90, f"CPU usage {summary['system_metrics']['max_cpu_percent']}% too high"
    
    @pytest.mark.performance
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_burst_load_handling(self, integration_orchestrator):
        """Test system handling of burst loads."""
        metrics = StressTestMetrics()
        metrics.start_monitoring()
        
        try:
            # Burst pattern: 200 requests every 30 seconds, 10 bursts
            burst_size = 200
            burst_interval = 30
            num_bursts = 10
            
            for burst in range(num_bursts):
                print(f"Executing burst {burst + 1}/{num_bursts}")
                
                # Generate burst
                burst_tasks = []
                for i in range(burst_size):
                    async def make_burst_request(req_id=i):
                        start_time = time.time()
                        try:
                            result = await integration_orchestrator.process_complete_pipeline(
                                input_text=f"Burst test request {req_id}",
                                user_context={"user_id": f"burst_user_{req_id % 50}"}
                            )
                            response_time = (time.time() - start_time) * 1000
                            metrics.record_request(True, response_time)
                            return result
                        except Exception as e:
                            response_time = (time.time() - start_time) * 1000
                            metrics.record_request(False, response_time, str(e))
                            return None
                    
                    burst_tasks.append(make_burst_request())
                
                # Execute burst
                burst_start = time.time()
                results = await asyncio.gather(*burst_tasks, return_exceptions=True)
                burst_duration = time.time() - burst_start
                
                print(f"Burst {burst + 1} completed in {burst_duration:.2f}s")
                
                # Wait between bursts (except last one)
                if burst < num_bursts - 1:
                    await asyncio.sleep(burst_interval)
            
        finally:
            metrics.stop_monitoring()
        
        # Analyze burst test results
        summary = metrics.get_stress_summary()
        
        # Verify burst handling
        assert summary["success_rate"] >= 0.85, f"Burst success rate {summary['success_rate']:.2%} below 85%"
        assert summary["response_times"]["p99_ms"] < 10000, f"P99 response time {summary['response_times']['p99_ms']}ms too high during bursts"
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_api_load_testing(self):
        """Test API under load using HTTP client."""
        import requests
        import threading
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        api_client = create_test_client()
        auth_headers = {"Authorization": "Bearer nlds_admin_key_001"}
        
        metrics = StressTestMetrics()
        metrics.start_monitoring()
        
        try:
            # Load test parameters
            num_threads = 20
            requests_per_thread = 50
            total_requests = num_threads * requests_per_thread
            
            def make_api_requests(thread_id: int):
                thread_results = []
                for i in range(requests_per_thread):
                    start_time = time.time()
                    try:
                        response = api_client.post("/process", json={
                            "input_text": f"API load test {thread_id}-{i}",
                            "mode": "standard"
                        }, headers=auth_headers)
                        
                        response_time = (time.time() - start_time) * 1000
                        success = response.status_code == 200
                        
                        metrics.record_request(success, response_time, 
                                             None if success else f"HTTP {response.status_code}")
                        
                        thread_results.append({
                            "success": success,
                            "response_time_ms": response_time,
                            "status_code": response.status_code
                        })
                        
                    except Exception as e:
                        response_time = (time.time() - start_time) * 1000
                        metrics.record_request(False, response_time, str(e))
                        thread_results.append({
                            "success": False,
                            "response_time_ms": response_time,
                            "error": str(e)
                        })
                
                return thread_results
            
            # Execute load test
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = [executor.submit(make_api_requests, i) for i in range(num_threads)]
                
                all_results = []
                for future in as_completed(futures):
                    thread_results = future.result()
                    all_results.extend(thread_results)
            
        finally:
            metrics.stop_monitoring()
        
        # Analyze API load test results
        summary = metrics.get_stress_summary()
        
        # Verify API load handling
        assert summary["success_rate"] >= 0.95, f"API load success rate {summary['success_rate']:.2%} below 95%"
        assert summary["response_times"]["mean_ms"] < 2000, f"Mean API response time {summary['response_times']['mean_ms']}ms too high"


class TestStressTesting:
    """Stress testing to find breaking points."""
    
    @pytest.mark.performance
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_memory_stress(self, integration_orchestrator):
        """Test system behavior under memory stress."""
        metrics = StressTestMetrics()
        metrics.start_monitoring()
        
        try:
            # Generate large inputs to stress memory
            large_inputs = [
                "A" * 5000 + f" Memory stress test {i} " + "B" * 5000
                for i in range(100)
            ]
            
            # Process large inputs concurrently
            semaphore = asyncio.Semaphore(20)
            
            async def process_large_input(input_text: str, req_id: int):
                async with semaphore:
                    start_time = time.time()
                    try:
                        result = await integration_orchestrator.process_complete_pipeline(
                            input_text=input_text,
                            user_context={"user_id": f"memory_stress_{req_id}"}
                        )
                        response_time = (time.time() - start_time) * 1000
                        metrics.record_request(True, response_time)
                        return result
                    except Exception as e:
                        response_time = (time.time() - start_time) * 1000
                        metrics.record_request(False, response_time, str(e))
                        return None
            
            # Execute memory stress test
            tasks = [
                process_large_input(input_text, i)
                for i, input_text in enumerate(large_inputs)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Force garbage collection
            gc.collect()
            
        finally:
            metrics.stop_monitoring()
        
        # Analyze memory stress results
        summary = metrics.get_stress_summary()
        
        # Verify memory handling
        assert summary["success_rate"] >= 0.80, f"Memory stress success rate {summary['success_rate']:.2%} below 80%"
        assert summary["system_metrics"]["max_memory_mb"] < 2000, f"Memory usage {summary['system_metrics']['max_memory_mb']}MB too high"
    
    @pytest.mark.performance
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_connection_stress(self, integration_orchestrator):
        """Test system under connection stress."""
        metrics = StressTestMetrics()
        metrics.start_monitoring()
        
        try:
            # Simulate many concurrent connections
            num_connections = 500
            connection_duration = 60  # seconds
            
            async def simulate_connection(conn_id: int):
                """Simulate a persistent connection making requests."""
                connection_start = time.time()
                request_count = 0
                
                while time.time() - connection_start < connection_duration:
                    start_time = time.time()
                    try:
                        result = await integration_orchestrator.process_complete_pipeline(
                            input_text=f"Connection {conn_id} request {request_count}",
                            user_context={"user_id": f"conn_user_{conn_id}"}
                        )
                        response_time = (time.time() - start_time) * 1000
                        metrics.record_request(True, response_time)
                        request_count += 1
                        
                        # Random delay between requests
                        await asyncio.sleep(random.uniform(0.5, 2.0))
                        
                    except Exception as e:
                        response_time = (time.time() - start_time) * 1000
                        metrics.record_request(False, response_time, str(e))
                        await asyncio.sleep(1)  # Back off on error
                
                return request_count
            
            # Create many concurrent connections
            connection_tasks = [
                simulate_connection(i) for i in range(num_connections)
            ]
            
            # Execute with limited concurrency to avoid overwhelming
            semaphore = asyncio.Semaphore(100)
            
            async def limited_connection(conn_id: int):
                async with semaphore:
                    return await simulate_connection(conn_id)
            
            limited_tasks = [limited_connection(i) for i in range(num_connections)]
            results = await asyncio.gather(*limited_tasks, return_exceptions=True)
            
        finally:
            metrics.stop_monitoring()
        
        # Analyze connection stress results
        summary = metrics.get_stress_summary()
        
        # Verify connection handling
        assert summary["success_rate"] >= 0.75, f"Connection stress success rate {summary['success_rate']:.2%} below 75%"
        assert summary["system_metrics"]["max_cpu_percent"] < 95, f"CPU usage {summary['system_metrics']['max_cpu_percent']}% too high under connection stress"
    
    @pytest.mark.performance
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_error_cascade_resilience(self, integration_orchestrator):
        """Test system resilience to error cascades."""
        metrics = StressTestMetrics()
        metrics.start_monitoring()
        
        try:
            # Mix of normal and error-inducing requests
            normal_requests = [f"Normal request {i}" for i in range(50)]
            error_requests = [
                "",  # Empty input
                "A" * 20000,  # Too long
                None,  # Invalid input
                "🚀" * 1000,  # Unicode stress
            ] * 25  # 100 error requests
            
            all_requests = normal_requests + error_requests
            random.shuffle(all_requests)
            
            # Process mixed requests
            async def process_mixed_request(input_text, req_id: int):
                start_time = time.time()
                try:
                    if input_text is None:
                        raise ValueError("None input")
                    
                    result = await integration_orchestrator.process_complete_pipeline(
                        input_text=input_text,
                        user_context={"user_id": f"error_test_{req_id}"}
                    )
                    response_time = (time.time() - start_time) * 1000
                    metrics.record_request(True, response_time)
                    return result
                except Exception as e:
                    response_time = (time.time() - start_time) * 1000
                    metrics.record_request(False, response_time, str(e))
                    return None
            
            # Execute mixed requests
            tasks = [
                process_mixed_request(req, i)
                for i, req in enumerate(all_requests)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
        finally:
            metrics.stop_monitoring()
        
        # Analyze error resilience
        summary = metrics.get_stress_summary()
        
        # System should handle errors gracefully
        # Success rate should be around 33% (50 normal out of 150 total)
        expected_success_rate = 50 / 150
        actual_success_rate = summary["success_rate"]
        
        assert actual_success_rate >= expected_success_rate * 0.8, f"Error resilience test: success rate {actual_success_rate:.2%} too low"
        assert summary["response_times"]["p95_ms"] < 5000, f"Error handling response time {summary['response_times']['p95_ms']}ms too high"
