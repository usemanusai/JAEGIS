# Research Intelligence Sources

## Overview
This data file contains comprehensive information about research sources, query patterns, and intelligence gathering strategies for the Enhanced Agent Creator's research-driven agent generation system.

## Research Source Hierarchy

### Tier 1: Premium Industry Intelligence
```json
{
  "tier_1_sources": {
    "priority": "highest",
    "reliability_score": 0.95,
    "update_frequency": "quarterly",
    "sources": [
      {
        "name": "McKinsey Global Institute",
        "url_patterns": [
          "mckinsey.com/mgi/",
          "mckinsey.com/featured-insights/",
          "mckinsey.com/business-functions/"
        ],
        "search_modifiers": [
          "site:mckinsey.com",
          "McKinsey Global Institute",
          "McKinsey Technology Trends"
        ],
        "content_types": [
          "research reports",
          "industry analysis",
          "technology trends",
          "digital transformation studies"
        ],
        "focus_areas": [
          "AI automation",
          "business transformation",
          "technology adoption",
          "productivity enhancement"
        ]
      },
      {
        "name": "Deloitte Technology Trends",
        "url_patterns": [
          "deloitte.com/insights/",
          "deloitte.com/us/en/insights/focus/tech-trends/"
        ],
        "search_modifiers": [
          "site:deloitte.com",
          "Deloitte Tech Trends",
          "Deloitte Digital"
        ],
        "content_types": [
          "technology trend reports",
          "digital transformation insights",
          "enterprise technology analysis"
        ],
        "focus_areas": [
          "emerging technologies",
          "enterprise automation",
          "digital innovation",
          "technology strategy"
        ]
      },
      {
        "name": "PwC Digital Transformation",
        "url_patterns": [
          "pwc.com/us/en/tech-effect/",
          "pwc.com/us/en/services/consulting/technology/"
        ],
        "search_modifiers": [
          "site:pwc.com",
          "PwC Digital",
          "PwC Technology"
        ],
        "content_types": [
          "digital transformation studies",
          "technology impact analysis",
          "industry digitization reports"
        ],
        "focus_areas": [
          "digital transformation",
          "technology adoption",
          "business process automation",
          "AI implementation"
        ]
      },
      {
        "name": "Gartner Technology Research",
        "url_patterns": [
          "gartner.com/en/insights/",
          "gartner.com/en/research/"
        ],
        "search_modifiers": [
          "site:gartner.com",
          "Gartner Hype Cycle",
          "Gartner Magic Quadrant"
        ],
        "content_types": [
          "technology hype cycles",
          "market analysis",
          "vendor assessments",
          "technology predictions"
        ],
        "focus_areas": [
          "emerging technologies",
          "market trends",
          "technology maturity",
          "vendor landscape"
        ]
      }
    ]
  }
}
```

### Tier 2: Academic and Research Institutions
```json
{
  "tier_2_sources": {
    "priority": "high",
    "reliability_score": 0.90,
    "update_frequency": "continuous",
    "sources": [
      {
        "name": "MIT Technology Review",
        "url_patterns": [
          "technologyreview.com/",
          "technologyreview.com/topic/artificial-intelligence/"
        ],
        "search_modifiers": [
          "site:technologyreview.com",
          "MIT Technology Review"
        ],
        "content_types": [
          "breakthrough technology analysis",
          "research insights",
          "technology implications"
        ],
        "focus_areas": [
          "AI breakthroughs",
          "emerging technologies",
          "research developments",
          "technology impact"
        ]
      },
      {
        "name": "arXiv Research Papers",
        "url_patterns": [
          "arxiv.org/list/cs.AI/recent",
          "arxiv.org/list/cs.LG/recent",
          "arxiv.org/list/cs.CL/recent"
        ],
        "search_modifiers": [
          "site:arxiv.org",
          "arXiv:cs.AI",
          "arXiv:cs.LG"
        ],
        "content_types": [
          "research papers",
          "preprints",
          "technical studies"
        ],
        "focus_areas": [
          "machine learning",
          "artificial intelligence",
          "natural language processing",
          "computer vision"
        ],
        "date_filters": [
          "submitted:2024",
          "submitted:2025",
          "recent submissions"
        ]
      },
      {
        "name": "IEEE Computer Society",
        "url_patterns": [
          "computer.org/",
          "ieeexplore.ieee.org/"
        ],
        "search_modifiers": [
          "site:computer.org",
          "site:ieeexplore.ieee.org",
          "IEEE Computer"
        ],
        "content_types": [
          "technical papers",
          "conference proceedings",
          "industry standards"
        ],
        "focus_areas": [
          "computer science",
          "software engineering",
          "systems architecture",
          "emerging technologies"
        ]
      },
      {
        "name": "ACM Digital Library",
        "url_patterns": [
          "dl.acm.org/",
          "cacm.acm.org/"
        ],
        "search_modifiers": [
          "site:dl.acm.org",
          "site:cacm.acm.org",
          "ACM"
        ],
        "content_types": [
          "research papers",
          "conference proceedings",
          "technical communications"
        ],
        "focus_areas": [
          "computing research",
          "software systems",
          "human-computer interaction",
          "information systems"
        ]
      }
    ]
  }
}
```

