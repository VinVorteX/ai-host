import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
from typing import Optional, Dict, List

class EnhancedRAG:
    def __init__(self, faq_file: str = "faq_database.json"):
        self.faq_file = faq_file
        self.faqs = {}  # {question: answer}
        self.questions_list = []
        self.vectorizer = TfidfVectorizer(
            stop_words='english', 
            lowercase=True,
            max_features=1000,  # Limit features for speed
            ngram_range=(1, 2)  # Include bigrams for better matching
        )
        self.tfidf_matrix = None
        self._similarity_cache = {}  # Cache for repeated queries
        self._load_initial_faqs()
        
    def _load_initial_faqs(self):
        """Load initial FAQs - either from JSON or use hardcoded defaults"""
        if os.path.exists(self.faq_file):
            self._load_from_json()
        else:
            self._load_hardcoded_faqs()
            self._save_to_json()
    
    def _load_hardcoded_faqs(self):
        """Your original hardcoded FAQs"""
        self.faqs = {
            "what is the nextgen supercomputing club": "We're a student-led club founded in 2025, dedicated to exploring high-performance computing and its applications in AI, scientific simulations, and big data. We offer hands-on learning, access to advanced hardware like NVIDIA DGX systems, and a community of tech enthusiasts. Our motto is 'Compute the Future, Today!'",
            "how to join": "Anyone passionate about computing can join! Students, faculty, and professionals from any discipline are welcome. No prior HPC experience required. Sign up at our inauguration or email nextgenclub@university.edu.",
            "what will the club do": "We host workshops on GPU programming, MPI, quantum computing basics, and provide access to NVIDIA DGX systems. You can work on projects like AI model training, parallel algorithm optimization, or quantum system simulations.",
            "what is supercomputing": "Supercomputing involves using powerful computers to solve complex problems at incredible speeds. Think AI training, climate modeling, or drug discovery. The Frontier supercomputer achieves 1.1 exaFLOPS, performing quintillions of calculations per second!",
            "whats the first event": "Our inauguration hackathon on October 15, 2025, where you'll build projects on our NVIDIA DGX system. It's a fun, collaborative way to kick off the club with prizes including cloud credits and mentorship sessions.",
            "what kind of projects": "You can develop AI models, optimize parallel algorithms, or simulate quantum systems. Past projects include neural network training, molecular dynamics, and climate simulations. We support all skill levels.",
            "do i need coding experience": "Not at all! We offer beginner-friendly workshops on Python, CUDA, and MPI. Our community supports all skill levels, from novices to experts.",
            "what resources": "We provide access to NVIDIA DGX systems, cloud HPC platforms, and software like TensorFlow, PyTorch, and OpenMPI. Plus, mentorship from industry experts and faculty members.",
            "whats exascale computing": "Exascale computers perform over a quintillion calculations per second - that's 10 to the 18th power! They're key for AI, physics simulations, and big data analytics.",
            "why should i care about hpc": "HPC powers breakthroughs in AI, medicine, and climate science. Learning HPC skills opens doors to careers in tech, research, and innovation."
        }
        self.questions_list = list(self.faqs.keys())
        self._update_vectorizer()
    
    def _load_from_json(self):
        """Load FAQs from JSON file"""
        try:
            with open(self.faq_file, 'r') as f:
                data = json.load(f)
                self.faqs = data.get("faqs", {})
                self.questions_list = list(self.faqs.keys())
                self._update_vectorizer()
                print(f"✅ Loaded {len(self.faqs)} FAQs from {self.faq_file}")
        except Exception as e:
            print(f"❌ Error loading FAQ JSON: {e}. Using hardcoded FAQs.")
            self._load_hardcoded_faqs()
    
    def _save_to_json(self):
        """Save FAQs to JSON file"""
        try:
            data = {"faqs": self.faqs}
            with open(self.faq_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✅ Saved {len(self.faqs)} FAQs to {self.faq_file}")
        except Exception as e:
            print(f"❌ Error saving FAQ JSON: {e}")
    
    def _update_vectorizer(self):
        """Update TF-IDF vectorizer with current questions"""
        if self.questions_list:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.questions_list)
    
    def add_faq(self, question: str, answer: str):
        """Add a new FAQ question-answer pair"""
        normalized_question = question.lower().strip()
        self.faqs[normalized_question] = answer
        
        # Update data structures
        if normalized_question not in self.questions_list:
            self.questions_list.append(normalized_question)
            self._update_vectorizer()
        
        # Auto-save to JSON
        self._save_to_json()
        print(f"✅ Added new FAQ: '{question}'")
    
    def find_best_match(self, user_question: str, similarity_threshold: float = 0.3) -> Optional[str]:
        """
        Find the best matching FAQ using TF-IDF cosine similarity.
        
        Args:
            user_question: The user's input question
            similarity_threshold: Minimum similarity score (0.0-1.0)
            
        Returns:
            Answer string if good match found, None otherwise
        """
        if not self.questions_list or not user_question.strip():
            return None
        
        user_question_clean = user_question.lower().strip()
        
        # Quick exact match first (fastest)
        if user_question_clean in self.faqs:
            return self.faqs[user_question_clean]
        
        # Check cache for repeated queries
        if user_question_clean in self._similarity_cache:
            cached_result = self._similarity_cache[user_question_clean]
            if cached_result:
                return self.faqs[cached_result]
            return None
        
        # TF-IDF similarity matching
        try:
            user_vector = self.vectorizer.transform([user_question_clean])
            similarities = cosine_similarity(user_vector, self.tfidf_matrix).flatten()
            
            best_match_idx = np.argmax(similarities)
            best_similarity = similarities[best_match_idx]
            
            if best_similarity > similarity_threshold:
                best_question = self.questions_list[best_match_idx]
                self._similarity_cache[user_question_clean] = best_question  # Cache result
                return self.faqs[best_question]
            else:
                self._similarity_cache[user_question_clean] = None  # Cache negative result
                return None
                
        except Exception as e:
            print(f"❌ Error in similarity matching: {e}")
            return None
    
    def get_faq_count(self) -> int:
        """Get total number of FAQs"""
        return len(self.faqs)
    
    def list_faqs(self) -> List[str]:
        """List all FAQ questions"""
        return list(self.faqs.keys())

# Global instance
faq_system = EnhancedRAG()

def simple_rag_lookup(question: str) -> Optional[str]:
    """
    Main interface function - uses enhanced RAG system.
    
    Args:
        question: User's question
        
    Returns:
        Answer if found in FAQs, None otherwise
    """
    return faq_system.find_best_match(question)