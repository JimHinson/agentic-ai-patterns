#!/usr/bin/env python3
"""
Parallel Content Generator - Parallelization Agentic AI Pattern Example

This script demonstrates how multiple AI agents can generate different sections
of content simultaneously, enabling faster creation of comprehensive materials.

Usage:
    python content_generator.py "comprehensive guide to machine learning"
"""

import asyncio
import time
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ContentSection:
    """Represents a content section to be generated."""
    section_id: str
    title: str
    description: str
    agent_id: str

@dataclass
class GeneratedContent:
    """Represents generated content from an agent."""
    agent_id: str
    section_id: str
    title: str
    content: str
    word_count: int
    generation_time: float
    timestamp: datetime

class MockContentGenerator:
    """Mock content generator - replace with real AI implementation."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
    
    def generate_content(self, title: str, description: str) -> str:
        """Generate content for a specific section."""
        # Simulate content generation time
        time.sleep(0.4)
        
        # Mock content based on the section
        content_templates = {
            "introduction": """
## Introduction

{title} has become increasingly important in today's digital landscape. This comprehensive guide will provide you with the foundational knowledge and practical insights needed to understand and apply these concepts effectively.

In this section, we'll explore the fundamental principles, key terminology, and the historical context that has shaped this field. Whether you're a beginner looking to get started or an experienced practitioner seeking to deepen your understanding, this guide offers valuable perspectives and actionable insights.

The importance of this topic cannot be overstated in our rapidly evolving technological environment. As businesses and individuals continue to adapt to digital transformation, understanding these concepts becomes crucial for success and innovation.
""",
            "fundamentals": """
## Core Fundamentals

Understanding the fundamental principles is essential for mastering any complex topic. In this section, we'll break down the key concepts into digestible components:

### Key Principles
- **Principle 1**: Foundation concepts that form the basis of understanding
- **Principle 2**: Advanced theories that build upon basic knowledge
- **Principle 3**: Practical applications and real-world implementations

### Essential Components
The core components include various elements that work together to create a comprehensive system. Each component plays a crucial role in the overall functionality and effectiveness of the approach.

### Best Practices
Following established best practices ensures optimal results and helps avoid common pitfalls that can derail progress.
""",
            "implementation": """
## Implementation Guide

This section provides practical guidance for implementing the concepts discussed in previous sections. We'll cover step-by-step processes, common challenges, and proven strategies for success.

### Getting Started
1. **Assessment Phase**: Evaluate current capabilities and requirements
2. **Planning Phase**: Develop a comprehensive implementation strategy
3. **Execution Phase**: Begin implementation with proper monitoring
4. **Optimization Phase**: Refine and improve based on results

### Tools and Technologies
Various tools and technologies can facilitate implementation. Selecting the right combination depends on specific requirements, budget constraints, and organizational capabilities.

### Common Challenges
Implementation often involves overcoming various obstacles. Being aware of potential challenges allows for proactive planning and risk mitigation.
""",
            "advanced_topics": """
## Advanced Topics

For those ready to explore more sophisticated concepts, this section delves into advanced topics that can significantly enhance understanding and capabilities.

### Advanced Techniques
Sophisticated techniques require deeper knowledge but offer greater potential for innovation and optimization. These approaches often involve:

- Complex algorithmic implementations
- Integration with multiple systems and platforms
- Advanced data processing and analysis methods
- Scalability considerations for large-scale applications

### Cutting-Edge Research
The field continues to evolve rapidly, with new research contributing to our understanding and opening new possibilities for application.

### Future Considerations
Looking ahead, several trends and developments will likely shape the future direction of this field.
""",
            "case_studies": """
## Real-World Case Studies

Learning from practical examples helps bridge the gap between theory and application. This section presents detailed case studies that illustrate successful implementations.

### Case Study 1: Enterprise Implementation
A large organization successfully implemented these concepts, resulting in significant improvements in efficiency and outcomes. Key factors in their success included:

- Strong leadership commitment
- Comprehensive training programs
- Phased implementation approach
- Continuous monitoring and adjustment

### Case Study 2: Small Business Success
A small business demonstrated that these concepts are scalable and applicable across different organizational sizes. Their approach focused on:

- Resource optimization
- Targeted implementation
- Community support and collaboration
- Measurable results and ROI

### Lessons Learned
These case studies highlight common patterns and provide valuable insights for future implementations.
""",
            "conclusion": """
## Conclusion and Next Steps

