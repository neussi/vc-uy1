import unittest
import requests
import time
from agent import collector, heartbeat, syncer

class TestVCAgent(unittest.TestCase):
    def test_machine_id_generation(self):
        mid = collector.get_machine_id()
        self.assertEqual(len(mid), 64) # SHA-256
        
    def test_stats_collection(self):
        stats = collector.get_stats()
        self.assertIn('cpu_percent', stats)
        self.assertIn('ram_percent_used', stats)
        
    def test_heartbeat_logic(self):
        heartbeat.write_heartbeat(shutdown_clean=True)
        status = heartbeat.detect_power_cut()
        self.assertEqual(status['type'], 'clean')

class TestVCServer(unittest.TestCase):
    BASE_URL = "http://localhost:76123"
    
    def test_api_root(self):
        try:
            res = requests.get(self.BASE_URL)
            self.assertEqual(res.status_code, 200)
        except:
            self.skipTest("Server not running locally on 76123")

if __name__ == '__main__':
    unittest.main()
