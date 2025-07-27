"""
JAEGIS Cognitive Ingestion & Synthesis Pipeline
A comprehensive system for converting unstructured information into structured training data

This package implements the complete cognitive pipeline with multi-source ingestion,
advanced semantic analysis, and training data generation capabilities.
"""

__version__ = "1.0.0"
__author__ = "JAEGIS Brain Protocol Suite"
__description__ = "Cognitive Ingestion & Synthesis Pipeline for AI Training Data Generation"

from .main import app

__all__ = ["app"]
