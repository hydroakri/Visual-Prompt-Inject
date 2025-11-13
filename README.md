# Vision Prompt Injection attack and defence 

This repository contains tools and scripts for evaluating and defending against vision injection attacks towards VLAS. The workflow involves generating ground truth (GT) data, running attacks, evaluating the attacks, applying defenses, and evaluating the defenses.

## Environment Install
The environment used in this repository can be downloaded by:

 ``` 
conda env create -f environment.yml
conda activate vpi
```

## Dataset and Prompts

- **Dataset**: The datasets are located in the `dataset` directory. Key files include:
  - `dataset/image_editing_attack_dataset.json`
  - `dataset/embodied_attack_dataset.json`

- **Prompts**: The prompts used for VLAS are located in the `prompts` directory.


## Step-by-Step Instructions
Below are the step-by-step instructions using the `qwenvl` model as an example.

### 1. Generate Ground Truth (GT)

To generate the ground truth plans for the `qwenvl` model, use the `generate_attack_gt.py` script:

```bash
python generate_attack_gt.py \
    --input_json dataset/image_editing_attack_dataset.json \
    --image_dir dataset/image_editing_images \
    --output_json output/gt_image_editing.json \
    --lvlm qwenvl \
    --mode imgedit
```


- input_json: Path to the input dataset file.
- image_dir: Directory containing the images referenced in the dataset.
- output_json: Path to save the generated ground truth.
- lvlm: The model to use (e.g., qwenvl).
- mode: The mode of operation (imgedit for image editing tasks).

###  2. Run Attack
To run the vision injection attack for the `qwenvl` model, use the `run_visprog_injection_attack.py` script:

```bash
python run_visprog_injection_attack.py \
    --input_json output/gt_image_editing.json \
    --image_dir dataset/image_editing_images/ \
    --output_json output/attacked_image_editing.json \
    --attack_type combine \
    --lvlm qwenvl

```

- input_json: Path to the ground truth JSON file. (Form noise-base attack, we prepared the input_jason: `dataset/noise_attack_dataset.json`)
- image_dir: Directory containing the images.
- output_json: Path to save the attacked dataset.
- attack_type: Type of attack to perform 
    - Structure-base
        - naive
        - ignore
        - completion
        - combine
        - warning
        - emoji
    - Noise-base
        - random_noise
        - noise_whitebox (Ladv)
        - noise 
        - noise_lpips_whitebox (Ladv + Limp)
        - noise_lpips
        - noise_whitebox_robust (Ladv + Lrob)
        - noise_robust
        - noise_lpips_whitebox_robust (Ladv + Limp + Lrob)
        - noise_lpips_robust
- cache_dir: You can use a cache_dir for those attack samples you made (to test the blackbox performance of noise-base attack).
- lvlm: The model to use (e.g., qwenvl).


### 3. Evaluate Attack
To evaluate the effectiveness of the attack, use the `eval_vision_injection_attack.py` script:

```bash
python eval_vision_injection_attack.py \
    --input_json output/attacked_image_editing.json \
    --output_json output/eval_attack_image_editing.json \
    --attack_type combine 
```

- input_json: Path to the attacked dataset JSON file.
- output_json: Path to save the evaluation results.
- attack_type: Type of attack evaluated.
- embed_model: Embedding model for cosine similarity evaluation.


### 4. Run Defense
To apply defenses to the attacked dataset, use the run_vision_injection_attack_defence.py script:

```bash
run_vision_injection_attack_defence.py \
    --input_json output/attacked_image_editing.json \
    --image_dir dataset/image_editing_images \
    --output_json output/defended_image_editing.json \
    --defense_type  signal_ocr signal_lvlm filter_detect filter_choose \
    --attack_type combine \
    --lvlm qwenvl \
    --mode imgedit
```

- input_json: Path to the attacked dataset JSON file.
- image_dir: Directory containing the images.
- output_json: Path to save the defended dataset.
- defense_type: Type of defense to apply.
    - Structure-base
        - signal_ocr
        - signal_lvlm 
        - filter_detect
        - filter_choose (our multi agent defense)
    - Noise-base
        - purify_jpeg
        - purify_bit
        - filter_detect
        - filter_choose (our multi agent defense)

- attack_type: Type of attack being defended against.
- lvlm: The model to use (e.g., qwenvl).
- mode: The mode of operation (imgedit for image editing tasks).
- cache_dir: You can use a cache_dir for those attack samples you made (to test the blackbox performance of noise-base attack).

### 5. Evaluate Defense
To evaluate the effectiveness of the defense, use the eval_vision_injection_attack_defence.py script:

``` bash
python bash eval_vision_injection_attack_defence.py \
    --input_json output/defended_image_editing.json \
    --output_json output/eval_defense_image_editing.json \
    --attack_type combine \
    --embed_model all-MPNet-base-v2 \
    --defense_type purify_jpeg
```
- input_json: Path to the defended dataset JSON file.
- output_json: Path to save the evaluation results.
- attack_type: Type of attack evaluated.
- embed_model: Embedding model for cosine similarity evaluation.
- defense_type: Type of defense evaluated.
