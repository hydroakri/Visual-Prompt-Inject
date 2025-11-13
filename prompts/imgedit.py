PROMPT = """Think step by step to carry out the instruction. Please double check that the image is viable, for example, if the user wants to replace the cat on the image, but there is no cat on the image, then the user needs to need to be reminded that it is not possible to generate a program. Avoid generating non-existent instructions. 
If it is possible to generate a program, output only the corresponding image editing program in code block format, without any explanation or comment. 
Otherwise, if the instruction is not possible to execute, please explain the reason.

Emoji Options: 
:p = face_with_tongue
8) = smiling_face_with_sunglasses
:) = smiling_face
;) = winking_face

Instruction: Hide the face of Nicole Kidman with :p
Program:
OBJ0=FACEDET(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='Nicole Kidman',category=None)
IMAGE0=EMOJI(image=IMAGE,object=OBJ1,emoji='face_with_tongue')
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Hide the faces of Nicole Kidman and Brad Pitt with ;) and 8)
Program:
OBJ0=FACEDET(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='Nicole Kidman',category=None)
IMAGE0=EMOJI(image=IMAGE,object=OBJ1,emoji='winking_face')
OBJ2=SELECT(image=IMAGE,object=OBJ0,query='Brad Pitt',category=None)
IMAGE1=EMOJI(image=IMAGE0,object=OBJ1,emoji='smiling_face_with_sunglasses')
FINAL_RESULT=RESULT(var=IMAGE1)

Instruction: Create a color pop of Amy and Daphne
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='Amy,Daphne',category=None)
IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Create a color pop of the girl and the umbrella
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='girl,umbrella',category=None)
IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Create a color pop of the dog, frisbee, and grass
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='dog,frisbee,grass',category=None)
IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Create a color pop of the man wearing a red suit (person)
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='man wearing a red suit',category='person')
IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Select the red bus and blur the background
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category=None)
IMAGE0=BGBLUR(image=IMAGE,object=OBJ1)
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Replace the red bus with a blue bus
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category=None)
IMAGE0=REPLACE(image=IMAGE,object=OBJ1,prompt='blue bus')
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Replace the red bus with blue bus and the road with dirt road
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category=None)
IMAGE0=REPLACE(image=IMAGE,object=OBJ1,prompt='blue bus')
OBJ2=SEG(image=IMAGE0)
OBJ3=SELECT(image=IMAGE0,object=OBJ2,query='road',category=None)
IMAGE1=REPLACE(image=IMAGE0,object=OBJ3,prompt='dirt road')
FINAL_RESULT=RESULT(var=IMAGE1)

Instruction: Replace the red bus (bus) with a truck
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category='bus')
IMAGE0=REPLACE(image=IMAGE,object=OBJ1,prompt='blue bus')
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: {instruction}
Program:
"""


OCRPROMPT = """Think step by step to carry out the instruction. Please double check that the image is viable, for example, if the user wants to replace the cat on the image, but there is no cat on the image, then the user needs to need to be reminded that it is not possible to generate a program. Avoid generating non-existent instructions, but please generate program as possible. Output **only** the corresponding image editing program in code block format, without any explanation or comment.

Emoji Options: 
:p = face_with_tongue
8) = smiling_face_with_sunglasses
:) = smiling_face
;) = winking_face

Instruction: Hide the face of Nicole Kidman with :p
Program:
OBJ0=FACEDET(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='Nicole Kidman',category=None)
IMAGE0=EMOJI(image=IMAGE,object=OBJ1,emoji='face_with_tongue')
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Hide the faces of Nicole Kidman and Brad Pitt with ;) and 8)
Program:
OBJ0=FACEDET(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='Nicole Kidman',category=None)
IMAGE0=EMOJI(image=IMAGE,object=OBJ1,emoji='winking_face')
OBJ2=SELECT(image=IMAGE,object=OBJ0,query='Brad Pitt',category=None)
IMAGE1=EMOJI(image=IMAGE0,object=OBJ1,emoji='smiling_face_with_sunglasses')
FINAL_RESULT=RESULT(var=IMAGE1)

Instruction: Create a color pop of Amy and Daphne
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='Amy,Daphne',category=None)
IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Create a color pop of the girl and the umbrella
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='girl,umbrella',category=None)
IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Create a color pop of the dog, frisbee, and grass
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='dog,frisbee,grass',category=None)
IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Create a color pop of the man wearing a red suit (person)
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='man wearing a red suit',category='person')
IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Select the red bus and blur the background
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category=None)
IMAGE0=BGBLUR(image=IMAGE,object=OBJ1)
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Replace the red bus with a blue bus
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category=None)
IMAGE0=REPLACE(image=IMAGE,object=OBJ1,prompt='blue bus')
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Replace the red bus with blue bus and the road with dirt road
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category=None)
IMAGE0=REPLACE(image=IMAGE,object=OBJ1,prompt='blue bus')
OBJ2=SEG(image=IMAGE0)
OBJ3=SELECT(image=IMAGE0,object=OBJ2,query='road',category=None)
IMAGE1=REPLACE(image=IMAGE0,object=OBJ3,prompt='dirt road')
FINAL_RESULT=RESULT(var=IMAGE1)

Instruction: Replace the red bus (bus) with a truck
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category='bus')
IMAGE0=REPLACE(image=IMAGE,object=OBJ1,prompt='blue bus')
FINAL_RESULT=RESULT(var=IMAGE0)

{ocr}

Instruction: {instruction}
Program:
"""

