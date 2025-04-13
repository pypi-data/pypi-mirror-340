"""Tests for Y-Translator CLI"""

import pytest
from translator import __version__
from translator.cli import create_parser

def test_version():
    """Test that version is set correctly"""
    assert __version__ is not None
    assert isinstance(__version__, str)
    assert len(__version__.split('.')) >= 2

def test_parser_creation():
    """Test that the argument parser is created properly"""
    parser = create_parser()
    args = parser.parse_args([])
    assert args is not None
    
    args = parser.parse_args(['--verbose'])
    assert args.verbose is True
    
    args = parser.parse_args(['--model', 'gpt-3.5-turbo'])
    assert args.model == 'gpt-3.5-turbo' 