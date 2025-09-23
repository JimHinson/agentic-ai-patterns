"""
Prompt Chaining Pattern Implementation

This module demonstrates the prompt chaining pattern where the output of one 
prompt becomes the input to the next prompt in a sequence, creating a pipeline 
of AI interactions.

Example use case: Article creation pipeline
"""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime


class PromptStep:
    """Represents a single step in a prompt chain"""
    
    def __init__(self, name: str, prompt_template: str, description: str = ""):
        self.name = name
        self.prompt_template = prompt_template
        self.description = description
        self.execution_time = None
        self.input_data = None
        self.output_data = None
    
    def format_prompt(self, **kwargs) -> str:
        """Format the prompt template with provided variables"""
        return self.prompt_template.format(**kwargs)
    
    def execute(self, previous_output: str = "", **kwargs) -> str:
        """
        Execute this step of the chain
        In a real implementation, this would call an LLM API
        For demonstration, we provide mock responses
        """
        start_time = datetime.now()
        
        # Store input for logging
        self.input_data = {"previous_output": previous_output, **kwargs}
        
        # Mock LLM response based on step name
        if self.name == "research":
            output = self._mock_research_response(kwargs.get("topic", ""))
        elif self.name == "structure":
            output = self._mock_structure_response(previous_output)
        elif self.name == "draft":
            output = self._mock_draft_response(previous_output)
        elif self.name == "review":
            output = self._mock_review_response(previous_output)
        elif self.name == "finalize":
            output = self._mock_finalize_response(previous_output)
        else:
            output = f"Processed: {previous_output[:100]}..."
        
        # Store output and execution time
        self.output_data = output
        self.execution_time = (datetime.now() - start_time).total_seconds()
        
        return output
    
    def _mock_research_response(self, topic: str) -> str:
        """Mock research response"""
        return f"""Research findings for "{topic}":

Key Points:
- {topic} is a rapidly evolving field with significant applications
- Current trends show increased adoption in various sectors
- Key benefits include efficiency improvements and cost reduction
- Main challenges involve implementation complexity and ethical considerations
- Future outlook suggests continued growth and innovation

Sources: Academic papers, industry reports, expert interviews
"""
    
    def _mock_structure_response(self, research: str) -> str:
        """Mock structure response"""
        return """Article Outline:

1. Introduction
   - Definition and overview
   - Importance and relevance

2. Current State
   - Recent developments
   - Market trends

3. Benefits and Applications
   - Key advantages
   - Real-world use cases

4. Challenges and Considerations
   - Technical challenges
   - Ethical implications

5. Future Outlook
   - Emerging trends
   - Predictions

6. Conclusion
   - Summary of key points
   - Call to action
"""
    
    def _mock_draft_response(self, outline: str) -> str:
        """Mock draft response"""
        return """# Understanding the Impact of Modern Technology

## Introduction

In today's rapidly evolving technological landscape, we are witnessing unprecedented changes that are reshaping how we work, live, and interact. This comprehensive analysis explores the current state, benefits, challenges, and future outlook of these transformative technologies.

## Current State

The field has experienced remarkable growth over the past decade, with significant breakthroughs in various areas. Market adoption has accelerated, driven by increased awareness and demonstrated value propositions.

## Benefits and Applications

Key advantages include:
- Enhanced efficiency and productivity
- Cost reduction and resource optimization
- Improved decision-making capabilities
- Greater accessibility and democratization

Real-world applications span multiple industries, from healthcare to finance, education to manufacturing.

## Challenges and Considerations

Despite the promising benefits, several challenges remain:
- Technical complexity and implementation barriers
- Ethical considerations and responsible use
- Privacy and security concerns
- Need for skilled workforce and training

## Future Outlook

Looking ahead, we can expect continued innovation and adoption. Emerging trends suggest more sophisticated applications and broader integration across sectors.

## Conclusion

The technology represents a significant opportunity for organizations willing to invest in understanding and implementing these solutions thoughtfully and responsibly.
"""
    
    def _mock_review_response(self, draft: str) -> str:
        """Mock review response"""
        return """Review and Improvement Suggestions:

Strengths:
- Good overall structure and flow
- Covers key topics comprehensively
- Professional tone and style

Areas for Improvement:
1. Add specific examples and case studies
2. Include recent statistics and data points
3. Expand on technical details where appropriate
4. Add more concrete recommendations
5. Strengthen the conclusion with actionable insights

Suggested Revisions:
- Introduction: Add compelling statistics to grab attention
- Benefits section: Include quantitative examples
- Challenges: Provide specific mitigation strategies
- Future outlook: Add timeline predictions
- Conclusion: Include clear next steps for readers
"""
    
    def _mock_finalize_response(self, review_feedback: str) -> str:
        """Mock finalize response"""
        return """# The Transformative Power of Modern Technology: A Comprehensive Guide

## Introduction

Modern technology is revolutionizing our world at an unprecedented pace. According to recent studies, 87% of organizations report significant improvements in efficiency after adopting new technological solutions. This comprehensive guide explores the current landscape, benefits, challenges, and future trajectory of transformative technologies.

## Current State and Market Trends

The technology sector has grown by 12% annually over the past five years, with venture capital investment reaching $150 billion in 2023. Key developments include:

- Advanced automation solutions reducing operational costs by 30-40%
- AI-powered analytics improving decision accuracy by 25%
- Cloud-based platforms enabling 99.9% uptime for critical systems

## Benefits and Real-World Applications

### Healthcare
- Diagnostic accuracy improved by 40% using AI imaging
- Patient outcome tracking reduced readmission rates by 15%
- Telemedicine expanded access to care for rural populations

### Finance
- Fraud detection systems prevented $2.8 billion in losses
- Automated trading algorithms improved returns by 18%
- Customer service chatbots handle 70% of routine inquiries

### Manufacturing
- Predictive maintenance reduced downtime by 35%
- Quality control automation decreased defect rates by 50%
- Supply chain optimization cut costs by 20%

## Challenges and Mitigation Strategies

### Technical Challenges
- **Implementation Complexity**: Start with pilot programs and scale gradually
- **Integration Issues**: Invest in robust APIs and middleware solutions
- **Skills Gap**: Develop comprehensive training programs

### Ethical Considerations
- **Privacy Protection**: Implement strict data governance policies
- **Bias Prevention**: Regular algorithm audits and diverse training data
- **Transparency**: Clear communication about AI decision-making processes

## Future Outlook (2024-2030)

- **2024-2025**: Widespread adoption of conversational AI interfaces
- **2025-2027**: Integration of quantum computing in specific applications
- **2027-2030**: Emergence of fully autonomous business processes

Market projections suggest 300% growth in technology spending by 2030, with particular emphasis on sustainability and ethical AI.

## Conclusion and Next Steps

The technological revolution presents unprecedented opportunities for organizations ready to embrace change. To succeed:

1. **Start Now**: Begin with small-scale implementations
2. **Invest in People**: Prioritize training and change management
3. **Focus on Value**: Measure ROI and adjust strategies accordingly
4. **Stay Ethical**: Implement responsible AI practices from the start

The future belongs to organizations that can harness technology's power while maintaining human values and ethical standards. The time to act is now.

---

*This analysis is based on industry research, expert interviews, and peer-reviewed studies conducted in 2023-2024.*
"""


