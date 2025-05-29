import random
import json
# Expanded lists for randomization
locations = [
    "Uttarakhand", "Rajasthan", "Goa", "Mumbai", "Delhi", 
    "Kerala", "Sundarbans", "Bangalore", "Kolkata", "Himalayas",
    "Ladakh", "Tamil Nadu", "Andaman Islands", "Jaipur", "Varanasi",
    "Hampi", "Darjeeling", "Chennai", "Pondicherry", "Rann of Kutch",
    "Amritsar", "Hyderabad", "Assam", "Meghalaya", "Kochi"
]
times_of_day = [
    "sunrise", "morning", "noon", "afternoon", "sunset", 
    "evening", "night", "midnight", "dawn", "twilight", 
    "early morning", "late afternoon", "dusk", "late night"
]
weather_conditions = [
    "sunny", "cloudy", "rainy", "foggy", "snowy", "windy", "stormy",
    "humid", "crisp", "overcast", "misty", "clear", "tropical"
]
adjectives = [
    "serene", "vibrant", "bustling", "tranquil", "majestic", 
    "picturesque", "lively", "calm", "dramatic", "enchanting",
    "ethereal", "radiant", "mystical", "pristine", "exotic", 
    "dynamic", "peaceful", "grand", "breathtaking", "festive"
]
sensory_details = [
    "sound of a shepherd’s flute", "aroma of sweets", 
    "scent of fresh jalebis", "salty scent of the river", 
    "chirping of birds", "rustling of leaves", "crashing of waves",
    "fragrance of jasmine flowers", "hum of a distant festival",
    "crackle of a bonfire", "whistle of the wind through mountains",
    "scent of sandalwood", "clinking of temple bells", "murmur of a crowd"
]

# Expanded category-specific elements
nature_main_elements = [
    "mountain valley with a crystal-clear lake reflecting snow-capped peaks",
    "dense forest with ancient trees and a carpet of wildflowers",
    "majestic waterfall cascading down a rocky cliff",
    "tranquil beach with golden sand and turquoise waters",
    "rolling hills covered in lush green tea plantations",
    "vibrant coral reef teeming with tropical fish",
    "golden desert dunes under a starlit sky",
    "bamboo forest with a hidden temple in the mist",
    "snow-covered meadow with grazing yaks",
    "mangrove-lined river with a Bengal tiger on the shore"
]

people_main_elements = [
    "group of women in colorful saris dancing at a festival",
    "fishermen unloading their catch at a bustling market",
    "children playing cricket in a dusty village street",
    "artisans crafting intricate pottery in a sunlit workshop",
    "farmers harvesting golden wheat under a clear blue sky",
    "street vendors selling spicy chaat in a crowded bazaar",
    "monks chanting in a Himalayan monastery",
    "tribal dancers performing in traditional attire",
    "yoga practitioners meditating on a riverbank",
    "weavers creating vibrant silk sarees on handlooms"
]

bollywood_celebrities = [
    "Shah Rukh Khan", "Amitabh Bachchan", "Deepika Padukone", 
    "Ranveer Singh", "Priyanka Chopra", "Salman Khan", "Aishwarya Rai",
    "Hrithik Roshan", "Kangana Ranaut", "Ranbir Kapoor", "Anushka Sharma",
    "Akshay Kumar", "Vidya Balan", "Ayushmann Khurrana"
]
hollywood_celebrities = [
    "Tom Holland", "Scarlett Johansson", "Dwayne Johnson", 
    "Emma Watson", "Chris Hemsworth", "Robert Downey Jr.", "Margot Robbie",
    "Leonardo DiCaprio", "Zendaya", "Ryan Reynolds", "Gal Gadot",
    "Brad Pitt", "Angelina Jolie", "Chris Evans"
]
celebrity_actions = [
    "standing atop a moving train in an action scene",
    "performing a dramatic monologue on a grand stage",
    "walking the red carpet at a glamorous event",
    "filming a romantic scene in a picturesque location",
    "signing autographs for adoring fans",
    "dancing energetically in a vibrant musical number",
    "riding a horse in an epic chase sequence",
    "posing for a photoshoot in a luxurious setting",
    "delivering a speech at a grand award ceremony",
    "training for a high-octane stunt scene"
]

historical_events = [
    "coronation of Chhatrapati Shivaji Maharaj at Raigad Fort",
    "Indian Independence Day celebration in 1947",
    "Battle of Panipat with warriors in traditional armor",
    "Construction of the Taj Mahal in Agra",
    "Gandhi's Salt March in 1930",
    "Vedic scholars chanting mantras in ancient Varanasi",
    "Ashoka’s victory at Kalinga in 261 BCE",
    "Rani Lakshmibai leading her troops in the 1857 rebellion",
    "Buddha attaining enlightenment under the Bodhi tree",
    "Akbar’s court in Fatehpur Sikri with scholars debating"
]

