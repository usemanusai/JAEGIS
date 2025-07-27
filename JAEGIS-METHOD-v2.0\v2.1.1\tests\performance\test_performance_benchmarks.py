"""
Performance Testing & Benchmarking for N.L.D.S.
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

Comprehensive performance tests to validate response time requirements (<500ms)
and capacity requirements (1000 req/min) for the N.L.D.S. system.
"""

import pytest
import asyncio
import time
import statistics
import concurrent.futures
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
import psutil
import threading
import queue
import json

from nlds.processing import ProcessingOrchestrator
from nlds.analysis import AnalysisOrchestrator
from nlds.translation import TranslationOrchestrator
from nlds.integration import NLDSIntegrationOrchestrator
from nlds.api import create_test_client


class PerformanceMetrics:
    """Performance metrics collection and analysis."""
    
    def __init__(self):
        self.response_times = []
        self.throughput_data = []
        self.error_rates = []
        self.resource_usage = []
        self.start_time = None
        self.end_time = None
    
    def start_measurement(self):
        """Start performance measurement."""
        self.start_time = time.time()
        self.response_times.clear()
        self.throughput_data.clear()
        self.error_rates.clear()
        self.resource_usage.clear()
    
    def record_response_time(self, response_time_ms: float):
        """Record response time."""
        self.response_times.append(response_time_ms)
    
    def record_throughput(self, requests_per_second: float):
        """Record throughput."""
        self.throughput_data.append(requests_per_second)
    
    def record_error_rate(self, error_rate: float):
        """Record error rate."""
        self.error_rates.append(error_rate)
    
    def record_resource_usage(self):
        """Record current resource usage."""
        cpu_percent = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        
        self.resource_usage.append({
            "timestamp": time.time(),
            "cpu_percent": cpu_percent,
            "memory_percent": memory_info.percent,
            "memory_used_mb": memory_info.used / (1024 * 1024)
        })
    
    def end_measurement(self):
        """End performance measurement."""
        self.end_time = time.time()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        if not self.response_times:
            return {"error": "No data collected"}
        
        return {
            "response_times": {
                "min_ms": min(self.response_times),
                "max_ms": max(self.response_times),
                "mean_ms": statistics.mean(self.response_times),
                "median_ms": statistics.median(self.response_times),
                "p95_ms": self._percentile(self.response_times, 95),
                "p99_ms": self._percentile(self.response_times, 99),
                "std_dev_ms": statistics.stdev(self.response_times) if len(self.response_times) > 1 else 0
            },
            "throughput": {
                "max_rps": max(self.throughput_data) if self.throughput_data else 0,
                "mean_rps": statistics.mean(self.throughput_data) if self.throughput_data else 0,
                "total_requests": len(self.response_times),
                "duration_seconds": self.end_time - self.start_time if self.end_time and self.start_time else 0
            },
            "error_rates": {
                "max_error_rate": max(self.error_rates) if self.error_rates else 0,
                "mean_error_rate": statistics.mean(self.error_rates) if self.error_rates else 0
            },
            "resource_usage": {
                "max_cpu_percent": max(r["cpu_percent"] for r in self.resource_usage) if self.resource_usage else 0,
                "mean_cpu_percent": statistics.mean(r["cpu_percent"] for r in self.resource_usage) if self.resource_usage else 0,
                "max_memory_mb": max(r["memory_used_mb"] for r in self.resource_usage) if self.resource_usage else 0,
                "mean_memory_mb": statistics.mean(r["memory_used_mb"] for r in self.resource_usage) if self.resource_usage else 0
            }
        }
    
    def _percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile."""
        sorted_data = sorted(data)
        index = int((percentile / 100) * len(sorted_data))
        return sorted_data[min(index, len(sorted_data) - 1)]


class LoadGenerator:
    """Load generator for performance testing."""
    
    def __init__(self, target_function, max_workers: int = 10):
        self.target_function = target_function
        self.max_workers = max_workers
        self.results_queue = queue.Queue()
        self.stop_event = threading.Event()
    
    async def generate_constant_load(self, requests_per_second: int, duration_seconds: int) -> List[Dict[str, Any]]:
        """Generate constant load for specified duration."""
        results = []
        interval = 1.0 / requests_per_second
        end_time = time.time() + duration_seconds
        
        while time.time() < end_time:
            start_time = time.time()
            
            try:
                result = await self.target_function()
                response_time = (time.time() - start_time) * 1000
                
                results.append({
                    "success": True,
                    "response_time_ms": response_time,
                    "timestamp": start_time
                })
            except Exception as e:
                response_time = (time.time() - start_time) * 1000
                results.append({
                    "success": False,
                    "response_time_ms": response_time,
                    "error": str(e),
                    "timestamp": start_time
                })
            
            # Wait for next request
            elapsed = time.time() - start_time
            sleep_time = max(0, interval - elapsed)
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
        
        return results
    
    async def generate_burst_load(self, burst_size: int, burst_interval: float, num_bursts: int) -> List[Dict[str, Any]]:
        """Generate burst load pattern."""
        results = []
        
        for burst in range(num_bursts):
            # Generate burst
            burst_tasks = []
            for _ in range(burst_size):
                burst_tasks.append(self._execute_request())
            
            burst_results = await asyncio.gather(*burst_tasks, return_exceptions=True)
            
            for result in burst_results:
                if isinstance(result, Exception):
                    results.append({
                        "success": False,
                        "response_time_ms": 0,
                        "error": str(result),
                        "timestamp": time.time()
                    })
                else:
                    results.append(result)
            
            # Wait between bursts
            if burst < num_bursts - 1:
                await asyncio.sleep(burst_interval)
        
        return results
    
    async def _execute_request(self) -> Dict[str, Any]:
        """Execute single request."""
        start_time = time.time()
        
        try:
            result = await self.target_function()
            response_time = (time.time() - start_time) * 1000
            
            return {
                "success": True,
                "response_time_ms": response_time,
                "timestamp": start_time,
                "result": result
            }
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return {
                "success": False,
                "response_time_ms": response_time,
                "error": str(e),
                "timestamp": start_time
            }


class TestProcessingPerformance:
    """Test processing component performance."""
    
    @pytest.fixture
    def processing_orchestrator(self, sample_config):
        """Create processing orchestrator for testing."""
        return ProcessingOrchestrator(sample_config["processing"])
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_single_request_response_time(self, processing_orchestrator):
        """Test single request response time meets <500ms requirement."""
        input_text = "Analyze market trends for renewable energy sector and provide strategic recommendations"
        
        # Measure response time
        start_time = time.time()
        result = await processing_orchestrator.process_input(input_text)
        response_time_ms = (time.time() - start_time) * 1000
        
        # Verify response time requirement
        assert response_time_ms < 500, f"Response time {response_time_ms}ms exceeds 500ms requirement"
        assert result.success
        assert result.confidence_score > 0.0
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_processing_throughput_capacity(self, processing_orchestrator):
        """Test processing throughput meets 1000 req/min capacity."""
        metrics = PerformanceMetrics()
        metrics.start_measurement()
        
        # Create load generator
        async def process_request():
            return await processing_orchestrator.process_input("Test input for throughput testing")
        
        load_generator = LoadGenerator(process_request)
        
        # Generate load for 60 seconds at target rate
        target_rps = 1000 / 60  # 1000 requests per minute = ~16.67 RPS
        results = await load_generator.generate_constant_load(
            requests_per_second=int(target_rps),
            duration_seconds=60
        )
        
        metrics.end_measurement()
        
        # Analyze results
        successful_requests = [r for r in results if r["success"]]
        total_requests = len(results)
        success_rate = len(successful_requests) / total_requests if total_requests > 0 else 0
        
        # Record metrics
        for result in successful_requests:
            metrics.record_response_time(result["response_time_ms"])
        
        summary = metrics.get_summary()
        
        # Verify capacity requirements
        assert total_requests >= 900, f"Only processed {total_requests} requests, expected ~1000"
        assert success_rate >= 0.95, f"Success rate {success_rate:.2%} below 95% threshold"
        assert summary["response_times"]["p95_ms"] < 500, f"P95 response time {summary['response_times']['p95_ms']}ms exceeds 500ms"
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_concurrent_request_handling(self, processing_orchestrator):
        """Test concurrent request handling performance."""
        num_concurrent = 50
        input_texts = [f"Test concurrent processing request {i}" for i in range(num_concurrent)]
        
        # Execute concurrent requests
        start_time = time.time()
        tasks = [processing_orchestrator.process_input(text) for text in input_texts]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        total_time = time.time() - start_time
        
        # Analyze results
        successful_results = [r for r in results if not isinstance(r, Exception)]
        success_rate = len(successful_results) / len(results)
        
        # Verify concurrent handling
        assert success_rate >= 0.95, f"Concurrent success rate {success_rate:.2%} below 95%"
        assert total_time < 10.0, f"Concurrent processing took {total_time:.2f}s, expected <10s"
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_memory_usage_under_load(self, processing_orchestrator):
        """Test memory usage under sustained load."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / (1024 * 1024)  # MB
        
        # Generate sustained load
        for i in range(100):
            await processing_orchestrator.process_input(f"Memory test input {i}")
            
            # Check memory every 10 requests
            if i % 10 == 0:
                current_memory = process.memory_info().rss / (1024 * 1024)
                memory_increase = current_memory - initial_memory
                
                # Memory increase should be reasonable
                assert memory_increase < 100, f"Memory increased by {memory_increase:.1f}MB, limit is 100MB"
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_processing_scalability(self, processing_orchestrator):
        """Test processing scalability with increasing load."""
        load_levels = [10, 25, 50, 100]  # Requests per test
        results_by_load = {}
        
        for load_level in load_levels:
            metrics = PerformanceMetrics()
            metrics.start_measurement()
            
            # Generate load
            tasks = [
                processing_orchestrator.process_input(f"Scalability test {i}")
                for i in range(load_level)
            ]
            
            start_time = time.time()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            total_time = time.time() - start_time
            
            # Record metrics
            successful_results = [r for r in results if not isinstance(r, Exception)]
            for result in successful_results:
                metrics.record_response_time(result.processing_time_ms)
            
            metrics.end_measurement()
            summary = metrics.get_summary()
            
            results_by_load[load_level] = {
                "total_time": total_time,
                "success_rate": len(successful_results) / len(results),
                "mean_response_time": summary["response_times"]["mean_ms"],
                "p95_response_time": summary["response_times"]["p95_ms"]
            }
        
        # Verify scalability
        for load_level, metrics in results_by_load.items():
            assert metrics["success_rate"] >= 0.95, f"Load {load_level}: Success rate {metrics['success_rate']:.2%} below 95%"
            assert metrics["p95_response_time"] < 1000, f"Load {load_level}: P95 response time {metrics['p95_response_time']}ms too high"