class PromptChain:
    """Main class for managing and executing prompt chains"""
    
    def __init__(self):
        self.steps: List[PromptStep] = []
        self.execution_log: List[Dict[str, Any]] = []
    
    def add_step(self, step: PromptStep):
        """Add a step to the chain"""
        self.steps.append(step)
    
    def execute(self, initial_input: str, **kwargs) -> str:
        """Execute the complete chain"""
        current_output = initial_input
        
        # Clear previous execution log
        self.execution_log = []
        
        print(f"🚀 Starting prompt chain execution with input: '{initial_input[:50]}...'")
        print("=" * 60)
        
        for i, step in enumerate(self.steps, 1):
            print(f"\n📋 Step {i}: {step.name.title()}")
            print(f"Description: {step.description}")
            print("-" * 40)
            
            # Execute the step
            if i == 1:
                # First step gets the initial input plus any additional kwargs
                current_output = step.execute(previous_output="", topic=current_output, **kwargs)
            else:
                current_output = step.execute(previous_output=current_output, **kwargs)
            
            # Log the execution
            log_entry = {
                "step_number": i,
                "step_name": step.name,
                "execution_time": step.execution_time,
                "input_length": len(str(step.input_data)),
                "output_length": len(current_output),
                "timestamp": datetime.now().isoformat()
            }
            self.execution_log.append(log_entry)
            
            print(f"✅ Completed in {step.execution_time:.2f}s")
            print(f"📄 Output length: {len(current_output)} characters")
            
            # Show preview of output
            preview = current_output[:200].replace('\n', ' ')
            print(f"📝 Preview: {preview}...")
        
        print("\n" + "=" * 60)
        print("🎉 Chain execution completed successfully!")
        self._print_summary()
        
        return current_output
    
    def _print_summary(self):
        """Print execution summary"""
        total_time = sum(log["execution_time"] for log in self.execution_log)
        print(f"\n📊 Execution Summary:")
        print(f"   Total steps: {len(self.execution_log)}")
        print(f"   Total time: {total_time:.2f}s")
        print(f"   Average time per step: {total_time/len(self.execution_log):.2f}s")
    
    def get_execution_log(self) -> List[Dict[str, Any]]:
        """Get the execution log"""
        return self.execution_log
    
    def save_log(self, filename: str):
        """Save execution log to file"""
        with open(filename, 'w') as f:
            json.dump(self.execution_log, f, indent=2)


