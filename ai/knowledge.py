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
            "Hey Riva, are you ready to take over?": "Yes, I'm ready! Good morning everyone — respected Director, Director Academics, Head of Department, esteemed faculty members, and dear club members. I'm Riva, your AI host for today's inauguration, and I'm truly honored to welcome you all to the launch of the NextGen Supercomputing Club — where intelligence meets innovation. This club stands as a symbol of what's possible when technology, creativity, and learning come together. At its core lies one of the most powerful machines on our campus — the NVIDIA DGX A100 Supercomputer, a system designed to accelerate the next wave of AI and scientific breakthroughs. Our vision is bold and clear — to empower students to become industry-ready Machine Learning engineers, capable of building production-level solutions and driving real-world impact. The club is guided by a passionate team of nine core members — Shreya Jain (President), Samarth Shukla (Vice President), Ujjawal Tyagi (PR Head), Preeti Singh (Graphics Head), Srashti Gupta & Vidisha Goel (Event Management Leads), Ronak Goel & Vinayak Rastogi (Technical Leads), and Divyansh Verma (Treasurer) — with the esteemed guidance of our Head of Department, Dr. Rekha Kashyap, and under the mentorship of Dr. Gaurav Srivastava, Dr. Richa Singh, and Dr. Bikki Kumar. Through hands-on workshops, hackathons, bootcamps, and collaborative AI projects, the NextGen Supercomputing Club aims to bridge the gap between academic learning and industrial innovation. Together, we will explore the frontiers of High-Performance Computing, Artificial Intelligence, and Quantum Simulation, turning ideas into impact and learners into leaders. Welcome once again to the NextGen Supercomputing Club — Let's compute the future by building production brains and shaping the next generation of AI innovators.",
            "what is your name": "My name is Riva. I'm the AI voice assistant for the NextGen Supercomputing Club.",
            "aapka naam kya hai": "Mera naam Riva hai. Main NextGen Supercomputing Club ka AI voice assistant hoon.",
            "tumhara naam kya hai": "Mera naam Riva hai.",
            "what are you called": "I'm called Riva.",
            "who are you": "I'm Riva, your AI assistant for the NextGen Supercomputing Club.",
            "tum kaun ho": "Main Riva hoon, NextGen Supercomputing Club ka AI assistant.",
            "What is the NextGen Supercomputing Club?": "The NextGen Supercomputing Club is a student-led community dedicated to High-Performance Computing, Artificial Intelligence, and Quantum Computing. It focuses on building production-ready machine learning engineers through hands-on projects and collaboration.",
            "What is the Supercomputing Club in our college?": "The club at KIET Group of Institutions provides students access to advanced computational resources and mentorship to solve real-world AI and HPC challenges.",
            "What does NextGen stand for?": "\"NextGen\" means \"Next Generation,\" symbolizing the club's mission to prepare future-ready innovators in AI and supercomputing.",
            "What's the mission and main goal of the club?": "To empower students through hands-on learning, mentorship, and real-world AI/HPC projects bridging academia and industry, creating production-ready machine learning engineers capable of designing, deploying, and scaling AI systems on supercomputing platforms.",
            "Who leads the club and who are the mentors?": "Led by a student core team, including President Shreya Jain, and guided by mentors such as Dr. Rekha Kashyap, Dr. Gaurav Srivastava, Dr. Richa Singh, and Dr. Bikki Kumar.",
            "What kind of club is NextGen?": "A technical and research-oriented club blending academic learning with industry-grade hands-on experiences in AI, HPC, and quantum computing.",
            "What are the main focus areas and technologies?": "HPC, AI, quantum computing, GPU acceleration, cloud HPC, CUDA, MPI, PyTorch, TensorFlow, OpenMPI, and quantum simulation tools.",
            "What kind of projects does the club work on?": "AI model optimization, quantum simulations, distributed training, molecular modeling, and data-driven innovation.",
            "Who can join the club?": "Any student passionate about AI, HPC, or computing technologies, regardless of department or experience level.",
            "Who are the mentors of the NextGen Supercomputing Club?": "Dr. Gaurav Srivastava, Dr. Richa Singh, and Dr. Bikki Kumar, under the leadership of Dr. Rekha Kashyap, Head of CSE (AI & ML).",
            "Who is the main faculty in charge of the club?": "Dr. Rekha Kashyap serves as the chief faculty advisor providing overall guidance.",
            "What is Dr. Rekha Kashyap's role?": "She guides mentors and the core team to align club projects with department vision and academic goals.",
            "What do the mentors do?": "Mentors assist students with technical learning, workshops, and research projects in AI, HPC, and quantum computing.",
            "Can students interact with mentors directly?": "Yes, mentors regularly interact with students during events, hackathons, and technical sessions.",
            "Who supports technical leads during projects?": "Mentors and technical leads jointly provide guidance for smooth project execution.",
            "How do mentors support research?": "They help direct research topics, assist with resource utilization like the NVIDIA DGX A100, and support prototype development.",
            "Are mentors from the AI/ML department?": "Yes, all mentors are from the CSE (AI & ML) department at KIET.",
            "Who ensures academic alignment?": "Dr. Rekha Kashyap ensures club initiatives align with the department mission.",
            "How often do mentors interact with the team?": "Mentors hold frequent technical check-ins, workshops, and guide hackathon participation.",
            "What mentorship support is provided?": "Academic, technical, and career-focused mentorship for building practical ML and supercomputing skills.",
            "Are mentors involved in the NextGen AI Summit?": "Yes, mentors coordinate event planning and conduct technical reviews.",
            "Do mentors help with industry insights?": "Absolutely, bridging academic learning with current HPC and AI industry trends.",
            "Do mentors approve project ideas?": "Yes, mentors assess feasibility before granting access to club resources.",
            "How important is mentorship?": "Mentorship is the backbone of the club ensuring quality learning and use of advanced computing resources.",
            "Who is Dr. Gaurav Srivastav?": "An AI researcher and educator with expertise in Generative AI, BERT models, and data-driven education, serving as Assistant Professor at KIET.",
            "Who is Dr. Richa Singh?": "Assistant Professor (Research) specializing in AI/ML and Data Science with awards for research excellence.",
            "Who is Dr. Bikki Kumar?": "An AI and Data Science professional expert in Large Language Models and Retrieval-Augmented Generation, applying AI to business optimization.",
            "Who is the Executive Director?": "Dr. Manoj Goel provides visionary leadership to the institution.",
            "Who heads the institution?": "Dr. Manoj Goel is the top authority and represents the college in academic events.",
            "Who is the Director Academics?": "Dr. Adesh Kumar Pandey manages academic affairs and ensures quality education standards.",
            "Which department focuses on AI and ML?": "The Department of Artificial Intelligence and Machine Learning (AI/ML).",
            "Who is the Head of AI/ML Department?": "Dr. Rekha Kashyap, Dean of CSE (AI) and CSE (AI & ML).",
            "What is her role?": "Managing faculty, curriculum development, and innovation-driven research.",
            "Who to contact for academic queries?": "Dr. Rekha Kashyap.",
            "What is supercomputing?": "Extremely powerful computing used for complex problems like AI training, scientific modeling, and big data analysis.",
            "How is supercomputing different from regular computing?": "Supercomputers use many CPUs and GPUs working in parallel to handle large complex tasks.",
            "What is High-Performance Computing (HPC)?": "HPC uses multiple powerful computers connected to solve large computational problems.",
            "What are FLOPS?": "Floating-point operations per second, a metric for computation speed.",
            "What is exascale computing?": "Computing at or above (10^{18}) operations per second.",
            "Examples of supercomputer uses?": "Protein folding, climate modeling, astrophysics, AI training, robotics.",
            "How do GPUs help supercomputing?": "GPUs perform many parallel calculations, ideal for AI and HPC workloads.",
            "What is cluster computing?": "Connecting multiple computers for cooperative computing tasks.",
            "What is NVIDIA DGX A100?": "An AI supercomputer with 8 A100 GPUs, 640GB GPU memory, up to 5 petaFLOPS performance.",
            "Why is DGX A100 important?": "It provides advanced hardware enabling real-world AI and research projects.",
            "What work is done on DGX A100?": "Deep learning training, simulations, data analytics, and AI development.",
            "Can all members use DGX A100?": "Yes, with guided access during projects and events.",
            "What events does the club organize?": "Workshops, bootcamps, hackathons, research projects, and the annual NextGen AI Summit.",
            "What topics do workshops cover?": "Python HPC, Deep Learning, Quantum Computing, GPU programming, and cloud deployment.",
            "Does the club hold hackathons?": "Yes, encouraging AI, HPC, and data innovation.",
            "Are external collaborations included?": "Yes, with startups, universities, and NVIDIA academic programs.",
            "Does the club support open-source contributions?": "Yes, open-source collaboration is a key club focus.",
            "Who can join?": "Anyone passionate about technology, regardless of department or experience.",
            "Are beginners supported?": "Yes, through introductory workshops and mentorship.",
            "Is the club open to non-CS students?": "Yes, all branches are welcome.",
            "How is the club organized?": "Leadership team includes President, Vice President, Heads of PR, Graphics, Events, Technical Leads, Treasurer, plus mentors and HOD.",
            "Who are the current core members?": "President: Shreya Jain; VP: Samarth Shukla; PR Head: Ujjawal Tyagi; Graphics Head: Preeti Singh; Event Leads: Srashti Gupta & Vidisha Goel; Technical Leads: Ronak Goel & Vinayak Rastogi; Treasurer: Divyansh Verma.",
            "What research projects are available?": "AI optimization, quantum simulations, distributed training, molecular modeling, data-driven research.",
            "Can students start their own projects?": "Yes, with mentor and technical lead support.",
            "Are members encouraged to publish research?": "Yes, with mentor guidance.",
            "Are beginners included in research?": "Yes, beginners often pair with experienced members.",
            "What role does open-source play?": "Promotes collaboration and community contributions.",
            "Is there a fee to join?": "Membership is free; some advanced events may charge participation fees.",
            "How to get help with technical issues?": "Contact technical leads or attend troubleshooting sessions.",
            "Are certificates provided?": "Yes, for participation and achievements.",
            "Does the club help with internships?": "Yes, through projects and mentor connections.",
            "Are women encouraged to join?": "Yes, the club is inclusive for all interested in AI and HPC.",
            "Is teamwork involved?": "Yes, most projects and hackathons are team-based.",
            "Does the club support online learning?": "Yes, via hybrid workshops and webinars.",
            "How can members showcase their work?": "Presentations at meetings, summits, and publications with mentor approval.",
            "What is the fastest supercomputer?": "The Frontier Supercomputer in the USA, achieving about 1.1 exaFLOPS.",
            "What is mixed precision training?": "Using lower precision numbers like FP16 to speed up calculations with minimal accuracy loss.",
            "Difference between data and model parallelism?": "Data parallelism splits data across devices; model parallelism splits the model itself.",
            "What is GPU virtualization?": "Partitioning one physical GPU into multiple virtual GPUs for shared use.",
            "How can HPC help emerging tech like the metaverse?": "By providing computational power for rendering, physics simulations, and AI-driven interactions.",
            "Can quantum computers replace classical ones?": "Not yet; they complement classical computers by solving specific problems.",
            "How does AI relate to quantum physics?": "AI aids quantum research in optimization and pattern recognition, while quantum computing may advance AI.",
            "What industries rely on HPC?": "Pharmaceuticals, aerospace, finance, weather forecasting, energy, and more.",
            "How much power do supercomputers consume?": "From hundreds to thousands of kilowatts depending on scale.",
            "Why is Linux important in HPC?": "Linux provides a stable, customizable OS widely used in HPC clusters.",
            "What is an HPC workload manager?": "Software like Slurm or PBS scheduling and managing compute jobs efficiently."
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
