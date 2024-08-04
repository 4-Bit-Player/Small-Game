

unlocks = {
    "Castell Shop": {
        "u_name": "Castell Shop",
        "type": "actions",
        "action_text": "Go to the shop.",
        "action_type": "go_to_location",
        "name": "Trinkets and Tincture Trove",
    },
    "Castell Potion Shop": {
        "u_name": "Castell Potion Shop",
        "type": "actions",
        "action_text": "Go to the potion shop.",
        "action_type": "go_to_location",
        "name": "Potion shop",
    },
    "Go to Forest": {
        "u_name": "Go to Forest",
        "type": "actions",
        "action_text": "Go to the Forest.",
        "action_type": "go_to_location",
        "name": "Forest",
    },
    "Go to Dark Forest": {
        "u_name": "Go to Dark Forest",
        "type": "actions",
        "action_text": "Go deeper into the forest.",
        "action_type": "go_to_location",
        "name": "Dark Forest",
    },
    "Go to Bottom of the Mountain": {
        "u_name": "Go to Bottom of the Mountain",
        "type": "actions",
        "action_text": "Continue your journey.",
        "action_type": "go_to_location",
        "name": "Bottom of the Mountain",
    },
    "Go to Blacksmith": {
        "u_name": "Go to Blacksmith",
        "type": "actions",
        "action_text": "Visit the Blacksmith",
        "action_type": "go_to_location",
        "name": "Blacksmith",
    },
    "Unlock Bottom of Mountain": {
        "u_name": "Unlock Bottom of Mountain",
        "broad_desc": "Follow the trail of the Deer",
        "text": [
            "It's difficult to follow the trail.",
            "Sometimes you loose the trail, but can find it again a bit further ahead.",
            "You are able to follow it like that for around half an hour.",
            "And it leads you out of the Dark Forest.",
            "But unfortunately you ultimately loose it completely.",
            "On the other hand, you find yourself at the bottom of a mountain.",
        ],
        "unlocks": "Go to Bottom of the Mountain",
        "unlock_location": "Dark Forest",
    },
    "Unlock Dark Forest": {
        "u_name": "Unlock Dark Forest",
        "broad_desc": "Look for hidden things",
        "text": [
            "You spot a path that leads deeper into the forest.",
            "The trees seem to be standing closer to each other there..."
        ],
        "unlocks": "Go to Dark Forest",
        "unlock_location": "Forest",
    },




    "Castell 1": {
        "u_name": "Castell 1",
        "broad_desc": "Walk through the streets of the city.",
        "text": [
            "As you walk around the city you spot a small shop that you haven't noticed before.",
            "They sell bread and equipment...",
            "Which is an odd combination, but who cares...",
        ],
        "unlocks": "Castell Shop",
        "unlock_location": "Castell City"
    },
    "Castell 2": {
        "u_name": "Castell 2",
        "broad_desc": "Walk around byways.",
        "text": [
            "As you continue to walk around you stumble upon a potion shop.",
            "It looks a bit run down, but it seems like someone still runs it.",
        ],
        "unlocks": "Castell Potion Shop",
        "unlock_location": "Castell City"
    },
    "Castell 3": {
        "u_name": "Castell 3",
        "broad_desc": "Walk to the gates.",
        "text": [
            "You have enough from walking around in the city.",
            "There are boars outside that are a threat to the people!",
            "And you have to revenge your friend!",
        ],
        "unlocks": "Go to Forest",
        "unlock_location": "Castell City"
    },


    "Forest 1": {
        "u_name": "Forest 1",
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





    "Dark Forest 1": {
        "u_name": "Dark Forest 1",
        "broad_desc": "Look at the surrounding area",
        "text": [
            "At the end of the forest you see a grand rocky mountain."
        ],
        "unlocks": {},
        "unlock_location": "",
    },
    "Dark Forest 2": {
        "u_name": "Dark Forest 2",
        "broad_desc": "Check out the camp at the side of the road",
        "text": [
            "As you walk around the camp you see quiet a few people.",
            "You notice a blacksmith who is repairing the gear from an adventurer.",
            "Maybe he can repair your gear as well..."
        ],
        "unlocks": "Go to Blacksmith",
        "unlock_location": "Bottom of the Mountain",
    }







}
unlocked = []