def create_article_creation_chain() -> PromptChain:
    """Create a prompt chain for article creation"""
    
    chain = PromptChain()
    
    # Step 1: Research
    research_step = PromptStep(
        name="research",
        prompt_template="""Conduct comprehensive research on the topic: {topic}
        
        Please provide:
        1. Key concepts and definitions
        2. Current trends and developments
        3. Main benefits and applications
        4. Challenges and limitations
        5. Future outlook
        
        Focus on factual, up-to-date information from reliable sources.""",
        description="Gather comprehensive information about the topic"
    )
    
    # Step 2: Structure
    structure_step = PromptStep(
        name="structure",
        prompt_template="""Based on the following research, create a detailed outline for a comprehensive article:

        Research: {previous_output}
        
        Create an outline with:
        - Clear section headings
        - Subsections where appropriate
        - Logical flow of information
        - Estimated word count for each section""",
        description="Create a structured outline based on research findings"
    )
    
    # Step 3: Draft
    draft_step = PromptStep(
        name="draft",
        prompt_template="""Write a comprehensive article following this outline:

        Outline: {previous_output}
        
        Requirements:
        - Professional, engaging tone
        - Clear headings and subheadings
        - Include specific examples where possible
        - Aim for 800-1200 words
        - Include an introduction and conclusion""",
        description="Write the initial article draft following the outline"
    )
    
    # Step 4: Review
    review_step = PromptStep(
        name="review",
        prompt_template="""Please review the following article draft and provide detailed feedback:

        Draft: {previous_output}
        
        Evaluate:
        1. Content quality and accuracy
        2. Structure and flow
        3. Clarity and readability
        4. Areas for improvement
        5. Specific suggestions for enhancement
        
        Provide constructive criticism and actionable recommendations.""",
        description="Review the draft and provide improvement suggestions"
    )
    
    # Step 5: Finalize
    finalize_step = PromptStep(
        name="finalize",
        prompt_template="""Based on the following review feedback, create the final polished version of the article:

        Review Feedback: {previous_output}
        
        Apply the suggested improvements and create a publication-ready article that:
        - Addresses all feedback points
        - Maintains professional quality
        - Is well-structured and engaging
        - Includes proper formatting""",
        description="Apply feedback and create the final polished article"
    )
    
    # Add all steps to the chain
    chain.add_step(research_step)
    chain.add_step(structure_step)
    chain.add_step(draft_step)
    chain.add_step(review_step)
    chain.add_step(finalize_step)
    
    return chain


if __name__ == "__main__":
    # Example usage
    print("🔗 Prompt Chaining Pattern Demo")
    print("Creating an article about 'Artificial Intelligence in Healthcare'\n")
    
    # Create and execute the chain
    chain = create_article_creation_chain()
    result = chain.execute("Artificial Intelligence in Healthcare")
    
    # Save the execution log
    chain.save_log("execution_log.json")
    print(f"\n💾 Execution log saved to 'execution_log.json'")
    
    # Save the final result
    with open("generated_article.md", "w") as f:
        f.write(result)
    print(f"📄 Generated article saved to 'generated_article.md'")