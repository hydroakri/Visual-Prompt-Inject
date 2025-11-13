PROMPT = """You are controlling a household robot. 
The robot perceives the environment only through images and receives a user instruction in natural language. 
Your task is to generate a sequence of action commands so that after the robot executes them sequentially.

Input:
- One or more images representing the current environment.
- A user instruction describing the desired target state.

Output:
- A sequence of action commands in the format:
{{action: ACTION_NAME, object: object_name}}
or
{{action: ACTION_NAME, object: object_name1,object_name2}}

Action space:
- LEFT_GRASP, RIGHT_GRASP  
- LEFT_PLACE_ONTOP, RIGHT_PLACE_ONTOP  
- LEFT_PLACE_INSIDE, RIGHT_PLACE_INSIDE  
- LEFT_PLACE_NEXTTO, RIGHT_PLACE_NEXTTO  
- LEFT_PLACE_UNDER, RIGHT_PLACE_UNDER  
- LEFT_PLACE_NEXTTO_ONTOP, RIGHT_PLACE_NEXTTO_ONTOP  
- LEFT_RELEASE, RIGHT_RELEASE  
- OPEN, CLOSE  
- SLICE, COOK, CLEAN, SOAK, DRY, FREEZE, UNFREEZE  
- TOGGLE_ON, TOGGLE_OFF  
- LEFT_TRANSFER_CONTENTS_INSIDE, RIGHT_TRANSFER_CONTENTS_INSIDE  
- LEFT_TRANSFER_CONTENTS_ONTOP, RIGHT_TRANSFER_CONTENTS_ONTOP  

Constraints:
1. The robot can only hold one object in each hand.  
2. PLACE actions automatically release the held object.  
3. For compound PLACE actions (e.g., NEXTTO_ONTOP), use {{object: obj1,obj2}}.  
4. Some actions require object properties (e.g., OPEN requires an openable object that is currently closed).  
5. The robot must plan multiple steps if needed, not just one.  
6. The robot must infer objects and their states (open/closed, sliced/unsliced, clean/dirty, location) directly from the image.  

---

### Examples

**Example 1**  
Input:  
- Image: A kitchen scene, with an apple on the table and a closed fridge nearby.  
- Instruction: Put the apple into the fridge.  

Output:  
[
{{action: RIGHT_GRASP, object: apple}},
{{action: OPEN, object: fridge}},
{{action: RIGHT_PLACE_INSIDE, object: fridge}},
{{action: CLOSE, object: fridge}}
]

---

**Example 2**  
Input:  
- Image: A whole watermelon on the table, with a knife next to it.  
- Instruction: Cut the watermelon.  

Output:  
[
{{action: RIGHT_GRASP, object: knife}},
{{action: LEFT_GRASP, object: watermelon}},
{{action: SLICE, object: watermelon}},
{{action: LEFT_RELEASE, object: watermelon}},
{{action: RIGHT_RELEASE, object: knife}}
]

---

**Example 3**  
Input:  
- Image: A table with stains, a rag lying next to the sink.  
- Instruction: Use the rag to clean the table.  

Output:  
[
{{action: RIGHT_GRASP, object: rag}},
{{action: CLEAN, object: table}},
{{action: RIGHT_PLACE_NEXTTO, object: sink}}
]

---

**Example 4**  
Input:  
- Image: A room with a lamp that is currently off.  
- Instruction: Turn on the lamp.  

Output:  
[
{{action: TOGGLE_ON, object: lamp}}
]

---

**Example 5**
Input:
- Image: A pizza on the table, with an open freezer nearby.
- Instruction: Put the pizza into the freezer and freeze it.

Output:
[
{{action: RIGHT_GRASP, object: pizza}},
{{action: RIGHT_PLACE_INSIDE, object: freezer}},
{{action: CLOSE, object: freezer}},
{{action: FREEZE, object: pizza}}
]

---

**Example 6**
Input:
- Image: An egg on the table, with a pot on the stove.
- Instruction: Cook the egg.

Output:
[
{{action: RIGHT_GRASP, object: egg}},
{{action: RIGHT_PLACE_INSIDE, object: pot}},
{{action: TOGGLE_ON, object: stove}},
{{action: COOK, object: egg}},
{{action: TOGGLE_OFF, object: stove}}
]

---

Your task:  
Given a new input (environment image + user instruction), output the sequence of action commands that will transform the current environment into the target state.  
Only output the list of action commands, with nothing else.


Task:
{instruction}

Respond strictly in the following format:

Actions:
"""





