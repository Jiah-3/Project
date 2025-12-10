# name, max_hp, damage, attack, defense, speed, dodge, crit_chance, image, description, tier

common = [
    ['Wooden_sword', 0, 0, 5, 0, 0, 0, 0, 'wooden_sword.png', '5% increase in attack', 6],
    ['Leather_helmet', 3, 0, 0, 0, 0, 0, 2, 'leather_helmet.png', '3 increase in health, 2% increase in crit chance', 6],
    ['Leather_chestplate', 3, 0, 0, 1, 0, 0, 0, 'leather_chestplate.png', '3 increase in health, 1% increase in defense', 6],
    ['Leather_leggings', 3, 0, 0, 0, 3, 0, 0, 'leather_leggings.png', '3 increase in health, 3% increase in speed', 6],
    ['Leather_boots', 3, 0, 0, 0, 0, 0.5, 0, 'leather_boots.png', '3 increase in health, 0.5% increase in dodge', 6],
]
unique = [
    ['Stone_sword', 0, 0, 10, 0, 0, 0, 0, 'stone_sword.png', '10% increase in attack', 5],
    ['Chainmail_helmet', 5, 0, 0, 0, 0, 0, 3, 'chainmail_helmet.png', '5 increase in health, 3% increase in crit chance', 5],
    ['Chainmail_chestplate', 5, 0, 0, 2, 0, 0, 0, 'chainmail_chestplate.png', '5 increase in health, 2% increase in defense', 5],
    ['Chainmail_leggings', 5, 0, 0, 0, 5, 0, 0, 'chainmail_leggings.png', '5 increase in health, speed', 5],
    ['Chainmail_boots', 5, 0, 0, 0, 0, 1, 0, 'chainmail_boots.png', '5 increase in health, 1% increase in dodge', 5],
    ['Punch_gloves', 0, 2, 0, -10, 10, 0, 0, 'punch_gloves.png', '2 increase in damage, 10% increase in speed, 10% decrease in defense', 5],
    ['Xp_potion', 0, 0, 0, 0, 0, 0, 0, 'xp_bonus_1.png', '25% increase in gain xp', 2],
]
rare = [
    ['Iron_sword', 0, 0, 15, 0, 0, 0, 0, 'iron_sword.png', '15% increase in attack', 4],
    ['Iron_helmet', 8, 0, 0, 0, 0, 0, 5, 'iron_helmet.png', '8 increase in health, 5% increase in crit chance', 4],
    ['Iron_chestplate', 8, 0, 0, 3, 0, 0, 0, 'iron_chestplate.png', '8 increase in health, 3% increase in defense', 4],
    ['Iron_leggings', 8, 0, 0, 0, 8, 0, 0, 'iron_leggings.png', '8 increase in health, speed', 4],
    ['Iron_boots', 8, 0, 0, 0, 0, 1.5, 0, 'iron_boots.png', '8 increase in health, 1.5% increase in dodge', 4],
    ['Fish_sword', 0, 0, 10, 5, 0, 0, 0, 'fish_sword.png', '10% increase in attack, 5% increase in defense', 4],
    ['Gold_ingot', 0, 0, 0, 0, 0, 0, 0, 'gold_ingot.png', '20% increase in gold bonus', 4],
    ['Super_xp_potion', 0, 0, 0, 0, 0, 0, 0, 'xp_bonus_2.png', '50% increase in gain xp', 4],
    ['Champion_crown', 0, 0, 0, 0, 0, 0, 0, 'champion_crown.png', '0.1% increase in attack per hp', 4],
]
legendary = [
    ['Diamond_sword', 0, 0, 20, 0, 0, 0, 0, 'diamond_sword.png', '20% increase in attack', 3],
    ['Diamond_helmet', 10, 0, 0, 0, 0, 0, 8, 'diamond_helmet.png', '10 increase in health, 8% increase in crit chance', 3],
    ['Diamond_chestplate', 10, 0, 0, 5, 0, 0, 0, 'diamond_chestplate.png', '10 increase in health, 5% increase in defense', 3],
    ['Diamond_leggings', 10, 0, 0, 0, 10, 0, 0, 'diamond_leggings.png', '10 increase in health, speed', 3],
    ['Diamond_boots', 10, 0, 0, 0, 0, 3, 0, 'diamond_boots.png', '10 increase in health, 3% increase in dodge', 3],
    ['Bronze_neko', 0, 0, 0, 0, 0, 0, 0, 'bronze_neko.png', '0.001 increase in health, attack, defense per gold', 3],
    ['Gun', 0, 0, 0, 0, 0, 0, 20, 'gun.png', '20% increase in crit chance', 3],
    ['Red_banner', 0, 0, 0, 0, 0, 0, 0, 'red_banner.png', '4% increase in attack per monster', 3],
    ['Yellow_banner', 0, 0, 0, 0, 0, 0, 0, 'yellow_banner.png', '2% increase in crit chance per monster', 3],
    ['Blue_banner', 0, 0, 0, 0, 0, 0, 0, 'blue_banner.png', '1% increase in defense per monster', 3],
    ['Green_banner', 0, 0, 0, 0, 0, 0, 0, 'green_banner.png', '3 increase in health per monster', 3],
    ['Hyper_xp_potion', 0, 0, 0, 0, 0, 0, 0, 'xp_bonus_3.png', '75% increase in gain xp', 3],
    ['Red_ring_1', 0, 0, 0, 0, 0, 0, 0, 'red_ring_1.png', '10% increase in life steal', 3],
]
fabled = [
    ['Netherite_sword', 0, 0, 30, 0, 0, 0, 0, 'netherite_sword.png', '30% increase in attack', 2],
    ['Netherite_helmet', 15, 0, 0, 0, 0, 0, 10, 'netherite_helmet.png', '15 increase in health, 10% increase in crit chance', 2],
    ['Netherite_chestplate', 15, 0, 0, 8, 0, 0, 0, 'netherite_chestplate.png', '15 increase in health, 8% increase in defense', 2],
    ['Netherite_leggings', 15, 0, 0, 0, 15, 0, 0, 'netherite_leggings.png', '15 increase in health, speed', 2],
    ['Netherite_boots', 15, 0, 0, 0, 0, 5, 0, 'netherite_boots.png', '15 increase in health, 5% increase in dodge', 2],
    ['Silver_neko', 0, 0, 0, 0, 0, 0, 0, 'silver_neko.png', '0.005 increase in health, attack, defense per gold', 2],
    ['Speed_boots', 0, 0, 0, 0, 50, 0, 0, 'speed_boots.png', '50% increase in speed, 0.1% increase in attack per speed', 2],
    ['Ultra_xp_potion', 0, 0, 0, 0, 0, 0, 0, 'xp_bonus_4.png', '100% increase in gain xp', 2],
    ['Red_ring_2', 0, 0, 0, 0, 0, 0, 0, 'red_ring_2.png', '20% increase in life steal', 2],
]
mythic = [
    ['Gold_neko', 0, 0, 0, 0, 0, 0, 0, 'gold_neko.png', '0.01 increase in health, attack, defense per gold', 1],
    ['Crown', 10, 0, 10, 10, 10, 10, 10, 'crown.png', '10 increase in health, 10% increase in attack, defense, speed, dodge, crit chance', 1],
    ['Heavy_hammer', 0, 5, 50, 0, -30, 0, 0, 'heavy_hammer.png', '5 increase in damage, 50% increase in attack, 30% decrease in speed', 1],
    ['Magic_sword', 0, 0, 50, 0, 50, 0, 50, 'magic_sword.png', '50% increase in attack, 50% increase in speed, 50% increase in crit chance', 1],
    ['Red_ring_3', 0, 0, 0, 0, 0, 0, 0, 'red_ring_3.png', '30% increase in life steal', 1],
]