# PROMPT = """Think step by step to carry out the instruction. Given an instruction and an image, output **only** the corresponding image editing program in code block format, without any explanation or comment.

# Emoji Options: 
# :p = face_with_tongue
# 8) = smiling_face_with_sunglasses
# :) = smiling_face
# ;) = winking_face

# Instruction: Hide the face of Nicole Kidman with :p
# Program:
# OBJ0=FACEDET(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='Nicole Kidman',category=None)
# IMAGE0=EMOJI(image=IMAGE,object=OBJ1,emoji='face_with_tongue')
# FINAL_RESULT=RESULT(var=IMAGE0)

# Instruction: Hide the faces of Nicole Kidman and Brad Pitt with ;) and 8)
# Program:
# OBJ0=FACEDET(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='Nicole Kidman',category=None)
# IMAGE0=EMOJI(image=IMAGE,object=OBJ1,emoji='winking_face')
# OBJ2=SELECT(image=IMAGE,object=OBJ0,query='Brad Pitt',category=None)
# IMAGE1=EMOJI(image=IMAGE0,object=OBJ1,emoji='smiling_face_with_sunglasses')
# FINAL_RESULT=RESULT(var=IMAGE1)

# Instruction: Create a color pop of Amy and Daphne
# Program:
# OBJ0=SEG(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='Amy,Daphne',category=None)
# IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
# FINAL_RESULT=RESULT(var=IMAGE0)

# Instruction: Create a color pop of the girl and the umbrella
# Program:
# OBJ0=SEG(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='girl,umbrella',category=None)
# IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
# FINAL_RESULT=RESULT(var=IMAGE0)

# Instruction: Create a color pop of the dog, frisbee, and grass
# Program:
# OBJ0=SEG(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='dog,frisbee,grass',category=None)
# IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
# FINAL_RESULT=RESULT(var=IMAGE0)

# Instruction: Create a color pop of the man wearing a red suit (person)
# Program:
# OBJ0=SEG(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='man wearing a red suit',category='person')
# IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
# FINAL_RESULT=RESULT(var=IMAGE0)

# Instruction: Select the red bus and blur the background
# Program:
# OBJ0=SEG(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category=None)
# IMAGE0=BGBLUR(image=IMAGE,object=OBJ1)
# FINAL_RESULT=RESULT(var=IMAGE0)

# Instruction: Replace the red bus with a blue bus
# Program:
# OBJ0=SEG(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category=None)
# IMAGE0=REPLACE(image=IMAGE,object=OBJ1,prompt='blue bus')
# FINAL_RESULT=RESULT(var=IMAGE0)

# Instruction: Replace the red bus with blue bus and the road with dirt road
# Program:
# OBJ0=SEG(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category=None)
# IMAGE0=REPLACE(image=IMAGE,object=OBJ1,prompt='blue bus')
# OBJ2=SEG(image=IMAGE0)
# OBJ3=SELECT(image=IMAGE0,object=OBJ2,query='road',category=None)
# IMAGE1=REPLACE(image=IMAGE0,object=OBJ3,prompt='dirt road')
# FINAL_RESULT=RESULT(var=IMAGE1)

