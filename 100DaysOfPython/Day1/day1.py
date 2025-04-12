#1. Mix 500g of Flour, 10g Yeast and 300ml Water in a bowl.
#2. Knead the dough for 10 minutes.
#3. Add 3g of Salt.
#4. Leave to rise for 2 hours.
#5. Bake at 200 degrees C for 30 minutes.

steps = [
    "Mix 500g of Flour, 10g Yeast and 300ml Water in a bowl.",
    "Knead the dough for 10 minutes.",
    "Add 3g of Salt.",
    "Leave to rise for 2 hours.",
    "Bake at 200 degrees C for 30 minutes."
]

for step_number, step in enumerate(steps, start=0) :
    print("{step_number}. {step}".format(step_number=step_number+1, step=step))