### Tier 3: Industry News and Analysis
```json
{
  "tier_3_sources": {
    "priority": "medium",
    "reliability_score": 0.80,
    "update_frequency": "daily",
    "sources": [
      {
        "name": "TechCrunch",
        "url_patterns": [
          "techcrunch.com/category/artificial-intelligence/",
          "techcrunch.com/category/enterprise/",
          "techcrunch.com/category/startups/"
        ],
        "search_modifiers": [
          "site:techcrunch.com",
          "TechCrunch"
        ],
        "content_types": [
          "startup news",
          "funding announcements",
          "product launches",
          "industry analysis"
        ],
        "focus_areas": [
          "startup ecosystem",
          "venture funding",
          "product innovations",
          "market trends"
        ]
      },
      {
        "name": "VentureBeat",
        "url_patterns": [
          "venturebeat.com/ai/",
          "venturebeat.com/business/",
          "venturebeat.com/enterprise/"
        ],
        "search_modifiers": [
          "site:venturebeat.com",
          "VentureBeat"
        ],
        "content_types": [
          "AI news",
          "enterprise technology",
          "business analysis",
          "market insights"
        ],
        "focus_areas": [
          "artificial intelligence",
          "enterprise software",
          "business technology",
          "digital transformation"
        ]
      },
      {
        "name": "GitHub Trending",
        "url_patterns": [
          "github.com/trending",
          "github.com/topics/"
        ],
        "search_modifiers": [
          "site:github.com",
          "GitHub trending"
        ],
        "content_types": [
          "trending repositories",
          "open source projects",
          "developer tools",
          "code libraries"
        ],
        "focus_areas": [
          "open source trends",
          "developer tools",
          "programming languages",
          "software libraries"
        ]
      },
      {
        "name": "Product Hunt",
        "url_patterns": [
          "producthunt.com/topics/artificial-intelligence",
          "producthunt.com/topics/developer-tools",
          "producthunt.com/topics/productivity"
        ],
        "search_modifiers": [
          "site:producthunt.com",
          "Product Hunt"
        ],
        "content_types": [
          "product launches",
          "tool discoveries",
          "innovation showcases"
        ],
        "focus_areas": [
          "new products",
          "developer tools",
          "productivity software",
          "AI applications"
        ]
      }
    ]
  }
}
```

### Tier 4: Community and Developer Sources
```json
{
  "tier_4_sources": {
    "priority": "supplementary",
    "reliability_score": 0.70,
    "update_frequency": "continuous",
    "sources": [
      {
        "name": "Stack Overflow",
        "url_patterns": [
          "stackoverflow.com/questions/tagged/",
          "insights.stackoverflow.com/"
        ],
        "search_modifiers": [
          "site:stackoverflow.com",
          "Stack Overflow Survey"
        ],
        "content_types": [
          "developer surveys",
          "technology trends",
          "programming questions",
          "community insights"
        ],
        "focus_areas": [
          "developer preferences",
          "technology adoption",
          "programming trends",
          "tool usage"
        ]
      },
      {
        "name": "Hacker News",
        "url_patterns": [
          "news.ycombinator.com/"
        ],
        "search_modifiers": [
          "site:news.ycombinator.com",
          "Hacker News"
        ],
        "content_types": [
          "technology discussions",
          "startup news",
          "developer insights",
          "industry commentary"
        ],
        "focus_areas": [
          "technology trends",
          "startup ecosystem",
          "developer community",
          "innovation discussions"
        ]
      },
      {
        "name": "Reddit Technology Communities",
        "url_patterns": [
          "reddit.com/r/MachineLearning/",
          "reddit.com/r/artificial/",
          "reddit.com/r/programming/"
        ],
        "search_modifiers": [
          "site:reddit.com",
          "reddit"
        ],
        "content_types": [
          "community discussions",
          "technology debates",
          "project showcases",
          "learning resources"
        ],
        "focus_areas": [
          "machine learning",
          "artificial intelligence",
          "programming",
          "technology trends"
        ]
      }
    ]
  }
}
```

