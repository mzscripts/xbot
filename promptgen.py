import random
import json
# Expanded lists for randomization
locations = [
    "Kashmir Valley", "Gujarat", "Lakshadweep", "Pune", "Agra",
    "Karnataka", "Brahmaputra River", "Mysore", "Guwahati", "Western Ghats",
    "Spiti Valley", "Andhra Pradesh", "Nicobar Islands", "Udaipur", "Jaisalmer",
    "Khajuraho", "Munnar", "Madurai", "Auroville", "Thar Desert",
    "Srinagar", "Ahmedabad", "Nagaland", "Sikkim", "Alleppey"
]

times_of_day = [
    "daybreak", "mid-morning", "midday", "late morning", "golden hour",
    "twilight", "late evening", "after midnight", "early dawn", "evening glow",
    "pre-dawn", "early afternoon", "nightfall", "wee hours"
]

weather_conditions = [
    "bright", "hazy", "showery", "misty", "frosty", "breezy", "thunderous",
    "sultry", "chilly", "partly cloudy", "dewy", "sparkling", "balmy"
]

adjectives = [
    "peaceful", "luminous", "energetic", "soothing", "regal",
    "charming", "spirited", "quiet", "striking", "magical",
    "dreamy", "vivid", "mysterious", "untouched", "alluring",
    "lively", "harmonious", "imposing", "stunning", "joyful"
]

sensory_details = [
    "melody of a sitar in the distance", "aroma of brewing chai",
    "scent of blooming lotuses", "briny breeze from the ocean",
    "twittering of sparrows", "swaying of palm fronds", "roar of a distant waterfall",
    "fragrance of marigold garlands", "echoes of a street musician’s flute",
    "crackling of dry leaves underfoot", "howl of a desert wind",
    "scent of freshly baked naan", "chiming of anklets in a dance",
    "buzz of a lively marketplace"
]

# Category-specific elements
nature_main_elements = [
    "lush valley with a meandering river and grazing deer",
    "ancient banyan grove with hanging roots and chirping parrots",
    "towering sand dunes casting dramatic shadows at dusk",
    "pristine lagoon fringed with coconut palms",
    "sprawling vineyards under a golden sunrise",
    "jagged cliffs overlooking a stormy sea",
    "frosty alpine meadow dotted with wild herbs",
    "moss-covered canyon with a trickling stream",
    "blooming orchid garden under a misty sky",
    "wetland with flamingos wading in shallow waters"
]

people_main_elements = [
    "elders sharing stories around a village bonfire",
    "merchants haggling in a vibrant spice market",
    "students practicing kathak dance in an open courtyard",
    "potters shaping clay on spinning wheels",
    "nomads herding camels across a desert expanse",
    "pilgrims bathing in a sacred river at dawn",
    "musicians playing folk tunes at a rural fair",
    "women embroidering intricate patterns in a cooperative",
    "kids flying kites on a windy hilltop",
    "vendors grilling kebabs at a bustling night market"
]

bollywood_celebrities = [
    "Ranbir Kapoor", "Alia Bhatt", "Varun Dhawan", "Katrina Kaif",
    "Saif Ali Khan", "Kareena Kapoor", "Vicky Kaushal", "Ananya Panday",
    "Shahid Kapoor", "Kiara Advani", "Tiger Shroff", "Janhvi Kapoor",
    "Sidharth Malhotra", "Disha Patani"
]

hollywood_celebrities = [
    "Chris Pratt", "Natalie Portman", "Tom Hanks", "Emma Stone",
    "Ryan Gosling", "Charlize Theron", "Hugh Jackman", "Florence Pugh",
    "Keanu Reeves", "Meryl Streep", "Johnny Depp", "Anne Hathaway",
    "Jake Gyllenhaal", "Zendaya"
]

celebrity_actions = [
    "rehearsing for a high-energy dance sequence",
    "delivering an emotional speech in a courtroom scene",
    "attending a charity gala in a dazzling outfit",
    "filming a chase scene through crowded streets",
    "posing for a magazine cover in a scenic backdrop",
    "performing a stunt on a helicopter",
    "singing a soulful ballad in a recording studio",
    "walking through a film set in period costume",
    "greeting fans at a movie premiere",
    "training in martial arts for an action role"
]

historical_events = [
    "Jallianwala Bagh gathering in 1919",
    "Coronation of Maharana Pratap in Mewar",
    "First train journey in India in 1853",
    "Construction of Qutub Minar in Delhi",
    "Tagore composing the national anthem in 1911",
    "Ancient artisans carving Ellora caves",
    "Tipu Sultan’s battle against the British in 1799",
    "Dandi Salt March led by Gandhi in 1930",
    "Chandragupta Maurya’s coronation in 321 BCE",
    "Ramanujan presenting mathematical theorems in 1914"
]

car_models = [
    "Porsche Taycan", "Lamborghini Huracán", "Tesla Model 3",
    "Ferrari SF90", "BMW M5", "McLaren 720S", "Mercedes-Benz G-Class",
    "Audi e-tron GT", "Bentley Continental", "Rolls-Royce Cullinan",
    "Jaguar I-PACE", "Aston Martin Vantage", "Lexus LC 500", "Chevrolet Corvette"
]

car_settings = [
    "gliding through a misty forest road at dawn",
    "parked in front of a grand palace",
    "speeding across a salt flat under a blazing sun",
    "showcased at a futuristic car expo",
    "cruising along a cliffside road at twilight",
    "racing through a tunnel with glowing lights",
    "parked on a cobblestone street in an old town",
    "revving up at a desert car rally",
    "navigating a snowy mountain pass",
    "displayed in a sleek urban showroom"
]

cartoon_characters = [
    "Little Krishna", "Bal Hanuman", "Roll No. 21", "Mighty Raju",
    "Noddy", "Peppa Pig", "SpongeBob SquarePants", "Simba the Lion",
    "Paw Patrol", "Dora the Explorer", "Mr. Bean (animated)", "Gattu Battu",
    "Vir: The Robot Boy"
]

cartoon_activities = [
    "racing bicycles in a colorful village",
    "searching for a hidden treasure in a pirate ship",
    "building a sandcastle on a sunny beach",
    "solving a mystery in a spooky mansion",
    "playing hide-and-seek in a magical garden",
    "performing in a lively school talent show",
    "exploring a glowing cave with friendly creatures",
    "flying kites in a vibrant festival",
    "baking a giant cake in a whimsical kitchen",
    "competing in a quirky robot-building contest"
]

superheroes = [
    "Black Widow", "Wolverine", "Hawkeye", "Shang-Chi", "Storm",
    "Deadpool", "Ant-Man", "Vision", "Scarlet Witch", "Falcon",
    "Green Arrow", "Black Canary", "Nightwing", "Iron Fist"
]

superhero_actions = [
    "leaping across rooftops in a moonlit city",
    "training with a master in a hidden dojo",
    "flying through a stormy sky to stop a disaster",
    "defending a fortress from an alien invasion",
    "rescuing villagers from a collapsing bridge",
    "unveiling a new gadget in a secret lab",
    "battling a robot army in a futuristic city",
    "patrolling a desert outpost at night",
    "chasing a villain through a crowded festival",
    "standing guard atop a sacred temple"
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
num_prompts = 1000
used_descriptions = set()
prompts = []
for i in range(num_prompts):
    prompt = generate_prompt(i + 1, used_descriptions)
    prompts.append(prompt)

# Save to JSON file
output_file = "prompts_1000.json"
with open(output_file, "w") as f:
    json.dump(prompts, f, indent=2)

print(f"Generated {num_prompts} prompts and saved to {output_file}")