class TestAnalysisPerformance:
    """Test analysis component performance."""
    
    @pytest.fixture
    def analysis_orchestrator(self, sample_config):
        """Create analysis orchestrator for testing."""
        return AnalysisOrchestrator(sample_config["analysis"])
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_analysis_response_time(self, analysis_orchestrator):
        """Test analysis response time requirements."""
        input_text = "Create comprehensive strategic business plan for digital transformation initiative"
        
        # Test different analysis depths
        for depth in range(1, 6):
            start_time = time.time()
            result = await analysis_orchestrator.analyze(input_text, depth_level=depth)
            response_time_ms = (time.time() - start_time) * 1000
            
            # Response time should scale with depth but stay reasonable
            max_time = 500 + (depth * 200)  # Allow more time for deeper analysis
            assert response_time_ms < max_time, f"Depth {depth}: {response_time_ms}ms exceeds {max_time}ms"
            assert result.overall_confidence > 0.0
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_analysis_concurrent_processing(self, analysis_orchestrator):
        """Test concurrent analysis processing."""
        inputs = [
            "Analyze market trends",
            "Create business strategy",
            "Develop innovation plan",
            "Assess risk factors",
            "Optimize operations"
        ] * 10  # 50 total requests
        
        start_time = time.time()
        tasks = [analysis_orchestrator.analyze(inp) for inp in inputs]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        total_time = time.time() - start_time
        
        successful_results = [r for r in results if not isinstance(r, Exception)]
        success_rate = len(successful_results) / len(results)
        
        assert success_rate >= 0.95, f"Analysis concurrent success rate {success_rate:.2%} below 95%"
        assert total_time < 30.0, f"Concurrent analysis took {total_time:.2f}s, expected <30s"


