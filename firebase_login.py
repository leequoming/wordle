import requests
import json
import pygame
import sys
import os
import random

API_KEY = "AIzaSyBjcj-iiO1paIflfnv7fNd7wLYppCsFb3I" 
DB_URL = "https://wordle-project1-hcmus-default-rtdb.asia-southeast1.firebasedatabase.app" 

class FirebaseManager:
    def __init__(self):
        self.token = None
        self.user_id = None
        self.email = None

    def login(self, email, password):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        try:
            r = requests.post(url, json=payload)
            data = r.json()
            if "error" in data:
                print("Login Error:", data['error']['message'])
                return False
            self.token = data['idToken']
            self.user_id = data['localId']
            self.email = email
            print("Logged in successfully!")
            return True
        except Exception as e:
            print(f"Network Error: {e}")
            return False

    def signup(self, email, password):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        try:
            r = requests.post(url, json=payload)
            data = r.json()
            if "error" in data:
                print("Signup Error:", data['error']['message'])
                return False
            self.token = data['idToken']
            self.user_id = data['localId']
            self.email = email
            print("Account created!")
            return True
        except Exception as e:
            print(f"Network Error: {e}")
            return False

    def save_game(self, word, success, guesses_count, mode):
        if not self.user_id: return
        
        # Structure: users/USER_ID/history
        url = f"{DB_URL}/users/{self.user_id}/history.json?auth={self.token}"
        data = {
            "word": word,
            "won": success,
            "guesses": guesses_count,
            "mode": mode # e.g. "5-letter"
        }
        requests.post(url, json=data)
        print("Game saved to cloud.")

    def get_stats(self):
        if not self.user_id: return "Not Logged In"
        url = f"{DB_URL}/users/{self.user_id}/history.json?auth={self.token}"
        r = requests.get(url)
        data = r.json()
        if not data: return "No games played yet."
        
        wins = 0
        total = 0
        for key, game in data.items():
            total += 1
            if game['won']: wins += 1
        return f"Games: {total} | Wins: {wins} | Win Rate: {int((wins/total)*100)}%"