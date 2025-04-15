import threading
import time
import random
import json
import traceback
import blockcoin as bc
from datetime import datetime

class BlockCoinFarm:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = None
        self.created_posts = []
        self.posts_lock = threading.Lock()
        self.start_time = None
        self.stop_event = threading.Event()
        self.initial_balance = 0
        self.target_balance = 0
        self.like_method = 1
        
    def login(self):
        try:
            self.session = bc.login(self.username, self.password)
            self.initial_balance = self.session.user.balance
            print(f"Logged in as: {self.session.user.display_name} | Balance: {self.initial_balance}")
            return True
        except Exception as e:
            print("Login Failed:")
            traceback.print_exc()
            return False
    
    def like_post(self, post):
        try:
            if self.like_method == 1:
                data = {"post": post.id}
                response = self.session.session.post(
                    "https://blockcoin.vercel.app/post/like",
                    headers={
                        "Content-Type": "application/json",
                    },
                    json=data
                )
                return response.status_code == 200
            else:
                return post.like()
        except Exception as e:
            print(f"Error liking post {post.id if hasattr(post, 'id') else 'unknown'}: {e}")
            return False

    def worker(self, thread_id, post_texts, prices):
        while not self.stop_event.is_set():
            try:
                current_balance = self.session.user.balance
                if current_balance >= self.target_balance:
                    self.stop_event.set()
                    break

                post_text = random.choice(post_texts)
                price = random.choice(prices)
                
                try:
                    post = self.session.create_post(post_text, price=price)
                    
                    if not hasattr(post, 'id'):
                        raise ValueError("Invalid post response")
                        
                except Exception as e:
                    if "No `const data = [`" in str(e):
                        print(e)
                        print(f"[Thread {thread_id}] Retrying after data parse error...")
                        time.sleep(2)
                        continue
                    raise

                if self.like_post(post):
                    if len(self.created_posts) < 50:
                        print(f"[Thread {thread_id}] Created post: '{post_text[:20]}...' (Price: {price})")

                with self.posts_lock:
                    self.created_posts.append({
                        'id': post.id,
                        'text': post_text,
                        'price': price,
                        'thread': thread_id
                    })
                
                time.sleep(random.uniform(0.5, 2))
                
            except Exception as e:
                error_msg = str(e)
                if "No `const data = [`" in error_msg:
                    sleep_time = random.uniform(1, 3)
                else:
                    sleep_time = 5
                    
                print(f"[Thread {thread_id}] Error: {error_msg[:100]}...")
                time.sleep(sleep_time)
            
    def get_blockcoins(self, post_texts, prices, thread_count=1, amount_of_blockcoins=None, like=1):
        if not self.session:
            if not self.login():
                return None
                
        self.like_method = like
        self.start_time = datetime.now()
        self.created_posts = []
        self.stop_event.clear()
        
        # Set target balance
        if amount_of_blockcoins is not None:
            self.target_balance = self.initial_balance + amount_of_blockcoins
            print(f"Target balance set to: {self.target_balance} (Current: {self.initial_balance})")
        else:
            self.target_balance = float('inf')
        
        threads = []
        for i in range(thread_count):
            t = threading.Thread(target=self.worker, args=(i+1, post_texts, prices))
            t.daemon = True
            t.start()
            threads.append(t)

        print(f"Started {thread_count} threads (Like Method: {like}). Press Ctrl+C to stop...")
        
        try:
            while not self.stop_event.is_set():
                time.sleep(1)
                
                if amount_of_blockcoins is not None:
                    current_balance = self.session.user.balance
                    if current_balance >= self.target_balance:
                        self.stop_event.set()
                        print(f"\nTarget balance reached! {current_balance}/{self.target_balance}")
                        break
                        
        except KeyboardInterrupt:
            print("\nStopping threads...")
            self.stop_event.set()
        
        for t in threads:
            t.join()
            
        current_balance = self.session.user.balance
        coins_earned = current_balance - self.initial_balance
        
        return {
            'initial_balance': self.initial_balance,
            'final_balance': current_balance,
            'coins_earned': coins_earned,
            'target_reached': current_balance >= self.target_balance,
            'time_took': str(datetime.now() - self.start_time),
            'posts_created': len(self.created_posts),
            'average_price': sum(p['price'] for p in self.created_posts) / len(self.created_posts) if self.created_posts else 0,
            'coins_per_minute': coins_earned / (datetime.now() - self.start_time).total_seconds() * 60,
            'like_method_used': self.like_method,
            'details': self.created_posts
        }

def login(username, password):
    return BlockCoinFarm(username, password)