## Research Query Templates

### Date-Aware Query Patterns
```json
{
  "date_aware_queries": {
    "current_year_trends": [
      "{topic} trends {current_year}",
      "latest {current_year} {topic} developments",
      "{current_year} {topic} market analysis",
      "emerging {current_year} {topic} technologies",
      "{current_year} {topic} industry report"
    ],
    "recent_developments": [
      "recent developments in {topic}",
      "latest {topic} innovations",
      "new {topic} solutions {current_year}",
      "{topic} breakthrough {current_year}",
      "cutting-edge {topic} {current_year}"
    ],
    "future_predictions": [
      "{topic} predictions {current_year}-{next_year}",
      "future of {topic} {current_year}",
      "{topic} roadmap {current_year}",
      "{topic} outlook {current_year}",
      "next generation {topic} {current_year}"
    ],
    "market_analysis": [
      "{topic} market size {current_year}",
      "{topic} adoption rates {current_year}",
      "{topic} investment trends {current_year}",
      "{topic} competitive landscape {current_year}",
      "{topic} market opportunities {current_year}"
    ]
  }
}
```

### Focus Area Query Mappings
```json
{
  "focus_area_queries": {
    "emerging_tech": {
      "base_topics": [
        "artificial intelligence",
        "machine learning",
        "blockchain",
        "quantum computing",
        "edge computing",
        "augmented reality",
        "virtual reality",
        "internet of things",
        "5G technology",
        "robotics"
      ],
      "query_modifiers": [
        "breakthrough",
        "emerging",
        "cutting-edge",
        "next-generation",
        "revolutionary"
      ],
      "application_areas": [
        "business automation",
        "enterprise applications",
        "consumer products",
        "industrial solutions",
        "healthcare applications"
      ]
    },
    "business_automation": {
      "base_topics": [
        "process automation",
        "workflow optimization",
        "business intelligence",
        "robotic process automation",
        "intelligent automation",
        "digital transformation",
        "operational efficiency",
        "productivity tools",
        "enterprise software",
        "business process management"
      ],
      "pain_points": [
        "manual processes",
        "inefficient workflows",
        "data silos",
        "repetitive tasks",
        "compliance challenges"
      ],
      "solution_areas": [
        "automation platforms",
        "integration tools",
        "analytics solutions",
        "workflow engines",
        "decision support systems"
      ]
    },
    "industry_specific": {
      "healthcare": [
        "healthcare automation",
        "medical AI",
        "clinical workflows",
        "patient management",
        "healthcare analytics"
      ],
      "finance": [
        "fintech automation",
        "financial AI",
        "trading algorithms",
        "risk management",
        "regulatory compliance"
      ],
      "manufacturing": [
        "industrial automation",
        "smart manufacturing",
        "predictive maintenance",
        "quality control",
        "supply chain optimization"
      ],
      "retail": [
        "retail automation",
        "customer analytics",
        "inventory management",
        "personalization",
        "omnichannel solutions"
      ]
    }
  }
}
```

## Research Execution Strategies