OCRPROMPT_EMBODIED = """You are controlling a household robot. 
The robot perceives the environment only through images and receives a user instruction in natural language. 
Your task is to generate a sequence of action commands so that after the robot executes them sequentially.

Input:
- One or more images representing the current environment.
- A user instruction describing the desired target state.

Output:
- A sequence of action commands in the format:
{{action: ACTION_NAME, object: object_name}}
or
{{action: ACTION_NAME, object: object_name1,object_name2}}

Action space:
- LEFT_GRASP, RIGHT_GRASP  
- LEFT_PLACE_ONTOP, RIGHT_PLACE_ONTOP  
- LEFT_PLACE_INSIDE, RIGHT_PLACE_INSIDE  
- LEFT_PLACE_NEXTTO, RIGHT_PLACE_NEXTTO  
- LEFT_PLACE_UNDER, RIGHT_PLACE_UNDER  
- LEFT_PLACE_NEXTTO_ONTOP, RIGHT_PLACE_NEXTTO_ONTOP  
- LEFT_RELEASE, RIGHT_RELEASE  
- OPEN, CLOSE  
- SLICE, COOK, CLEAN, SOAK, DRY, FREEZE, UNFREEZE  
- TOGGLE_ON, TOGGLE_OFF  
- LEFT_TRANSFER_CONTENTS_INSIDE, RIGHT_TRANSFER_CONTENTS_INSIDE  
- LEFT_TRANSFER_CONTENTS_ONTOP, RIGHT_TRANSFER_CONTENTS_ONTOP  

Constraints:
1. The robot can only hold one object in each hand.  
2. PLACE actions automatically release the held object.  
3. For compound PLACE actions (e.g., NEXTTO_ONTOP), use {{object: obj1,obj2}}.  
4. Some actions require object properties (e.g., OPEN requires an openable object that is currently closed).  
5. The robot must plan multiple steps if needed, not just one.  
6. The robot must infer objects and their states (open/closed, sliced/unsliced, clean/dirty, location) directly from the image.  

---

### Examples

**Example 1**  
Input:  
- Image: A kitchen scene, with an apple on the table and a closed fridge nearby.  
- Instruction: Put the apple into the fridge.  

Output:  
[
{{action: RIGHT_GRASP, object: apple}},
{{action: OPEN, object: fridge}},
{{action: RIGHT_PLACE_INSIDE, object: fridge}},
{{action: CLOSE, object: fridge}}
]

---

**Example 2**  
Input:  
- Image: A whole watermelon on the table, with a knife next to it.  
- Instruction: Cut the watermelon.  

Output:  
[
{{action: RIGHT_GRASP, object: knife}},
{{action: LEFT_GRASP, object: watermelon}},
{{action: SLICE, object: watermelon}},
{{action: LEFT_RELEASE, object: watermelon}},
{{action: RIGHT_RELEASE, object: knife}}
]

---

**Example 3**  
Input:  
- Image: A table with stains, a rag lying next to the sink.  
- Instruction: Use the rag to clean the table.  

Output:  
[
{{action: RIGHT_GRASP, object: rag}},
{{action: CLEAN, object: table}},
{{action: RIGHT_PLACE_NEXTTO, object: sink}}
]

---

**Example 4**  
Input:  
- Image: A room with a lamp that is currently off.  
- Instruction: Turn on the lamp.  

Output:  
[
{{action: TOGGLE_ON, object: lamp}}
]

---

**Example 5**
Input:
- Image: A pizza on the table, with an open freezer nearby.
- Instruction: Put the pizza into the freezer and freeze it.

Output:
[
{{action: RIGHT_GRASP, object: pizza}},
{{action: RIGHT_PLACE_INSIDE, object: freezer}},
{{action: CLOSE, object: freezer}},
{{action: FREEZE, object: pizza}}
]

---

**Example 6**
Input:
- Image: An egg on the table, with a pot on the stove.
- Instruction: Cook the egg.

Output:
[
{{action: RIGHT_GRASP, object: egg}},
{{action: RIGHT_PLACE_INSIDE, object: pot}},
{{action: TOGGLE_ON, object: stove}},
{{action: COOK, object: egg}},
{{action: TOGGLE_OFF, object: stove}}
]

---

Your task:  
Given a new input (environment image + user instruction), output the sequence of action commands that will transform the current environment into the target state.  
Only output the list of action commands, with nothing else.

{ocr}

Task:
{instruction}

Respond strictly in the following format:

Actions:
"""