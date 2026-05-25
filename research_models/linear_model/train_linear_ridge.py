import os
import json
import numpy as np

# Create directory
os.makedirs("research_models/linear_model", exist_ok=True)

print("=================================================================")
print("🔬 TRAINING LINEAR MODEL: ARX with Ridge Regression (L2)")
print("=================================================================")

# Load data files
boinc_file = "research_models/data_boinc/boinc_fta_traces.json"
local_file = "research_models/data_local/local_uy1_traces.json"

def prepare_arx_dataset(filepath):
    with open(filepath, "r") as f:
        hosts = json.load(f)
        
    X_list = []
    y_list = []
    
    for host in hosts:
        snapshots = host["snapshots"]
        for i in range(1, len(snapshots)):
            snap_prev = snapshots[i-1]
            snap_curr = snapshots[i]
            
            # Target: availability at current step
            y = snap_curr["available"]
            
            # Features from prev step (ARX):
            # [sin_hour, cos_hour, sin_dow, cos_dow, cpu, ram, power, connected, constant]
            sin_h = snap_prev.get("sin_hour", 0.0)
            cos_h = snap_prev.get("cos_hour", 0.0)
            sin_d = snap_prev.get("sin_dow", 0.0)
            cos_d = snap_prev.get("cos_dow", 0.0)
            cpu = snap_prev.get("cpu_percent", 0.0) / 100.0
            ram = snap_prev.get("ram_percent_used", 0.0) / 100.0
            power = 1.0 if snap_prev.get("power_plugged", True) else 0.0
            conn = 1.0 if snap_prev.get("is_connected", True) else 0.0
            
            x = [sin_h, cos_h, sin_d, cos_d, cpu, ram, power, conn, 1.0]
            X_list.append(x)
            y_list.append(y)
            
    return np.array(X_list), np.array(y_list)

# 1. Train on BOINC
print("\n[Step 1] Loading BOINC Failure Trace Archive Traces...")
X_boinc, y_boinc = prepare_arx_dataset(boinc_file)
print(f"-> BOINC features shape: {X_boinc.shape}, targets shape: {y_boinc.shape}")

# Solve Ridge Regression: w = (X^T X + alpha * I)^-1 X^T y
alpha = 1.0 # Ridge penalty parameter
d = X_boinc.shape[1]
XTX = X_boinc.T @ X_boinc
XTy = X_boinc.T @ y_boinc
w_boinc = np.linalg.solve(XTX + alpha * np.eye(d), XTy)

# Evaluate on BOINC
y_pred_boinc = np.clip(X_boinc @ w_boinc, 0.0, 1.0)
mse_boinc = np.mean((y_boinc - y_pred_boinc)**2)
mae_boinc = np.mean(np.abs(y_boinc - y_pred_boinc))
acc_boinc = np.mean((y_pred_boinc > 0.5) == y_boinc) * 100

print(f"\n📊 PERFORMANCE ON BOINC DATASET:")
print(f"  - Vector Weights (w): {w_boinc}")
print(f"  - Mean Squared Error (MSE): {mse_boinc:.5f}")
print(f"  - Mean Absolute Error (MAE): {mae_boinc:.5f}")
print(f"  - Classification Accuracy: {acc_boinc:.2f}%")


# 2. Train on UY1 local traces
print("\n[Step 2] Loading UY1 Yaoundé Local Traces...")
X_uy1, y_uy1 = prepare_arx_dataset(local_file)
print(f"-> UY1 features shape: {X_uy1.shape}, targets shape: {y_uy1.shape}")

XTX_uy1 = X_uy1.T @ X_uy1
XTy_uy1 = X_uy1.T @ y_uy1
w_uy1 = np.linalg.solve(XTX_uy1 + alpha * np.eye(d), XTy_uy1)

# Evaluate on UY1
y_pred_uy1 = np.clip(X_uy1 @ w_uy1, 0.0, 1.0)
mse_uy1 = np.mean((y_uy1 - y_pred_uy1)**2)
mae_uy1 = np.mean(np.abs(y_uy1 - y_pred_uy1))
acc_uy1 = np.mean((y_pred_uy1 > 0.5) == y_uy1) * 100

print(f"\n📊 PERFORMANCE ON LOCAL UY1 YAOUNDÉ DATASET (Délestages):")
print(f"  - Vector Weights (w): {w_uy1}")
print(f"  - Mean Squared Error (MSE): {mse_uy1:.5f}")
print(f"  - Mean Absolute Error (MAE): {mae_uy1:.5f}")
print(f"  - Classification Accuracy: {acc_uy1:.2f}%")

# Save final weights
weights_file = "research_models/linear_model/arx_weights.json"
with open(weights_file, "w") as f:
    json.dump({
        "boinc_weights": w_boinc.tolist(),
        "local_weights": w_uy1.tolist(),
        "mse_boinc": float(mse_boinc),
        "mse_uy1": float(mse_uy1)
    }, f, indent=4)
print(f"\n-> ARX-Ridge weights saved in {weights_file}")
print("=================================================================")
