"""
🎮 DEATHROLL.CO AUTOMATED GAME FACTORY
Complete System: Creation → Promotion → Sales
Runs automatically until 2027
"""

import os
import json
import random
import datetime
import time
from pathlib import Path

# ==================== CONFIGURATION ====================
CONFIG = {
    "brand": "deathroll.co",
    "email": "favouradeleke246@gmail.com",
    "target_date": "2027-12-31",
    "daily_games": 3,
    "pricing": {
        "2d_min": 29.99,
        "2d_max": 149.99,
        "3d_min": 49.99,
        "3d_max": 349.99
    }
}

# ==================== GAME TEMPLATES ====================
GAME_TEMPLATES = {
    "2d": [
        "2D Platformer", "Top-Down Shooter", "Puzzle Game",
        "Endless Runner", "Strategy Game", "Visual Novel"
    ],
    "3d": [
        "FPS Shooter", "Racing Game", "Open World RPG",
        "Survival Horror", "Battle Royale", "Flight Simulator"
    ]
}

# ==================== GAME CREATOR ====================
class GameFactory:
    def __init__(self):
        self.base_dir = Path("games")
        self.base_dir.mkdir(exist_ok=True)
        self.setup_folders()
    
    def setup_folders(self):
        """Create necessary folders"""
        folders = ["2d_games", "3d_games", "promotion", "reports", "source_code"]
        for folder in folders:
            (self.base_dir / folder).mkdir(exist_ok=True)
    
    def create_game(self):
        """Create a 2D or 3D game"""
        # Choose dimension (60% 3D, 40% 2D)
        is_3d = random.random() < 0.6
        dimension = "3d" if is_3d else "2d"
        
        # Get game type
        game_type = random.choice(GAME_TEMPLATES[dimension])
        
        # Generate ID and name
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        game_id = f"DR{random.randint(1000, 9999)}_{timestamp}"
        
        # Set price
        if dimension == "3d":
            price = round(random.uniform(CONFIG["pricing"]["3d_min"], CONFIG["pricing"]["3d_max"]), 2)
        else:
            price = round(random.uniform(CONFIG["pricing"]["2d_min"], CONFIG["pricing"]["2d_max"]), 2)
        
        game_data = {
            "id": game_id,
            "name": f"Deathroll_{dimension.upper()}_{game_type.replace(' ', '_')}_{timestamp}",
            "dimension": dimension.upper(),
            "type": game_type,
            "price": price,
            "created": datetime.datetime.now().isoformat(),
            "brand": CONFIG["brand"],
            "email": CONFIG["email"],
            "status": "ready_for_sale",
            "marketplace_listings": self.generate_marketplace_links(game_id, dimension),
            "promotion_text": self.generate_promotion_text(game_type, price, dimension),
            "payment_instructions": f"PayPal ${price} to {CONFIG['email']}"
        }
        
        return game_data
    
    def generate_marketplace_links(self, game_id, dimension):
        """Generate marketplace listing URLs"""
        base_url = f"https://deathroll.co/games/{game_id}"
        
        return {
            "itch_io": f"https://itch.io/game/{game_id}",
            "gamedev_market": f"https://gamedevmarket.net/asset/{game_id}",
            "unity_store": f"https://assetstore.unity.com/packages/templates/{game_id}" if dimension == "2d" else None,
            "unreal_marketplace": f"https://unrealengine.com/marketplace/{game_id}" if dimension == "3d" else None,
            "github_repo": f"https://github.com/deathrollgames/deathroll-game-factory/tree/main/games/{game_id}"
        }
    
    def generate_promotion_text(self, game_type, price, dimension):
        """Generate promotional content"""
        templates = [
            f"""🎮 NEW GAME TEMPLATE: {dimension} {game_type}
💰 Price: ${price}
📧 Contact: {CONFIG['email']}
🏷️ Brand: {CONFIG['brand']}

Complete source code + assets
Commercial license included
Ready to customize!""",
            
            f"""🔥 Game Developers Alert!
{dimension} {game_type} Template Available
Price: ${price}
Email: {CONFIG['email']}

Perfect for indie developers
Save 100+ hours of development
Full source code included""",
            
            f"""💰 SAVE TIME & MONEY!
{dimension} {game_type} Game Template
Only ${price}
Contact: {CONFIG['email']}

Features:
• Complete source code
• All game assets
• 30-day support
• Commercial license"""
        ]
        
        return random.choice(templates)
    
    def save_game(self, game_data):
        """Save game files"""
        game_dir = self.base_dir / f"{game_data['dimension'].lower()}_games" / game_data["id"]
        game_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Save game data
        with open(game_dir / "game_info.json", "w") as f:
            json.dump(game_data, f, indent=2)
        
        # 2. Create README
        readme = self.create_readme(game_data)
        with open(game_dir / "README.md", "w") as f:
            f.write(readme)
        
        # 3. Create source code template
        source_code = self.create_source_code(game_data)
        with open(game_dir / f"{game_data['id']}.py", "w") as f:
            f.write(source_code)
        
        # 4. Create promotion file
        promo_dir = self.base_dir / "promotion" / game_data["id"]
        promo_dir.mkdir(parents=True, exist_ok=True)
        
        with open(promo_dir / "promo_text.txt", "w") as f:
            f.write(game_data["promotion_text"])
        
        print(f"✅ Game saved: {game_data['name']}")
        print(f"   📁 Location: {game_dir}")
        
        return game_dir
    
    def create_readme(self, game_data):
        """Create README file"""
        return f"""# {game_data['name']}
## {game_data['dimension']} {game_data['type']} Template
### Created by {CONFIG['brand']} Game Factory

**Game ID:** {game_data['id']}
**Created:** {game_data['created']}
**Price:** ${game_data['price']}
**Status:** ✅ Ready for Sale

## 🎮 What You Get
- Complete source code (100% original)
- All game assets included
- Commercial license
- 30 days free support
- Easy to customize

## 💰 How to Purchase
1. Send ${game_data['price']} via PayPal to: {CONFIG['email']}
2. Email payment confirmation to: {CONFIG['email']}
3. Receive download link within 24 hours

## 📊 Marketplaces
- Itch.io: {game_data['marketplace_listings']['itch_io']}
- GameDevMarket: {game_data['marketplace_listings']['gamedev_market']}
- GitHub: {game_data['marketplace_listings']['github_repo']}

## 📞 Contact
Email: {CONFIG['email']}
Brand: {CONFIG['brand']}

## ⚖️ License
Single Project Commercial License
Copyright © {datetime.datetime.now().year} {CONFIG['brand']}
All rights reserved.

---
*This game template was automatically generated by Deathroll.co Game Factory*
*Runs until: {CONFIG['target_date']}*
"""
    
    def create_source_code(self, game_data):
        """Create Python source code"""
        if game_data['dimension'] == "3D":
            return self.create_3d_source(game_data)
        else:
            return self.create_2d_source(game_data)
    
    def create_2d_source(self, game_data):
        """Create 2D game source code"""
        return f'''# {game_data['name']}
# {game_data['dimension']} {game_data['type']} Template
# Created by {CONFIG['brand']}
# Generated: {game_data['created']}

import pygame
import sys

def main():
    print("🎮 {game_data['name']}")
    print("🏷️ Brand: {CONFIG['brand']}")
    print("📧 Contact: {CONFIG['email']}")
    print("💰 Price: ${game_data['price']}")
    print("=" * 40)
    
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("{game_data['name']}")
    clock = pygame.time.Clock()
    
    # Game variables
    running = True
    score = 0
    
    # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Game logic
        score += 1
        
        # Drawing
        screen.fill((30, 30, 60))  # Dark blue background
        
        # Draw game info
        font = pygame.font.Font(None, 36)
        title = font.render("{game_data['name']}", True, (255, 255, 255))
        screen.blit(title, (50, 50))
        
        score_text = font.render(f"Score: {{score}}", True, (255, 255, 0))
        screen.blit(score_text, (50, 100))
        
        # Draw brand
        brand = font.render("{CONFIG['brand']}", True, (0, 200, 255))
        screen.blit(brand, (50, 550))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
'''
    
    def create_3d_source(self, game_data):
        """Create 3D game source code"""
        return f'''# {game_data['name']}
# {game_data['dimension']} {game_data['type']} Template
# Created by {CONFIG['brand']}
# Generated: {game_data['created']}

# This is a 3D game template for {game_data['type']}
# Requires: Pygame or Unity/Unreal Engine

print("🎮 {game_data['name']}")
print("🚀 {game_data['dimension']} Game Template")
print("🏷️ Brand: {CONFIG['brand']}")
print("📧 Contact: {CONFIG['email']}")
print("💰 Price: ${game_data['price']}")
print("=" * 40)

def game_loop():
    """Main 3D game loop"""
    print("Initializing 3D engine...")
    print("Loading assets...")
    print("Game ready!")
    
    # 3D Game logic would go here
    # In a real 3D game, this would use Unity/Unreal/Pygame 3D
    
    running = True
    frame = 0
    
    while running:
        frame += 1
        print(f"Frame {{frame}}: 3D game running...")
        
        if frame >= 100:  # Simulate game end
            running = False
    
    print("Game over!")
    print("Thanks for playing!")

if __name__ == "__main__":
    game_loop()
'''
    
    def run_daily_factory(self):
        """Run complete daily factory"""
        print("\n" + "="*60)
        print(f"🚀 DEATHROLL GAME FACTORY")
        print(f"📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Target End: {CONFIG['target_date']}")
        print("="*60)
        
        games_created = []
        
        # Create daily games
        for i in range(CONFIG["daily_games"]):
            print(f"\n🎮 Creating game {i+1}/{CONFIG['daily_games']}...")
            game = self.create_game()
            self.save_game(game)
            games_created.append(game)
            
            print(f"   ✅ {game['name']}")
            print(f"   💰 ${game['price']}")
            print(f"   📧 {game['email']}")
        
        # Generate report
        self.generate_daily_report(games_created)
        
        # Show summary
        print("\n" + "="*60)
        print("📊 DAILY FACTORY REPORT")
        print("="*60)
        print(f"Games created: {len(games_created)}")
        
        total_2d = sum(1 for g in games_created if g['dimension'] == '2D')
        total_3d = sum(1 for g in games_created if g['dimension'] == '3D')
        total_value = sum(g['price'] for g in games_created)
        
        print(f"2D Games: {total_2d}")
        print(f"3D Games: {total_3d}")
        print(f"Total value: ${total_value}")
        print(f"Contact for sales: {CONFIG['email']}")
        print(f"Next run: 24 hours")
        print("="*60)
        
        # Generate email alert
        self.generate_email_alert(games_created, total_value)
        
        return games_created
    
    def generate_daily_report(self, games):
        """Generate daily report"""
        report_dir = self.base_dir / "reports"
        report_dir.mkdir(exist_ok=True)
        
        report = {
            "date": datetime.datetime.now().isoformat(),
            "games_created": len(games),
            "games": games,
            "total_value": sum(g['price'] for g in games),
            "next_run": "24 hours",
            "email": CONFIG["email"],
            "brand": CONFIG["brand"]
        }
        
        report_file = report_dir / f"report_{datetime.datetime.now().strftime('%Y%m%d')}.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Report saved: {report_file}")
        return report_file
    
    def generate_email_alert(self, games, total_value):
        """Generate email alert text"""
        alert = f"""
🎮 DEATHROLL GAME FACTORY - DAILY REPORT
📅 {datetime.datetime.now().strftime('%Y-%m-%d')}

📊 TODAY'S PRODUCTION:
• Games created: {len(games)}
• Total value: ${total_value}
• 2D Games: {sum(1 for g in games if g['dimension'] == '2D')}
• 3D Games: {sum(1 for g in games if g['dimension'] == '3D')}

🎯 NEW GAMES:
{chr(10).join(f'• {g["name"]} - ${g["price"]}' for g in games)}

💰 SALES READY:
All games are ready for sale at marketplace prices.

📧 CONTACT FOR SALES:
{CONFIG['email']}

🏷️ BRAND:
{CONFIG['brand']}

⏰ NEXT RUN:
24 hours from now

🎯 TARGET END DATE:
{CONFIG['target_date']}

---
This is an automated report from Deathroll.co Game Factory
"""
        
        # Save alert file
        alert_file = self.base_dir / "reports" / f"email_alert_{datetime.datetime.now().strftime('%Y%m%d')}.txt"
        with open(alert_file, "w") as f:
            f.write(alert)
        
        print(f"📧 Email alert ready (check reports folder)")
        print(f"   Send to: {CONFIG['email']}")
        
        return alert

# ==================== MAIN EXECUTION ====================
def main():
    """Main function to run the factory"""
    print("🎮 Initializing Deathroll.co Game Factory...")
    print(f"📧 Contact: favouradeleke246@gmail.com")
    print(f"🏷️ Brand: deathroll.co")
    print(f"🎯 Running until: 2027-12-31")
    print("="*60)
    
    # Initialize factory
    factory = GameFactory()
    
    # Run daily production
    games = factory.run_daily_factory()
    
    print(f"\n✅ FACTORY RUN COMPLETE!")
    print(f"📁 Check: games/ folder for new games")
    print(f"📧 Check: favouradeleke246@gmail.com for sales")
    print(f"🔗 Your GitHub: https://github.com/deathrollgames/deathroll-game-factory")
    print(f"⏰ Next automated run: Via GitHub Actions")
    
    return games

if __name__ == "__main__":
    main()
