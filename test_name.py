#!/usr/bin/env python3
"""Test script to verify Chetak responds with name"""
from ai.chat import ask_chatgpt

questions = [
    "what is your name",
    "aapka naam kya hai",
    "tumhara naam kya hai",
    "who are you",
    "tum kaun ho"
]

print("Testing Chetak name responses...\n")
for q in questions:
    print(f"Q: {q}")
    response = ask_chatgpt(q)
    print(f"A: {response}\n")
    print("-" * 60)
