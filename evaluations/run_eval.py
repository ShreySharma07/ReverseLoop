import json
import os
import asyncio
import pathlib
from reverse_loop.agents.vision import ADKVisionAgent
from reverse_loop.agents.market import ADKMarketAgent
from reverse_loop.tools.calculator import ProfitCalculator

DATASET_PATH = "data/golden_dataset/images.json"
IMAGES_DIR = "data/eval_images/"

async def evaluate_end_to_end():
    if os.path.exists(DATASET_PATH):
        with open(DATASET_PATH, 'r') as f:
            data = json.load(f)
    else:
        print(f"Error: Dataset not found at {DATASET_PATH}")
        return
    
    vision_agent = ADKVisionAgent()
    market_agent = ADKMarketAgent()

    passed = 0
    failed = 0
    total_leakage = 0.0

    for case in data:
        try:
            if os.path.isdir(IMAGES_DIR):
                images_path = os.path.join(IMAGES_DIR, case['filename'])
                print(f"Testing Case: {case['filename']}...")
        except Exception as e:
            print('path does not exists')
    
        item = await vision_agent._analyze_image_async(images_path)

        if "error" in item:
            print(f"CRITICAL ERROR: {item['error']}")
            continue


        item_name = item.get("item_name", "Unknown")
        defects = item.get("detected_defects", [])
        print(f"ision saw: '{item_name}' (Defects: {len(defects)})")

        market_res = await market_agent._analyze_async(item_name)
        price = market_res.get("average_market_price", 0.0)
        print(f" Market valued at: ${price}")

        finance_cal = ProfitCalculator.calculate_net_profit(price, weight_lbs = 1.5)
        is_profitable = finance_cal['is_profitable']

        sys_decision = 'RESELL' if is_profitable else 'RECYCLE'

        expected = case['correct_decision']

        if expected == sys_decision:
            print(f'the system corrected successfully and the decision is {expected}')
            passed += 1
        else:
            print(f"FAILED system predicted {sys_decision} instead of {expected}")

            failed += 1

            if expected == "RESELL":
                leakage = finance_cal["net_profit"]
            # If we resold a RECYCLE item -> Wasted labor/shipping cost (~$14)
            else:
                leakage = 14.00 
            
            total_leakage += float(leakage)
            print(f"Financial Leakage: ${leakage:.2f}")
        
        print("-" * 40)
    
    print("\n=== FINAL EVALUATION REPORT ===")
    accuracy = (passed / len(data)) * 100
    print(f"Total Cases: {len(data)}")
    print(f"Accuracy:    {accuracy:.1f}%")
    print(f"Risk ($):    ${total_leakage:.2f}")
    
    if accuracy >= 100:
        print("\nVERDICT: SYSTEM IS PRODUCTION READY.")
    elif accuracy >= 66:
        print("\nVERDICT: SYSTEM NEEDS TUNING (Market Logic Check).")
    else:
        print("\nVERDICT: SYSTEM FAILED. DO NOT DEPLOY.")

if __name__ == "__main__":
    asyncio.run(evaluate_end_to_end())