class TestTranslationPerformance:
    """Test translation component performance."""
    
    @pytest.fixture
    def translation_orchestrator(self, sample_config):
        """Create translation orchestrator for testing."""
        return TranslationOrchestrator(sample_config["translation"])
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_translation_response_time(self, translation_orchestrator, sample_analysis_result):
        """Test translation response time meets requirements."""
        start_time = time.time()
        result = await translation_orchestrator.translate(sample_analysis_result)
        response_time_ms = (time.time() - start_time) * 1000
        
        # Translation should be fast (<200ms)
        assert response_time_ms < 200, f"Translation time {response_time_ms}ms exceeds 200ms requirement"
        assert result.success
        assert result.primary_command is not None
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_translation_batch_processing(self, translation_orchestrator):
        """Test translation batch processing performance."""
        # Create multiple analysis results
        analysis_results = [
            Mock(synthesis=Mock(overall_confidence=0.85 + i*0.01))
            for i in range(20)
        ]
        
        start_time = time.time()
        results = await translation_orchestrator.translate_batch(analysis_results)
        total_time = time.time() - start_time
        
        # Batch processing should be efficient
        assert len(results) == len(analysis_results)
        assert total_time < 5.0, f"Batch translation took {total_time:.2f}s, expected <5s"
        
        for result in results:
            assert result.success


