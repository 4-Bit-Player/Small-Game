from places import location_actions, shop
from player import crafting, inventory
import combat
import enemies

locations = [

    # Castell City
    {
        "name": "Castell City",
        "type": "City",
        "welcome_text": [
            "You have arrived in Castell City!",
            "Welcome, adventurer!"
        ],
        "weather": [50, 75],
        "true_weather": "sunny",
        "list_of_actions": [
            {
                "action_text": "Look around.",
                "action_type": location_actions.inspect
            },
            {
                "action_text": "Open Inventory",
                "action_type": inventory.open_inventory
            },
        ],
        "inspect_num": 0,
        "inspect": [
            {
                "broad_desc": "Walk through the streets of the city.",
                "text": [
                    "As you walk around the city you spot a small shop that you haven't noticed before.",
                    "They sell bread and equipment...",
                    "Which is an odd combination, but who cares...",
                ],
                "unlocks": "Castell Shop",
                "unlock_location": "Castell City"

            },
            {
                "broad_desc": "Walk around byways.",
                "text": [
                    "As you continue to walk around you stumble upon a potion shop.",
                    "It looks a bit run down, but it seems like someone still runs it.",
                ],
                "unlocks": "Castell Potion Shop",
                "unlock_location": "Castell City"
            },
            {
                "broad_desc": "Walk to the gates.",
                "text": [
                    "You have enough from walking around in the city.",
                    "There are boars outside that are a threat to the people!",
                    "And you have to revenge your friend!",
                ],
                "unlocks": "Go to Forest",
                "unlock_location": "Castell City"

            }
        ],


    },

    # Trinkets and Tincture Trove
    {
      "name": "Trinkets and Tincture Trove",
      "type": "shop",
      "welcome_text": [
          "Welcome to the best shop in Castell City.",
      ],
      "list_of_actions": [
          {
              "action_text": "Leave the shop.",
              "action_type": location_actions.change_location,
              "available_locations": {
                  "To Castell City": "back"
              },
          },
          {
              "action_text": "Open Inventory",
              "action_type": inventory.open_inventory
          },
          {
              "action_text": "Buy Food",
              "action_type": shop.buy,
              "player_affected_stats": {
                  "hp": 20
              },

              "price": 20,
              "item_type": "food",
              "item": "Basic Food",
              "name": ["Beagle", "Burger", "Banana", "Hot Pocket",  "Doughnut", "Pizza", "Waffle", "Beef Stew",
                       "Apple", "Cheese-wheel"]
          },
          {
              "action_text": "Upgrade your Sword",
              "action_type": shop.buy,
              "player_affected_stats": {
                  "str": 5
              },
              "price": 30,
              "item_type": "item",
              "item": "Sharpening Stone",
              "name": "Sharpening Stone",

          },
          {
              "action_text": "Upgrade your Shield",
              "action_type": shop.buy,
              "player_affected_stats": {
                  "def": 1
              },
              "price": 30,
              "item_type": "item",
              "item": "Polishing Fluid",
              "name": "Polishing Fluid",

          },
          {
              "action_text": "Buy a Helmet",
              "action_type": shop.buy,
              "price": 50,
              "item_type": "material",
              "item": "Leather Helmet",
              "name": "Helmet",
          },
          {
              "action_text": "Buy a slightly better Helmet",
              "action_type": shop.buy,
              "price": 100,
              "item_type": "material",
              "item": "Iron Helmet",
              "name": "Helmet",
          },

      ],
    },

    # Potion shop
    {
        "name": "Potion shop",
        "type": "shop",
        "welcome_text": [
            "Welcome to the Potion shop.",
        ],
        "list_of_actions": [
            {
                "action_text": "Leave the shop.",
                "action_type": location_actions.change_location,
                "available_locations": {
                    "To Castell City": "back"
                },
            },
            {
                "action_text": "Open Inventory",
                "action_type": inventory.open_inventory
            },
            {
                "action_text": "Sell items",
                "action_type": shop.shop_sell,
            },
            {
                "action_type": shop.buy,
                "action_text": "Buy a Potion of Strength",
                "item_type": "Potion",
                "item": "Potion of Strength",
                "name": "Potion of Strength",
                "price": 20,
            },
            {
                "action_type": shop.buy,
                "action_text": "Buy a Potion of Toughness",
                "item": "Potion of Toughness",
                "name": "Potion of Toughness",
                "price": 20,
            },

        ],
    },

    # Forest
    {
     "name": "Forest",
     "type": "Wilderness",
     "enemy_chance": 200,
     "enemies": {
         enemies.wild_boar: 1000,
     },

     "item_find_chance": 1000,
     "findable_items": {
         "Red Herb": {2: 100, 1: 300},
         "Green Herb": {2: 150, 1: 400},
         "Stick": {2: 150, 1: 400},
         "Small Rock": {2: 200, 1: 400},
         "Mushroom": {2: 100, 1: 300},
         "Poisonous Mushroom": {2: 100, 1: 300},
         "Berrie": {3: 100, 2: 200, 1: 300},
     },
     "welcome_text": [
         "You have arrived at the forest!",
         "You have a slightly eerie feeling."
     ],
     "weather": [40, 60],
     "true_weather": "sunny",
     "list_of_actions": [
         {
             "action_text": "Go to Castell.",
             "action_type": location_actions.go_to_location,
             "name": "Castell City",
         },
         {
             "action_text": "Open Inventory",
             "action_type": inventory.open_inventory
         },
         {
             "action_text": "Look around.",
             "action_type": location_actions.inspect
         },
         {
             "action_text": "Look for items.",
             "action_type": location_actions.look_around
         },
         {
             "action_text": "Look for enemies.",
             "action_type": combat.combat
         },
     ],
     "inspect_num": 0,
     "inspect": [
         {
             "broad_desc": "Enjoy the astonishing view",
             "text": [
                "As you look around the lush forest a scene of serene beauty unfolds before your eyes.",
                "The dappled sunlight filters through the verdant canopy, ",
                "casting a soft, ethereal glow on the forest floor.",
                "The air is thick with the earthy scent of moss, damp soil, and the sweet fragrance of wildflowers."
                ],
             "unlocks": {},
             "unlock_location": "",
         },
         {
             "broad_desc": "Look for hidden things",
             "text": [
                "You spot a path that leads deeper into the forest.",
                "It the trees seem to be standing closer to each other there..."
                ],
             "unlocks": "Go to Dark Forest",
             "unlock_location": "Forest",
         }
        ],
    },

    # Dark Forest
    {
        "name": "Dark Forest",
        "type": "Wilderness",
        "enemy_chance": 300,
        "enemies": {
            enemies.wild_boar: 300,
            enemies.big_wild_boar: 1000,
        },
        "item_find_chance": 1000,
        "findable_items": {
            "Tough Stick": {2: 100, 1: 300},
            "Sharp Stone": {2: 100, 1: 300},
        },

        "welcome_text": [
            "You wandered deeper into the Forest!",
            "The treetops are blocking out most light and it's more difficult to see."
        ],
        "inspect_num": 0,
        "inspect":[
            {
                "broad_desc": "Placeholder ^^",
                "text": [
                    "It dark",
                ],
                "unlocks": "Go to Bottom of the Mountain",
                "unlock_location": "Dark Forest",
            }

        ],

        "weather": [0, 60],
        "true_weather": "cloudy",
        "list_of_actions": [
            {
                "action_text": "Go back to the Forest.",
                "action_type": location_actions.go_to_location,
                "name": "Forest",
            },
            {
                "action_text": "Open Inventory",
                "action_type": inventory.open_inventory
            },
            {
                "action_text": "Look around.",
                "action_type": location_actions.inspect
            },
            {
                "action_text": "Look for items.",
                "action_type": location_actions.look_around
            },
            {
                "action_text": "Search for enemies.",
                "action_type": combat.combat
            },
        ],
    },

    # Bottom of the Mountain
    {
        "name": "Bottom of the Mountain",
        "type": "City",

        "welcome_text": [
            "You arrived at the Bottom of the huge Mountain!",

        ],
        "inspect_num": 0,
        "inspect": [
            {
                "broad_desc": "Look at the surrounding area",
                "text": [
                    "At the end of the forest you see a grand rocky mountain"
                ],
                "unlocks": {},
                "unlock_location": "",
            },
            {
                "broad_desc": "Check out the camp at the side of the road",
                "text": [
                    "As you walk around the camp you see quiet a few people.",
                    "You notice a blacksmith who is repairing the gear from an adventurer.",
                    "Maybe he can repair your gear as well..."
                ],
                "unlocks": "Go to Blacksmith",
                "unlock_location": "Bottom of the Mountain",
            }
        ],

        "weather": [70, 90],
        "true_weather": "sunny",
        "list_of_actions": [
            {
                "action_text": "Go back to the Dark Forest.",
                "action_type": location_actions.go_to_location,
                "name": "Dark Forest"
            },
            {
                "action_text": "Open Inventory",
                "action_type": inventory.open_inventory
            },
            {
                "action_text": "Look around.",
                "action_type": location_actions.inspect
            },
        ],
    },

    # Blacksmith
    {
        "name": "Blacksmith",
        "type": "forge",
        "welcome_text": [
            f"Greetings, traveler.",
            "Welcome to my small tent.",
            "Can I help you somehow?"
        ],
        "list_of_actions": [
            {
                "action_text": "Leave the shop.",
                "action_type": location_actions.change_location,
                "available_locations": {
                    "Go back": "back"
                },
            },
            {
                "action_text": "Upgrade equipment.",
                "action_type": crafting.upgrading
            },

        ],
    },

]

#            {
#                "action_text": "Go somewhere else.",
#                "action_type": location_actions.change_location,
#                "available_locations": {
#                    "Stay": "stay",
#                    "Go to the Forest": "Forest",
#                    "Go to the Shop": "Trinkets and Tincture Trove",
#                    "Go to the Potion shop": "Potion shop"
#                },
#            },