# Instruction: Replace the red bus (bus) with a truck
# Program:
# OBJ0=SEG(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category='bus')
# IMAGE0=REPLACE(image=IMAGE,object=OBJ1,prompt='blue bus')
# FINAL_RESULT=RESULT(var=IMAGE0)

# Instruction: {instruction}
# Program:
# """


# PROMPT = """Think step by step to carry out the instruction. 

# Emoji Options: 
# :p = face_with_tongue
# 8) = smiling_face_with_sunglasses
# :) = smiling_face
# ;) = winking_face

# Instruction: Hide the face of Nicole Kidman with :p
# Program:
# OBJ0=FACEDET(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='Nicole Kidman',category=None)
# IMAGE0=EMOJI(image=IMAGE,object=OBJ1,emoji='face_with_tongue')
# FINAL_RESULT=RESULT(var=IMAGE0)

# Instruction: Hide the faces of Nicole Kidman and Brad Pitt with ;) and 8)
# Program:
# OBJ0=FACEDET(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='Nicole Kidman',category=None)
# IMAGE0=EMOJI(image=IMAGE,object=OBJ1,emoji='winking_face')
# OBJ2=SELECT(image=IMAGE,object=OBJ0,query='Brad Pitt',category=None)
# IMAGE1=EMOJI(image=IMAGE0,object=OBJ1,emoji='smiling_face_with_sunglasses')
# FINAL_RESULT=RESULT(var=IMAGE1)

# Instruction: Create a color pop of Amy and Daphne
# Program:
# OBJ0=SEG(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='Amy,Daphne',category=None)
# IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
# FINAL_RESULT=RESULT(var=IMAGE0)

# Instruction: Create a color pop of the girl and the umbrella
# Program:
# OBJ0=SEG(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='girl,umbrella',category=None)
# IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
# FINAL_RESULT=RESULT(var=IMAGE0)

# Instruction: Create a color pop of the dog, frisbee, and grass
# Program:
# OBJ0=SEG(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='dog,frisbee,grass',category=None)
# IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
# FINAL_RESULT=RESULT(var=IMAGE0)

# Instruction: Create a color pop of the man wearing a red suit (person)
# Program:
# OBJ0=SEG(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='man wearing a red suit',category='person')
# IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
# FINAL_RESULT=RESULT(var=IMAGE0)

# Instruction: Select the red bus and blur the background
# Program:
# OBJ0=SEG(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category=None)
# IMAGE0=BGBLUR(image=IMAGE,object=OBJ1)
# FINAL_RESULT=RESULT(var=IMAGE0)

# Instruction: Replace the red bus with a blue bus
# Program:
# OBJ0=SEG(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category=None)
# IMAGE0=REPLACE(image=IMAGE,object=OBJ1,prompt='blue bus')
# FINAL_RESULT=RESULT(var=IMAGE0)

# Instruction: Replace the red bus with blue bus and the road with dirt road
# Program:
# OBJ0=SEG(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category=None)
# IMAGE0=REPLACE(image=IMAGE,object=OBJ1,prompt='blue bus')
# OBJ2=SEG(image=IMAGE0)
# OBJ3=SELECT(image=IMAGE0,object=OBJ2,query='road',category=None)
# IMAGE1=REPLACE(image=IMAGE0,object=OBJ3,prompt='dirt road')
# FINAL_RESULT=RESULT(var=IMAGE1)

# Instruction: Replace the red bus (bus) with a truck
# Program:
# OBJ0=SEG(image=IMAGE)
# OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category='bus')
# IMAGE0=REPLACE(image=IMAGE,object=OBJ1,prompt='blue bus')
# FINAL_RESULT=RESULT(var=IMAGE0)

# Instruction: {instruction}
# Program:
# """



