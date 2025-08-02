import random
import time

class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.hp = 100
        self.max_hp = 100
        self.attack = 15
        self.defense = 5
        self.gold = 50
        self.exp = 0
        self.exp_to_next = 100
        self.inventory = ["Health Potion", "Health Potion"]
    
    def level_up(self):
        self.level += 1
        self.max_hp += 20
        self.hp = self.max_hp
        self.attack += 5
        self.defense += 3
        self.exp = 0
        self.exp_to_next = self.level * 100
        print(f"\n🎉 Level up! You are now level {self.level}!")
        print(f"HP: {self.max_hp}, Attack: {self.attack}, Defense: {self.defense}")
    
    def gain_exp(self, amount):
        self.exp += amount
        print(f"Gained {amount} EXP!")
        if self.exp >= self.exp_to_next:
            self.level_up()
    
    def use_potion(self):
        if "Health Potion" in self.inventory:
            heal_amount = 50
            self.hp = min(self.max_hp, self.hp + heal_amount)
            self.inventory.remove("Health Potion")
            print(f"Used Health Potion! Restored {heal_amount} HP. Current HP: {self.hp}")
            return True
        else:
            print("No Health Potions in inventory!")
            return False
    
    def show_stats(self):
        print(f"\n--- {self.name}'s Stats ---")
        print(f"Level: {self.level}")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")
        print(f"Gold: {self.gold}")
        print(f"EXP: {self.exp}/{self.exp_to_next}")
        print(f"Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}")

class Enemy:
    def __init__(self, name, hp, attack, defense, gold_reward, exp_reward):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.gold_reward = gold_reward
        self.exp_reward = exp_reward

def create_enemy(player_level):
    enemies = [
        Enemy("Goblin", 30 + player_level * 10, 8 + player_level * 2, 2, 10 + player_level * 5, 25 + player_level * 5),
        Enemy("Orc", 50 + player_level * 15, 12 + player_level * 3, 4, 15 + player_level * 7, 35 + player_level * 7),
        Enemy("Skeleton", 40 + player_level * 12, 10 + player_level * 2, 3, 12 + player_level * 6, 30 + player_level * 6),
        Enemy("Troll", 80 + player_level * 20, 15 + player_level * 4, 6, 25 + player_level * 10, 50 + player_level * 10)
    ]
    return random.choice(enemies)

def combat(player, enemy):
    print(f"\n⚔️  A wild {enemy.name} appears!")
    print(f"{enemy.name} - HP: {enemy.hp}, Attack: {enemy.attack}")
    
    while player.hp > 0 and enemy.hp > 0:
        print(f"\n--- Combat Turn ---")
        print(f"Your HP: {player.hp}/{player.max_hp}")
        print(f"{enemy.name} HP: {enemy.hp}/{enemy.max_hp}")
        
        action = input("\nChoose action: (a)ttack, (u)se potion, (r)un: ").lower()
        
        if action == 'a':
            # Player attacks
            damage = max(1, player.attack - enemy.defense + random.randint(-3, 3))
            enemy.hp -= damage
            print(f"You deal {damage} damage to {enemy.name}!")
            
            if enemy.hp <= 0:
                print(f"\n🎉 You defeated the {enemy.name}!")
                player.gold += enemy.gold_reward
                player.gain_exp(enemy.exp_reward)
                print(f"Gained {enemy.gold_reward} gold!")
                
                # Chance for item drop
                if random.random() < 0.3:
                    player.inventory.append("Health Potion")
                    print("Found a Health Potion!")
                return True
            
            # Enemy attacks
            damage = max(1, enemy.attack - player.defense + random.randint(-2, 2))
            player.hp -= damage
            print(f"{enemy.name} deals {damage} damage to you!")
            
        elif action == 'u':
            if not player.use_potion():
                continue
        elif action == 'r':
            if random.random() < 0.5:
                print("Successfully ran away!")
                return False
            else:
                print("Couldn't escape!")
        else:
            print("Invalid action!")
            continue
        
        time.sleep(1)
    
    if player.hp <= 0:
        print("\n💀 Game Over! You were defeated!")
        return False
    
    return True

def shop(player):
    print("\n🏪 Welcome to the Shop!")
    print("1. Health Potion - 20 gold")
    print("2. Attack Boost (permanent) - 100 gold")
    print("3. Defense Boost (permanent) - 80 gold")
    print("4. Leave shop")
    
    choice = input("What would you like to buy? (1-4): ")
    
    if choice == '1':
        if player.gold >= 20:
            player.gold -= 20
            player.inventory.append("Health Potion")
            print("Purchased Health Potion!")
        else:
            print("Not enough gold!")
    elif choice == '2':
        if player.gold >= 100:
            player.gold -= 100
            player.attack += 3
            print("Attack increased by 3!")
        else:
            print("Not enough gold!")
    elif choice == '3':
        if player.gold >= 80:
            player.gold -= 80
            player.defense += 2
            print("Defense increased by 2!")
        else:
            print("Not enough gold!")
    elif choice == '4':
        print("Thanks for visiting!")
    else:
        print("Invalid choice!")

def main_game():
    print("🗡️  Welcome to the Simple RPG Adventure! 🗡️")
    name = input("Enter your character's name: ")
    player = Player(name)
    
    print(f"\nWelcome, {player.name}! Your adventure begins now...")
    player.show_stats()
    
    while player.hp > 0:
        print("\n" + "="*50)
        print("What would you like to do?")
        print("1. Explore and fight monsters")
        print("2. Visit shop")
        print("3. Rest (restore HP)")
        print("4. View stats")
        print("5. Quit game")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            enemy = create_enemy(player.level)
            combat_result = combat(player, enemy)
            if not combat_result and player.hp <= 0:
                break
                
        elif choice == '2':
            shop(player)
            
        elif choice == '3':
            if player.gold >= 10:
                player.gold -= 10
                player.hp = player.max_hp
                print("You rest at an inn and restore full HP! (-10 gold)")
            else:
                player.hp = min(player.max_hp, player.hp + 20)
                print("You rest in the wilderness and restore some HP.")
                
        elif choice == '4':
            player.show_stats()
            
        elif choice == '5':
            print(f"Thanks for playing! Final level: {player.level}")
            break
            
        else:
            print("Invalid choice! Please try again.")
    
    if player.hp <= 0:
        print(f"\n🪦 Game Over! {player.name} reached level {player.level}")
        print("Better luck next time!")

if __name__ == "__main__":
    main_game()