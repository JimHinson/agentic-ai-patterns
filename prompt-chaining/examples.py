"""
Example usage of the Prompt Chaining Pattern

This script demonstrates different ways to use the prompt chaining pattern
for various use cases.
"""

from prompt_chaining import PromptChain, PromptStep, create_article_creation_chain


def example_simple_chain():
    """Example of a simple 3-step chain"""
    print("🔗 Example 1: Simple Analysis Chain")
    print("=" * 50)
    
    chain = PromptChain()
    
    # Step 1: Analyze the problem
    analyze_step = PromptStep(
        name="analyze",
        prompt_template="Analyze this problem: {previous_output}. Identify key issues and challenges.",
        description="Analyze the input problem"
    )
    
    # Step 2: Generate solutions
    solutions_step = PromptStep(
        name="solutions",
        prompt_template="Based on this analysis: {previous_output}, generate 3 potential solutions.",
        description="Generate potential solutions"
    )
    
    # Step 3: Evaluate solutions
    evaluate_step = PromptStep(
        name="evaluate",
        prompt_template="Evaluate these solutions: {previous_output}. Rank them and explain why.",
        description="Evaluate and rank solutions"
    )
    
    chain.add_step(analyze_step)
    chain.add_step(solutions_step)
    chain.add_step(evaluate_step)
    
    result = chain.execute("Our team is struggling with meeting project deadlines")
    print(f"\n🎯 Final Result:\n{result[:300]}...\n")


def example_code_development_chain():
    """Example chain for code development process"""
    print("🔗 Example 2: Code Development Chain")
    print("=" * 50)
    
    chain = PromptChain()
    
    # Requirements analysis
    requirements_step = PromptStep(
        name="requirements",
        prompt_template="Analyze these requirements: {previous_output}. Create detailed technical requirements.",
        description="Analyze and refine requirements"
    )
    
    # Architecture design
    architecture_step = PromptStep(
        name="architecture",
        prompt_template="Based on requirements: {previous_output}, design the system architecture.",
        description="Design system architecture"
    )
    
    # Implementation plan
    implementation_step = PromptStep(
        name="implementation",
        prompt_template="Create implementation plan for: {previous_output}. Include timeline and milestones.",
        description="Create implementation plan"
    )
    
    chain.add_step(requirements_step)
    chain.add_step(architecture_step)
    chain.add_step(implementation_step)
    
    result = chain.execute("Build a web app for task management with user authentication")
    print(f"\n🎯 Final Result:\n{result[:300]}...\n")


def example_article_creation():
    """Example of the article creation chain"""
    print("🔗 Example 3: Article Creation Chain")
    print("=" * 50)
    
    # Use the pre-built article creation chain
    chain = create_article_creation_chain()
    result = chain.execute("Machine Learning in Finance")
    
    print(f"\n🎯 Final Article Preview:\n{result[:500]}...\n")


def example_custom_chain_with_branching():
    """Example showing conditional logic in chains"""
    print("🔗 Example 4: Custom Chain with Conditional Logic")
    print("=" * 50)
    
    # This is a conceptual example showing how you might extend
    # the basic chain for more complex scenarios
    
    class ConditionalPromptChain(PromptChain):
        """Extended chain with conditional execution"""
        
        def execute_with_conditions(self, initial_input: str, **kwargs):
            """Execute chain with conditional branching"""
            print(f"🤔 Analyzing input to determine best chain path...")
            
            # Simple keyword-based routing (in practice, this could be more sophisticated)
            if "technical" in initial_input.lower() or "code" in initial_input.lower():
                print("📋 Detected technical content - using development chain")
                return self._execute_technical_chain(initial_input, **kwargs)
            elif "article" in initial_input.lower() or "write" in initial_input.lower():
                print("📝 Detected content creation - using writing chain")
                return self._execute_writing_chain(initial_input, **kwargs)
            else:
                print("🔍 Using general analysis chain")
                return self._execute_analysis_chain(initial_input, **kwargs)
        
        def _execute_technical_chain(self, input_text: str, **kwargs):
            # Mock technical processing
            return f"Technical analysis result for: {input_text}"
        
        def _execute_writing_chain(self, input_text: str, **kwargs):
            # Mock writing processing
            return f"Content creation result for: {input_text}"
        
        def _execute_analysis_chain(self, input_text: str, **kwargs):
            # Mock general analysis
            return f"General analysis result for: {input_text}"
    
    # Demonstrate the conditional chain
    conditional_chain = ConditionalPromptChain()
    
    test_inputs = [
        "Write an article about renewable energy",
        "Debug this Python code that's crashing",
        "Analyze market trends in cryptocurrency"
    ]
    
    for test_input in test_inputs:
        print(f"\nInput: {test_input}")
        result = conditional_chain.execute_with_conditions(test_input)
        print(f"Result: {result}\n")


if __name__ == "__main__":
    print("🚀 Prompt Chaining Pattern - Usage Examples")
    print("=" * 60)
    
    # Run all examples
    example_simple_chain()
    print("\n" + "=" * 60 + "\n")
    
    example_code_development_chain()
    print("\n" + "=" * 60 + "\n")
    
    example_article_creation()
    print("\n" + "=" * 60 + "\n")
    
    example_custom_chain_with_branching()
    
    print("\n🎉 All examples completed!")
    print("\n💡 Tips for using prompt chaining:")
    print("   1. Keep each step focused on a single task")
    print("   2. Design clear handoffs between steps")
    print("   3. Include error handling and validation")
    print("   4. Monitor performance and costs")
    print("   5. Test individual steps before chaining")