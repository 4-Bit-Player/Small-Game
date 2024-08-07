from places.unlock import unlocks
locations = []


def search_location(location_name: str):
    for i in locations:
        if i["name"] == location_name:
            return i


default_locations = [
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
                "action_text": "Look around",
                "action_type": "inspect"
            },
            {
                "action_text": "Open Inventory",
                "action_type": "open_inventory"
            },
            {
                "action_text": "Look at active Quests",
                "action_type": "check_active_quests"
            }
        ],
        "inspect_num": 0,
        "inspect": [
            unlocks["Castell 1"],
            unlocks["Castell 2"],
            unlocks["Castell 3"],
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
              "action_text": "Leave the shop",
              "action_type": "change_location",
              "available_locations": {
                  "To Castell City": "back"
              },
          },
          {
              "action_text": "Open Inventory",
              "action_type": "open_inventory"
          },
          {
              "action_text": "Buy Food",
              "action_type": "buy",
              "player_affected_stats": {
                  "hp": 20
              },

              "price": 20,
              "item_type": "food",
              "item": "Basic Food",
              "name": [
                  "Beagle", "Burger", "Banana", "Hot Pocket", "Doughnut", "Pizza", "Waffle", "Beef Stew", "Apple",
                  "Cheese-Wheel", "Steamed Ham", "Sandwich", "Noodles", "Ramen", "Salad", "Cucumber", "Fried Rice",
                  "Pancake", "Melon", "Rice Cracker", "Bread", "Sushi", "Fruit Salad", "Strawberry", "Pineapple",
                  "Block of Butter", "Salami", "Lettuce", "Chips", "Fries", "Fish", "Onion", "Peanuts", "Sausage",
                  "Garlic", "Hazelnuts", "Tinned Tuna", "Fried Plaice", "Turkey", "Mayonnaise"
              ]
          },
          {
              "action_text": "Upgrade your Sword",
              "action_type": "buy",
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
              "action_type": "buy",
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
              "action_type": "buy",
              "price": 50,
              "item_type": "material",
              "item": "Leather Helmet",
              "name": "Helmet",
          },
          {
              "action_text": "Buy a slightly better Helmet",
              "action_type": "buy",
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
                "action_type": "change_location",
                "available_locations": {
                    "To Castell City": "back"
                },
            },
            {
                "action_text": "Open Inventory",
                "action_type": "open_inventory"
            },
            {
                "action_text": "Sell items",
                "action_type": "shop_sell",
            },
            {
                "action_type": "buy",
                "action_text": "Buy a Potion of Strength",
                "item_type": "Potion",
                "item": "Potion of Strength",
                "name": "Potion of Strength",
                "price": 100,
            },
            {
                "action_type": "buy",
                "action_text": "Buy a Potion of Toughness",
                "item": "Potion of Toughness",
                "name": "Potion of Toughness",
                "price": 100,
            },

        ],
    },

    # Forest
    {
     "name": "Forest",
     "type": "Wilderness",
     "enemy_chance": 200,
     "enemies": {
         "wild_boar": 1000,
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
             "action_type": "go_to_location",
             "name": "Castell City",
         },
         {
             "action_text": "Open Inventory",
             "action_type": "open_inventory"
         },
         {
             "action_text": "Look around.",
             "action_type": "inspect"
         },
         {
             "action_text": "Look for items.",
             "action_type": "look_around"
         },
         {
             "action_text": "Look for enemies.",
             "action_type": "combat"
         },
     ],
     "inspect_num": 0,
     "inspect": [
         unlocks["Forest 1"],
        ],
    },

    # Dark Forest
    {
        "name": "Dark Forest",
        "type": "Wilderness",
        "enemy_chance": 300,
        "enemies": {
            "wild_boar": 300,
            "big_wild_boar": 1000,
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
        "inspect": [
            unlocks["Dark Forest 1"]

        ],

        "weather": [0, 60],
        "true_weather": "cloudy",
        "list_of_actions": [
            {
                "action_text": "Go back to the Forest.",
                "action_type": "go_to_location",
                "name": "Forest",
            },
            {
                "action_text": "Open Inventory",
                "action_type": "open_inventory"
            },
            {
                "action_text": "Look around.",
                "action_type": "inspect"
            },
            {
                "action_text": "Look for items.",
                "action_type": "look_around"
            },
            {
                "action_text": "Search for enemies.",
                "action_type": "combat"
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
            unlocks["Bottom Mountain 1"],
            unlocks["Bottom Mountain 2"],
        ],

        "weather": [70, 90],
        "true_weather": "sunny",
        "list_of_actions": [
            {
                "action_text": "Go back to the Dark Forest.",
                "action_type": "go_to_location",
                "name": "Dark Forest"
            },
            {
                "action_text": "Open Inventory",
                "action_type": "open_inventory"
            },
            {
                "action_text": "Look around.",
                "action_type": "inspect"
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
                "action_type": "change_location",
                "available_locations": {
                    "Go back": "back"
                },
            },
            {
                "action_text": "Upgrade equipment.",
                "action_type": "upgrading"
            },
            {
                "action_text": "Buy Food",
                "action_type": "buy",
                "player_affected_stats": {
                    "hp": 20
                },

                "price": 20,
                "item_type": "food",
                "item": "Basic Food",
                "name": [
                    "Beagle", "Burger", "Banana", "Hot Pocket", "Doughnut", "Pizza", "Waffle", "Beef Stew", "Apple",
                    "Cheese-Wheel", "Steamed Ham", "Sandwich", "Noodles", "Ramen", "Salad", "Cucumber", "Fried Rice",
                    "Pancake", "Melon", "Rice Cracker", "Bread", "Sushi", "Fruit Salad", "Strawberry", "Pineapple",
                    "Block of Butter", "Salami", "Lettuce", "Chips", "Fries", "Fish", "Onion", "Peanuts", "Sausage",
                    "Garlic", "Hazelnuts", "Tinned Tuna", "Fried Plaice", "Turkey", "Mayonnaise"
                ]
            },

        ],
    },

    # The Cave
    {
        "name": "The Cave",
        "type": "Wilderness",
        "enemy_chance": 300,
        "enemies": {
            "skeleton": 990,
            "ogre": 1000,
        },
        "item_find_chance": 1000,
        "findable_items": {
            "Small Rock": {1: 800},
            "Shiny Crystal": {1: 10}
        },

        "welcome_text": [
            "You are in a cave in the mountain!",
            "You think that you can hear something huge walking around far down some tunnels.",
        ],
        "inspect_num": 0,
        "inspect": [

        ],

        "weather": [0, 60],
        "true_weather": "cloudy",
        "list_of_actions": [
            {
                "action_text": "Go back to the camp.",
                "action_type": "go_to_location",
                "name": "Bottom of the Mountain",
            },
            {
                "action_text": "Open Inventory",
                "action_type": "open_inventory"
            },
            {
                "action_text": "Look around.",
                "action_type": "inspect"
            },
            {
                "action_text": "Look for items.",
                "action_type": "look_around"
            },
            {
                "action_text": "Search for enemies.",
                "action_type": "combat"
            },
        ],
    },

]

#            {
#                "action_text": "Go somewhere else.",
#                "action_type": "change_location",
#                "available_locations": {
#                    "Stay": "stay",
#                    "Go to the Forest": "Forest",
#                    "Go to the Shop": "Trinkets and Tincture Trove",
#                    "Go to the Potion shop": "Potion shop"
#                },
#            },
