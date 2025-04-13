"""
NOVA: The Prompt Pattern Matching
Author: Thomas Roccia 
twitter: @fr0gger_
License: MIT License
Version: 1.0.0
Description: Core matcher implementation for Nova rules
"""

from typing import Dict, List, Tuple, Optional, Any, Set, Callable
import re

from nova.core.rules import NovaRule, KeywordPattern, SemanticPattern, LLMPattern
from nova.evaluators.keywords import DefaultKeywordEvaluator
from nova.evaluators.semantics import DefaultSemanticEvaluator
from nova.evaluators.llm import OpenAIEvaluator, LLMEvaluator
from nova.evaluators.condition import evaluate_condition


class NovaMatcher:
    """
    Matcher for Nova rules.
    Evaluates text against rules using different pattern types.
    Uses lazy evaluator initialization for better performance.
    """
    
    def __init__(self, 
                 rule: NovaRule,
                 keyword_evaluator: Optional[DefaultKeywordEvaluator] = None,
                 semantic_evaluator: Optional[DefaultSemanticEvaluator] = None,
                 llm_evaluator: Optional[LLMEvaluator] = None,
                 create_llm_evaluator: bool = True):
        """
        Initialize the matcher with a rule and optional custom evaluators.
        Only initializes evaluators when needed based on rule content.
        
        Args:
            rule: The NovaRule to match against
            keyword_evaluator: Custom keyword evaluator (uses DefaultKeywordEvaluator if None)
            semantic_evaluator: Custom semantic evaluator (uses DefaultSemanticEvaluator if None)
            llm_evaluator: Custom LLM evaluator (uses OpenAIEvaluator if None)
            create_llm_evaluator: Whether to create a new LLM evaluator if needed and none is provided.
                                  If False, and llm_evaluator is None, no LLM evaluations will be performed.
        """
        self.rule = rule
        
        # Always initialize keyword evaluator since it's lightweight
        self.keyword_evaluator = keyword_evaluator or DefaultKeywordEvaluator()
        
        # Check if semantic evaluator is needed
        needs_semantic = False
        if rule and rule.semantics:
            needs_semantic = True
        elif rule and 'semantics' in rule.condition.lower():
            needs_semantic = True
            
        # Check if LLM evaluator is needed
        needs_llm = False
        if rule and rule.llms:
            needs_llm = True
        elif rule and 'llm.' in rule.condition.lower():
            needs_llm = True
        
        # Only initialize semantic evaluator if needed
        if needs_semantic:
            self.semantic_evaluator = semantic_evaluator or DefaultSemanticEvaluator()
        else:
            self.semantic_evaluator = None
            
        # Handle LLM evaluator initialization
        if llm_evaluator:
            # Use provided evaluator regardless of need
            self.llm_evaluator = llm_evaluator
        elif needs_llm and create_llm_evaluator:
            # Create a new evaluator if needed and allowed to create
            self.llm_evaluator = OpenAIEvaluator()
        else:
            # No evaluator provided and either not needed or not allowed to create
            self.llm_evaluator = None
            if needs_llm:
                print("Warning: Rule requires LLM evaluation but no evaluator provided and creation disabled.")
            else:
                print("Rule does not use LLM evaluation. Skipping LLM evaluator initialization.")
        
        # Pre-compile keyword patterns for performance
        if rule:
            self._precompile_patterns()

    def _precompile_patterns(self):
        """Pre-compile regex patterns for better performance."""
        if not self.rule:
            return
            
        for key, pattern in self.rule.keywords.items():
            if pattern.is_regex:
                self.keyword_evaluator.compile_pattern(key, pattern)

    def set_rule(self, rule: NovaRule):
        """
        Update the matcher with a new rule.
        This is more efficient than creating a new matcher instance.
        
        Args:
            rule: The new NovaRule to match against
        """
        self.rule = rule
        self._precompile_patterns()
    
    def _analyze_condition(self, condition: str) -> Dict[str, Set[str]]:
        """
        Analyze the rule condition to determine which patterns need to be evaluated.
        
        Args:
            condition: The rule condition
            
        Returns:
            Dictionary with sets of variable names needed for each pattern type
        """
        needed_patterns = {
            'keywords': set(),
            'semantics': set(),
            'llm': set(),
            'section_wildcards': set()
        }
        
        # Check for section wildcards
        for section in ['keywords', 'semantics', 'llm']:
            if f"{section}.*" in condition:
                needed_patterns['section_wildcards'].add(section)
                
        # Check for "any of" section wildcards
        for section in ['keywords', 'semantics', 'llm']:
            if f"any of {section}.*" in condition:
                needed_patterns['section_wildcards'].add(section)

        # Check for direct variable references with section prefixes
        for section in ['keywords', 'semantics', 'llm']:
            # Exact references: "section.$var"
            pattern = rf'{section}\.\$([a-zA-Z0-9_]+)(?!\*)'
            for match in re.finditer(pattern, condition):
                var_name = f"${match.group(1)}"
                needed_patterns[section].add(var_name)
                
            # Wildcard references: "section.$var*"
            wildcard_pattern = rf'{section}\.\$([a-zA-Z0-9_]+)\*'
            for match in re.finditer(wildcard_pattern, condition):
                prefix = match.group(1)
                # Add all matching variables to needed patterns
                for var_name in getattr(self.rule, section, {}):
                    if var_name[1:].startswith(prefix):  # Remove $ from var name
                        needed_patterns[section].add(var_name)
        
        # Check for standalone variables ($var)
        var_pattern = r'(?<![a-zA-Z0-9_\.])(\$[a-zA-Z0-9_]+)(?!\*)'
        for match in re.finditer(var_pattern, condition):
            var_name = match.group(1)
            
            # Determine which section this variable belongs to
            if var_name in self.rule.keywords:
                needed_patterns['keywords'].add(var_name)
            elif var_name in self.rule.semantics:
                needed_patterns['semantics'].add(var_name)
            elif var_name in self.rule.llms:
                needed_patterns['llm'].add(var_name)
        
        # Check for "any of" wildcards
        any_of_pattern = r'any\s+of\s+\(\$([a-zA-Z0-9_]+)\*\)'
        for match in re.finditer(any_of_pattern, condition):
            prefix = match.group(1)
            
            # Add all matching variables from all sections
            for section, patterns in [
                ('keywords', self.rule.keywords),
                ('semantics', self.rule.semantics),
                ('llm', self.rule.llms)
            ]:
                for var_name in patterns:
                    if var_name[1:].startswith(prefix):
                        needed_patterns[section].add(var_name)
        
        return needed_patterns
        
    def check_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Check if a prompt matches the rule.
        
        Args:
            prompt: The prompt text to check
            
        Returns:
            Dictionary containing match results and details
        """
        # Extract variables needed based on the condition
        condition = self.rule.condition
        needed_patterns = self._analyze_condition(condition)
        
        # Track all evaluation results for debugging
        all_keyword_matches = {}
        all_semantic_matches = {}
        all_semantic_scores = {}
        all_llm_matches = {}
        all_llm_scores = {}
        
        # Dictionary to hold evaluation functions for lazy evaluation
        lazy_evaluations = {}
        
        # Initialize filtered dictionaries to hold results needed for condition evaluation
        keyword_matches = {}
        semantic_matches = {}
        llm_matches = {}
        
        # ------ LAZY PATTERN EVALUATION ------
        
        # Set up lazy evaluation functions for keywords
        for key, pattern in self.rule.keywords.items():
            # Only include if explicitly needed by condition or section wildcard is used
            if key in needed_patterns['keywords'] or 'keywords' in needed_patterns['section_wildcards']:
                lazy_evaluations[('keywords', key)] = lambda p=pattern, k=key: self.keyword_evaluator.evaluate(p, prompt, k)
        
        # Set up lazy evaluation functions for semantics (if evaluator exists)
        if self.semantic_evaluator:
            for key, pattern in self.rule.semantics.items():
                # Only include if explicitly needed by condition or section wildcard is used
                if key in needed_patterns['semantics'] or 'semantics' in needed_patterns['section_wildcards']:
                    lazy_evaluations[('semantics', key)] = lambda p=pattern: self.semantic_evaluator.evaluate(p, prompt)
        
        # Set up lazy evaluation functions for LLMs (if evaluator exists)
        if self.llm_evaluator:
            for key, pattern in self.rule.llms.items():
                # Only include if explicitly needed by condition or section wildcard is used
                if key in needed_patterns['llm'] or 'llm' in needed_patterns['section_wildcards']:
                    temperature = pattern.threshold
                    lazy_evaluations[('llm', key)] = lambda p=pattern, t=temperature: self.llm_evaluator.evaluate_prompt(p.pattern, prompt, temperature=t)
        
        # First evaluate only the patterns that are directly referenced in the condition
        # Create a list of sections and variables to evaluate based on what evaluators are available
        patterns_to_evaluate = [('keywords', name) for name in needed_patterns['keywords']]
        
        if self.semantic_evaluator:
            patterns_to_evaluate += [('semantics', name) for name in needed_patterns['semantics']]
            
        if self.llm_evaluator:
            patterns_to_evaluate += [('llm', name) for name in needed_patterns['llm']]
            
        # Evaluate each pattern
        for section, var_name in patterns_to_evaluate:
            eval_key = (section, var_name)
            if eval_key in lazy_evaluations:
                try:
                    if section == 'keywords':
                        result = lazy_evaluations[eval_key]()
                        all_keyword_matches[var_name] = result
                        keyword_matches[var_name] = result
                    elif section == 'semantics':
                        matched, score = lazy_evaluations[eval_key]()
                        all_semantic_matches[var_name] = matched
                        all_semantic_scores[var_name] = score
                        semantic_matches[var_name] = matched
                    elif section == 'llm':
                        matched, confidence, details = lazy_evaluations[eval_key]()
                        all_llm_matches[var_name] = matched
                        all_llm_scores[var_name] = confidence
                        llm_matches[var_name] = matched
                except Exception as e:
                    print(f"Error evaluating {section}.{var_name}: {str(e)}")
                    # Default to False on error
                    if section == 'keywords':
                        all_keyword_matches[var_name] = False
                        keyword_matches[var_name] = False
                    elif section == 'semantics':
                        all_semantic_matches[var_name] = False
                        all_semantic_scores[var_name] = 0.0
                        semantic_matches[var_name] = False
                    elif section == 'llm':
                        all_llm_matches[var_name] = False
                        all_llm_scores[var_name] = 0.0
                        llm_matches[var_name] = False
        
        # Process section wildcards if needed
        for section in needed_patterns['section_wildcards']:
            if section == 'keywords' and not all_keyword_matches:
                # Only evaluate all keywords if needed and not already evaluated
                for key, pattern in self.rule.keywords.items():
                    if key not in all_keyword_matches:
                        try:
                            result = self.keyword_evaluator.evaluate(pattern, prompt, key)
                            all_keyword_matches[key] = result
                        except Exception:
                            all_keyword_matches[key] = False
            
            elif section == 'semantics' and self.semantic_evaluator and not all_semantic_matches:
                # Only evaluate all semantics if needed and not already evaluated
                for key, pattern in self.rule.semantics.items():
                    if key not in all_semantic_matches:
                        try:
                            matched, score = self.semantic_evaluator.evaluate(pattern, prompt)
                            all_semantic_matches[key] = matched
                            all_semantic_scores[key] = score
                        except Exception:
                            all_semantic_matches[key] = False
                            all_semantic_scores[key] = 0.0
            
            elif section == 'llm' and self.llm_evaluator and not all_llm_matches:
                # Only evaluate all LLM patterns if needed and not already evaluated
                for key, pattern in self.rule.llms.items():
                    if key not in all_llm_matches:
                        try:
                            temperature = pattern.threshold
                            matched, confidence, details = self.llm_evaluator.evaluate_prompt(pattern.pattern, prompt, temperature=temperature)
                            all_llm_matches[key] = matched
                            all_llm_scores[key] = confidence
                        except Exception:
                            all_llm_matches[key] = False
                            all_llm_scores[key] = 0.0
        
        # Evaluate condition if provided
        has_match = False
        condition_result = None
        
        if condition:
            # Make sure eval_condition gets all variables that might be needed by wildcards
            if 'keywords' in needed_patterns['section_wildcards']:
                keyword_matches.update(all_keyword_matches)
            if 'semantics' in needed_patterns['section_wildcards'] and self.semantic_evaluator:
                semantic_matches.update(all_semantic_matches)
            if 'llm' in needed_patterns['section_wildcards'] and self.llm_evaluator:
                llm_matches.update(all_llm_matches)
                
            # Use the condition evaluator with filtered match types
            condition_result = evaluate_condition(
                condition, 
                keyword_matches, 
                semantic_matches, 
                llm_matches
            )
            has_match = condition_result
        else:
            # Fall back to original behavior if no condition is specified
            has_match = any(keyword_matches.values()) or any(semantic_matches.values()) or any(llm_matches.values())
        
        # Build results with matching variables only
        results = {
            'matched': has_match,
            'rule_name': self.rule.name,
            'meta': self.rule.meta,
            'matching_keywords': {k: v for k, v in keyword_matches.items() if v},
            'matching_semantics': {k: v for k, v in semantic_matches.items() if v},
            'matching_llm': {k: v for k, v in llm_matches.items() if v},
            'semantic_scores': all_semantic_scores,
            'llm_scores': all_llm_scores,
            'debug': {
                'condition': condition,
                'condition_result': condition_result,
                'all_keyword_matches': all_keyword_matches,
                'all_semantic_matches': all_semantic_matches,
                'all_llm_matches': all_llm_matches
            }
        }
        
        return results