#!/usr/bin/env python3
"""
Parallel Document Analyzer - Parallelization Agentic AI Pattern Example

This script demonstrates how multiple AI agents can analyze different documents
simultaneously, providing faster processing of large document sets.

Usage:
    python document_analyzer.py examples/sample_documents/
"""

import asyncio
import os
import time
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

@dataclass
class DocumentTask:
    """Represents a document analysis task."""
    file_path: str
    content: str
    agent_id: str

@dataclass
class AnalysisResult:
    """Represents the analysis result from a document agent."""
    agent_id: str
    file_path: str
    summary: str
    key_topics: List[str]
    sentiment: str
    word_count: int
    analysis_time: float
    timestamp: datetime

class MockDocumentAnalyzer:
    """Mock document analyzer - replace with real AI implementation."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
    
    def analyze_document(self, content: str, file_path: str) -> Dict[str, Any]:
        """Analyze a document and return insights."""
        # Simulate processing time
        time.sleep(0.3)
        
        # Mock analysis based on content
        word_count = len(content.split())
        
        # Simple keyword-based topic extraction (replace with real NLP)
        topics = []
        keywords = {
            "ai": "Artificial Intelligence",
            "machine learning": "Machine Learning", 
            "data": "Data Science",
            "algorithm": "Algorithms",
            "neural": "Neural Networks",
            "business": "Business Strategy",
            "technology": "Technology",
            "innovation": "Innovation"
        }
        
        content_lower = content.lower()
        for keyword, topic in keywords.items():
            if keyword in content_lower:
                topics.append(topic)
        
        # Mock sentiment analysis
        positive_words = ["good", "great", "excellent", "positive", "success", "benefit"]
        negative_words = ["bad", "poor", "negative", "problem", "issue", "challenge"]
        
        pos_count = sum(1 for word in positive_words if word in content_lower)
        neg_count = sum(1 for word in negative_words if word in content_lower)
        
        if pos_count > neg_count:
            sentiment = "Positive"
        elif neg_count > pos_count:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        
        # Generate summary (first 200 characters + ...)
        summary = content[:200] + "..." if len(content) > 200 else content
        
        return {
            "summary": summary,
            "key_topics": topics[:5],  # Top 5 topics
            "sentiment": sentiment,
            "word_count": word_count
        }

class ParallelDocumentProcessor:
    """Coordinates multiple document analysis agents working in parallel."""
    
    def __init__(self, max_concurrent_agents: int = 3):
        self.max_concurrent_agents = max_concurrent_agents
    
    def load_documents(self, directory_path: str) -> List[DocumentTask]:
        """Load documents from a directory."""
        tasks = []
        directory = Path(directory_path)
        
        if not directory.exists():
            print(f"❌ Directory not found: {directory_path}")
            return tasks
        
        # Support common text file formats
        supported_extensions = {'.txt', '.md', '.py', '.js', '.json', '.csv'}
        
        for i, file_path in enumerate(directory.rglob('*')):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    tasks.append(DocumentTask(
                        file_path=str(file_path),
                        content=content,
                        agent_id=f"doc_agent_{i+1}"
                    ))
                except Exception as e:
                    print(f"⚠️  Could not read {file_path}: {e}")
        
        return tasks
    
    def analyze_document(self, task: DocumentTask) -> AnalysisResult:
        """Analyze a single document using an AI agent."""
        start_time = time.time()
        
        try:
            analyzer = MockDocumentAnalyzer(task.agent_id)
            analysis = analyzer.analyze_document(task.content, task.file_path)
            
            execution_time = time.time() - start_time
            
            return AnalysisResult(
                agent_id=task.agent_id,
                file_path=task.file_path,
                summary=analysis["summary"],
                key_topics=analysis["key_topics"],
                sentiment=analysis["sentiment"],
                word_count=analysis["word_count"],
                analysis_time=execution_time,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return AnalysisResult(
                agent_id=task.agent_id,
                file_path=task.file_path,
                summary=f"Error analyzing document: {str(e)}",
                key_topics=[],
                sentiment="Unknown",
                word_count=0,
                analysis_time=execution_time,
                timestamp=datetime.now()
            )
    
    def process_documents_parallel(self, directory_path: str) -> Dict[str, Any]:
        """Process multiple documents in parallel."""
        print(f"📁 Loading documents from: {directory_path}")
        
        # Load documents
        tasks = self.load_documents(directory_path)
        
        if not tasks:
            print("❌ No documents found to process")
            return {"error": "No documents found"}
        
        print(f"📄 Found {len(tasks)} documents to analyze")
        print(f"🤖 Using {min(self.max_concurrent_agents, len(tasks))} parallel agents")
        
        # Process documents in parallel
        start_time = time.time()
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_concurrent_agents) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(self.analyze_document, task): task 
                for task in tasks
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    results.append(result)
                    filename = Path(result.file_path).name
                    print(f"✅ {result.agent_id} analyzed '{filename}' in {result.analysis_time:.2f}s")
                except Exception as e:
                    print(f"❌ {task.agent_id} failed on {task.file_path}: {str(e)}")
        
        total_time = time.time() - start_time
        
        # Generate analysis report
        report = self.generate_analysis_report(results, total_time, directory_path)
        return report
    
    def generate_analysis_report(self, results: List[AnalysisResult], total_time: float, directory_path: str) -> Dict[str, Any]:
        """Generate a comprehensive analysis report."""
        if not results:
            return {"error": "No successful analyses"}
        
        # Calculate statistics
        total_words = sum(r.word_count for r in results)
        avg_analysis_time = sum(r.analysis_time for r in results) / len(results)
        
        # Aggregate topics
        all_topics = []
        for result in results:
            all_topics.extend(result.key_topics)
        
        topic_counts = {}
        for topic in all_topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        top_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Sentiment distribution
        sentiment_counts = {}
        for result in results:
            sentiment_counts[result.sentiment] = sentiment_counts.get(result.sentiment, 0) + 1
        
        report = {
            "directory": directory_path,
            "analysis_summary": {
                "total_documents": len(results),
                "total_words_analyzed": total_words,
                "total_processing_time": total_time,
                "average_analysis_time": avg_analysis_time,
                "timestamp": datetime.now().isoformat()
            },
            "document_results": [
                {
                    "file_path": r.file_path,
                    "agent_id": r.agent_id,
                    "summary": r.summary,
                    "key_topics": r.key_topics,
                    "sentiment": r.sentiment,
                    "word_count": r.word_count,
                    "analysis_time": r.analysis_time
                }
                for r in results
            ],
            "aggregate_insights": {
                "top_topics": [{"topic": topic, "frequency": count} for topic, count in top_topics],
                "sentiment_distribution": sentiment_counts,
                "processing_efficiency": {
                    "sequential_estimate": sum(r.analysis_time for r in results),
                    "parallel_actual": total_time,
                    "speedup_factor": sum(r.analysis_time for r in results) / total_time if total_time > 0 else 1
                }
            }
        }
        
        return report

def print_analysis_report(report: Dict[str, Any]):
    """Pretty print the document analysis report."""
    if "error" in report:
        print(f"❌ Error: {report['error']}")
        return
    
    print("\n" + "="*80)
    print(f"📊 PARALLEL DOCUMENT ANALYSIS REPORT")
    print("="*80)
    
    # Summary
    summary = report['analysis_summary']
    print(f"\n📁 DIRECTORY: {report['directory']}")
    print(f"📄 Documents Analyzed: {summary['total_documents']}")
    print(f"📝 Total Words: {summary['total_words_analyzed']:,}")
    print(f"⏱️  Total Processing Time: {summary['total_processing_time']:.2f} seconds")
    print(f"⚡ Average Analysis Time: {summary['average_analysis_time']:.2f} seconds")
    
    # Efficiency metrics
    efficiency = report['aggregate_insights']['processing_efficiency']
    print(f"\n🚀 EFFICIENCY METRICS:")
    print(f"   • Sequential Estimate: {efficiency['sequential_estimate']:.2f}s")
    print(f"   • Parallel Actual: {efficiency['parallel_actual']:.2f}s")
    print(f"   • Speedup Factor: {efficiency['speedup_factor']:.1f}x")
    
    # Top topics
    top_topics = report['aggregate_insights']['top_topics']
    if top_topics:
        print(f"\n🏷️  TOP TOPICS ACROSS ALL DOCUMENTS:")
        for topic_info in top_topics[:5]:
            print(f"   • {topic_info['topic']}: {topic_info['frequency']} documents")
    
    # Sentiment distribution
    sentiment_dist = report['aggregate_insights']['sentiment_distribution']
    print(f"\n😊 SENTIMENT DISTRIBUTION:")
    for sentiment, count in sentiment_dist.items():
        print(f"   • {sentiment}: {count} documents")
    
    # Individual document results
    print(f"\n📋 INDIVIDUAL DOCUMENT RESULTS:")
    for result in report['document_results'][:5]:  # Show first 5
        filename = Path(result['file_path']).name
        print(f"\n📄 {filename}")
        print(f"   Agent: {result['agent_id']}")
        print(f"   Words: {result['word_count']}")
        print(f"   Sentiment: {result['sentiment']}")
        print(f"   Topics: {', '.join(result['key_topics'][:3])}")
        print(f"   Summary: {result['summary'][:100]}...")
    
    if len(report['document_results']) > 5:
        print(f"\n   ... and {len(report['document_results']) - 5} more documents")

def create_sample_documents():
    """Create sample documents for demonstration."""
    sample_dir = Path("examples/sample_documents")
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    sample_docs = [
        {
            "filename": "ai_overview.txt",
            "content": """Artificial Intelligence (AI) represents a revolutionary technology that is transforming industries worldwide. Machine learning algorithms enable computers to learn from data without explicit programming, while neural networks mimic the human brain's structure to process complex information. The benefits of AI include increased efficiency, automated decision-making, and the ability to analyze vast amounts of data quickly. However, challenges remain in ensuring fairness, transparency, and ethical use of these powerful technologies."""
        },
        {
            "filename": "business_strategy.md", 
            "content": """# Digital Transformation Strategy

Organizations today face unprecedented challenges in adapting to digital innovation. Successful companies are leveraging data analytics, cloud computing, and AI to gain competitive advantages. The key to successful digital transformation lies in understanding customer needs, optimizing business processes, and fostering a culture of continuous innovation. Poor planning and resistance to change can lead to failed transformation initiatives."""
        },
        {
            "filename": "technical_guide.py",
            "content": """# Technical Implementation Guide
# This document outlines algorithms and data structures for efficient processing

def process_data(input_data):
    \"\"\"
    Advanced algorithm for data processing and analysis.
    Implements machine learning techniques for pattern recognition.
    \"\"\"
    # Neural network implementation
    results = []
    for item in input_data:
        # Apply complex mathematical transformations
        processed = algorithm_transform(item)
        results.append(processed)
    return results

# Excellent performance characteristics with good scalability"""
        }
    ]
    
    for doc in sample_docs:
        file_path = sample_dir / doc["filename"]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(doc["content"])
    
    print(f"✅ Created {len(sample_docs)} sample documents in {sample_dir}")
    return str(sample_dir)

def main():
    """Main function to run the document analysis example."""
    if len(sys.argv) < 2:
        print("Creating sample documents for demonstration...")
        directory_path = create_sample_documents()
    else:
        directory_path = sys.argv[1]
    
    # Initialize the processor
    processor = ParallelDocumentProcessor(max_concurrent_agents=3)
    
    # Process documents
    report = processor.process_documents_parallel(directory_path)
    
    # Display results
    print_analysis_report(report)
    
    # Save report
    filename = f"document_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n💾 Report saved to: {filename}")

if __name__ == "__main__":
    main()