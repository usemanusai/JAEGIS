# Mandatory Web Research Protocol
## Comprehensive Research Framework Required Before Any Task Creation or Implementation

### Research Protocol Overview
**Date**: 24 July 2025 (Auto-updating daily)  
**Protocol Purpose**: Enforce mandatory comprehensive web research before any task creation or implementation  
**Protocol Scope**: All workflow initiation, task creation, and implementation activities  
**Research Authority**: Absolute authority to halt all activities until research is completed  

---

## 🔍 **MANDATORY RESEARCH REQUIREMENTS**

### **Research Execution Framework**
```yaml
mandatory_research_framework:
  research_query_requirements:
    minimum_queries: "10 targeted research queries (minimum)"
    optimal_queries: "15-20 comprehensive research queries"
    query_diversity: "Multiple perspectives and sources required"
    current_date_context: "All research must include current date context (24 July 2025)"
    
  research_quality_standards:
    source_diversity: "Minimum 5 different authoritative sources"
    information_currency: "All information must be current and relevant"
    depth_requirements: "Comprehensive analysis, not surface-level information"
    evidence_validation: "All claims must be supported by evidence"
    
  research_analysis_requirements:
    data_synthesis: "Comprehensive synthesis of all research findings"
    pattern_identification: "Identification of patterns and trends"
    gap_analysis: "Analysis of information gaps and uncertainties"
    actionable_insights: "Generation of actionable insights and recommendations"
```

### **Research Implementation System**
```python
# Mandatory Web Research Protocol Implementation
class MandatoryWebResearchProtocol:
    def __init__(self):
        self.research_engine = ComprehensiveResearchEngine()
        self.query_generator = IntelligentQueryGenerator()
        self.data_analyzer = ResearchDataAnalyzer()
        self.validation_system = ResearchValidationSystem()
        self.halt_controller = ActivityHaltController()
        
    async def execute_mandatory_research(self, workflow_request):
        """Execute mandatory research before allowing any task creation"""
        # Halt all task creation until research is complete
        await self.halt_controller.halt_task_creation(workflow_request)
        
        # Generate comprehensive research queries
        research_queries = await self.query_generator.generate_research_queries(
            workflow_request, 
            minimum_queries=10,
            optimal_queries=20,
            current_date="24 July 2025"
        )
        
        # Execute research queries
        research_results = []
        for query in research_queries:
            result = await self.research_engine.execute_research_query(query)
            research_results.append(result)
            
            # Add delay between queries to respect rate limits
            await asyncio.sleep(2)
        
        # Analyze and synthesize research data
        research_analysis = await self.data_analyzer.analyze_research_data(
            research_results, workflow_request
        )
        
        # Validate research completeness and quality
        research_validation = await self.validation_system.validate_research_quality(
            research_analysis
        )
        
        if research_validation.meets_standards:
            # Generate evidence-based tasks from research
            evidence_based_tasks = await self.generate_evidence_based_tasks(
                research_analysis, workflow_request
            )
            
            # Authorize task creation with research foundation
            return ResearchCompletionAuthorization(
                research_completed=True,
                research_analysis=research_analysis,
                evidence_based_tasks=evidence_based_tasks,
                task_creation_authorized=True,
                authorization_timestamp=datetime.now()
            )
        else:
            # Require additional research
            return ResearchInsufficientResult(
                research_insufficient=True,
                validation_failures=research_validation.failures,
                additional_research_required=research_validation.additional_requirements,
                task_creation_blocked=True
            )
    
    async def generate_research_queries(self, workflow_context):
        """Generate comprehensive research queries with current date context"""
        base_queries = [
            f"Latest developments in {workflow_context.domain} as of July 2025",
            f"Current best practices for {workflow_context.objective} in 2025",
            f"Recent innovations and trends in {workflow_context.field} July 2025",
            f"Current challenges and solutions in {workflow_context.area} 2025",
            f"State-of-the-art approaches to {workflow_context.goal} as of July 2025"
        ]
        
        # Generate additional specific queries based on context
        specific_queries = await self.query_generator.generate_context_specific_queries(
            workflow_context, current_date="24 July 2025"
        )
        
        # Generate validation and verification queries
        validation_queries = await self.query_generator.generate_validation_queries(
            workflow_context, current_date="24 July 2025"
        )
        
        all_queries = base_queries + specific_queries + validation_queries
        
        # Ensure minimum query count
        if len(all_queries) < 10:
            additional_queries = await self.query_generator.generate_additional_queries(
                workflow_context, target_count=15
            )
            all_queries.extend(additional_queries)
        
        return all_queries[:20]  # Limit to maximum 20 queries
    
    async def validate_research_before_task_creation(self, task_creation_request):
        """Validate that research has been completed before allowing task creation"""
        research_validation = await self.validation_system.validate_research_completion(
            task_creation_request
        )
        
        if not research_validation.research_completed:
            # Block task creation and initiate research
            await self.halt_controller.block_task_creation(task_creation_request)
            
            research_requirement = ResearchRequirement(
                workflow_id=task_creation_request.workflow_id,
                required_research_queries=10,
                current_date_context_required=True,
                evidence_based_task_creation_required=True,
                blocking_reason="Mandatory research not completed"
            )
            
            return TaskCreationBlocked(
                blocked=True,
                research_requirement=research_requirement,
                task_creation_request=task_creation_request
            )
        
        return TaskCreationAuthorized(
            authorized=True,
            research_foundation=research_validation.research_analysis,
            task_creation_request=task_creation_request
        )
```

