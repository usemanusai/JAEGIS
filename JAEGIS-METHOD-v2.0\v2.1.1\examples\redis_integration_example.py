"""
P.I.T.C.E.S. Framework - Redis Integration Example
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component Integration

This example demonstrates the complete Redis vector integration with the P.I.T.C.E.S. framework,
including vector-based decision making, advanced caching, real-time streams, and monitoring.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any

# P.I.T.C.E.S. Core Components
from pitces.core.enhanced_controller import EnhancedPITCESController
from pitces.core.models import ProjectSpecs, Task, Priority, TaskStatus, WorkflowType
from pitces.config.redis_integration_config import RedisIntegrationConfig
from pitces.monitoring.redis_monitoring_dashboard import RedisMonitoringDashboard


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PITCESRedisIntegrationDemo:
    """
    Comprehensive demonstration of P.I.T.C.E.S. Redis vector integration.
    
    This demo showcases:
    - Enhanced workflow selection with vector similarity
    - Advanced caching with multi-tier storage
    - Real-time task management with Redis Streams
    - Intelligent gap analysis with pattern recognition
    - Performance monitoring and optimization
    """
    
    def __init__(self):
        """Initialize the demo with enhanced P.I.T.C.E.S. controller."""
        # Load configuration (development mode for demo)
        self.config = RedisIntegrationConfig.get_development_config()
        
        # Initialize enhanced controller
        self.controller = EnhancedPITCESController(self.config.to_dict())
        
        # Monitoring dashboard
        self.dashboard = None
        
        logger.info("P.I.T.C.E.S. Redis Integration Demo initialized")
    
    async def run_complete_demo(self):
        """Run the complete Redis integration demonstration."""
        try:
            logger.info("Starting P.I.T.C.E.S. Redis Integration Demo")
            
            # Step 1: Initialize enhanced features
            await self._initialize_enhanced_features()
            
            # Step 2: Demonstrate vector-based workflow selection
            await self._demo_vector_workflow_selection()
            
            # Step 3: Demonstrate enhanced caching
            await self._demo_enhanced_caching()
            
            # Step 4: Demonstrate Redis Streams integration
            await self._demo_redis_streams()
            
            # Step 5: Demonstrate gap analysis with vector similarity
            await self._demo_vector_gap_analysis()
            
            # Step 6: Demonstrate performance monitoring
            await self._demo_performance_monitoring()
            
            # Step 7: Demonstrate optimization features
            await self._demo_optimization_features()
            
            # Step 8: Generate comprehensive report
            await self._generate_demo_report()
            
            logger.info("P.I.T.C.E.S. Redis Integration Demo completed successfully")
            
        except Exception as e:
            logger.error(f"Demo failed: {e}")
            raise
    
    async def _initialize_enhanced_features(self):
        """Initialize all enhanced Redis features."""
        logger.info("Initializing enhanced P.I.T.C.E.S. features...")
        
        # Initialize enhanced controller features
        success = await self.controller.initialize_enhanced_features()
        
        if not success:
            raise RuntimeError("Failed to initialize enhanced features")
        
        # Initialize monitoring dashboard
        self.dashboard = RedisMonitoringDashboard(
            vector_engine=self.controller.vector_engine,
            caching_layer=self.controller.caching_layer,
            streams_manager=self.controller.streams_manager,
            cluster_manager=self.controller.cluster_manager,
            context_engine=self.controller.enhanced_context_engine
        )
        
        await self.dashboard.start_monitoring()
        
        logger.info("Enhanced features initialized successfully")
    
    async def _demo_vector_workflow_selection(self):
        """Demonstrate vector-based workflow selection."""
        logger.info("Demonstrating vector-based workflow selection...")
        
        # Create sample project specifications
        projects = [
            ProjectSpecs(
                task_count=25,
                requirements_clarity=90.0,
                complexity_score=3,
                risk_level='LOW',
                team_size=5,
                technology_stack=['Python', 'React'],
                external_dependencies=['Redis', 'PostgreSQL']
            ),
            ProjectSpecs(
                task_count=150,
                requirements_clarity=60.0,
                complexity_score=8,
                risk_level='HIGH',
                team_size=12,
                technology_stack=['Java', 'Angular', 'Microservices'],
                external_dependencies=['Kafka', 'Elasticsearch', 'MongoDB']
            ),
            ProjectSpecs(
                task_count=75,
                requirements_clarity=85.0,
                complexity_score=5,
                risk_level='MEDIUM',
                team_size=8,
                technology_stack=['Python', 'Vue.js'],
                external_dependencies=['Redis', 'MySQL']
            )
        ]
        
        # Demonstrate workflow selection for each project
        for i, project in enumerate(projects, 1):
            logger.info(f"Selecting workflow for Project {i}...")
            
            # First selection (no vector similarity available)
            workflow_type = await self.controller.select_workflow_enhanced(
                project, use_vector_similarity=True
            )
            
            logger.info(f"Project {i}: Selected workflow = {workflow_type.value}")
            
            # Simulate some delay
            await asyncio.sleep(1)
        
        # Now demonstrate similarity-based selection
        logger.info("Demonstrating similarity-based workflow selection...")
        
        # Create a similar project to the first one
        similar_project = ProjectSpecs(
            task_count=30,  # Similar to first project
            requirements_clarity=88.0,
            complexity_score=3,
            risk_level='LOW',
            team_size=6,
            technology_stack=['Python', 'React'],
            external_dependencies=['Redis', 'PostgreSQL']
        )
        
        # This should find similarity with the first project
        workflow_type = await self.controller.select_workflow_enhanced(
            similar_project, use_vector_similarity=True, similarity_threshold=0.8
        )
        
        logger.info(f"Similar project: Selected workflow = {workflow_type.value} (using vector similarity)")
    
    async def _demo_enhanced_caching(self):
        """Demonstrate enhanced caching capabilities."""
        logger.info("Demonstrating enhanced caching capabilities...")
        
        if not self.controller.caching_layer:
            logger.warning("Caching layer not available")
            return
        
        # Create sample tasks for caching demo
        tasks = [
            Task(
                name=f"Demo Task {i}",
                description=f"Sample task {i} for caching demonstration",
                priority=Priority.MEDIUM,
                estimated_duration_hours=2.0
            )
            for i in range(1, 6)
        ]
        
        # Cache task contexts
        logger.info("Caching task contexts...")
        for task in tasks:
            success = await self.controller.enhanced_context_engine.save_task_context_enhanced(
                task, include_vector=True
            )
            logger.info(f"Cached task {task.name}: {'Success' if success else 'Failed'}")
        
        # Demonstrate cache retrieval
        logger.info("Retrieving cached contexts...")
        for task in tasks[:3]:  # Retrieve first 3 tasks
            context = await self.controller.enhanced_context_engine.load_task_context_enhanced(
                task.id, include_similar=True
            )
            
            if context:
                source = context.get('source', 'unknown')
                logger.info(f"Retrieved {task.name} from {source}")
            else:
                logger.warning(f"Failed to retrieve {task.name}")
        
        # Demonstrate cache warming
        logger.info("Demonstrating cache warming...")
        warming_stats = await self.controller.caching_layer.warm_cache_patterns()
        logger.info(f"Cache warming completed: {warming_stats}")
        
        # Get cache metrics
        cache_metrics = self.controller.caching_layer.get_cache_metrics()
        logger.info(f"Cache performance: {cache_metrics['hit_ratio']:.1f}% hit ratio")
    
    async def _demo_redis_streams(self):
        """Demonstrate Redis Streams integration."""
        logger.info("Demonstrating Redis Streams integration...")
        
        if not self.controller.streams_manager:
            logger.warning("Streams manager not available")
            return
        
        # Publish various types of messages
        logger.info("Publishing messages to Redis Streams...")
        
        # Task priority message
        sample_task = Task(
            name="Stream Demo Task",
            description="Task for streams demonstration",
            priority=Priority.HIGH
        )
        
        await self.controller.streams_manager.publish_task_priority_message(
            sample_task, Priority.CRITICAL, {'reason': 'urgent_requirement'}
        )
        
        # Workflow decision message
        await self.controller.streams_manager.publish_workflow_decision_message(
            {'task_count': 50, 'complexity': 'medium'},
            WorkflowType.CI_AR,
            {'decision_method': 'enhanced_algorithm'}
        )
        
        # System event message
        await self.controller.streams_manager.publish_system_event_message(
            'demo_event',
            {'component': 'redis_integration', 'status': 'active'},
            'INFO'
        )
        
        # Get stream metrics
        stream_metrics = await self.controller.streams_manager.get_stream_metrics()
        logger.info(f"Stream metrics: {stream_metrics['messages_published']} messages published")
    
    async def _demo_vector_gap_analysis(self):
        """Demonstrate gap analysis with vector similarity."""
        logger.info("Demonstrating vector-based gap analysis...")
        
        # Create sample project for gap analysis
        project = ProjectSpecs(
            task_count=100,
            requirements_clarity=75.0,
            complexity_score=6,
            risk_level='MEDIUM',
            team_size=10,
            technology_stack=['Python', 'React', 'PostgreSQL'],
            external_dependencies=['Redis', 'Elasticsearch']
        )
        
        # Create sample tasks
        tasks = [
            Task(
                name=f"Analysis Task {i}",
                description=f"Task {i} for gap analysis",
                priority=Priority.MEDIUM
            )
            for i in range(1, 11)
        ]
        
        # Run enhanced gap analysis
        analysis_results = await self.controller.run_enhanced_gap_analysis(
            project, tasks, use_similar_analyses=True
        )
        
        logger.info("Gap analysis completed:")
        logger.info(f"- Analysis domains: {len(analysis_results['analysis_results'])}")
        logger.info(f"- Similar analyses found: {len(analysis_results['similar_analyses'])}")
        logger.info(f"- Vector stored: {analysis_results['vector_stored']}")
        logger.info(f"- Results cached: {analysis_results['cached']}")
    
    async def _demo_performance_monitoring(self):
        """Demonstrate performance monitoring capabilities."""
        logger.info("Demonstrating performance monitoring...")
        
        if not self.dashboard:
            logger.warning("Monitoring dashboard not available")
            return
        
        # Get comprehensive dashboard data
        dashboard_data = await self.dashboard.get_dashboard_data()
        
        logger.info("Dashboard Data Summary:")
        logger.info(f"- Components monitored: {len(dashboard_data.get('components', {}))}")
        logger.info(f"- Active alerts: {len(dashboard_data.get('alerts', {}).get('active', []))}")
        logger.info(f"- System health score: {dashboard_data.get('system_health', 0):.1f}")
        
        # Get specific analytics
        if self.controller.vector_engine:
            vector_analytics = await self.dashboard.get_vector_analytics()
            logger.info(f"Vector search performance: {vector_analytics.get('search_performance', {})}")
        
        if self.controller.caching_layer:
            cache_analytics = await self.dashboard.get_cache_analytics()
            logger.info(f"Cache performance: {cache_analytics.get('performance', {})}")
        
        if self.controller.streams_manager:
            stream_analytics = await self.dashboard.get_stream_analytics()
            logger.info(f"Stream performance: {stream_analytics.get('message_flow', {})}")
    
    async def _demo_optimization_features(self):
        """Demonstrate optimization features."""
        logger.info("Demonstrating optimization features...")
        
        # Run performance optimization
        optimization_results = await self.controller.optimize_performance()
        
        logger.info("Optimization Results:")
        logger.info(f"- Cache optimization: {optimization_results.get('cache_optimization', {})}")
        logger.info(f"- Overall improvement: {optimization_results.get('overall_improvement', 0):.2f}%")
        
        # Demonstrate context synchronization
        if self.controller.enhanced_context_engine:
            sync_results = await self.controller.enhanced_context_engine.synchronize_contexts()
            logger.info(f"Context synchronization: {sync_results}")
        
        # Demonstrate cache optimization
        if self.controller.caching_layer:
            cache_optimization = await self.controller.caching_layer.optimize_cache_performance()
            logger.info(f"Cache optimization: {cache_optimization}")
    
    async def _generate_demo_report(self):
        """Generate comprehensive demo report."""
        logger.info("Generating comprehensive demo report...")
        
        # Get comprehensive metrics
        metrics = self.controller.get_comprehensive_metrics()
        
        # Generate performance report
        if self.dashboard:
            performance_report = await self.dashboard.generate_performance_report(time_range_hours=1)
            
            logger.info("Demo Performance Report:")
            logger.info(f"- Report period: {performance_report.get('report_period', {})}")
            logger.info(f"- System health: {performance_report.get('system_health_score', 0):.1f}")
            logger.info(f"- Recommendations: {len(performance_report.get('optimization_recommendations', []))}")
        
        # Log final metrics summary
        logger.info("Final Metrics Summary:")
        logger.info(f"- Enhanced operations: {metrics.get('enhanced_controller', {}).get('total_enhanced_operations', 0)}")
        logger.info(f"- Vector decisions: {metrics.get('enhanced_controller', {}).get('vector_decisions', 0)}")
        logger.info(f"- Performance improvements: {metrics.get('enhanced_controller', {}).get('performance_improvements', 0):.2f}%")
    
    async def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up demo resources...")
        
        if self.dashboard:
            await self.dashboard.stop_monitoring()
        
        # Additional cleanup would go here
        logger.info("Demo cleanup completed")


async def main():
    """Main demo function."""
    demo = PITCESRedisIntegrationDemo()
    
    try:
        await demo.run_complete_demo()
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        raise
    finally:
        await demo.cleanup()


if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
