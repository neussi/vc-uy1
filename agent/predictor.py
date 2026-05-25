import os
import json
import logging
import datetime
import numpy as np

logger = logging.getLogger("VC-Predictor")

WEIGHTS_FILE = "rls_weights.json"
BUFFER_FILE = "sliding_window_72h.json"
MAX_BUFFER_HOURS = 72
MINUTES_IN_72H = MAX_BUFFER_HOURS * 60  # 4320 snapshots at 1-min interval

class FrugalPredictor:
    def __init__(self, feature_dim=11, lambda_coeff=0.995):
        self.d = feature_dim
        self.lambda_ = lambda_coeff
        
        # Initialize RLS states
        self.w = np.zeros(self.d)
        self.P = np.eye(self.d) * 100.0  # P = delta^-1 * I (delta = 0.01)
        
        self.load_weights()
        
    def load_weights(self):
        """Load RLS state from local weights file."""
        if os.path.exists(WEIGHTS_FILE):
            try:
                with open(WEIGHTS_FILE, "r") as f:
                    data = json.load(f)
                    self.w = np.array(data.get("w", self.w.tolist()))
                    self.P = np.array(data.get("P", self.P.tolist()))
                logger.info("RLS weights loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load RLS weights: {e}")

    def save_weights(self):
        """Persist RLS state to local weights file."""
        try:
            with open(WEIGHTS_FILE, "w") as f:
                json.dump({
                    "w": self.w.tolist(),
                    "P": self.P.tolist(),
                    "updated_at": datetime.datetime.utcnow().isoformat()
                }, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save RLS weights: {e}")

    def extract_features(self, snapshot):
        """Extract a standardized 11-dimension ARX feature vector from snapshot."""
        try:
            # Extract features from 18-dim feature array or raw fields
            features = snapshot.get("features", [])
            if len(features) >= 18:
                # Cyclic time dimensions (1-4)
                s_hour, c_hour, s_dow, c_dow = features[0], features[1], features[2], features[3]
            else:
                # Fallback to manual computation
                local_now = datetime.datetime.now()
                s_hour = np.sin(2 * np.pi * local_now.hour / 24.0)
                c_hour = np.cos(2 * np.pi * local_now.hour / 24.0)
                s_dow = np.sin(2 * np.pi * local_now.weekday() / 7.0)
                c_dow = np.cos(2 * np.pi * local_now.weekday() / 7.0)

            cpu_percent = snapshot.get("cpu_percent", 0.0) / 100.0
            ram_percent = snapshot.get("ram_percent_used", 0.0) / 100.0
            power_plugged = 1.0 if snapshot.get("power_plugged", True) else 0.0
            is_connected = 1.0 if snapshot.get("is_connected", True) else 0.0
            idle_score = min(snapshot.get("idle_seconds", 0) / 3600.0, 1.0)
            
            # 11-dimension ARX vector:
            # [sin_hour, cos_hour, sin_dow, cos_dow, cpu, ram, power, connected, idle, constant_bias, interaction_power_cpu]
            x = np.array([
                s_hour, c_hour, s_dow, c_dow,
                cpu_percent, ram_percent,
                power_plugged, is_connected, idle_score,
                1.0,
                power_plugged * cpu_percent
            ])
            return x
        except Exception as e:
            logger.error(f"Feature extraction failed: {e}")
            return np.zeros(self.d)

    def update(self, x, y):
        """Run a recursive RLS step to update weights with exponential forgetting."""
        try:
            # Predict with current weights
            y_pred = np.dot(self.w, x)
            alpha = y - y_pred  # Prediction error
            
            # Kalman gain update: g = Px / (lambda + x^T P x)
            Px = np.dot(self.P, x)
            xPx = np.dot(x, Px)
            g = Px / (self.lambda_ + xPx)
            
            # Covariance matrix update: P = (P - g x^T P) / lambda
            g_xt_P = np.outer(g, np.dot(x, self.P))
            self.P = (self.P - g_xt_P) / self.lambda_
            
            # Weights update: w = w + alpha * g
            self.w = self.w + alpha * g
            
            # Constrain weights to prevent numerical instability
            self.w = np.clip(self.w, -10.0, 10.0)
            
        except Exception as e:
            logger.error(f"RLS update step failed: {e}")

    def predict(self, x):
        """Compute the linear ARX prediction probability [0, 1]."""
        try:
            prob = np.dot(self.w, x)
            return float(np.clip(prob, 0.0, 1.0))
        except Exception as e:
            logger.error(f"Inference failed: {e}")
            return 1.0


class SlidingWindowBuffer:
    def __init__(self):
        self.buffer = []
        self.load_buffer()

    def load_buffer(self):
        """Load history from local JSON file."""
        if os.path.exists(BUFFER_FILE):
            try:
                with open(BUFFER_FILE, "r") as f:
                    self.buffer = json.load(f)
                logger.info(f"Loaded {len(self.buffer)} snapshots in sliding buffer.")
            except:
                pass

    def save_buffer(self):
        """Persist buffer state to local file."""
        try:
            with open(BUFFER_FILE, "w") as f:
                json.dump(self.buffer, f)
        except Exception as e:
            logger.error(f"Failed to write sliding buffer: {e}")

    def append(self, snapshot):
        """Append new snapshot and enforce 72-hour sliding window."""
        self.buffer.append(snapshot)
        if len(self.buffer) > MINUTES_IN_72H:
            self.buffer = self.buffer[-MINUTES_IN_72H:]
        self.save_buffer()

    def get_all(self):
        return self.buffer
