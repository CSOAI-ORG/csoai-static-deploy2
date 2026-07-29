#!/usr/bin/env python3
"""enhance_reasoning_training.py — Add ARC-Challenge and HellaSwag style reasoning examples.

Generates 80+ new training examples focused on:
1. ARC-Challenge: Scientific reasoning (grade school level)
2. HellaSwag: Commonsense inference about everyday scenarios
3. Multi-step logical reasoning
4. Causal reasoning
5. Analogical reasoning

Output: sov_all_training_data_enhanced.json (240+ examples total)
"""
import json
from pathlib import Path

# ARC-Challenge style: Scientific reasoning
ARC_CHALLENGE_EXAMPLES = [
    # Physics
    {
        "prompt": "A student puts a ice cube on a plate in direct sunlight. What will happen to the ice cube?",
        "completion": "The ice cube will melt. Sunlight provides heat energy, which raises the temperature of the ice above 0°C, causing it to change from solid to liquid state through melting.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
    {
        "prompt": "Which force keeps the planets in orbit around the Sun?",
        "completion": "Gravity keeps the planets in orbit. The Sun's massive gravitational pull attracts planets, while their forward momentum creates a balance that results in stable elliptical orbits.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
    {
        "prompt": "A ball is thrown straight up into the air. What happens to its speed as it rises?",
        "completion": "The ball's speed decreases as it rises. Gravity pulls downward, decelerating the ball at 9.8 m/s² until it reaches its highest point where speed is momentarily zero.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
    {
        "prompt": "Why does a metal spoon feel colder than a wooden spoon at the same temperature?",
        "completion": "Metal conducts heat away from your hand faster than wood. Both spoons are the same temperature, but metal's higher thermal conductivity transfers heat more efficiently, making it feel colder.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
    {
        "prompt": "What happens to the volume of a gas when you increase its temperature at constant pressure?",
        "completion": "The volume increases. According to Charles's Law, volume is directly proportional to temperature (at constant pressure). Heating gas molecules move faster and spread further apart.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
    # Biology
    {
        "prompt": "Why do plants need sunlight to grow?",
        "completion": "Plants need sunlight for photosynthesis. They convert light energy, water, and carbon dioxide into glucose (food) and oxygen. Without sunlight, plants cannot produce energy for growth.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
    {
        "prompt": "What would happen if all decomposers were removed from an ecosystem?",
        "completion": "Dead organisms would accumulate and nutrients would not recycle. Decomposers break down dead matter, returning nutrients to soil. Without them, ecosystems would collapse as nutrient cycles break.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
    {
        "prompt": "Why do we see lightning before we hear thunder?",
        "completion": "Light travels much faster than sound. Lightning produces both light and sound simultaneously, but light reaches us almost instantly while sound travels at about 343 meters per second.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
    {
        "prompt": "How does a vaccine protect the body from disease?",
        "completion": "Vaccines train the immune system. They contain weakened or inactive pathogens that stimulate antibody production. If the real pathogen enters later, the body recognizes and fights it quickly.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
    {
        "prompt": "Why does the Moon appear to change shape throughout the month?",
        "completion": "The Moon's apparent shape changes due to its position relative to Earth and Sun. As the Moon orbits Earth, different portions of its sunlit half become visible from Earth.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
    # Chemistry
    {
        "prompt": "What happens when you mix baking soda and vinegar?",
        "completion": "A chemical reaction produces carbon dioxide gas, water, and sodium acetate. The bubbling is CO₂ escaping. This is an acid-base reaction between acetic acid and sodium bicarbonate.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
    {
        "prompt": "Why does iron rust faster in wet conditions?",
        "completion": "Water accelerates oxidation. Iron rusts when it reacts with oxygen and water. Moisture provides the electrolyte needed for the electrochemical reaction that converts iron to iron oxide.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
    {
        "prompt": "What makes salt dissolve in water?",
        "completion": "Water molecules attract and separate salt ions. Water is polar—its oxygen attracts sodium ions while hydrogen attracts chloride ions. This pulls the crystal structure apart.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
    # Earth Science
    {
        "prompt": "Why are fossils found in mountain rocks?",
        "completion": "Mountains were once underwater. Fossils form in sedimentary rock at sea level. Over millions of years, tectonic plate collisions pushed these rocks upward, forming mountains with marine fossils.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
    {
        "prompt": "What causes seasons on Earth?",
        "completion": "Earth's tilted axis causes seasons. As Earth orbits the Sun, different hemispheres receive varying amounts of direct sunlight. Summer occurs when your hemisphere tilts toward the Sun.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
    {
        "prompt": "Why does hot air rise?",
        "completion": "Hot air is less dense than cold air. Heating causes air molecules to move faster and spread apart, making hot air lighter. Buoyancy forces push the lighter hot air upward.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
    {
        "prompt": "How do earthquakes happen?",
        "completion": "Earthquakes occur when tectonic plates suddenly slip. Stress builds up along fault lines until rocks break, releasing energy as seismic waves that shake the ground.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
    {
        "prompt": "Why is the sky blue?",
        "completion": "The sky appears blue due to Rayleigh scattering. Shorter blue wavelengths of sunlight scatter more in the atmosphere than longer wavelengths, making the sky look blue from all directions.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
    {
        "prompt": "What causes rainbows?",
        "completion": "Rainbows form when sunlight refracts, reflects, and disperses in water droplets. Different wavelengths bend at different angles, separating white light into the visible spectrum.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
    {
        "prompt": "Why do we have high and low tides?",
        "completion": "Tides are caused by the Moon's gravitational pull. The Moon attracts water toward it, creating a bulge (high tide). The opposite side also bulges due to inertia, creating two high tides daily.",
        "category": "reasoning",
        "type": "arc_challenge"
    },
]

# HellaSwag style: Commonsense inference about everyday scenarios
HELLASWAG_EXAMPLES = [
    {
        "prompt": "A person is cooking pasta. They put the pasta in boiling water. What happens next?",
        "completion": "The pasta softens and cooks. After 8-12 minutes in boiling water, the pasta absorbs water, becomes tender, and is ready to eat. The person will drain it in a colander.",
        "category": "reasoning",
        "type": "hellaswag"
    },
    {
        "prompt": "Someone is walking in the rain without an umbrella. What will they do?",
        "completion": "They will get wet and likely seek shelter. They might run to find cover, hold something over their head, or accept getting soaked while continuing to their destination.",
        "category": "reasoning",
        "type": "hellaswag"
    },
    {
        "prompt": "A cat is sitting on a windowsill watching birds outside. What does the cat do?",
        "completion": "The cat watches intently, possibly chattering its teeth or making chirping sounds. Its pupils dilate, tail twitches, and it may crouch in a pre-pounce position, though it cannot reach the birds.",
        "category": "reasoning",
        "type": "hellaswag"
    },
    {
        "prompt": "Someone drops their phone in water. What should they do immediately?",
        "completion": "They should turn off the phone immediately and not try to charge it. They should dry the exterior, remove the case, and place it in rice or silica gel to absorb moisture.",
        "category": "reasoning",
        "type": "hellaswag"
    },
    {
        "prompt": "A person is running late for work. What might they skip?",
        "completion": "They might skip breakfast, skip their morning coffee, or skip checking email. They would rush through their routine, possibly skipping makeup or grooming to save time.",
        "category": "reasoning",
        "type": "hellaswag"
    },
    {
        "prompt": "Someone finds a wallet on the street. What is the right thing to do?",
        "completion": "The right thing is to return it. They should check for ID to contact the owner, turn it in to nearby business, or take it to the police station. Most people would try to find the owner.",
        "category": "reasoning",
        "type": "hellaswag"
    },
    {
        "prompt": "A child is learning to ride a bicycle. What happens when they lose balance?",
        "completion": "The child falls, possibly scraping their knee. A parent might rush to help, apply a bandage, and encourage them to try again. The child learns through practice and falling.",
        "category": "reasoning",
        "type": "hellaswag"
    },
    {
        "prompt": "Someone is studying for an exam late at night. What might help them focus?",
        "completion": "They might drink coffee or tea, take short breaks, use flashcards, or play background music. They could also remove distractions like their phone and study in a quiet room.",
        "category": "reasoning",
        "type": "hellaswag"
    },
    {
        "prompt": "A person sees a dog running toward them without a leash. What should they do?",
        "completion": "They should stay calm and still. Running might trigger the dog's chase instinct. They should avoid direct eye contact, stand sideways, and let the dog sniff them if it approaches.",
        "category": "reasoning",
        "type": "hellaswag"
    },
    {
        "prompt": "Someone burns their hand on a hot stove. What is the first aid?",
        "completion": "They should run cool (not cold) water over the burn for 10-20 minutes. They should not apply ice, butter, or toothpaste. They can cover it with a clean bandage and take pain relievers.",
        "category": "reasoning",
        "type": "hellaswag"
    },
    {
        "prompt": "A person is driving and their tire blows out. What should they do?",
        "completion": "They should grip the steering firmly, take their foot off the gas, and gradually slow down. They should not brake hard. They should pull over safely, turn on hazard lights, and call for help.",
        "category": "reasoning",
        "type": "hellaswag"
    },
    {
        "prompt": "Someone is allergic to cats but visits a house with cats. What might happen?",
        "completion": "They might sneeze, get itchy eyes, or develop a rash. They could take antihistamines beforehand, avoid touching their face, or limit their visit duration to reduce symptoms.",
        "category": "reasoning",
        "type": "hellaswag"
    },
    {
        "prompt": "A person leaves milk out of the refrigerator all day. Is it safe to drink?",
        "completion": "It depends on the temperature. Milk left out for more than 2 hours (1 hour if above 90°F) should be discarded. Bacteria multiply rapidly at room temperature, spoiling the milk.",
        "category": "reasoning",
        "type": "hellaswag"
    },
    {
        "prompt": "Someone is painting a room. What should they do before painting?",
        "completion": "They should prepare the room by moving furniture, covering floors with drop cloths, taping edges, filling holes with spackle, sanding rough spots, and applying primer if needed.",
        "category": "reasoning",
        "type": "hellaswag"
    },
    {
        "prompt": "A person receives a suspicious email asking for their password. What should they do?",
        "completion": "They should not reply or click any links. They should report it as phishing, delete it, and if concerned, change their password directly through the official website, not through email links.",
        "category": "reasoning",
        "type": "hellaswag"
    },
    {
        "prompt": "Someone is moving to a new apartment. What do they need to do first?",
        "completion": "They should start by packing non-essential items, notifying their landlord, setting up utilities at the new place, and arranging for movers or a rental truck.",
        "category": "reasoning",
        "type": "hellaswag"
    },
    {
        "prompt": "A person wants to start exercising regularly. What is a good approach?",
        "completion": "They should start slowly with activities they enjoy, like walking or swimming. They can set realistic goals, schedule workouts, find a workout buddy, and gradually increase intensity.",
        "category": "reasoning",
        "type": "hellaswag"
    },
    {
        "prompt": "Someone's car won't start on a cold morning. What might be wrong?",
        "completion": "The battery might be weak or dead, as cold reduces battery capacity. The oil might be too thick, or the fuel line could be frozen. They might need a jump start or battery replacement.",
        "category": "reasoning",
        "type": "hellaswag"
    },
    {
        "prompt": "A person is hosting a dinner party. What should they consider?",
        "completion": "They should consider guest dietary restrictions, plan a menu, shop for ingredients, clean the house, set the table, and prepare dishes that can be made ahead of time.",
        "category": "reasoning",
        "type": "hellaswag"
    },
    {
        "prompt": "Someone loses their house keys. What can they do?",
        "completion": "They can check common places like pockets, bags, and counters. They might have a spare key hidden outside, or they can call a locksmith. They could also check if a roommate is home.",
        "category": "reasoning",
        "type": "hellaswag"
    },
]

# Multi-step logical reasoning
MULTI_STEP_REASONING = [
    {
        "prompt": "If it takes 3 hours to paint a room, how long would it take 3 painters working together?",
        "completion": "It would take 1 hour. Three painters working together can complete three times the work in the same time. So 3 hours divided by 3 painters equals 1 hour.",
        "category": "reasoning",
        "type": "multi_step"
    },
    {
        "prompt": "A store has 100 items. 40% are on sale. Of those on sale, 25% are also discounted an extra 10%. How many items have the extra discount?",
        "completion": "10 items have the extra discount. 40% of 100 is 40 items on sale. 25% of those 40 items is 10 items with the extra 10% discount.",
        "category": "reasoning",
        "type": "multi_step"
    },
    {
        "prompt": "If you save $50 per month, how much will you have after 2 years with 5% annual interest?",
        "completion": "You'll have approximately $1,283. Without interest: $50 × 24 months = $1,200. With 5% annual interest compounded monthly, you earn about $83 in interest over 2 years.",
        "category": "reasoning",
        "type": "multi_step"
    },
    {
        "prompt": "A train leaves at 9 AM traveling 60 mph. Another train leaves at 10 AM traveling 80 mph in the same direction. When does the second train catch up?",
        "completion": "The second train catches up at 12 PM (noon). By 10 AM, the first train has a 60-mile lead. The second train closes the gap at 20 mph (80-60). It takes 3 hours to close 60 miles.",
        "category": "reasoning",
        "type": "multi_step"
    },
    {
        "prompt": "If a shirt costs $25 after a 20% discount, what was the original price?",
        "completion": "The original price was $31.25. If $25 is 80% of the original (100% - 20% discount), then $25 ÷ 0.80 = $31.25.",
        "category": "reasoning",
        "type": "multi_step"
    },
    {
        "prompt": "A baker makes 120 cookies. He sells 60% in the morning and 50% of the remainder in the afternoon. How many are left?",
        "completion": "24 cookies are left. He sells 60% (72 cookies) in the morning, leaving 48. He sells 50% of those (24 cookies) in the afternoon, leaving 24.",
        "category": "reasoning",
        "type": "multi_step"
    },
    {
        "prompt": "If 5 apples cost $3, how much do 8 apples cost?",
        "completion": "8 apples cost $4.80. Each apple costs $3 ÷ 5 = $0.60. So 8 apples cost 8 × $0.60 = $4.80.",
        "category": "reasoning",
        "type": "multi_step"
    },
    {
        "prompt": "A rectangle is 3 times as long as it is wide. If the perimeter is 48 cm, what are the dimensions?",
        "completion": "The rectangle is 6 cm wide and 18 cm long. If width = w, then length = 3w. Perimeter = 2(w + 3w) = 8w = 48. So w = 6 cm and length = 18 cm.",
        "category": "reasoning",
        "type": "multi_step"
    },
    {
        "prompt": "If you flip a coin 3 times, what is the probability of getting exactly 2 heads?",
        "completion": "The probability is 3/8 (37.5%). There are 8 possible outcomes (2³). Three outcomes have exactly 2 heads: HHT, HTH, THH. So 3/8 = 0.375.",
        "category": "reasoning",
        "type": "multi_step"
    },
    {
        "prompt": "A car travels 150 miles in 3 hours. If it maintains this speed, how far will it travel in 5 hours?",
        "completion": "It will travel 250 miles. The speed is 150 ÷ 3 = 50 mph. In 5 hours: 50 × 5 = 250 miles.",
        "category": "reasoning",
        "type": "multi_step"
    },
]

# Causal reasoning
CAUSAL_REASONING = [
    {
        "prompt": "Why does turning up the thermostat make a room warmer?",
        "completion": "The thermostat signals the heating system to produce more heat. The furnace or boiler runs longer, generating more warm air or water that circulates through the room, raising the temperature.",
        "category": "reasoning",
        "type": "causal"
    },
    {
        "prompt": "What causes a glass to break when you pour boiling water into it?",
        "completion": "Thermal shock causes the glass to break. The boiling water rapidly heats the inner surface, causing it to expand faster than the outer surface. This uneven expansion creates stress that cracks the glass.",
        "category": "reasoning",
        "type": "causal"
    },
    {
        "prompt": "Why does exercise make you feel tired?",
        "completion": "Exercise depletes energy stores and produces waste products. Muscles use glycogen for energy, producing lactic acid. The body also uses oxygen faster than it can be replaced, causing fatigue.",
        "category": "reasoning",
        "type": "causal"
    },
    {
        "prompt": "What causes a sore throat when you have a cold?",
        "completion": "The cold virus infects throat tissues, causing inflammation. The immune response increases blood flow and mucus production, leading to swelling, irritation, and pain in the throat.",
        "category": "reasoning",
        "type": "causal"
    },
    {
        "prompt": "Why do roads get slippery when it first starts raining?",
        "completion": "Rain mixes with oil and dust on the road surface, creating a slippery film. This mixture reduces tire traction before the rain washes it away, making roads most slippery at the start of rain.",
        "category": "reasoning",
        "type": "causal"
    },
    {
        "prompt": "What causes the batteries in a remote control to die?",
        "completion": "Batteries die as chemical reactions deplete their stored energy. Each use converts chemical energy to electrical energy. Over time, reactants are consumed and waste products accumulate, reducing voltage.",
        "category": "reasoning",
        "type": "causal"
    },
    {
        "prompt": "Why does food cook faster in a pressure cooker?",
        "completion": "A pressure cooker raises the boiling point of water. Increased pressure raises the temperature above 100°C, causing water to boil at 120°C. Higher temperature cooks food faster.",
        "category": "reasoning",
        "type": "causal"
    },
    {
        "prompt": "What causes static electricity when you rub a balloon on your hair?",
        "completion": "Friction transfers electrons between surfaces. The balloon gains electrons from your hair, becoming negatively charged. Your hair loses electrons, becoming positively charged. Opposite charges attract.",
        "category": "reasoning",
        "type": "causal"
    },
    {
        "prompt": "Why does alcohol evaporate faster than water?",
        "completion": "Alcohol has weaker intermolecular forces than water. Ethanol molecules are less attracted to each other, requiring less energy to escape the liquid surface. This makes alcohol evaporate faster.",
        "category": "reasoning",
        "type": "causal"
    },
    {
        "prompt": "What causes a plant to wilt when not watered?",
        "completion": "Without water, plant cells lose turgor pressure. Water normally fills cell vacuoles, keeping cells rigid. When water is scarce, cells shrink, causing the plant to wilt and droop.",
        "category": "reasoning",
        "type": "causal"
    },
]

# Analogical reasoning
ANALOGICAL_REASONING = [
    {
        "prompt": "How is the heart similar to a pump?",
        "completion": "Both move fluid through a system. The heart pumps blood through blood vessels, just as a pump moves water through pipes. Both use pressure to circulate fluid in one direction.",
        "category": "reasoning",
        "type": "analogical"
    },
    {
        "prompt": "How is the brain similar to a computer?",
        "completion": "Both process information and store memories. The brain uses neurons and synapses like a computer uses circuits and memory. Both receive input, process it, and produce output.",
        "category": "reasoning",
        "type": "analogical"
    },
    {
        "prompt": "How is DNA similar to a blueprint?",
        "completion": "Both contain instructions for building something. DNA contains genetic instructions for building organisms, just as blueprints contain specifications for building structures.",
        "category": "reasoning",
        "type": "analogical"
    },
    {
        "prompt": "How is the immune system similar to an army?",
        "completion": "Both defend against invaders. The immune system identifies and destroys pathogens like an army identifies and fights threats. Both have specialized units for different threats.",
        "category": "reasoning",
        "type": "analogical"
    },
    {
        "prompt": "How is a cell membrane similar to a security gate?",
        "completion": "Both control what enters and exits. The cell membrane selectively allows molecules through like a security gate checks who enters. Both protect what's inside from unwanted elements.",
        "category": "reasoning",
        "type": "analogical"
    },
    {
        "prompt": "How is the Earth's crust similar to an eggshell?",
        "completion": "Both are thin, hard outer layers protecting what's inside. The Earth's crust is a thin rocky layer over the mantle, like an eggshell protects the egg's contents.",
        "category": "reasoning",
        "type": "analogical"
    },
    {
        "prompt": "How is a river delta similar to a tree's roots?",
        "completion": "Both branch out into smaller parts. A river splits into smaller channels at a delta, like tree roots branch into smaller roots. Both spread out to cover more area.",
        "category": "reasoning",
        "type": "analogical"
    },
    {
        "prompt": "How is the ozone layer similar to sunscreen?",
        "completion": "Both block harmful radiation. The ozone layer absorbs UV radiation from the Sun, like sunscreen blocks UV rays from reaching your skin. Both protect living things from damage.",
        "category": "reasoning",
        "type": "analogical"
    },
    {
        "prompt": "How is a thermostat similar to a traffic light?",
        "completion": "Both regulate flow based on conditions. A thermostat controls heating/cooling based on temperature, like traffic lights control vehicle flow based on traffic conditions.",
        "category": "reasoning",
        "type": "analogical"
    },
    {
        "prompt": "How is photosynthesis similar to a solar panel?",
        "completion": "Both convert light energy into usable energy. Photosynthesis converts sunlight into chemical energy (glucose), like solar panels convert sunlight into electrical energy.",
        "category": "reasoning",
        "type": "analogical"
    },
]

def main():
    # Load existing training data
    input_path = Path("sov_all_training_data.json")
    if not input_path.exists():
        print(f"ERROR: {input_path} not found")
        return
    
    with open(input_path) as f:
        existing_data = json.load(f)
    
    print(f"Loaded {len(existing_data)} existing training examples")
    
    # Count existing reasoning examples
    existing_reasoning = [d for d in existing_data if d['category'] == 'reasoning']
    print(f"Existing reasoning examples: {len(existing_reasoning)}")
    
    # Combine all new examples
    new_examples = (
        ARC_CHALLENGE_EXAMPLES +
        HELLASWAG_EXAMPLES +
        MULTI_STEP_REASONING +
        CAUSAL_REASONING +
        ANALOGICAL_REASONING
    )
    
    print(f"New reasoning examples to add: {len(new_examples)}")
    
    # Combine with existing data
    enhanced_data = existing_data + new_examples
    
    # Count by category
    categories = {}
    for d in enhanced_data:
        cat = d['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\nEnhanced dataset: {len(enhanced_data)} total examples")
    print("Categories:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")
    
    # Save enhanced data
    output_path = Path("sov_all_training_data_enhanced.json")
    with open(output_path, 'w') as f:
        json.dump(enhanced_data, f, indent=2)
    
    print(f"\nSaved to {output_path}")
    
    # Also create JSONL for Kaggle
    jsonl_path = Path("sov_enhanced_training.jsonl")
    with open(jsonl_path, 'w') as f:
        for d in enhanced_data:
            # Format for Mistral instruction tuning
            entry = {
                "instruction": d["prompt"],
                "output": d["completion"],
                "input": ""
            }
            f.write(json.dumps(entry) + "\n")
    
    print(f"Created JSONL for Kaggle: {jsonl_path}")
    
    # Count reasoning by type
    reasoning_types = {}
    for d in new_examples:
        rtype = d.get('type', 'unknown')
        reasoning_types[rtype] = reasoning_types.get(rtype, 0) + 1
    
    print("\nNew reasoning examples by type:")
    for rtype, count in sorted(reasoning_types.items()):
        print(f"  {rtype}: {count}")

if __name__ == "__main__":
    main()
