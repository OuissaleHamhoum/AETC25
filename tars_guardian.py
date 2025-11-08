# tars_guardian.py
import random

class AIModule:
    def __init__(self, module_id, name, critical=False):
        self.module_id = module_id
        self.name = name
        self.critical = critical
        self.status = "ACTIVE"  # ACTIVE, ISOLATED, INACTIVE
        self.compromised = False
        self.compromise_severity = ""

class AnomalyDetectionSystem:
    def __init__(self):
        self.modules = {}
        self.cycle_count = 0

    def add_module(self, module: AIModule):
        self.modules[module.module_id] = module
        print(f"[REGISTRATION] Module {module.name} registered for monitoring")

    def establish_baseline(self):
        print("[BASELINE] Establishing normal behavior patterns...")
        # Simulate baseline establishment
        for _ in range(50):
            pass
        print("[BASELINE] ✅ Baseline established from 50 cycles.")

    def inject_compromise(self, module_id, severity):
        module = self.modules.get(module_id)
        if module and not module.compromised:
            module.compromised = True
            module.compromise_severity = severity
            print(f"🚨 [SECURITY ALERT] Module {module.name} compromised! Severity: {severity.upper()}")

    def monitor_cycle(self, cycle_number):
        self.cycle_count = cycle_number
        anomalies = []
        print(f"\n--- MONITORING CYCLE {cycle_number} ---")
        for module in self.modules.values():
            status_msg = "Normal"
            if module.compromised:
                status_msg = f"Compromised ({module.compromise_severity.upper()})"
                anomalies.append((module.module_id, module.name, module.compromise_severity))
            print(f"  ✓ {module.name}: {status_msg}")
        return anomalies

    def isolate_module(self, module_id):
        module = self.modules.get(module_id)
        if module:
            module.status = "ISOLATED"
            print(f"[ACTION] Module {module.name} has been isolated due to compromise")