car_models = [
    "Ferrari 488", "Lamborghini Aventador", "Tesla Model S", 
    "BMW i8", "Porsche 911", "Bugatti Chiron", "Mercedes-Benz AMG",
    "Audi R8", "McLaren P1", "Rolls-Royce Phantom", "Jaguar F-Type",
    "Aston Martin DB11", "Nissan GT-R", "Ford Mustang Mach-E"
]
car_settings = [
    "speeding through neon-lit streets at midnight",
    "parked elegantly at a luxury hotel entrance",
    "racing on a winding mountain road",
    "displayed at a high-profile auto show",
    "cruising along a coastal highway at sunset",
    "drifting around corners in a desert rally",
    "parked beside a serene lake with mountains in the background",
    "revving up at a futuristic car launch event",
    "navigating a bustling city street during rush hour",
    "gleaming under the lights of a grand showroom"
]

cartoon_characters = [
    "Chhota Bheem", "Motu Patlu", "Shinchan", "Doraemon", "Tom and Jerry",
    "Mickey Mouse", "Bugs Bunny", "Krishna Kanhaiya", "Oggy and the Cockroaches",
    "Powerpuff Girls", "Ben 10", "Phineas and Ferb", "Scooby-Doo"
]
cartoon_activities = [
    "playing kabaddi in a dusty village field",
    "embarking on a treasure hunt in a mysterious jungle",
    "solving a puzzle in a colorful animated world",
    "enjoying a picnic with friends in a sunny meadow",
    "competing in a fun-filled sports tournament",
    "building a quirky invention in a vibrant workshop",
    "chasing a mischievous villain through a bustling town",
    "performing in a lively cartoon talent show",
    "exploring a magical forest with glowing creatures",
    "riding a rollercoaster in a whimsical amusement park"
]

superheroes = [
    "Spider-Man", "Wonder Woman", "Iron Man", "Captain America", "Black Panther",
    "Superman", "Batman", "Thor", "Hulk", "Captain Marvel", "Aquaman",
    "The Flash", "Green Lantern", "Doctor Strange"
]
superhero_actions = [
    "swinging between palm trees on a beach",
    "standing atop a historical monument, ready to leap into action",
    "flying over a city skyline at dusk",
    "training in a high-tech facility",
    "leading a team of heroes into battle",
    "defending a village from a cosmic threat",
    "racing through a jungle to rescue a lost expedition",
    "unveiling a new suit in a futuristic lab",
    "battling a villain atop a skyscraper",
    "patrolling a city under a starry sky"
]

# List of categories (unchanged)
categories = [
    "nature", "people", "bollywood", "hollywood", "history", 
    "cars", "cartoons", "superheroes"
]
# Define the base template for prompts
base_template = (
    "A {adjective} scene in {location} at {time_of_day}, "
    "with {weather_condition} weather, featuring {main_element}, "
    "and {sensory_detail}."
)

# Function to generate a single prompt
def generate_prompt(prompt_id, used_descriptions):
    """Generate a single unique prompt based on a random category."""
    max_attempts = 10  # Prevent infinite loops
    for _ in range(max_attempts):
        category = random.choice(categories)
        location = random.choice(locations)
        time_of_day = random.choice(times_of_day)
        weather = random.choice(weather_conditions)
        adjective = random.choice(adjectives)
        sensory_detail = random.choice(sensory_details)
        
        # Select main element based on category
        if category == "nature":
            main_element = random.choice(nature_main_elements)
        elif category == "people":
            main_element = random.choice(people_main_elements)
        elif category == "bollywood":
            celebrity = random.choice(bollywood_celebrities)
            action = random.choice(celebrity_actions)
            main_element = f"{celebrity} {action}"
        elif category == "hollywood":
            celebrity = random.choice(hollywood_celebrities)
            action = random.choice(celebrity_actions)
            main_element = f"{celebrity} {action}"
        elif category == "history":
            event = random.choice(historical_events)
            main_element = f"the {event}"
        elif category == "cars":
            car = random.choice(car_models)
            setting = random.choice(car_settings)
            main_element = f"{car} {setting}"
        elif category == "cartoons":
            character = random.choice(cartoon_characters)
            activity = random.choice(cartoon_activities)
            main_element = f"{character} {activity}"
        elif category == "superheroes":
            superhero = random.choice(superheroes)
            action = random.choice(superhero_actions)
            main_element = f"{superhero} {action}"
        
        # Format the prompt
        description = base_template.format(
            adjective=adjective,
            location=location,
            time_of_day=time_of_day,
            weather_condition=weather,
            main_element=main_element,
            sensory_detail=sensory_detail
        )
        
        # Check for uniqueness
        if description not in used_descriptions:
            used_descriptions.add(description)
            return {"prompt_id": prompt_id, "description": description}
    
    # Fallback if unique prompt can't be generated
    return {"prompt_id": prompt_id, "description": description}

# Generate 2000 prompts
num_prompts = 2000
used_descriptions = set()
prompts = []
for i in range(num_prompts):
    prompt = generate_prompt(i + 1, used_descriptions)
    prompts.append(prompt)

# Save to JSON file
output_file = "prompts_2000.json"
with open(output_file, "w") as f:
    json.dump(prompts, f, indent=2)

print(f"Generated {num_prompts} prompts and saved to {output_file}")