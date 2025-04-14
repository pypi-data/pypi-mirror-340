"""
Basic tests for the LitPrinter package.
"""

import io
import sys
from unittest import mock

import pytest

from litprinter import litprint, lit


def test_litprint_basic():
    """Test basic functionality of litprint."""
    # Redirect stdout to capture output
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    try:
        # Call litprint with a simple string
        litprint("Hello, world!")
        
        # Get the output
        output = captured_output.getvalue()
        
        # Check that the output contains our string
        assert "Hello, world!" in output
        
        # Check that it has the LIT prefix
        assert "LIT" in output
    finally:
        # Reset stdout
        sys.stdout = sys.__stdout__


def test_lit_basic():
    """Test basic functionality of lit."""
    # Redirect stdout to capture output
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    try:
        # Call lit with a simple string
        lit("Hello, world!")
        
        # Get the output
        output = captured_output.getvalue()
        
        # Check that the output contains our string
        assert "Hello, world!" in output
        
        # Check that it has the LIT prefix
        assert "LIT" in output
    finally:
        # Reset stdout
        sys.stdout = sys.__stdout__
