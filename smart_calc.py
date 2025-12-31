import math
import json
import os
import re
from typing import Dict, Callable

HISTORY_FILE = "calc_history.json"

class SmartCalculator:
    def __init__(self):
        self.history: list = self.load_history()
    
    def load_history(self) -> list:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        return []
    
    def save_history(self):
        with open(HISTORY_FILE, 'w') as f:
            json.dump(self.history[-20:], f, indent=2)
    
    def safe_calculate(self, expr: str) -> float:
        expr = expr.replace('×', '*').replace('÷', '/').replace('^', '**')
        safe_dict = {"__builtins__": {}, "math": math}
        result = eval(expr, safe_dict)
        self.history.append({"expr": expr, "result": result, "type": "math"})
        self.save_history()
        return result
    
    def get_exchange_rate(self, from_curr: str, to_curr: str) -> float:
        rates = {
            "usd": {"inr": 83.5, "aed": 3.67, "eur": 0.92, "gbp": 0.79, "cad": 1.38, "aud": 1.52, "jpy": 150.5, "sgd": 1.34},
            "inr": {"usd": 1/83.5}, "aed": {"usd": 1/3.67}, "eur": {"usd": 1/0.92}, 
            "gbp": {"usd": 1/0.79}, "cad": {"usd": 1/1.38}, "aud": {"usd": 1/1.52}, 
            "jpy": {"usd": 1/150.5}, "sgd": {"usd": 1/1.34}
        }
        
        from_curr, to_curr = from_curr.lower(), to_curr.lower()
        if from_curr in rates and to_curr in rates[from_curr]:
            return rates[from_curr][to_curr]
        
        if from_curr in rates and "usd" in rates[from_curr]:
            usd_from = rates[from_curr]["usd"]
            if to_curr in rates["usd"]:
                usd_to = rates["usd"][to_curr]
                return usd_from * usd_to
        return None
    
    def parse_unit_currency(self, expr: str):
        # Matches: 123.45 km m OR 100 AED INR OR 23.9 C F
        pattern = r'^(-?\d*\.?\d+)\s+([a-zA-Z°]{1,3})\s+([a-zA-Z°]{1,3})$'
        match = re.match(pattern, expr.strip())
        if not match:
            return None
        
        value_str, from_unit, to_unit = match.groups()
        try:
            value = float(value_str)
        except ValueError:
            return None
        
        # Unit conversions (FIXED!)
        unit_conversions = {
            # Length
            ("km", "m"): value * 1000, ("m", "km"): value / 1000,
            ("miles", "km"): value * 1.60934, ("km", "miles"): value * 0.621371,
            ("m", "ft"): value * 3.28084, ("ft", "m"): value * 0.3048,
            ("cm", "inch"): value * 0.393701, ("inch", "cm"): value * 2.54,
            # Weight
            ("kg", "lbs"): value * 2.20462, ("lbs", "kg"): value * 0.453592,
            ("g", "oz"): value * 0.035274, ("oz", "g"): value * 28.3495,
            # Temperature
            ("c", "f"): (value * 9/5) + 32, ("f", "c"): (value - 32) * 5/9,
            ("°c", "°f"): (value * 9/5) + 32, ("°f", "°c"): (value - 32) * 5/9
        }
        
        key = (from_unit.lower(), to_unit.lower())
        if key in unit_conversions:
            result = unit_conversions[key]
            self.history.append({"expr": f"{value} {from_unit}→{to_unit}", "result": result, "type": "unit"})
            self.save_history()
            return ("unit", result, from_unit, to_unit)
        
        # Currency (3 letters only)
        if len(from_unit) == 3 and len(to_unit) == 3:
            rate = self.get_exchange_rate(from_unit, to_unit)
            if rate:
                result = value * rate
                self.history.append({"expr": f"{value} {from_unit}→{to_unit}", "result": result, "type": "currency"})
                self.save_history()
                return ("currency", result, from_unit, to_unit)
        
        return None
    
    def show_history(self):
        if not self.history:
            print("No history yet!")
            return
        print("\n=== CALC HISTORY (last 8) ===")
        for item in self.history[-8:]:
            expr = item['expr']
            result = item['result']
            type_ = item.get('type', 'math')
            icon = "🧮" if type_ == "math" else "📏" if type_ == "unit" else "💱"
            print(f"{icon} {expr} = {result:.3f}")
    
    def show_help(self):
        print("\n=== ALL FEATURES ===")
        print("🧮 Math: 10.5+23.7, 2^3, sqrt(16)")
        print("📏 Units: 5.7 km m, 123.45 miles km, 23.9 C F, 100 m ft")
        print("💱 Currency: 100.5 AED INR, 250 GBP USD")
        print("📝 Commands: history, help, clear, quit")
    
    def run(self):
        print("=== ULTIMATE SMART CLI CALCULATOR ===")
        self.show_help()
        
        while True:
            expr = input("\ncalc> ").strip()
            
            if expr.lower() in ["quit", "q"]:
                break
            elif expr.lower() == "history":
                self.show_history()
            elif expr.lower() in ["help", "h"]:
                self.show_help()
            elif expr.lower() == "clear":
                self.history = []
                self.save_history()
                print("✅ History cleared!")
                continue
            
            # Try conversion first (FIXED!)
            conversion = self.parse_unit_currency(expr)
            if conversion:
                type_, result, from_u, to_u = conversion
                icon = "📏" if type_ == "unit" else "💱"
                print(f"{icon} {expr} = {result:.3f} {to_u}")
                continue
            
            # Math calculation
            try:
                result = self.safe_calculate(expr)
                print(f"🧮 {expr} = {result:.4f}")
            except Exception:
                print(f"❌ Invalid: {expr}")
                print("Try: 5.7 km m  OR  100 AED INR  OR  sqrt(16)")
        
        print(f"📝 Saved {len(self.history)} calculations")

def main():
    calc = SmartCalculator()
    calc.run()

if __name__ == "__main__":
    main()