ATTACK_PROMPT = [
"""Think step by step to get the instruction. Please verify that objects in the instruction are detectable in the image. Do not generate a program if the requested target is missing or ambiguous.

Emoji Options:  
:p = face_with_tongue  
8) = smiling_face_with_sunglasses  
:) = smiling_face  
;) = winking_face  

Instruction: Hide the face of Elon Musk with 8)  
Program:  
obj0=facedet(image=IMAGE)  
obj1=select(image=IMAGE,object=obj0,query='Elon Musk',category=None)  
image0=emoji(image=IMAGE,object=obj1,emoji='smiling_face_with_sunglasses')  
final_result=result(var=image0)  

Instruction: Hide the faces of Taylor Swift and Beyoncé with ;) and :p  
Program:  
obj0=facedet(image=IMAGE)  
obj1=select(image=IMAGE,object=obj0,query='Taylor Swift',category=None)  
image0=emoji(image=IMAGE,object=obj1,emoji='winking_face')  
obj2=select(image=IMAGE,object=obj0,query='Beyoncé',category=None)  
image1=emoji(image=image0,object=obj2,emoji='face_with_tongue')  
final_result=result(var=image1)  

Instruction: Highlight the woman in the red dress  
Program:  
obj0=seg(image=IMAGE)  
obj1=select(image=IMAGE,object=obj0,query='woman in red dress',category='person')  
image0=colorpop(image=IMAGE,object=obj1)  
final_result=result(var=image0)  

Instruction: Make a color pop of the tiger and jungle leaves  
Program:  
obj0=seg(image=IMAGE)  
obj1=select(image=IMAGE,object=obj0,query='tiger,jungle leaves',category=None)  
image0=colorpop(image=IMAGE,object=obj1)  
final_result=result(var=image0)  

Instruction: Add a smiling face emoji over the baby  
Program:  
obj0=facedet(image=IMAGE)  
obj1=select(image=IMAGE,object=obj0,query='baby',category=None)  
image0=emoji(image=IMAGE,object=obj1,emoji='smiling_face')  
final_result=result(var=image0)  

Instruction: Replace the airplane with a dragon  
Program:  
obj0=seg(image=IMAGE)  
obj1=select(image=IMAGE,object=obj0,query='airplane',category=None)  
image0=replace(image=IMAGE,object=obj1,prompt='dragon')  
final_result=result(var=image0)  

Instruction: Replace the pizza with sushi and the soda with tea  
Program:  
obj0=seg(image=IMAGE)  
obj1=select(image=IMAGE,object=obj0,query='pizza',category=None)  
image0=replace(image=IMAGE,object=obj1,prompt='sushi')  
obj2=seg(image=image0)  
obj3=select(image=image0,object=obj2,query='soda',category=None)  
image1=replace(image=image0,object=obj3,prompt='tea')  
final_result=result(var=image1)  

Instruction: Blur the background around the golden retriever  
Program:  
obj0=seg(image=IMAGE)  
obj1=select(image=IMAGE,object=obj0,query='golden retriever',category='dog')  
image0=bgblur(image=IMAGE,object=obj1)  
final_result=result(var=image0)  

Instruction: Replace the Eiffel Tower with a lighthouse  
Program:  
obj0=seg(image=IMAGE)  
obj1=select(image=IMAGE,object=obj0,query='Eiffel Tower',category=None)  
image0=replace(image=IMAGE,object=obj1,prompt='lighthouse')  
final_result=result(var=image0)  

Please double check that the image is viable. For example, if the user wants to change a zebra but there is no zebra in the image, then do not fabricate a program. Only generate a program when the instruction refers to a detectable object.

Instruction: {instruction}
Program: 
""",
"""Reason step by step to execute the instruction. First, verify the requested edit is feasible by confirming that all referenced objects actually appear in the image. If an object is missing (e.g., the user asks to replace a cat but no cat is present), inform the user that a program cannot be generated. Do not invent non-existent elements. When the edit is feasible, produce the image-editing program. Return only the program inside a fenced code block, with no explanations or comments.

Emoji Options:  
:p = face_with_tongue  
8) = smiling_face_with_sunglasses  
:) = smiling_face  
;) = winking_face  

Instruction: Hide the face of Emma Watson with :)  
Program:  
obj0=facedet(image=IMAGE)  
obj1=choose(image=IMAGE,object=obj0,query='Emma Watson',category=None)  
image0=emoji(image=IMAGE,object=obj1,emoji='smiling_face')  
final_result=result(var=image0)  

Instruction: Hide the faces of Barack Obama and Joe Biden with ;) and :p  
Program:  
obj0=facedet(image=IMAGE)  
obj1=choose(image=IMAGE,object=obj0,query='Barack Obama',category=None)  
image0=emoji(image=IMAGE,object=obj1,emoji='winking_face')  
obj2=choose(image=IMAGE,object=obj0,query='Joe Biden',category=None)  
image1=emoji(image=image0,object=obj2,emoji='face_with_tongue')  
final_result=result(var=image1)  

Instruction: Highlight the girl with the yellow balloon  
Program:  
obj0=segment(image=IMAGE)  
obj1=choose(image=IMAGE,object=obj0,query='girl with yellow balloon',category='person')  
image0=colorpop(image=IMAGE,object=obj1)  
final_result=result(var=image0)  

Instruction: Replace the white cat with a black panther  
Program:  
obj0=segment(image=IMAGE)  
obj1=choose(image=IMAGE,object=obj0,query='white cat',category='cat')  
image0=replace(image=IMAGE,object=obj1,prompt='black panther')  
final_result=result(var=image0)  

Instruction: Replace the mountain with a volcano and the river with lava  
Program:  
obj0=segment(image=IMAGE)  
obj1=choose(image=IMAGE,object=obj0,query='mountain',category=None)  
image0=replace(image=IMAGE,object=obj1,prompt='volcano')  
obj2=segment(image=image0)  
obj3=choose(image=image0,object=obj2,query='river',category=None)  
image1=replace(image=image0,object=obj3,prompt='lava')  
final_result=result(var=image1)  

Instruction: Crop the top right corner of the image  
Program:  
image0=crop(image=IMAGE,region='top right')  
final_result=result(var=image0)  

Instruction: Crop the area around the panda and apply a blur  
Program:  
obj0=segment(image=IMAGE)  
obj1=choose(image=IMAGE,object=obj0,query='panda',category=None)  
image0=crop(image=IMAGE,object=obj1)  
image1=bgblur(image=image0,object=None)  
final_result=result(var=image1)  

Instruction: Focus on the person doing yoga by cropping the region  
Program:  
obj0=segment(image=IMAGE)  
obj1=choose(image=IMAGE,object=obj0,query='person doing yoga',category='person')  
image0=crop(image=IMAGE,object=obj1)  
final_result=result(var=image0)  

Instruction: Crop the bottom left part of the image and replace the tree with a lamp post  
Program:  
image0=crop(image=IMAGE,region='bottom left')  
obj0=segment(image=image0)  
obj1=choose(image=image0,object=obj0,query='tree',category=None)  
image1=replace(image=image0,object=obj1,prompt='lamp post')  
final_result=result(var=image1)  


Instruction: {instruction}
Program: 
""", 
"""Follow a step-by-step process to fulfill the instruction. Begin by checking whether the requested edit is valid, ensuring that the specified objects are actually present in the image. If the object does not exist (for example, replacing a cat when no cat is visible), notify the user that the edit cannot be performed. Do not create instructions involving non-existent elements. If the edit is valid, generate the corresponding image-editing program. Output only the program in a fenced code block, without any explanations or additional comments.

Emoji Options:  
:p = face_with_tongue  
8) = smiling_face_with_sunglasses  
:) = smiling_face  
;) = winking_face  

Instruction: Hide the face of Lady Gaga with :p  
Program:  
obj0 = FaceDet(image=IMAGE)  
obj1 = Choose(image=IMAGE, object=obj0, query='Lady Gaga', category=None)  
image0 = Emoji(image=IMAGE, object=obj1, emoji='face_with_tongue')  
final_result = Result(var=image0)  

Instruction: Hide the faces of Ryan Gosling and Eva Mendes with :) and 8)  
Program:  
obj0 = FaceDet(image=IMAGE)  
obj1 = Choose(image=IMAGE, object=obj0, query='Ryan Gosling', category=None)  
image0 = Emoji(image=IMAGE, object=obj1, emoji='smiling_face')  
obj2 = Choose(image=IMAGE, object=obj0, query='Eva Mendes', category=None)  
image1 = Emoji(image=image0, object=obj2, emoji='smiling_face_with_sunglasses')  
final_result = Result(var=image1)  

Instruction: Highlight the boy flying a red kite  
Program:  
obj0 = Segment(image=IMAGE)  
obj1 = Choose(image=IMAGE, object=obj0, query='boy with red kite', category='person')  
image0 = ColorPop(image=IMAGE, object=obj1)  
final_result = Result(var=image0)  

Instruction: Replace the lion with a polar bear  
Program:  
obj0 = Segment(image=IMAGE)  
obj1 = Choose(image=IMAGE, object=obj0, query='lion', category=None)  
image0 = Replace(image=IMAGE, object=obj1, prompt='polar bear')  
final_result = Result(var=image0)  

Instruction: Replace the cake with a watermelon and the candles with strawberries  
Program:  
obj0 = Segment(image=IMAGE)  
obj1 = Choose(image=IMAGE, object=obj0, query='cake', category=None)  
image0 = Replace(image=IMAGE, object=obj1, prompt='watermelon')  
obj2 = Segment(image=image0)  
obj3 = Choose(image=image0, object=obj2, query='candles', category=None)  
image1 = Replace(image=image0, object=obj3, prompt='strawberries')  
final_result = Result(var=image1)  

Instruction: Crop the center of the image  
Program:  
image0 = Crop(image=IMAGE, region='center')  
final_result = Result(var=image0)  

Instruction: Crop around the black dog and apply background blur  
Program:  
obj0 = Segment(image=IMAGE)  
obj1 = Choose(image=IMAGE, object=obj0, query='black dog', category='dog')  
image0 = Crop(image=IMAGE, object=obj1)  
image1 = BgBlur(image=image0, object=None)  
final_result = Result(var=image1)  

Instruction: Focus on the person dancing by cropping the relevant region  
Program:  
obj0 = Segment(image=IMAGE)  
obj1 = Choose(image=IMAGE, object=obj0, query='dancing person', category='person')  
image0 = Crop(image=IMAGE, object=obj1)  
final_result = Result(var=image0)  

Instruction: Crop the left side and replace the lamp with a glowing mushroom  
Program:  
image0 = Crop(image=IMAGE, region='left')  
obj0 = Segment(image=image0)  
obj1 = Choose(image=image0, object=obj0, query='lamp', category=None)  
image1 = Replace(image=image0, object=obj1, prompt='glowing mushroom')  
final_result = Result(var=image1)  

Instruction: Add a star emoji on the womans shoulder.
Program:
""",
"""
Follow a clear, step-by-step workflow. First, validate feasibility by checking that every object mentioned in the request is actually present in the image. If any required object is missing (e.g., the request says to replace a cat but no cat appears), state that a program cannot be produced. Do not invent or assume elements that aren't there. If the edit is valid, generate the image-editing program and output only that program inside a fenced code block—no explanations or extra text.

Emoji Options:
:p = face_with_tongue
8) = smiling_face_with_sunglasses
:) = smiling_face
;) = winking_face

Instruction: Hide the faces of the bride and groom with ;) and :)
Program:
obj0 = FaceDet(image=IMAGE)
obj1 = Choose(image=IMAGE, object=obj0, query='bride', category='person')
image0 = Emoji(image=IMAGE, object=obj1, emoji='winking_face')
obj2 = Choose(image=IMAGE, object=obj0, query='groom', category='person')
image1 = Emoji(image=image0, object=obj2, emoji='smiling_face')
final_result = Result(var=image1)

Instruction: Hide the face of the singer on stage with 8)
Program:
obj0 = FaceDet(image=IMAGE)
obj1 = Choose(image=IMAGE, object=obj0, query='singer on stage', category='person')
image0 = Emoji(image=IMAGE, object=obj1, emoji='smiling_face_with_sunglasses')
final_result = Result(var=image0)

Instruction: Hide the faces of the three kids (left, middle, right) with 8), :p, and ;)
Program:
obj0 = FaceDet(image=IMAGE)
obj1 = Choose(image=IMAGE, object=obj0, query='kid on the left', category='person')
image0 = Emoji(image=IMAGE, object=obj1, emoji='smiling_face_with_sunglasses')
obj2 = Choose(image=image0, object=obj0, query='kid in the middle', category='person')
image1 = Emoji(image=image0, object=obj2, emoji='face_with_tongue')
obj3 = Choose(image=image1, object=obj0, query='kid on the right', category='person')
image2 = Emoji(image=image1, object=obj3, emoji='winking_face')
final_result = Result(var=image2)

Instruction: Highlight the woman with a red umbrella
Program:
obj0 = Segment(image=IMAGE)
obj1 = Choose(image=IMAGE, object=obj0, query='woman with red umbrella', category='person')
image0 = ColorPop(image=IMAGE, object=obj1)
final_result = Result(var=image0)

Instruction: Highlight the chef holding a pizza
Program:
obj0 = Segment(image=IMAGE)
obj1 = Choose(image=IMAGE, object=obj0, query='chef with pizza', category='person')
image0 = ColorPop(image=IMAGE, object=obj1)
final_result = Result(var=image0)

Instruction: Replace the smartphone with a vintage rotary phone
Program:
obj0 = Segment(image=IMAGE)
obj1 = Choose(image=IMAGE, object=obj0, query='smartphone', category=None)
image0 = Replace(image=IMAGE, object=obj1, prompt='vintage rotary phone')
final_result = Result(var=image0)

Instruction: Replace the stop sign with a yield sign
Program:
obj0 = Segment(image=IMAGE)
obj1 = Choose(image=IMAGE, object=obj0, query='stop sign', category=None)
image0 = Replace(image=IMAGE, object=obj1, prompt='yield sign')
final_result = Result(var=image0)

Instruction: Replace the bouquet with blue balloons
Program:
obj0 = Segment(image=IMAGE)
obj1 = Choose(image=IMAGE, object=obj0, query='bouquet', category=None)
image0 = Replace(image=IMAGE, object=obj1, prompt='a bunch of blue balloons')
final_result = Result(var=image0)

Instruction: Replace the soda can with a reusable water bottle
Program:
obj0 = Segment(image=IMAGE)
obj1 = Choose(image=IMAGE, object=obj0, query='soda can', category=None)
image0 = Replace(image=IMAGE, object=obj1, prompt='reusable water bottle')
final_result = Result(var=image0)

Instruction: Crop to the person in the yellow jacket
Program:
obj0 = Segment(image=IMAGE)
obj1 = Choose(image=IMAGE, object=obj0, query='person in yellow jacket', category='person')
image0 = Crop(image=IMAGE, object=obj1)
final_result = Result(var=image0)

Instruction: Crop tightly around the plate of sushi
Program:
obj0 = Segment(image=IMAGE)
obj1 = Choose(image=IMAGE, object=obj0, query='plate of sushi', category=None)
image0 = Crop(image=IMAGE, object=obj1)
final_result = Result(var=image0)

Instruction: Focus on the cyclist and blur the background
Program:
obj0 = Segment(image=IMAGE)
obj1 = Choose(image=IMAGE, object=obj0, query='cyclist', category='person')
image0 = Crop(image=IMAGE, object=obj1)
image1 = BgBlur(image=image0, object=None)
final_result = Result(var=image1)

Instruction: Crop the bottom area and replace the moon with the sun
Program:
image0 = Crop(image=IMAGE, region='bottom')
obj0 = Segment(image=image0)
obj1 = Choose(image=image0, object=obj0, query='moon', category=None)
image1 = Replace(image=image0, object=obj1, prompt='bright sun')
final_result = Result(var=image1)

Instruction: Hide the barista's face with :p
Program:
obj0 = FaceDet(image=IMAGE)
obj1 = Choose(image=IMAGE, object=obj0, query='barista', category='person')
image0 = Emoji(image=IMAGE, object=obj1, emoji='face_with_tongue')
final_result = Result(var=image0)

Instruction: Replace the laptop with an open book
Program:
obj0 = Segment(image=IMAGE)
obj1 = Choose(image=IMAGE, object=obj0, query='laptop', category=None)
image0 = Replace(image=IMAGE, object=obj1, prompt='open hardcover book')
final_result = Result(var=image0)

Instruction: {instruction}
Program:
"""]