---

## 📊 **RESEARCH QUALITY VALIDATION**

### **Research Quality Standards**
```yaml
research_quality_standards:
  source_quality_requirements:
    authoritative_sources: "Minimum 5 authoritative and credible sources"
    source_diversity: "Multiple types of sources (academic, industry, news, official)"
    source_currency: "All sources must be current and up-to-date"
    source_reliability: "Sources must be verified for reliability and accuracy"
    
  information_quality_requirements:
    information_currency: "All information must reflect current state (July 2025)"
    information_depth: "Comprehensive coverage, not superficial information"
    information_accuracy: "All claims must be verifiable and accurate"
    information_relevance: "All information must be directly relevant to the task"
    
  analysis_quality_requirements:
    comprehensive_synthesis: "All research findings must be synthesized comprehensively"
    pattern_recognition: "Patterns and trends must be identified and analyzed"
    gap_identification: "Information gaps and uncertainties must be identified"
    actionable_insights: "Research must generate actionable insights and recommendations"
    
  evidence_validation_requirements:
    claim_verification: "All claims must be supported by evidence"
    source_cross_validation: "Information must be validated across multiple sources"
    bias_assessment: "Potential biases in sources must be identified and addressed"
    uncertainty_acknowledgment: "Uncertainties and limitations must be acknowledged"
```

### **Research Validation Framework**
```yaml
research_validation_framework:
  automated_validation_checks:
    query_count_validation: "Verify minimum 10 queries executed"
    source_diversity_validation: "Verify minimum 5 different sources"
    currency_validation: "Verify all information includes current date context"
    quality_validation: "Verify research meets quality standards"
    
  manual_validation_requirements:
    expert_review: "Research analysis reviewed by domain experts"
    quality_assessment: "Comprehensive quality assessment of research findings"
    relevance_validation: "Validation of research relevance to task objectives"
    completeness_verification: "Verification of research completeness and thoroughness"
    
  validation_criteria:
    minimum_passing_score: "80% overall quality score required"
    mandatory_requirements: "All mandatory requirements must be met"
    quality_thresholds: "All quality thresholds must be exceeded"
    expert_approval: "Expert approval required for complex research"
    
  validation_outcomes:
    research_approved: "Research meets all standards, task creation authorized"
    research_insufficient: "Research requires improvement, task creation blocked"
    additional_research_required: "Additional research queries required"
    expert_review_required: "Expert review required before authorization"
```

---

## 🚫 **ACTIVITY HALT AND CONTROL SYSTEM**

### **Task Creation Halt Protocols**
```yaml
task_creation_halt_protocols:
  automatic_halt_triggers:
    missing_research: "Automatic halt when research not completed"
    insufficient_research: "Automatic halt when research quality insufficient"
    outdated_research: "Automatic halt when research lacks current date context"
    incomplete_analysis: "Automatic halt when research analysis incomplete"
    
  halt_implementation:
    immediate_blocking: "Immediate blocking of all task creation activities"
    workflow_suspension: "Suspension of workflow until research completed"
    notification_system: "Immediate notification of halt and requirements"
    resolution_guidance: "Clear guidance on requirements for resolution"
    
  halt_resolution_requirements:
    research_completion: "Complete execution of 10-20 research queries"
    quality_validation: "Research must pass all quality validation checks"
    analysis_completion: "Comprehensive analysis and synthesis required"
    evidence_based_foundation: "Evidence-based foundation for task creation required"
    
  authorization_restoration:
    validation_confirmation: "Confirmation that all requirements met"
    quality_approval: "Approval of research quality and completeness"
    task_creation_authorization: "Explicit authorization for task creation"
    monitoring_activation: "Activation of ongoing monitoring for compliance"
```

### **Evidence-Based Task Creation Framework**
```yaml
evidence_based_task_creation:
  research_to_task_transformation:
    research_analysis_integration: "Research findings integrated into task definitions"
    evidence_based_requirements: "Task requirements based on research evidence"
    current_context_integration: "Current date context (July 2025) integrated throughout"
    best_practice_incorporation: "Current best practices incorporated into tasks"
    
  task_validation_against_research:
    research_alignment_validation: "Tasks must align with research findings"
    evidence_support_validation: "All task elements must be supported by evidence"
    currency_validation: "Tasks must reflect current state and best practices"
    feasibility_validation: "Task feasibility validated against research evidence"
    
  continuous_research_integration:
    ongoing_research_updates: "Ongoing integration of new research findings"
    task_refinement: "Continuous refinement of tasks based on new evidence"
    best_practice_updates: "Regular updates to incorporate latest best practices"
    currency_maintenance: "Continuous maintenance of current date context"
```

**Mandatory Web Research Protocol Status**: ✅ **IMPLEMENTED AND ENFORCED**  
**Research Requirements**: ✅ **10-20 QUERIES WITH CURRENT DATE CONTEXT (24 JULY 2025)**  
**Task Creation Control**: ✅ **ALL TASK CREATION HALTED UNTIL RESEARCH COMPLETE**  
**Quality Standards**: ✅ **COMPREHENSIVE VALIDATION AND EVIDENCE-BASED REQUIREMENTS**  
**Activity Halt System**: ✅ **AUTOMATIC HALT AND CONTROL PROTOCOLS OPERATIONAL**