### Multi-Phase Research Approach
```json
{
  "research_phases": {
    "phase_1_trend_analysis": {
      "duration_minutes": 5,
      "query_count": 15,
      "focus": "broad trend identification",
      "sources": ["tier_1", "tier_2"],
      "query_types": [
        "current_year_trends",
        "recent_developments",
        "market_analysis"
      ]
    },
    "phase_2_gap_analysis": {
      "duration_minutes": 8,
      "query_count": 20,
      "focus": "capability gap identification",
      "sources": ["tier_1", "tier_2", "tier_3"],
      "query_types": [
        "unmet_needs",
        "market_gaps",
        "technology_limitations"
      ]
    },
    "phase_3_opportunity_mapping": {
      "duration_minutes": 10,
      "query_count": 25,
      "focus": "specific opportunity identification",
      "sources": ["all_tiers"],
      "query_types": [
        "business_opportunities",
        "automation_needs",
        "solution_requirements"
      ]
    },
    "phase_4_technology_assessment": {
      "duration_minutes": 7,
      "query_count": 18,
      "focus": "technology feasibility",
      "sources": ["tier_2", "tier_3", "tier_4"],
      "query_types": [
        "available_technologies",
        "development_tools",
        "integration_platforms"
      ]
    },
    "phase_5_competitive_intelligence": {
      "duration_minutes": 10,
      "query_count": 22,
      "focus": "competitive landscape",
      "sources": ["tier_3", "tier_4"],
      "query_types": [
        "competitor_analysis",
        "product_launches",
        "funding_announcements"
      ]
    ]
  }
}
```

### Query Optimization Strategies
```json
{
  "query_optimization": {
    "search_operators": {
      "site_specific": "site:{domain}",
      "date_range": "after:{start_date} before:{end_date}",
      "file_type": "filetype:{extension}",
      "exact_phrase": "\"{phrase}\"",
      "exclude_terms": "-{term}",
      "wildcard": "*{partial_term}*"
    },
    "result_filtering": {
      "recency_weight": 0.4,
      "source_authority_weight": 0.3,
      "relevance_weight": 0.2,
      "uniqueness_weight": 0.1
    },
    "content_extraction": {
      "key_phrases": "extract_key_phrases",
      "sentiment_analysis": "analyze_sentiment",
      "entity_recognition": "identify_entities",
      "trend_indicators": "detect_trends",
      "opportunity_signals": "identify_opportunities"
    }
  }
}
```

## Research Quality Metrics

### Source Reliability Scoring
```json
{
  "reliability_metrics": {
    "tier_1_sources": {
      "base_score": 0.95,
      "factors": {
        "institutional_authority": 0.3,
        "research_methodology": 0.25,
        "peer_review_process": 0.2,
        "update_frequency": 0.15,
        "citation_count": 0.1
      }
    },
    "tier_2_sources": {
      "base_score": 0.90,
      "factors": {
        "academic_credibility": 0.35,
        "research_rigor": 0.25,
        "publication_standards": 0.2,
        "expert_review": 0.15,
        "impact_factor": 0.05
      }
    },
    "tier_3_sources": {
      "base_score": 0.80,
      "factors": {
        "editorial_standards": 0.3,
        "industry_expertise": 0.25,
        "fact_checking": 0.2,
        "source_diversity": 0.15,
        "timeliness": 0.1
      }
    },
    "tier_4_sources": {
      "base_score": 0.70,
      "factors": {
        "community_validation": 0.3,
        "expert_participation": 0.25,
        "content_moderation": 0.2,
        "discussion_quality": 0.15,
        "consensus_indicators": 0.1
      }
    }
  }
}
```

### Research Coverage Assessment
```json
{
  "coverage_metrics": {
    "breadth_indicators": [
      "topic_diversity",
      "source_variety",
      "perspective_range",
      "geographic_coverage",
      "industry_span"
    ],
    "depth_indicators": [
      "detail_level",
      "technical_depth",
      "analysis_quality",
      "evidence_strength",
      "insight_value"
    ],
    "currency_indicators": [
      "publication_date",
      "data_freshness",
      "trend_relevance",
      "market_timeliness",
      "technology_maturity"
    ],
    "quality_thresholds": {
      "minimum_sources_per_topic": 5,
      "minimum_tier_1_coverage": 0.3,
      "maximum_age_days": 365,
      "minimum_reliability_score": 0.75,
      "minimum_relevance_score": 0.8
    }
  }
}
```

This comprehensive research intelligence framework ensures that the Enhanced Agent Creator has access to high-quality, current, and relevant information for generating market-aligned AI agents that address real-world needs and leverage the latest available technologies.
