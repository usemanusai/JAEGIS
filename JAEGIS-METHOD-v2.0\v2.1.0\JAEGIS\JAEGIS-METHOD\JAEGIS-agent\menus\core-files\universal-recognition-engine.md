# JAEGIS Universal Recognition Engine
## Advanced Pattern Recognition for All Help Request Variations

### Recognition Engine Overview
This system provides comprehensive recognition of all possible help request variations, ensuring users can access help using any natural language pattern or command format.

---

## 🎯 **UNIVERSAL RECOGNITION ENGINE**

### **Advanced Recognition Architecture**
```python
class JAEGISUniversalRecognitionEngine:
    """
    Advanced pattern recognition system for universal help request detection
    """
    
    def __init__(self):
        """
        Initialize universal recognition engine with comprehensive patterns
        """
        print("🎯 JAEGIS UNIVERSAL RECOGNITION ENGINE: INITIALIZING")
        
        # Load recognition pattern libraries
        self.exact_patterns = self.load_exact_patterns()
        self.natural_language_patterns = self.load_natural_language_patterns()
        self.contextual_patterns = self.load_contextual_patterns()
        self.partial_patterns = self.load_partial_patterns()
        self.fuzzy_patterns = self.load_fuzzy_patterns()
        
        # Initialize recognition processors
        self.pattern_matcher = PatternMatcher()
        self.context_analyzer = ContextAnalyzer()
        self.intent_classifier = IntentClassifier()
        self.confidence_scorer = ConfidenceScorer()
        
        # Initialize recognition cache
        self.recognition_cache = {}
        self.pattern_statistics = {}
        
        print("   ✅ Exact patterns: LOADED")
        print("   ✅ Natural language patterns: LOADED")
        print("   ✅ Contextual patterns: LOADED")
        print("   ✅ Partial patterns: LOADED")
        print("   ✅ Fuzzy patterns: LOADED")
        print("   ✅ Recognition processors: ACTIVE")
        print("   ✅ Universal recognition: OPERATIONAL")
    
    def recognize_help_request(self, user_input):
        """
        Recognize if user input is a help request using universal patterns
        """
        # Normalize input for processing
        normalized_input = self.normalize_input(user_input)
        
        # Check cache first for performance
        if normalized_input in self.recognition_cache:
            return self.recognition_cache[normalized_input]
        
        # Multi-tier recognition process
        recognition_result = {
            'is_help_request': False,
            'confidence_score': 0.0,
            'recognition_method': None,
            'matched_pattern': None,
            'response_type': 'none',
            'processing_details': {}
        }
        
        # Tier 1: Exact pattern matching (highest confidence)
        exact_match = self.check_exact_patterns(normalized_input)
        if exact_match['matched']:
            recognition_result.update({
                'is_help_request': True,
                'confidence_score': 1.0,
                'recognition_method': 'exact_pattern',
                'matched_pattern': exact_match['pattern'],
                'response_type': 'comprehensive_help'
            })
            
        # Tier 2: Natural language pattern matching
        elif not recognition_result['is_help_request']:
            nl_match = self.check_natural_language_patterns(normalized_input)
            if nl_match['matched']:
                recognition_result.update({
                    'is_help_request': True,
                    'confidence_score': nl_match['confidence'],
                    'recognition_method': 'natural_language',
                    'matched_pattern': nl_match['pattern'],
                    'response_type': 'comprehensive_help'
                })
        
        # Tier 3: Contextual pattern analysis
        elif not recognition_result['is_help_request']:
            context_match = self.check_contextual_patterns(normalized_input)
            if context_match['matched']:
                recognition_result.update({
                    'is_help_request': True,
                    'confidence_score': context_match['confidence'],
                    'recognition_method': 'contextual_analysis',
                    'matched_pattern': context_match['pattern'],
                    'response_type': 'helpful_guidance'
                })
        
        # Tier 4: Partial pattern matching
        elif not recognition_result['is_help_request']:
            partial_match = self.check_partial_patterns(normalized_input)
            if partial_match['matched']:
                recognition_result.update({
                    'is_help_request': True,
                    'confidence_score': partial_match['confidence'],
                    'recognition_method': 'partial_pattern',
                    'matched_pattern': partial_match['pattern'],
                    'response_type': 'basic_help'
                })
        
        # Tier 5: Fuzzy pattern matching (lowest threshold)
        elif not recognition_result['is_help_request']:
            fuzzy_match = self.check_fuzzy_patterns(normalized_input)
            if fuzzy_match['matched']:
                recognition_result.update({
                    'is_help_request': True,
                    'confidence_score': fuzzy_match['confidence'],
                    'recognition_method': 'fuzzy_matching',
                    'matched_pattern': fuzzy_match['pattern'],
                    'response_type': 'clarification_help'
                })
        
        # Cache result for performance
        self.recognition_cache[normalized_input] = recognition_result
        
        # Update pattern statistics
        self.update_pattern_statistics(recognition_result)
        
        return recognition_result
    
    def load_exact_patterns(self):
        """
        Load exact command patterns for help requests
        """
        exact_patterns = {
            'primary_commands': [
                '/help', '/HELP', 'help', 'HELP'
            ],
            'alternative_commands': [
                '/h', '/H', 'h', 'H'
            ],
            'extended_commands': [
                '/help-me', '/assistance', '/guide', '/commands'
            ],
            'case_variations': [
                'Help', 'HELP', 'help', 'HeLp', 'hElP'
            ]
        }
        return exact_patterns
    
    def load_natural_language_patterns(self):
        """
        Load natural language patterns for help requests
        """
        natural_patterns = {
            'direct_questions': [
                'what commands are available',
                'show me all commands',
                'how do the commands work',
                'list all commands',
                'what can i do',
                'available commands',
                'command list',
                'show commands',
                'help menu'
            ],
            'question_variations': [
                'what are the available commands',
                'can you show me the commands',
                'how do i use commands',
                'what commands can i use',
                'show me what i can do',
                'list the available commands',
                'display all commands',
                'what are my options'
            ],
            'help_seeking_phrases': [
                'i need help with commands',
                'help me with the commands',
                'can you help me',
                'i need assistance',
                'how does this work',
                'what can this system do',
                'show me the features',
                'what functionality is available'
            ],
            'exploration_phrases': [
                'what else can i do',
                'what other commands',
                'more options',
                'other features',
                'additional commands',
                'more commands'
            ]
        }
        return natural_patterns
    
    def load_contextual_patterns(self):
        """
        Load contextual patterns indicating help need
        """
        contextual_patterns = {
            'confusion_indicators': [
                'i dont know',
                'i am confused',
                'i need help',
                'how do i',
                'i dont understand',
                'what should i do',
                'im lost',
                'i need assistance',
                'i am stuck',
                'not sure what to do'
            ],
            'exploration_indicators': [
                'what can i try',
                'what are my choices',
                'what options do i have',
                'how can i proceed',
                'what next',
                'where do i start'
            ],
            'capability_questions': [
                'what does this do',
                'how powerful is this',
                'what are the capabilities',
                'what can this handle',
                'how advanced is this'
            ]
        }
        return contextual_patterns
    
    def load_partial_patterns(self):
        """
        Load partial patterns for incomplete help requests
        """
        partial_patterns = {
            'help_keywords': [
                'command', 'commands', 'help', 'menu', 'options',
                'available', 'list', 'show', 'display', 'tell'
            ],
            'question_words': [
                'what', 'how', 'where', 'when', 'why', 'which', 'who'
            ],
            'action_words': [
                'show', 'list', 'display', 'tell', 'explain',
                'describe', 'demonstrate', 'guide', 'assist'
            ],
            'capability_words': [
                'can', 'able', 'possible', 'available', 'supported',
                'features', 'functions', 'capabilities', 'options'
            ]
        }
        return partial_patterns
    
    def load_fuzzy_patterns(self):
        """
        Load fuzzy patterns for ambiguous help requests
        """
        fuzzy_patterns = {
            'vague_requests': [
                'help', 'assist', 'guide', 'support', 'info',
                'information', 'details', 'more', 'explain'
            ],
            'incomplete_phrases': [
                'how to', 'what is', 'can you', 'is there',
                'do you', 'will you', 'could you'
            ],
            'general_inquiries': [
                'anything else', 'more info', 'tell me more',
                'what about', 'how about', 'any other'
            ]
        }
        return fuzzy_patterns
    
    def check_exact_patterns(self, normalized_input):
        """
        Check for exact pattern matches
        """
        for pattern_group, patterns in self.exact_patterns.items():
            for pattern in patterns:
                if normalized_input.lower() == pattern.lower():
                    return {
                        'matched': True,
                        'pattern': pattern,
                        'pattern_group': pattern_group,
                        'confidence': 1.0
                    }
        
        return {'matched': False}
    
    def check_natural_language_patterns(self, normalized_input):
        """
        Check for natural language pattern matches
        """
        input_lower = normalized_input.lower()
        
        for pattern_group, patterns in self.natural_language_patterns.items():
            for pattern in patterns:
                if pattern.lower() in input_lower:
                    # Calculate confidence based on pattern completeness
                    pattern_words = set(pattern.lower().split())
                    input_words = set(input_lower.split())
                    
                    overlap = len(pattern_words.intersection(input_words))
                    confidence = overlap / len(pattern_words)
                    
                    if confidence >= 0.7:  # 70% word overlap threshold
                        return {
                            'matched': True,
                            'pattern': pattern,
                            'pattern_group': pattern_group,
                            'confidence': confidence
                        }
        
        return {'matched': False}
    
    def check_contextual_patterns(self, normalized_input):
        """
        Check for contextual pattern matches
        """
        input_lower = normalized_input.lower()
        
        for pattern_group, patterns in self.contextual_patterns.items():
            for pattern in patterns:
                if pattern.lower() in input_lower:
                    # Contextual patterns have medium confidence
                    confidence = 0.8
                    return {
                        'matched': True,
                        'pattern': pattern,
                        'pattern_group': pattern_group,
                        'confidence': confidence
                    }
        
        return {'matched': False}
    
    def check_partial_patterns(self, normalized_input):
        """
        Check for partial pattern matches using keyword combinations
        """
        input_words = set(normalized_input.lower().split())
        
        # Count matches in each category
        help_keywords = sum(1 for word in input_words if word in self.partial_patterns['help_keywords'])
        question_words = sum(1 for word in input_words if word in self.partial_patterns['question_words'])
        action_words = sum(1 for word in input_words if word in self.partial_patterns['action_words'])
        capability_words = sum(1 for word in input_words if word in self.partial_patterns['capability_words'])
        
        # Determine if combination suggests help request
        total_matches = help_keywords + question_words + action_words + capability_words
        
        # Various combination rules
        if help_keywords >= 1 and (question_words >= 1 or action_words >= 1):
            confidence = min(0.9, 0.3 + (total_matches * 0.15))
            return {
                'matched': True,
                'pattern': f"keyword_combination_{total_matches}_matches",
                'pattern_group': 'partial_patterns',
                'confidence': confidence
            }
        elif total_matches >= 3:
            confidence = min(0.8, 0.2 + (total_matches * 0.1))
            return {
                'matched': True,
                'pattern': f"multiple_keywords_{total_matches}_matches",
                'pattern_group': 'partial_patterns',
                'confidence': confidence
            }
        
        return {'matched': False}
    
    def check_fuzzy_patterns(self, normalized_input):
        """
        Check for fuzzy pattern matches with low threshold
        """
        input_lower = normalized_input.lower()
        
        for pattern_group, patterns in self.fuzzy_patterns.items():
            for pattern in patterns:
                if pattern.lower() in input_lower:
                    # Fuzzy patterns have lower confidence
                    confidence = 0.6
                    return {
                        'matched': True,
                        'pattern': pattern,
                        'pattern_group': pattern_group,
                        'confidence': confidence
                    }
        
        return {'matched': False}
    
    def normalize_input(self, user_input):
        """
        Normalize user input for consistent processing
        """
        if not user_input:
            return ""
        
        # Basic normalization
        normalized = user_input.strip()
        
        # Remove extra whitespace
        normalized = ' '.join(normalized.split())
        
        # Handle common punctuation
        normalized = normalized.replace('?', '').replace('!', '').replace('.', '')
        
        return normalized
    
    def update_pattern_statistics(self, recognition_result):
        """
        Update pattern usage statistics for optimization
        """
        if recognition_result['is_help_request']:
            method = recognition_result['recognition_method']
            pattern = recognition_result['matched_pattern']
            
            if method not in self.pattern_statistics:
                self.pattern_statistics[method] = {}
            
            if pattern not in self.pattern_statistics[method]:
                self.pattern_statistics[method][pattern] = 0
            
            self.pattern_statistics[method][pattern] += 1
```

This universal recognition engine ensures comprehensive detection of help requests across all possible user input variations, providing maximum accessibility and user-friendly help system interaction.