This comprehensive guide has covered the essential aspects of {title}, from fundamental principles to advanced implementation strategies. The key takeaways include:

### Key Insights
- Understanding core principles is essential for successful implementation
- Practical application requires careful planning and execution
- Continuous learning and adaptation are crucial for long-term success
- Real-world examples provide valuable guidance and inspiration

### Recommended Actions
To make the most of the knowledge presented in this guide:

1. **Start Small**: Begin with manageable implementations to build experience
2. **Seek Community**: Connect with others who share similar interests and challenges
3. **Stay Updated**: Continue learning about new developments and best practices
4. **Apply Iteratively**: Use an iterative approach to continuously improve results

### Future Learning
This guide provides a solid foundation, but the journey of learning and improvement continues. Consider exploring specialized topics, attending workshops, and participating in relevant communities to further develop your expertise.

The field continues to evolve, offering exciting opportunities for innovation and growth. By applying the concepts and strategies outlined in this guide, you'll be well-positioned to achieve success and make meaningful contributions.
"""
        }
        
        # Select appropriate template
        section_key = None
        for key in content_templates.keys():
            if key in title.lower() or key in description.lower():
                section_key = key
                break
        
        if not section_key:
            section_key = "fundamentals"  # default
        
        content = content_templates[section_key].format(title=title).strip()
        return content

class ParallelContentCoordinator:
    """Coordinates multiple content generation agents working in parallel."""
    
    def __init__(self, max_concurrent_agents: int = 4):
        self.max_concurrent_agents = max_concurrent_agents
    
    def create_content_sections(self, topic: str) -> List[ContentSection]:
        """Create content sections for a comprehensive guide."""
        sections = [
            {
                "id": "introduction",
                "title": f"Introduction to {topic}",
                "description": f"Provide an engaging introduction to {topic}, including overview, importance, and what readers will learn."
            },
            {
                "id": "fundamentals", 
                "title": f"Fundamentals of {topic}",
                "description": f"Explain the core concepts, principles, and foundational knowledge needed to understand {topic}."
            },
            {
                "id": "implementation",
                "title": f"Implementation Guide for {topic}",
                "description": f"Provide practical, step-by-step guidance for implementing {topic} concepts in real-world scenarios."
            },
            {
                "id": "advanced_topics",
                "title": f"Advanced {topic} Topics",
                "description": f"Cover advanced concepts, techniques, and cutting-edge developments in {topic}."
            },
            {
                "id": "case_studies",
                "title": f"{topic} Case Studies",
                "description": f"Present real-world examples and case studies demonstrating successful application of {topic}."
            },
            {
                "id": "conclusion",
                "title": f"Conclusion and Next Steps for {topic}",
                "description": f"Summarize key points, provide actionable next steps, and suggest additional resources for {topic}."
            }
        ]
        
        return [
            ContentSection(
                section_id=section["id"],
                title=section["title"],
                description=section["description"],
                agent_id=f"content_agent_{i+1}_{section['id']}"
            )
            for i, section in enumerate(sections)
        ]
    
    def generate_section_content(self, section: ContentSection) -> GeneratedContent:
        """Generate content for a specific section."""
        start_time = time.time()
        
        try:
            generator = MockContentGenerator(section.agent_id)
            content = generator.generate_content(section.title, section.description)
            word_count = len(content.split())
            generation_time = time.time() - start_time
            
            return GeneratedContent(
                agent_id=section.agent_id,
                section_id=section.section_id,
                title=section.title,
                content=content,
                word_count=word_count,
                generation_time=generation_time,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            generation_time = time.time() - start_time
            return GeneratedContent(
                agent_id=section.agent_id,
                section_id=section.section_id,
                title=section.title,
                content=f"Error generating content: {str(e)}",
                word_count=0,
                generation_time=generation_time,
                timestamp=datetime.now()
            )
    
    def generate_content_parallel(self, topic: str) -> Dict[str, Any]:
        """Generate comprehensive content using parallel agents."""
        print(f"📝 Starting parallel content generation for: '{topic}'")
        
        # Create content sections
        sections = self.create_content_sections(topic)
        print(f"📋 Created {len(sections)} content sections")
        print(f"🤖 Using {min(self.max_concurrent_agents, len(sections))} parallel agents")
        
        # Generate content in parallel
        start_time = time.time()
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_concurrent_agents) as executor:
            # Submit all tasks
            future_to_section = {
                executor.submit(self.generate_section_content, section): section 
                for section in sections
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_section):
                section = future_to_section[future]
                try:
                    result = future.result()
                    results.append(result)
                    print(f"✅ {result.agent_id} generated '{result.section_id}' ({result.word_count} words) in {result.generation_time:.2f}s")
                except Exception as e:
                    print(f"❌ {section.agent_id} failed on {section.section_id}: {str(e)}")
        
        total_time = time.time() - start_time
        
        # Compile final document
        document = self.compile_final_document(topic, results, total_time)
        return document
    
    def compile_final_document(self, topic: str, results: List[GeneratedContent], total_time: float) -> Dict[str, Any]:
        """Compile all generated content into a final document."""
        # Sort results by section order
        section_order = ["introduction", "fundamentals", "implementation", "advanced_topics", "case_studies", "conclusion"]
        results_sorted = sorted(results, key=lambda x: section_order.index(x.section_id) if x.section_id in section_order else 999)
        
        total_words = sum(r.word_count for r in results)
        total_generation_time = sum(r.generation_time for r in results)
        
        document = {
            "title": f"Comprehensive Guide to {topic}",
            "generation_summary": {
                "topic": topic,
                "total_sections": len(results),
                "total_words": total_words,
                "total_generation_time": total_generation_time,
                "parallel_execution_time": total_time,
                "speedup_factor": total_generation_time / total_time if total_time > 0 else 1,
                "timestamp": datetime.now().isoformat()
            },
            "sections": [
                {
                    "section_id": result.section_id,
                    "title": result.title,
                    "content": result.content,
                    "word_count": result.word_count,
                    "agent_id": result.agent_id,
                    "generation_time": result.generation_time
                }
                for result in results_sorted
            ],
            "full_document": self.create_full_document(topic, results_sorted)
        }
        
        return document
    
    def create_full_document(self, topic: str, results: List[GeneratedContent]) -> str:
        """Create a single consolidated document from all sections."""
        document_parts = [
            f"# Comprehensive Guide to {topic}",
            f"*Generated by Parallel AI Agents on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
            "",
            "---",
            ""
        ]
        
        for result in results:
            document_parts.append(result.content)
            document_parts.append("")
            document_parts.append("---")
            document_parts.append("")
        
        return "\n".join(document_parts)

def print_generation_report(document: Dict[str, Any]):
    """Pretty print the content generation report."""
    print("\n" + "="*80)
    print(f"📚 PARALLEL CONTENT GENERATION REPORT")
    print("="*80)
    
    # Summary
    summary = document['generation_summary']
    print(f"\n📝 DOCUMENT: {document['title']}")
    print(f"📊 Generation Summary:")
    print(f"   • Sections Generated: {summary['total_sections']}")
    print(f"   • Total Words: {summary['total_words']:,}")
    print(f"   • Sequential Time Estimate: {summary['total_generation_time']:.2f}s")
    print(f"   • Parallel Execution Time: {summary['parallel_execution_time']:.2f}s")
    print(f"   • Speedup Factor: {summary['speedup_factor']:.1f}x")
    
    # Section details
    print(f"\n📋 SECTION DETAILS:")
    for section in document['sections']:
        print(f"\n🎯 {section['title']}")
        print(f"   Agent: {section['agent_id']}")
        print(f"   Words: {section['word_count']}")
        print(f"   Time: {section['generation_time']:.2f}s")
        print(f"   Preview: {section['content'][:100]}...")

def save_document_files(document: Dict[str, Any]):
    """Save the generated document to files."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save full document as markdown
    doc_filename = f"generated_guide_{timestamp}.md"
    with open(doc_filename, 'w', encoding='utf-8') as f:
        f.write(document['full_document'])
    
    # Save detailed report as JSON
    report_filename = f"generation_report_{timestamp}.json"
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(document, f, indent=2, default=str)
    
    print(f"\n💾 Files saved:")
    print(f"   • Full Document: {doc_filename}")
    print(f"   • Detailed Report: {report_filename}")
    
    return doc_filename, report_filename

def main():
    """Main function to run the content generation example."""
    if len(sys.argv) < 2:
        print("Usage: python content_generator.py \"<content topic>\"")
        sys.exit(1)
    
    topic = sys.argv[1]
    
    # Initialize the coordinator
    coordinator = ParallelContentCoordinator(max_concurrent_agents=4)
    
    # Generate content
    document = coordinator.generate_content_parallel(topic)
    
    # Display results
    print_generation_report(document)
    
    # Save files
    save_document_files(document)

if __name__ == "__main__":
    main()