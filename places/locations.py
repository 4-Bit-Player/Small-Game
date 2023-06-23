from things import food, items, potions
from player import user, inventory
from places import location_actions
import combat

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
                "action_text": "Go somewhere else.",
                "action_type": location_actions.change_location,
                "available_locations": {
                    "Stay": "stay",
                    "Go to the Forest": "Forest",
                    "Go to the Shop": "Trinkets and Tincture Trove",
                    "Go to the Potion shop": "Potion shop"
                },
            },
            {
                "action_text": "Go to the shop.",
                "action_type": location_actions.go_to_location,
                "name": "Trinkets and Tincture Trove",
            },
            {
                "action_text": "Check stats.",
                "action_type": user.check_player_stats,
            },
            {
                "action_text": "Open Inventory.",
                "action_type": inventory.open_inventory,
            },
            {
                "action_text": "Retire.",
                "action_type": location_actions.retire_check
                },
        ]

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
              "action_type": location_actions.shop,
              "action_text": "food",
              "item": food.basic_food,
              "name": "Basic Food",
              "price": 20,
          },
          {
              "action_text": "Buy Food (health+20)",
              "action_type": location_actions.shop,
              "player_affected_stats": {
                  "hp": 20
              },

              "price": 20,
              "item_type": "food",
              "item": food.basic_food,
              "name": ["Beagle", "Burger", "Banana", "Hot Pocket",  "Doughnut", "Pizza", "Waffle", "Beef Stew",
                       "Apple", "Cheese-wheel"]
          },
          {
              "action_text": "Upgrade your Sword (atk + 5)",
              "action_type": location_actions.shop,
              "player_affected_stats": {
                  "str": 5
              },
              "price": 50,
              "item": items.sharpening_stone,
              "name": "Sharpening Stone",

          },
          {
              "action_text": "Improve you Shield (def + 1)",
              "action_type": location_actions.shop,
              "player_affected_stats": {
                  "def": 1
              },
              "price": 50,
              "item_type": "stat_upgrade",
              "item": items.polishing_fluid,
              "name": "Polishing Fluid",

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
                "action_type": location_actions.shop,
                "action_text": "Buy a Potion of Strength",
                "item": potions.enhance_strength,
                "name": "Potion of Strength",
                "price": 20,
            },
            {
                "action_type": location_actions.shop,
                "action_text": "Buy a Potion of Toughness",
                "item": potions.enhance_toughness,
                "name": "Potion of Toughness",
                "price": 20,
            },

        ],
    },

    # Forest
    {
     "name": "Forest",
     "type": "Wilderness",
     "enemies": {
         "Wild Boar": 1000,
     },
     "welcome_text": [
         "You have arrived at the forest!",
         "You have a slightly eerie feeling."
     ],
     "weather": [40, 60],
     "true_weather": "sunny",
     "list_of_actions": [
         {
             "action_text": "Go somewhere else.",
             "action_type": location_actions.change_location,
             "available_locations": {
                 "Stay": "stay",
                 "To Castell City": "Castell City",
                 "Go deeper into the Forest": "Dark Forest",
             },
         },

         {
             "action_text": "Look around.",
             "action_type": combat.combat
         },
         {
             "action_text": "Check Stats",
             "action_type": user.check_player_stats
         },
         {
             "action_text": "Open Inventory.",
             "action_type": inventory.open_inventory,
         },
     ]
    },

    # Dark Forest
    {
        "name": "Dark Forest",
        "type": "Wilderness",
        "enemies": {
            "Green Herb": 100,
            "Wild Boar": 300,
            "Big Wild Boar": 1000,

        },
        "welcome_text": [
            "You wandered deeper into the Forest!",
            "The treetops are blocking out most light and it's more difficult to see."
        ],
        "inspect":["As you look around the lush forest a scene of serene beauty unfolds before your eyes.",
                   "The dappled sunlight filters through the verdant canopy, "
                   "casting a soft, ethereal glow on the forest floor.",
                   "The air is thick with the earthy scent of moss, damp soil, and the sweet fragrance of wildflowers.",
                   "Amongst this idyllic setting, your attention is captivated by a magnificent creature-"
                   ],

        "weather": [0, 60],
        "true_weather": "cloudy",
        "list_of_actions": [
            {
                "action_text": "Go back.",
                "action_type": location_actions.location_back,
                "available_locations": {
                    "Stay": "stay",
                    "To Castell City": "Castell City"
                },
            },

            {
                "action_text": "Look around.",
                "action_type": location_actions.inspect
            },
            {
                "action_text": "Search for enemies.",
                "action_type": combat.combat
            },
            {
                "action_text": "Open Inventory.",
                "action_type": inventory.open_inventory,
            },
        ]
    },

]
