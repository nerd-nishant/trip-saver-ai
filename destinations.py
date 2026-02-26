"""
destinations.py
Static data for popular Indian student travel destinations.
"""

DESTINATIONS = {
    "Rishikesh": {
        "tagline": "Adventure Capital of India",
        "description": (
            "Nestled in the foothills of the Himalayas, Rishikesh is the perfect blend of "
            "adventure, spirituality, and natural beauty. Famous for white-water rafting, "
            "bungee jumping, yoga ashrams, and the iconic Ganga Aarti."
        ),
        "state": "Uttarakhand",
        "best_time": "October – April",
        "avg_budget_per_day": {"budget": 500, "mid": 1200, "premium": 2500},
        "transport_from": {
            "Delhi": {"train": "₹300–500 (Haridwar then bus/taxi)", "bus": "₹400–700 (Direct AC)"},
            "Mumbai": {"train": "₹800–1500 (to Haridwar)", "flight": "₹3000–6000 (to Dehradun)"},
            "Varanasi": {"train": "₹400–700 (to Haridwar)", "bus": "₹600–900"},
        },
        "places": [
            "Lakshman Jhula & Ram Jhula",
            "Triveni Ghat – Ganga Aarti",
            "Neelkanth Mahadev Temple",
            "Beatles Ashram (Chaurasi Kutia)",
            "Rajaji National Park",
            "Neer Garh Waterfall",
            "Kunjapuri Devi Temple (sunrise view)",
            "Shivpuri – Rafting Zone",
        ],
        "activities": [
            "White Water Rafting (₹600–1200/person)",
            "Bungee Jumping (₹3550/jump)",
            "Camping by Ganges (₹700–1500/night)",
            "Yoga & Meditation Classes (₹200–500/session)",
            "Trekking to Kunjapuri",
            "Giant Swing (₹1000/person)",
            "Cliff Jumping",
        ],
        "food_spots": [
            "Chotiwala Restaurant – Famous thali",
            "Madras Café – South Indian",
            "Little Buddha Café – Rooftop & Continental",
            "Ramana's Organic Bakery – Budget breakfast",
            "The Sitting Elephant – Traveller favourite",
        ],
        "accommodation": {
            "budget": "Hostels ₹300–600/night (Zostel, Moustache)",
            "mid": "Guesthouses ₹800–1500/night",
            "premium": "Riverside resorts ₹2500–5000/night",
        },
        "student_tips": [
            "Carry student ID – some ashrams offer free yoga",
            "Avoid flashy jewellery near ghats",
            "Book rafting packages online to save ₹200–300",
            "Travel in groups – share camping costs",
            "Best sunset from Lakshman Jhula bridge",
        ],
        "maps_url": "https://maps.google.com/?q=Rishikesh,Uttarakhand",
        "emoji": "🏔️",
        "color": "#2ecc71",
    },

    "Varanasi (Banaras)": {
        "tagline": "The Spiritual Soul of India",
        "description": (
            "One of the world's oldest and holiest cities, Varanasi (Banaras) sits on the "
            "banks of the Ganga. Home to BHU (Banaras Hindu University), 88 ghats, ancient "
            "temples, and the mesmerising Ganga Aarti. A deeply cultural experience for every student."
        ),
        "state": "Uttar Pradesh",
        "best_time": "October – March",
        "avg_budget_per_day": {"budget": 400, "mid": 900, "premium": 2000},
        "transport_from": {
            "Delhi": {"train": "₹300–600 (8–9 hrs)", "flight": "₹2500–5000"},
            "Mumbai": {"train": "₹500–1200 (15–18 hrs)", "flight": "₹3000–7000"},
            "Rishikesh": {"train": "₹400–700 (via Haridwar)", "bus": "₹500–800"},
        },
        "places": [
            "Dashashwamedh Ghat – Ganga Aarti",
            "Manikarnika Ghat (sacred cremation ghat)",
            "Kashi Vishwanath Temple",
            "Assi Ghat – Student favourite",
            "Sarnath – Buddha's first sermon site",
            "Ramnagar Fort",
            "BHU (Banaras Hindu University) Campus",
            "Tulsi Manas Temple",
            "Durga Temple (Monkey Temple)",
        ],
        "activities": [
            "Sunrise boat ride on Ganges (₹150–300/person)",
            "Evening Ganga Aarti at Dashashwamedh Ghat",
            "Banarasi silk shopping",
            "Explore narrow lanes of Old City",
            "Day trip to Sarnath (₹50 auto)",
            "Cooking class – Banarasi food",
            "Cycle tour of ghats (₹100–200)",
        ],
        "food_spots": [
            "Kashi Chat Bhandar – Famous chaat",
            "Deena Chat House – Must visit",
            "Blue Lassi Shop – Iconic Banaras lassi since 1925",
            "Mukund Lal Kachori Wala – Breakfast",
            "Pizzeria Vatika – Budget western",
            "Bati Chokha – Local Bihari-UP cuisine",
        ],
        "accommodation": {
            "budget": "Hostels & dharamshalas ₹200–500/night",
            "mid": "Guesthouses on ghats ₹700–1500/night",
            "premium": "Heritage hotels ₹3000–6000/night",
        },
        "student_tips": [
            "Wear modest clothing near temples and ghats",
            "Early morning (5 AM) boat ride is cheapest and most magical",
            "Chai & thandai are must-tries",
            "BHU museum is free for students",
            "Negotiate prices for rickshaws and auto-rickshaws",
            "Store valuables safely – crowded ghats attract pickpockets",
        ],
        "maps_url": "https://maps.google.com/?q=Varanasi,Uttar+Pradesh",
        "emoji": "🕉️",
        "color": "#e67e22",
    },

    "Manali": {
        "tagline": "Snow-Capped Paradise for Adventurers",
        "description": (
            "Manali is a high-altitude Himalayan resort town in Himachal Pradesh, favourite "
            "among student travellers for its snow-covered peaks, adventure sports, and vibrant "
            "backpacker culture in Old Manali."
        ),
        "state": "Himachal Pradesh",
        "best_time": "Oct–Jun (avoid Jul–Aug rains), Dec–Feb for snow",
        "avg_budget_per_day": {"budget": 600, "mid": 1500, "premium": 3000},
        "transport_from": {
            "Delhi": {"bus": "₹600–1200 (13–14 hrs overnight)", "shared taxi": "₹900–1200"},
            "Chandigarh": {"bus": "₹350–600 (8–9 hrs)", "taxi": "₹600–900"},
        },
        "places": [
            "Rohtang Pass (snow point)",
            "Solang Valley – Adventure sports",
            "Hadimba Devi Temple",
            "Old Manali – Café culture",
            "Vashisht Hot Springs",
            "Naggar Castle",
            "Jogini Waterfall Trek",
        ],
        "activities": [
            "Snow Activities at Solang (₹300–800)",
            "Paragliding (₹1500–2500)",
            "Trekking to Bhrigu Lake",
            "River Crossing & Zorbing",
            "Rohtang Pass jeep safari (₹2500–3500 for shared jeep)",
        ],
        "food_spots": [
            "Johnson's Café – Continental",
            "Casa Bella Vista – Rooftop",
            "Café 1947 – Budget & cosy",
            "Drifters Inn – Backpacker favourite",
        ],
        "accommodation": {
            "budget": "Hostels ₹400–700/night (Zostel Manali)",
            "mid": "Guesthouses ₹1000–2000/night",
            "premium": "Resorts ₹3000–8000/night",
        },
        "student_tips": [
            "Book Rohtang Pass permit online – only 1200 vehicles/day allowed",
            "Carry heavy woolens even in summer",
            "Old Manali has cheaper stays than Mall Road",
            "Group bookings save significantly on jeep safaris",
        ],
        "maps_url": "https://maps.google.com/?q=Manali,Himachal+Pradesh",
        "emoji": "❄️",
        "color": "#3498db",
    },

    "Goa": {
        "tagline": "Sun, Sand & Student Vibes",
        "description": (
            "India's smallest state and most popular beach destination. Goa offers "
            "a unique blend of Portuguese heritage, stunning beaches, vibrant nightlife, "
            "and affordable backpacker stays — a student favourite year-round."
        ),
        "state": "Goa",
        "best_time": "November – February",
        "avg_budget_per_day": {"budget": 700, "mid": 1500, "premium": 3500},
        "transport_from": {
            "Mumbai": {"train": "₹300–700 (9–11 hrs)", "flight": "₹2000–4000 (1 hr)"},
            "Bangalore": {"train": "₹300–600 (9–11 hrs)", "bus": "₹600–900"},
        },
        "places": [
            "Baga & Calangute Beach",
            "Anjuna Flea Market",
            "Dudhsagar Falls",
            "Fort Aguada",
            "Palolem Beach – South Goa",
            "Old Goa – Churches & Heritage",
            "Arambol Beach – Hippie vibe",
        ],
        "activities": [
            "Water sports – parasailing, jet ski, surfing (₹500–2000)",
            "Scooter/bike rental (₹250–400/day)",
            "Dudhsagar Falls jeep tour (₹900–1200)",
            "Night market at Anjuna",
        ],
        "food_spots": [
            "Fisherman's Wharf – Seafood",
            "Britto's – Beach shack classic",
            "Café Tato – Cheap local thali",
            "Martin's Corner – Goan cuisine",
        ],
        "accommodation": {
            "budget": "Hostels ₹450–800/night (Zostel, Jungle by Stunn)",
            "mid": "Beach guesthouses ₹1200–2500/night",
            "premium": "Beach resorts ₹4000–10000/night",
        },
        "student_tips": [
            "Rent a scooter – most economical way to explore",
            "South Goa (Palolem) is cheaper and quieter than North Goa",
            "Avoid December peak season – prices spike 3x",
            "Carry student ID for museum discounts",
        ],
        "maps_url": "https://maps.google.com/?q=Goa,India",
        "emoji": "🏖️",
        "color": "#f39c12",
    },

    "Jaipur": {
        "tagline": "The Pink City of Rajasthan",
        "description": (
            "Jaipur, the capital of Rajasthan, is a stunning walled city known for its "
            "pink-hued architecture, magnificent forts, and vibrant bazaars. Part of the "
            "Golden Triangle with Delhi and Agra, it's historically and culturally unmissable."
        ),
        "state": "Rajasthan",
        "best_time": "October – March",
        "avg_budget_per_day": {"budget": 500, "mid": 1200, "premium": 2800},
        "transport_from": {
            "Delhi": {"train": "₹200–500 (4–5 hrs)", "bus": "₹250–450", "flight": "₹2000–4000"},
            "Mumbai": {"train": "₹400–900 (16–18 hrs)", "flight": "₹2500–5000"},
        },
        "places": [
            "Amber Fort",
            "Hawa Mahal (Palace of Winds)",
            "City Palace",
            "Jantar Mantar (UNESCO site)",
            "Jal Mahal (Water Palace)",
            "Nahargarh Fort – sunset point",
            "Johari Bazaar – shopping",
        ],
        "activities": [
            "Elephant ride at Amber Fort (₹900/person)",
            "Hot air balloon (₹5500–7000/person)",
            "Camel ride at Jal Mahal",
            "Rajasthani cooking class",
            "Heritage walk in Old City",
            "Shopping – gems, textiles, handicrafts",
        ],
        "food_spots": [
            "Lassiwala – Famous lassi since 1944",
            "Rawat Mishtan Bhandar – Pyaaz kachori",
            "Chokhi Dhani – Cultural village dining",
            "Peacock Rooftop Restaurant",
        ],
        "accommodation": {
            "budget": "Hostels ₹350–700/night (Moustache Jaipur)",
            "mid": "Heritage guesthouses ₹1000–2000/night",
            "premium": "Heritage palaces ₹4000–15000/night",
        },
        "student_tips": [
            "Composite ticket for 5 forts saves money (₹300 for students)",
            "Bargain hard at bazaars – first price is always 3x",
            "Jaipur metro is cheap and covers key areas",
            "Combine with Agra & Delhi for the Golden Triangle budget trip",
        ],
        "maps_url": "https://maps.google.com/?q=Jaipur,Rajasthan",
        "emoji": "🏰",
        "color": "#e74c3c",
    },

    "Darjeeling": {
        "tagline": "Queen of Hills & Tea Gardens",
        "description": (
            "Darjeeling is a charming hill station in West Bengal, famous for its toy train, "
            "world-renowned Darjeeling tea, views of Kangchenjunga, and the colonial-era charm "
            "of its bazaars and monasteries."
        ),
        "state": "West Bengal",
        "best_time": "March – May, September – November",
        "avg_budget_per_day": {"budget": 500, "mid": 1200, "premium": 2500},
        "transport_from": {
            "Kolkata": {"train": "₹300–600 (to NJP, then toy train/jeep)", "flight": "₹2500–5000 to Bagdogra"},
            "Siliguri": {"jeep": "₹200–300 shared, 3 hrs"},
        },
        "places": [
            "Tiger Hill – Sunrise & Kanchenjunga view",
            "Toy Train (UNESCO World Heritage)",
            "Batasia Loop",
            "Peace Pagoda",
            "Happy Valley Tea Estate",
            "Rock Garden & Ganga Maya Park",
            "Himalayan Mountaineering Institute",
        ],
        "activities": [
            "Sunrise at Tiger Hill (₹100, bus ₹80)",
            "Toy train joy ride (₹1460/person)",
            "Tea tasting at tea estates (Free–₹200)",
            "Trekking – Sandakphu (3630m altitude)",
        ],
        "food_spots": [
            "Glenary's Bakery – Famous since 1935",
            "Kunga Restaurant – Tibetan & Nepali",
            "Nathmull's Tea Room",
            "Hot Stimulating Café",
        ],
        "accommodation": {
            "budget": "Guesthouses ₹400–800/night",
            "mid": "Hotels ₹1000–2000/night",
            "premium": "Heritage bungalows ₹3000–6000/night",
        },
        "student_tips": [
            "Carry warm layers – even in summer it's cold",
            "Shared jeeps are cheapest transport option",
            "Book toy train in advance, especially peak season",
            "Visit tea estates early morning for best experience",
        ],
        "maps_url": "https://maps.google.com/?q=Darjeeling,West+Bengal",
        "emoji": "🍵",
        "color": "#9b59b6",
    },
}
