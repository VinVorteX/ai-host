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
            "what is your name": "My name is Riva. I'm the AI voice assistant for the NextGen Supercomputing Club.",
            "aapka naam kya hai": "Mera naam Riva hai. Main NextGen Supercomputing Club ka AI voice assistant hoon.",
            "tumhara naam kya hai": "Mera naam Riva hai.",
            "what are you called": "I'm called Riva.",
            "who are you": "I'm Riva, your AI assistant for the NextGen Supercomputing Club.",
            "tum kaun ho": "Main Riva hoon, NextGen Supercomputing Club ka AI assistant.",
            "what is the nextgen supercomputing club": "We're a student-led club founded in 2025, dedicated to advancing computational excellence through education, collaboration, and innovation. We explore high-performance computing, AI acceleration, quantum simulation, parallel programming, and GPU development through hands-on projects, hackathons, and workshops.",
            "how to join": "Anyone passionate about computing can join! Students, faculty, and professionals from any discipline are welcome. No prior HPC experience required — just curiosity and a desire to learn.",
            "who can join the club": "Anyone interested in computing and innovation is welcome! You don’t need prior HPC experience — we’ll help you get started with workshops, mentorship, and collaborative projects.",
            "what will the club do": "We organize hands-on workshops, hackathons, and collaborative research projects across HPC, AI, and quantum computing. Members explore GPU clusters, exascale simulations, and AI-driven research using advanced resources like NVIDIA DGX systems and cloud HPC platforms.",
            "what is supercomputing": "Supercomputing uses extremely powerful computers to perform complex calculations at unmatched speeds. It's used for AI training, weather prediction, drug discovery, and quantum physics simulations. For example, the Frontier supercomputer performs 1.1 exaFLOPS — over a quintillion calculations per second.",
            "what kind of projects": "You can build AI models, optimize parallel algorithms, or simulate quantum systems. Past projects include neural network training, molecular dynamics experiments, and climate modeling. Our mentors support all experience levels.",
            "do i need coding experience": "Not at all! We offer beginner-friendly workshops on Python, CUDA, and MPI. Whether you’re new to coding or an expert developer, there’s a place for you in the club.",
            "what resources": "We provide access to NVIDIA DGX systems, cloud HPC platforms, and open-source tools like TensorFlow, PyTorch, CUDA, and OpenMPI. Members also receive guidance from faculty experts and industry mentors.",
            "whats exascale computing": "Exascale computing refers to systems capable of executing over one quintillion (10^18) calculations per second. It’s crucial for scientific simulations, AI training, and big data analysis — and our club helps members explore how exascale computing shapes the future.",
            "why should i care about hpc": "High-performance computing drives discoveries in AI, medicine, climate modeling, and beyond. Learning HPC gives you valuable technical skills and career opportunities while letting you help build the technologies of tomorrow.",
            "who are the club members": "The club's core committee includes: President – Shreya Jain, Vice President – Samarth Shukla, PR Head – Ujjawal Tyagi, Graphics Head – Preeti Singh, Event Management (Leads) – Srashti Gupta and Vidisha Goel, Technical Leads – Ronak Goel and Vinayak Rastogi, Treasurer – Divyansh Verma.",
            "who is the president": "The President of the NextGen Supercomputing Club is Shreya Jain. She leads the club’s strategic direction, initiatives, and collaborations, driving its mission to advance computational innovation.",
            "who is the vice president": "The Vice President is Samarth Shukla. He supports the President in managing club operations and coordinates between departments to ensure smooth execution of events and projects.",
            "who is the pr head": "The PR Head is Ujjawal Tyagi. He manages the club’s external communications, social media presence, and public relations to increase outreach and community engagement.",
            "who is the graphics head": "The Graphics Head is Preeti Singh. She oversees all design and creative outputs, including event posters, digital campaigns, and visual branding for the club.",
            "who are the event management leads": "The Event Management Leads are Srashti Gupta and Vidisha Goel. They plan, organize, and execute all club events — from hackathons to workshops — ensuring everything runs smoothly.",
            "who are the technical leads": "The Technical Leads are Vinayak Rastogi and Ronak Goel. They guide members on HPC projects, conduct coding workshops, and maintain the technical infrastructure of the club.",
            "who is the treasurer": "The Treasurer is Divyansh Verma. He manages the club’s finances, budgeting, and resource allocation for events, ensuring financial transparency and stability.",
            "fun facts": "1. The world’s fastest supercomputer, Frontier, is 1,000x faster than a high-end laptop.\n2. Supercomputing helped design COVID-19 vaccines by simulating protein interactions.\n3. Our club’s NVIDIA DGX can train AI models 10x faster than a standard GPU."
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
    
    def find_best_match(self, user_question: str, similarity_threshold: float = 0.25) -> Optional[str]:
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