#!/usr/bin/env python3
"""
Parallelization Pattern Demo - Showcase all examples

This script demonstrates all three examples of the Parallelization pattern:
1. Parallel Research Agents
2. Document Analyzer 
3. Content Generator

Usage:
    python demo_parallelization.py
"""

import subprocess
import sys
import time
from pathlib import Path

def run_command(command, description):
    """Run a command and display the output."""
    print(f"\n{'='*80}")
    print(f"🚀 {description}")
    print(f"Command: {command}")
    print('='*80)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(result.stdout)
            if result.stderr:
                print(f"Warnings: {result.stderr}")
        else:
            print(f"❌ Error (exit code {result.returncode}):")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("❌ Command timed out after 60 seconds")
    except Exception as e:
        print(f"❌ Exception running command: {e}")

def main():
    """Run the parallelization pattern demonstration."""
    print("🎯 PARALLELIZATION AGENTIC AI PATTERN DEMONSTRATION")
    print("This demo showcases how multiple AI agents can work in parallel")
    print("to achieve faster processing and comprehensive results.")
    
    # Ensure we're in the right directory
    script_dir = Path(__file__).parent
    if script_dir.name != "parallelization-pattern":
        print("❌ This script should be run from the parallelization-pattern directory")
        sys.exit(1)
    
    # Demo 1: Parallel Research Agents
    run_command(
        'python parallel_research_agents.py "quantum computing applications"',
        "DEMO 1: Parallel Research Agents - Multiple agents research different aspects simultaneously"
    )
    
    time.sleep(2)  # Brief pause between demos
    
    # Demo 2: Document Analyzer (will create sample docs if none exist)
    run_command(
        'python document_analyzer.py',
        "DEMO 2: Document Analyzer - Parallel processing of multiple documents"
    )
    
    time.sleep(2)  # Brief pause between demos
    
    # Demo 3: Content Generator
    run_command(
        'python content_generator.py "blockchain technology guide"',
        "DEMO 3: Content Generator - Parallel generation of comprehensive content"
    )
    
    print(f"\n{'='*80}")
    print("✅ PARALLELIZATION PATTERN DEMONSTRATION COMPLETE")
    print("="*80)
    print("\n🎉 Key Benefits Demonstrated:")
    print("   • Concurrent execution improves processing speed")
    print("   • Multiple perspectives enhance result quality")
    print("   • Scalable approach handles complex tasks efficiently")
    print("   • Robust error handling ensures reliable operation")
    
    print("\n📁 Generated Files:")
    print("   • Research reports (research_report_*.json)")
    print("   • Document analysis (document_analysis_*.json)")
    print("   • Generated content (generated_guide_*.md)")
    print("   • Detailed reports (generation_report_*.json)")
    
    print("\n💡 Next Steps:")
    print("   • Modify examples to use real OpenAI API calls")
    print("   • Experiment with different numbers of parallel agents")
    print("   • Try the examples with your own topics and documents")
    print("   • Explore other agentic AI patterns in this repository")

if __name__ == "__main__":
    main()