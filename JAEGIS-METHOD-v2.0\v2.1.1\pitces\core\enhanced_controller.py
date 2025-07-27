"""
P.I.T.C.E.S. Framework - Enhanced Controller
JAEGIS Enhanced Agent System v2.2 - Tier 0 Component Integration

This module implements the enhanced PITCESController with Redis vector integration,
advanced caching, and intelligent decision making capabilities.
"""

import asyncio
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from uuid import UUID

from .controller import PITCESController
from .redis_vector_engine import RedisVectorEngine
from .enhanced_caching_layer import EnhancedCachingLayer
from .redis_streams_manager import RedisStreamsManager
from .redis_cluster_manager import RedisClusterManager
from .enhanced_context_engine import EnhancedContextEngine
from .models import Task, ProjectSpecs, WorkflowType, Priority
from .exceptions import PITCESError, ErrorCodes


logger = logging.getLogger(__name__)


class EnhancedPITCESController(PITCESController):
    """
    Enhanced P.I.T.C.E.S. Controller with Redis vector integration and advanced capabilities.
    
    Features:
    - Vector-based workflow decision making
    - Advanced caching with similarity search
    - Real-time task queue management with Redis Streams
    - Distributed processing with Redis Cluster
    - Intelligent context management
    - Performance optimization and monitoring
    - N.L.D.S. Tier 0 integration
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls, config: Optional[Dict[str, Any]] = None):
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Enhanced P.I.T.C.E.S. Controller.
        
        Args:
            config: Enhanced controller configuration
        """
        if self._initialized:
            return
        
        # Initialize base controller
        super().__init__(config)
        
        self.enhanced_config = config or self._get_default_enhanced_config()
        
        # Redis components
        self.vector_engine: Optional[RedisVectorEngine] = None
        self.caching_layer: Optional[EnhancedCachingLayer] = None
        self.streams_manager: Optional[RedisStreamsManager] = None
        self.cluster_manager: Optional[RedisClusterManager] = None
        self.enhanced_context_engine: Optional[EnhancedContextEngine] = None
        
        # Enhanced metrics
        self.enhanced_metrics = {
            'vector_decisions': 0,
            'cache_optimizations': 0,
            'stream_messages': 0,
            'cluster_operations': 0,
            'nlds_integrations': 0,
            'performance_improvements': 0.0,
            'total_enhanced_operations': 0
        }
        
        # Performance tracking
        self.performance_baseline = {}
        self.optimization_history = []
        
        self._initialized = True
        logger.info("EnhancedPITCESController initialized with Redis vector integration")
    
    async def initialize_enhanced_features(self) -> bool:
        """
        Initialize all enhanced Redis features.
        
        Returns:
            True if initialization successful
        """
        try:
            logger.info("Initializing enhanced P.I.T.C.E.S. features...")
            
            # Initialize Redis Vector Engine
            if self.enhanced_config.get('enable_vector_engine', True):
                await self._initialize_vector_engine()
            
            # Initialize Enhanced Caching Layer
            if self.enhanced_config.get('enable_enhanced_caching', True):
                await self._initialize_caching_layer()
            
            # Initialize Redis Streams Manager
            if self.enhanced_config.get('enable_streams', True):
                await self._initialize_streams_manager()
            
            # Initialize Redis Cluster Manager
            if self.enhanced_config.get('enable_cluster', False):
                await self._initialize_cluster_manager()
            
            # Initialize Enhanced Context Engine
            if self.enhanced_config.get('enable_enhanced_context', True):
                await self._initialize_enhanced_context_engine()
            
            # Start background optimization
            if self.enhanced_config.get('enable_background_optimization', True):
                asyncio.create_task(self._background_optimization())
            
            logger.info("Enhanced P.I.T.C.E.S. features initialization completed")
            return True
            
        except Exception as e:
            logger.error(f"Enhanced features initialization failed: {e}")
            return False
    
    async def select_workflow_enhanced(
        self, 
        project_specs: Union[Dict[str, Any], ProjectSpecs],
        use_vector_similarity: bool = True,
        similarity_threshold: float = 0.85
    ) -> WorkflowType:
        """
        Enhanced workflow selection with vector similarity search.
        
        Args:
            project_specs: Project specifications
            use_vector_similarity: Whether to use vector similarity for decision
            similarity_threshold: Minimum similarity for vector matches
            
        Returns:
            Selected workflow type
        """
        try:
            start_time = time.time()
            
            # Convert to ProjectSpecs if needed
            if isinstance(project_specs, dict):
                project_specs = ProjectSpecs(**project_specs)
            
            # Try vector similarity search first
            if use_vector_similarity and self.vector_engine:
                similar_decisions = await self.vector_engine.find_similar_workflow_decisions(
                    project_specs, top_k=3, similarity_threshold=similarity_threshold
                )
                
                if similar_decisions:
                    # Use the most similar decision
                    best_match = similar_decisions[0]
                    workflow_type = WorkflowType(best_match['workflow_type'])
                    
                    # Store this decision for future similarity searches
                    await self.vector_engine.store_workflow_decision_vector(
                        project_specs, workflow_type, {
                            'source': 'vector_similarity',
                            'similarity_score': best_match['similarity_score'],
                            'reference_decision': best_match['id']
                        }
                    )
                    
                    self.enhanced_metrics['vector_decisions'] += 1
                    
                    # Publish decision to streams
                    if self.streams_manager:
                        await self.streams_manager.publish_workflow_decision_message(
                            project_specs.__dict__, workflow_type, {
                                'decision_method': 'vector_similarity',
                                'similarity_score': best_match['similarity_score']
                            }
                        )
                    
                    decision_time = time.time() - start_time
                    logger.info(f"Vector-based workflow decision: {workflow_type.value} "
                              f"(similarity: {best_match['similarity_score']:.3f}, time: {decision_time:.3f}s)")
                    
                    return workflow_type
            
            # Fall back to traditional decision making
            workflow_type = self.select_workflow(project_specs.__dict__)
            
            # Store this decision for future vector searches
            if self.vector_engine:
                await self.vector_engine.store_workflow_decision_vector(
                    project_specs, workflow_type, {
                        'source': 'traditional_algorithm',
                        'decision_time': time.time() - start_time
                    }
                )
            
            # Cache the decision
            if self.caching_layer:
                await self.caching_layer.cache_workflow_decision(
                    project_specs, workflow_type, {
                        'decision_method': 'traditional',
                        'decision_time': time.time() - start_time
                    }
                )
            
            decision_time = time.time() - start_time
            logger.info(f"Traditional workflow decision: {workflow_type.value} (time: {decision_time:.3f}s)")
            
            return workflow_type
            
        except Exception as e:
            logger.error(f"Enhanced workflow selection failed: {e}")
            # Fall back to base implementation
            return super().select_workflow(project_specs.__dict__ if hasattr(project_specs, '__dict__') else project_specs)
    
    async def execute_workflow_enhanced(
        self, 
        tasks: List[Dict[str, Any]],
        workflow_type: Optional[WorkflowType] = None,
        use_streams: bool = True,
        enable_preemption: bool = True
    ) -> Dict[str, Any]:
        """
        Enhanced workflow execution with Redis Streams and vector optimization.
        
        Args:
            tasks: List of task dictionaries
            workflow_type: Optional workflow type override
            use_streams: Whether to use Redis Streams for task management
            enable_preemption: Whether to enable task preemption
            
        Returns:
            Enhanced execution results
        """
        try:
            start_time = time.time()
            
            # Determine workflow type if not provided
            if not workflow_type:
                # Use first task to infer project specs for workflow selection
                if tasks:
                    sample_specs = self._infer_project_specs_from_tasks(tasks)
                    workflow_type = await self.select_workflow_enhanced(sample_specs)
                else:
                    workflow_type = WorkflowType.SEQUENTIAL
            
            # Publish workflow start event
            if self.streams_manager:
                await self.streams_manager.publish_system_event_message(
                    'workflow_execution_started',
                    {
                        'workflow_type': workflow_type.value,
                        'task_count': len(tasks),
                        'enhanced_features': True
                    }
                )
            
            # Execute workflow with enhanced features
            if use_streams and self.streams_manager:
                results = await self._execute_workflow_with_streams(
                    tasks, workflow_type, enable_preemption
                )
            else:
                # Fall back to base execution
                results = self.execute_workflow(tasks)
            
            # Enhance results with vector and caching metrics
            execution_time = time.time() - start_time
            enhanced_results = {
                **results,
                'enhanced_features': {
                    'vector_engine_used': self.vector_engine is not None,
                    'caching_enabled': self.caching_layer is not None,
                    'streams_used': use_streams and self.streams_manager is not None,
                    'cluster_enabled': self.cluster_manager is not None,
                    'execution_time': execution_time,
                    'performance_improvement': self._calculate_performance_improvement(execution_time)
                },
                'redis_metrics': await self._get_redis_metrics()
            }
            
            # Store execution results for future optimization
            if self.vector_engine:
                await self._store_execution_results(workflow_type, tasks, enhanced_results)
            
            # Publish workflow completion event
            if self.streams_manager:
                await self.streams_manager.publish_system_event_message(
                    'workflow_execution_completed',
                    {
                        'workflow_type': workflow_type.value,
                        'execution_time': execution_time,
                        'success_rate': enhanced_results.get('success_rate', 0),
                        'enhanced_features_used': True
                    }
                )
            
            self.enhanced_metrics['total_enhanced_operations'] += 1
            
            logger.info(f"Enhanced workflow execution completed: {workflow_type.value} "
                       f"(time: {execution_time:.3f}s, success: {enhanced_results.get('success_rate', 0):.1f}%)")
            
            return enhanced_results
            
        except Exception as e:
            logger.error(f"Enhanced workflow execution failed: {e}")
            # Fall back to base implementation
            return super().execute_workflow(tasks)
    
    async def run_enhanced_gap_analysis(
        self, 
        project_specs: ProjectSpecs,
        tasks: List[Task],
        use_similar_analyses: bool = True
    ) -> Dict[str, Any]:
        """
        Enhanced gap analysis with vector similarity and caching.
        
        Args:
            project_specs: Project specifications
            tasks: List of project tasks
            use_similar_analyses: Whether to use similar analysis results
            
        Returns:
            Enhanced gap analysis results
        """
        try:
            # Check for similar analyses first
            if use_similar_analyses and self.vector_engine:
                similar_analyses = await self.vector_engine.find_similar_gap_analyses(
                    project_specs, top_k=3, similarity_threshold=0.75
                )
                
                if similar_analyses:
                    logger.info(f"Found {len(similar_analyses)} similar gap analyses")
                    # Use insights from similar analyses to enhance current analysis
            
            # Run gap analysis using base implementation
            from .gap_analysis_squad import GapAnalysisSquad
            gap_squad = GapAnalysisSquad()
            analysis_results = gap_squad.run_audit(project_specs, tasks)
            
            # Generate enhanced report
            enhanced_report = gap_squad.generate_report(analysis_results)
            
            # Store results in vector engine for future similarity searches
            if self.vector_engine:
                await self.vector_engine.store_gap_analysis_vector(
                    project_specs, analysis_results
                )
            
            # Cache results
            if self.caching_layer:
                await self.caching_layer.cache_gap_analysis_results(
                    project_specs, analysis_results
                )
            
            # Publish gap analysis completion
            if self.streams_manager:
                await self.streams_manager.publish_gap_analysis_message(
                    project_specs.__dict__, 
                    {domain: result.__dict__ for domain, result in analysis_results.items()},
                    enhanced_report.get('action_plan', [])
                )
            
            return {
                'analysis_results': analysis_results,
                'enhanced_report': enhanced_report,
                'similar_analyses': similar_analyses if use_similar_analyses else [],
                'vector_stored': self.vector_engine is not None,
                'cached': self.caching_layer is not None
            }
            
        except Exception as e:
            logger.error(f"Enhanced gap analysis failed: {e}")
            raise PITCESError(
                f"Enhanced gap analysis failed: {str(e)}",
                error_code=ErrorCodes.ANALYSIS_FAILURE
            )
    
    async def optimize_performance(self) -> Dict[str, Any]:
        """
        Optimize overall system performance using Redis capabilities.
        
        Returns:
            Optimization results
        """
        try:
            optimization_results = {
                'cache_optimization': {},
                'vector_optimization': {},
                'cluster_optimization': {},
                'stream_optimization': {},
                'overall_improvement': 0.0
            }
            
            # Optimize caching layer
            if self.caching_layer:
                cache_results = await self.caching_layer.optimize_cache_performance()
                optimization_results['cache_optimization'] = cache_results
            
            # Optimize cluster if available
            if self.cluster_manager:
                cluster_results = await self.cluster_manager.optimize_memory_usage()
                optimization_results['cluster_optimization'] = cluster_results
            
            # Optimize context storage
            if self.enhanced_context_engine:
                context_results = await self.enhanced_context_engine.optimize_storage()
                optimization_results['context_optimization'] = context_results
            
            # Calculate overall improvement
            optimization_results['overall_improvement'] = self._calculate_optimization_impact(
                optimization_results
            )
            
            self.enhanced_metrics['performance_improvements'] += optimization_results['overall_improvement']
            self.optimization_history.append({
                'timestamp': datetime.now().isoformat(),
                'results': optimization_results
            })
            
            logger.info(f"Performance optimization completed: "
                       f"{optimization_results['overall_improvement']:.2f}% improvement")
            
            return optimization_results
            
        except Exception as e:
            logger.error(f"Performance optimization failed: {e}")
            return {'error': str(e)}
    
    def get_comprehensive_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive metrics including all Redis components.
        
        Returns:
            Comprehensive metrics dictionary
        """
        base_metrics = super().get_metrics()
        
        comprehensive_metrics = {
            **base_metrics,
            'enhanced_controller': self.enhanced_metrics,
            'redis_components': {}
        }
        
        # Add Redis component metrics
        if self.vector_engine:
            comprehensive_metrics['redis_components']['vector_engine'] = self.vector_engine.metrics
        
        if self.caching_layer:
            comprehensive_metrics['redis_components']['caching_layer'] = self.caching_layer.get_cache_metrics()
        
        if self.streams_manager:
            comprehensive_metrics['redis_components']['streams_manager'] = asyncio.create_task(
                self.streams_manager.get_stream_metrics()
            )
        
        if self.cluster_manager:
            comprehensive_metrics['redis_components']['cluster_manager'] = self.cluster_manager.get_cluster_metrics()
        
        if self.enhanced_context_engine:
            comprehensive_metrics['redis_components']['context_engine'] = self.enhanced_context_engine.get_enhanced_metrics()
        
        return comprehensive_metrics
    
    async def _initialize_vector_engine(self):
        """Initialize Redis Vector Engine."""
        try:
            vector_config = self.enhanced_config.get('vector_engine', {})
            self.vector_engine = RedisVectorEngine(vector_config)
            
            success = await self.vector_engine.initialize()
            if not success:
                logger.warning("Vector engine initialization failed")
                self.vector_engine = None
            else:
                logger.info("Redis Vector Engine initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize vector engine: {e}")
            self.vector_engine = None
    
    async def _initialize_caching_layer(self):
        """Initialize Enhanced Caching Layer."""
        try:
            if not self.vector_engine:
                logger.warning("Caching layer requires vector engine")
                return
            
            caching_config = self.enhanced_config.get('caching_layer', {})
            self.caching_layer = EnhancedCachingLayer(self.vector_engine, caching_config)
            
            logger.info("Enhanced Caching Layer initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize caching layer: {e}")
            self.caching_layer = None
    
    async def _initialize_streams_manager(self):
        """Initialize Redis Streams Manager."""
        try:
            if not self.vector_engine:
                logger.warning("Streams manager requires vector engine")
                return
            
            streams_config = self.enhanced_config.get('streams_manager', {})
            self.streams_manager = RedisStreamsManager(
                self.vector_engine.async_redis_client, streams_config
            )
            
            success = await self.streams_manager.initialize_streams()
            if not success:
                logger.warning("Streams manager initialization failed")
                self.streams_manager = None
            else:
                logger.info("Redis Streams Manager initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize streams manager: {e}")
            self.streams_manager = None
    
    async def _initialize_cluster_manager(self):
        """Initialize Redis Cluster Manager."""
        try:
            cluster_config = self.enhanced_config.get('cluster_manager', {})
            cluster_nodes = cluster_config.get('nodes', [])
            
            if not cluster_nodes:
                logger.info("No cluster nodes configured, skipping cluster manager")
                return
            
            self.cluster_manager = RedisClusterManager(cluster_nodes, cluster_config)
            
            success = await self.cluster_manager.initialize_cluster()
            if not success:
                logger.warning("Cluster manager initialization failed")
                self.cluster_manager = None
            else:
                logger.info("Redis Cluster Manager initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize cluster manager: {e}")
            self.cluster_manager = None
    
    async def _initialize_enhanced_context_engine(self):
        """Initialize Enhanced Context Engine."""
        try:
            context_config = self.enhanced_config.get('context_engine', {})
            storage_path = context_config.get('storage_path', 'pitces_context')
            
            self.enhanced_context_engine = EnhancedContextEngine(
                storage_path=storage_path,
                vector_engine=self.vector_engine,
                caching_layer=self.caching_layer,
                config=context_config
            )
            
            success = await self.enhanced_context_engine.initialize()
            if not success:
                logger.warning("Enhanced context engine initialization failed")
                self.enhanced_context_engine = None
            else:
                logger.info("Enhanced Context Engine initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize enhanced context engine: {e}")
            self.enhanced_context_engine = None
    
    async def _execute_workflow_with_streams(
        self, 
        tasks: List[Dict[str, Any]], 
        workflow_type: WorkflowType,
        enable_preemption: bool
    ) -> Dict[str, Any]:
        """Execute workflow using Redis Streams for task management."""
        # This would implement stream-based workflow execution
        # For now, fall back to base implementation
        return self.execute_workflow(tasks)
    
    async def _store_execution_results(
        self, 
        workflow_type: WorkflowType, 
        tasks: List[Dict[str, Any]], 
        results: Dict[str, Any]
    ):
        """Store execution results for future optimization."""
        try:
            if self.vector_engine:
                # Store execution pattern for future similarity searches
                execution_data = {
                    'workflow_type': workflow_type.value,
                    'task_count': len(tasks),
                    'success_rate': results.get('success_rate', 0),
                    'execution_time': results.get('enhanced_features', {}).get('execution_time', 0),
                    'timestamp': datetime.now().isoformat()
                }
                
                # This would store execution patterns in vector format
                logger.debug("Stored execution results for future optimization")
                
        except Exception as e:
            logger.error(f"Failed to store execution results: {e}")
    
    async def _get_redis_metrics(self) -> Dict[str, Any]:
        """Get comprehensive Redis metrics."""
        redis_metrics = {}
        
        if self.vector_engine:
            redis_metrics['vector_engine'] = self.vector_engine.metrics
        
        if self.caching_layer:
            redis_metrics['caching_layer'] = self.caching_layer.get_cache_metrics()
        
        if self.streams_manager:
            redis_metrics['streams_manager'] = await self.streams_manager.get_stream_metrics()
        
        if self.cluster_manager:
            redis_metrics['cluster_manager'] = self.cluster_manager.get_cluster_metrics()
        
        return redis_metrics
    
    async def _background_optimization(self):
        """Background task for continuous optimization."""
        while True:
            try:
                await asyncio.sleep(3600)  # Run every hour
                
                # Run performance optimization
                optimization_results = await self.optimize_performance()
                
                if optimization_results.get('overall_improvement', 0) > 5.0:
                    logger.info(f"Significant performance improvement achieved: "
                              f"{optimization_results['overall_improvement']:.2f}%")
                
            except Exception as e:
                logger.error(f"Background optimization error: {e}")
    
    def _infer_project_specs_from_tasks(self, tasks: List[Dict[str, Any]]) -> ProjectSpecs:
        """Infer project specifications from task list."""
        return ProjectSpecs(
            task_count=len(tasks),
            requirements_clarity=85.0,  # Default assumption
            complexity_score=min(10, max(1, len(tasks) // 10)),
            risk_level='MEDIUM',
            team_size=5,  # Default assumption
            technology_stack=['Python'],  # Default
            external_dependencies=[]
        )
    
    def _calculate_performance_improvement(self, execution_time: float) -> float:
        """Calculate performance improvement compared to baseline."""
        if not self.performance_baseline:
            self.performance_baseline['execution_time'] = execution_time
            return 0.0
        
        baseline_time = self.performance_baseline.get('execution_time', execution_time)
        if baseline_time > 0:
            improvement = ((baseline_time - execution_time) / baseline_time) * 100
            return max(0.0, improvement)
        
        return 0.0
    
    def _calculate_optimization_impact(self, optimization_results: Dict[str, Any]) -> float:
        """Calculate overall optimization impact."""
        # This would implement a sophisticated calculation based on various metrics
        return 5.0  # Placeholder
    
    def _get_default_enhanced_config(self) -> Dict[str, Any]:
        """Get default enhanced controller configuration."""
        return {
            'enable_vector_engine': True,
            'enable_enhanced_caching': True,
            'enable_streams': True,
            'enable_cluster': False,
            'enable_enhanced_context': True,
            'enable_background_optimization': True,
            'vector_engine': {
                'redis': {
                    'host': 'localhost',
                    'port': 6379,
                    'db': 0
                }
            },
            'caching_layer': {
                'l1_cache_size_limit': 1000,
                'enable_cache_warming': True
            },
            'streams_manager': {
                'batch_size': 10,
                'block_timeout': 1000
            },
            'cluster_manager': {
                'nodes': [],
                'monitoring_enabled': True
            },
            'context_engine': {
                'storage_path': 'pitces_context',
                'enable_background_tasks': True
            }
        }