class TestAPIPerformance:
    """Test API performance."""
    
    @pytest.fixture
    def api_client(self):
        """Create API test client."""
        return create_test_client()
    
    @pytest.fixture
    def auth_headers(self):
        """Create authentication headers."""
        return {"Authorization": "Bearer nlds_admin_key_001"}
    
    @pytest.mark.performance
    def test_api_endpoint_response_times(self, api_client, auth_headers):
        """Test API endpoint response times."""
        endpoints = [
            ("GET", "/health", {}),
            ("GET", "/status", {}),
            ("POST", "/process", {"input_text": "Test processing", "mode": "standard"}),
            ("POST", "/analyze", {"input_text": "Test analysis", "analysis_types": ["logical"]}),
            ("POST", "/translate", {"input_text": "Test translation", "priority": "normal"})
        ]
        
        for method, endpoint, data in endpoints:
            start_time = time.time()
            
            if method == "GET":
                response = api_client.get(endpoint, headers=auth_headers)
            else:
                response = api_client.post(endpoint, json=data, headers=auth_headers)
            
            response_time_ms = (time.time() - start_time) * 1000
            
            # API endpoints should respond quickly
            max_time = 1000 if endpoint in ["/process", "/analyze", "/translate"] else 100
            assert response_time_ms < max_time, f"{method} {endpoint}: {response_time_ms}ms exceeds {max_time}ms"
            assert response.status_code in [200, 201]
    
    @pytest.mark.performance
    def test_api_concurrent_requests(self, api_client, auth_headers):
        """Test API concurrent request handling."""
        import threading
        import time
        
        results = []
        num_threads = 20
        requests_per_thread = 5
        
        def make_requests():
            thread_results = []
            for i in range(requests_per_thread):
                start_time = time.time()
                response = api_client.post("/process", json={
                    "input_text": f"Concurrent test {i}",
                    "mode": "standard"
                }, headers=auth_headers)
                response_time = (time.time() - start_time) * 1000
                
                thread_results.append({
                    "status_code": response.status_code,
                    "response_time_ms": response_time,
                    "success": response.status_code == 200
                })
            
            results.extend(thread_results)
        
        # Create and start threads
        threads = []
        start_time = time.time()
        
        for _ in range(num_threads):
            thread = threading.Thread(target=make_requests)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        total_time = time.time() - start_time
        
        # Analyze results
        successful_requests = [r for r in results if r["success"]]
        success_rate = len(successful_requests) / len(results)
        mean_response_time = statistics.mean([r["response_time_ms"] for r in successful_requests])
        
        assert success_rate >= 0.95, f"API concurrent success rate {success_rate:.2%} below 95%"
        assert mean_response_time < 2000, f"Mean response time {mean_response_time:.1f}ms too high"
        assert total_time < 60, f"Total concurrent test time {total_time:.1f}s too long"


class TestEndToEndPerformance:
    """Test end-to-end system performance."""
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_complete_pipeline_performance(self, integration_orchestrator):
        """Test complete pipeline performance."""
        input_text = "Analyze renewable energy market trends and create strategic investment recommendations for Q4 2025"
        
        start_time = time.time()
        result = await integration_orchestrator.process_complete_pipeline(
            input_text=input_text,
            user_context={"user_id": "perf_test_user"}
        )
        total_time_ms = (time.time() - start_time) * 1000
        
        # Complete pipeline should execute within 3 seconds
        assert total_time_ms < 3000, f"Complete pipeline took {total_time_ms}ms, expected <3000ms"
        assert result.success
        assert result.jaegis_command is not None
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_system_under_sustained_load(self, integration_orchestrator):
        """Test system performance under sustained load."""
        metrics = PerformanceMetrics()
        metrics.start_measurement()
        
        # Generate sustained load for 5 minutes
        async def process_request():
            return await integration_orchestrator.process_complete_pipeline(
                input_text="Sustained load test input",
                user_context={"user_id": "load_test_user"}
            )
        
        load_generator = LoadGenerator(process_request)
        results = await load_generator.generate_constant_load(
            requests_per_second=5,  # Moderate sustained load
            duration_seconds=300    # 5 minutes
        )
        
        metrics.end_measurement()
        
        # Analyze sustained load results
        successful_requests = [r for r in results if r["success"]]
        success_rate = len(successful_requests) / len(results) if results else 0
        
        # Record response times
        for result in successful_requests:
            metrics.record_response_time(result["response_time_ms"])
        
        summary = metrics.get_summary()
        
        # Verify sustained performance
        assert success_rate >= 0.95, f"Sustained load success rate {success_rate:.2%} below 95%"
        assert summary["response_times"]["p95_ms"] < 5000, f"P95 response time {summary['response_times']['p95_ms']}ms too high under load"
        assert len(results) >= 1400, f"Only processed {len(results)} requests in 5 minutes, expected ~1500"
